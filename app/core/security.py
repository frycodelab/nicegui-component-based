"""Security layer: password hashing, login rate limiting, request middlewares
and session-based authentication/authorization helpers.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui

if TYPE_CHECKING:
    from models.user import User

logger = logging.getLogger(__name__)

# Password hashing (stdlib PBKDF2-HMAC-SHA256)
_PBKDF2_ITERATIONS = 260_000
_SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Return an encoded `pbkdf2_sha256$iterations$salt$hash` string."""
    salt = os.urandom(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, _PBKDF2_ITERATIONS)
    return f'pbkdf2_sha256${_PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}'


def verify_password(password: str, encoded: str) -> bool:
    """Constant-time verification of a password against an encoded hash."""
    try:
        algorithm, iterations, salt_hex, hash_hex = encoded.split('$')
        if algorithm != 'pbkdf2_sha256':
            return False
        expected = bytes.fromhex(hash_hex)
        digest = hashlib.pbkdf2_hmac(
            'sha256', password.encode(), bytes.fromhex(salt_hex), int(iterations)
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(digest, expected)


# Session helpers

def current_user() -> 'User | None':
    """Return the authenticated user (fetched fresh from the DB) or None."""
    if not app.storage.user.get('authenticated', False):
        return None
    username = app.storage.user.get('username')
    if not username:
        return None
    # lazy imports avoid a circular dependency at module load time
    from core.database import get_session
    from services.user_service import UserService
    with get_session() as session:
        return UserService(session).get_user_by_username(username)


def is_admin() -> bool:
    user = current_user()
    return user is not None and user.is_admin


def logout() -> None:
    """Log out the current user and redirect to the login page."""
    uname = app.storage.user.get('username', 'Unknown')
    logger.info(f"User {uname} logged out")
    # Lazy import avoids a circular dependency at module load time.
    from services.audit_service import record as audit_record
    from models.audit import AuditAction
    audit_record(AuditAction.LOGOUT, username=uname, user_id=app.storage.user.get('user_id'))
    app.storage.user.clear()
    ui.run_javascript('window.location.href = "/login"')


# Route access control
unrestricted_page_routes = {'/login', '/health', '/favicon.ico', '/manifest.json', '/sw.js'}

_PUBLIC_ASSET_PREFIXES = (
    '/assets/css/',
    '/assets/images/',
    '/assets/icons/',
    '/assets/fonts/',
)

# Session timeouts
IDLE_TIMEOUT_SECONDS = 30 * 60       # 30 min inactivity
MAX_SESSION_SECONDS = 12 * 60 * 60   # 12 h absolute cap

# In-memory rate limiter
_MAX_ATTEMPTS = 5
_WINDOW_SECONDS = 900    # 15 min sliding window
_LOCKOUT_SECONDS = 1800  # 30 min lockout


@dataclass
class _Attempt:
    timestamp: float
    success: bool


_attempts_by_ip: dict[str, list[_Attempt]] = defaultdict(list)
_lockouts_by_ip: dict[str, float] = {}
_last_cleanup: float = 0.0


def _prune_stale_ips() -> None:
    """Remove IPs with no recent activity to prevent unbounded memory growth."""
    global _last_cleanup
    now = time.time()
    if now - _last_cleanup < 300:  # prune at most every 5 minutes
        return
    _last_cleanup = now
    stale = [ip for ip, attempts in _attempts_by_ip.items()
             if not attempts or now - attempts[-1].timestamp > _WINDOW_SECONDS]
    for ip in stale:
        _attempts_by_ip.pop(ip, None)
    expired_locks = [ip for ip, until in _lockouts_by_ip.items() if now >= until]
    for ip in expired_locks:
        _lockouts_by_ip.pop(ip, None)


def is_locked(ip: str) -> tuple[bool, str]:
    now = time.time()
    if ip in _lockouts_by_ip:
        remaining = int(_lockouts_by_ip[ip] - now)
        if remaining > 0:
            mins, secs = divmod(remaining, 60)
            return True, f"Too many failed attempts. Please wait {mins}m {secs}s."
        del _lockouts_by_ip[ip]
    return False, ""


def record_attempt(ip: str, success: bool) -> tuple[bool, str]:
    """Record a login attempt. Returns (allowed, message)."""
    now = time.time()
    _prune_stale_ips()
    _attempts_by_ip[ip] = [
        a for a in _attempts_by_ip[ip] if now - a.timestamp < _WINDOW_SECONDS
    ]
    _attempts_by_ip[ip].append(_Attempt(timestamp=now, success=success))

    if success:
        _lockouts_by_ip.pop(ip, None)
        return True, ""

    failures = sum(1 for a in _attempts_by_ip[ip] if not a.success)
    remaining = _MAX_ATTEMPTS - failures

    if remaining <= 0:
        _lockouts_by_ip[ip] = now + _LOCKOUT_SECONDS
        logger.warning(f"IP {ip} locked out after {_MAX_ATTEMPTS} failed login attempts")
        return False, "Too many failed attempts. Account locked for 30 minutes."

    if remaining <= 2:
        return True, f"Invalid credentials. {remaining} attempt(s) remaining before lockout."

    return True, "Invalid credentials."


# Middlewares

# Paths the middleware must never block regardless of auth state
_ALWAYS_PASS = ('/_nicegui', '/_starlette')


class AuthMiddleware(BaseHTTPMiddleware):
    """Restricts access to authenticated users and enforces session timeouts."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Fast-path: NiceGUI internal WebSocket/SSE frames never touch storage
        if any(path.startswith(p) for p in _ALWAYS_PASS):
            return await call_next(request)

        is_auth = app.storage.user.get('authenticated', False)
        is_public_asset = any(path.startswith(p) for p in _PUBLIC_ASSET_PREFIXES)

        if is_auth:
            now = time.time()
            last_active = app.storage.user.get('last_activity', now)
            login_at = app.storage.user.get('login_at', now)

            idle_expired = (now - last_active) > IDLE_TIMEOUT_SECONDS
            abs_expired = (now - login_at) > MAX_SESSION_SECONDS

            if idle_expired or abs_expired:
                reason = 'timeout' if idle_expired else 'expired'
                app.storage.user.clear()
                is_auth = False
                if not is_public_asset:
                    if path.startswith('/api/'):
                        return JSONResponse({'error': 'Session expired'}, status_code=401)
                    return RedirectResponse(f'/login?reason={reason}')
            elif not is_public_asset:
                app.storage.user['last_activity'] = now

        if is_auth and not is_public_asset and app.storage.user.get('must_change_password'):
            allowed_paths = {'/change-password'} | unrestricted_page_routes
            if path not in allowed_paths:
                if path.startswith('/api/'):
                    return JSONResponse({'error': 'Password change required'}, status_code=403)
                return RedirectResponse('/change-password')

        if not is_auth and path not in unrestricted_page_routes and not is_public_asset:
            if path.startswith('/api/'):
                return JSONResponse({'error': 'Unauthorized'}, status_code=401)
            return RedirectResponse(f'/login?redirect_to={path}')

        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Injects hardening HTTP response headers."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        h = response.headers
        h.setdefault('X-Content-Type-Options', 'nosniff')
        h.setdefault('X-Frame-Options', 'DENY')
        h.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        h.setdefault('X-XSS-Protection', '0')
        h.setdefault('Permissions-Policy', 'camera=(self), microphone=(), geolocation=()')
        h.setdefault('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        return response

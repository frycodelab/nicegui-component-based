"""Login page — authenticates against the database-backed user store."""

import logging
import time
from pathlib import Path

from fastapi import Request  # noqa: F401  (injected by NiceGUI into page handlers)
from nicegui import app, ui

from core.database import get_session
from core.security import is_locked, record_attempt
from models.audit import AuditAction
from services.audit_service import record as audit_record
from services.user_service import UserService
from components.notifications import notify

logger = logging.getLogger(__name__)

# CSS cached once at import so it is not read from disk per request
_CSS = (Path(__file__).parent.parent / 'assets' / 'css' / 'global-css.css').read_text()


def get_current_year() -> int:
    return time.localtime().tm_year


@ui.page('/login')
async def login_page(request: Request, redirect_to: str = '/', reason: str = '') -> None:
    """Login page — verifies credentials against the users table."""

    # Prevent open redirect
    if not redirect_to.startswith('/') or redirect_to.startswith('//'):
        redirect_to = '/'

    if reason not in ('timeout', 'expired'):
        reason = ''

    if app.storage.user.get('authenticated', False):
        ui.navigate.to(redirect_to)
        return

    # Capture IP at page-load time (HTTP context), not in the click handler
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    client_ip: str = forwarded_for.split(',')[0].strip() if forwarded_for else (
        request.client.host if request.client else 'unknown'
    )

    async def try_login() -> None:
        if not username.value or not password.value:
            notify('Please enter username and password.', type='warning')
            return

        # Rate-limit by IP and by targeted username so neither a single source nor
        # a single account can be brute-forced (username key normalised to lowercase).
        user_key = f"user:{username.value.strip().lower()}"
        for key in (client_ip, user_key):
            locked, lock_msg = is_locked(key)
            if locked:
                notify(lock_msg, type='negative')
                return

        with get_session() as session:
            user = UserService(session).verify_credentials(username.value, password.value)

        if user is None:
            allowed, msg = record_attempt(client_ip, success=False)
            record_attempt(user_key, success=False)
            logger.warning(f"Failed login for '{username.value}' from {client_ip}")
            audit_record(AuditAction.LOGIN_FAILED, username=username.value.strip() or 'unknown',
                         user_id=None, ip=client_ip)
            notify(msg, type='negative')
            return

        if not user.is_active:
            record_attempt(client_ip, success=False)
            record_attempt(user_key, success=False)
            logger.warning(f"Login blocked for disabled account '{user.username}'")
            audit_record(AuditAction.LOGIN_FAILED, username=user.username, user_id=user.id,
                         details='account disabled', ip=client_ip)
            notify('This account is disabled. Please contact an administrator.', type='negative')
            return

        record_attempt(client_ip, success=True)
        record_attempt(user_key, success=True)
        logger.info(f"Login successful for '{user.username}' from {client_ip}")
        now_ts = time.time()
        app.storage.user.update({
            'authenticated': True,
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'must_change_password': user.must_change_password,
            'language': user.language,
            'login_at': now_ts,
            'last_activity': now_ts,
        })
        audit_record(AuditAction.LOGIN, username=user.username, user_id=user.id, ip=client_ip)
        ui.navigate.to('/change-password' if user.must_change_password else redirect_to)

    # Styling
    ui.colors(primary='#18181b', secondary='#f4f4f5', positive='#4caf50',
              negative='#ef4444', warning='#f59e0b', info='#3b82f6', accent='#e4e4e7')

    ui.add_head_html(f'<style>{_CSS}</style>')
    ui.add_head_html('<link rel="stylesheet" href="/assets/css/icons.css">')
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1.0">')

    if reason:
        _msg = (
            'Your session expired due to inactivity. Please log in again.'
            if reason == 'timeout'
            else 'Your session has expired. Please log in again.'
        )
        ui.timer(0.5, lambda m=_msg: notify(m, type='warning', duration=7000), once=True)

    with ui.column().classes('absolute-center items-center gap-2').style(
        'min-height: 70vh; width: 100%; padding: 1rem;'
    ):
        # Logo
        ui.html(
            '<div style="width:15rem;height:7rem;'
            'background-image:url(\'/assets/images/logo.png\');'
            'background-size:contain;background-repeat:no-repeat;'
            'background-position:center;margin-bottom:1rem;"></div>',
            sanitize=False,
        )

        with ui.card().classes('login-card').style('width: 100%; max-width: 450px;'):
            with ui.column().classes('w-full gap-4'):
                ui.label('Demo Login').classes('text-xl font-bold text-center mb-2')

                with ui.column().classes('w-full gap-3'):
                    with ui.element('div').classes('w-full'):
                        ui.label('Username').classes('field-label')
                        username = ui.input(placeholder='').classes('w-full').props('outlined dense')
                        username.on('keydown.enter', try_login)

                    with ui.element('div').classes('w-full'):
                        ui.label('Password').classes('field-label')
                        password = ui.input(
                            password=True, password_toggle_button=True
                        ).classes('w-full').props('outlined dense')
                        password.on('keydown.enter', try_login)

                    ui.button('Sign in', on_click=try_login, color='white') \
                        .props('no-caps') \
                        .classes('button button-primary w-full mt-4')


        ui.label(f'© {get_current_year()} Frycode Lab').classes('text-xs text-muted mt-6')

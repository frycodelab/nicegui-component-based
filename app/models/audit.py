"""Audit log domain model.

A plain data container describing a single recorded action ("who did what").
All persistence lives in :class:`services.audit_service.AuditService`; the model
itself stays free of database dependencies so it can be reused and tested alone.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass


class AuditAction(enum.Enum):
    """Stable identifiers for the actions worth recording in the audit trail.

    The values are stored verbatim in the database, so keep them stable; the UI
    maps each one to a translated label and an icon.
    """

    LOGIN = 'login'
    LOGIN_FAILED = 'login_failed'
    LOGOUT = 'logout'
    PASSWORD_CHANGED = 'password_changed'
    PASSWORD_RESET = 'password_reset'
    USER_CREATED = 'user_created'
    USER_DELETED = 'user_deleted'
    ROLE_CHANGED = 'role_changed'
    USER_ACTIVATED = 'user_activated'
    USER_DEACTIVATED = 'user_deactivated'
    PROFILE_UPDATED = 'profile_updated'
    LANGUAGE_CHANGED = 'language_changed'


@dataclass(frozen=True)
class AuditEntry:
    id: int
    created_at: str
    action: str
    username: str
    user_id: int | None = None
    target: str | None = None
    details: str | None = None
    ip: str | None = None

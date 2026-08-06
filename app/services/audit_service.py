"""Audit service: persistence and queries for the audit trail.

An :class:`AuditService` wraps an open SQLAlchemy session handed out by
:func:`core.database.get_session`, mirroring :class:`services.user_service.UserService`.

For call sites that just want to record an action without managing a session, use
the module-level :func:`record`, which opens its own session, fills in the acting
user from the current session storage and never raises \u2014 auditing must not be able
to break the action it is recording.
"""

from __future__ import annotations

import logging

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from core.database import AuditLogRecord
from models.audit import AuditAction, AuditEntry

logger = logging.getLogger(__name__)


def _record_to_entry(record: AuditLogRecord) -> AuditEntry:
    return AuditEntry(
        id=record.id,
        created_at=record.created_at,
        action=record.action,
        username=record.username,
        user_id=record.user_id,
        target=record.target,
        details=record.details,
        ip=record.ip,
    )


class AuditService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def log(
        self,
        action: AuditAction | str,
        *,
        username: str,
        user_id: int | None = None,
        target: str | None = None,
        details: str | None = None,
        ip: str | None = None,
    ) -> None:
        self.session.add(
            AuditLogRecord(
                action=action.value if isinstance(action, AuditAction) else str(action),
                username=username,
                user_id=user_id,
                target=target,
                details=details,
                ip=ip,
            )
        )

    def get_recent(self, *, limit: int = 100, action: str | None = None) -> list[AuditEntry]:
        query = select(AuditLogRecord).order_by(AuditLogRecord.id.desc())
        if action:
            query = query.where(AuditLogRecord.action == action)
        records = self.session.scalars(query.limit(limit)).all()
        return [_record_to_entry(r) for r in records]

    def count(self) -> int:
        return self.session.scalar(select(func.count()).select_from(AuditLogRecord)) or 0

    def clear(self) -> int:
        """Delete every audit entry; returns the number of rows removed."""
        result = self.session.execute(delete(AuditLogRecord))
        return result.rowcount or 0


def record(
    action: AuditAction | str,
    *,
    username: str | None = None,
    user_id: int | None = None,
    target: str | None = None,
    details: str | None = None,
    ip: str | None = None,
) -> None:
    """Record an audit entry, resolving the actor from session storage by default.

    Safe to call from any UI event or page handler: it swallows and logs any error
    so a failure to audit never propagates into the action being audited.
    """
    # Lazy imports keep the model layer import-time-free of framework/DB deps.
    from nicegui import app

    from core.database import get_session

    try:
        actor_id = user_id
        actor_name = username
        if actor_id is None or actor_name is None:
            try:
                store = app.storage.user
            except Exception:
                store = {}
            if actor_id is None:
                actor_id = store.get('user_id')
            if actor_name is None:
                actor_name = store.get('username')
        actor_name = actor_name or 'system'

        with get_session() as session:
            AuditService(session).log(
                action,
                username=actor_name,
                user_id=actor_id,
                target=target,
                details=details,
                ip=ip,
            )
    except Exception:  # auditing must never break the audited action
        logger.exception('Failed to write audit log entry for action %s', action)

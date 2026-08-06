"""Tests for the audit service against an isolated database via the temp_db fixture."""

from contextlib import contextmanager

from core.database import get_session
from models.audit import AuditAction
from services.audit_service import AuditService


@contextmanager
def service():
    with get_session() as session:
        yield AuditService(session)


def test_log_and_get_recent(temp_db):
    with service() as svc:
        svc.log(AuditAction.LOGIN, username='alice', user_id=1, ip='127.0.0.1')
        svc.log(AuditAction.USER_CREATED, username='alice', user_id=1, target='bob')

    with service() as svc:
        entries = svc.get_recent(limit=10)

    # Most recent first
    assert [e.action for e in entries] == ['user_created', 'login']
    assert entries[0].target == 'bob'
    assert entries[1].ip == '127.0.0.1'


def test_get_recent_filters_by_action(temp_db):
    with service() as svc:
        svc.log(AuditAction.LOGIN, username='alice')
        svc.log(AuditAction.LOGOUT, username='alice')
        svc.log(AuditAction.LOGIN, username='bob')

    with service() as svc:
        logins = svc.get_recent(action='login')

    assert len(logins) == 2
    assert all(e.action == 'login' for e in logins)


def test_count_and_clear(temp_db):
    with service() as svc:
        svc.log(AuditAction.LOGIN, username='alice')
        svc.log(AuditAction.LOGOUT, username='alice')

    with service() as svc:
        assert svc.count() == 2

    with service() as svc:
        removed = svc.clear()

    assert removed == 2
    with service() as svc:
        assert svc.count() == 0


def test_string_action_accepted(temp_db):
    with service() as svc:
        svc.log('custom_action', username='system')

    with service() as svc:
        entries = svc.get_recent()

    assert entries[0].action == 'custom_action'

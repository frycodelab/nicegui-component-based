"""Tests for the user service against an isolated database via the temp_db fixture."""

from contextlib import contextmanager

import pytest

from core.database import get_session
from models.enums import UserRole
from services.user_service import (
    DEFAULT_USER_PASSWORD,
    UserService,
    validate_password,
)


@contextmanager
def service():
    with get_session() as session:
        yield UserService(session)


def test_default_admin_seeded(temp_db):
    with service() as svc:
        admin = svc.get_user_by_username('admin')
    assert admin is not None
    assert admin.is_admin
    assert admin.must_change_password


def test_verify_credentials(temp_db):
    with service() as svc:
        assert svc.verify_credentials('admin', 'admin') is not None
        assert svc.verify_credentials('admin', 'wrong') is None


def test_create_user(temp_db):
    with service() as svc:
        user = svc.create_user('alice')
    assert user.role is UserRole.USER
    assert user.must_change_password
    with service() as svc:
        assert svc.verify_credentials('alice', DEFAULT_USER_PASSWORD) is not None


def test_duplicate_username_rejected(temp_db):
    with service() as svc:
        svc.create_user('alice')
    with pytest.raises(ValueError):
        with service() as svc:
            svc.create_user('alice')


def test_change_password(temp_db):
    with service() as svc:
        uid = svc.create_user('alice').id
    with service() as svc:
        svc.change_password(uid, 'BrandNew1!')
    with service() as svc:
        assert not svc.get_user(uid).must_change_password


def test_password_policy():
    validate_password('BrandNew1!')
    with pytest.raises(ValueError):
        validate_password('weak')


def test_update_profile(temp_db):
    with service() as svc:
        uid = svc.create_user('alice').id
        svc.update_profile(uid, email='alice@example.com', display_name='Alice')
    with service() as svc:
        user = svc.get_user(uid)
    assert user.email == 'alice@example.com'
    assert user.display_name == 'Alice'


def test_protected_admin_cannot_be_deleted(temp_db):
    with service() as svc:
        admin_id = svc.get_user_by_username('admin').id
    with pytest.raises(ValueError):
        with service() as svc:
            svc.delete_user(admin_id)



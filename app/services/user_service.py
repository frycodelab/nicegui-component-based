"""User service: all persistence and business rules for user accounts.

A :class:`UserService` wraps an open SQLAlchemy session handed out by
:func:`core.database.get_session`.  Callers open a session, do their work through
the service and let the ``with`` block commit:

    with get_session() as session:
        UserService(session).create_user('alice')
"""

from __future__ import annotations

import re
import string
import os

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.database import UserRecord
from core.security import hash_password, verify_password
from models.enums import UserRole
from models.user import User

_EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def _is_valid_email(email: str) -> bool:
    return bool(_EMAIL_RE.match(email))

# Password every freshly created / reset account starts with.  Users are forced
# to pick a new one on first login (``must_change_password``).
DEFAULT_USER_PASSWORD = 'changeme'

# Precomputed hash used to equalize verification time for unknown usernames so an
# attacker cannot enumerate valid accounts by measuring the login response time.
_DUMMY_PASSWORD_HASH = hash_password(os.urandom(16).hex())

# Password policy (shared by the service and the change-password UI).
MIN_PASSWORD_LENGTH = 10
MAX_PASSWORD_LENGTH = 64


def password_requirements(password: str) -> list[tuple[str, bool]]:
    """Return ``(i18n_key, satisfied)`` pairs describing the password policy.

    Keys are translated by the UI; server-side validation uses English fallbacks.
    """
    return [
        ('password.req.length',  MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH),
        ('password.req.upper',   any(c.isupper() for c in password)),
        ('password.req.lower',   any(c.islower() for c in password)),
        ('password.req.number',  any(c.isdigit() for c in password)),
        ('password.req.special', any(c in string.punctuation for c in password)),
    ]


# English fallbacks for server-side error messages (UI translates the keys itself).
_REQUIREMENT_LABELS = {
    'password.req.length':  f'{MIN_PASSWORD_LENGTH}\u2013{MAX_PASSWORD_LENGTH} characters',
    'password.req.upper':   'At least one uppercase letter',
    'password.req.lower':   'At least one lowercase letter',
    'password.req.number':  'At least one number',
    'password.req.special': 'At least one special character',
}


def validate_password(password: str) -> None:
    """Raise ``ValueError`` when the password violates the policy."""
    unmet = [_REQUIREMENT_LABELS[key] for key, ok in password_requirements(password) if not ok]
    if unmet:
        raise ValueError('Password requirements not met: ' + '; '.join(unmet) + '.')


# The bootstrap admin can never be deleted, deactivated or demoted.
_PROTECTED_USERNAME = 'admin'


def _record_to_user(record: UserRecord) -> User:
    """Convert an ORM row into the framework-free domain model."""
    return User(
        id=record.id,
        username=record.username,
        role=UserRole(record.role),
        is_active=bool(record.is_active),
        must_change_password=bool(record.must_change_password),
        created_at=record.created_at,
        email=record.email,
        display_name=record.display_name,
        avatar=record.avatar,
        language=record.language or 'en',
    )


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session

    # Queries
    def get_all_users(self) -> list[User]:
        records = self.session.scalars(
            select(UserRecord).order_by(func.lower(UserRecord.username))
        ).all()
        return [_record_to_user(r) for r in records]

    def get_user(self, user_id: int) -> User | None:
        record = self.session.get(UserRecord, user_id)
        return _record_to_user(record) if record else None

    def get_user_by_username(self, username: str) -> User | None:
        record = self._find_by_username(username)
        return _record_to_user(record) if record else None

    def count_admins(self) -> int:
        return self.session.scalar(
            select(func.count())
            .select_from(UserRecord)
            .where(UserRecord.role == UserRole.ADMIN.value, UserRecord.is_active.is_(True))
        ) or 0

    # Authentication
    def verify_credentials(self, username: str, password: str) -> User | None:
        """Return the user when the password matches, otherwise ``None``.

        Activation is not checked here; the caller decides how to treat a
        disabled account so it can show a dedicated message.
        """
        record = self._find_by_username(username)
        if record is None:
            # Verify against a throwaway hash so timing does not reveal that the
            # username is unknown, then fail.
            verify_password(password, _DUMMY_PASSWORD_HASH)
            return None
        if not verify_password(password, record.password_hash):
            return None
        return _record_to_user(record)

    # Mutations
    def create_user(
        self,
        username: str,
        *,
        role: UserRole = UserRole.USER,
        password: str | None = None,
        must_change_password: bool = True,
    ) -> User:
        username = username.strip()
        if not username:
            raise ValueError('Username is required.')
        if password is None:
            password = DEFAULT_USER_PASSWORD
        record = UserRecord(
            username=username,
            password_hash=hash_password(password),
            role=role.value,
            is_active=True,
            must_change_password=must_change_password,
        )
        self.session.add(record)
        try:
            self.session.flush()
        except IntegrityError as exc:
            raise ValueError(f'User "{username}" already exists.') from exc
        return _record_to_user(record)

    def set_role(self, user_id: int, role: UserRole) -> None:
        record = self._require(user_id)
        if record.username == _PROTECTED_USERNAME and role is not UserRole.ADMIN:
            raise ValueError('The default admin must remain an admin.')
        is_admin = record.role == UserRole.ADMIN.value
        if is_admin and role is not UserRole.ADMIN and self.count_admins() <= 1:
            raise ValueError('Cannot demote the last remaining admin.')
        record.role = role.value

    def set_active(self, user_id: int, active: bool) -> None:
        record = self._require(user_id)
        if record.username == _PROTECTED_USERNAME and not active:
            raise ValueError('The default admin cannot be deactivated.')
        is_admin = record.role == UserRole.ADMIN.value
        if is_admin and not active and self.count_admins() <= 1:
            raise ValueError('Cannot deactivate the last active admin.')
        record.is_active = active

    def reset_password(self, user_id: int) -> None:
        """Reset to the default password and force a change on next login."""
        record = self._require(user_id)
        record.password_hash = hash_password(DEFAULT_USER_PASSWORD)
        record.must_change_password = True

    def change_password(self, user_id: int, new_password: str) -> None:
        record = self._require(user_id)
        validate_password(new_password)
        record.password_hash = hash_password(new_password)
        record.must_change_password = False

    def update_profile(self, user_id: int, *, email: str | None,
                       display_name: str | None) -> None:
        record = self._require(user_id)
        email = (email or '').strip() or None
        display_name = (display_name or '').strip() or None
        if email is not None and not _is_valid_email(email):
            raise ValueError('Please enter a valid email address.')
        record.email = email
        record.display_name = display_name

    def set_avatar(self, user_id: int, avatar: str | None) -> None:
        record = self._require(user_id)
        record.avatar = avatar

    def set_language(self, user_id: int, language: str) -> None:
        record = self._require(user_id)
        record.language = language

    def delete_user(self, user_id: int) -> None:
        record = self._require(user_id)
        if record.username == _PROTECTED_USERNAME:
            raise ValueError('The default admin cannot be deleted.')
        self.session.delete(record)

    # Internal
    def _find_by_username(self, username: str) -> UserRecord | None:
        return self.session.scalar(
            select(UserRecord).where(UserRecord.username == username.strip())
        )

    def _require(self, user_id: int) -> UserRecord:
        record = self.session.get(UserRecord, user_id)
        if record is None:
            raise ValueError('User not found.')
        return record

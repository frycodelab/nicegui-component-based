"""Domain enumerations shared across models, services and views."""

from __future__ import annotations

import enum


class UserRole(enum.Enum):
    """Role-based access control levels."""

    ADMIN = 'admin'
    USER = 'user'

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return tuple(member.value for member in cls)

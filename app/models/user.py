"""User domain model.

This is a plain data container.  All persistence and business rules live in
`services.user_service.UserService`; the model itself stays free of database or
security dependencies so it can be reused and tested in isolation.
"""

from __future__ import annotations

from dataclasses import dataclass

from models.enums import UserRole


@dataclass(frozen=True)
class User:
    id: int
    username: str
    role: UserRole
    is_active: bool
    must_change_password: bool
    created_at: str
    email: str | None = None
    display_name: str | None = None
    avatar: str | None = None
    language: str = 'en'

    @property
    def is_admin(self) -> bool:
        return self.role is UserRole.ADMIN

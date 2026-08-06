"""Example UI smoke tests using NiceGUI's user-simulation harness."""

import pytest

pytest.importorskip('nicegui.testing')

from nicegui import ui
from nicegui.testing import User


async def test_app_requires_login(user: User) -> None:
    await user.open('/')
    await user.should_see('Demo Login')


async def test_login_page_renders(user: User) -> None:
    await user.open('/login')
    await user.should_see('Sign in')


async def test_admin_login_forces_password_change(user: User, temp_db) -> None:
    await user.open('/login')
    user.find(ui.input).type('admin')  # both username and password inputs receive 'admin'
    user.find('Sign in').click()
    await user.should_see('Set a new password')

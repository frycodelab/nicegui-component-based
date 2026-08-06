"""Forced password change page.

Shown right after login when the account still has ``must_change_password`` set
(freshly created accounts and password resets).  Until the password is changed,
:class:`core.security.AuthMiddleware` redirects every other page here.
"""

import logging
from pathlib import Path

from nicegui import app, ui

from components.notifications import notify
from components.password_form import PasswordChangeForm
from core.database import get_session
from models.audit import AuditAction
from services.audit_service import record as audit_record
from services.user_service import UserService

logger = logging.getLogger(__name__)

_CSS = (Path(__file__).parent.parent / 'assets' / 'css' / 'global-css.css').read_text()


@ui.page('/change-password')
async def change_password_page() -> None:
    if not app.storage.user.get('authenticated', False):
        ui.navigate.to('/login')
        return

    user_id = app.storage.user.get('user_id')

    async def submit() -> None:
        if not form.is_valid():
            notify('Password does not meet the requirements.', type='warning')
            return
        if user_id is None:
            ui.navigate.to('/login')
            return
        try:
            with get_session() as session:
                UserService(session).change_password(user_id, form.new_pw.value)
        except ValueError as exc:
            notify(str(exc), type='negative')
            return
        app.storage.user['must_change_password'] = False
        logger.info(f"Password changed for user_id={user_id}")
        audit_record(AuditAction.PASSWORD_CHANGED, user_id=user_id)
        notify('Password updated.', type='positive')
        ui.navigate.to('/')

    # Styling
    ui.colors(primary='#18181b', secondary='#f4f4f5', positive='#4caf50',
              negative='#ef4444', warning='#f59e0b', info='#3b82f6', accent='#e4e4e7')
    ui.add_head_html(f'<style>{_CSS}</style>')
    ui.add_head_html('<link rel="stylesheet" href="/assets/css/icons.css">')
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1.0">')

    with ui.column().classes('absolute-center items-center gap-2').style(
        'min-height: 70vh; width: 100%; padding: 1rem;'
    ):
        with ui.card().classes('login-card').style('width: 100%; max-width: 450px;'):
            with ui.column().classes('w-full gap-4'):
                ui.label('Set a new password').classes('text-xl font-bold text-center mb-2')
                ui.label('You must choose a new password before continuing.') \
                    .classes('text-xs text-muted text-center')

                with ui.column().classes('w-full gap-3'):
                    def _sync_button() -> None:
                        (save_btn.enable if form.is_valid() else save_btn.disable)()

                    form = PasswordChangeForm(on_change=_sync_button, on_submit=submit)

                    save_btn = ui.button('Save password', on_click=submit, color='white') \
                        .props('no-caps').classes('button button-primary w-full mt-4')
                    save_btn.disable()

"""Account settings page: profile, avatar, language and password management."""

from __future__ import annotations

import base64
import logging

from nicegui import app, ui

from components.notifications import notify
from components.dropzone import dropzone
from components.password_form import PasswordChangeForm
from core.database import get_session
from core.security import current_user
from models.audit import AuditAction
from services import i18n
from services.audit_service import record as audit_record
from services.i18n import LANGUAGES, current_language, set_language, t
from services.user_service import UserService

logger = logging.getLogger(__name__)

_MAX_AVATAR_BYTES = 2_000_000


def content() -> None:
    user = current_user()
    if user is None:
        ui.navigate.to('/login')
        return

    user_id = user.id

    # Page header with language selector top-right
    with ui.row().classes('w-full items-start justify-between gap-4 mt-4 mb-2 no-wrap'):
        with ui.column().classes('gap-1 min-w-0'):
            i18n.bind(ui.label(t('settings.title')).classes('page-title'), 'settings.title')
            i18n.bind(ui.label(t('settings.subtitle')).classes('text-sm text-muted'), 'settings.subtitle')

        def _on_language(e) -> None:
            set_language(e.value)
            audit_record(AuditAction.LANGUAGE_CHANGED, details=e.value)
            notify(t('settings.language_saved'), type='positive')

        with ui.column().classes('gap-1 items-end flex-shrink-0').style('min-width: 200px;'):
            i18n.bind(ui.label(t('language.label')).classes('field-label').style('margin-bottom: 0;'),
                      'language.label')
            ui.select(options=LANGUAGES, value=current_language(), on_change=_on_language) \
                .props('outlined dense').classes('w-full')
    ui.element('div').classes('divider mb-4')

    # Profile & security, side by side
    with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-6 w-full items-start'):

        # Profile & avatar
        with ui.element('div').classes('card w-full'):
            with ui.column().classes('gap-1 w-full'):
                i18n.bind(ui.label(t('settings.profile')).classes('card-title'), 'settings.profile')
                i18n.bind(ui.label(t('settings.profile_desc')).classes('card-description'), 'settings.profile_desc')

            @ui.refreshable
            def avatar_view() -> None:
                u = current_user()
                if u and u.avatar:
                    ui.image(u.avatar).style(
                        'width: 88px; height: 88px; border-radius: 9999px; object-fit: cover;'
                    )
                else:
                    initial = ((u.display_name or u.username)[:1].upper()) if u else '?'
                    with ui.element('div').classes(
                        'flex items-center justify-center rounded-full'
                    ).style(
                        'width: 88px; height: 88px; background: var(--secondary); color: var(--fg); '
                        'font-weight: 600; font-size: 1.75rem; flex-shrink: 0;'
                    ):
                        ui.label(initial)

            async def _on_upload(e) -> None:
                raw = e.content.read()
                if len(raw) > _MAX_AVATAR_BYTES:
                    notify(t('settings.image_too_large'), type='negative')
                    return
                mime = getattr(e, 'type', None) or 'image/png'
                data_url = f'data:{mime};base64,' + base64.b64encode(raw).decode()
                with get_session() as session:
                    UserService(session).set_avatar(user_id, data_url)
                avatar_view.refresh()
                notify(t('settings.saved'), type='positive')

            def _remove_avatar() -> None:
                with get_session() as session:
                    UserService(session).set_avatar(user_id, None)
                avatar_view.refresh()

            with ui.row().classes('items-start gap-5 w-full no-wrap mt-4'):
                with ui.column().classes('items-center gap-2 flex-shrink-0'):
                    avatar_view()
                    i18n.bind(
                        ui.button(t('settings.remove_photo'), icon='delete', on_click=_remove_avatar)
                        .props('flat no-caps').classes('button button-ghost button-sm'),
                        'settings.remove_photo',
                    )
                with ui.column().classes('flex-1 min-w-0 gap-0'):
                    dropzone(on_upload=_on_upload, max_file_size=_MAX_AVATAR_BYTES,
                             accept='image/*')

            ui.element('div').classes('divider')

            with ui.element('div').classes('w-full'):
                i18n.bind(ui.label(t('settings.username')).classes('field-label'), 'settings.username')
                ui.input(value=user.username).props('outlined dense readonly').classes('w-full')

            with ui.element('div').classes('w-full mt-4'):
                i18n.bind(ui.label(t('settings.display_name')).classes('field-label'), 'settings.display_name')
                display_name = ui.input(value=user.display_name or '') \
                    .props('outlined dense').classes('w-full')

            with ui.element('div').classes('w-full mt-4'):
                i18n.bind(ui.label(t('settings.email')).classes('field-label'), 'settings.email')
                email = ui.input(value=user.email or '') \
                    .props('outlined dense type=email').classes('w-full')

            def _save_profile() -> None:
                try:
                    with get_session() as session:
                        UserService(session).update_profile(
                            user_id, email=email.value, display_name=display_name.value
                        )
                except ValueError as exc:
                    notify(str(exc), type='negative')
                    return
                audit_record(AuditAction.PROFILE_UPDATED)
                notify(t('settings.saved'), type='positive')

            with ui.element('div').classes('card-footer justify-end'):
                i18n.bind(
                    ui.button(t('settings.save'), icon='save', on_click=_save_profile)
                    .props('no-caps').classes('button button-primary'),
                    'settings.save',
                )

        # Security (password change)
        with ui.element('div').classes('card w-full'):
            with ui.column().classes('gap-1 w-full'):
                i18n.bind(ui.label(t('settings.security')).classes('card-title'), 'settings.security')
                i18n.bind(ui.label(t('settings.security_desc')).classes('card-description'), 'settings.security_desc')

            def _sync_button() -> None:
                (update_btn.enable if form.is_valid() else update_btn.disable)()

            async def _update_password() -> None:
                if not form.is_valid():
                    notify(t('settings.password_not_met'), type='warning')
                    return
                try:
                    with get_session() as session:
                        UserService(session).change_password(user_id, form.new_pw.value)
                except ValueError as exc:
                    notify(str(exc), type='negative')
                    return
                app.storage.user['must_change_password'] = False
                form.reset()
                update_btn.disable()
                audit_record(AuditAction.PASSWORD_CHANGED)
                notify(t('settings.password_updated'), type='positive')

            with ui.column().classes('w-full mt-2'):
                form = PasswordChangeForm(
                    new_label=t('settings.new_password'),
                    confirm_label=t('settings.confirm_password'),
                    on_change=_sync_button,
                    on_submit=_update_password,
                )

            with ui.element('div').classes('card-footer justify-end'):
                update_btn = i18n.bind(
                    ui.button(t('settings.update_password'), icon='lock_reset',
                              on_click=_update_password)
                    .props('no-caps').classes('button button-primary'),
                    'settings.update_password',
                )
                update_btn.disable()

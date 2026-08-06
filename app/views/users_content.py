"""Users administration page: create, delete, toggle roles and reset passwords.

Admin-only.  All persistence goes through :class:`services.user_service.UserService`;
this view only orchestrates the UI and delegates every mutation to the service.
"""

from __future__ import annotations

from nicegui import app, ui

from components.dialogs import confirm_dialog, info_dialog
from components.notifications import notify
from core.database import get_session
from models.audit import AuditAction
from models.enums import UserRole
from services.audit_service import record as audit_record
from services.i18n import t
from services.user_service import DEFAULT_USER_PASSWORD, UserService
from views._common import page_header

# The bootstrap admin is protected: it can never be deleted or disabled.
_PROTECTED_USERNAME = 'admin'

# Icons are classic Material Icons (Quasar's bundled set).
_ROLE_BADGE = {
    UserRole.ADMIN.value: ('badge badge-warning', 'admin_panel_settings'),
    UserRole.USER.value: ('badge badge-default', 'person'),
}


def _is_admin() -> bool:
    return app.storage.user.get('role') == UserRole.ADMIN.value


def content() -> None:
    page_header(t('users.title'), t('users.subtitle'))

    if not _is_admin():
        with ui.column().classes('card w-full items-center gap-2 p-8'):
            ui.icon('lock', size='2rem').classes('text-muted')
            ui.label(t('users.access_denied')).classes('section-title')
            ui.label(t('users.admin_only')).classes('text-muted')
        return

    current_username = app.storage.user.get('username', '')

    @ui.refreshable
    def user_table() -> None:
        with get_session() as session:
            users = [
                {
                    'id': u.id,
                    'username': u.username,
                    'role': u.role.value,
                    'is_active': u.is_active,
                    'must_change_password': u.must_change_password,
                }
                for u in UserService(session).get_all_users()
            ]

        with ui.column().classes('card w-full gap-0 p-0'):
            # Header row
            with ui.row().classes('w-full items-center px-4 py-3 label-text').style(
                'border-bottom: 1px solid var(--border, #e4e4e7);'
            ):
                ui.label(t('users.col.user')).classes('flex-1')
                ui.label(t('users.col.role')).style('width: 120px;')
                ui.label(t('users.col.status')).style('width: 120px;')
                ui.label(t('users.col.actions')).style('width: 180px;')

            for u in users:
                is_self = u['username'] == current_username
                is_protected = u['username'] == _PROTECTED_USERNAME
                badge_cls, badge_icon = _ROLE_BADGE.get(u['role'], _ROLE_BADGE[UserRole.USER.value])

                with ui.row().classes('w-full items-center px-4 py-3').style(
                    'border-bottom: 1px solid var(--border, #f4f4f5);'
                ):
                    # User
                    with ui.row().classes('flex-1 items-center gap-3 min-w-0'):
                        with ui.element('div').classes(
                            'flex items-center justify-center rounded-full'
                        ).style(
                            'width: 32px; height: 32px; background: #f4f4f5; '
                            'color: #18181b; font-weight: 600; flex-shrink: 0;'
                        ):
                            ui.label(u['username'][:1].upper())
                        with ui.column().classes('gap-0 min-w-0'):
                            ui.label(u['username']).classes('truncate').style('font-weight: 500;')
                            if u['must_change_password']:
                                ui.label(t('users.pw_pending')).classes('text-xs text-muted')

                    # Role
                    with ui.element('div').style('width: 120px;'):
                        with ui.element('span').classes(badge_cls).style('gap: 4px;'):
                            ui.icon(badge_icon, size='0.9rem')
                            ui.label(t('users.role.admin') if u['role'] == UserRole.ADMIN.value else t('users.role.user'))

                    # Status
                    with ui.element('div').style('width: 120px;'):
                        if u['is_active']:
                            with ui.element('span').classes('badge badge-success'):
                                ui.label(t('status.active'))
                        else:
                            with ui.element('span').classes('badge badge-default'):
                                ui.label(t('status.inactive'))

                    # Actions
                    with ui.row().classes('items-center gap-1').style('width: 180px;'):
                        ui.button(icon='lock_reset', on_click=lambda _, uid=u['id']: _reset(uid)) \
                            .props('flat dense round').tooltip(t('users.tip.reset'))

                        role_btn = ui.button(
                            icon='swap_horiz', on_click=lambda _, uid=u['id']: _toggle_role(uid)
                        ).props('flat dense round').tooltip(t('users.tip.switch_role'))

                        active_icon = 'block' if u['is_active'] else 'check_circle'
                        active_btn = ui.button(
                            icon=active_icon, on_click=lambda _, uid=u['id']: _toggle_active(uid)
                        ).props('flat dense round').tooltip(
                            t('users.tip.deactivate') if u['is_active'] else t('users.tip.activate')
                        )

                        delete_btn = ui.button(
                            icon='delete',
                            on_click=lambda _, uid=u['id'], name=u['username']: _delete(uid, name),
                        ).props('flat dense round color=negative').tooltip(t('users.tip.delete'))

                        if is_protected or is_self:
                            active_btn.disable()
                            delete_btn.disable()
                        if is_protected:
                            role_btn.disable()

    # Action handlers
    async def _reset(uid: int) -> None:
        try:
            with get_session() as session:
                service = UserService(session)
                target = service.get_user(uid)
                service.reset_password(uid)
        except ValueError as exc:
            await info_dialog(str(exc), title=t('users.not_possible'), danger=True)
            return
        audit_record(AuditAction.PASSWORD_RESET, target=target.username if target else str(uid))
        notify(t('users.pw_reset').format(pw=DEFAULT_USER_PASSWORD), type='positive')
        user_table.refresh()

    async def _toggle_role(uid: int) -> None:
        try:
            with get_session() as session:
                service = UserService(session)
                user = service.get_user(uid)
                if user is None:
                    return
                new_role = UserRole.USER if user.is_admin else UserRole.ADMIN
                service.set_role(uid, new_role)
        except ValueError as exc:
            await info_dialog(str(exc), title=t('users.not_possible'), danger=True)
            return
        audit_record(AuditAction.ROLE_CHANGED, target=user.username, details=new_role.value)
        user_table.refresh()

    async def _toggle_active(uid: int) -> None:
        try:
            with get_session() as session:
                service = UserService(session)
                user = service.get_user(uid)
                if user is None:
                    return
                service.set_active(uid, not user.is_active)
        except ValueError as exc:
            await info_dialog(str(exc), title=t('users.not_possible'), danger=True)
            return
        activated = not user.is_active
        audit_record(
            AuditAction.USER_ACTIVATED if activated else AuditAction.USER_DEACTIVATED,
            target=user.username,
        )
        user_table.refresh()

    async def _delete(uid: int, name: str) -> None:
        confirmed = await confirm_dialog(
            t('users.delete_confirm').format(name=name),
            title=t('users.delete_title'),
            confirm_text=t('common.delete'),
            danger=True,
        )
        if not confirmed:
            return
        try:
            with get_session() as session:
                UserService(session).delete_user(uid)
        except ValueError as exc:
            await info_dialog(str(exc), title=t('users.not_possible'), danger=True)
            return
        audit_record(AuditAction.USER_DELETED, target=name)
        notify(t('users.deleted').format(name=name), type='warning')
        user_table.refresh()

    # Create dialog
    def _open_create_dialog() -> None:
        with ui.dialog() as dialog, ui.column().classes('login-card gap-4'):
            ui.label(t('users.create_new')).classes('section-title')
            username = ui.input(t('users.col.user')).props('outlined dense').classes('w-full')
            role = ui.select(
                options={UserRole.USER.value: t('users.role.user'), UserRole.ADMIN.value: t('users.role.admin')},
                value=UserRole.USER.value,
                label=t('users.col.role'),
            ).props('outlined dense').classes('w-full')
            ui.label(
                t('users.initial_pw').format(pw=DEFAULT_USER_PASSWORD)
            ).classes('text-xs text-muted')

            async def create() -> None:
                name = (username.value or '').strip()
                if not name:
                    notify(t('users.enter_username'), type='warning')
                    return
                try:
                    with get_session() as session:
                        service = UserService(session)
                        if service.get_user_by_username(name) is not None:
                            notify(t('users.exists').format(name=name), type='negative')
                            return
                        service.create_user(name, role=UserRole(role.value))
                except ValueError as exc:
                    notify(str(exc), type='negative')
                    return
                audit_record(AuditAction.USER_CREATED, target=name, details=role.value)
                notify(t('users.created').format(name=name), type='positive')
                dialog.close()
                user_table.refresh()

            with ui.row().classes('w-full justify-end gap-2'):
                ui.button(t('common.cancel'), on_click=dialog.close).classes('button button-secondary')
                ui.button(t('common.create'), on_click=create).classes('button button-primary')

        dialog.open()

    with ui.row().classes('w-full justify-end mb-3'):
        ui.button(t('users.create'), icon='person_add', on_click=_open_create_dialog) \
            .classes('button button-primary')

    user_table()

"""Audit log page: a chronological view of who did what across the app.

Admin-only.  All persistence goes through :class:`services.audit_service.AuditService`;
this view only orchestrates the UI and delegates every query to the service.
"""

from __future__ import annotations

from nicegui import app, ui

from components.dialogs import confirm_dialog, info_dialog
from components.notifications import notify
from core.database import get_session
from models.audit import AuditAction
from models.enums import UserRole
from services.audit_service import AuditService
from services.i18n import t
from views._common import page_header

# action value -> (Material icon, badge class) for the activity list.
_ACTION_META: dict[str, tuple[str, str]] = {
    AuditAction.LOGIN.value:            ('login', 'badge badge-success'),
    AuditAction.LOGIN_FAILED.value:     ('gpp_bad', 'badge badge-danger'),
    AuditAction.LOGOUT.value:           ('logout', 'badge badge-default'),
    AuditAction.PASSWORD_CHANGED.value: ('password', 'badge badge-info'),
    AuditAction.PASSWORD_RESET.value:   ('lock_reset', 'badge badge-warning'),
    AuditAction.USER_CREATED.value:     ('person_add', 'badge badge-success'),
    AuditAction.USER_DELETED.value:     ('person_remove', 'badge badge-danger'),
    AuditAction.ROLE_CHANGED.value:     ('swap_horiz', 'badge badge-info'),
    AuditAction.USER_ACTIVATED.value:   ('check_circle', 'badge badge-success'),
    AuditAction.USER_DEACTIVATED.value: ('block', 'badge badge-warning'),
    AuditAction.PROFILE_UPDATED.value:  ('manage_accounts', 'badge badge-info'),
    AuditAction.LANGUAGE_CHANGED.value: ('language', 'badge badge-default'),
}

_DEFAULT_META = ('history', 'badge badge-default')

# How many rows the list shows at once.
_LIMIT = 200


def _is_admin() -> bool:
    return app.storage.user.get('role') == UserRole.ADMIN.value


def _action_label(action: str) -> str:
    return t(f'audit.action.{action}')


def content() -> None:
    page_header(t('audit.title'), t('audit.subtitle'))

    if not _is_admin():
        with ui.column().classes('card w-full items-center gap-2 p-8'):
            ui.icon('lock', size='2rem').classes('text-muted')
            ui.label(t('audit.admin_only')).classes('text-muted')
        return

    # Filter state: '' means all actions.
    state = {'action': ''}

    @ui.refreshable
    def audit_table() -> None:
        with get_session() as session:
            service = AuditService(session)
            total = service.count()
            entries = [
                {
                    'created_at': e.created_at,
                    'action': e.action,
                    'username': e.username,
                    'target': e.target,
                    'details': e.details,
                    'ip': e.ip,
                }
                for e in service.get_recent(limit=_LIMIT, action=state['action'] or None)
            ]

        ui.label(t('audit.showing').format(shown=len(entries), total=total)) \
            .classes('text-xs text-muted mb-2')

        if not entries:
            with ui.column().classes('card w-full items-center gap-2 p-8'):
                ui.icon('history', size='2rem').classes('text-muted')
                ui.label(t('audit.empty')).classes('text-muted')
            return

        with ui.column().classes('card w-full gap-0 p-0'):
            # Header row
            with ui.row().classes('w-full items-center px-4 py-3 label-text').style(
                'border-bottom: 1px solid var(--border, #e4e4e7);'
            ):
                ui.label(t('audit.col.time')).style('width: 170px;')
                ui.label(t('audit.col.user')).style('width: 160px;')
                ui.label(t('audit.col.action')).style('width: 190px;')
                ui.label(t('audit.col.details')).classes('flex-1')
                ui.label(t('audit.col.ip')).style('width: 130px;')

            for e in entries:
                icon, badge_cls = _ACTION_META.get(e['action'], _DEFAULT_META)
                detail_parts = [p for p in (e['target'], e['details']) if p]
                detail_text = ' · '.join(detail_parts)

                with ui.row().classes('w-full items-center px-4 py-3 no-wrap').style(
                    'border-bottom: 1px solid var(--border, #f4f4f5);'
                ):
                    ui.label(e['created_at']).style(
                        'width: 170px; font-family: monospace;'
                    ).classes('text-xs text-muted')

                    ui.label(e['username']).style('width: 160px;').classes('truncate')

                    with ui.element('div').style('width: 190px;'):
                        with ui.element('span').classes(badge_cls).style('gap: 4px;'):
                            ui.icon(icon, size='0.9rem')
                            ui.label(_action_label(e['action']))

                    ui.label(detail_text or '—').classes('flex-1 truncate text-sm')

                    ui.label(e['ip'] or '—').style(
                        'width: 130px; font-family: monospace;'
                    ).classes('text-xs text-muted')

    # Action handlers
    def _on_filter(e) -> None:
        state['action'] = e.value or ''
        audit_table.refresh()

    async def _clear() -> None:
        confirmed = await confirm_dialog(
            t('audit.clear_confirm'),
            title=t('audit.clear_title'),
            confirm_text=t('audit.clear'),
            danger=True,
        )
        if not confirmed:
            return
        try:
            with get_session() as session:
                removed = AuditService(session).clear()
        except Exception as exc:  # noqa: BLE001  surfaced to the admin
            await info_dialog(str(exc), title=t('audit.clear_title'), danger=True)
            return
        notify(t('audit.cleared').format(n=removed), type='warning')
        audit_table.refresh()

    # Toolbar: action filter, refresh, clear
    filter_options = {'': t('audit.filter.all')}
    filter_options.update({a.value: _action_label(a.value) for a in AuditAction})

    with ui.row().classes('w-full items-center justify-between gap-2 mb-3 no-wrap'):
        ui.select(options=filter_options, value='', on_change=_on_filter) \
            .props('outlined dense').classes('flex-1').style('max-width: 260px;')
        with ui.row().classes('items-center gap-2'):
            ui.button(t('common.refresh'), icon='refresh', on_click=lambda: audit_table.refresh()) \
                .props('flat no-caps').classes('button button-secondary')
            ui.button(t('audit.clear'), icon='delete_sweep', on_click=_clear) \
                .props('flat no-caps color=negative').classes('button button-ghost')

    audit_table()

"""Admin-only application settings page for logging configuration.

The log level is applied live across the whole application and persisted so it
survives restarts.  Log records are written to a rolling file in the ``logs/``
folder (see :mod:`core.logging_config`).
"""

from nicegui import app, ui

from components.notifications import notify
from core.logging_config import LOG_FILE, LOG_LEVELS, get_log_level, set_log_level
from models.enums import UserRole
from services.i18n import t
from views._common import page_header


def _is_admin() -> bool:
    return app.storage.user.get('role') == UserRole.ADMIN.value


def content() -> None:
    page_header(t('appsettings.title'), t('appsettings.subtitle'))

    if not _is_admin():
        with ui.column().classes('card w-full items-center gap-2 p-8'):
            ui.icon('lock', size='2rem').classes('text-muted')
            ui.label(t('appsettings.admin_only')).classes('text-muted')
        return

    def _on_level_change(e) -> None:
        if set_log_level(e.value):
            notify(t('appsettings.level_saved').format(level=e.value), type='positive')

    with ui.column().classes('card w-full gap-1 p-6').style('max-width: 640px;'):
        with ui.row().classes('items-center gap-2'):
            ui.icon('article', size='sm').classes('text-muted')
            ui.label(t('appsettings.logging')).classes('card-title')
        ui.label(t('appsettings.logging_desc')).classes('card-description mb-4')

        with ui.element('div').classes('w-full'):
            ui.label(t('appsettings.log_level')).classes('field-label')
            ui.select(
                LOG_LEVELS,
                value=get_log_level(),
                on_change=_on_level_change,
            ).props('outlined dense').classes('w-full').style('max-width: 260px;')

        with ui.row().classes('items-center gap-2 mt-4'):
            ui.label(f"{t('appsettings.log_file')}:").classes('text-sm text-muted')
            ui.label(str(LOG_FILE)).classes('text-sm').style('font-family: monospace;')

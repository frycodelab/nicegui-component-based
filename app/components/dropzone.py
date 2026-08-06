"""Reusable drag & drop upload zone styled to match the design system.

Wraps Quasar's uploader (via :func:`ui.upload`) so a file can be dropped on the
zone or selected by clicking it, entirely in Python. The visual (icon, title,
hint) is rendered underneath a transparent, full-cover uploader that captures
both clicks and native file drops.
"""

from __future__ import annotations

from typing import Callable

from nicegui import ui

from services import i18n


def dropzone(
    *,
    on_upload: Callable,
    max_file_size: int,
    accept: str = 'image/*',
    icon: str = 'cloud_upload',
    title_key: str = 'dropzone.title',
    hint_key: str = 'dropzone.hint',
) -> ui.upload:
    """Render a design-system dropzone and return the underlying ``ui.upload``.

    ``on_upload`` receives the standard NiceGUI upload event (``auto_upload``).
    """
    with ui.element('div').classes('dropzone'):
        with ui.column().classes('dropzone__content'):
            ui.icon(icon).classes('dropzone__icon')
            i18n.bind(ui.label().classes('dropzone__title'), title_key)
            i18n.bind(ui.label().classes('dropzone__hint'), hint_key)
        upload = ui.upload(on_upload=on_upload, auto_upload=True, max_file_size=max_file_size)
        upload.props(f'accept="{accept}" flat').classes('dropzone__input')
    return upload

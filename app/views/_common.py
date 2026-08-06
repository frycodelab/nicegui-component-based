"""Shared view building blocks used across the different content pages."""

from __future__ import annotations

from nicegui import ui


def page_header(title: str, subtitle: str | None = None) -> None:
    """Render a consistent page title, optional subtitle and a divider."""
    with ui.column().classes('w-full gap-1 mt-4 mb-2'):
        ui.label(title).classes('page-title')
        if subtitle:
            ui.label(subtitle).classes('text-sm text-muted')
    ui.element('div').classes('divider mb-4')

"""Settings page — stub for user and application configuration."""

from nicegui import ui


def content() -> None:
    ui.label('Welcome to the Settings').style('font-size: 1.5rem; font-weight: 400;').classes('w-full text-center')

    with ui.row().classes('w-full justify-left'):
        ui.icon('settings', size='md')
        ui.label('Settings').style('font-size: 1.0rem; font-weight: 500;').classes('mt-1')
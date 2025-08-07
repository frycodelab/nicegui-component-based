from nicegui import ui, app

def content() -> None:
    with ui.row().classes('w-full'):
            ui.icon('settings', size='md').classes('')
            ui.label('Settings').style('font-size: 1.0rem; font-weight: 500;').classes('mt-1')
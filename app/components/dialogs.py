"""Reusable modal dialogs: confirmation and info modals with a consistent look.

Usage:
    from components.dialogs import confirm_dialog, info_dialog

    if await confirm_dialog('Delete this item?', title='Delete', danger=True):
        ...  # user pressed the confirm button

    await info_dialog('This action is not allowed.', title='Not possible')
"""

from nicegui import ui


async def confirm_dialog(
    message: str,
    *,
    title: str = 'Please confirm',
    confirm_text: str = 'Yes',
    cancel_text: str = 'Cancel',
    icon: str = 'help',
    danger: bool = False,
) -> bool:
    """Show a Yes/Cancel modal and return True when the user confirms."""
    with ui.dialog() as dialog, ui.card().classes('dialog-card'):
        with ui.row().classes('items-center gap-3 mb-1 no-wrap'):
            ui.icon(icon).classes('text-danger' if danger else 'text-info').style('font-size: 1.6rem;')
            ui.label(title).classes('dialog-title').style('margin-bottom: 0 !important;')
        ui.label(message).classes('dialog-body')
        with ui.element('div').classes('dialog-footer'):
            ui.button(cancel_text, on_click=lambda: dialog.submit(False), color='white') \
                .props('flat no-caps').classes('button button-secondary button-sm')
            ui.button(confirm_text, on_click=lambda: dialog.submit(True), color='white') \
                .props('flat no-caps') \
                .classes(f'button button-sm {"button-danger" if danger else "button-primary"}')
    return bool(await dialog)


async def info_dialog(
    message: str,
    *,
    title: str = 'Notice',
    ok_text: str = 'Got it',
    icon: str = 'info',
    danger: bool = False,
) -> None:
    """Show an informational modal with a single acknowledge button."""
    with ui.dialog() as dialog, ui.card().classes('dialog-card'):
        with ui.row().classes('items-center gap-3 mb-1 no-wrap'):
            ui.icon(icon).classes('text-danger' if danger else 'text-info').style('font-size: 1.6rem;')
            ui.label(title).classes('dialog-title').style('margin-bottom: 0 !important;')
        ui.label(message).classes('dialog-body')
        with ui.element('div').classes('dialog-footer'):
            ui.button(ok_text, on_click=lambda: dialog.submit(True), color='white') \
                .props('flat no-caps').classes('button button-primary button-sm')
    await dialog

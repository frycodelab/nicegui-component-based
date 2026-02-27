import logging

logger = logging.getLogger(__name__)

from nicegui import ui

from services.notifications import notify

from database.db import AsyncSessionLocal
from database.crud import (
    get_orders,
    create_order,
    delete_order
)

def _delete_confirmation_dialog(selected_rows, delete_func):
    """display confirmation modal before delete with details of rows"""
    with ui.dialog(value=True) as dlg, ui.card().style('min-width:500px;padding:28px 32px'):
        with ui.row().classes('w-full mb-4'):
            ui.label('Delete Order(s)?').classes('dialog-title text-danger')
        ui.label(f'This will permanently delete {len(selected_rows)} order(s):').classes('text-sm font-semi mb-3')
        
        # show table preview of rows to delete
        with ui.element('table').classes('data-table w-full').style('max-height:200px;overflow-y:auto;'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in ['ID', 'Customer', 'Product', 'Qty']:
                        with ui.element('th'): ui.label(col).classes('text-xs')
            with ui.element('tbody'):
                for row in selected_rows:
                    with ui.element('tr'):
                        with ui.element('td'): ui.label(str(row['id'])).classes('text-xs')
                        with ui.element('td'): ui.label(row['customer_name']).classes('text-xs')
                        with ui.element('td'): ui.label(row['product']).classes('text-xs')
                        with ui.element('td'): ui.label(str(row['quantity'])).classes('text-xs')
        
        ui.separator().classes('mb-4')
        with ui.row().classes('gap-3 justify-end w-full mt-4'):
            ui.button('Cancel', color='white', on_click=dlg.close).props('flat no-caps').classes('button button-outline button-sm')
            async def confirm_delete():
                await delete_func(selected_rows)
                dlg.close()
            ui.button('Delete', color='white', on_click=confirm_delete).props('flat no-caps').classes('button button-danger button-sm')
    return dlg


def _new_order_dialog(refresh_func):
    """display dialog to input and create a new order"""
    with ui.dialog() as dlg, ui.card().style('min-width:380px;padding:28px 32px'):
        with ui.row().classes('items-center justify-between w-full mb-4'):
            ui.label('New Order').classes('card-title')
            ui.button(icon='close', color='white', on_click=dlg.close).props('flat round dense').classes('button button-ghost')
        
        with ui.column().classes('gap-4 w-full'):
            with ui.element('div').classes('w-full'):
                ui.label('Customer').classes('field-label')
                sel_customer = ui.input(placeholder='Customer name').classes('w-full').props('outlined dense')
            with ui.element('div').classes('w-full'):
                ui.label('Product').classes('field-label')
                sel_product = ui.input(placeholder='Product name').classes('w-full').props('outlined dense')
            with ui.element('div').classes('w-full'):
                ui.label('Quantity').classes('field-label')
                sel_qty = ui.number(value=1, min=1).classes('w-full').props('outlined dense')

        ui.separator().classes('mb-4')
        with ui.row().classes('gap-3 justify-end w-full'):
            ui.button('Cancel', color='white', on_click=dlg.close).props('flat no-caps').classes('button button-outline button-sm')
            async def create():
                # sanity check
                if not sel_customer.value.strip():
                    notify('Customer name is required', type='warning')
                    return
                if not sel_product.value.strip():
                    notify('Product is required', type='warning')
                    return
                if sel_qty.value <= 0:
                    notify('Quantity must be greater than 0', type='warning')
                    return
                async with AsyncSessionLocal() as db:
                    await create_order(db, sel_customer.value.strip(), sel_product.value.strip(), int(sel_qty.value))
                await refresh_func()
                notify('Order created successfully', type='positive', title='Order Created')
                dlg.close()
            ui.button('Create Order', color='white', on_click=create).props('flat no-caps').classes('button button-primary button-sm')
    return dlg


def content() -> None:

    # --- helper functions ---------------------------------------------------
    async def refresh():
        logger.info("Refreshing orders from database")
        async with AsyncSessionLocal() as db:
            orders = await get_orders(db)
            logger.info(f"Fetched {len(orders)} orders")
            table.rows = [
                {
                    "id": o.id,
                    "customer_name": o.customer_name,
                    "product": o.product,
                    "quantity": o.quantity
                }
                for o in orders
            ]
            table.update()

    async def delete_selected():
        selected = table.selected or []
        if not selected:
            notify('No order selected', type='warning')
            return
        
        async def perform_delete(rows):
            async with AsyncSessionLocal() as db:
                for row in rows:
                    await delete_order(db, row['id'])
            await refresh()
            notify(f'{len(rows)} order(s) deleted', type='negative', title='Deleted')
        
        _delete_confirmation_dialog(selected, perform_delete)

    #  page header 
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Database').classes('page-title')
            ui.label('View and manage orders stored in the database.').classes('text-sm text-muted')
        add_dialog = _new_order_dialog(lambda: refresh())
        ui.button('+ New Order', color='white', on_click=add_dialog.open).props('flat no-caps').classes('button button-primary')
    ui.button('Refresh', icon='refresh', color='white', on_click=refresh).props('flat no-caps').classes('button button-outline') 
    ui.element('div').classes('divider mb-4')


    # keep a reference to the table so we can update/inspect selection
    table = ui.table(
        columns=[
            {"name": "id", "label": "ID", "field": "id"},
            {"name": "customer_name", "label": "Customer", "field": "customer_name"},
            {"name": "product", "label": "Product", "field": "product"},
            {"name": "quantity", "label": "Qty", "field": "quantity"},
        ],
        rows=[],
        row_key='id',
    ).classes('data-table w-full').props('flat dense selection=multiple')

    # controls card with actions
    with ui.element('div').classes('mb-4'):
        with ui.row().classes('items-center justify-between mb-4'):
            ui.button('Delete selected', color='white', on_click=delete_selected).props('flat no-caps').classes('button button-danger button-sm')
        table  # table within the card

    ui.timer(0.1, refresh, once=True)

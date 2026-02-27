"""Shipping page — AG Grid shipment list with live search, status badges and KPI cards."""

import random
from nicegui import ui
from services.notifications import notify

_STATUS_HTML = {
    'Pending':    '<span class="badge badge-warning">Pending</span>',
    'In Transit': '<span class="badge badge-info">In Transit</span>',
    'Delivered':  '<span class="badge badge-success">Delivered</span>',
    'Cancelled':  '<span class="badge badge-danger">Cancelled</span>',
}

_CARRIERS  = ['DHL', 'FedEx', 'UPS', 'GLS', 'DPD']
_CUSTOMERS = ['Acme Corp', 'Beta GmbH', 'Gamma Ltd', 'Delta AG', 'Epsilon BV',
              'Zeta KG', 'Eta SRL', 'Theta Inc', 'Iota LLC', 'Kappa OY']
_CITIES    = ['Berlin', 'Hamburg', 'Munich', 'Amsterdam', 'Vienna',
              'Zurich', 'Brussels', 'Lyon', 'Milan', 'Warsaw']

_ROWS = [
    {'id': f'SHP-{1000+i}',
     'customer':    _CUSTOMERS[i % len(_CUSTOMERS)],
     'destination': _CITIES[i % len(_CITIES)],
     'carrier':     _CARRIERS[i % len(_CARRIERS)],
     'status':      s,
     'eta':         f'2026-03-{(i % 28)+1:02d}',
     'weight_kg':   round(5 + i * 2.3, 1),
     'status_html': _STATUS_HTML[s]}
    for i, s in enumerate(
        ['In Transit', 'Pending', 'Delivered', 'In Transit', 'Pending',
         'Delivered', 'Cancelled', 'In Transit', 'Delivered', 'Pending',
         'In Transit', 'Delivered', 'Pending', 'Cancelled', 'In Transit']
    )
]


def content() -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Shipping').classes('page-title')
            ui.label('Manage outbound shipments and carrier assignments.').classes('text-sm text-muted')
        ui.button('+ Add Shipment', color='white',
                  on_click=lambda: _add_row(grid_ref, notify)).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── KPI row ───────────────────────────────────────────────────
    counts = {s: sum(1 for r in _ROWS if r['status'] == s) for s in _STATUS_HTML}
    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            ('Total Shipments', str(len(_ROWS)),            'this week',       'text-info',    'local_shipping'),
            ('In Transit',      str(counts['In Transit']),  'currently active','text-warning',  'moving'),
            ('Delivered',       str(counts['Delivered']),   'completed',       'text-success',  'check_circle'),
            ('Pending',         str(counts['Pending']),     'awaiting pickup', 'text-muted',    'schedule'),
            ('Cancelled',       str(counts['Cancelled']),   'this week',       'text-danger',   'cancel'),
        ]:
            with ui.element('div').classes('card').style('min-width:150px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # ── Toolbar ───────────────────────────────────────────────────
    grid_ref = {}
    with ui.row().classes('w-full items-center gap-3 mb-3 flex-wrap'):
        search = ui.input(placeholder='Search shipments…').classes('flex-1').props('outlined rounded dense clearable')
        search.add_slot('prepend', '<q-icon name="search" />')
        ui.button('Export', color='white',
                  on_click=lambda: notify('Export started', type='info', title='Export')).props('flat no-caps').classes('button button-outline button-sm')

    # ── AG Grid ───────────────────────────────────────────────────
    grid = ui.aggrid({
        'columnDefs': [
            {'headerName': 'Shipment ID', 'field': 'id',           'width': 130, 'pinned': 'left'},
            {'headerName': 'Customer',    'field': 'customer',      'filter': 'agTextColumnFilter',   'floatingFilter': True},
            {'headerName': 'Destination', 'field': 'destination',   'filter': 'agTextColumnFilter',   'floatingFilter': True},
            {'headerName': 'Carrier',     'field': 'carrier',       'filter': 'agTextColumnFilter',   'floatingFilter': True, 'width': 110},
            {'headerName': 'Status',      'field': 'status_html',   'width': 150},
            {'headerName': 'ETA',         'field': 'eta',           'width': 120, 'sort': 'asc'},
            {'headerName': 'Weight (kg)', 'field': 'weight_kg',     'width': 130, 'filter': 'agNumberColumnFilter'},
        ],
        'rowData': _ROWS,
        'rowSelection': {'mode': 'multiRow'},
        'domLayout': 'autoHeight',
        'suppressCellFocus': True,
    }, html_columns=[4]).classes('w-full')
    grid_ref['grid'] = grid

    search.on('update:model-value', lambda e: grid.run_grid_method(
        'setGridOption', 'quickFilterText', e.args or ''))


def _add_row(grid_ref, notify_fn):
    grid = grid_ref.get('grid')
    if not grid:
        return
    i = len(grid.options['rowData'])
    s = random.choice(list(_STATUS_HTML))
    row = {
        'id':          f'SHP-{2000+i}',
        'customer':    random.choice(_CUSTOMERS),
        'destination': random.choice(_CITIES),
        'carrier':     random.choice(_CARRIERS),
        'status':      s,
        'eta':         f'2026-03-{random.randint(1, 28):02d}',
        'weight_kg':   round(random.uniform(2, 50), 1),
        'status_html': _STATUS_HTML[s],
    }
    grid.options['rowData'].append(row)
    grid.run_grid_method('ensureIndexVisible', i)
    grid.update()
    notify_fn(f'Added {row["id"]}', type='positive', title='Shipment added')

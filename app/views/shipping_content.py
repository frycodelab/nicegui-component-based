"""Shipping page: AG Grid shipment list with live search, status badges and KPI cards."""

import random
from nicegui import ui
from components.notifications import notify
from services.i18n import t

_STATUS_BADGE = {
    'Pending':    'badge-warning',
    'In Transit': 'badge-info',
    'Delivered':  'badge-success',
    'Cancelled':  'badge-danger',
}
_STATUS_KEY = {
    'Pending':    'status.pending',
    'In Transit': 'status.in_transit',
    'Delivered':  'status.delivered',
    'Cancelled':  'status.cancelled',
}


def _badge(status: str) -> str:
    return f'<span class="badge {_STATUS_BADGE[status]}">{t(_STATUS_KEY[status])}</span>'

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
     'weight_kg':   round(5 + i * 2.3, 1)}
    for i, s in enumerate(
        ['In Transit', 'Pending', 'Delivered', 'In Transit', 'Pending',
         'Delivered', 'Cancelled', 'In Transit', 'Delivered', 'Pending',
         'In Transit', 'Delivered', 'Pending', 'Cancelled', 'In Transit']
    )
]


def content() -> None:

    # Page header
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label(t('shipping.title')).classes('page-title')
            ui.label(t('shipping.subtitle')).classes('text-sm text-muted')
        ui.button(t('shipping.add'), color='white',
                  on_click=lambda: _add_row(grid_ref, notify)).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # KPI row
    counts = {s: sum(1 for r in _ROWS if r['status'] == s) for s in _STATUS_BADGE}
    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            (t('shipping.kpi.shipments'), str(len(_ROWS)),      t('shipping.sub.this_week'), 'text-info',    'local_shipping'),
            (t('status.in_transit'),      str(counts['In Transit']), t('shipping.sub.active'),    'text-warning',  'moving'),
            (t('status.delivered'),       str(counts['Delivered']),  t('shipping.sub.completed'), 'text-success',  'check_circle'),
            (t('status.pending'),         str(counts['Pending']),    t('shipping.sub.awaiting'),  'text-muted',    'schedule'),
            (t('status.cancelled'),       str(counts['Cancelled']),  t('shipping.sub.this_week'), 'text-danger',   'cancel'),
        ]:
            with ui.element('div').classes('card').style('min-width:150px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # Toolbar
    grid_ref = {}
    with ui.row().classes('w-full items-center gap-3 mb-3 flex-wrap'):
        search = ui.input(placeholder=t('shipping.search')).classes('flex-1').props('outlined rounded dense clearable')
        search.add_slot('prepend', '<q-icon name="search" />')
        ui.button(t('common.export'), color='white',
                  on_click=lambda: notify(t('shipping.export_started'), type='info', title=t('common.export'))).props('flat no-caps').classes('button button-outline button-sm')

    # AG Grid
    rows = [{**r, 'status_html': _badge(r['status'])} for r in _ROWS]
    grid = ui.aggrid({
        'columnDefs': [
            {'headerName': t('shipping.col.id'),          'field': 'id',           'width': 130, 'pinned': 'left'},
            {'headerName': t('common.customer'),          'field': 'customer',      'filter': 'agTextColumnFilter',   'floatingFilter': True},
            {'headerName': t('shipping.col.destination'), 'field': 'destination',   'filter': 'agTextColumnFilter',   'floatingFilter': True},
            {'headerName': t('shipping.col.carrier'),     'field': 'carrier',       'filter': 'agTextColumnFilter',   'floatingFilter': True, 'width': 110},
            {'headerName': t('common.status'),            'field': 'status_html',   'width': 150},
            {'headerName': t('shipping.col.eta'),         'field': 'eta',           'width': 120, 'sort': 'asc'},
            {'headerName': t('shipping.col.weight'),      'field': 'weight_kg',     'width': 130, 'filter': 'agNumberColumnFilter'},
        ],
        'rowData': rows,
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
    s = random.choice(list(_STATUS_BADGE))
    row = {
        'id':          f'SHP-{2000+i}',
        'customer':    random.choice(_CUSTOMERS),
        'destination': random.choice(_CITIES),
        'carrier':     random.choice(_CARRIERS),
        'status':      s,
        'eta':         f'2026-03-{random.randint(1, 28):02d}',
        'weight_kg':   round(random.uniform(2, 50), 1),
        'status_html': _badge(s),
    }
    grid.options['rowData'].append(row)
    grid.run_grid_method('ensureIndexVisible', i)
    grid.update()
    notify_fn(f'Added {row["id"]}', type='positive', title=t('shipping.added_title'))

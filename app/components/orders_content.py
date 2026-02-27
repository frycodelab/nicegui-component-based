"""Orders page — KPI summary, daily volume/revenue chart and recent orders table."""

from nicegui import ui
from services.notifications import notify

# ── Mock data ─────────────────────────────────────────────────────────────────
_RECENT = [
    {'id': 'ORD-4014', 'customer': 'Acme Corp',  'product': 'Gear Box',      'qty': 3,  'total': '€ 412.50',  'status': 'Fulfilled',  'date': 'Feb 27, 14:32'},
    {'id': 'ORD-4013', 'customer': 'Beta GmbH',  'product': 'Sensor Kit',    'qty': 1,  'total': '€ 137.50',  'status': 'Processing', 'date': 'Feb 27, 11:05'},
    {'id': 'ORD-4012', 'customer': 'Gamma Ltd',  'product': 'Panel Module',  'qty': 5,  'total': '€ 687.50',  'status': 'Open',       'date': 'Feb 27, 09:48'},
    {'id': 'ORD-4011', 'customer': 'Delta AG',   'product': 'Cable Harness', 'qty': 2,  'total': '€ 275.00',  'status': 'Cancelled',  'date': 'Feb 26, 17:21'},
    {'id': 'ORD-4010', 'customer': 'Epsilon BV', 'product': 'Widget A',      'qty': 10, 'total': '€ 1375.00', 'status': 'Fulfilled',  'date': 'Feb 26, 14:10'},
    {'id': 'ORD-4009', 'customer': 'Zeta KG',    'product': 'Motor Drive',   'qty': 1,  'total': '€ 137.50',  'status': 'On Hold',    'date': 'Feb 26, 10:55'},
]

_STATUS_COUNTS = {'Open': 3, 'Processing': 2, 'Fulfilled': 7, 'Cancelled': 2, 'On Hold': 1}
_DAILY = {
    'days':   ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'orders': [8, 12, 7, 15, 11, 4, 6],
    'revenue': [1100, 1650, 960, 2060, 1515, 550, 825],
}

_STATUS_STYLE = {
    'Open':       ('badge-info',    '#60a5fa'),
    'Processing': ('badge-warning', '#fbbf24'),
    'Fulfilled':  ('badge-success', '#4ade80'),
    'Cancelled':  ('badge-danger',  '#f87171'),
    'On Hold':    ('badge-default', '#a1a1aa'),
}

_TT  = {'backgroundColor': '#fff', 'borderColor': '#e4e4e7', 'textStyle': {'color': '#09090b', 'fontSize': 12}}
_AX  = {'axisLine': {'lineStyle': {'color': '#e4e4e7'}}, 'axisTick': {'show': False},
        'axisLabel': {'color': '#71717a', 'fontSize': 11}}
_SL  = {'splitLine': {'lineStyle': {'color': '#f4f4f5', 'type': 'dashed'}}}


def content(searchFilter=None) -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Orders').classes('page-title')
            ui.label('Track and manage incoming customer orders.').classes('text-sm text-muted')
        ui.button('+ New Order', color='white', on_click=_new_order_dialog).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── KPI row ───────────────────────────────────────────────────
    total   = sum(_STATUS_COUNTS.values())
    revenue = sum(_DAILY['revenue'])
    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            ('Total Orders', str(total),                           'this week',   'text-info',    'receipt_long'),
            ('Revenue',      f'\u20ac {revenue:,}',                'this week',   'text-success', 'payments'),
            ('Fulfilled',    str(_STATUS_COUNTS['Fulfilled']),     'completed',   'text-success', 'check_circle'),
            ('Processing',   str(_STATUS_COUNTS['Processing']),    'in progress', 'text-warning', 'autorenew'),
            ('Cancelled',    str(_STATUS_COUNTS['Cancelled']),     'this week',   'text-danger',  'cancel'),
        ]:
            with ui.element('div').classes('card').style('min-width:150px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # ── Charts row ────────────────────────────────────────────────
    with ui.row().classes('gap-4 flex-wrap w-full mb-6'):

        # Status donut
        with ui.element('div').classes('card').style('flex:1;min-width:280px'):
            ui.label('Status Breakdown').classes('card-title mb-1')
            ui.echart({
                'tooltip': {'trigger': 'item', **_TT},
                'legend':  {'bottom': 0, 'left': 'center',
                            'textStyle': {'color': '#71717a', 'fontSize': 12},
                            'itemWidth': 10, 'itemHeight': 10, 'itemGap': 12},
                'series': [{
                    'type': 'pie', 'radius': ['46%', '70%'], 'center': ['50%', '44%'],
                    'avoidLabelOverlap': False,
                    'label': {'show': False},
                    'emphasis': {'label': {'show': True, 'fontSize': 13, 'fontWeight': 'bold', 'color': '#09090b'}},
                    'labelLine': {'show': False},
                    'data': [
                        {'name': k, 'value': v, 'itemStyle': {'color': _STATUS_STYLE[k][1]}}
                        for k, v in _STATUS_COUNTS.items()
                    ],
                }],
            }).classes('w-full').style('height:280px')

        # Orders (bars) + Revenue (line) — dual axis
        with ui.element('div').classes('card').style('flex:2;min-width:360px'):
            ui.label('Orders & Revenue — This Week').classes('card-title mb-1')
            ui.echart({
                'tooltip': {'trigger': 'axis', **_TT, 'axisPointer': {'type': 'cross'}},
                'legend': {'data': ['Orders', 'Revenue'], 'top': 0,
                           'textStyle': {'color': '#71717a', 'fontSize': 12}},
                'grid': {'left': '3%', 'right': '4%', 'bottom': '3%', 'top': '14%', 'containLabel': True},
                'xAxis': {'type': 'category', 'data': _DAILY['days'], **_AX},
                'yAxis': [
                    {**_AX, **_SL, 'type': 'value', 'name': 'Orders',
                     'axisLabel': {'color': '#71717a', 'fontSize': 11}},
                    {**_AX, **_SL, 'type': 'value', 'name': 'Revenue (€)',
                     'splitLine': {'show': False},
                     'axisLabel': {':formatter': 'v => "€" + v', 'color': '#71717a', 'fontSize': 11}},
                ],
                'series': [
                    {'name': 'Orders', 'type': 'bar', 'yAxisIndex': 0,
                     'data': _DAILY['orders'], 'barMaxWidth': 32,
                     'itemStyle': {'color': '#60a5fa', 'borderRadius': [4, 4, 0, 0]}},
                    {'name': 'Revenue', 'type': 'line', 'smooth': True, 'yAxisIndex': 1,
                     'data': _DAILY['revenue'], 'symbol': 'circle', 'symbolSize': 6,
                     'lineStyle': {'width': 2.5, 'color': '#4ade80'},
                     'itemStyle': {'color': '#4ade80', 'borderWidth': 2, 'borderColor': '#fff'}},
                ],
            }).classes('w-full').style('height:280px')

    # ── Recent orders table ───────────────────────────────────────
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('items-center justify-between mb-4'):
            with ui.column().classes('gap-0'):
                ui.label('Recent Orders').classes('card-title')
                ui.label(f'{len(_RECENT)} orders shown').classes('text-xs text-muted mt-1')
            ui.button('View all', color='white',
                      on_click=lambda: notify('Loading full order list…', type='info')).props('flat no-caps').classes('button button-ghost button-sm')
        with ui.element('table').classes('data-table w-full'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in ['Order ID', 'Customer', 'Product', 'Qty', 'Total', 'Status', 'Date']:
                        with ui.element('th'): ui.label(col)
            with ui.element('tbody'):
                for r in _RECENT:
                    badge_cls, _ = _STATUS_STYLE.get(r['status'], ('badge-default', '#a1a1aa'))
                    with ui.element('tr'):
                        with ui.element('td'):
                            ui.label(r['id']).classes('font-semi text-sm')
                        with ui.element('td'): ui.label(r['customer'])
                        with ui.element('td'): ui.label(r['product'])
                        with ui.element('td'): ui.label(str(r['qty']))
                        with ui.element('td'):
                            ui.label(r['total']).classes('font-semi')
                        with ui.element('td'):
                            ui.label(r['status']).classes(f'badge {badge_cls}')
                        with ui.element('td'):
                            ui.label(r['date']).classes('text-muted')


def _new_order_dialog() -> None:
    with ui.dialog(value=True) as dlg, ui.card().style('min-width:380px;padding:28px 32px'):
        with ui.row().classes('items-center justify-between w-full mb-4'):
            ui.label('New Order').classes('card-title')
            ui.button(icon='close', color='white', on_click=dlg.close).props('flat round dense').classes('button button-ghost')
        with ui.column().classes('gap-4 w-full'):
            with ui.element('div').classes('w-full'):
                ui.label('Customer').classes('field-label')
                ui.select(['Acme Corp', 'Beta GmbH', 'Gamma Ltd', 'Delta AG', 'Epsilon BV'],
                          value='Acme Corp').classes('w-full').props('outlined dense')
            with ui.element('div').classes('w-full'):
                ui.label('Product').classes('field-label')
                ui.select(['Widget A', 'Gear Box', 'Control Unit', 'Panel Module'],
                          value='Widget A').classes('w-full').props('outlined dense')
            with ui.row().classes('gap-4 w-full'):
                with ui.element('div').classes('flex-1'):
                    ui.label('Quantity').classes('field-label')
                    ui.number(value=1, min=1, max=999).classes('w-full').props('outlined dense')
                with ui.element('div').classes('flex-1'):
                    ui.label('Priority').classes('field-label')
                    ui.select(['Normal', 'High', 'Urgent'], value='Normal').classes('w-full').props('outlined dense')
        ui.element('div').classes('divider mt-4 mb-4')
        with ui.row().classes('gap-3 justify-end w-full'):
            ui.button('Cancel', color='white', on_click=dlg.close).props('flat no-caps').classes('button button-outline button-sm')
            ui.button('Create Order', color='white', on_click=lambda: [
                notify('Order created successfully', type='positive', title='Order Created'),
                dlg.close(),
            ]).props('flat no-caps').classes('button button-primary button-sm')


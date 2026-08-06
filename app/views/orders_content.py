"""Orders page: KPI summary, daily volume/revenue chart and recent orders table."""

from nicegui import ui
from components.notifications import notify
from services.i18n import t

# Mock data
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

_STATUS_KEY = {
    'Open':       'status.open',
    'Processing': 'status.processing',
    'Fulfilled':  'status.fulfilled',
    'Cancelled':  'status.cancelled',
    'On Hold':    'status.on_hold',
}

_TT  = {'backgroundColor': '#fff', 'borderColor': '#e4e4e7', 'textStyle': {'color': '#09090b', 'fontSize': 12}}
_AX  = {'axisLine': {'lineStyle': {'color': '#e4e4e7'}}, 'axisTick': {'show': False},
        'axisLabel': {'color': '#71717a', 'fontSize': 11}}
_SL  = {'splitLine': {'lineStyle': {'color': '#f4f4f5', 'type': 'dashed'}}}


def content(searchFilter=None) -> None:

    # Page header
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label(t('orders.title')).classes('page-title')
            ui.label(t('orders.subtitle')).classes('text-sm text-muted')
        ui.button(t('orders.add'), color='white', on_click=_new_order_dialog).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # KPI row
    total   = sum(_STATUS_COUNTS.values())
    revenue = sum(_DAILY['revenue'])
    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            (t('orders.kpi.total'),      str(total),                       t('orders.sub.this_week'),   'text-info',    'receipt_long'),
            (t('orders.kpi.revenue'),    f'\u20ac {revenue:,}',            t('orders.sub.this_week'),   'text-success', 'payments'),
            (t('orders.kpi.fulfilled'),  str(_STATUS_COUNTS['Fulfilled']), t('orders.sub.completed'),   'text-success', 'check_circle'),
            (t('orders.kpi.processing'), str(_STATUS_COUNTS['Processing']),t('orders.sub.in_progress'), 'text-warning', 'autorenew'),
            (t('orders.kpi.cancelled'),  str(_STATUS_COUNTS['Cancelled']), t('orders.sub.this_week'),   'text-danger',  'cancel'),
        ]:
            with ui.element('div').classes('card').style('min-width:150px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # Charts row
    with ui.row().classes('gap-4 flex-wrap w-full mb-6'):

        # Status donut
        with ui.element('div').classes('card').style('flex:1;min-width:280px'):
            ui.label(t('orders.status_breakdown')).classes('card-title mb-1')
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
                        {'name': t(_STATUS_KEY[k]), 'value': v, 'itemStyle': {'color': _STATUS_STYLE[k][1]}}
                        for k, v in _STATUS_COUNTS.items()
                    ],
                }],
            }).classes('w-full').style('height:280px')

        # Orders (bars) + revenue (line), dual axis
        with ui.element('div').classes('card').style('flex:2;min-width:360px'):
            ui.label(t('orders.orders_revenue')).classes('card-title mb-1')
            ui.echart({
                'tooltip': {'trigger': 'axis', **_TT, 'axisPointer': {'type': 'cross'}},
                'legend': {'data': [t('orders.legend.orders'), t('orders.legend.revenue')], 'top': 0,
                           'textStyle': {'color': '#71717a', 'fontSize': 12}},
                'grid': {'left': '3%', 'right': '4%', 'bottom': '3%', 'top': '14%', 'containLabel': True},
                'xAxis': {'type': 'category', 'data': _DAILY['days'], **_AX},
                'yAxis': [
                    {**_AX, **_SL, 'type': 'value', 'name': t('orders.legend.orders'),
                     'axisLabel': {'color': '#71717a', 'fontSize': 11}},
                    {**_AX, **_SL, 'type': 'value', 'name': t('orders.legend.revenue') + ' (€)',
                     'splitLine': {'show': False},
                     'axisLabel': {':formatter': 'v => "€" + v', 'color': '#71717a', 'fontSize': 11}},
                ],
                'series': [
                    {'name': t('orders.legend.orders'), 'type': 'bar', 'yAxisIndex': 0,
                     'data': _DAILY['orders'], 'barMaxWidth': 32,
                     'itemStyle': {'color': '#60a5fa', 'borderRadius': [4, 4, 0, 0]}},
                    {'name': t('orders.legend.revenue'), 'type': 'line', 'smooth': True, 'yAxisIndex': 1,
                     'data': _DAILY['revenue'], 'symbol': 'circle', 'symbolSize': 6,
                     'lineStyle': {'width': 2.5, 'color': '#4ade80'},
                     'itemStyle': {'color': '#4ade80', 'borderWidth': 2, 'borderColor': '#fff'}},
                ],
            }).classes('w-full').style('height:280px')

    # Recent orders table
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('items-center justify-between mb-4'):
            with ui.column().classes('gap-0'):
                ui.label(t('orders.recent')).classes('card-title')
                ui.label(t('orders.shown').format(n=len(_RECENT))).classes('text-xs text-muted mt-1')
            ui.button(t('common.view_all'), color='white',
                      on_click=lambda: notify(t('orders.loading_all'), type='info')).props('flat no-caps').classes('button button-ghost button-sm')
        with ui.element('table').classes('data-table w-full'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in [t('orders.col.id'), t('common.customer'), t('common.product'), t('orders.col.qty'), t('common.total'), t('common.status'), t('common.date')]:
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
                            ui.label(t(_STATUS_KEY.get(r['status'], 'status.open'))).classes(f'badge {badge_cls}')
                        with ui.element('td'):
                            ui.label(r['date']).classes('text-muted')


def _new_order_dialog() -> None:
    with ui.dialog(value=True) as dlg, ui.card().style('min-width:380px;padding:28px 32px'):
        with ui.row().classes('items-center justify-between w-full mb-4'):
            ui.label(t('orders.new_order')).classes('card-title')
            ui.button(icon='close', color='white', on_click=dlg.close).props('flat round dense').classes('button button-ghost')
        with ui.column().classes('gap-4 w-full'):
            with ui.element('div').classes('w-full'):
                ui.label(t('common.customer')).classes('field-label')
                ui.select(['Acme Corp', 'Beta GmbH', 'Gamma Ltd', 'Delta AG', 'Epsilon BV'],
                          value='Acme Corp').classes('w-full').props('outlined dense')
            with ui.element('div').classes('w-full'):
                ui.label(t('common.product')).classes('field-label')
                ui.select(['Widget A', 'Gear Box', 'Control Unit', 'Panel Module'],
                          value='Widget A').classes('w-full').props('outlined dense')
            with ui.row().classes('gap-4 w-full'):
                with ui.element('div').classes('flex-1'):
                    ui.label(t('orders.quantity')).classes('field-label')
                    ui.number(value=1, min=1, max=999).classes('w-full').props('outlined dense')
                with ui.element('div').classes('flex-1'):
                    ui.label(t('orders.priority')).classes('field-label')
                    ui.select([t('orders.priority.normal'), t('orders.priority.high'), t('orders.priority.urgent')], value=t('orders.priority.normal')).classes('w-full').props('outlined dense')
        ui.element('div').classes('divider mt-4 mb-4')
        with ui.row().classes('gap-3 justify-end w-full'):
            ui.button(t('common.cancel'), color='white', on_click=dlg.close).props('flat no-caps').classes('button button-outline button-sm')
            ui.button(t('orders.create_order'), color='white', on_click=lambda: [
                notify(t('orders.created'), type='positive', title=t('orders.created_title')),
                dlg.close(),
            ]).props('flat no-caps').classes('button button-primary button-sm')


"""Production page — live line status, KPI summary and hourly throughput chart."""

from nicegui import ui
from services.notifications import notify

_LINES = [
    {'name': 'Line A', 'product': 'Gear Box',     'shift': 'Morning',   'target': 500, 'actual': 487, 'status': 'Running', 'status_cls': 'badge-success'},
    {'name': 'Line B', 'product': 'Sensor Kit',   'shift': 'Morning',   'target': 300, 'actual': 210, 'status': 'Paused',  'status_cls': 'badge-warning'},
    {'name': 'Line C', 'product': 'Control Unit', 'shift': 'Afternoon', 'target': 400, 'actual': 398, 'status': 'Running', 'status_cls': 'badge-success'},
    {'name': 'Line D', 'product': 'Panel Module', 'shift': 'Afternoon', 'target': 250, 'actual': 0,   'status': 'Error',   'status_cls': 'badge-danger'},
    {'name': 'Line E', 'product': 'Widget A',     'shift': 'Night',     'target': 600, 'actual': 561, 'status': 'Running', 'status_cls': 'badge-success'},
]

_THROUGHPUT = {
    'hours':  ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
    'line_a': [42, 58, 61, 55, 63, 60, 58, 49],
    'line_c': [38, 50, 54, 48, 55, 52, 50, 43],
    'line_e': [60, 72, 75, 68, 78, 74, 71, 65],
}

_TT = {'backgroundColor': '#fff', 'borderColor': '#e4e4e7', 'textStyle': {'color': '#09090b', 'fontSize': 12}}
_AX = {'axisLine': {'lineStyle': {'color': '#e4e4e7'}}, 'axisTick': {'show': False},
       'axisLabel': {'color': '#71717a', 'fontSize': 11}}
_SL = {'splitLine': {'lineStyle': {'color': '#f4f4f5', 'type': 'dashed'}}}


def content(searchFilter=None) -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Production').classes('page-title')
            ui.label('Monitor line status, work orders and throughput.').classes('text-sm text-muted')
        ui.button('+ New Work Order', color='white',
                  on_click=lambda: notify('Work order form coming soon', type='info')).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── KPI row ───────────────────────────────────────────────────
    running = sum(1 for l in _LINES if l['status'] == 'Running')
    total_t = sum(l['target'] for l in _LINES)
    total_a = sum(l['actual'] for l in _LINES)
    eff     = int(total_a / total_t * 100) if total_t else 0
    alerts  = sum(1 for l in _LINES if l['status'] == 'Error')

    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            ('Active Lines', f'{running} / {len(_LINES)}', 'currently running',          'text-success',                               'conveyor_belt'),
            ('Units Today',  f'{total_a:,}',               f'of {total_t:,} target',     'text-info',                                  'inventory_2'),
            ('Efficiency',   f'{eff} %',                   'vs daily target',            'text-success' if eff >= 90 else 'text-warning','speed'),
            ('Shifts',       '3',                          'Morning / Afternoon / Night', 'text-info',                                  'schedule'),
            ('Alerts',       str(alerts),                  'lines in error state',        'text-danger' if alerts else 'text-muted',    'warning'),
        ]:
            with ui.element('div').classes('card').style('min-width:150px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # ── Line status table ─────────────────────────────────────────
    with ui.element('div').classes('card mb-6'):
        with ui.row().classes('items-center justify-between mb-4'):
            with ui.column().classes('gap-0'):
                ui.label('Line Status').classes('card-title')
                ui.label(f'{len(_LINES)} production lines').classes('text-xs text-muted mt-1')
            ui.button('Refresh', color='white',
                      on_click=lambda: notify('Line data refreshed', type='info')).props('flat no-caps').classes('button button-ghost button-sm')
        with ui.element('table').classes('data-table w-full'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in ['Line', 'Product', 'Shift', 'Progress', 'Actual / Target', 'Status']:
                        with ui.element('th'): ui.label(col)
            with ui.element('tbody'):
                for line in _LINES:
                    pct = int(line['actual'] / line['target'] * 100) if line['target'] else 0
                    bar_color = ('#4ade80' if pct >= 90 else '#fbbf24' if pct >= 60 else '#f87171')
                    with ui.element('tr'):
                        with ui.element('td'):
                            ui.label(line['name']).classes('font-semi')
                        with ui.element('td'): ui.label(line['product'])
                        with ui.element('td'): ui.label(line['shift'])
                        with ui.element('td').style('min-width:160px'):
                            ui.element('div').style(
                                f'height:6px;border-radius:9999px;background:#f4f4f5;overflow:hidden'
                            ).add_slot('default',
                                f'<div style="width:{pct}%;height:100%;background:{bar_color};border-radius:9999px;transition:width .4s"></div>'
                            )
                        with ui.element('td'):
                            ui.label(f'{line["actual"]:,} / {line["target"]:,}').classes('text-sm')
                            ui.label(f'{pct} %').classes('text-xs text-muted')
                        with ui.element('td'):
                            ui.label(line['status']).classes(f'badge {line["status_cls"]}')

    # ── Throughput chart ──────────────────────────────────────────
    with ui.element('div').classes('card mb-4').style('padding:20px 20px 12px 20px'):
        with ui.row().classes('items-start justify-between mb-1'):
            with ui.column().classes('gap-0'):
                ui.label('Throughput Today').classes('card-title')
                ui.label('Units per hour — running lines only').classes('text-xs text-muted mt-1')
        ui.echart({
            'tooltip': {'trigger': 'axis', **_TT,
                        'axisPointer': {'type': 'cross', 'label': {'backgroundColor': '#60a5fa'}}},
            'legend': {'data': ['Line A', 'Line C', 'Line E'], 'top': 0,
                       'textStyle': {'color': '#71717a', 'fontSize': 12},
                       'itemWidth': 10, 'itemHeight': 10, 'itemGap': 16},
            'grid': {'left': '2%', 'right': '2%', 'bottom': '2%', 'top': '14%', 'containLabel': True},
            'xAxis': {'type': 'category', 'data': _THROUGHPUT['hours'], 'boundaryGap': False, **_AX},
            'yAxis': {**_AX, **_SL, 'type': 'value', 'name': 'units / h',
                      'axisLabel': {'color': '#71717a', 'fontSize': 11}},
            'series': [
                {'name': 'Line A', 'type': 'line', 'smooth': True,
                 'data': _THROUGHPUT['line_a'], 'symbol': 'circle', 'symbolSize': 5,
                 'lineStyle': {'width': 2.5, 'color': '#60a5fa'},
                 'itemStyle': {'color': '#60a5fa'},
                 'areaStyle': {'color': '#60a5fa', 'opacity': 0.10}},
                {'name': 'Line C', 'type': 'line', 'smooth': True,
                 'data': _THROUGHPUT['line_c'], 'symbol': 'circle', 'symbolSize': 5,
                 'lineStyle': {'width': 2.5, 'color': '#4ade80'},
                 'itemStyle': {'color': '#4ade80'},
                 'areaStyle': {'color': '#4ade80', 'opacity': 0.10}},
                {'name': 'Line E', 'type': 'line', 'smooth': True,
                 'data': _THROUGHPUT['line_e'], 'symbol': 'circle', 'symbolSize': 5,
                 'lineStyle': {'width': 2.5, 'color': '#fbbf24'},
                 'itemStyle': {'color': '#fbbf24'},
                 'areaStyle': {'color': '#fbbf24', 'opacity': 0.10}},
            ],
        }).classes('w-full').style('height:380px')
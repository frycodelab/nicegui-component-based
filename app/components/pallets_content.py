"""Pallets page — inventory cards, KPI row and per-location capacity summary table."""

from nicegui import ui
from services.notifications import notify

_PALLETS = [
    {'id': 'PLT-3000', 'type': 'EUR Pallet',     'location': 'Warehouse A', 'cap': 500, 'load': 480, 'status': 'In Use',     'dot': 'info'},
    {'id': 'PLT-3001', 'type': 'Half Pallet',     'location': 'Dock 1',      'cap': 300, 'load': 0,   'status': 'Available',  'dot': 'success'},
    {'id': 'PLT-3002', 'type': 'EUR Pallet',      'location': 'Warehouse B', 'cap': 500, 'load': 500, 'status': 'In Transit', 'dot': 'warning'},
    {'id': 'PLT-3003', 'type': 'Chemical Pallet', 'location': 'Staging',     'cap': 400, 'load': 120, 'status': 'Available',  'dot': 'success'},
    {'id': 'PLT-3004', 'type': 'Display Pallet',  'location': 'Line A',      'cap': 250, 'load': 210, 'status': 'In Use',     'dot': 'info'},
    {'id': 'PLT-3005', 'type': 'EUR Pallet',      'location': 'Dock 2',      'cap': 500, 'load': 80,  'status': 'Damaged',    'dot': 'danger'},
    {'id': 'PLT-3006', 'type': 'One-way',         'location': 'Warehouse A', 'cap': 600, 'load': 0,   'status': 'Available',  'dot': 'success'},
    {'id': 'PLT-3007', 'type': 'Half Pallet',     'location': 'Line B',      'cap': 300, 'load': 290, 'status': 'In Use',     'dot': 'info'},
]

_STATUS_BADGE = {
    'Available':  'badge-success',
    'In Use':     'badge-info',
    'In Transit': 'badge-warning',
    'Damaged':    'badge-danger',
}

_LOCATION_COUNTS: dict = {}
for _p in _PALLETS:
    _LOCATION_COUNTS[_p['location']] = _LOCATION_COUNTS.get(_p['location'], 0) + 1


def content() -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Pallets').classes('page-title')
            ui.label('Track pallet inventory, locations and capacity utilisation.').classes('text-sm text-muted')
        ui.button('+ Register Pallet', color='white',
                  on_click=lambda: notify('Registration form coming soon', type='info')).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── KPI row ───────────────────────────────────────────────────
    by_status: dict = {}
    for p in _PALLETS:
        by_status[p['status']] = by_status.get(p['status'], 0) + 1

    total_load = sum(p['load'] for p in _PALLETS)
    total_cap  = sum(p['cap']  for p in _PALLETS)
    util_pct   = int(total_load / total_cap * 100) if total_cap else 0

    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            ('Total',       str(len(_PALLETS)),                   'registered',       'text-info',    'inventory_2'),
            ('Available',   str(by_status.get('Available', 0)),   'ready to use',     'text-success', 'check_circle'),
            ('In Use',      str(by_status.get('In Use', 0)),      'currently loaded', 'text-info',    'forklift'),
            ('In Transit',  str(by_status.get('In Transit', 0)),  'on the move',      'text-warning', 'moving'),
            ('Damaged',     str(by_status.get('Damaged', 0)),     'needs inspection', 'text-danger',  'warning'),
            ('Utilisation', f'{util_pct} %',                      'fleet avg load',   'text-info' if util_pct < 80 else 'text-warning', 'speed'),
        ]:
            with ui.element('div').classes('card').style('min-width:130px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # ── Pallet cards ──────────────────────────────────────────────
    with ui.row().classes('items-center justify-between mb-3'):
        with ui.column().classes('gap-0'):
            ui.label('Pallet Inventory').classes('card-title')
            ui.label(f'{len(_PALLETS)} pallets registered').classes('text-xs text-muted mt-1')

    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for p in _PALLETS:
            fill = int(p['load'] / p['cap'] * 100) if p['cap'] else 0
            bar_color = ('#f87171' if p['status'] == 'Damaged'
                         else '#4ade80' if fill >= 80
                         else '#60a5fa')
            with ui.element('div').classes('card').style('min-width:210px;flex:1;max-width:300px'):
                # Card header
                with ui.row().classes('items-center justify-between mb-3'):
                    with ui.row().classes('items-center gap-2'):
                        ui.element('span').classes(f'status-dot {p["dot"]}')
                        ui.label(p['id']).classes('font-semi text-sm')
                    ui.label(p['status']).classes(f'badge {_STATUS_BADGE.get(p["status"], "badge-default")}')
                # Meta
                with ui.column().classes('gap-1 mb-3'):
                    ui.label(p['type']).classes('text-sm font-medium')
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('location_on').style('font-size:13px;color:var(--muted-fg)')
                        ui.label(p['location']).classes('text-xs text-faint')
                # Load bar
                with ui.element('div').classes('w-full mb-3'):
                    with ui.row().classes('items-center justify-between mb-1'):
                        ui.label('Load capacity').classes('text-xs text-muted')
                        ui.label(f'{fill} %').classes('text-xs font-semi')
                    ui.element('div').style(
                        'height:6px;border-radius:9999px;background:#f4f4f5;overflow:hidden;width:100%'
                    ).add_slot('default',
                        f'<div style="width:{fill}%;height:100%;background:{bar_color};'
                        f'border-radius:9999px;transition:width .4s"></div>'
                    )
                    ui.label(f'{p["load"]} / {p["cap"]} kg').classes('text-xs text-faint mt-1')
                # Actions
                ui.element('div').classes('divider mt-0 mb-2')
                with ui.row().classes('gap-2'):
                    ui.button('Move', color='white',
                              on_click=lambda pid=p['id']: notify(f'{pid} move scheduled', type='info')).props('flat no-caps').classes('button button-outline button-sm')
                    ui.button('Inspect', color='white',
                              on_click=lambda pid=p['id']: notify(f'{pid} inspection queued', type='warning')).props('flat no-caps').classes('button button-ghost button-sm')

    # ── Location summary ──────────────────────────────────────────
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('items-center justify-between mb-4'):
            with ui.column().classes('gap-0'):
                ui.label('By Location').classes('card-title')
                ui.label(f'{len(_LOCATION_COUNTS)} locations').classes('text-xs text-muted mt-1')
        with ui.element('table').classes('data-table w-full'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in ['Location', 'Pallets', 'Total Load', 'Utilisation']:
                        with ui.element('th'): ui.label(col)
            with ui.element('tbody'):
                for loc, cnt in sorted(_LOCATION_COUNTS.items()):
                    loc_pallets = [p for p in _PALLETS if p['location'] == loc]
                    t_load = sum(p['load'] for p in loc_pallets)
                    t_cap  = sum(p['cap']  for p in loc_pallets)
                    util   = int(t_load / t_cap * 100) if t_cap else 0
                    bar_c  = '#4ade80' if util < 80 else '#fbbf24'
                    with ui.element('tr'):
                        with ui.element('td'): ui.label(loc).classes('font-semi')
                        with ui.element('td'): ui.label(str(cnt))
                        with ui.element('td'): ui.label(f'{t_load:,} / {t_cap:,} kg').classes('text-muted')
                        with ui.element('td'):
                            with ui.element('div').classes('flex items-center gap-3'):
                                ui.element('div').style(
                                    'flex:1;height:6px;border-radius:9999px;background:#f4f4f5;overflow:hidden'
                                ).add_slot('default',
                                    f'<div style="width:{util}%;height:100%;background:{bar_c};'
                                    f'border-radius:9999px;transition:width .4s"></div>'
                                )
                                ui.label(f'{util} %').classes('text-xs text-muted').style('min-width:36px')
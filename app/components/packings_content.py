"""Packings page — Kanban board (Pending → In Progress → Packed) with pipeline summary."""

from nicegui import ui
from services.notifications import notify

_COLUMNS = {
    'Pending': [
        {'id': 'PKG-6000', 'order': 'ORD-4007', 'customer': 'Acme Corp',  'product': 'Gear Box',       'units': 3,  'due': 'Mar 01', 'pack_type': 'Box M'},
        {'id': 'PKG-6001', 'order': 'ORD-4010', 'customer': 'Gamma Ltd',  'product': 'Sensor Kit',     'units': 1,  'due': 'Mar 02', 'pack_type': 'Envelope'},
        {'id': 'PKG-6002', 'order': 'ORD-4012', 'customer': 'Zeta KG',    'product': 'Panel Module',   'units': 5,  'due': 'Mar 03', 'pack_type': 'Box L'},
        {'id': 'PKG-6003', 'order': 'ORD-4014', 'customer': 'Theta Inc',  'product': 'Widget A',       'units': 10, 'due': 'Mar 04', 'pack_type': 'Pallet'},
    ],
    'In Progress': [
        {'id': 'PKG-6004', 'order': 'ORD-4001', 'customer': 'Beta GmbH',  'product': 'Control Unit',   'units': 2,  'due': 'Feb 28', 'pack_type': 'Box S'},
        {'id': 'PKG-6005', 'order': 'ORD-4003', 'customer': 'Delta AG',   'product': 'Cable Harness',  'units': 4,  'due': 'Mar 01', 'pack_type': 'Box M'},
        {'id': 'PKG-6006', 'order': 'ORD-4009', 'customer': 'Iota LLC',   'product': 'Motor Drive',    'units': 1,  'due': 'Mar 01', 'pack_type': 'Box S'},
    ],
    'Packed': [
        {'id': 'PKG-6007', 'order': 'ORD-4000', 'customer': 'Epsilon BV', 'product': 'Filter Pack',    'units': 6,  'due': 'Feb 27', 'pack_type': 'Box L'},
        {'id': 'PKG-6008', 'order': 'ORD-4002', 'customer': 'Kappa OY',   'product': 'Valve Assembly', 'units': 2,  'due': 'Feb 27', 'pack_type': 'Box M'},
        {'id': 'PKG-6009', 'order': 'ORD-4004', 'customer': 'Eta SRL',    'product': 'Bracket Set',    'units': 8,  'due': 'Feb 26', 'pack_type': 'Pallet'},
        {'id': 'PKG-6010', 'order': 'ORD-4006', 'customer': 'Acme Corp',  'product': 'Gear Box',       'units': 1,  'due': 'Feb 26', 'pack_type': 'Envelope'},
        {'id': 'PKG-6011', 'order': 'ORD-4008', 'customer': 'Beta GmbH',  'product': 'Widget A',       'units': 3,  'due': 'Feb 25', 'pack_type': 'Box S'},
    ],
}

_COL_STYLE = {
    'Pending':     ('badge-warning', 'text-warning', 'inventory',    '#fbbf24'),
    'In Progress': ('badge-info',    'text-info',    'pending',      '#60a5fa'),
    'Packed':      ('badge-success', 'text-success', 'check_circle', '#4ade80'),
}

_COL_ACTION = {
    'Pending':     ('Start',       'button-outline',  'info',     'Started'),
    'In Progress': ('Mark Packed', 'button-success',  'positive', 'Packed'),
    'Packed':      ('Dispatch',    'button-primary',  'positive', 'Dispatched'),
}


def content() -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Packings').classes('page-title')
            ui.label('Manage packing jobs across all stages.').classes('text-sm text-muted')
        ui.button('+ New Job', color='white',
                  on_click=lambda: notify('New job form coming soon', type='info')).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── Pipeline summary strip ────────────────────────────────────
    total       = sum(len(v) for v in _COLUMNS.values())
    total_units = sum(j['units'] for jobs in _COLUMNS.values() for j in jobs)

    with ui.row().classes('gap-0 flex-wrap mb-6 w-full').style(
            'border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden'):
        # Left summary
        with ui.element('div').style(
                'flex:1;min-width:160px;padding:18px 24px;border-right:1px solid var(--border)'):
            ui.label('TOTAL JOBS').classes('label-text mb-1')
            ui.label(str(total)).classes('text-2xl font-bold text-info')
            ui.label(f'{total_units} units to pack').classes('text-xs text-muted mt-1')

        # Pipeline stages
        for col_name in ('Pending', 'In Progress', 'Packed'):
            badge_cls, text_cls, col_icon, col_color = _COL_STYLE[col_name]
            cnt = len(_COLUMNS[col_name])
            pct = int(cnt / total * 100) if total else 0
            is_last = col_name == 'Packed'
            with ui.element('div').style(
                    f'flex:1;min-width:140px;padding:18px 24px;'
                    f'{"" if is_last else "border-right:1px solid var(--border)"}'):
                with ui.row().classes('items-center gap-2 mb-1'):
                    ui.icon(col_icon).style(f'font-size:1rem;color:{col_color}')
                    ui.label(col_name).classes('label-text')
                ui.label(str(cnt)).classes(f'text-2xl font-bold {text_cls}')
                ui.label(f'{pct} % of jobs').classes('text-xs text-muted mt-1')

    # ── Kanban board ──────────────────────────────────────────────
    with ui.row().classes('gap-4 items-start w-full'):
        for col_name, jobs in _COLUMNS.items():
            badge_cls, text_cls, col_icon, col_color = _COL_STYLE[col_name]
            action_label, action_cls, action_type, action_title = _COL_ACTION[col_name]

            with ui.element('div').style(
                    f'flex:1;min-width:260px;padding:14px;border-radius:var(--radius-lg);'
                    f'border:1px solid var(--border);background:var(--faint)'):

                # Column header
                with ui.row().classes('items-center justify-between mb-4').style(
                        f'padding-bottom:12px;border-bottom:2px solid {col_color}'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon(col_icon).style(f'font-size:1.1rem;color:{col_color}')
                        ui.label(col_name).classes('font-semi text-base')
                    ui.label(str(len(jobs))).classes(f'badge {badge_cls}')

                # Job cards
                with ui.column().classes('gap-3 w-full'):
                    for job in jobs:
                        with ui.element('div').classes('card').style('padding:16px 18px'):

                            # Card top: ID + due date
                            with ui.row().classes('items-center justify-between mb-2'):
                                ui.label(job['id']).classes('font-semi text-sm')
                                with ui.row().classes('items-center gap-1'):
                                    ui.icon('event').style('font-size:12px;color:var(--faint-fg)')
                                    ui.label(f'Due {job["due"]}').classes('text-xs text-faint')

                            # Product + customer
                            ui.label(job['product']).classes('text-sm font-medium mb-1')
                            ui.label(job['customer']).classes('text-xs text-muted mb-3')

                            # Chips row
                            with ui.row().classes('gap-2 flex-wrap mb-3'):
                                with ui.element('span').classes('chip'):
                                    ui.icon('inventory_2').style('font-size:11px;margin-right:3px')
                                    ui.label(job['pack_type'])
                                with ui.element('span').classes('chip'):
                                    ui.icon('numbers').style('font-size:11px;margin-right:3px')
                                    ui.label(f'{job["units"]} units')

                            # Footer: order ref + action
                            ui.element('div').classes('divider mt-0 mb-2')
                            with ui.row().classes('items-center justify-between'):
                                ui.label(job['order']).classes('text-xs text-faint')
                                ui.button(action_label, color='white',
                                          on_click=lambda jid=job['id'], t=action_type, ti=action_title:
                                          notify(f'{jid} — {ti.lower()}', type=t, title=ti),
                                          ).props('flat no-caps').classes(f'button {action_cls} button-sm')
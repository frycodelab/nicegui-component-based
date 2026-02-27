"""Application shell — top header bar, collapsible sidebar and active-link tracking."""

from contextlib import contextmanager

from nicegui import ui, app


@contextmanager
def frame(title: str, version: str, get_logo_func=None):

    # ── Sidebar toggle — persists collapsed state in user session storage ───────────
    async def toggle_sidebar():
        app.storage.user['sidebar-collapsed'] = not app.storage.user['sidebar-collapsed']

        if app.storage.user['sidebar-collapsed']:
            left_drawer.props("width=300")
            corps.text = "Collapse"
            corps.icon = "chevron_left"
            await ui.run_javascript('new Promise(resolve => setTimeout(resolve, 50))')
            for label in sidebar_labels:
                label.classes(remove='collapsed', add='expanded')
        else:
            for label in sidebar_labels:
                label.classes(remove='expanded', add='collapsed')
            await ui.run_javascript('new Promise(resolve => setTimeout(resolve, 50))')
            left_drawer.props("width=100")
            corps.text = ""
            corps.icon = "chevron_right"

    # ── Header toolbar ─────────────────────────────────────────────────────────────────
    with ui.header().classes(replace='row items-center h-20 justify-start') as header:
        ui.label("").classes('pr-4')
        ui.html('<div style="width: 4rem; height: 4rem; background-image: url(\'/assets/images/logo.png\'); background-size: contain; background-repeat: no-repeat; background-position: center;"></div>', sanitize=False)
        ui.label("").classes("pr-2")
        ui.label(title).classes('app-name')
        ui.space()
        with ui.dropdown_button('', icon='account_circle').classes('mr-4 header-account-btn').props('flat push no-icon-animation auto-close unelevated'):
            with ui.element('div').classes('account-dropdown'):
                ui.label('John Doe').classes('account-name')
                ui.element('div').classes('account-separator')
                with ui.row().classes('account-menu-item').style('min-height: 48px;').on('click', lambda e: ui.notify('Account clicked')):
                    ui.icon('person').classes('account-icon')
                    ui.label('Account')
                with ui.row().classes('account-menu-item').style('min-height: 48px;').on('click', lambda e: ui.navigate.to('/settings')):
                    ui.icon('settings').classes('account-icon')
                    ui.label('Settings')
                ui.element('div').classes('account-separator')
                with ui.row().classes('account-menu-item logout').style('min-height: 48px;').on('click', lambda e: ui.notify('Logout clicked')):
                    ui.icon('logout').classes('account-icon')
                    ui.label('Logout')

    header.style('background-color: #F8FAFD;')

    # ── Sidebar nav ──────────────────────────────────────────────────────────────────
    with ui.left_drawer().classes('text-black relative').style('background-color: #F8FAFD; transition: width 0.3s ease-in-out;').props('breakpoint=400') as left_drawer:

        sidebar_labels = []
        nav_links = []

        with ui.link('', '/').classes('w-full no-underline text-black').style('border-radius: 2rem;') as dashboard_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                dashboard_icon = ui.icon('dashboard').classes('ml-5 text-2xl flex-shrink-0')
                dashboard_label = ui.label('Dashboard').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(dashboard_label)
        nav_links.append({'link': dashboard_link, 'icon': dashboard_icon, 'patterns': ['/'], 'exact': True})

        with ui.link('', '/shipping').classes('w-full no-underline text-black').style('border-radius: 2rem;') as shipping_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                shipping_icon = ui.icon('local_shipping').classes('ml-5 text-2xl flex-shrink-0')
                shipping_label = ui.label('Shipping').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(shipping_label)
        nav_links.append({'link': shipping_link, 'icon': shipping_icon, 'patterns': ['/shipping', '/customer'], 'exact': False})

        with ui.link('', '/production').classes('w-full no-underline text-black').style('border-radius: 2rem;') as production_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                production_icon = ui.icon('precision_manufacturing').classes('ml-5 text-2xl flex-shrink-0')
                production_label = ui.label('Production').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(production_label)
        nav_links.append({'link': production_link, 'icon': production_icon, 'patterns': ['/production'], 'exact': False})

        with ui.link('', '/orders').classes('w-full no-underline text-black').style('border-radius: 2rem;') as orders_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                orders_icon = ui.icon('fact_check').classes('ml-5 text-2xl flex-shrink-0')
                orders_label = ui.label('Orders').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(orders_label)
        nav_links.append({'link': orders_link, 'icon': orders_icon, 'patterns': ['/orders'], 'exact': False})

        with ui.link('', '/pallets').classes('w-full no-underline text-black').style('border-radius: 2rem;') as pallets_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                pallets_icon = ui.icon('pallet').classes('ml-5 text-2xl flex-shrink-0')
                pallets_label = ui.label('Pallets').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(pallets_label)
        nav_links.append({'link': pallets_link, 'icon': pallets_icon, 'patterns': ['/pallets'], 'exact': False})

        with ui.link('', '/packing').classes('w-full no-underline text-black').style('border-radius: 2rem;') as packing_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                packing_icon = ui.icon('inventory_2').classes('ml-5 text-2xl flex-shrink-0')
                packing_label = ui.label('Packing').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(packing_label)
        nav_links.append({'link': packing_link, 'icon': packing_icon, 'patterns': ['/packing'], 'exact': False})

        with ui.link('', '/print-demo').classes('w-full no-underline text-black').style('border-radius: 2rem;') as print_demo_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                print_demo_icon = ui.icon('print').classes('ml-5 text-2xl flex-shrink-0')
                print_demo_label = ui.label('Print Demo').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(print_demo_label)
        nav_links.append({'link': print_demo_link, 'icon': print_demo_icon, 'patterns': ['/print-demo'], 'exact': False})


        ui.separator()

        with ui.link('', '/icons').classes('w-full no-underline text-black').style('border-radius: 2rem;') as icons_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                icons_icon = ui.icon('grid_view').classes('ml-5 text-2xl flex-shrink-0')
                icons_label = ui.label('Icons').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(icons_label)
        nav_links.append({'link': icons_link, 'icon': icons_icon, 'patterns': ['/icons'], 'exact': False})



        with ui.link('', '/design-system').classes('w-full no-underline text-black').style('border-radius: 2rem;') as design_system_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                design_system_icon = ui.icon('palette').classes('ml-5 text-2xl flex-shrink-0')
                design_system_label = ui.label('Design System').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                sidebar_labels.append(design_system_label)
        nav_links.append({'link': design_system_link, 'icon': design_system_icon, 'patterns': ['/design-system'], 'exact': False})

        corps = ui.button("Collapse", icon='chevron_left').classes('absolute bottom-4 right-4 transition-all duration-300').props('flat').on('click', lambda: toggle_sidebar())

        def apply_highlight(active_item) -> None:
            for item in nav_links:
                item['link'].classes(remove='nav-link-active')
                item['icon'].classes(remove='nav-icon-active')
            active_item['link'].classes(add='nav-link-active')
            active_item['icon'].classes(add='nav-icon-active')

        # Instant highlight on click — no polling, no round-trip
        for nav_item in nav_links:
            nav_item['link'].on('click', lambda _, i=nav_item: apply_highlight(i))

        # One-shot JS call on first load to highlight the correct item on direct URL access
        async def init_highlight() -> None:
            path = await ui.run_javascript('window.location.pathname')
            for item in nav_links:
                for pattern in item['patterns']:
                    match = (path == pattern) if item['exact'] else (path == pattern or path.startswith(pattern + '/'))
                    if match:
                        apply_highlight(item)
                        return

        ui.timer(0, init_highlight, once=True)

    # ── Sync drawer width and label visibility to the persisted state ────────────
    if app.storage.user['sidebar-collapsed']:
        left_drawer.props("width=300")
        corps.text = "Collapse"
        corps.icon = "chevron_left"
        for label in sidebar_labels:
            label.classes(add='expanded')
    else:
        left_drawer.props("width=100")
        corps.text = ""
        corps.icon = "chevron_right"
        for label in sidebar_labels:
            label.classes(add='collapsed')

    with ui.column().classes('w-full items-stretch'):
        yield
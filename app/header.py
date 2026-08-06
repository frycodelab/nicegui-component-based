"""Application shell: header bar, collapsible sidebar and active-link tracking."""

from contextlib import contextmanager
from components.notifications import notify, notify_ongoing
from components.sidebar_hint import sidebar_hint
from nicegui import ui, app
from core.security import logout, current_user
from services import i18n


# Sections surfaced through the mobile burger sheet, beyond the 3 primary tabs
_SHEET_SECTIONS = [
    ('nav.orders',        'fact_check',  '/orders'),
    ('nav.pallets',       'pallet',      '/pallets'),
    ('nav.packing',       'inventory_2', '/packing'),
    ('nav.print_demo',    'print',       '/print-demo'),
    ('nav.icons',         'grid_view',   '/icons'),
    ('nav.design_system', 'palette',     '/design-system'),
]


@contextmanager
def frame(title: str, version: str, get_logo_func=None):

    # persists collapsed state in user session storage
    async def toggle_sidebar():
        app.storage.user['sidebar-collapsed'] = not app.storage.user['sidebar-collapsed']

        if app.storage.user['sidebar-collapsed']:
            left_drawer.props("width=240")
            corps.text = i18n.t('action.collapse')
            corps.icon = "chevron_left"
            await ui.run_javascript('new Promise(resolve => setTimeout(resolve, 50))')
            for label in sidebar_labels:
                label.classes(remove='collapsed', add='expanded')
            for tip in sidebar_hints:
                tip.set_visibility(False)
        else:
            for label in sidebar_labels:
                label.classes(remove='expanded', add='collapsed')
            for tip in sidebar_hints:
                tip.set_visibility(True)
            await ui.run_javascript('new Promise(resolve => setTimeout(resolve, 50))')
            left_drawer.props("width=100")
            corps.text = ""
            corps.icon = "chevron_right"

    # Header toolbar
    with ui.header().classes(replace='row items-center h-20 justify-start') as header:
        ui.label("").classes('pr-4 md:pr-8')
        ui.html('<div style="width: 4rem; height: 4rem; background-image: url(\'/assets/images/logo.png\'); background-size: contain; background-repeat: no-repeat; background-position: center;"></div>', sanitize=False)
        ui.label("").classes("pr-2")
        ui.label(title).classes('app-name')
        ui.space()
        with i18n.bind_language_name(ui.dropdown_button('', icon='language').classes('mr-2 header-lang-btn').props('flat push no-icon-animation auto-close unelevated')):
            with ui.element('div').classes('account-dropdown'):
                i18n.bind(ui.label(i18n.t('language.label')).classes('account-name'), 'language.label')
                ui.element('div').classes('account-separator')
                for _code, _name in i18n.LANGUAGES.items():
                    with ui.row().classes('account-menu-item').style('min-height: 44px;').on(
                        'click', lambda _, c=_code: i18n.set_language(c)
                    ):
                        ui.label(_name)
        with ui.dropdown_button('', icon='account_circle').classes('mr-4 header-account-btn').props('flat push no-icon-animation auto-close unelevated'):
            me = current_user()
            with ui.element('div').classes('account-dropdown'):
                ui.label(me.username if me else 'Guest').classes('account-name')
                ui.element('div').classes('account-separator')
                with ui.row().classes('account-menu-item').style('min-height: 48px;').on('click', lambda: ui.navigate.to('/account')):
                    ui.icon('person').classes('account-icon')
                    i18n.bind(ui.label(i18n.t('account.account')), 'account.account')
                if me and me.is_admin:
                    with ui.row().classes('account-menu-item').style('min-height: 48px;').on('click', lambda: ui.navigate.to('/users')):
                        ui.icon('group').classes('account-icon')
                        i18n.bind(ui.label(i18n.t('nav.users')), 'nav.users')
                    with ui.row().classes('account-menu-item').style('min-height: 48px;').on('click', lambda: ui.navigate.to('/settings')):
                        ui.icon('tune').classes('account-icon')
                        i18n.bind(ui.label(i18n.t('appsettings.title')), 'appsettings.title')
                ui.element('div').classes('account-separator')
                with ui.row().classes('account-menu-item logout').style('min-height: 48px;').on('click', lambda e: logout()):
                    ui.icon('logout').classes('account-icon')
                    i18n.bind(ui.label(i18n.t('account.logout')), 'account.logout')

    header.style('background-color: #F8FAFD;')

    # Sidebar nav
    with ui.left_drawer().classes('text-black relative').style('background-color: #F8FAFD; transition: width 0.3s ease-in-out;').props('breakpoint=1024') as left_drawer:

        sidebar_labels = []
        nav_links = []
        sidebar_hints = []

        with ui.link('', '/').classes('w-full no-underline text-black').style('border-radius: 2rem;') as dashboard_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                dashboard_icon = ui.icon('dashboard').classes('ml-5 text-2xl flex-shrink-0')
                dashboard_label = i18n.bind(ui.label('Dashboard').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.dashboard')
                sidebar_labels.append(dashboard_label)
            sidebar_hints.append(sidebar_hint('nav.dashboard'))
        nav_links.append({'link': dashboard_link, 'icon': dashboard_icon, 'patterns': ['/'], 'exact': True})

        with ui.link('', '/shipping').classes('w-full no-underline text-black').style('border-radius: 2rem;') as shipping_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                shipping_icon = ui.icon('local_shipping').classes('ml-5 text-2xl flex-shrink-0')
                shipping_label = i18n.bind(ui.label('Shipping').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.shipping')
                sidebar_labels.append(shipping_label)
            sidebar_hints.append(sidebar_hint('nav.shipping'))
        nav_links.append({'link': shipping_link, 'icon': shipping_icon, 'patterns': ['/shipping', '/customer'], 'exact': False})

        with ui.link('', '/production').classes('w-full no-underline text-black').style('border-radius: 2rem;') as production_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                production_icon = ui.icon('precision_manufacturing').classes('ml-5 text-2xl flex-shrink-0')
                production_label = i18n.bind(ui.label('Production').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.production')
                sidebar_labels.append(production_label)
            sidebar_hints.append(sidebar_hint('nav.production'))
        nav_links.append({'link': production_link, 'icon': production_icon, 'patterns': ['/production'], 'exact': False})

        with ui.link('', '/orders').classes('w-full no-underline text-black').style('border-radius: 2rem;') as orders_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                orders_icon = ui.icon('fact_check').classes('ml-5 text-2xl flex-shrink-0')
                orders_label = i18n.bind(ui.label('Orders').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.orders')
                sidebar_labels.append(orders_label)
            sidebar_hints.append(sidebar_hint('nav.orders'))
        nav_links.append({'link': orders_link, 'icon': orders_icon, 'patterns': ['/orders'], 'exact': False})

        with ui.link('', '/pallets').classes('w-full no-underline text-black').style('border-radius: 2rem;') as pallets_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                pallets_icon = ui.icon('pallet').classes('ml-5 text-2xl flex-shrink-0')
                pallets_label = i18n.bind(ui.label('Pallets').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.pallets')
                sidebar_labels.append(pallets_label)
            sidebar_hints.append(sidebar_hint('nav.pallets'))
        nav_links.append({'link': pallets_link, 'icon': pallets_icon, 'patterns': ['/pallets'], 'exact': False})

        with ui.link('', '/packing').classes('w-full no-underline text-black').style('border-radius: 2rem;') as packing_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                packing_icon = ui.icon('inventory_2').classes('ml-5 text-2xl flex-shrink-0')
                packing_label = i18n.bind(ui.label('Packing').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.packing')
                sidebar_labels.append(packing_label)
            sidebar_hints.append(sidebar_hint('nav.packing'))
        nav_links.append({'link': packing_link, 'icon': packing_icon, 'patterns': ['/packing'], 'exact': False})

        with ui.link('', '/print-demo').classes('w-full no-underline text-black').style('border-radius: 2rem;') as print_demo_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                print_demo_icon = ui.icon('print').classes('ml-5 text-2xl flex-shrink-0')
                print_demo_label = i18n.bind(ui.label('Print Demo').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.print_demo')
                sidebar_labels.append(print_demo_label)
            sidebar_hints.append(sidebar_hint('nav.print_demo'))
        nav_links.append({'link': print_demo_link, 'icon': print_demo_icon, 'patterns': ['/print-demo'], 'exact': False})


        ui.separator()

        with ui.link('', '/icons').classes('w-full no-underline text-black').style('border-radius: 2rem;') as icons_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                icons_icon = ui.icon('grid_view').classes('ml-5 text-2xl flex-shrink-0')
                icons_label = i18n.bind(ui.label('Icons').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.icons')
                sidebar_labels.append(icons_label)
            sidebar_hints.append(sidebar_hint('nav.icons'))
        nav_links.append({'link': icons_link, 'icon': icons_icon, 'patterns': ['/icons'], 'exact': False})


        with ui.link('', '/design-system').classes('w-full no-underline text-black').style('border-radius: 2rem;') as design_system_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                design_system_icon = ui.icon('palette').classes('ml-5 text-2xl flex-shrink-0')
                design_system_label = i18n.bind(ui.label('Design System').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.design_system')
                sidebar_labels.append(design_system_label)
            sidebar_hints.append(sidebar_hint('nav.design_system'))
        nav_links.append({'link': design_system_link, 'icon': design_system_icon, 'patterns': ['/design-system'], 'exact': False})
        

        if me and me.is_admin:
            with ui.link('', '/users').classes('w-full no-underline text-black').style('border-radius: 2rem;') as users_link:
                with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                    users_icon = ui.icon('group').classes('ml-5 text-2xl flex-shrink-0')
                    users_label = i18n.bind(ui.label('Users').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'nav.users')
                    sidebar_labels.append(users_label)
                sidebar_hints.append(sidebar_hint('nav.users'))
            nav_links.append({'link': users_link, 'icon': users_icon, 'patterns': ['/users'], 'exact': False})

            with ui.link('', '/settings').classes('w-full no-underline text-black').style('border-radius: 2rem;') as settings_link:
                with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                    settings_icon = ui.icon('tune').classes('ml-5 text-2xl flex-shrink-0')
                    settings_label = i18n.bind(ui.label('App Settings').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'appsettings.title')
                    sidebar_labels.append(settings_label)
                sidebar_hints.append(sidebar_hint('appsettings.title'))
            nav_links.append({'link': settings_link, 'icon': settings_icon, 'patterns': ['/settings'], 'exact': False})

            with ui.link('', '/audit').classes('w-full no-underline text-black').style('border-radius: 2rem;') as audit_link:
                with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                    audit_icon = ui.icon('history').classes('ml-5 text-2xl flex-shrink-0')
                    audit_label = i18n.bind(ui.label('Audit Log').classes('text-lg sidebar-label ml-3 flex-shrink-0'), 'audit.title')
                    sidebar_labels.append(audit_label)
                sidebar_hints.append(sidebar_hint('audit.title'))
            nav_links.append({'link': audit_link, 'icon': audit_icon, 'patterns': ['/audit'], 'exact': False})

        ui.separator()

        with ui.link(target='https://github.com/frycodelab/nicegui-component-based', new_tab=True).classes('w-full no-underline text-black').style('border-radius: 2rem;') as github_link:
            with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                with ui.element('div').classes('ml-8 flex-shrink-0').style('width: 2rem; height: 2rem; display: flex; align-items: center; justify-content: center;'):
                    ui.image('/assets/images/GitHub_Invertocat_Black_Clearspace.svg').style('width: 2rem; height: auto;')
                github_label = ui.label('GitHub').classes(f'text-lg sidebar-label ml-2 flex-shrink-0')
                sidebar_labels.append(github_label)
            sidebar_hints.append(sidebar_hint('GitHub', translate=False))

        with ui.column().classes('absolute bottom-2 right-4 items-end gap-0'):
            corps = ui.button(i18n.t('action.collapse'), icon='chevron_left').classes('transition-all duration-300').props('flat').on('click', lambda: toggle_sidebar())
            version_label = ui.label(version).classes('text-xs text-muted sidebar-label mr-2')
            sidebar_labels.append(version_label)

        def apply_highlight(active_item) -> None:
            for item in nav_links:
                item['link'].classes(remove='nav-link-active')
                item['icon'].classes(remove='nav-icon-active')
            active_item['link'].classes(add='nav-link-active')
            active_item['icon'].classes(add='nav-icon-active')

        # highlight on click without a server round-trip
        for nav_item in nav_links:
            nav_item['link'].on('click', lambda _, i=nav_item: apply_highlight(i))

        # highlight the correct item when a page is opened via a direct URL
        async def init_highlight() -> None:
            try:
                path = await ui.run_javascript('window.location.pathname')
            except Exception:
                return
            for item in nav_links:
                for pattern in item['patterns']:
                    match = (path == pattern) if item['exact'] else (path == pattern or path.startswith(pattern + '/'))
                    if match:
                        apply_highlight(item)
                        return

        # on_connect fires only for a real WebSocket, so bots never reach this
        ui.context.client.on_connect(init_highlight)

    # sync drawer width and label visibility to the persisted state
    if app.storage.user['sidebar-collapsed']:
        left_drawer.props("width=240")
        corps.text = i18n.t('action.collapse')
        corps.icon = "chevron_left"
        for label in sidebar_labels:
            label.classes(add='expanded')
        for tip in sidebar_hints:
            tip.set_visibility(False)
    else:
        left_drawer.props("width=100")
        corps.text = ""
        corps.icon = "chevron_right"
        for label in sidebar_labels:
            label.classes(add='collapsed')
        for tip in sidebar_hints:
            tip.set_visibility(True)

    with ui.column().classes('w-full items-stretch mobile-content'):
        yield

    # About dialog
    with ui.dialog() as about_dialog, ui.card().classes('dialog-card'):
        i18n.bind(ui.label(i18n.t('about.title')).classes('dialog-title'), 'about.title')
        i18n.bind(ui.label(i18n.t('about.body')).classes('dialog-body'), 'about.body')
        with ui.element('div').classes('dialog-body'):
            i18n.bind(ui.label(i18n.t('about.source')).classes('text-sm text-muted mb-2'), 'about.source')
            i18n.bind(ui.link(i18n.t('about.repo'), 'https://github.com/frycodelab/nicegui-component-based', new_tab=True).classes('text-info').style('text-decoration: underline;'), 'about.repo')
        with ui.element('div').classes('dialog-footer'):
            i18n.bind(ui.button(i18n.t('action.close'), on_click=about_dialog.close, color='white').props('flat no-caps').classes('button button-primary button-sm'), 'action.close')

    # Mobile burger sheet with the remaining sections, hidden on desktop
    with ui.dialog().props('position=bottom') as menu_sheet, ui.card().classes('mobile-sheet'):
        ui.element('div').classes('mobile-sheet-handle')
        i18n.bind(ui.label(i18n.t('menu.all_sections')).classes('mobile-sheet-title'), 'menu.all_sections')
        with ui.element('div').classes('mobile-sheet-grid'):
            for label_key, icon_name, target in _SHEET_SECTIONS:
                with ui.element('div').classes('mobile-sheet-item').on('click', lambda _, t=target: [menu_sheet.close(), ui.navigate.to(t)]):
                    ui.icon(icon_name).classes('mobile-sheet-icon')
                    i18n.bind(ui.label(i18n.t(label_key)).classes('mobile-sheet-label'), label_key)
            with ui.element('div').classes('mobile-sheet-item').on('click', lambda: [menu_sheet.close(), about_dialog.open()]):
                ui.icon('info').classes('mobile-sheet-icon')
                i18n.bind(ui.label(i18n.t('menu.about')).classes('mobile-sheet-label'), 'menu.about')

        # Account actions, moved here from the top bar on mobile
        i18n.bind(ui.label(i18n.t('account.account')).classes('mobile-sheet-title').style('margin-top: 20px;'),
                  'account.account')
        with ui.element('div').classes('mobile-sheet-grid'):
            with ui.element('div').classes('mobile-sheet-item').on('click', lambda: [menu_sheet.close(), ui.navigate.to('/account')]):
                ui.icon('person').classes('mobile-sheet-icon')
                i18n.bind(ui.label(i18n.t('account.settings')).classes('mobile-sheet-label'), 'account.settings')
            if me and me.is_admin:
                with ui.element('div').classes('mobile-sheet-item').on('click', lambda: [menu_sheet.close(), ui.navigate.to('/users')]):
                    ui.icon('group').classes('mobile-sheet-icon')
                    i18n.bind(ui.label(i18n.t('nav.users')).classes('mobile-sheet-label'), 'nav.users')
                with ui.element('div').classes('mobile-sheet-item').on('click', lambda: [menu_sheet.close(), ui.navigate.to('/settings')]):
                    ui.icon('tune').classes('mobile-sheet-icon')
                    i18n.bind(ui.label(i18n.t('appsettings.title')).classes('mobile-sheet-label'), 'appsettings.title')
                with ui.element('div').classes('mobile-sheet-item').on('click', lambda: [menu_sheet.close(), ui.navigate.to('/audit')]):
                    ui.icon('history').classes('mobile-sheet-icon')
                    i18n.bind(ui.label(i18n.t('audit.title')).classes('mobile-sheet-label'), 'audit.title')
            with ui.element('div').classes('mobile-sheet-item').on('click', lambda: [menu_sheet.close(), logout()]):
                ui.icon('logout').classes('mobile-sheet-icon')
                i18n.bind(ui.label(i18n.t('account.logout')).classes('mobile-sheet-label'), 'account.logout')

    # Floating bottom navigation, shown only below the desktop breakpoint via CSS
    mobile_nav = []
    with ui.element('div').classes('mobile-nav-floating'):
        with ui.link('', '/').classes('mobile-nav-item') as m_home:
            ui.icon('dashboard').classes('mobile-nav-icon')
            i18n.bind(ui.label(i18n.t('nav.home')).classes('mobile-nav-label'), 'nav.home')
        mobile_nav.append({'el': m_home, 'nav': True, 'patterns': ['/'], 'exact': True})

        with ui.link('', '/shipping').classes('mobile-nav-item') as m_ship:
            ui.icon('local_shipping').classes('mobile-nav-icon')
            i18n.bind(ui.label(i18n.t('nav.shipping')).classes('mobile-nav-label'), 'nav.shipping')
        mobile_nav.append({'el': m_ship, 'nav': True, 'patterns': ['/shipping', '/customer'], 'exact': False})

        with ui.link('', '/production').classes('mobile-nav-item') as m_prod:
            ui.icon('precision_manufacturing').classes('mobile-nav-icon')
            i18n.bind(ui.label(i18n.t('nav.production')).classes('mobile-nav-label'), 'nav.production')
        mobile_nav.append({'el': m_prod, 'nav': True, 'patterns': ['/production'], 'exact': False})

        with ui.element('div').classes('mobile-nav-item').on('click', lambda: menu_sheet.open()) as m_menu:
            ui.icon('menu').classes('mobile-nav-icon')
            i18n.bind(ui.label(i18n.t('menu.menu')).classes('mobile-nav-label'), 'menu.menu')
        mobile_nav.append({'el': m_menu, 'nav': False,
                           'patterns': [t for _, _, t in _SHEET_SECTIONS], 'exact': False})

    def apply_mobile_highlight(active_item) -> None:
        for item in mobile_nav:
            item['el'].classes(remove='mobile-nav-active')
        active_item['el'].classes(add='mobile-nav-active')

    # highlight on tap for the real destinations; the burger only opens a sheet
    for item in mobile_nav:
        if item['nav']:
            item['el'].on('click', lambda _, i=item: apply_mobile_highlight(i))

    async def init_mobile_highlight() -> None:
        try:
            path = await ui.run_javascript('window.location.pathname')
        except Exception:
            return
        for item in mobile_nav:
            for pattern in item['patterns']:
                match = (path == pattern) if item['exact'] else (path == pattern or path.startswith(pattern + '/'))
                if match:
                    apply_mobile_highlight(item)
                    return

    ui.context.client.on_connect(init_mobile_highlight)
from contextlib import contextmanager
from nicegui import ui, app

@contextmanager
def frame(title: str, version : str, get_logo_func=None):

    current_route = ui.context.client.page.path
    
    async def toggle_sidebar():
        app.storage.user['sidebar-collapsed'] = not app.storage.user['sidebar-collapsed']
        
        if app.storage.user['sidebar-collapsed']:
            # Expanding: Adjust width first, then show labels
            left_drawer.props("width=300")
            corps.text = "Collapse"
            corps.icon = "chevron_left"
            
            # Small delay then show labels
            await ui.run_javascript('new Promise(resolve => setTimeout(resolve, 50))')
            
            for label in sidebar_labels:
                label.classes(remove='collapsed', add='expanded')
        else:
            # Collapsing: Hide labels first, then adjust width
            for label in sidebar_labels:
                label.classes(remove='expanded', add='collapsed')
            
            # Wait for label fade out animation
            await ui.run_javascript('new Promise(resolve => setTimeout(resolve, 50))')
            
            left_drawer.props("width=100")
            corps.text = ""
            corps.icon = "chevron_right"

    """Custom page frame to share the same styling and behavior across all pages"""
    with ui.header().classes(replace='row items-center h-16 justify-start') as header:
        ui.label("").tailwind("pr-4")
        # Use CSS background image for better performance and no flicker
        ui.html('<div style="width: 5rem; height: 5rem; background-image: url(\'/assets/images/logo.png\'); background-size: contain; background-repeat: no-repeat; background-position: center;"></div>')
        ui.label("").tailwind("px-0.5")
        ui.label(title).classes('app-name')
        #badge = ui.badge(version, color="grey").style("margin-left: 0.5rem;").props("outline size=0.6rem align='top'")
        ui.space()
        # Modern account dropdown styled for the app (menu look)
        with ui.dropdown_button('', icon='account_circle', color='#004A77').classes('mr-4 mb-2').props('flat push no-icon-animation auto-close') as account_dropdown:

            with ui.element('div').classes('account-dropdown'):
                # Display Name
                ui.label('John Doe').classes('account-name')

                # Divider
                ui.element('div').classes('account-separator')

                # Account Item
                with ui.row().classes('account-menu-item').style('min-height: 48px;').on('click', lambda e: ui.notify('Account clicked')):
                    ui.icon('person').classes('account-icon')
                    ui.label('Account')

                # Settings Item
                with ui.row().classes('account-menu-item').style('min-height: 48px;').on('click', lambda e: ui.navigate.to('/settings')):
                    ui.icon('settings').classes('account-icon')
                    ui.label('Settings')

                # Divider
                ui.element('div').classes('account-separator')

                # Logout Item
                with ui.row().classes('account-menu-item logout').style('min-height: 48px;').on('click', lambda e: ui.notify('Logout clicked')):
                    ui.icon('logout').classes('account-icon')
                    ui.label('Logout')
        
    header.style('background-color: #F8FAFD;')
    
    with ui.left_drawer().classes('text-black relative').style('background-color: #F8FAFD; transition: width 0.3s ease-in-out;').props('breakpoint=400') as left_drawer:
                
                # Store references to labels for smooth toggle
                sidebar_labels = []
                
                '''
                with ui.dropdown_button('Neu', icon='add', color='white').props('flat push fab no-icon-animation auto-close').style('box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); border-radius:20px; ').classes('mb-2'):
                        with ui.column():
                            with ui.button().classes('cursor-pointer w-full mt-4').props('flat').style('border-radius: 0;'):
                                    with ui.row().classes('w-full'):
                                        ui.icon('person_add')
                                        ui.label('Neues item anlegen').style('color: black; font-size: 0.8rem; font-weight: 500;')
                '''

                with ui.link('', '/').classes(f'w-full no-underline text-black {"bg-light-blue-2" if current_route == "/" else ""}').style('border-radius: 2rem;'):
                    with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                        ui.icon('dashboard').classes(f'ml-5 text-2xl flex-shrink-0').style(f'{"color:#004A77;" if current_route == "/" else ""}')
                        dashborad_label = ui.label('Dashboard').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                        sidebar_labels.append(dashborad_label)

                with ui.link('', '/shipping').classes(f'w-full no-underline text-black {"bg-light-blue-3" if current_route.startswith("/shipping") or current_route.startswith("/customer") else ""}').style('border-radius: 2rem;'):
                    with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                        ui.icon('local_shipping').classes('ml-5 text-2xl flex-shrink-0').style(f'{"color:#004A77;" if current_route.startswith("/shipping") or current_route.startswith("/customer") else ""}')
                        shipping_label = ui.label('Shipping').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                        sidebar_labels.append(shipping_label)

                with ui.link('', '/production').classes(f'w-full no-underline text-black {"bg-light-blue-3" if current_route.startswith("/production") else ""}').style('border-radius: 2rem;'):
                    with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                        ui.icon('precision_manufacturing').classes('ml-5 text-2xl flex-shrink-0').style(f'{"color:#004A77;" if current_route.startswith("/production") else ""}')
                        production_label = ui.label('Production').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                        sidebar_labels.append(production_label)

                with ui.link('', '/orders').classes(f'w-full no-underline text-black {"bg-light-blue-3" if current_route.startswith("/orders") else ""}').style('border-radius: 2rem;'):
                    with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                        ui.icon('fact_check').classes('ml-5 text-2xl flex-shrink-0').style(f'{"color:#004A77;" if current_route.startswith("/orders") else ""}')
                        orders_label = ui.label('Orders').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                        sidebar_labels.append(orders_label)

                with ui.link('', '/pallets').classes(f'w-full no-underline text-black {"bg-light-blue-3" if current_route.startswith("/pallets") else ""}').style('border-radius: 2rem;'):
                    with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                        ui.icon('pallet').classes('ml-5 text-2xl flex-shrink-0').style(f'{"color:#004A77;" if current_route.startswith("/pallets") else ""}')
                        pallets_label = ui.label('Paletts').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                        sidebar_labels.append(pallets_label)

                with ui.link('', '/packing').classes(f'w-full no-underline text-black {"bg-light-blue-3" if current_route.startswith("/packing") else ""}').style('border-radius: 2rem;'):
                    with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                        ui.icon('inventory_2').classes('ml-5 text-2xl flex-shrink-0').style(f'{"color:#004A77;" if current_route.startswith("/packing") else ""}')
                        packing_label = ui.label('Packing').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                        sidebar_labels.append(packing_label)
                
                ui.separator()

                with ui.link('', '/settings').classes(f'w-full no-underline text-black {"bg-light-blue-3" if current_route.startswith("/settings") else ""}').style('border-radius: 2rem;'):
                    with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
                        ui.icon('settings').classes('ml-5 text-2xl flex-shrink-0').style(f'{"color:#004A77;" if current_route.startswith("/settings") else ""}')
                        settings_label = ui.label('Settings').classes('text-lg sidebar-label ml-3 flex-shrink-0')
                        sidebar_labels.append(settings_label)

                corps = ui.button("Collapse", icon='chevron_left').classes('absolute bottom-4 right-4 transition-all duration-300').props('flat').on('click', lambda: toggle_sidebar())

    # Initialize sidebar state
    if app.storage.user['sidebar-collapsed']:
        # Expanded state
        left_drawer.props("width=300")
        corps.text = "Collapse"
        corps.icon = "chevron_left"
        for label in sidebar_labels:
            label.classes(add='expanded')
    else:
        # Collapsed state
        left_drawer.props("width=100")
        corps.text = ""
        corps.icon = "chevron_right"
        for label in sidebar_labels:
            label.classes(add='collapsed')

    with ui.column().classes('items-center w-full'):
        yield
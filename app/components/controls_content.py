from nicegui import ui, app


def content() -> None:
        with ui.card().classes('w-full'):

                ui.markdown("**Expansion**")

                with ui.expansion(value=True).classes('w-full fro-accordion') as general_data:
                    
                    with general_data.add_slot('header'):

                            with ui.row().classes('w-full'):
                                    ui.icon("calendar_today").classes('text-2xl')
                                    ui.label("OVERVIEW").tailwind("pt-1")

                    ui.label("Your Content 1")

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Buttons**")

                with ui.row().classes('gap-2'):
                    with ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):
                        badge = ui.badge('0', color='red').props('floating')

                    with ui.dropdown_button('Open me!', auto_close=True):
                        ui.item('Item 1', on_click=lambda: ui.notify('You clicked item 1'))
                        ui.item('Item 2', on_click=lambda: ui.notify('You clicked item 2'))

                    ui.radio(['x', 'y', 'z'], value='x').props('inline color=green')
                    ui.button(icon='touch_app').props('outline round').classes('shadow-lg')
                    ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Chips**")

                with ui.row().classes('gap-1'):
                    ui.chip('Click me', icon='ads_click', on_click=lambda: ui.notify('Clicked'))
                    ui.chip('Selectable', selectable=True, icon='bookmark', color='orange')
                    ui.chip('Removable', removable=True, icon='label', color='indigo-3')
                    ui.chip('Styled', icon='star', color='green').props('outline square')
                    ui.chip('Disabled', icon='block', color='red').set_enabled(False)

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Toggle**")

                toggle1 = ui.toggle([1, 2, 3], value=1)
                toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Radio Selection**")

                radio1 = ui.radio([1, 2, 3], value=1).props('inline')
                radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Dropdown Selection**")

                select1 = ui.select([1, 2, 3], value=1)
                select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Switch/Checkbox**")

                checkbox = ui.checkbox('check me')
                ui.label('Check!').bind_visibility_from(checkbox, 'value')

                switch = ui.switch('switch me')
                ui.label('Switch!').bind_visibility_from(switch, 'value')

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Sliders**")

                slider = ui.slider(min=0, max=100, value=50)
                ui.label().bind_text_from(slider, 'value')

                min_max_range = ui.range(min=0, max=100, value={'min': 20, 'max': 80})
                ui.label().bind_text_from(min_max_range, 'value',
                                        backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')
                
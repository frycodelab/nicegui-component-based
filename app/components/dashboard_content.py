from nicegui import ui, app
import random
import services.helpers as helpers

def content() -> None:
        
        ui.label('Welcome to the Dashboard').style('font-size: 1.5rem;').style('font-weight: 400;')

        with ui.card().classes('plot-card w-full mt-4'):
                chart = ui.highchart({
                'title': False,
                'chart': {'type': 'bar'},
                'xAxis': {'categories': ['A', 'B']},
                'series': [
                        {'name': 'Alpha', 'data': [0.1, 0.2]},
                        {'name': 'Beta', 'data': [0.3, 0.4]},
                ],
                }).classes('w-full h-64')

                async def update():
                        chart.options['series'][0]['data'][0] = random.random()
                        ui.notify(await helpers.dummy_function())
                        chart.update()

                with ui.row().classes('w-full items-center justify-end'):
                        ui.button('Delete', on_click= lambda : ui.notify('Item was deleted...')).props('flat no-caps').classes('google-like-button secondary')
                        ui.button('Cancel', on_click= lambda : ui.notify('Task was canceled...')).props('flat no-caps').classes('google-like-button tertiary')
                        ui.button('Update', on_click=update).props("").props('flat no-caps').classes('google-like-button primary')
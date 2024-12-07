from nicegui import ui, app
from random import random

def content() -> None:

        with ui.card().classes('w-full'):

                ui.markdown("**Spinner**")

                with ui.row():
                    ui.spinner(size='lg')
                    ui.spinner('audio', size='lg', color='green')
                    ui.spinner('dots', size='lg', color='red')

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Chart**")

                chart = ui.highchart({
                    'title': False,
                    'chart': {'type': 'bar'},
                    'xAxis': {'categories': ['A', 'B']},
                    'series': [
                        {'name': 'Alpha', 'data': [0.1, 0.2]},
                        {'name': 'Beta', 'data': [0.3, 0.4]},
                    ],
                }).classes('w-full h-64')

                def update():
                    chart.options['series'][0]['data'][0] = random()
                    chart.update()

                ui.button('Update', on_click=update)

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**EChart**")

                echart = ui.echart({
                    'xAxis': {'type': 'value'},
                    'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},
                    'legend': {'textStyle': {'color': 'gray'}},
                    'series': [
                        {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},
                        {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},
                    ],
                })

                def update():
                    echart.options['series'][0]['data'][0] = random()
                    echart.update()

                ui.button('Update', on_click=update)

        ui.separator()
        with ui.card().classes('w-full'):

                ui.markdown("**Table**")

                
                columns = [
                    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
                    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
                ]
                rows = [
                    {'name': 'Elsa', 'age': 18},
                    {'name': 'Oaken', 'age': 46},
                    {'name': 'Hans', 'age': 20},
                    {'name': 'Sven'},
                    {'name': 'Olaf', 'age': 4},
                    {'name': 'Anna', 'age': 17},
                ]

                ui.table(columns=columns, rows=rows, pagination=3).classes('w-full')

                ui.separator()

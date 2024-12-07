import header
import footer
import components.home_content
import components.controls_content
import components.data_content
from pathlib import Path

import os
import json
from nicegui import app, ui

with open('config.json', 'r') as file:
    config = json.load(file)

# Read config file
appName = config["appName"]
appVersion = config["appVersion"]
appPort = config["appPort"]

app.add_static_files('/assets', "assets")


@ui.page('/')
def index():

    ui.colors(primary='#28323C', secondary="#B4C3AA", positive='#53B689', accent='#111B1E')
    ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")

    with header.frame(title=appName, version=appVersion):

        with ui.header().classes(replace='row items-center').style('background-color:white; border-bottom: 1px solid #D4D6D8;') as header_below:
            with ui.column().classes('w-full items-center'):

                with ui.tabs().props("active-color=blue-grey-14 active-bg-color=white") as tabs1:
                    
                    with ui.row():

                        with ui.tab("tab_1", label="").style('color: black; font-family: "Rational Display", sans-serif;').props("no-caps") as tab_three:
                            ui.icon("o_home").classes('text-3xl')
                            ui.label("Home")

                        with ui.tab("tab_2", label="").style('color: black; font-family: "Rational Display", sans-serif;').props("no-caps") as tab_one:
                            ui.icon("tune").classes('text-3xl')
                            ui.label("Controls")

                        with ui.tab("tab_3", label="").style('color: black; font-family: "Rational Display", sans-serif;').props("no-caps") as tab_two:
                            ui.icon("o_analytics").classes('text-3xl')
                            ui.label("Data")


        with ui.tab_panels(tabs1, value='tab_1').classes('w-full') as tab_panel:

        #####################################################################################
        
                with ui.tab_panel('tab_1').style('font-family: "Rational Display", sans-serif;'):
                    components.home_content.content()
                    
                with ui.tab_panel('tab_2').style('font-family: "Rational Display", sans-serif;'):
                    
                    components.controls_content.content()
                    
                with ui.tab_panel('tab_3').style('font-family: "Rational Display", sans-serif;'):
                    
                    components.data_content.content()

        header_below.tailwind("pt-16")
        tab_panel.tailwind("pt-16 pl-16 pr-16")

        footer.frame(title=appName, version=appVersion)

def handle_shutdown():
    print('Shutdown has been initiated!')


app.on_shutdown(handle_shutdown)

#For dev
ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀')

#For prod
#ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀')

#For native
#ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀', reload=False, native=True, window_size=(1600,900))

#For Docker
#ui.run(storage_secret=os.environ['STORAGE_SECRET'])
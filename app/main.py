import header
import components.dashboard_content
import components.shipping_content
import components.production_content
import components.orders_content
import components.pallets_content
import components.packings_content
import components.data_content
import components.settings_content
import components.print_component
from pathlib import Path
import json
from nicegui import app, ui
import os
from functools import wraps

with open('config.json', 'r') as file:
    config = json.load(file)

# Read config file
appName = config["appName"]
appVersion = config["appVersion"]
appPort = config["appPort"]

app.add_static_files('/assets', "assets")

# Create a global logo image instance to prevent reloading
logo_image = None

def get_logo_image():
    global logo_image
    if logo_image is None:
        logo_image = ui.image('assets/images/logo.png').style('width: 5rem; height: auto;')
    return logo_image


def with_base_layout(route_handler):
    @wraps(route_handler)
    def wrapper(*args, **kwargs):
        ui.colors(primary='#212121', secondary="#B4C3AA", positive='#53B689', accent='#111B1E')
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "icons.css").read() + "</style>")
        
        # Preload the logo image to prevent flickering
        ui.add_head_html('<link rel="preload" href="/assets/images/logo.png" as="image">')

        if 'sidebar-collapsed' not in app.storage.user:
            app.storage.user['sidebar-collapsed'] = True
            print("Sidebar state initialized to False")

        with header.frame(title=appName, version=appVersion,  get_logo_func=get_logo_image):
            return route_handler(*args, **kwargs)
    return wrapper


@ui.page('/')
@with_base_layout
def index():
    components.dashboard_content.content()


@ui.page('/shipping')
@with_base_layout
def shipping():
    components.shipping_content.content()


@ui.page('/production')
@with_base_layout
def production():
    components.production_content.content(searchFilter='')


@ui.page('/production/{searchFilter}')
@with_base_layout
def production_search(searchFilter):
    components.production_content.content(searchFilter=searchFilter)


@ui.page('/orders')
@with_base_layout
def orders():
    components.orders_content.content()


@ui.page('/pallets')
@with_base_layout
def pallets():
    components.pallets_content.content()


@ui.page('/packing')
@with_base_layout
def packing():
    components.packings_content.content()


@ui.page('/settings')
@with_base_layout
def settings():
    components.settings_content.content()


@ui.page('/customer/{kundennummer}')
@with_base_layout
def customer_page(kundennummer):
    components.data_content.content(kundennummer)


@ui.page('/print/{data}')
def print_page(data):
    ui.colors(primary='#212121', secondary="#B4C3AA", positive='#53B689', accent='#111B1E')
    ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")
    components.print_component.content(data)


# For dev
ui.run(storage_secret="myStorageSecret", title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20)  # log_level="debug")

# For prod
# ui.run(host='0.0.0.0', storage_secret="myStorageSecret", title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)

# For native
# ui.run(storage_secret="myStorageSecret", title=appName, port=appPort, favicon='🧿', reload=False, native=True, window_size=(1600,900))

# For Docker
# ui.run(storage_secret=os.environ['STORAGE_SECRET'], host=os.environ['HOST'], title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)

# python -m PyInstaller --name 'ProductionSuite' --onedir main.py --add-data 'C:\Users\Anwender\Desktop\Frycode-Lab Projekte\ProductionSuite\app\venv\Lib\site-packages\nicegui;nicegui' --noconfirm --clean #--add-data "ico.ico;." --icon="ico.ico"
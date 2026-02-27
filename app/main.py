"""Application entry point — page routing, shared layout decorator and run targets."""

import json
import os
from functools import wraps
from pathlib import Path

from nicegui import app, ui

import header
import components.dashboard_content
import components.design_system_content
import components.shipping_content
import components.production_content
import components.orders_content
import components.pallets_content
import components.packings_content
import components.icons_content
import components.settings_content
import components.print_component
import components.print_demo_content

# ── Config ────────────────────────────────────────────────────────────────────────────────
with open('config.json') as f:
    config = json.load(f)

appName    = config["appName"]
appVersion = config["appVersion"]
appPort    = config["appPort"]

app.add_static_files('/assets', 'assets')

# ── Logo singleton — one instance shared across requests to avoid reload cost ──────
logo_image = None

def get_logo_image():
    global logo_image
    if logo_image is None:
        logo_image = ui.image('assets/images/logo.png').style('width: 5rem; height: auto;')
    return logo_image


# ── Base layout decorator — applies theme, global CSS and sidebar shell ────────────
def with_base_layout(route_handler):
    @wraps(route_handler)
    def wrapper(*args, **kwargs):
        ui.colors(primary='#18181b', secondary='#f4f4f5', positive='#4caf50', negative='#ef4444', warning='#f59e0b', info='#3b82f6', accent='#e4e4e7')
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>", shared=True)
        ui.add_head_html('<link rel="stylesheet" href="/assets/css/icons.css">', shared=True)
        
        # Preload avoids a layout-shift flash when the sidebar logo first renders
        ui.add_head_html('<link rel="preload" href="/assets/images/logo.png" as="image">')

        if 'sidebar-collapsed' not in app.storage.user:
            app.storage.user['sidebar-collapsed'] = True

        with header.frame(title=appName, version=appVersion,  get_logo_func=get_logo_image):
            return route_handler(*args, **kwargs)
    return wrapper

# ── Page and sub-page routing ────────────────────────────────────────────────────────────
@ui.page('/')
@with_base_layout
def root():
    ui.sub_pages({
    '/': index,
    '/design-system': design_system,
    '/shipping': shipping,
    '/production': production,
    '/production/{searchFilter}' : production_search,
    '/orders' : orders,
    '/pallets' : pallets,
    '/packing' : packing,
    '/icons'      : icons,
    '/print-demo' : print_demo,
    '/settings'   : settings,
    '/customer/{kundennummer}': customer_page,
    })



# ── Sub-page handlers ────────────────────────────────────────────────────────────
def index():
    components.dashboard_content.content()

def design_system():
    components.design_system_content.content()

def shipping():
    components.shipping_content.content()

def production():
    components.production_content.content(searchFilter='')

def orders():
    components.orders_content.content()

def pallets():
    components.pallets_content.content()

def packing():
    components.packings_content.content()

def icons():
    components.icons_content.content()

def print_demo():
    components.print_demo_content.content()

def settings():
    components.settings_content.content()

def production_search(searchFilter):
    components.production_content.content(searchFilter=searchFilter)

def customer_page(kundennummer):
    components.data_content.content(kundennummer)


# Standalone print route — no sidebar, no header, no layout wrapper
@ui.page('/print/{data}')
def print_standalone(data: str):
    ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")
    components.print_component.content(data)


# ── Entry point — uncomment exactly one target ────────────────────────────────
ui.run(root, storage_secret="myStorageSecret", title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20)
# ui.run(root, host='0.0.0.0', storage_secret="myStorageSecret", title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)           # prod
# ui.run(root, storage_secret="myStorageSecret", title=appName, port=appPort, favicon='ico.ico', reload=False, native=True, window_size=(1600, 900))                # native
# ui.run(root, storage_secret=os.environ['STORAGE_SECRET'], host=os.environ['HOST'], title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)  # docker

#ui.run(root, storage_secret=os.environ.get('STORAGE_SECRET', 'myStorageSecret'), host=os.environ.get('HOST', '0.0.0.0'), title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False, on_air='qe2X7GHI9mcjiwgh')
# python -m PyInstaller --name 'ProductionSuite' --onedir main.py --add-data '...\nicegui;nicegui' --noconfirm --clean
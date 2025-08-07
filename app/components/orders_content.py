from nicegui import ui, app
from datetime import datetime

def content(searchFilter=None) -> None:

    ui.label('Welcome to the Order Center').style('font-size: 1.5rem;').style('font-weight: 400;')

    search_input = ui.input('Search for cutomers', placeholder="Type in name/customer...").classes('w-2/3 q-input mb-6').props("outlined clearable rounded standout")
    search_input.add_slot('prepend','''<q-icon name="search" />''')
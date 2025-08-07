from nicegui import ui, app, events

def content() -> None:
    
    ui.label('Welcome to the Packaging Center').style('font-size: 1.5rem;').style('font-weight: 400;')

    search_input = ui.input('Search for packages', placeholder="Type in id/customer...").classes('w-2/3 q-input mb-6').props("outlined clearable rounded standout")
    search_input.add_slot('prepend','''<q-icon name="search" />''')

    
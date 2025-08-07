from nicegui import ui, app

def content(searchFilter = None) -> None:
        
    ui.label('Welcome to Manufacturing').style('font-size: 1.5rem;').style('font-weight: 400;')

    search_input = ui.input('Search for components', placeholder="Type in id/number").classes('w-2/3 q-input mb-6').props("outlined clearable rounded standout")
    search_input.add_slot('prepend','''<q-icon name="search" />''')

    search_input.value = searchFilter
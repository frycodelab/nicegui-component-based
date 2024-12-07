from contextlib import contextmanager

from nicegui import ui,app

@contextmanager
def frame(title: str, version : str):
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')

    with ui.footer().classes('w-full items-center'):
        ui.space()
        ui.html("""<p>Copyright &copy; 2024, All Right Reserved <a href="https://nicegui.io/">NiceGUI</a> | <a href="https://frycode-lab.com/">Frycode Lab.</a></p>""")
        ui.space()

        with ui.button(on_click= lambda: ui.run_javascript("window.open('https://github.com/frycodelab','_newtab')")).props("outline").style("margin-right:4px"):
            ui.icon('eva-github', color="white").classes('text-5xl')
            ui.tooltip("Got GitHub repo @frycodelab")
        ui.space()
from nicegui import ui, app

def content() -> None:
    with ui.card().classes('w-full'):

                with ui.row():
                    ui.icon("o_info").classes('text-xl')

                    with ui.element('div').classes(' bg-white').style("border-radius: 10px;"):
                        ui.label("Due to running on a Raspberry Pi, you might experience some slowdowns.").style("font-size: 12px;color:grey;").tailwind("pr-2")

                ui.label("Welcome!").style('color: black; font-family: "Rational Display", sans-serif; font-size:28px;')

                ui.label("This App is build based on the NiceGUI framework - modified and adapted for easyier modularized use.").style('color: black; font-family: "Rational Display", sans-serif; font-size:18px;')

                ui.label("Available for:")

                with ui.row():
                    ui.icon("o_devices").classes('text-3xl')

                    with ui.element('div').classes('p-1 bg-grey-10').style("border-radius: 10px;"):
                        ui.label("Windows | Linux | MacOS ").style("font-size: 14px;color:white;").tailwind("pl-2 pr-2")

                with ui.row():
                    ui.icon("o_terminal").classes('text-3xl')

                    with ui.element('div').classes('p-1 bg-grey-10').style("border-radius: 10px;"):
                        ui.label("Desktop | Server | Docker ").style("font-size: 14px;color:white;").tailwind("pl-2 pr-2")

                with ui.row():
                    #ui.icon("o_dns").classes('text-3xl')

                    ui.spinner('puff', size='2em', color='green', thickness=12)

                    with ui.column():

                        def system_info_toggle():

                            state = system_info.visible

                            if state is True:
                                system_info.visible = False
                            else:
                                system_info.visible = True


                        with ui.element('div').classes('p-1 bg-green').style("border-radius: 10px; cursor: pointer;").on('click', lambda e: system_info_toggle()):
                            ui.label("Running on a Raspberry Pi 5").style("font-size: 14px;color:white;").tailwind("pl-2 pr-2")

                        #ui.chip('Running on a Raspberry Pi 5', text_color="white", color="green", on_click=lambda: ui.notify('Clicked')).props('square')

                        with ui.element() as system_info:

                            with ui.row():
                                ui.icon("o_info").classes('text-xl')

                                with ui.element('div').classes(' bg-white').style("border-radius: 10px;"):
                                    ui.label("Model B Rev 1.0 64-bit").style("font-size: 12px;color:black;").tailwind("pl-2 pr-2")

                            with ui.row():
                                ui.icon("o_memory").classes('text-xl')

                                with ui.element('div').classes(' bg-white').style("border-radius: 10px;"):
                                    ui.label("Quad-Core ARM @2.44GHz ").style("font-size: 12px;color:black;").tailwind("pl-2 pr-2")

                            with ui.row():
                                ui.icon("select_all").classes('text-xl')

                                with ui.element('div').classes(' bg-white').style("border-radius: 10px;"):
                                    ui.label("8 GB of LPDDR4X RAM").style("font-size: 12px;color:black;").tailwind("pl-2 pr-2")

                            with ui.row():
                                ui.icon("o_storage").classes('text-xl')

                                with ui.element('div').classes(' bg-white').style("border-radius: 10px;"):
                                    ui.label("SanDisk 64 GB").style("font-size: 12px;color:black;").tailwind("pl-2 pr-2")

                    system_info.visible = True

                ui.label("This app is designed for desktop use - you may encounter some minor performance issues on mobile devices.").tailwind("pt-1")

                ui.html('''
                        
                        

                        <p>
			            <strong>This could be your application!</strong>
                        </p>
                        
                        <p style="margin-top:4px;">
                        Available for Windows, Linux, and MacOS - as server, docker or native desktop app.
			            Browse through plenty of live demos.
                        Interact with your custom application through buttons, dialogs, 3D scenes, plots and much more. </p>
                        <p>

                        The Framework manages web development details, letting you focus on backend code for diverse applications, including robotics, IoT solutions, smart home automation, and machine learning. Designed to work smoothly with connected peripherals like webcams and GPIO pins in IoT setups, this framework streamlines the management of all your code in one place.
                        </p>

                        <p style="margin-top:12px;">
                        <strong>This is just a small insight - if you want to know more, please get in touch.</strong>
                        </p>
                        ''')
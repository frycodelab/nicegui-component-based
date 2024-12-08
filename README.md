

<img align="left" src="/FRYCODE_LAB.png">

We are focused on developing custom software solutions for different purposes.
This template is the result of the learning curve we had developing many applications.
We want to share it with the community - to help NiceGUI becomming bigger. A big thank you to @zauberzeug/niceGUI for this amazing framework.
<br clear="left"/>



# Component based NiceGUI template 

This is a template based on **NiceGUI, a fully python based framwork for web/native development**.
\
You can use plain HTML/CSS/JavaScript or your own components from the NiceGUI libary itself - they are build with **Quasar**.

Goal of this template is to modularize the way a project is set up/ worked on.
The main aim is to make it easy for beginners/or advanced developers to start off relatively fast and make the code **more readable/maintainable**.

![Logo](/Demo.PNG)

## Requirements

**All you need is:**

- [python](https://www.python.org/downloads/)
- [pip](https://phoenixnap.com/kb/install-pip-windows)

## Project structure

```javascript

nicegui-template/
├─ README.md
├─ .gitignore
├─ Dockerfile
├─ requirements.txt
├─ docker-compose.yaml
├─ app/
│  ├─ config.json
│  ├─ main.py
│  ├─ header.py
│  ├─ footer.py
│  ├─ components/
│  │  ├─ home_content.py
│  │  ├─ data_content.py
│  │  ├─ controls_content.py
│  ├─ assets/
│  │  ├─ css/
│  │  │  ├─ global-css.css
│  │  ├─ images/
│  │  │  ├─ logo.png

```


## Installation

- Clone the project first - unzip and open folder with VS Code
- Open new terminal **powershell/cmd/git-bash**:

    ```bash
    cd path/to/project
    python -m venv venv
    venv/bin/activate
    pip install nicegui
    pip install pyinstaller
    pip install -r requirements.txt
    cd app/
    ```
    
## Deployment/Testing


- To run this project run **within ./app** folder:

    ```bash
    cd app/
    python ./main.py
    ```

- To change name, version or port for the application - adjust `app/config.json`:

    ```json
    {
        "appName" : "App-Template",
        "appVersion" : "Preview",
        "appPort" : 3000
    }
    ```

    To change the logo simply replace the logo.png in `app/assets/images/logo.png`.

- Option within `main.py` - **use only one/uncomment others**:

    ```python
    #For dev
    ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀')

    #For prod only web
    ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀')

    #For native as desktop app
    ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀',     reload=False, native=True, window_size=(1600,900))

    #For Docker image/container
    ui.run(storage_secret=os.environ['STORAGE_SECRET'])
    ```

- For **Docker** adjust `main.py` and use:

    ```bash
        #For Docker
        ui.run(storage_secret=os.environ['STORAGE_SECRET'])
    ```

    Go one folder back in terminal where the **docker-compose.yaml** is located:

    ```bash
        cd ..
        docker compose up
    ```

Your container should build an image template:latest and run the container on http://localhost:8080.


## Acknowledgements/Learnings

- Add local assets to server - add in `main.py`:

    ```python
    app.add_static_files("/the-folder-name-you-want-to have-on-server","local-folder-you-want-to-add")
    ```

- Global styling in `/app/css/global-css.css`:

  You can add a global styling to the quasar elements with css:

  ```css
  .q-tooltip{
    font-size:2rem;
  }
  .q-input{
    font-size:2rem;
  }

  ```

  You can look up the quasar classes in the browser dev-console.

- Changing **.props** of **ui.elements()**:

  You can change the properties from all elements that with simply adding .props()

  ```python
  ui.input("").props("outline")
  ui.button("").props("flat")

  ```

  The props for the different elements are documented in [Quasar]("https://quasar.dev/vue-components/input#input-types").

- Changing **.style** of single **ui.elements()**

  You can change the style from all elements that with simply adding .style()

  ```python
  ui.input("").style("font-size:2rem")
  ui.button("").style("color:red")

  ```

    Stylesheet language .css  is beeing used.

## Publishing es .exe

**Make sure reload=False is in ui.run()!**

- Got to /app folder in terminal:

    `--onefile` procedure:

    ```bash
    nicegui-pack --onefile --name "myapp" main.py
    ```

    `--onedir` procedure:
    ```
    python -m PyInstaller --name 'Appname' --onedir main.py --add-data 'C:your\path\to\venv\lib\site-packages\nicegui;nicegui' --noconfirm --clean --add-data "xc.ico;." --icon="xc.ico"
    ```

    The `--onedir` direct pyinstaller call is more complex, but more **tweakable**.
    \
    Plus the startup time, especially for native apps is significantlly **faster**. That because the `--onefile` has to exctract all dependencies first, 
    \
    whereas the `--onedir` has everything unpacked.
You can have a look at the full documentation [here](https://nicegui.io/documentation/section_configuration_deployment).

## Optimizations

We took Node.js/Next.js frameworks like Angular/React/Svelte etc. as blueprint and modularized the header/footer/router-outlet.
As the projects became larger and more complex - it was a necessity to do so, to make it more readable/maintainable.

The main idea is to split/modularize components that can be reused.
So the header/footer are beeing reused, every single component has it own .py file in **/app/components** and you reuse them as often as you wish.

- Example below in `main.py`:

    ```python
    #Import all components
    import components.page_name_1
    import components.page_name_2
    #Some other imports ....

    #Some initializing code.....

    @ui.page('/')
    def index():

        #Define main colors for page/subcomponents and add css
        ui.colors(primary='#28323C', secondary="#B4C3AA", positive='#53B689', accent='#111B1E')
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")

        with header.frame(title=appName, version=appVersion):

            #Your page content from components.page_name_1.content()
            components.page_name_1()

            footer.frame(title=appName, version=appVersion)

    @ui.page('/second')
    def index():

        #Define main colors for page/subcomponents and add css
        ui.colors(primary='#28323C', secondary="#B4C3AA", positive='#53B689', accent='#111B1E')
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")

        with header.frame(title=appName, version=appVersion):

            #Your page content from components.page_name_2()

            components.page_name_2.content()

            footer.frame(title=appName, version=appVersion)

    #Some more code ...

    ```


## Authors

- [@frycodelab](https://frycode-lab.com)

## Feedback

If you have any feedback, please reach out to us at frycodelab@gmail.com.

## Demo

[Demo based on dockerized app](https://nicegui-template-black-sun-7413.fly.dev/).


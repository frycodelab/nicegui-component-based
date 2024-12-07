
# Component based NiceGUI template 

This is a template based on NiceGUI, a fully python based framwork for web/native development. Yout can use plain HTML/CSS/JavaScript or components from the NiceGUI libary itself - they are mostly build with Quasar.

Goal of this template is to modularize the way a project is set up/ worked on.
The main aim is to make it easy for beginners/or advanced developers to start off relatively fast.




## Project structure

```javascript

nicegui-template/
├─ .gitignore
├─ Dockerfile
├─ docker-compose.yaml
├─ README.md
├─ requirements.txt
├─ app/
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


## Requirements

- [python]()
- [pip]()


## Installation

- Clone the project first - unzip and open folder with VS Code
- Open new terminal powershell/cmd/git-bash

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

To run this project run within ./app folder

```bash
  python ./main.py
```

- Option within main.py - use only one/uncomment others

```bash
  #For dev
  ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀')

  #For prod
  ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀')

  #For native
  ui.run(storage_secret="myStorageSecret",title=appName,port=appPort,favicon='🚀',     reload=False, native=True, window_size=(1600,900))

  #For Docker
  ui.run(storage_secret=os.environ['STORAGE_SECRET'])
```

- For  **Docker** adjust main.py 

```bash
  #For Docker
  ui.run(storage_secret=os.environ['STORAGE_SECRET'])

```

- Go on folder back whre the docker-compose.yaml is located

```bash
  cd ..
  docker compose up

```

Your container should build an image template:latest and run the container on localhost:8080 



## Acknowledgements

- Add local assets to server - add in main.py

  ```
  app.add_static_files('/the-folder-name-you-want-to have-on-server', "local-folder-you-want-to-add")

  ```

- Global styling in /app/css/global-css.css

  You can add a global styling to the quasar elements with css.

  ```
  .q-tooltip{
    font-size:2rem;
  }
  .q-input{
    font-size:2rem;
  }

  ```

  You can look up the quasar classes in the browser dev-console.

- Changing .props of ui.elements()

  You can change the properties from all elements that with simply adding .props()

  ```
  ui.input("").props("outline")
  ui.button("").props("flat")

  ```

  The props for the different elements are documented in [Quasar]("https://quasar.dev/vue-components/input#input-types").

## Publishing es .exe

**Make sure reload=False in ui.run()!**

Got to /app folder in terminal

```bash
nicegui-pack --onefile --name "myapp" main.py
```

You can have a look at the full documentation [here]("https://nicegui.io/documentation/section_configuration_deployment").





## Optimizations

As the project became larger and more complex - it was a necessity to make it more readable/maintainable.




## Authors

- [@frycodelab](https://frycode-lab.com)


## Demo

[Demo based on dockerized app](https://nicegui-template-black-sun-7413.fly.dev/).


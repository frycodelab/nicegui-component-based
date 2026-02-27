<img align="left" src="/FRYCODE_LAB.png">

We are focused on developing custom software solutions for different purposes.
This template is the result of the learning curve we had developing many applications.
We want to share it with the community - to help NiceGUI becomming bigger. A big thank you to @zauberzeug/niceGUI for this amazing framework.
<br clear="left"/>

# NiceGUI Component-Based Template

This repository is a starter template for building web applications with NiceGUI. It is primarily targeted at desktop and tablet screen sizes and is not optimized for mobile devices. It includes:

- A header and collapsible sidebar layout
- Component pages placed in `app/components/`
- A design system page with reusable CSS tokens and components
- An icon browser for Tabler and Material icons (click to copy)
- A print system supporting raw HTML, base64 images, and structured pages
- Small service modules for notifications and mock dashboard data

Target: desktop and tablet (not optimized for mobile)

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![NiceGUI](https://img.shields.io/badge/NiceGUI-latest-green.svg)
![UV](https://img.shields.io/badge/uv-package%20manager-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

<img align="center" src="/Demo.gif">

## Core files and components

```
app/
├── main.py                       # Application entry point and routes
├── header.py                     # Header and sidebar implementation
├── footer.py                     # Footer (optional)
├── config.json                   # App configuration
├── pyproject.toml                # Dependencies
├── assets/                       # CSS and image assets
│   ├── css/
│   │   ├── global-css.css
│   │   └── icons.css
│   └── images/
├── database/                     # Database layer (models & helpers)
│   ├── crud.py
│   ├── db.py
│   ├── init_db.py
│   ├── models.py
│   └── __pycache__/
├── components/                  # Page components
│   ├── dashboard_content.py
│   ├── design_system_content.py # Live design system reference
│   ├── icons_content.py         # Icon browser (Tabler + Material)
│   ├── print_demo_content.py    # Demo pages for print modes
│   ├── print_component.py       # Print helpers and /print/ route
│   ├── production_content.py
│   ├── shipping_content.py
│   ├── orders_content.py
│   ├── pallets_content.py
│   ├── packings_content.py
│   └── settings_content.py
└── services/                    # Utility services
    ├── __init__.py
    ├── helpers.py
    ├── notifications.py         # Custom notifications
    └── dashboard_data.py        # Mock KPI and chart data
```

## Design system

The `design_system_content.py` page is a live reference for the project's CSS tokens, utility classes and component examples. It demonstrates:

- Typography scales and text utility classes
- Button variants, sizes and disabled states
- Cards, panels, badges and status dots
- Alerts, notifications and positioned toasts
- Form inputs, groups, selects and validation styles
- Progress indicators, dialogs, tooltips, steppers and more

Use this page to see available classes and example usage when building new components.

## Icon browser

The icon browser (`icons_content.py`) parses Tabler icons from `assets/css/icons.css` and includes a curated list of Material icons. It provides a searchable grid and click-to-copy behavior for icon names or classes.

## Print system

The print system is implemented in `components/print_component.py`. It provides helper functions used by other components:

- `encode_html(html: str) -> str` — encode raw HTML for the `/print/{token}` route
- `encode_image(b64_data: str, mime: str, caption: str) -> str` — encode a base64 image
- `encode_page(title, subtitle, sections) -> str` — encode a structured document
- `open_print(token: str)` — open the print view in a new tab

`print_demo_content.py` shows interactive examples for all three print modes (HTML, image, structured page).

## Services

- `services/helpers.py` — assorted utilities referenced by components
- `services/notifications.py` — custom HTML notifications with position and type options
- `services/dashboard_data.py` — generates mock KPI and chart data for the dashboard component

## Requirements

- Python 3.11 or newer
- UV package manager

## Setup and run

Install uv package manager:

```bash
pip install uv
```

Change to app directory:

```bash
cd app
```

Install dependencies:

```bash
uv sync
```

Run in development:

```bash
uv run python main.py
```

## Logging

- **Log files:** At startup the app creates a `logs` folder and writes rotating logs to `logs/app.log` (configured in `app/main.py`). The handler is a `RotatingFileHandler` configured with a 5 MB file size and 5 backup files by default.
- **Capture module logs:** The logging handler is attached to the root logger so `logging.getLogger(__name__)` calls from other modules (for example in components and services) are written to `logs/app.log`.
- **Control SQL verbosity:** SQLAlchemy engine SQL output is controlled by the engine `echo` flag and the `sqlalchemy.engine` logger level. To enable verbose SQL to console/file, set `echo=True` in `app/database/db.py` or change the logger level for `sqlalchemy.engine`.
- **Quick dev commands:**

```powershell
cd app
uv run python main.py
# On Windows (PowerShell) tail logs:
Get-Content .\logs\app.log -Wait -Tail 50
```

## Database initialization and seeding

- **Auto-seed on startup:** The project ships with `app/database/init_db.py` which creates tables and inserts deterministic sample rows. By default the initializer will clear the target tables and seed sample data so the UI tables are populated immediately in development.
- **Run seeding manually:** From the `app/` folder you can run the initializer directly if you need to reseed without restarting the full app:

```bash
python -c "from database.init_db import init_db; import asyncio; asyncio.run(init_db())"
```

- **Customize seeding:** Edit `app/database/init_db.py` to change which sample rows are inserted or to guard seeding behind an environment variable if you want to preserve production data.

## Adding or updating a component

1. Add a new module in `app/components/`.
2. Implement a `content()` function that constructs the UI via NiceGUI.
3. Register the route in `app/main.py` and add a sidebar entry in `app/header.py`.

## Deployment Options

### Development
```python
ui.run(root, host='0.0.0.0', storage_secret="your-secret", title=appName, 
       port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=True)
```

### Production
```python
ui.run(root, host='0.0.0.0', storage_secret="your-secret", title=appName, 
       port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)
```

### Native Application
```python
ui.run(root, storage_secret="your-secret", title=appName, port=appPort, 
       favicon='🧿', reload=False, native=True, window_size=(1600,900))
```

### Docker Deployment
```python
ui.run(root, storage_secret=os.environ['STORAGE_SECRET'], 
       host=os.environ['HOST'], title=appName, port=appPort, 
       favicon='ico.ico', reconnect_timeout=20, reload=False)
```

- For **Docker** adjust `main.py` and use:

    ```bash
        #For Docker
        ui.run(root, storage_secret=os.environ['STORAGE_SECRET'])
    ```

    Go one folder back in terminal where the **docker-compose.yaml** is located:

    ```bash
        cd ..
        docker compose up
    ```

Your container should build an image template:latest and run the container on http://localhost:8080.

### PyInstaller Build
```bash
python -m PyInstaller --name 'YourApp' --onedir main.py --add-data 'venv/Lib/site-packages/nicegui;nicegui' --noconfirm --clean
```

## License and authors

See project files for license details.

- Author: @frycodelab (https://frycode-lab.com)

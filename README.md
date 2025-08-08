<img align="left" src="/FRYCODE_LAB.png">

We are focused on developing custom software solutions for different purposes.
This template is the result of the learning curve we had developing many applications.
We want to share it with the community - to help NiceGUI becomming bigger. A big thank you to @zauberzeug/niceGUI for this amazing framework.
<br clear="left"/>


# NiceGUI Component-Based Boilerplate

A modern, component-based NiceGUI application boilerplate with a responsive sidebar, header wrapper, and modular architecture. Built with `uv` for fast dependency management and featuring smooth animations, optimized performance, and a clean UI.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![NiceGUI](https://img.shields.io/badge/NiceGUI-latest-green.svg)
![UV](https://img.shields.io/badge/uv-package%20manager-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

<img align="center" src="/Demo.gif">

## 🚀 Features

### 🎨 UI/UX Features
- **Responsive Collapsible Sidebar** with smooth animations
- **Modern Header** with account dropdown menu
- **Component-based Architecture** for maintainable code
- **Print System** with Base64 support for documents/images
- **Custom Styling** with Google-inspired button designs
- **Logo Optimization** with lazy loading and preloading
- **Smooth Transitions** and animations throughout the app

### 🏗️ Architecture Features
- **Modular Component System** - Each page is a separate component
- **Service Layer** - Helper functions organized in services directory
- **Configuration-driven** - Centralized config management
- **Route Wrapper System** - Consistent layout across all pages
- **Asset Management** - Organized CSS, images, and static files

### ⚡ Performance Optimizations
- **Logo Preloading** - Prevents flickering on page loads
- **Global CSS Injection** - Optimized styling delivery
- **Favicon Support** - Professional branding
- **Static File Serving** - Efficient asset delivery

## 📁 Project Structure

```
nicegui-base-main/
├── main.py                 # Main application entry point
├── header.py               # Header component with sidebar
├── footer.py               # Footer component (optional)
├── pyproject.toml          # UV/Python project configuration
├── uv.lock                 # UV lock file for reproducible builds
├── ico.ico                 # Application favicon
├── config.json             # Application configuration
│
├── assets/
│   ├── css/
│   │   ├── global-css.css  # Global application styles
│   │   └── icons.css       # Tabler icons CSS
│   └── images/
│       ├── logo.png        # Application logo
│       ├── extension_icon.png
│       └── salzit.png
│
├── components/             # Page components
│   ├── dashboard_content.py
│   ├── shipping_content.py
│   ├── production_content.py
│   ├── orders_content.py
│   ├── pallets_content.py
│   ├── packings_content.py
│   ├── data_content.py
│   ├── settings_content.py
│   └── print_component.py  # Special print functionality
│
└── services/               # Helper functions and utilities
    ├── __init__.py
    └── helpers.py
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- [UV Package Manager](https://github.com/astral-sh/uv)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd nicegui-base-main
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Create your configuration file**
   ```json
   {
     "appName": "Your App Name",
     "appVersion": "1.0.0",
     "appPort": 8080
   }
   ```

4. **Run the application**
   ```bash
   uv run python main.py
   ```

## 🎯 Key Components

### 📱 Main Application (`main.py`)

The main application file sets up the core functionality:

- **Base Layout Wrapper**: `with_base_layout` decorator that applies consistent styling and layout
- **Route Definitions**: All application routes with their respective components
- **Global Configurations**: Colors, CSS injection, and asset management
- **Logo Optimization**: Global logo instance to prevent reloading

```python
# Logo optimization with global instance
logo_image = None

def get_logo_image():
    global logo_image
    if logo_image is None:
        logo_image = ui.image('assets/images/logo.png').style('width: 5rem; height: auto;')
    return logo_image
```

### 🎨 Header Component (`header.py`)

Features a sophisticated sidebar with smooth animations:

- **Collapsible Sidebar** with width transitions (300px ↔ 100px)
- **Label Animations** with fade-in/fade-out effects
- **Active Route Highlighting** with visual indicators
- **Account Dropdown** with modern styling
- **Logo Integration** using CSS background for optimal performance

**Animation System:**
```python
async def toggle_sidebar():
    if app.storage.user['sidebar-collapsed']:
        # Expanding: Width first, then labels
        left_drawer.props("width=300")
        await ui.run_javascript('new Promise(resolve => setTimeout(resolve, 50))')
        for label in sidebar_labels:
            label.classes(remove='collapsed', add='expanded')
    else:
        # Collapsing: Labels first, then width
        for label in sidebar_labels:
            label.classes(remove='expanded', add='collapsed')
        await ui.run_javascript('new Promise(resolve => setTimeout(resolve, 50))')
        left_drawer.props("width=100")
```

### 🖨️ Print System (`print_component.py`)

Advanced printing functionality supporting various content types:

- **Base64 Decoding** for encoded content
- **Non-blocking Print** using invisible iframes
- **Automatic Window Management** 
- **Error Handling** for malformed data

### 🎨 Global Styling (`global-css.css`)

Comprehensive styling system featuring:

#### Account Dropdown Styling
```css
.account-dropdown {
  font-family: 'Roboto', sans-serif;
  min-width: 200px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
  padding: 24px 0 16px 0;
}
```

#### Google-Inspired Buttons
```css
.google-like-button {
  padding: 8px 30px !important;
  border-radius: 34px !important;
  font-weight: bold !important;
  transition: background-color 0.2s ease-in-out !important;
}
```

#### Smooth Sidebar Transitions
```css
.sidebar-label {
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out !important;
  transform-origin: left center;
}

.sidebar-label.collapsed {
  opacity: 0;
  transform: translateX(-10px);
}
```

## 🔧 Configuration

### Application Config (`config.json`)
```json
{
  "appName": "Your Application Name",
  "appVersion": "1.0.0",
  "appPort": 8080
}
```

### UV Configuration (`pyproject.toml`)
```toml
[project]
name = "nicegui-component-based"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "nicegui",
    "nicegui[highcharts]",
    "pyinstaller>=6.13.0",
    "pywebview>=5.4",
]
```

## 🎨 Customization

### Adding New Components

1. Create a new file in `components/`
2. Implement a `content()` function
3. Add route in `main.py`
4. Update sidebar navigation in `header.py`

**Example Component:**
```python
# components/new_component.py
from nicegui import ui

def content() -> None:
    ui.label('New Component').style('font-size: 1.5rem;')
    # Your component content here
```

### Styling Customization

- **Colors**: Modify in `main.py` `ui.colors()` call
- **CSS**: Add custom styles to `global-css.css`
- **Icons**: Uses Tabler Icons via `icons.css`

### Sidebar Navigation

Add new menu items in `header.py`:
```python
with ui.link('', '/your-route').classes(f'w-full no-underline text-black {"bg-light-blue-3" if current_route.startswith("/your-route") else ""}'):
    with ui.row().classes('items-center mb-2 mt-2 cursor-pointer w-full no-wrap'):
        ui.icon('your_icon').classes('ml-5 text-2xl flex-shrink-0')
        your_label = ui.label('Your Page').classes('text-lg sidebar-label ml-3 flex-shrink-0')
        sidebar_labels.append(your_label)
```

## 🚀 Deployment Options

### Development
```bash
uv run python main.py
```

### Production
```python
ui.run(host='0.0.0.0', storage_secret="your-secret", title=appName, 
       port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)
```

### Native Application
```python
ui.run(storage_secret="your-secret", title=appName, port=appPort, 
       favicon='🧿', reload=False, native=True, window_size=(1600,900))
```

### Docker Deployment
```python
ui.run(storage_secret=os.environ['STORAGE_SECRET'], 
       host=os.environ['HOST'], title=appName, port=appPort, 
       favicon='ico.ico', reconnect_timeout=20, reload=False)
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

### PyInstaller Build
```bash
python -m PyInstaller --name 'YourApp' --onedir main.py --add-data 'venv/Lib/site-packages/nicegui;nicegui' --noconfirm --clean
```

## 🎯 Performance Features

### Logo Optimization
- **Preloading**: `<link rel="preload" href="/assets/images/logo.png" as="image">`
- **Global Instance**: Prevents reloading across page navigation
- **CSS Background**: Better performance than `<img>` tags

### Asset Management
- **Static File Serving**: Efficient delivery via `app.add_static_files('/assets', "assets")`
- **CSS Injection**: Inline styles for optimal loading
- **Icon Fonts**: Tabler Icons for scalable iconography

### Animation Performance
- **CSS Transitions**: Hardware-accelerated animations
- **Strategic Delays**: Coordinated timing for smooth effects
- **Class-based Management**: Efficient DOM manipulation

## 🧩 Services Architecture

The `services/` directory contains reusable helper functions:

```python
# services/helpers.py
async def dummy_function():
    return "Helper function called successfully!"
```

Import and use in components:
```python
import services.helpers as helpers
result = await helpers.dummy_function()
```

## 📄 Print System Usage

The print component supports Base64 encoded content:

```python
# Generate a print URL
import base64
content = "<h1>Hello World</h1>"
encoded = base64.b64encode(content.encode()).decode()
print_url = f"/print/{encoded}"

# Navigate to print
ui.navigate.to(print_url)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [NiceGUI](https://nicegui.io/) - The amazing Python web framework
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager
- [Tabler Icons](https://tabler.io/icons) - Beautiful open-source icons
- [Quasar Framework](https://quasar.dev/) - UI components underlying NiceGUI

## 📞 Support

If you find this boilerplate helpful, please ⭐ star the repository!

For questions and support, please open an issue on GitHub.

---

**Happy coding with NiceGUI! 🚀**

## Authors

- [@frycodelab](https://frycode-lab.com)

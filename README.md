# NiceGUI Component-Based Boilerplate with Login and User Management

A modern, component-based NiceGUI application boilerplate with authentication, user management, responsive sidebar, and modular architecture. Built with `uv` for fast dependency management and featuring OAuth integration, local database support, and a comprehensive service layer.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![NiceGUI](https://img.shields.io/badge/NiceGUI-latest-green.svg)
![UV](https://img.shields.io/badge/uv-package%20manager-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-database-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

### 🔐 Authentication & Security
- **Multi-provider Authentication** - Local database + Google OAuth
- **Role-based Access Control** - Admin and user roles
- **Session Management** - Secure user sessions with middleware
- **Password Security** - SHA-256 hashing for local accounts
- **Route Protection** - Middleware-based authentication checks

### 👥 User Management
- **Admin Dashboard** - Complete user management interface
- **User Creation** - Admin-controlled user registration
- **User Deletion** - Protected admin operations (admin cannot be deleted)
- **User Profiles** - Full name, email, and role management
- **User Listing** - Comprehensive user overview with role badges

### 🎨 UI/UX Features
- **Responsive Collapsible Sidebar** with smooth animations
- **Modern Header** with account dropdown menu
- **Component-based Architecture** for maintainable code
- **Print System** with Base64 support for documents/images
- **Custom Styling** with Google-inspired button designs
- **Dialog System** - Confirmation dialogs for critical actions
- **Notification System** - Success, error, and info notifications

### 🏗️ Architecture Features
- **Service Layer Architecture** - Clean separation of concerns
- **Modular Component System** - Each page is a separate component
- **Database Abstraction** - SQLite with migration support
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
├── config.json             # Application configuration (OAuth, etc.)
│
├── db/                     # Database layer
│   ├── __init__.py
│   ├── database.py         # Database operations & models
│   └── users.db            # SQLite database file
│
├── services/               # Business logic layer
│   ├── __init__.py         # Service exports
│   ├── user_service.py     # User management service
│   ├── auth_service.py     # Authentication service
│   └── helpers.py          # Utility functions
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
├── components/             # Page components
│   ├── dashboard_content.py
│   ├── shipping_content.py
│   ├── production_content.py
│   ├── orders_content.py
│   ├── pallets_content.py
│   ├── packings_content.py
│   ├── data_content.py
│   ├── settings_content.py  # User management interface
│   └── print_component.py   # Special print functionality
│
└── .nicegui/               # NiceGUI storage (auto-generated)
    └── storage-*.json      # User session data
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

3. **Configure the application**
   
   The application will create a default `config.json` file on first run. Update it with your settings:
   
   ```json
   {
     "appName": "Your App Name",
     "appVersion": "1.0.0",
     "appPort": 3000,
     "google_oauth": {
       "client_id": "your-google-client-id",
       "client_secret": "your-google-client-secret",
       "redirect_uri": "http://localhost:3000/auth"
     }
   }
   ```

4. **Run the application**
   ```bash
   
   # With authentication (recommended)
   uv run python main.py
   ```

5. **Default Admin Access**
   - Username: `admin`
   - Password: `admin`
   - ⚠️ **Change the default admin password after first login!**

## 🔐 Authentication Setup

### Local Database Authentication

The application uses SQLite for local user management:

- **Automatic Setup**: Database and admin user created on first run
- **Password Hashing**: SHA-256 for secure password storage
- **User Roles**: Admin and regular user permissions
- **Session Management**: Secure session handling with middleware

### Google OAuth Setup

To enable Google OAuth authentication:

1. **Go to Google Cloud Console**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Google+ API**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:3000/auth` (development)
     - `https://yourdomain.com/auth` (production)

4. **Update Configuration**
   ```json
   {
     "google_oauth": {
       "client_id": "your-actual-client-id.googleusercontent.com",
       "client_secret": "your-actual-client-secret",
       "redirect_uri": "http://localhost:3000/auth"
     }
   }
   ```

### Authentication Middleware

The application uses custom middleware for route protection:

```python
class AuthMiddleware(BaseHTTPMiddleware):
    """Restricts access to all NiceGUI pages"""
    
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            # Check if route is unrestricted
            is_unrestricted = (
                request.url.path.startswith('/_nicegui') or 
                request.url.path in unrestricted_page_routes or
                request.url.path.startswith('/print/') or
                request.url.path.startswith('/assets/')
            )
            
            if not is_unrestricted:
                # Store intended destination and redirect to login
                app.storage.user['referrer_path'] = request.url.path
                return RedirectResponse('/login')
        
        return await call_next(request)
```

**Protected Routes**: All application routes except:
- `/login` - Login page
- `/auth` - OAuth callback
- `/assets/*` - Static assets
- `/print/*` - Print functionality
- `/_nicegui/*` - NiceGUI internal routes

## 👥 User Management

### Admin Features

Administrators have access to comprehensive user management:

1. **User Creation**
   - Create new users with username, password, email, and full name
   - Assign admin or regular user roles
   - Form validation and confirmation dialogs

2. **User Listing**
   - View all users with role badges
   - See user creation dates and last login times
   - Real-time user list updates

3. **User Deletion**
   - Delete users with confirmation dialogs
   - Protected: Admin user cannot be deleted
   - Immediate UI updates after deletion

### Service Layer Architecture

The application follows a clean service layer pattern:

#### User Service (`services/user_service.py`)
```python
class UserService:
    @staticmethod
    def create_user(username, password, email=None, full_name=None, is_admin=False):
        """Create user with validation and business logic"""
        
    @staticmethod
    def get_all_users():
        """Retrieve all users"""
        
    @staticmethod
    def delete_user(username):
        """Delete user with protection rules"""
```

#### Authentication Service (`services/auth_service.py`)
```python
class AuthService:
    @staticmethod
    def is_current_user_admin():
        """Check if current user has admin privileges"""
        
    @staticmethod
    def get_current_user():
        """Get current user data"""
        
    @staticmethod
    def login_user(user_data):
        """Handle user login session"""
```

### Database Schema

The SQLite database includes:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    full_name TEXT,
    is_admin BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

**Migration Support**: Automatic schema updates for existing databases
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

The configuration file supports both application settings and OAuth:

```json
{
  "appName": "Your Application Name",
  "appVersion": "1.0.0",
  "appPort": 3000,
  "google_oauth": {
    "client_id": "your-google-oauth-client-id",
    "client_secret": "your-google-oauth-client-secret", 
    "redirect_uri": "http://localhost:3000/auth"
  }
}
```

**Security Note**: Never commit real OAuth credentials to version control!

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
    "authlib",
    "requests",
    "urllib3"
]
```

## 🔐 Security Best Practices

### Password Security
- SHA-256 hashing for local accounts
- Minimum 6-character password requirement
- Admin user protection (cannot be deleted)

### Session Security
- Secure session storage with NiceGUI
- Session-based authentication checks
- Automatic session cleanup on logout

### OAuth Security
- CSRF protection via state parameters
- Secure redirect URI validation
- Token-based authentication flow

### Environment Security
```bash
# For production, use environment variables
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export STORAGE_SECRET="your-random-secret"
```

## 🎨 Customization

### Adding New Components

1. Create a new file in `components/`
2. Implement a `content()` function
3. Add route in `main_login.py` (for authenticated routes)
4. Update sidebar navigation in `header.py`
5. Use service layer for business logic

**Example Component:**
```python
# components/new_component.py
from nicegui import ui
from services.auth_service import is_current_user_admin
from services.user_service import UserService

def content() -> None:
    ui.label('New Component').style('font-size: 1.5rem;')
    
    # Example of using services
    if is_current_user_admin():
        users = UserService.get_all_users()
        ui.label(f'Total users: {len(users)}')
```

### Adding New Services

1. Create service file in `services/`
2. Implement static methods for business logic
3. Add imports to `services/__init__.py`
4. Use in components via service layer

**Example Service:**
```python
# services/example_service.py
from typing import List, Dict

class ExampleService:
    @staticmethod
    def get_data() -> List[Dict]:
        """Get example data with business logic"""
        # Your business logic here
        return []
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
# Without authentication
uv run python main.py

# With authentication (recommended)
uv run python main_login.py
```

### Production
```python
# Secure production deployment
ui.run(
    host='0.0.0.0', 
    storage_secret=os.environ.get('STORAGE_SECRET', 'change-this-secret'), 
    title=appName, 
    port=appPort, 
    favicon='ico.ico', 
    reconnect_timeout=20, 
    reload=False
)
```

### Native Application
```python
ui.run(storage_secret="your-secret", title=appName, port=appPort, 
       favicon='🧿', reload=False, native=True, window_size=(1600,900))
```

### Docker Deployment
```python
# Docker-ready configuration
ui.run(
    storage_secret=os.environ['STORAGE_SECRET'], 
    host=os.environ.get('HOST', '0.0.0.0'), 
    title=appName, 
    port=int(os.environ.get('PORT', appPort)), 
    favicon='ico.ico', 
    reconnect_timeout=20, 
    reload=False
)
```

**Dockerfile example:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

ENV STORAGE_SECRET=your-production-secret
ENV GOOGLE_CLIENT_ID=your-client-id
ENV GOOGLE_CLIENT_SECRET=your-client-secret

EXPOSE 3000
CMD ["uv", "run", "python", "main_login.py"]
```

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

The application follows a clean service layer architecture for maintainable and testable code:

### Service Layer Benefits
- **Separation of Concerns**: UI components focus on presentation
- **Reusability**: Business logic can be shared across components  
- **Testability**: Services can be unit tested independently
- **Maintainability**: Centralized business logic

### User Service (`services/user_service.py`)
```python
from services.user_service import UserService

# Create a new user
result = UserService.create_user(
    username="john_doe",
    password="secure_password",
    email="john@example.com",
    full_name="John Doe",
    is_admin=False
)

# Get all users
users = UserService.get_all_users()

# Delete a user
result = UserService.delete_user("john_doe")
```

### Authentication Service (`services/auth_service.py`)
```python
from services.auth_service import AuthService

# Check current user
current_user = AuthService.get_current_user()
is_admin = AuthService.is_current_user_admin()
username = AuthService.get_current_username()

# Session management
AuthService.login_user(user_data)
AuthService.logout_user()
```

### Helper Utilities (`services/helpers.py`)
```python
from services.helpers import (
    show_success_notification,
    show_error_notification,
    validate_required_fields,
    format_user_display_name
)

# Show notifications
show_success_notification("User created successfully!")
show_error_notification("Operation failed!")

# Validate form data
is_valid, error = validate_required_fields(
    data={'username': 'john', 'password': ''},
    required_fields=['username', 'password']
)
```

## � Authentication Flow

### Login Process
1. **User Access**: User attempts to access protected route
2. **Middleware Check**: `AuthMiddleware` verifies authentication
3. **Redirect**: Unauthenticated users redirected to `/login`
4. **Authentication**: User logs in via local account or Google OAuth
5. **Session Creation**: Successful login creates secure session
6. **Redirect**: User redirected to originally requested page

### OAuth Flow
1. **Google Login**: User clicks "Login with Google"
2. **Redirect**: User redirected to Google authorization server
3. **Authorization**: User grants permissions to application
4. **Callback**: Google redirects to `/auth` with authorization code
5. **Token Exchange**: Application exchanges code for access token
6. **Profile Fetch**: Application fetches user profile from Google
7. **Session Creation**: User session created with Google profile data

### Route Protection
```python
# Unrestricted routes (no authentication required)
unrestricted_page_routes = {
    '/login',      # Login page
    '/auth',       # OAuth callback
    '/unauthorized', # Error page
    '/print',      # Print functionality
    '/favicon.ico' # Favicon
}

# All other routes require authentication
```

## 👤 User Roles & Permissions

### Admin Users
- **User Management**: Create, view, and delete users
- **System Access**: Full access to all application features
- **Settings**: Access to settings and configuration
- **Protected**: Admin user cannot be deleted

### Regular Users  
- **Limited Access**: Access to non-administrative features
- **No User Management**: Cannot create or delete users
- **Profile Access**: Can view own profile information

### Permission Checks
```python
from services.auth_service import is_current_user_admin

def content():
    if is_current_user_admin():
        # Show admin-only content
        ui.label("Admin Panel")
    else:
        # Show regular user content  
        ui.label("User Dashboard")
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

## 🛡️ Security Considerations

### Production Deployment
- Change default admin password immediately
- Use environment variables for secrets
- Enable HTTPS in production
- Set secure storage secrets
- Regularly update dependencies

### OAuth Security
- Use HTTPS redirect URIs in production
- Validate OAuth state parameters
- Store client secrets securely
- Regularly rotate OAuth credentials

### Database Security
- Regular database backups
- Monitor user access patterns
- Implement proper logging
- Use connection pooling for production

## 🐛 Troubleshooting

### Common Issues

**OAuth Not Working**
- Verify redirect URIs match exactly
- Check client ID and secret in config
- Ensure Google+ API is enabled
- Verify HTTPS for production

**Database Errors**
- Check file permissions on `db/users.db`
- Verify SQLite installation
- Check for database locks

**Authentication Issues**
- Clear browser storage/cookies
- Check session storage configuration
- Verify middleware is properly installed

**User Management Issues**
- Ensure user has admin privileges
- Check database connectivity
- Verify service layer imports

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

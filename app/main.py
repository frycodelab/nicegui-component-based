import header
import components.dashboard_content
import components.shipping_content
import components.production_content
import components.orders_content
import components.pallets_content
import components.packings_content
import components.data_content
import components.settings_content
import components.print_component
from pathlib import Path
import json
from nicegui import app, ui
from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
import requests
from authlib.integrations.starlette_client import OAuthError
import traceback
import logging
import urllib3

# Import database functions
from services.user_service import UserService
from services.auth_service import AuthService

# Disable SSL warnings when verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to read config file, create default if not exists
with open('config.json', 'r') as file:
        config = json.load(file)

# Read config values
appName = config["appName"]
appVersion = config["appVersion"]
appPort = config["appPort"]

# Google OAuth configuration
CLIENT_ID = config["google_oauth"]["client_id"]
CLIENT_SECRET = config["google_oauth"]["client_secret"]
REDIRECT_URI = config["google_oauth"]["redirect_uri"]

app.add_static_files('/assets', "assets")

# Create a global logo image instance to prevent reloading
logo_image = None

def get_logo_image():
    global logo_image
    if logo_image is None:
        logo_image = ui.image('assets/images/logo.png').style('width: 5rem; height: auto;')
    return logo_image

# Define unrestricted routes (accessible without authentication)
unrestricted_page_routes = {'/login', '/unauthorized', '/auth', '/logout', '/print', '/', '/favicon.ico'}

class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.
    
    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            # Check if route is unrestricted or a print page
            is_unrestricted = (
                request.url.path.startswith('/_nicegui') or 
                request.url.path in unrestricted_page_routes or
                request.url.path.startswith('/print/') or
                request.url.path.startswith('/assets/') or  # Allow access to static assets
                request.url.path.endswith('.ico') or  # Allow favicon and icon files
                request.url.path.endswith('.png') or  # Allow image files
                request.url.path.endswith('.css') or  # Allow CSS files
                request.url.path.endswith('.js')      # Allow JS files
            )
            
            if not is_unrestricted:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')  # Redirect to login instead of unauthorized
        return await call_next(request)

app.add_middleware(AuthMiddleware)

def with_auth_layout(route_handler):
    """Decorator for authenticated pages that includes the base layout"""
    @wraps(route_handler)
    def wrapper(*args, **kwargs):
        ui.colors(primary='#212121', secondary="#B4C3AA", positive='#53B689', accent='#111B1E')
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "icons.css").read() + "</style>")
        
        # Preload the logo image to prevent flickering
        ui.add_head_html('<link rel="preload" href="/assets/images/logo.png" as="image">')

        if 'sidebar-collapsed' not in app.storage.user:
            app.storage.user['sidebar-collapsed'] = True

        with header.frame(title=appName, version=appVersion, get_logo_func=get_logo_image):
            return route_handler(*args, **kwargs)
    return wrapper

def with_login_layout(route_handler):
    """Decorator for login pages with minimal styling"""
    @wraps(route_handler)
    def wrapper(*args, **kwargs):
        ui.colors(primary='#212121', secondary="#B4C3AA", positive='#53B689', accent='#111B1E')
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")
        ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "icons.css").read() + "</style>")
        
        return route_handler(*args, **kwargs)
    return wrapper

# Authentication and login pages
@ui.page('/')
def login_check():
    """Root page that checks authentication and redirects accordingly"""
    try:
        if app.storage.user.get('authenticated', False):
            user_data = app.storage.user.get('userdata', {})
            logger.info(f'User already logged in: {user_data.get("email", "Unknown")}')
            
            # Redirect to referrer or dashboard - avoid favicon issues
            referrer = app.storage.user.get('referrer_path', '/dashboard')
            app.storage.user.pop('referrer_path', None)  # Clear referrer
            
            # Force navigation to dashboard if referrer is problematic
            target_url = '/dashboard'
            if referrer and referrer not in ['/', '/favicon.ico'] and not referrer.endswith('.ico'):
                target_url = referrer
            
            ui.navigate.to(target_url)
        else:
            ui.navigate.to('/login')
    except Exception as e:
        logger.error(f"Error in login check: {e}")
        ui.navigate.to('/login')

@ui.page('/login')
@with_login_layout
def login_page():
    """Login page with Google OAuth and local login options"""
    try:
        # Check if already authenticated
        if app.storage.user.get('authenticated', False):
            ui.navigate.to('/dashboard')
            return
        
        with ui.column().classes('items-center justify-center min-h-screen w-full'):
            with ui.card().classes('p-8 max-w-md w-full'):
                # Logo and title
                with ui.row().classes('w-full justify-center mb-6'):
                    ui.html('<div style="width: 8rem; height: 8rem; background-image: url(\'/assets/images/logo.png\'); background-size: contain; background-repeat: no-repeat; background-position: center;"></div>')
                
                ui.label(appName).classes('text-2xl font-bold text-center w-full mt-4 mb-2')
                
                # Show not logged in message
                ui.label('You are not logged in.').classes('text-center text-orange-600 text-sm mb-6')
                
                # Create tabs for different login methods
                with ui.tabs().classes('w-full') as tabs:
                    local_tab = ui.tab('Local Login')
                    google_tab = ui.tab('Google OAuth')
                
                with ui.tab_panels(tabs, value=local_tab).classes('w-full'):
                    # Local login panel
                    with ui.tab_panel(local_tab):
                        username_input = ui.input('Username', placeholder='Enter username').classes('w-full mb-4')
                        password_input = ui.input('Password', placeholder='Enter password', password=True).classes('w-full mb-4')
                        error_label = ui.label('').classes('text-red-500 text-sm mb-4').style('display: none;')
                        
                        def handle_local_login():
                            try:
                                username = username_input.value.strip()
                                password = password_input.value
                                
                                if not username or not password:
                                    error_label.text = 'Please enter both username and password'
                                    error_label.style('display: block;')
                                    return
                                
                                # Authenticate user
                                user_data = UserService.authenticate_user(username, password)
                                
                                if user_data:
                                    # Store user data and mark as authenticated
                                    AuthService.login_user(user_data)
                                    
                                    logger.info(f'Local user logged in: {username}')
                                    
                                    # Clear error display
                                    error_label.style('display: none;')
                                    
                                    # Redirect to referrer or dashboard - avoid favicon issues
                                    referrer = app.storage.user.get('referrer_path', '/dashboard')
                                    app.storage.user.pop('referrer_path', None)
                                    
                                    # Force navigation to dashboard if referrer is problematic
                                    target_url = '/dashboard'
                                    if referrer and referrer not in ['/', '/favicon.ico'] and not referrer.endswith('.ico'):
                                        target_url = referrer
                                    
                                    ui.navigate.to(target_url)
                                else:
                                    error_label.text = 'Invalid username or password'
                                    error_label.style('display: block;')
                                    
                            except Exception as e:
                                logger.error(f"Local login error: {e}")
                                error_label.text = 'Login failed. Please try again.'
                                error_label.style('display: block;')
                        
                        ui.button('Sign In', icon='login').classes('w-full').props('size=lg color=primary').on('click', handle_local_login)
                        
                        # Default credentials hint
                        ui.label('Default: admin / admin').classes('text-center text-gray-500 text-xs mt-2')
                    
                    # Google OAuth panel
                    with ui.tab_panel(google_tab):
                        ui.label('Sign in with your Google account').classes('text-center text-gray-600 mb-4')
                        
                        google_auth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
                        
                        ui.button('Sign in with Google', icon='login').classes('w-full').props('size=lg color=primary').on('click', lambda: ui.navigate.to(google_auth_url))
                
                ui.label('Choose your preferred login method').classes('text-center text-gray-600 text-sm mt-4')
                
    except Exception as e:
        logger.error(f"Error in login page: {e}")
        ui.label(f'Error: {str(e)}').classes('text-red-500')

@ui.page('/auth')
def auth_callback(code: str):
    """Google OAuth callback handler"""
    try:
        if not code:
            logger.error("No authorization code received")
            ui.navigate.to('/login')
            return
            
        # Exchange authorization code for access token
        token_url = "https://oauth2.googleapis.com/token"
        
        data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        
        response = requests.post(token_url, data=data, verify=False)
        
        if response.status_code != 200:
            logger.error(f"Token exchange failed: {response.text}")
            ui.navigate.to('/login')
            return
            
        token_data = response.json()
        access_token = token_data.get("access_token")
        id_token = token_data.get("id_token")
        
        if not access_token:
            logger.error("No access token received")
            ui.navigate.to('/login')
            return
        
        # Store tokens
        app.storage.user["access_token"] = access_token
        app.storage.user["id_token"] = id_token
        
        # Get user information
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            verify=False
        )
        
        if user_info_response.status_code != 200:
            logger.error(f"Failed to get user info: {user_info_response.text}")
            ui.navigate.to('/login')
            return
            
        user_data = user_info_response.json()
        
        # Store user data and mark as authenticated
        app.storage.user.update({
            'userdata': user_data, 
            'authenticated': True
        })
        
        logger.info(f'User logged in successfully: {user_data.get("email", "Unknown")}')
        
        # Redirect to originally requested page or dashboard - avoid favicon issues
        referrer = app.storage.user.get('referrer_path', '/dashboard')
        app.storage.user.pop('referrer_path', None)  # Remove referrer after use
        
        # Force navigation to dashboard if referrer is problematic
        target_url = '/dashboard'
        if referrer and referrer not in ['/', '/favicon.ico'] and not referrer.endswith('.ico'):
            target_url = referrer
        
        ui.navigate.to(target_url)
        
    except Exception as e:
        logger.error(f"Authentication error: {traceback.format_exc()}")
        ui.navigate.to('/login')

@ui.page('/logout')
def logout():
    """Logout handler"""
    try:
        id_token = app.storage.user.get('id_token')
        user_email = app.storage.user.get('userdata', {}).get('email', 'Unknown')
        
        # Clear user session
        app.storage.user.clear()
        
        logger.info(f'User logged out: {user_email}')
        
        # Redirect to login page
        ui.navigate.to('/login')
            
    except Exception as e:
        logger.error(f"Logout error: {e}")
        app.storage.user.clear()
        ui.navigate.to('/login')

# Main application pages (all protected)
@ui.page('/dashboard')
@with_auth_layout
def dashboard():
    """Main dashboard page (protected) - replaces the original index route"""
    try:
        user_data = app.storage.user.get('userdata', {})
        user_name = user_data.get('name', 'User')
        
        components.dashboard_content.content()
            
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        ui.label('Error loading dashboard').classes('text-red-500')

@ui.page('/shipping')
@with_auth_layout
def shipping():
    components.shipping_content.content()

@ui.page('/production')
@with_auth_layout
def production():
    components.production_content.content(searchFilter='')

@ui.page('/production/{searchFilter}')
@with_auth_layout
def production_search(searchFilter):
    components.production_content.content(searchFilter=searchFilter)

@ui.page('/orders')
@with_auth_layout
def orders():
    components.orders_content.content()

@ui.page('/pallets')
@with_auth_layout
def pallets():
    components.pallets_content.content()

@ui.page('/packing')
@with_auth_layout
def packing():
    components.packings_content.content()

@ui.page('/settings')
@with_auth_layout
def settings():
    components.settings_content.content()

@ui.page('/customer/{customernumber}')
@with_auth_layout
def customer_page(customernumber):
    components.data_content.content(customernumber)

# Print page (unrestricted - doesn't require authentication)
@ui.page('/print/{data}')
def print_page(data):
    ui.colors(primary='#212121', secondary="#B4C3AA", positive='#53B689', accent='#111B1E')
    ui.add_head_html("<style>" + open(Path(__file__).parent / "assets" / "css" / "global-css.css").read() + "</style>")
    components.print_component.content(data)

# Update the header.py logout functionality
def update_header_logout():
    """This function should be called to update the logout functionality in header.py"""
    pass

if __name__ == "__main__":
    # For dev
    ui.run(storage_secret="myStorageSecret", title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)  # log_level="debug")

    # For prod
    # ui.run(host='0.0.0.0', storage_secret="myStorageSecret", title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)

    # For native
    # ui.run(storage_secret="myStorageSecret", title=appName, port=appPort, favicon='🧿', reload=False, native=True, window_size=(1600,900))

    # For Docker
    # ui.run(storage_secret=os.environ['STORAGE_SECRET'], host=os.environ['HOST'], title=appName, port=appPort, favicon='ico.ico', reconnect_timeout=20, reload=False)

    # python -m PyInstaller --name 'ProductionSuite' --onedir main.py --add-data 'C:\Users\Anwender\Desktop\Frycode-Lab Projekte\ProductionSuite\app\venv\Lib\site-packages\nicegui;nicegui' --noconfirm --clean #--add-data "ico.ico;." --icon="ico.ico"

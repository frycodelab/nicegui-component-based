from nicegui import ui, app
from services.user_service import UserService
from services.auth_service import is_current_user_admin
import services.helpers as helpers

def content() -> None:
    with ui.row().classes('w-full mt-4'):
        ui.icon('settings', size='md').classes('')
        ui.label('Settings').style('font-size: 1.0rem; font-weight: 500;').classes('mt-1')
    
    # Only show user management for admin users
    if is_current_user_admin():
        # User creation section
        with ui.card().classes('user-management-card w-full mt-6'):
            ui.label('User Management').classes('form-section-title')
            
            with ui.column().classes('user-management-form w-full'):
                with ui.row().classes('w-full gap-4'):
                    username_input = ui.input('Username', placeholder='Enter username').props("size=60")
                    password_input = ui.input('Password', password=True, placeholder='Minimum 6 characters').props("size=60")
                    

                with ui.row().classes('w-full gap-4'):
                    email_input = ui.input('Email', placeholder='user@example.com').props("size=60")
                    full_name_input = ui.input('Full Name', placeholder='Enter full name').props("size=60")
                
                admin_checkbox = ui.checkbox('Admin privileges').classes('mt-2')
                
                result_label = ui.label('').classes('mt-2')
                
                async def show_create_user_dialog():
                    username = username_input.value.strip()
                    password = password_input.value.strip()
                    email = email_input.value.strip() or None
                    full_name = full_name_input.value.strip() or None
                    
                    # Validation
                    if not username or not password:
                        result_label.text = 'Username and password are required'
                        result_label.classes('text-red-500')
                        return
                    
                    if len(password) < 6:
                        result_label.text = 'Password must be at least 6 characters'
                        result_label.classes('text-red-500')
                        return
                    
                    if len(username) < 3:
                        result_label.text = 'Username must be at least 3 characters'
                        result_label.classes('text-red-500')
                        return
                    
                    # Show confirmation dialog
                    with ui.dialog() as dialog, ui.card():
                        ui.label('Confirm User Creation').classes('dialog-title')
                        
                        ui.label('You are about to create a new user with the following information:').classes('dialog-content mb-4')
                        
                        with ui.column().classes('w-full gap-2'):
                            with ui.row().classes('user-info-item w-full'):
                                ui.label('Username:').style('font-weight: 500; min-width: 100px;')
                                ui.label(username)

                            with ui.row().classes('user-info-item w-full'):
                                ui.label('Password:').style('font-weight: 500; min-width: 100px;')
                                ui.label(password)
                            
                            if full_name:
                                with ui.row().classes('user-info-item w-full'):
                                    ui.label('Full Name:').style('font-weight: 500; min-width: 100px;')
                                    ui.label(full_name)
                            
                            if email:
                                with ui.row().classes('user-info-item w-full'):
                                    ui.label('Email:').style('font-weight: 500; min-width: 100px;')
                                    ui.label(email)
                            
                            with ui.row().classes('user-info-item w-full'):
                                ui.label('Role:').style('font-weight: 500; min-width: 100px;')
                                ui.label('Administrator' if admin_checkbox.value else 'Regular User')

                            ui.label('Store password securely - only shown once!').classes('text-red-500 mt-2')

                        ui.separator()

                        with ui.row().classes('w-full justify-end gap-2 mt-6'):
                            ui.button('Cancel', on_click=dialog.close).props('flat no-caps').classes('google-like-button tertiary')
                            ui.button('Create User', on_click=lambda: handle_create_user_confirmed(dialog, username, password, email, full_name)).props('flat no-caps').classes('google-like-button primary')
                    
                    dialog.open()
                
                async def handle_create_user_confirmed(dialog, username, password, email, full_name):
                    # Create user using service layer
                    result = UserService.create_user(
                        username=username,
                        password=password,
                        email=email,
                        full_name=full_name,
                        is_admin=admin_checkbox.value
                    )
                    
                    dialog.close()
                    
                    if result["success"]:
                        result_label.text = result["message"]
                        result_label.classes('text-green-600')
                        # Clear form
                        clear_form()
                        # Refresh user list
                        refresh_user_list()
                        ui.notify(result["message"], type='positive')
                    else:
                        result_label.text = result["message"]
                        result_label.classes('text-red-500')
                        ui.notify(result["message"], type='negative')
                
                with ui.row().classes('w-full justify-end gap-2 mt-6'):
                    ui.button('Clear', on_click=lambda: clear_form()).props('flat no-caps').classes('google-like-button tertiary')
                    ui.button('Create User', on_click=show_create_user_dialog).props('flat no-caps').classes('google-like-button primary')
                
                def clear_form():
                    username_input.value = ''
                    password_input.value = ''
                    email_input.value = ''
                    full_name_input.value = ''
                    admin_checkbox.value = False
                    result_label.text = ''
        
        # User list section
        with ui.card().classes('user-management-card w-full mt-4'):
            ui.label('Existing Users').classes('form-section-title')
            
            def refresh_user_list():
                user_list_container.clear()
                users = UserService.get_all_users()
                
                if not users:
                    with user_list_container:
                        ui.label('No users found').classes('text-gray-500 italic p-4 text-center')
                    return
                
                for user in users:
                    with user_list_container:
                        with ui.row().classes('user-list-item w-full'):
                            with ui.column().classes('flex-1'):
                                with ui.row().classes('items-center gap-2'):
                                    ui.label(user['username']).style('font-weight: 500; font-size: 1rem;')
                                    if user['is_admin']:
                                        ui.label('ADMIN').classes('user-badge admin')
                                    else:
                                        ui.label('USER').classes('user-badge user')
                                
                                if user['full_name']:
                                    ui.label(user['full_name']).classes('text-gray-600 text-sm')
                                if user['email']:
                                    ui.label(user['email']).classes('text-gray-500 text-xs')
                            
                            with ui.column().classes('items-end gap-2'):
                                with ui.column().classes('items-end text-xs text-gray-400'):
                                    if user['created_at']:
                                        ui.label(f"Created: {user['created_at'][:10]}")
                                    if user['last_login']:
                                        ui.label(f"Last login: {user['last_login'][:10]}")
                                
                                # Add delete button (only for non-admin users)
                                if user['username'] != 'admin':
                                    async def show_delete_dialog(username=user['username'], full_name=user.get('full_name'), email=user.get('email')):
                                        # Show confirmation dialog
                                        with ui.dialog() as dialog, ui.card():
                                            ui.label('Confirm User Deletion').classes('dialog-title')
                                            
                                            ui.label('You are about to permanently delete the following user:').classes('dialog-content mb-4 text-red-600')
                                            
                                            with ui.column().classes('w-full gap-2'):
                                                with ui.row().classes('user-info-item w-full'):
                                                    ui.label('Username:').style('font-weight: 500; min-width: 100px;')
                                                    ui.label(username)
                                                
                                                if full_name:
                                                    with ui.row().classes('user-info-item w-full'):
                                                        ui.label('Full Name:').style('font-weight: 500; min-width: 100px;')
                                                        ui.label(full_name)
                                                
                                                if email:
                                                    with ui.row().classes('user-info-item w-full'):
                                                        ui.label('Email:').style('font-weight: 500; min-width: 100px;')
                                                        ui.label(email)
                                            
                                            ui.separator()

                                            with ui.row().classes('w-full justify-end gap-2 mt-6'):
                                                ui.button('Cancel', on_click=dialog.close).props('flat no-caps').classes('google-like-button tertiary')
                                                ui.button('Delete User', on_click=lambda: handle_delete_user_confirmed(dialog, username)).props('flat no-caps').classes('google-like-button secondary')
                                        
                                        dialog.open()
                                    
                                    async def handle_delete_user_confirmed(dialog, username):
                                        dialog.close()
                                        result = UserService.delete_user(username)
                                        if result["success"]:
                                            ui.notify(result["message"], type='positive')
                                            refresh_user_list()
                                        else:
                                            ui.notify(result["message"], type='negative')
                                    
                                    ui.button('Delete', on_click=show_delete_dialog).props('flat no-caps size=sm').classes('google-like-button secondary')
            
            user_list_container = ui.column().classes('w-full')
            refresh_user_list()
    
    else:
        with ui.card().classes('user-management-card w-full mt-6'):
            with ui.column().classes('items-center p-8 w-full'):
                ui.icon('admin_panel_settings', size='xl').classes('text-gray-400 mb-4')
                ui.label('Admin Access Required').style('font-size: 1.2rem; font-weight: 500;').classes('text-gray-600')
                ui.label('User management is only available to administrators').classes('text-gray-500 text-center mt-2')
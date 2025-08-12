# This file makes the services directory a Python package 

"""
Services Package

This package contains all business logic services for the application.
Services provide a clean abstraction layer between the UI components
and the database layer.
"""

# Import main service classes for easy access
from .user_service import UserService
from .auth_service import AuthService

# Import convenience functions for backward compatibility
from .user_service import (
    create_user,
    get_all_users,
    delete_user,
    get_user,
    authenticate_user,
    is_admin_user
)

from .auth_service import (
    get_current_user,
    is_authenticated,
    is_current_user_admin,
    get_current_username,
    require_admin,
    require_authentication
)

__all__ = [
    # Service classes
    'UserService',
    'AuthService',
    
    # User service functions
    'create_user',
    'get_all_users',
    'delete_user',
    'get_user',
    'authenticate_user',
    'is_admin_user',
    
    # Auth service functions
    'get_current_user',
    'is_authenticated',
    'is_current_user_admin',
    'get_current_username',
    'require_admin',
    'require_authentication'
] 
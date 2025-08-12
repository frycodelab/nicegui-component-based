"""
Authentication Service Module

This module provides authentication and authorization utilities
for the application, including session management helpers.
"""

from typing import Optional, Dict
from nicegui import app
from services.user_service import UserService


class AuthService:
    """Service class for authentication and authorization operations"""
    
    @staticmethod
    def get_current_user() -> Optional[Dict]:
        """
        Get the currently logged-in user data
        
        Returns:
            User data dictionary or None if not authenticated
        """
        return app.storage.user.get('userdata')
    
    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if the current user is authenticated
        
        Returns:
            True if user is authenticated, False otherwise
        """
        return app.storage.user.get('authenticated', False)
    
    @staticmethod
    def is_current_user_admin() -> bool:
        """
        Check if the current user has admin privileges
        
        Returns:
            True if current user is admin, False otherwise
        """
        user_data = AuthService.get_current_user()
        return UserService.is_admin(user_data) if user_data else False
    
    @staticmethod
    def get_current_username() -> Optional[str]:
        """
        Get the current user's username
        
        Returns:
            Username string or None if not authenticated
        """
        user_data = AuthService.get_current_user()
        return user_data.get('username') if user_data else None
    
    @staticmethod
    def get_current_user_id() -> Optional[int]:
        """
        Get the current user's ID
        
        Returns:
            User ID or None if not authenticated
        """
        user_data = AuthService.get_current_user()
        return user_data.get('id') if user_data else None
    
    @staticmethod
    def login_user(user_data: Dict) -> None:
        """
        Log in a user by setting session data
        
        Args:
            user_data: User data dictionary from authentication
        """
        app.storage.user['userdata'] = user_data
        app.storage.user['authenticated'] = True
    
    @staticmethod
    def logout_user() -> None:
        """
        Log out the current user by clearing session data
        """
        app.storage.user.clear()
    
    @staticmethod
    def require_admin() -> bool:
        """
        Check if current user is admin, can be used for route protection
        
        Returns:
            True if user is admin, False otherwise
        """
        return AuthService.is_current_user_admin()
    
    @staticmethod
    def require_authentication() -> bool:
        """
        Check if current user is authenticated, can be used for route protection
        
        Returns:
            True if user is authenticated, False otherwise
        """
        return AuthService.is_authenticated()


# Convenience functions for easier imports
def get_current_user() -> Optional[Dict]:
    """Get the currently logged-in user"""
    return AuthService.get_current_user()


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return AuthService.is_authenticated()


def is_current_user_admin() -> bool:
    """Check if current user is admin"""
    return AuthService.is_current_user_admin()


def get_current_username() -> Optional[str]:
    """Get current username"""
    return AuthService.get_current_username()


def require_admin() -> bool:
    """Require admin privileges"""
    return AuthService.require_admin()


def require_authentication() -> bool:
    """Require authentication"""
    return AuthService.require_authentication()

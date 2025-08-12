"""
User Service Module

This module provides high-level user management operations,
abstracting database operations and providing business logic.
"""

from typing import List, Dict, Optional, Union
from db.database import (
    create_user as db_create_user,
    get_all_users as db_get_all_users,
    delete_user as db_delete_user,
    get_user as db_get_user,
    authenticate_user as db_authenticate_user
)


class UserService:
    """Service class for user management operations"""
    
    @staticmethod
    def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
        is_admin: bool = False
    ) -> Dict[str, Union[bool, str]]:
        """
        Create a new user with validation
        
        Args:
            username: Unique username
            password: User password
            email: Optional email address
            full_name: Optional full name
            is_admin: Whether user has admin privileges
            
        Returns:
            Dict with success status and message
        """
        # Validation
        if not username or not username.strip():
            return {"success": False, "message": "Username is required"}
        
        if not password or not password.strip():
            return {"success": False, "message": "Password is required"}
        
        username = username.strip()
        password = password.strip()
        
        if len(username) < 3:
            return {"success": False, "message": "Username must be at least 3 characters"}
        
        if len(password) < 6:
            return {"success": False, "message": "Password must be at least 6 characters"}
        
        # Clean optional fields
        email = email.strip() if email else None
        full_name = full_name.strip() if full_name else None
        
        # Attempt to create user
        success = db_create_user(username, password, email, full_name, is_admin)
        
        if success:
            return {"success": True, "message": f"User '{username}' created successfully"}
        else:
            return {"success": False, "message": f"Username '{username}' already exists"}
    
    @staticmethod
    def get_all_users() -> List[Dict]:
        """
        Get all users from the database
        
        Returns:
            List of user dictionaries
        """
        return db_get_all_users()
    
    @staticmethod
    def delete_user(username: str) -> Dict[str, Union[bool, str]]:
        """
        Delete a user with business logic validation
        
        Args:
            username: Username to delete
            
        Returns:
            Dict with success status and message
        """
        if not username or not username.strip():
            return {"success": False, "message": "Username is required"}
        
        username = username.strip()
        
        # Prevent deletion of admin user
        if username == 'admin':
            return {"success": False, "message": "Cannot delete the admin user"}
        
        success = db_delete_user(username)
        
        if success:
            return {"success": True, "message": f"User '{username}' deleted successfully"}
        else:
            return {"success": False, "message": f"Failed to delete user '{username}' or user not found"}
    
    @staticmethod
    def get_user(username: str) -> Optional[Dict]:
        """
        Get a specific user by username
        
        Args:
            username: Username to retrieve
            
        Returns:
            User dictionary or None if not found
        """
        if not username or not username.strip():
            return None
        
        return db_get_user(username.strip())
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict]:
        """
        Authenticate a user
        
        Args:
            username: Username
            password: Password
            
        Returns:
            User data dictionary if authenticated, None otherwise
        """
        if not username or not password:
            return None
        
        return db_authenticate_user(username.strip(), password)
    
    @staticmethod
    def is_admin(user_data: Dict) -> bool:
        """
        Check if user has admin privileges
        
        Args:
            user_data: User data dictionary
            
        Returns:
            True if user is admin, False otherwise
        """
        return user_data.get('is_admin', False) if user_data else False


# Convenience functions for backward compatibility and simpler imports
def create_user(username: str, password: str, email: str = None, 
                full_name: str = None, is_admin: bool = False) -> Dict[str, Union[bool, str]]:
    """Convenience function for creating a user"""
    return UserService.create_user(username, password, email, full_name, is_admin)


def get_all_users() -> List[Dict]:
    """Convenience function for getting all users"""
    return UserService.get_all_users()


def delete_user(username: str) -> Dict[str, Union[bool, str]]:
    """Convenience function for deleting a user"""
    return UserService.delete_user(username)


def get_user(username: str) -> Optional[Dict]:
    """Convenience function for getting a user"""
    return UserService.get_user(username)


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Convenience function for authenticating a user"""
    return UserService.authenticate_user(username, password)


def is_admin_user(user_data: Dict) -> bool:
    """Convenience function for checking admin status"""
    return UserService.is_admin(user_data)

"""
Helper Functions Module

This module contains utility functions and common helpers
used across the application.
"""

import logging
from typing import Any, Dict, List, Optional
from functools import wraps
from nicegui import ui

# Setup logging
logger = logging.getLogger(__name__)


def safe_execute(func, *args, **kwargs) -> tuple[bool, Any]:
    """
    Safely execute a function and return success status with result
    
    Args:
        func: Function to execute
        *args: Function arguments
        **kwargs: Function keyword arguments
        
    Returns:
        Tuple of (success: bool, result: Any)
    """
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {str(e)}")
        return False, str(e)


def validate_required_fields(data: Dict, required_fields: List[str]) -> tuple[bool, str]:
    """
    Validate that required fields are present and not empty
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    for field in required_fields:
        if field not in data or not data[field] or not str(data[field]).strip():
            return False, f"Field '{field}' is required"
    return True, ""


def sanitize_string(value: Any) -> Optional[str]:
    """
    Sanitize and clean string input
    
    Args:
        value: Value to sanitize
        
    Returns:
        Cleaned string or None if empty
    """
    if value is None:
        return None
    
    cleaned = str(value).strip()
    return cleaned if cleaned else None


def format_user_display_name(user: Dict) -> str:
    """
    Format a user's display name from user data
    
    Args:
        user: User dictionary
        
    Returns:
        Formatted display name
    """
    full_name = user.get('full_name')
    username = user.get('username', 'Unknown')
    
    if full_name and full_name.strip():
        return f"{full_name.strip()} ({username})"
    return username


def show_success_notification(message: str) -> None:
    """Show success notification to user"""
    ui.notify(message, type='positive')


def show_error_notification(message: str) -> None:
    """Show error notification to user"""
    ui.notify(message, type='negative')


def show_info_notification(message: str) -> None:
    """Show info notification to user"""
    ui.notify(message, type='info')


def show_warning_notification(message: str) -> None:
    """Show warning notification to user"""
    ui.notify(message, type='warning')


def require_confirmation(action_name: str, item_name: str = None) -> str:
    """
    Generate confirmation message for destructive actions
    
    Args:
        action_name: Name of the action (e.g., 'delete', 'remove')
        item_name: Name of the item being acted upon
        
    Returns:
        Confirmation message string
    """
    if item_name:
        return f"Are you sure you want to {action_name} '{item_name}'? This action cannot be undone."
    return f"Are you sure you want to {action_name}? This action cannot be undone."


async def dummy_function():
    """Legacy dummy function for backward compatibility"""
    return "Helper function called successfully!" 
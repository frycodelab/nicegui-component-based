import sqlite3
import hashlib
import os
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent / "users.db"

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(password) == hashed

def init_database():
    """Initialize the database and create tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            full_name TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Check if is_admin column exists, if not add it
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'is_admin' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0')
        print("Added is_admin column to users table")
    
    # Check if admin user exists
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
    if cursor.fetchone()[0] == 0:
        # Create default admin user
        admin_password_hash = hash_password('admin')
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, full_name, is_admin) 
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', admin_password_hash, 'admin@localhost', 'Administrator', 1))
        print("Default admin user created (username: admin, password: admin)")
    else:
        # Update existing admin user to have admin privileges
        cursor.execute('UPDATE users SET is_admin = 1 WHERE username = ?', ('admin',))
    
    conn.commit()
    conn.close()

def authenticate_user(username: str, password: str) -> dict:
    """Authenticate a user with username and password"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, password_hash, email, full_name, is_admin, is_active 
        FROM users WHERE username = ? AND is_active = 1
    ''', (username,))
    
    user = cursor.fetchone()
    
    if user and verify_password(password, user[2]):
        # Update last login
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        ''', (user[0],))
        conn.commit()
        
        user_data = {
            'id': user[0],
            'username': user[1],
            'email': user[3] or f'{user[1]}@localhost',
            'name': user[4] or user[1],
            'is_admin': bool(user[5]),
            'login_type': 'local'
        }
        conn.close()
        return user_data
    
    conn.close()
    return None

def create_user(username: str, password: str, email: str = None, full_name: str = None, is_admin: bool = False) -> bool:
    """Create a new user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, full_name, is_admin) 
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password_hash, email, full_name, is_admin))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists

def get_user(username: str) -> dict:
    """Get user information by username"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, full_name, is_admin, is_active, created_at, last_login 
        FROM users WHERE username = ?
    ''', (username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'full_name': user[3],
            'is_admin': bool(user[4]),
            'is_active': user[5],
            'created_at': user[6],
            'last_login': user[7]
        }
    return None

def get_all_users() -> list:
    """Get all users for admin interface"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, full_name, is_admin, is_active, created_at, last_login 
        FROM users ORDER BY created_at DESC
    ''')
    
    users = cursor.fetchall()
    conn.close()
    
    return [{
        'id': user[0],
        'username': user[1],
        'email': user[2],
        'full_name': user[3],
        'is_admin': bool(user[4]),
        'is_active': bool(user[5]),
        'created_at': user[6],
        'last_login': user[7]
    } for user in users]

def delete_user(username: str) -> bool:
    """Delete a user (cannot delete admin user)"""
    if username == 'admin':
        return False  # Cannot delete admin user
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    except sqlite3.Error:
        return False

# Initialize database on import
init_database()

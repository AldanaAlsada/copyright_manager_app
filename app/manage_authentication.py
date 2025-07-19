"""
this file has code for user authentication
"""

import sqlite3
import hashlib
from pathlib import Path

db_file_path = Path("database/artefact.db")

def hash_user_password(user_password):
    """to secure password I use SHA-256."""
    return hashlib.sha256(user_password.encode()).hexdigest()

def login_user():
    """This function takes user login details and validates."""
    user_name = input("Username: ")
    user_password = input("Password: ")
    hashed_password = hash_user_password(user_password) #hash user password to compare in DB

    with sqlite3.connect(db_file_path) as db_connection:
        db_connection.row_factory = sqlite3.Row
        connection_cursor = db_connection.cursor()
        connection_cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user_name, hashed_password))
        user_results = connection_cursor.fetchone()

        if user_results:
            print(f"This login is successful. Role of user: {user_results['role']}")
            return dict(user_results)
        print("Username or password is wrong.")
        return None

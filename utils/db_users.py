import sqlite3
from .db_setup import DB_PATH
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)

def add_reading_user(username):
    """Add a username to the list of users who can be read."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO reading_users (username) VALUES (?)', (username,))
        conn.commit()
        logger.info(f"User '{username}' added to reading users.")
    except sqlite3.IntegrityError:
        logger.info(f"User '{username}' is already in the reading users list.")
    finally:
        conn.close()

def remove_reading_user(username):
    """Remove a username from the list of users who can be read."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM reading_users WHERE username = ?', (username,))
        conn.commit()
        logger.info(f"User '{username}' removed from reading users.")
    except sqlite3.Error as e:
        logger.error(f"Error removing user '{username}': {e}")
    finally:
        conn.close()

def get_reading_users():
    """Retrieve the list of users who can be read."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT username FROM reading_users')
        users = cursor.fetchall()
        logger.info(f"Retrieved reading users: {[user[0] for user in users]}")
        return [user[0] for user in users]
    except sqlite3.Error as e:
        logger.error(f"Error retrieving reading users: {e}")
        return []
    finally:
        conn.close()

def user_exists(username):
    """Check if a username exists in the reading users list."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT 1 FROM reading_users WHERE username = ?', (username,))
        exists = cursor.fetchone() is not None
        logger.info(f"User '{username}' exists: {exists}")
        return exists
    except sqlite3.Error as e:
        logger.error(f"Error checking existence of user '{username}': {e}")
        return False
    finally:
        conn.close()

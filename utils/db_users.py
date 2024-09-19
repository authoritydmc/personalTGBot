import sqlite3
from .db_setup import DB_PATH

def add_reading_user(username):
    """Add a username to the list of users who can be read."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO reading_users (username) VALUES (?)', (username,))
        conn.commit()
        print(f"User '{username}' added to reading users.")
    except sqlite3.IntegrityError:
        print(f"User '{username}' is already in the reading users list.")
    conn.close()

def remove_reading_user(username):
    """Remove a username from the list of users who can be read."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM reading_users WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    print(f"User '{username}' removed from reading users.")

def get_reading_users():
    """Retrieve the list of users who can be read."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT username FROM reading_users')
    users = cursor.fetchall()
    conn.close()

    return [user[0] for user in users]

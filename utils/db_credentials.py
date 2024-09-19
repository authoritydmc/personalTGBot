import sqlite3
from .db_setup import DB_PATH

def set_credentials(api_id, api_hash):
    """Insert or update API credentials in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT OR REPLACE INTO credentials (id, api_id, api_hash)
    VALUES (1, ?, ?)
    ''', (api_id, api_hash))

    conn.commit()
    conn.close()
    print("Credentials saved successfully.")

def get_credentials():
    """Retrieve API credentials from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT api_id, api_hash FROM credentials WHERE id = 1')
    result = cursor.fetchone()
    conn.close()

    return result if result else None

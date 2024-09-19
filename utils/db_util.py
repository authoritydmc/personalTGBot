import sqlite3
import os

# Define the path to the SQLite database
DB_PATH = 'bot.db'

def create_db():
    """Create the SQLite database and the credentials table if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create a table for storing API credentials
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_id INTEGER NOT NULL,
            api_hash TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        print("Database and table created successfully.")
    else:
        print("Database already exists.")

def set_credentials(api_id, api_hash):
    """Insert or update API credentials in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert or replace the credentials
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

    if result:
        return result
    else:
        return None

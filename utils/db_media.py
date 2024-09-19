import sqlite3
from .db_setup import DB_PATH

def log_media(username, media_type, file_path):
    """Log media information to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO media_logs (username, media_type, file_path)
    VALUES (?, ?, ?)
    ''', (username, media_type, file_path))

    conn.commit()
    conn.close()
    print(f"Media logged: {username}, {media_type}, {file_path}")

import sqlite3
import os
import logging

# Define the path to the SQLite database
DATA_FOLDER = 'data'
DB_PATH = os.path.join(DATA_FOLDER, 'bot.db')
# Configure logging for this module
logger = logging.getLogger(__name__)

def log_db_size():
    """Log the size of the database file."""
    if os.path.exists(DB_PATH):
        file_size = os.path.getsize(DB_PATH) / 1024  # size in KB
        logger.info(f"Database file size: {file_size:.2f} KB")
    else:
        logger.info("Database file does not exist, so size cannot be determined.")

def create_db():
    """Create the SQLite database and the tables if they don't exist, and log their status."""
    if not os.path.exists(DB_PATH):
        logger.info("Database does not exist. Creating database and tables.")
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Create table for API credentials
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_id INTEGER NOT NULL,
                api_hash TEXT NOT NULL
            )
            ''')
            logger.info("Table 'credentials' created or already exists.")

            # Create table for reading users
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS reading_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE
            )
            ''')
            logger.info("Table 'reading_users' created or already exists.")

            # Create table for media logs
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS media_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                media_type TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
            ''')
            logger.info("Table 'media_logs' created or already exists.")

            conn.commit()
            conn.close()
            logger.info("Database and tables created successfully.")
            log_db_size()  # Log database file size after creation

        except Exception as e:
            logger.error(f"Error creating database or tables: {e}")
    else:
        logger.info("Database already exists.")
        log_db_size()  # Log database file size if it already exists

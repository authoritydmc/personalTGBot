import sqlite3
import logging
from .db_setup import DB_PATH

# Configure logging for this module
logger = logging.getLogger(__name__)

def log_all_tables():
    """Log all available tables in the SQLite database in a single list."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        table_names = [table[0] for table in tables]
        
        if table_names:
            logger.info("Available tables in the database: %s", ', '.join(table_names))
            return table_names
        else:
            logger.info("No tables found in the database.")
            return []
    
    except Exception as e:
        logger.error(f"Error retrieving tables from the database: {e}")
    
    finally:
        conn.close()

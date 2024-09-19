import logging
from .db_setup import create_db
from .db_credentials import set_credentials, get_credentials
from .db_users import add_reading_user, remove_reading_user, get_reading_users
from .db_media import log_media
from .log_all_tables import log_all_tables as logTables
# Configure logging for this module
logger = logging.getLogger(__name__)

def initialize_db():
    """Initialize the database by creating tables."""
    logger.info("Initializing the database.")
    try:
        create_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

def set_api_credentials(api_id, api_hash):
    """Set API credentials in the database."""
    logger.info("Setting API credentials.")
    try:
        set_credentials(api_id, api_hash)
        logger.info("API credentials set successfully.")
    except Exception as e:
        logger.error(f"Failed to set API credentials: {e}")

def get_api_credentials():
    """Get API credentials from the database."""
    logger.info("Retrieving API credentials.")
    try:
        credentials = get_credentials()
        if credentials:
            logger.info("API credentials retrieved successfully.")
        else:
            logger.warning("No API credentials found in the database.")
        return credentials
    except Exception as e:
        logger.error(f"Failed to retrieve API credentials: {e}")
        return None

def add_user_to_reading_list(username):
    """Add a user to the reading users list."""
    logger.info(f"Adding user '{username}' to the reading list.")
    try:
        add_reading_user(username)
        logger.info(f"User '{username}' added to the reading list.")
    except Exception as e:
        logger.error(f"Failed to add user '{username}' to the reading list: {e}")
        raise e

def remove_user_from_reading_list(username):
    """Remove a user from the reading users list."""
    logger.info(f"Removing user '{username}' from the reading list.")
    try:
        remove_reading_user(username)
        logger.info(f"User '{username}' removed from the reading list.")
    except Exception as e:
        logger.error(f"Failed to remove user '{username}' from the reading list: {e}")

def get_reading_user_list():
    """Get the list of users who are allowed to be read."""
    logger.info("Retrieving the list of reading users.")
    try:
        users = get_reading_users()
        logger.info("List of reading users retrieved successfully.")
        return users
    except Exception as e:
        logger.error(f"Failed to retrieve the list of reading users: {e}")
        return []

def log_media_info(username, media_type, file_path):
    """Log media information to the database."""
    logger.info(f"Logging media info for user '{username}'.")
    try:
        log_media(username, media_type, file_path)
        logger.info(f"Media info logged successfully: {media_type} - {file_path}")
    except Exception as e:
        logger.error(f"Failed to log media info for user '{username}': {e}")
def log_all_tables():
    logTables()
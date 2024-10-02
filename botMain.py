import argparse
import logging
import importlib
import os
import threading
import asyncio
import socket
from telethon import TelegramClient
from utils import db_util
from webapp.app import app as flask_app  # Import the Flask app instance
import version
# Configure logging for this script
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

MODULES_FOLDER = "modules"
DATA_FOLDER = "data"  # Define the data folder

def run_flask_app():
    """Run the Flask app and handle exceptions."""
    try:
        flask_app.run(debug=False, port=5000)  # Access the Flask app instance
        logger.info("Flask application is running.")
    except Exception as e:
        logger.error(f"Flask application encountered an error: {e}")

async def load_modules(client):
    """Dynamically load all modules from the 'modules' folder and run them"""
    loaded_modules = []
    for module_name in os.listdir(MODULES_FOLDER):
        if module_name.endswith(".py") and not module_name.startswith("__"):
            module_path = f"{MODULES_FOLDER}.{module_name[:-3]}"
            logger.info(f"Loading module: {module_name}")
            
            try:
                module = importlib.import_module(module_path)
                await module.run(client)  # Each module must have a 'run' function
                loaded_modules.append(module_name)
                logger.info(f"Module {module_name} loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading module {module_name}: {e}")
    return loaded_modules

async def main():
    """Main function to initialize the client and load modules"""
    # Set up argparse to get command-line arguments if provided
    parser = argparse.ArgumentParser(description='Telegram API client setup')
    parser.add_argument('--api-id', type=int, help='Telegram API ID')
    parser.add_argument('--api-hash', type=str, help='Telegram API Hash')

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the database and log available tables
    db_util.initialize_db()
    tables = db_util.log_all_tables()

    # Attempt to get API credentials from command-line arguments, environment variables, or database
    api_id = args.api_id
    api_hash = args.api_hash

    if not api_id or not api_hash:
        # Load API credentials from environment variables if not provided via command-line arguments
        api_id = os.getenv('TELEGRAM_API_ID')
        api_hash = os.getenv('TELEGRAM_API_HASH')

    if not api_id or not api_hash:
        # Load API credentials from the database if not provided via command-line arguments or environment variables
        api_credentials = db_util.get_api_credentials()
        if not api_credentials:
            logger.info("No credentials found in environment variables or database. Please enter them.")
            api_id = int(input("Enter your API ID: "))
            api_hash = input("Enter your API Hash: ")
            db_util.set_api_credentials(api_id, api_hash)
        else:
            api_id, api_hash = api_credentials

    # Ensure api_id is an integer as required by Telethon
    api_id = int(api_id)

    # Fetch host details
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    logger.info(f"Running on host: {hostname} ({ip_address})")

    logger.info(f"Starting TelegramClient with API ID: {api_id}")

    # Ensure the data folder exists
    os.makedirs(DATA_FOLDER, exist_ok=True)
    
    # Specify the session file path within the data folder
    session_file_path = os.path.join(DATA_FOLDER, 'anon.session')
    # Load version info from version.json using the version module
    version_info = version.load_version_info()
    if not version_info:
        logger.warning("Version information is unavailable.")
    else:
        git_info = version_info.get('git', {})
        build_info = version_info.get('build', {})
       # Get the Git information
    commit_count = git_info.get('commit_count', 'N/A') if version_info else 'N/A'
    commit_hash = git_info.get('commit_hash', 'N/A') if version_info else 'N/A'
    branch_name = git_info.get('branch_name', 'N/A') if version_info else 'N/A'
    tag = git_info.get('tag', 'N/A') if version_info else 'N/A'
    commit_date = git_info.get('commit_date', 'N/A') if version_info else 'N/A'
    versionID=git_info.get('versionID')

    # Get the Build information
    build_username = build_info.get('username', 'N/A') if version_info else 'N/A'
    build_hostname = build_info.get('hostname', 'N/A') if version_info else 'N/A'
    build_timestamp = build_info.get('build_timestamp', 'N/A') if version_info else 'N/A'
    # Initialize TelegramClient with the session file path in the 'data' folder
    async with TelegramClient(session_file_path, api_id, api_hash) as client:
        try:
            # Load modules and send status updates
            loaded_modules = await load_modules(client)
            status_message = (
                f"Bot has started successfully!\n"
                f"Modules loaded: {', '.join(loaded_modules)}\n"
                f"Database tables: {(tables)}\n"
                f"Flask application is running on port 5000.\n"
                f"Host: {hostname} ({ip_address})\n"
                f"🔧 **Git Info**:\n"
                f"- Version : `{tag if tag else 'No tag'}-{commit_count}` (`{versionID}`)\n"
                f"- Commit Hash: `{commit_hash[:10]}`\n"
                f"- Branch Name: `{branch_name}`\n"
                f"- Commit Date: {commit_date}\n\n"
                f"🛠 **Build Info**:\n"
                f"- Build Username: `{build_username}`\n"
                f"- Build Hostname: `{build_hostname}`\n"
                f"- Build Timestamp: {build_timestamp}\n"

            )
            await client.send_message('me', status_message)

            # Start the Flask app in a separate thread
            flask_thread = threading.Thread(target=run_flask_app, daemon=True)
            flask_thread.start()

            # Run the Telegram client
            await client.run_until_disconnected()
            logger.info("Telegram client disconnected.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

# Entry point for the script
if __name__ == "__main__":
    logger.info("Bot is starting...")
    version.main()
    asyncio.run(main())
    logger.info("Bot has stopped.")

import argparse
import logging
import importlib
import os
import threading
import asyncio
from telethon import TelegramClient
from utils import db_util
from webapp.app import app as flask_app  # Import the Flask app instance

# Configure logging for this script
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

MODULES_FOLDER = "modules"


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

    # Check for command-line arguments first, otherwise fall back to config
    if args.api_id and args.api_hash:
        api_id = args.api_id
        api_hash = args.api_hash
    else:
        logger.info("No command-line arguments provided, loading API credentials from config.")
        api_credentials = db_util.get_api_credentials()
        if not api_credentials:
            logger.info("No credentials found. Please enter them.")
            api_id = int(input("Enter your API ID: "))
            api_hash = input("Enter your API Hash: ")
            db_util.set_api_credentials(api_id, api_hash)
        else:
            api_id, api_hash = api_credentials

    # Ensure api_id is an integer as required by Telethon
    api_id = int(api_id)

    logger.info(f"Starting TelegramClient with API ID: {api_id}")

    # The first parameter is the .session file name (absolute paths allowed)
    async with TelegramClient('anon', api_id, api_hash) as client:
        try:
            # Load modules and send status updates
            loaded_modules = await load_modules(client)
            status_message = (
                f"Bot has started successfully!\n"
                f"Modules loaded: {', '.join(loaded_modules)}\n"
                f"Database tables: {(tables)}\n"
                f"Flask application is running on port 5000."
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
    asyncio.run(main())
    logger.info("Bot has stopped.")

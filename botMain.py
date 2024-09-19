import argparse
import logging
import importlib
import os
from telethon import TelegramClient
from utils import db_util
import asyncio

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

MODULES_FOLDER = "modules"

async def load_modules(client):
    """Dynamically load all modules from the 'modules' folder and run them."""
    for module_name in os.listdir(MODULES_FOLDER):
        if module_name.endswith(".py") and not module_name.startswith("__"):
            module_path = f"{MODULES_FOLDER}.{module_name[:-3]}"
            logger.info(f"Loading module: {module_name}")

            try:
                module = importlib.import_module(module_path)
                if hasattr(module, 'run'):
                    await module.run(client)  # Each module must have a 'run' function
                    logger.info(f"Module {module_name} loaded successfully.")
                else:
                    logger.warning(f"Module {module_name} does not have a 'run' function.")
            except Exception as e:
                logger.error(f"Error loading module {module_name}: {e}")

async def main():
    """Main function to initialize the client and load modules."""
    # Set up argparse to get command-line arguments if provided
    parser = argparse.ArgumentParser(description='Telegram API client setup')
    parser.add_argument('--api-id', type=int, help='Telegram API ID')
    parser.add_argument('--api-hash', type=str, help='Telegram API Hash')

    # Parse the arguments
    args = parser.parse_args()

    # Check for command-line arguments first, otherwise fall back to the database
    if args.api_id and args.api_hash:
        api_id = args.api_id
        api_hash = args.api_hash
        # Save to the database for future use
        db_util.set_credentials(api_id, api_hash)
    else:
        logger.info("No command-line arguments provided. Loading API credentials from the database.")
        credentials = db_util.get_credentials()
        if credentials:
            api_id, api_hash = credentials
        else:
            logger.error("No API credentials found in the database. Exiting...")
            return

    # Ensure api_id is an integer as required by Telethon
    api_id = int(api_id)

    logger.info(f"Starting TelegramClient with API ID: {api_id}")

    # Create a TelegramClient session
    async with TelegramClient('anon', api_id, api_hash) as client:
        try:
            logger.info("Client connected. Loading bot modules...")
            await load_modules(client)
            logger.info("All modules loaded. Running the client...")
            await client.run_until_disconnected()
        except Exception as e:
            logger.error(f"An error occurred while running the client: {e}")

# Entry point for the script
if __name__ == "__main__":
    logger.info("Bot is starting...")
    asyncio.run(main())
    logger.info("Bot has stopped.")

import os
import json

# Define the config file path
CONFIG_FILE = 'config.json'

# Function to load API credentials from config.json
def load_config():
    """
    Loads the configuration from the config.json file if it exists.
    Returns a dictionary with api_id and api_hash if present.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save API credentials to config.json
def save_config(api_id, api_hash):
    """
    Saves the API credentials (api_id, api_hash) into config.json file.
    """
    with open(CONFIG_FILE, 'w') as file:
        json.dump({'api_id': api_id, 'api_hash': api_hash}, file)

# Function to get api_id and api_hash, prompt the user if not found
def get_api_credentials():
    """
    Retrieves api_id and api_hash from either the config.json file or environment variables.
    If not found, it will prompt the user to input them and save them in the config.json file.
    Returns:
        (api_id, api_hash) as a tuple.
    """
    config = load_config()

    api_id = config.get('api_id') or os.getenv('TELEGRAM_API_ID')
    api_hash = config.get('api_hash') or os.getenv('TELEGRAM_API_HASH')

    if not api_id:
        api_id = input("Please enter your Telegram API ID: ")
    if not api_hash:
        api_hash = input("Please enter your Telegram API Hash: ")

    # Save the credentials to config.json if missing
    save_config(api_id, api_hash)

    # Ensure api_id is an integer as required by Telethon
    return int(api_id), api_hash

import os
import json
import argparse
from telethon import TelegramClient

# Define the config file path
CONFIG_FILE = 'config.json'

# Function to load API credentials from config.json
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save API credentials to config.json
def save_config(api_id, api_hash):
    with open(CONFIG_FILE, 'w') as file:
        json.dump({'api_id': api_id, 'api_hash': api_hash}, file)

# Set up argparse to get command-line arguments if provided
parser = argparse.ArgumentParser(description='Telegram API client setup')
parser.add_argument('--api-id', type=int, help='Telegram API ID')
parser.add_argument('--api-hash', type=str, help='Telegram API Hash')

# Parse the arguments
args = parser.parse_args()

# Load config from file if it exists
config = load_config()

# Check for command-line arguments, environment variables, or config file
api_id = args.api_id or os.getenv('TELEGRAM_API_ID') or config.get('api_id')
api_hash = args.api_hash or os.getenv('TELEGRAM_API_HASH') or config.get('api_hash')

# If api_id or api_hash is still not provided, ask the user for input
if not api_id:
    api_id = input("Please enter your Telegram API ID: ")
if not api_hash:
    api_hash = input("Please enter your Telegram API Hash: ")

# Save the credentials to config.json for future use
save_config(api_id, api_hash)

# Ensure api_id is an integer as required by Telethon
api_id = int(api_id)

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))

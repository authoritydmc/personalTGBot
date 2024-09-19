import logging
import re
from telethon import events
from utils import db_util

# Configure logging for this module
logger = logging.getLogger(__name__)

async def run(client):
    """Handle incoming messages using the client object passed from the main script"""

    logger.info("Setting up userBot message handler...")

    # Register the event handler dynamically using the client passed as a parameter
    @client.on(events.NewMessage)
    async def handler(event):
        logger.info(f"New message received: {event.raw_text}")

        # Regex pattern to match '.addUser [username]'
        pattern = re.compile(r'\.addUser\s+(\w+)')
        match = pattern.search(event.raw_text)

        if match:
            username = match.group(1)
            logger.info(f"Adding user to reading list: {username}")
            try:
                db_util.add_user_to_reading_list(username)
                await event.reply(f"User '{username}' has been added to the reading list.")
                logger.info(f"User '{username}' added to the reading list successfully.")
            except Exception as e:
                await event.reply("Failed to add user to the reading list.")
                logger.error(f"Failed to add user '{username}' to the reading list: {e}")

    logger.info("userBot is listening for new messages.")

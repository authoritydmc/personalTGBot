import logging
from telethon import events

# Configure logging for this module
logger = logging.getLogger(__name__)

async def run(client):
    """Handle incoming messages using the client object passed from the main script"""

    logger.info("Setting up userBot message handler...")

    # Register the event handler dynamically using the client passed as a parameter
    @client.on(events.NewMessage)
    async def handler(event):
        logger.info(f"New message received: {event.raw_text}")
        
        if 'hello' in event.raw_text.lower():
            logger.info("Replying with 'hi!'")
            await event.reply('hi!')


    logger.info("userBot is listening for new messages.")

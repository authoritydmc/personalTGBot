import logging
from telethon import events

# Configure logging for this module
logger = logging.getLogger(__name__)

async def run(client):
    """Another bot module to handle specific keywords"""

    logger.info("Setting up anotherBot message handler...")

    @client.on(events.NewMessage)
    async def handler(event):
        logger.info(f"anotherBot received: {event.raw_text}")

        if 'bye' in event.raw_text.lower():
            logger.info("Replying with 'goodbye!'")
            await event.reply('goodbye!')
        else:
            logger.info("Message does not contain 'bye'")

    logger.info("anotherBot is listening for new messages.")

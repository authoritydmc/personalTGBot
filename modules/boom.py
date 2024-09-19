import logging
import re
from telethon import events, types
from telethon.tl.types import PeerUser
from utils import command_registry

# Configure logging for this module
logger = logging.getLogger(__name__)

command_registry.register_command("boom", "Save all media after the replied message")

# Define a case-insensitive regex pattern to match the command
command_pattern = re.compile(r'\.boom', re.IGNORECASE)

async def run(client):
    """Sets up the message handler for the '.boom' module."""
    
    logger.info("Setting up '.boom' module message handler...")

    @client.on(events.NewMessage(outgoing=True, pattern=command_pattern))
    async def handler(event):
        """Handles new incoming messages."""
        
        if event.is_reply:
            # Extract the replied-to message ID and the chat ID
            replied_to_message = await event.get_reply_message()
            if not replied_to_message:
                logger.info("No message found to reply to.")
                return
            
            replied_to_message_id = replied_to_message.id
            chat_id = replied_to_message.chat_id

            logger.info(f"Reply detected to message ID {replied_to_message_id} in chat ID {chat_id}. Starting to track messages after this ID.")
            await event.delete()
            # Iterate over messages sent after the replied-to message
            try:
                async for message in client.iter_messages(
                    chat_id,
                    min_id=replied_to_message_id,
                    reverse=False  # Change to True if you want to get messages in reverse order
                ):
                    # Process each message
                    logger.info(f"Message ID {message.id} sent after the replied-to message ID {replied_to_message_id}. Content: {message.raw_text[:100]}")

                    
                    details = (
                        f"Video received from: {chat_id}\n"
                        f"Message ID: {message.id}\n"
                        f"Caption: {message.text if message.text else 'No caption'}"
                                            )
                    
                    # Example: Save or process the message, e.g., save media
                    if message.media:
                        # Implement your media saving logic here
                        file_path = f"data/{chat_id}/{message.id}.jpg" if isinstance(message.media, types.MessageMediaPhoto) else f"data/media/{message.id}.mp4"
                        await message.download_media(file_path)
                        logger.info(f"Media saved to {file_path}")
                        await client.send_message('me', details, file=file_path)
            except Exception as e:
                logger.error(f"Error iterating over messages: {e}")

    logger.info("'.boom' module is now listening for new messages.")

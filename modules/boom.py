import logging
import re
import os
from telethon import events, types
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
            
            # Ensure directory exists for saving media
            media_dir = f"data/{chat_id}"
            os.makedirs(media_dir, exist_ok=True)

            # Send initial status update message
            status_message = await client.send_message('me', f"Starting to track messages after ID {replied_to_message_id} in chat {chat_id}...")

            # Initialize a counter for the number of processed messages
            processed_count = 0
            
            # Iterate over messages sent after the replied-to message
            
            async for message in client.iter_messages(
                    chat_id,
                    min_id=replied_to_message_id ,  # Start with the next message
                    reverse=False  # Change to True if you want to get messages in reverse order
                ):
                try:
                    # Increment the processed message counter
                    processed_count += 1

                    # Process each message
                    logger.info(f"Processing message ID {message.id}. Content: {message.raw_text[:100]}")
                    update_message = f"Processing message ID{message.id}"
                    await client.edit_message(status_message, update_message)

                    details = (
                        f"Media received from: {chat_id}\n"
                        f"Message ID: {message.id}\n"
                        f"Caption: {message.text if message.text else 'No caption'}"
                    )

                    # Determine file path based on media type
                    if message.media:
                        if isinstance(message.media, types.MessageMediaPhoto):
                            file_extension = '.jpg'
                        elif isinstance(message.media, types.MessageMediaDocument):
                            mime_type = message.media.document.mime_type
                            if mime_type.startswith('video'):
                                file_extension = '.mp4'
                            else:
                                file_extension = '.doc'  # Fallback for other types
                        else:
                            file_extension = '.bin'  # Fallback for unknown types

                        file_path = os.path.join(media_dir, f"{message.id}{file_extension}")

                        # Download media
                        await message.download_media(file_path)
                        logger.info(f"Media saved to {file_path}")

                        # Send details and media
                        await client.send_message('me', details, file=file_path)

                    # Update status message with the number of processed messages
                    update_message = f"Processed {message.id} |{processed_count} messages so far. Last media saved to {file_path}."
                    await client.edit_message(status_message, update_message)

                except Exception as e:
                    logger.error(f"Error iterating over messages: {e}")

            # Finalize status message to indicate completion
            await client.edit_message(status_message, "Finished processing messages.")
            
            # Optionally, delete the status message if you want to clean up
            await client.delete_messages('me', status_message.id)

    logger.info("'.boom' module is now listening for new messages.")

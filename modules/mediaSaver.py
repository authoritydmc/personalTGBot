import logging
import os
from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from utils import db_util

# Configure logging for this module
logger = logging.getLogger(__name__)

async def run(client):
    """Handles incoming media messages and text, saves them to disk, and resends them with details."""

    logger.info("Setting up MediaSaver message handler...")

    @client.on(events.NewMessage)
    async def handler(event):
        sender_username = event.sender.username if event.sender and event.sender.username else 'unknown_sender'
        
        # Check if the sender is in the list of reading users
        reading_users = db_util.get_reading_user_list()
        if sender_username not in reading_users:
            logger.info(f"Message from '{sender_username}' is not in the reading users list. Ignoring.")
            return
        
        # Determine the directory to save the media
        save_dir = os.path.join('data', sender_username)
        os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

        if isinstance(event.message.media, MessageMediaPhoto):
            file_path = os.path.join(save_dir, f"{event.message.id}.jpg")
            try:
                await event.message.download_media(file_path)
                logger.info(f"Photo saved to {file_path}")

                details = (
                    f"Photo received from: {sender_username}\n"
                    f"Message ID: {event.message.id}\n"
                    f"Caption: {event.message.text if event.message.text else 'No caption'}"
                )

                await client.send_message('me', details, file=file_path)
                logger.info(f"Photo and details sent to yourself")

                # Log media information to the database
                db_util.log_media_info(sender_username, 'photo', file_path)

            except Exception as e:
                logger.error(f"Failed to handle photo: {e}")

        elif isinstance(event.message.media, MessageMediaDocument):
            if event.message.media.document.mime_type.startswith('video'):
                file_path = os.path.join(save_dir, f"{event.message.id}.mp4")
                try:
                    await event.message.download_media(file_path)
                    logger.info(f"Video saved to {file_path}")

                    details = (
                        f"Video received from: {sender_username}\n"
                        f"Message ID: {event.message.id}\n"
                        f"Caption: {event.message.text if event.message.text else 'No caption'}"
                    )

                    await client.send_message('me', details, file=file_path)
                    logger.info(f"Video and details sent to yourself")

                    # Log media information to the database
                    db_util.log_media_info(sender_username, 'video', file_path)

                except Exception as e:
                    logger.error(f"Failed to handle video: {e}")

    logger.info("MediaSaver is listening for new messages.")

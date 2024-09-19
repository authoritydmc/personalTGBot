import logging
import os
from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from utils import db_util

# Configure logging for this module
logger = logging.getLogger(__name__)

async def run(client):
    """Handles incoming media messages and text, saves them to disk, and updates download progress in a single message."""
    
    logger.info("Setting up MediaSaver message handler...")

    @client.on(events.NewMessage(incoming=True,outgoing=False))
    async def handler(event):
        # Determine sender info: username or user ID
        sender_username = event.sender.username if event.sender and event.sender.username else None
        sender_id = str(event.peer_id.user_id) if event.peer_id  else 'unknown_id'

        if sender_username:
            user_identifier = sender_username
        else:
            user_identifier = str(sender_id)


        # Check if the sender is in the list of reading users
        reading_users = db_util.get_reading_user_list()
        # logger.info(f"Allowed users: {reading_users}")
        # logger.info(f"Checking sender: username='{sender_username}', ID='{sender_id}'")
        # logger.info(f"Type of sender ID: {type(sender_id)}")
        # logger.info(f"Type of elements in reading_users: {[type(user) for user in reading_users]}")
        # Determine if the sender ID is allowed
        id_allowed = sender_id in reading_users
        # logger.info(f"Sender ID '{sender_id}' allowed: {id_allowed}")

        # Determine if the sender username is allowed
        username_allowed = sender_username in reading_users if sender_username else False
        # logger.info(f"Sender username '{sender_username}' allowed: {username_allowed}")

        # Determine if the sender is overall allowed
        user_allowed = id_allowed or username_allowed
        logger.info(f"Overall user allowed: {user_allowed} {user_identifier}")

        if not user_allowed:
            logger.info(f"User with ID '{sender_id}' or username '{sender_username}' is not in the reading users list. Ignoring message: {event.raw_text[:20]}")
            return



        # Determine the directory to save the media
        save_dir = os.path.join('data', user_identifier)
        os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Update message status
        status_message = await client.send_message('me', f"Received message from {user_identifier}. Preparing to download...")

        try:
            if isinstance(event.message.media, MessageMediaPhoto):
                file_path = os.path.join(save_dir, f"{event.message.id}.jpg")
                await client.edit_message(status_message, f"Starting download of photo (ID: {event.message.id})...")

                # Download photo with progress updates
                await event.message.download_media(file_path, progress_callback=lambda current, total: update_progress(client, status_message, current, total))
                
                await client.edit_message(status_message, f"Photo downloaded successfully!\nSaved to: {file_path}")

                details = (
                    f"Photo received from: {user_identifier}\n"
                    f"Message ID: {event.message.id}\n"
                    f"Caption: {event.message.text if event.message.text else 'No caption'}"
                    f"Status:{status_message.message}"
                )
                await status_message.delete()
                
                await client.send_message('me', details, file=file_path)
                logger.info(f"Photo and details sent to yourself")

                # Log media information to the database
                db_util.log_media_info(user_identifier, 'photo', file_path)

            elif isinstance(event.message.media, MessageMediaDocument):
                if event.message.media.document.mime_type.startswith('video'):
                    file_path = os.path.join(save_dir, f"{event.message.id}.mp4")
                    await client.edit_message(status_message, f"Starting download of video (ID: {event.message.id})...")

                    # Download video with progress updates
                    await event.message.download_media(file_path, progress_callback=lambda current, total: update_progress(client, status_message, current, total))

                    await client.edit_message(status_message, f"Video downloaded successfully!\nSaved to: {file_path}")

                    details = (
                        f"Video received from: {user_identifier}\n"
                        f"Message ID: {event.message.id}\n"
                        f"Caption: {event.message.text if event.message.text else 'No caption'}"
                       f"Status:{status_message.message}"
                        )
                    await status_message.delete()
                    await client.send_message('me', details, file=file_path)
                    logger.info(f"Video and details sent to yourself")

                    # Log media information to the database
                    db_util.log_media_info(user_identifier, 'video', file_path)

        except Exception as e:
            await client.edit_message(status_message, f"Failed to handle media: {e}")
            logger.error(f"Failed to handle media: {e}")

    logger.info("MediaSaver is listening for new messages.")

async def update_progress(client, status_message, current, total):
    """Update progress of media download in a single message."""
    if total:
        percent_complete = (current / total) * 100
        if percent_complete % 10 == 0:  # Update every 10%
            progress_message = f"Download progress: {current / 1024:.2f} KB / {total / 1024:.2f} KB ({percent_complete:.1f}%)"
            await client.edit_message(status_message, progress_message)

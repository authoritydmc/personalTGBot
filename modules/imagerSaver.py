import logging
import os
from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Configure logging for this module
logger = logging.getLogger(__name__)

async def run(client):
    """Handles incoming media messages and text, saves them to disk, and resends them with details."""

    logger.info("Setting up imageSaver message handler...")

    @client.on(events.NewMessage)
    async def handler(event):
        # Determine the sender's username or use 'unknown_sender' if not available
        sender_username = event.sender.username if event.sender and event.sender.username else 'unknown_sender'
        # Determine the directory to save the media
        save_dir = os.path.join('data', sender_username)
        os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

        if isinstance(event.message.media, MessageMediaPhoto):
            # Save photo
            file_path = os.path.join(save_dir, f"{event.message.id}.jpg")
            try:
                await event.message.download_media(file_path)
                logger.info(f"Photo saved to {file_path}")

                # Prepare message with details
                details = (
                    f"Photo received from: {sender_username}\n"
                    f"Message ID: {event.message.id}\n"
                    f"Caption: {event.message.text if event.message.text else 'No caption'}"
                )

                # Resend the photo to yourself with the details
                await client.send_message('me', details, file=file_path)
                logger.info(f"Photo and details sent to yourself")

            except Exception as e:
                logger.error(f"Failed to handle photo: {e}")

        elif isinstance(event.message.media, MessageMediaDocument):
            # Check if the document is a video
            if event.message.media.document.mime_type.startswith('video'):
                # Save video
                file_path = os.path.join(save_dir, f"{event.message.id}.mp4")
                try:
                    await event.message.download_media(file_path)
                    logger.info(f"Video saved to {file_path}")

                    # Prepare message with details
                    details = (
                        f"Video received from: {sender_username}\n"
                        f"Message ID: {event.message.id}\n"
                        f"Caption: {event.message.text if event.message.text else 'No caption'}"
                    )

                    # Resend the video to yourself with the details
                    await client.send_message('me', details, file=file_path)
                    logger.info(f"Video and details sent to yourself")

                except Exception as e:
                    logger.error(f"Failed to handle video: {e}")

        else:
            # Handle text messages
            if event.message.text:
                # Save text message
                file_path = os.path.join(save_dir, f"{event.message.id}.txt")
                try:
                    with open(file_path, 'w') as file:
                        file.write(event.message.text)
                    logger.info(f"Text message saved to {file_path}")

                    # Prepare message with details
                    details = (
                        f"Text message received from: {sender_username}\n"
                        f"Message ID: {event.message.id}\n"
                        f"Text: {event.message.text}"
                    )

                    # Resend the text message to yourself
                    await client.send_message('me', details)
                    logger.info(f"Text message and details sent to yourself")

                except Exception as e:
                    logger.error(f"Failed to handle text message: {e}")

    logger.info("imageSaver is listening for new messages.")

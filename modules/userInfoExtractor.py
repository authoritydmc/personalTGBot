
import logging

from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from utils import command_registry

# Configure logging for this module
logger = logging.getLogger(__name__)

async def run(client):
    """Handles the '.whois' command to retrieve and send important user details."""

    logger.info("Setting up Whois command handler...")
    command_registry.register_command("whois", "Retrieve and send important user details.")

    @client.on(events.NewMessage(outgoing=True,pattern=r'\.whois\s?(.*)'))
    async def handler(event):
        if event.fwd_from:
            return
        
        # Retrieve full user details
        replied_user, error = await get_full_user(client, event)
        if replied_user is None:
            await event.reply(f"Error retrieving user details: {error}")
            return
        
        replied_user = replied_user

        try:
            # Extract user information
                        
            # Delete the original message
            await event.delete()
            for user in replied_user.users:
                user_id = user.id
                first_name = user.first_name or "No Name"
                last_name = user.last_name or "No Last Name"
                username = user.username or "No Username"

                # Prepare message to send details to you (the bot user)
                message_to_send = (
                    f"User ID: {user_id}\n"
                    f"First Name: {first_name}\n"
                    f"Last Name: {last_name}\n"
                    f"Username: {username}\n"
                )

                # Send the message to yourself
                await client.send_message('me', message_to_send)

            logger.info(f"Sent user details to the bot user and deleted the original message.")

        except Exception as e:
            logger.error(f"Failed to retrieve or send user details: {e}")   

async def get_full_user(client, event):
    """Retrieve full user details based on the event context."""
    try:
        if event.reply_to_msg_id:
            logger.info("Fetching user info from a reply...")
            previous_message = await event.get_reply_message()
            if previous_message.forward:
                user_id = previous_message.forward.from_id or previous_message.forward.channel_id
                logger.info(f"Fetching full user info for ID from forward: {user_id}")
                replied_user = await client(GetFullUserRequest(user_id))
            else:
                user_id = previous_message.from_id
                logger.info(f"Fetching full user info for ID from reply: {user_id}")
                replied_user = await client(GetFullUserRequest(user_id))
            return replied_user, None
        
        else:
            input_str = event.pattern_match.group(1).strip()
            logger.info(f"Processing user input: {input_str}")

            if event.message.entities:
                mention_entity = event.message.entities[0]
                if isinstance(mention_entity, MessageEntityMentionName):
                    user_id = mention_entity.user_id
                    logger.info(f"Fetching full user info for ID from mention: {user_id}")
                    replied_user = await client(GetFullUserRequest(user_id))
                    return replied_user, None
            
            if event.is_private:
                user_id = event.chat_id
                logger.info(f"Fetching full user info for ID from private chat: {user_id}")
                replied_user = await client(GetFullUserRequest(user_id))
                return replied_user, None
            
            else:
                user_object = await client.get_entity(input_str)
                user_id = user_object.id
                logger.info(f"Fetching full user info for ID from entity: {user_id}")
                replied_user = await client(GetFullUserRequest(user_id))
                return replied_user, None
    
    except Exception as e:
        logger.error(f"Error retrieving user details: {e}")
        return None, str(e)

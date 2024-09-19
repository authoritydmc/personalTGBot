import logging
import re
from telethon import events
from utils import db_util,command_registry

# Configure logging for this module
logger = logging.getLogger(__name__)

# Register commands with descriptions
command_registry.register_command("addUser", "Add a user to the reading list")
command_registry.register_command("removeUser", "Remove a user from the reading list")
command_registry.register_command("getUsers", "Get the list of users in the reading list")

# Define a case-insensitive regex pattern to match all commands
command_pattern = re.compile(r'\.(addUser|removeUser|getUsers)\s*(\w*)', re.IGNORECASE)

async def run(client):
    """Handle incoming messages using the client object passed from the main script"""

    logger.info("Setting up userBot message handler...")

    # Register the event handler dynamically using the client passed as a parameter
    @client.on(events.NewMessage(outgoing=True,pattern=command_pattern))
    async def handler(event):
        # Match the command pattern
        match = command_pattern.search(event.raw_text)
        if match:
            command = match.group(1).lower()  # Convert command to lower case
            argument = match.group(2)

            if command == "adduser":
                logger.info(f"Processing '.addUser' command for username: {argument}")
                if db_util.is_reading_user_exists(argument):
                    await event.reply(f"User '{argument}' is already in the reading list.")
                    logger.info(f"User '{argument}' is already in the reading list.")
                else:
                    try:
                        db_util.add_reading_user(argument)
                        await event.reply(f"User '{argument}' has been added to the reading list.")
                        logger.info(f"User '{argument}' added to the reading list successfully.")
                    except Exception as e:
                        await event.reply("Failed to add user to the reading list.")
                        logger.error(f"Failed to add user '{argument}' to the reading list: {e}")

            elif command == "removeuser":
                logger.info(f"Processing '.removeUser' command for username: {argument}")
                if not db_util.user_exists(argument):
                    await event.reply(f"User '{argument}' is not in the reading list.")
                    logger.info(f"User '{argument}' is not in the reading list.")
                else:
                    try:
                        db_util.remove_reading_user(argument)
                        await event.reply(f"User '{argument}' has been removed from the reading list.")
                        logger.info(f"User '{argument}' removed from the reading list successfully.")
                    except Exception as e:
                        await event.reply("Failed to remove user from the reading list.")
                        logger.error(f"Failed to remove user '{argument}' from the reading list: {e}")

            elif command == "getusers":
                logger.info("Processing '.getUsers' command.")
                try:
                    users = db_util.get_reading_users()
                    if users:
                        user_list = "\n".join(users)
                        await event.reply(f"Reading users:\n{user_list}")
                        logger.info(f"Retrieved reading users: {users}")
                    else:
                        await event.reply("No users in the reading list.")
                        logger.info("No users in the reading list.")
                except Exception as e:
                    await event.reply("Failed to retrieve users from the reading list.")
                    logger.error(f"Failed to retrieve users from the reading list: {e}")

    logger.info("userBot is listening for new messages.")

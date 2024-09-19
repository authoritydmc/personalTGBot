# modules/help_module.py

import logging
import re
from telethon import events
from utils import command_registry

# Configure logging for this module
logger = logging.getLogger(__name__)

# Register help command
command_registry.register_command("help", "Show a list of available commands")

async def run(client):
    """Handle incoming messages using the client object passed from the main script"""

    logger.info("Setting up help message handler...")
    
    @client.on(events.NewMessage(outgoing=True,pattern=r'\.help'))
    async def handler(event):
        commands = command_registry.get_commands()
        help_text = "Available commands:\n"
        for command, description in commands.items():
            help_text += f".{command}: {description}\n"
        
        await event.reply(help_text)

    logger.info("Help module is listening for the '.help' command.")

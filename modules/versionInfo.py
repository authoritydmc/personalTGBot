import logging
from telethon import events
from utils import command_registry
import version  # Ensure the version module is imported

# Configure logging for this module
logger = logging.getLogger(__name__)

# Register info command
command_registry.register_command("info", "Show the version information")

async def run(client):
    """Handle incoming messages using the client object passed from the main script."""
    
    logger.info("Setting up version info message handler...")
    
    @client.on(events.NewMessage(outgoing=True, pattern=r'\.info'))
    async def handler(event):
        # Load version info from version.json using the version module
        version_info = version.load_version_info()
        if not version_info:
            await event.reply("Version information is unavailable.")
            return
        
        # Get Git, Build, and System information
        git_info = version_info.get('git', {})
        build_info = version_info.get('build', {})
        system_info = version_info.get('system', {})
        
        # Extract Git details
        commit_count = git_info.get('commit_count', 'N/A')
        commit_hash = git_info.get('commit_hash', 'N/A')
        branch_name = git_info.get('branch_name', 'N/A')
        tag = git_info.get('tag', 'N/A')
        commit_date = git_info.get('commit_date', 'N/A')
        versionID = git_info.get('versionID', 'N/A')

        # Extract Build details
        build_username = build_info.get('username', 'N/A')
        build_hostname = build_info.get('hostname', 'N/A')
        build_timestamp = build_info.get('build_timestamp', 'N/A')
        cwd = build_info.get('cwd', 'N/A')

        # Extract System details
        os_name = system_info.get('os', 'N/A')
        os_version = system_info.get('os_version', 'N/A')
        platform = system_info.get('platform', 'N/A')
        machine = system_info.get('machine', 'N/A')
        processor = system_info.get('processor', 'N/A')
        python_version = system_info.get('python_version', 'N/A')
        python_implementation = system_info.get('python_implementation', 'N/A')
        architecture = system_info.get('architecture', 'N/A')

        # Construct the version information message
        info_message = (
            f"🔧 **Version Info**:\n"
            f"- Version: `{tag if tag else 'No tag'}-{commit_count}` (`{versionID}`)\n"
            f"- Commit Hash: `{commit_hash[:10]}`\n"
            f"- Branch Name: `{branch_name}`\n"
            f"- Commit Date: {commit_date}\n\n"
            f"🛠 **Build Info**:\n"
            f"- Build Username: `{build_username}`\n"
            f"- Build Hostname: `{build_hostname}`\n"
            f"- Build Timestamp: {build_timestamp}\n"
            f"- Current Working Directory: `{cwd}`\n\n"
            f"🖥 **System Info**:\n"
            f"- OS: `{os_name}`\n"
            f"- OS Version: `{os_version}`\n"
            f"- Platform: `{platform}`\n"
            f"- Machine: `{machine}`\n"
            f"- Processor: `{processor}`\n"
            f"- Python Version: `{python_version}`\n"
            f"- Python Implementation: `{python_implementation}`\n"
            f"- Architecture: `{architecture}`\n"
        )
        
        # Reply with the version information
        await event.reply(info_message)

    logger.info("Version info module is listening for the '.info' command.")

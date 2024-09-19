# utils/command_registry.py

# Dictionary to store command descriptions
command_registry = {}

def register_command(command_name, description):
    """Register a command with its description."""
    command_registry[command_name] = description

def get_commands():
    """Retrieve the command dictionary."""
    return command_registry

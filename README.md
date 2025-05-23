# Telegram Bot with Modular Handlers
[![Docker Image CI](https://github.com/authoritydmc/personalTGBot/actions/workflows/docker-image.yml/badge.svg)](https://github.com/authoritydmc/personalTGBot/actions/workflows/docker-image.yml)


This project is a modular Telegram bot built using the [Telethon](https://github.com/LonamiWebs/Telethon) library. Each functionality of the bot (message handlers, event listeners, etc.) is separated into individual Python modules, making it easy to maintain and expand.

## Features
- **Dynamic Module Loading**: Each bot functionality is defined in separate modules, which are dynamically loaded at runtime.
- **Configuration Management**: The bot uses an SQLite database to store API credentials.
- **Logging**: Each module has logging integrated to track bot activity.

## Project Structure

```
project/
│
├── modules/
│   ├── userBot.py        # Example module to handle "hello" messages
│   ├── anotherBot.py     # Another example module to handle "bye" messages
│   └── __init__.py       # Empty init file
│
├── config.py             # Handles database operations (API credentials)
├── botMain.py            # Main entry point of the bot
├── bot.db                # SQLite database (auto-generated on first run)
└── README.md             # This readme file
```

## Getting Started

### Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8+
- [Telethon](https://pypi.org/project/Telethon/)

You can install Telethon via pip:
```bash
pip install telethon
```

### API Credentials

To use the Telegram bot, you'll need API credentials:
1. Go to [my.telegram.org](https://my.telegram.org).
2. Log in and navigate to **API Development Tools**.
3. Create a new application to get your `api_id` and `api_hash`.

### Setup

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-repo/telegram-modular-bot.git
   cd telegram-modular-bot
   ```

2. **Add API Credentials**:
   You can provide the API credentials in two ways:
   
   - **Via Command Line Arguments**:
     Run the bot with your API credentials:
     ```bash
     python botMain.py --api-id YOUR_API_ID --api-hash YOUR_API_HASH
     ```

   - **Via SQLite Database**:
     On the first run, if credentials are not provided through the command line, the bot will prompt you for the `api_id` and `api_hash`. These credentials will be saved in an SQLite database (`bot.db`) for future runs. 

### Running the Bot

Run the bot using the following command:
```bash
python botMain.py
```

The bot will:
1. Connect to Telegram using the provided API credentials.
2. Dynamically load all modules from the `modules/` folder.
3. Start listening for incoming messages and events based on the logic defined in the modules.

### Adding New Modules

To add a new feature to your bot:
1. Create a new Python file in the `modules/` folder (e.g., `modules/newFeatureBot.py`).
2. Define an `async def run(client)` function in your module.
3. Use Telethon’s event handler system (e.g., `events.NewMessage`) to define the behavior of your bot.

#### Example of a New Module:

```python
import logging
from telethon import events

logger = logging.getLogger(__name__)

async def run(client):
    """A new bot module to handle specific keywords"""

    @client.on(events.NewMessage)
    async def handler(event):
        logger.info(f"Received: {event.raw_text}")

        if 'good morning' in event.raw_text.lower():
            logger.info("Replying with 'Good morning!'")
            await event.reply('Good morning!')
        else:
            logger.info("No relevant keyword found.")
    
    logger.info("New feature bot is listening for new messages.")
```

Once you add a new module and run the bot, it will be automatically loaded without modifying `botMain.py`.

### Logging

Logging is enabled throughout the application. Logs from each module and the main script will be printed to the console by default. You can customize the logging level by modifying the `logging.basicConfig(level=logging.INFO)` line in `botMain.py`.

## Example Modules

### `userBot.py` (Handles "hello" messages)
```python
import logging
from telethon import events

logger = logging.getLogger(__name__)

async def run(client):
    @client.on(events.NewMessage)
    async def handler(event):
        logger.info(f"New message received: {event.raw_text}")
        
        if 'hello' in event.raw_text.lower():
            logger.info("Replying with 'hi!'")
            await event.reply('hi!')
```

### `anotherBot.py` (Handles "bye" messages)
```python
import logging
from telethon import events

logger = logging.getLogger(__name__)

async def run(client):
    @client.on(events.NewMessage)
    async def handler(event):
        if 'bye' in event.raw_text.lower():
            logger.info("Replying with 'goodbye!'")
            await event.reply('goodbye!')
```

## Troubleshooting

- **Error: `NameError: name 'client' is not defined`**
  Ensure that the `client` object is passed correctly to each module's `run(client)` function.

- **Module not loading**:
  Check that your module has the correct file extension (`.py`) and is placed in the `modules` folder.

## Docker Support

For Docker-based setup instructions, including how to build and run the Docker image, refer to [DOCKER_README.md](DOCKER_README.md).

## Contributing

If you'd like to contribute or add new features, feel free to submit a pull request.
Adios

---

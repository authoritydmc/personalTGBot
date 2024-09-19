# Telegram Bot with Flask Integration

This project sets up a Telegram bot using the Telethon library and integrates a Flask web application. The bot supports dynamic module loading and interacts with a database for storing API credentials and other configurations.

## Docker Setup

### Build the Docker Image

To build the Docker image, run the following command from the root directory of the project:

```sh
docker build -t telegram-bot .
```

### Run the Docker Container

To run the Docker container, you need to pass the API credentials either via environment variables or command-line arguments. If neither is provided, the bot will prompt you to enter the credentials interactively on the first run.

#### Using Environment Variables

Set the environment variables `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` for the API credentials:

```sh
docker run -d \
  -e TELEGRAM_API_ID=your_api_id \
  -e TELEGRAM_API_HASH=your_api_hash \
  -p 5000:5000 \
  telegram-bot
```

#### Using Command-Line Arguments

Alternatively, pass the API credentials as command-line arguments:

```sh
docker run -d \
  -p 5000:5000 \
  telegram-bot \
  --api-id your_api_id \
  --api-hash your_api_hash
```

### Interactive Setup

If no API credentials are provided through environment variables or command-line arguments, the bot will prompt you to enter them interactively on the first run. Ensure you have a terminal available to input the credentials.

### Exposed Ports

- **Port 5000**: Used by the Flask application to serve web requests.

### Notes

- Make sure your database is correctly configured and accessible from the Docker container.
- The bot will start and load all modules from the `modules` directory.
- Flask application logs will be visible in the Docker container logs.

## Stopping the Container

To stop the running container, use:

```sh
docker stop <container_id>
```

Replace `<container_id>` with the actual ID of the running container, which you can find using:

```sh
docker ps
```

## Logs

To view the logs of the running container:

```sh
docker logs <container_id>
```

Replace `<container_id>` with the actual ID of the running container.

---

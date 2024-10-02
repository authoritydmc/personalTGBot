# Telegram Bot with Flask Integration

This project sets up a Telegram bot using the Telethon library and integrates a Flask web application. The bot supports dynamic module loading and interacts with a database for storing API credentials and other configurations.

## Docker Setup

### Build the Docker Image

To build the Docker image, run:

```sh
docker build -t telegram-bot .
```

### Run the Docker Container

To run the Docker container with automatic restart and mount the `data` folder to the host system, use:

```sh
docker run -it --restart unless-stopped --name telegram-bot -p 5000:5000 -v /path/on/host/data:/app/data telegram-bot
```

Here’s a concise version of the README for running the Docker container for your Telegram bot:

---

### Running the Docker Container for Telegram Bot

#### Initial Setup (Generate Session File)

Run the following command to generate the session file for the first time:

```sh
docker run -it --restart unless-stopped --name telegram-bot -p 5000:5000 -v /path/on/host/data:/app/data rajlabs/tgbot
```

#### Subsequent Runs (Detached Mode)

After signing in, stop and remove the old container:

```sh
docker stop telegram-bot
docker rm telegram-bot
```

Then, start the container in detached mode:

```sh
docker run -d --restart unless-stopped --name telegram-bot -p 5000:5000 -v /path/on/host/data:/app/data rajlabs/tgbot
```

### Note

Replace `/path/on/host/data` with your actual host path.




**Explanation**:
- `--restart unless-stopped`: This policy ensures that the container is automatically restarted if it exits due to an error or system reboot, but not if it is manually stopped.
- `-v /path/on/host/data:/app/data`: Mounts the `data` directory on the host (`/path/on/host/data`) to the `data` directory in the container (`/app/data`). Replace `/path/on/host/data` with the path to the directory on your host system where you want to store the data files.

During the first run, the bot will prompt you to enter the `api_id` and `api_hash`. These credentials will be saved in the `data` directory on the host system, ensuring persistence and easy access.

### Exposed Ports

- **Port 5000**: Used by the Flask application to serve web requests.

### Notes

- Ensure that the directory you mount (`/path/on/host/data`) exists on your host system and has the appropriate permissions for Docker to read and write.
- The bot will start and load all modules from the `modules` directory.
- Flask application logs will be visible in the Docker container logs.

## Stopping the Container

To stop the running container manually, use:

```sh
docker stop <container_id>
```

Replace `<container_id>` with the actual ID of the running container, which you can find using:

```sh
docker ps
```

### Logs

To view the logs of the running container, use:

```sh
docker logs <container_id>
```

Replace `<container_id>` with the actual ID of the running container.

---
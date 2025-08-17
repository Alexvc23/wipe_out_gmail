# Gmail Cleanup 🚀📧

Tired of those unread emails or the growing spam messages? This Gmail Cleanup script is here to help you declutter your inbox in a flash! With simple commands, keep your Gmail neat and organized.

## Table of Contents (fixed)

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Docker Setup](#docker-setup)
   - [Using the Makefile](#using-the-makefile)
- [Running the Script with a Desktop Shortcut](#running-the-script-with-a-desktop-shortcut)
- [File Structure](#file-structure)
- [Sources](#sources)
- [Contributions](#contributions)
- [License](#license)

## Introduction 📄

This script uses the Gmail API to programmatically manage and clean up your Gmail inbox. Whether you have unread emails cluttering your inbox or spam that needs to be purged, this script makes the task easy.

## Prerequisites 🛠️

- Python 3.x
- Gmail account
- `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, and `google-api-python-client` libraries.

## Features ✨

1. **Delete Unread Emails**: Clears all unread emails with a single command.
2. **Delete Spam**: Instantly clean out all messages in the spam folder.
3. **Delete Bin**: Empty the bin folder.

## Setup 🛠

1. **Google API Credentials Setup** 🗝️

To create the credentials in the Google API Console, follow these steps:

1. Go to the [Google API Console](https://console.developers.google.com/).
2. Select your project from the top-left dropdown menu.
3. Click on "Library" in the left-hand menu.
4. Search for "Gmail API" and click on it.
5. Click the "Enable" button to enable the Gmail API for your project.
6. Click on "Create credentials" at the top of the page.
7. In the "Which API are you using?" dropdown, select "Gmail API".
8. In the "Where will you be calling the API from?" dropdown, select "Other non-UI (e.g., cron job, daemon)".
9. In the "What data will you be accessing?" section, select "Application data".
10. Click "What credentials do I need?".
11. Enter a name for your OAuth 2.0 client ID, and click "Create OAuth 2.0 client ID".
12. Download the `credentials.json` file by clicking the download button.
13. Place the `credentials.json` file in your project directory.

2. **Environment Setup**:
   - It's recommended to use a virtual environment:
     ```sh
     python3 -m venv myenv
     source myenv/bin/activate
     ```
   - Install the required packages:
     ```sh
     pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
     ```

3. **First-time Run**: 
   - On first run, the script will open a new browser window asking for Gmail permissions.
   - Authenticate and allow the script access.
   - This will generate a `token.pickle` file which will be used for subsequent authentications.

## Usage 💻

To delete unread emails:
```sh
python3 src/clean_up_mail.py delete_unread
```

To delete emails from the spam folder:
```sh
python3 src/clean_up_mail.py delete_spam
```

To delete emails from the bin folder:
```sh
python3 src/clean_up_mail.py delete_bin
```

To exit from the python virtual environment:
```sh
deactivate
```

## Docker Setup 🐳

1. Build the Docker image:
   ```sh
   docker-compose build
   ```

2. Run the Docker container:
   ```sh
   docker-compose up
   ```

3. View logs from the Docker container:
   ```sh
   make logs
   ```

### Using the Makefile

This project includes a `Makefile` to simplify common Docker Compose workflows. The `Makefile` uses a project-specific `docker compose` invocation and a small helper that ensures the Docker daemon is running before performing actions.

Key points:

- The Makefile defines these variables and targets:
   - `PROJECT_NAME` – set to `wipe_out_gmail` (used as the Compose project name).
   - `COMPOSE_CMD` – a shortcut for `docker compose -p $(PROJECT_NAME)` so all Compose commands use the `-p wipe_out_gmail` project flag.

- The Makefile provides these user-facing targets (all appear in `make help`):
   - `make up`    — Start services in detached mode and follow logs.
   - `make down`  — Stop and remove services.
   - `make build` — Build or rebuild services.
   - `make logs`  — Stream container logs (`-f`).
   - `make restart` — Restart services (runs `down` then `up`).
   - `make re`    — Rebuild and restart (runs `build` then `restart`).

- Docker pre-check: the `ensure-docker` target verifies the Docker daemon is running before running Docker Compose commands. On macOS it will attempt to start Docker Desktop using `open -a Docker` and then wait until `docker info` succeeds.

   Notes and alternatives:
   - The `open -a Docker` command is macOS-specific. If you're on Linux, you may instead use `sudo systemctl start docker` or ensure your Docker service is running via your distro's service manager.
   - On Windows (or WSL), make sure Docker Desktop is running and that the `docker` CLI is available in your environment.

Examples:

Stream logs (follows them):
```sh
make logs
```

Start services (detached) and follow logs:
```sh
make up
```

Build images then restart:
```sh
make re
```

## Running the Script with a Desktop Shortcut 🖱️

To run the script using a desktop shortcut, follow these steps:

1. **Create a Shell Script**: Ensure you have the `run_script.sh` file in your project directory.
2. **Create a .command File**: Create a `.command` file to execute the shell script.
   ```sh
   # filepath: /Users/alex/Documents/programing/python/wipe_out_gmail/run_script.command
   #!/bin/bash
   /Users/alex/Documents/programing/python/wipe_out_gmail/run_script.sh
   ```
   Make the `.command` file executable:
   ```sh
   chmod +x /Users/alex/Documents/programing/python/wipe_out_gmail/run_script.command
   ```

Now, you can double-click the `run_script.command` file to execute the `run_script.sh` script.

## File Structure 📁

```
/Users/alex/Documents/programing/python/wipe_out_gmail
│
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── run_script.sh
├── run_script.command
├── src
│   ├── __init__.py
│   └── clean_up_mail.py
└── README.md
```

## Sources:
- [Google API Console](https://console.developers.google.com/)
- [Google API Client Libraries - Python](https://developers.google.com/api-client-library/python/start/get_started)
- [Google Auth Library - Python](https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.flow.html#google.oauth2.flow.InstalledAppFlow.run_local_server)
- [OAuth 2.0 for Mobile & Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
- [Google API Console - Redirect URIs](https://developers.google.com/identity/protocols/oauth2/web-server#redirect-uri)

## Contributions 🙌

All contributions are welcome! If you have suggestions or improvements, please open an issue or send a pull request.

## License 📜

This project is open-source, available under the [MIT License](https://choosealicense.com/licenses/mit/).

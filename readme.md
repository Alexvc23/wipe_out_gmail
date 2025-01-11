# Gmail Cleanup 🚀📧

Tired of those unread emails or the growing spam messages? This Gmail Cleanup script is here to help you declutter your inbox in a flash! With simple commands, keep your Gmail neat and organized.

## Table of Contents 📖

- [Introduction](#Introduction-)
- [Prerequisites](#Prerequisites-)
- [Features](#Features-)
- [Setup](#Setup-)
- [Installation](#Installation-)
- [Usage](#Usage-)
- [Docker Setup](#Docker-Setup-)
- [File Structure](#File-Structure-)
- [Sources](#Sources-)
- [Contributions](#Contributions-)
- [License](#License-)

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

## File Structure 📁

```
/Users/alex/Documents/programing/python/wipe_out_gmail
│
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
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

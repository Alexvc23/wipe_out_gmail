# Gmail Cleanup 🚀📧

Tired of those unread emails or the growing spam messages? This Gmail Cleanup script is here to help you declutter your inbox in a flash! With simple commands, keep your Gmail neat and organized.

## Table of Contents 📖

- [Introduction](#Introduction-)
- [Prerequisites](#Prerequisites-)
- [Features](#Features-)
- [Setup](#Setup-)
- [Installation](#Installation-)
- [Usage](#Usage-)
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

## Setup 🛠

1 **Google API Credentials Setup** 🗝️

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
     ```
     python3 -m venv myenv
     source myenv/bin/activate
     ```
   - Install the required packages:
     ```
     pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
     ```

3. **First-time Run**: 
   - On first run, the script will open a new browser window asking for Gmail permissions.
   - Authenticate and allow the script access.
   - This will generate a `token.pickle` file which will be used for subsequent authentications.

## Usage 💻

To delete unread emails:
```bash
python3 script_name.py delete_unread
```

To delete emails from the spam folder:

```bash
python3 script_name.py delete_spam
```

Replace script_name.py with the name of your script file.

## Local Server and Redirect URI Explanation 🌐

The `run_local_server()` method is used to authenticate your script with the Gmail API. It sets up a local development server on your machine using the HTTP protocol and port 8080. Port 8080 is a commonly used alternative to the default HTTP port 80, which might be reserved or already in use by other services on your machine.

The local server listens for the authorization response from Google after you grant the script access to your Gmail account. The default redirect URI for the `run_local_server()` method is `http://localhost:8080/`. This URI should be added to the "Authorized redirect URIs" section in your Google API Console to ensure a successful authentication process.

The `run_local_server()` method uses the HTTP protocol instead of HTTPS because it is intended for local development purposes, where the primary goal is to test and debug your application. Setting up HTTPS for local development requires additional steps, such as generating SSL certificates and configuring the server to use them. While it is possible to set up HTTPS for local development, it is not the default behavior for the `run_local_server()` method to simplify the setup process and minimize potential issues during development.


## Contributions 🙌

All contributions are welcome! If you have suggestions or improvements, please open an issue or send a pull request.
License 📜

This project is open-source, available under the [MIT License](https://choosealicense.com/licenses/mit/).

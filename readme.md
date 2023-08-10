# Gmail Cleanup 🚀📧

Tired of those unread emails or the growing spam messages? This Gmail Cleanup script is here to help you declutter your inbox in a flash! With simple commands, keep your Gmail neat and organized.

## Table of Contents 📖

- [Features](#features-✨)
- [Setup](#setup-🛠)
- [Usage](#usage-💻)
- [Contributions](#contributions-🙌)
- [License](#license-📜)

## Features ✨

1. **Delete Unread Emails**: Clears all unread emails with a single command.
2. **Delete Spam**: Instantly clean out all messages in the spam folder.

## Setup 🛠

1. **Google Cloud Console Setup**: 
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project.
   - Enable Gmail API.
   - Create OAuth 2.0 credentials and download the `credentials.json` file. Place it in the project directory.

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

## Contributions 🙌

All contributions are welcome! If you have suggestions or improvements, please open an issue or send a pull request.
License 📜

This project is open-source, available under the [MIT License](https://choosealicense.com/licenses/mit/).
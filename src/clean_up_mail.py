import pickle
import os.path
import sys
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://mail.google.com/']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing access token: {e}")
                sys.exit(1)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_console()
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def delete_emails(service, user_id, query):
    while True:
        results = service.users().messages().list(userId=user_id, q=query).execute()
        messages = results.get('messages', [])
        if not messages:
            break

        for message in messages:
            retries = 5
            while retries > 0:
                try:
                    service.users().messages().delete(userId=user_id, id=message['id']).execute()
                    print(f"Deleted message with ID: {message['id']}")
                    break
                except Exception as e:
                    print(f"Failed to delete message with ID {message['id']}: {e}")
                    retries -= 1
                    if retries > 0:
                        print(f"Retrying... ({5 - retries}/5)")
                        time.sleep(2)
                    else:
                        print(f"Giving up on message with ID {message['id']} after 5 attempts.")

if __name__ == '__main__':
    service = get_service()
    user_id = 'me'

    actions = {
        'delete_unread': 'is:unread',
        'delete_spam': 'in:spam',
        'delete_bin': 'in:trash'
    }

    if len(sys.argv) > 1:
        action = sys.argv[1]
        query = actions.get(action)
        if query:
            delete_emails(service, user_id, query)
        else:
            print(f"Unknown argument: {action}")
            print("Usage: python script_name.py [delete_unread|delete_spam|delete_bin]")
    else:
        # No specific action specified, execute all actions
        for action, query in actions.items():
            print(f"Executing {action}...")
            delete_emails(service, user_id, query)

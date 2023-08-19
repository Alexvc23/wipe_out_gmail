import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_console()

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def delete_unread_emails(service):
    user_id = 'me'
    query = 'is:unread'
    results = service.users().messages().list(userId=user_id, q=query).execute()
    messages = results.get('messages', [])

    for message in messages:
        msg_id = message['id']
        msg = service.users().messages().get(userId=user_id, id=msg_id).execute()
        subject = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'][0]
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
        print(f'Deleted message with subject: {subject}')

def delete_spam_emails(service):
    user_id = 'me'
    query = 'in:spam'
    results = service.users().messages().list(userId=user_id, q=query).execute()
    messages = results.get('messages', [])

    for message in messages:
        msg_id = message['id']
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
        print(f'Message with ID {msg_id} deleted from Spam.')

if __name__ == '__main__':
    service = get_service()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'delete_unread':
            delete_unread_emails(service)
        elif sys.argv[1] == 'delete_spam':
            delete_spam_emails(service)
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Usage: python script_name.py [delete_unread|delete_spam]")
    else:
        print("Specify an action: delete_unread or delete_spam")

import pickle
import os.path
import sys
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://mail.google.com/']

def get_service():
    """
    Get Gmail service with robust authentication handling.
    
    Priority:
    1. Use existing valid token.pickle
    2. Refresh expired token if refresh_token exists
    3. Interactive auth via browser (local development)
    4. Manual auth code input (headless/Docker environments)
    """
    creds = None
    token_file = 'token.pickle'
    
    # Load existing credentials
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Check if credentials are valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Try to refresh the token
            try:
                print("Refreshing expired access token...")
                creds.refresh(Request())
                print("Token refreshed successfully!")
            except Exception as e:
                print(f"Error refreshing access token: {e}")
                print("Need to re-authenticate...")
                creds = None
        
        if not creds:
            # Need new authentication
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json file not found!")
                print("Please ensure credentials.json is in the working "
                      "directory.")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            # Try different authentication methods
            try:
                # Method 1: Try local server (works in local development)
                print("Attempting browser-based authentication...")
                creds = flow.run_local_server(port=8080, prompt='consent')
                print("Authentication successful via browser!")
            except Exception as e:
                print(f"Browser authentication failed: {e}")
                try:
                    # Method 2: Manual auth code input (headless environments)
                    print("\nFalling back to manual authentication...")
                    print("Since browser authentication failed, we'll use "
                          "manual auth code input.")
                    print("\n" + "="*60)
                    print("MANUAL AUTHENTICATION REQUIRED")
                    print("="*60)
                    
                    # Get the authorization URL
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    print("\n1. Open this URL in your browser:")
                    print(f"   {auth_url}")
                    print("\n2. Complete the authorization flow")
                    print("3. Copy the authorization code from the final URL")
                    print("4. Paste it below when prompted")
                    print("\n" + "="*60)
                    
                    # Get auth code from user input
                    auth_code = input(
                        "\nEnter the authorization code: ").strip()
                    
                    if not auth_code:
                        print("Error: No authorization code provided!")
                        sys.exit(1)
                    
                    # Exchange auth code for credentials
                    flow.fetch_token(code=auth_code)
                    creds = flow.credentials
                    print("Manual authentication successful!")
                    
                except Exception as manual_error:
                    print(f"Manual authentication failed: {manual_error}")
                    print("\nAuthentication failed completely. "
                          "Possible solutions:")
                    print("1. Generate token.pickle locally and mount it "
                          "into Docker")
                    print("2. Check credentials.json is valid and not expired")
                    print("3. Ensure proper OAuth redirect URI configuration")
                    sys.exit(1)
            
            # Save credentials for future use
            try:
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
                print(f"Credentials saved to {token_file}")
            except Exception as e:
                print(f"Warning: Could not save token file: {e}")
    
    return build('gmail', 'v1', credentials=creds)


def delete_emails(service, user_id, query):
    """Delete emails matching the query. Uses batch operations for efficiency."""
    total_deleted = 0
    
    while True:
        results = service.users().messages().list(
            userId=user_id, q=query, maxResults=100).execute()
        messages = results.get('messages', [])
        
        if not messages:
            break
        
        print(f"Found {len(messages)} messages to delete...")
        
        # For large batches, consider using batchDelete (commented out below)
        # Uncomment and use this for better performance with large datasets:
        #
        # if len(messages) > 10:
        #     try:
        #         message_ids = [msg['id'] for msg in messages]
        #         service.users().messages().batchDelete(
        #             userId=user_id,
        #             body={'ids': message_ids}
        #         ).execute()
        #         total_deleted += len(messages)
        #         print(f"Batch deleted {len(messages)} messages")
        #         continue
        #     except Exception as e:
        #         print(f"Batch delete failed: {e}, "
        #               f"falling back to individual delete")
        
        # Individual delete with retry logic
        for message in messages:
            retries = 3
            while retries > 0:
                try:
                    service.users().messages().delete(
                        userId=user_id, id=message['id']).execute()
                    total_deleted += 1
                    print(f"Deleted message {total_deleted} "
                          f"(ID: {message['id']})")
                    break
                except Exception as e:
                    print(f"Failed to delete message with ID "
                          f"{message['id']}: {e}")
                    retries -= 1
                    if retries > 0:
                        print(f"Retrying... ({3 - retries}/3)")
                        time.sleep(1)
                    else:
                        print(f"Giving up on message with ID "
                              f"{message['id']} after 3 attempts.")
    
    print(f"Total deleted: {total_deleted} messages")


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
            print("Usage: python script_name.py "
                  "[delete_unread|delete_spam|delete_bin]")
    else:
        # No specific action specified, execute all actions
        for action, query in actions.items():
            print(f"Executing {action}...")
            delete_emails(service, user_id, query)

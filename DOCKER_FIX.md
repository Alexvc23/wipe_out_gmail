# Gmail Cleanup Docker Authentication Fix

## Problem

The error `AttributeError: 'InstalledAppFlow' object has no attribute 'run_console'` occurs because:

1. **Outdated Method**: `run_console()` was deprecated in newer versions of `google-auth-oauthlib`
2. **Headless Environment**: Docker containers don't have interactive terminals needed for `run_console()` or `run_local_server()`
3. **Missing Authentication**: Docker can't open browsers for OAuth flow

## Solution Overview

### 1. Minimum Required Versions
- `google-auth-oauthlib >= 1.0.0`
- `google-auth >= 2.23.4`
- `google-api-python-client >= 2.0.0`

### 2. Authentication Strategy
The updated `get_service()` function uses a robust fallback approach:

1. **First**: Try existing `token.pickle` file
2. **Second**: Refresh expired token if refresh_token exists
3. **Third**: Browser-based auth (local development)
4. **Fourth**: Manual auth code input (headless environments)

## Detailed Authentication Process

### Understanding OAuth 2.0 Flow in Docker Containers

The Gmail API uses OAuth 2.0 for authentication, which traditionally requires a browser to complete the authorization flow. In Docker containers (headless environments), this creates a challenge that our solution addresses through multiple fallback mechanisms.

#### Step 1: Initial Authentication Attempt
When you run the container, the application first tries:
```python
creds = flow.run_local_server(port=8080, prompt='consent')
```
This attempts to:
1. Start a local web server on port 8080
2. Open your default browser to Google's OAuth page
3. Handle the callback automatically

**Why this fails in Docker:**
- Docker containers don't have access to your desktop browser
- The container can't start a GUI application
- Network isolation prevents direct browser access

#### Step 2: Automatic Fallback to Manual Authentication
When browser authentication fails, the application automatically switches to manual mode:
```python
auth_url, _ = flow.authorization_url(prompt='consent')
print(f"Open this URL in your browser: {auth_url}")
auth_code = input("Enter the authorization code: ")
```

### How to Extract the Authorization Code

When running in Docker, you'll see output like this:
```
============================================================
MANUAL AUTHENTICATION REQUIRED
============================================================

1. Open this URL in your browser:
   https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=...

2. Complete the authorization flow
3. Copy the authorization code from the final URL
4. Paste it below when prompted

============================================================
Enter the authorization code:
```

#### Step-by-Step Token Extraction Process:

1. **Copy the OAuth URL**: Copy the entire URL from the terminal output

2. **Open in Browser**: Paste and open the URL in any web browser

3. **Complete Google Authorization**:
   - Log in to your Google account if prompted
   - Review the permissions (Gmail access)
   - Click "Allow" or "Continue"

4. **Handle the Redirect Error**: After authorization, Google redirects to:
   ```
   http://localhost:8080/?state=XXX&code=YOUR_AUTH_CODE&scope=https://mail.google.com/
   ```
   
   **Important**: You'll see a browser error like "This site can't be reached" or "Connection refused". This is **EXPECTED** and **NORMAL** in Docker environments.

5. **Extract the Authorization Code**: 
   Look at the URL in your browser's address bar. The authorization code is the value after `code=`:
   
   **Example URL:**
   ```
   http://localhost:8080/?state=NuPyqAZ6fhwls4Pm93Qj9tjp2kbKFt&code=4/0AVMBsJhk7bhx8qK6HEo3MwTNv-gwv2wO8AuFJDYxnOLCStyZySZE-1Qn0RwL28LVhOuicA&scope=https://mail.google.com/
   ```
   
   **Authorization Code:**
   ```
   4/0AVMBsJhk7bhx8qK6HEo3MwTNv-gwv2wO8AuFJDYxnOLCStyZySZE-1Qn0RwL28LVhOuicA
   ```

6. **Paste Code in Terminal**: Copy just the authorization code (not the entire URL) and paste it into the Docker container terminal when prompted

#### Visual Guide for Code Extraction:

```
FULL URL:
http://localhost:8080/?state=XXX&code=4/0AVMBsJhk7bhx8qK6HEo3MwTNv-gwv2wO8AuFJDYxnOLCStyZySZE-1Qn0RwL28LVhOuicA&scope=https://mail.google.com/

EXTRACT THIS PART:
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                           This is your authorization code
```

#### Common URL Patterns:
- The code always starts with `4/0A` for most Google OAuth flows
- The code is between `code=` and `&scope=` (or at the end if no scope parameter)
- The code is typically 60-80 characters long
- Don't include any `&` characters or other URL parameters

### Token Storage and Persistence

After successful authentication:
1. **Token Creation**: The application exchanges your authorization code for access and refresh tokens
2. **Token Storage**: Tokens are saved in `token.pickle` file for future use
3. **Automatic Refresh**: When access tokens expire, refresh tokens are used automatically
4. **Persistence**: The `token.pickle` file is mounted/copied between container runs

#### Token File Lifecycle:
```
First Run:  No token.pickle → Manual Auth → Create token.pickle
Second Run: token.pickle exists → Load tokens → Check validity
            ├─ Valid: Use existing tokens
            ├─ Expired but has refresh_token: Auto-refresh
            └─ Invalid/No refresh: Manual auth again
```

### 3. Deployment Options

#### Option A: Pre-generate token.pickle (Recommended)
1. Run authentication locally first:
   ```bash
   python src/clean_up_mail.py delete_unread
   ```
2. This generates `token.pickle` file
3. Copy/mount this file into Docker container

#### Option B: Manual authentication in Docker
1. Run container interactively:
   ```bash
   docker compose run --rm app python src/clean_up_mail.py delete_unread
   ```
2. Follow the manual authentication prompts
3. Copy the generated auth URL to your browser
4. Paste the authorization code back into the terminal

## Build and Run Instructions

### 1. Rebuild Docker Image
```bash
# Clean rebuild
docker compose build --no-cache

# Start container
docker compose up
```

### 2. Interactive Authentication (if needed)
```bash
# Run interactively for first-time auth
docker compose run --rm -it app python src/clean_up_mail.py delete_unread
```

### 3. Production Setup with Pre-generated Token
```bash
# Generate token locally first
python src/clean_up_mail.py delete_unread

# Then run in Docker (token.pickle will be mounted)
docker compose up
```

## Security Notes

### 1. Credentials Management
- **credentials.json** contains `client_secret` - keep this secure
- **Never commit credentials.json** to version control
- Consider rotating the client_secret periodically
- Use environment variables or Docker secrets for production

### 2. Token Security
- **token.pickle** contains access/refresh tokens
- Store securely and don't commit to version control
- Tokens expire and need refresh - the code handles this automatically

### 3. OAuth Redirect URI
Ensure your Google API Console has the correct redirect URIs:
- `http://localhost:8080/` (for local development)
- `urn:ietf:wg:oauth:2.0:oob` (for manual auth code flow)

## Performance Optimization

The updated code includes batch delete capability (commented out). To enable for large datasets:

```python
# Uncomment these lines in delete_emails() function:
if len(messages) > 10:
    try:
        message_ids = [msg['id'] for msg in messages]
        service.users().messages().batchDelete(
            userId=user_id,
            body={'ids': message_ids}
        ).execute()
        total_deleted += len(messages)
        print(f"Batch deleted {len(messages)} messages")
        continue
    except Exception as e:
        print(f"Batch delete failed: {e}, falling back to individual delete")
```

**Note**: Batch delete permanently removes messages (bypasses trash).

## Troubleshooting

### Understanding the "This site can't be reached" Error

When you see this browser error, **don't panic** - it's completely normal in Docker environments:

```
This site can't be reached
localhost refused to connect.
ERR_CONNECTION_REFUSED
```

**Why this happens:**
- Google redirects to `http://localhost:8080/` after authorization
- Your local machine has no web server running on port 8080
- The Docker container can't expose this port to handle the callback
- This is the expected behavior when using manual authentication

**What to do:**
1. **Don't close the browser tab** - you need the URL
2. **Look at the address bar** - the authorization code is in the URL
3. **Extract the code** as described in the authentication section above
4. **Paste it in the terminal** when prompted

### Common Issues

1. **"Browser authentication failed"**
   - Expected in Docker - will fallback to manual auth
   - Copy the URL and open in your browser

2. **"Manual authentication failed"**
   - Check credentials.json is valid
   - Verify OAuth redirect URIs in Google Console
   - Ensure authorization code is copied correctly
   - Make sure you copied ONLY the code part, not the entire URL

3. **"Token refresh failed"**
   - Delete token.pickle and re-authenticate
   - Check internet connectivity

4. **"Permission denied" errors**
   - Verify Gmail API is enabled in Google Console
   - Check OAuth scopes are correct
   - Ensure Gmail account has necessary permissions

5. **"Invalid authorization code" errors**
   - Code might be expired (they expire quickly, usually within 10 minutes)
   - Ensure you copied the complete code without extra characters
   - Don't include URL parameters like `&scope=` or `&state=`
   - Try the authentication process again with a fresh code

### Real-World Authentication Example

Here's a complete example of what you'll see during authentication:

```bash
$ docker compose run --rm -it app python src/clean_up_mail.py delete_unread

Attempting browser-based authentication...
Browser authentication failed: could not locate runnable browser

Falling back to manual authentication...
Since browser authentication failed, we'll use manual auth code input.

============================================================
MANUAL AUTHENTICATION REQUIRED
============================================================

1. Open this URL in your browser:
   https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=654642886962-nih6km389e2i731r8mi0a7ppqtob2l6q.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&scope=https%3A%2F%2Fmail.google.com%2F&state=ABC123&prompt=consent&access_type=offline

2. Complete the authorization flow
3. Copy the authorization code from the final URL
4. Paste it below when prompted

============================================================

Enter the authorization code: 4/0AVMBsJhk7bhx8qK6HEo3MwTNv-gwv2wO8AuFJDYxnOLCStyZySZE-1Qn0RwL28LVhOuicA

Manual authentication successful!
Credentials saved to token.pickle
Found 100 messages to delete...
```

### Debug Commands

```bash
# Check installed versions
docker compose run --rm app pip show google-auth-oauthlib google-auth google-api-python-client

# Test authentication only
docker compose run --rm app python -c "from src.clean_up_mail import get_service; print('Auth successful:', get_service() is not None)"

# Run with verbose output
docker compose run --rm app python -v src/clean_up_mail.py delete_unread

# Check if token.pickle exists and is valid
docker compose run --rm app python -c "
import pickle, os
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as f:
        creds = pickle.load(f)
    print(f'Token exists: {creds.valid if creds else False}')
    print(f'Token expired: {creds.expired if creds else "N/A"}')
    print(f'Has refresh token: {bool(creds.refresh_token) if creds else False}')
else:
    print('No token.pickle file found')
"

# Test OAuth URL generation (without authentication)
docker compose run --rm app python -c "
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ['https://mail.google.com/']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
auth_url, _ = flow.authorization_url(prompt='consent')
print('OAuth URL generated successfully:', len(auth_url) > 0)
"
```

### Security Best Practices for Container Authentication

1. **Token File Security**:
   ```bash
   # Set proper permissions on token file
   chmod 600 token.pickle
   
   # Don't commit token files
   echo "token.pickle" >> .gitignore
   ```

2. **Credentials Management**:
   ```bash
   # Use environment variables for production
   export GOOGLE_CLIENT_ID="your-client-id"
   export GOOGLE_CLIENT_SECRET="your-client-secret"
   
   # Or use Docker secrets
   docker secret create gmail_credentials ./credentials.json
   ```

3. **Container Volume Mounting**:
   ```yaml
   # In docker-compose.yml
   services:
     app:
       volumes:
         - ./token.pickle:/app/token.pickle:ro  # Read-only mount
         - ./credentials.json:/app/credentials.json:ro
   ```

## File Structure After Fix

```
wipe_out_gmail/
├── .dockerignore          # Docker ignore patterns
├── Dockerfile             # Updated to copy credentials.json
├── docker-compose.yml     # Service configuration
├── requirements.txt       # Updated minimum versions
├── credentials.json       # OAuth client secrets (keep secure!)
├── token.pickle          # Generated auth tokens (keep secure!)
├── src/
│   ├── __init__.py
│   └── clean_up_mail.py  # Fixed authentication logic
└── README.md
```

## Next Steps

1. **Backup Strategy**: Implement email backup before mass deletion
2. **Logging**: Add proper logging instead of print statements
3. **Configuration**: Move to environment variables for sensitive data
4. **Monitoring**: Add health checks and monitoring for production use
5. **Testing**: Add unit tests for authentication and email operations

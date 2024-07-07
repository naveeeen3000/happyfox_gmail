"""Fetch user mails from Gmail account."""
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from gmail.oauth import authorize
import os

def fetch_mails(limit=None):
    """Fetch user mails from Gmail account."""
    try:
        if not os.path.exists('token.json'):
            creds = authorize()
        else:
            creds = Credentials.from_authorized_user_file('token.json')
        
        service = build('gmail', 'v1', credentials=creds)

        ## Fetch the user's mails

        messages = service.users().messages().list(userId='me').execute()
        mail_ids = messages.get('messages', [])
        if limit:
            mail_ids = mail_ids[:limit]

        print(f"Total mails: {len(mail_ids)}")
        mails = []
        for mail in mail_ids:
            print(f"Fetching mail {mail.get('id')}")
            mail_id = mail.get('id')
            if not mail_id:
                continue
            message = service.users().messages().get(userId='me', id=mail_id).execute()
            mails.append(message)
        return mails
    except Exception as e:
        print(f"Error fetching mails: {e}")
        return []
    
"""GMAIL REST APIS"""
from gmail.oauth import authorize
from core.models import Mail
import requests
import json

def move_mail(mail: Mail, label_id: str, labels: list[str] = []):
    """Move mail to a label."""
    mail_id = mail.mail_id
    creds = authorize()
    url = f'https://www.googleapis.com/gmail/v1/users/me/messages/{mail_id}/modify'
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }
    data = {
        'addLabelIds': [label_id],
        'removeLabelIds': labels
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Mail moved to {label_id}. Subject: {mail.subject}")
    else:
        print(response.content)
        print(f"Failed to move mail to {label_id}")

def mark_read(mail: Mail):
    """Mark mail as read."""
    mail_id = mail.mail_id
    creds = authorize()
    url = f'https://www.googleapis.com/gmail/v1/users/me/messages/{mail_id}/modify'
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }
    data = {
        'removeLabelIds': ['UNREAD']
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Mail marked as read. Subject: {mail.subject}")
    else:
        print(response.content)
        print(f"Failed to mark mail as read")

def mark_unread(mail: Mail):
    """Mark mail as unread."""
    mail_id = mail.mail_id
    creds = authorize()
    url = f'https://www.googleapis.com/gmail/v1/users/me/messages/{mail_id}/modify'
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }
    data = {
        'addLabelIds': ['UNREAD']
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Mail marked as unread. Subject: {mail.subject}")
    else:
        print(response.content)
        print(f"Failed to mark mail as unread")

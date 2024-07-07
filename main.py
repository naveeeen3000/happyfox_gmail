"""Entry point for the application."""
from gmail.gmail import fetch_mails
from core.database import Database
from core import rules, utils, queries as query
from core.models import Mail
from sqlalchemy.orm import Session

def main():
    """Entry point for the application."""
    db = Database()
    session = db.get_session()
    db.base.metadata.create_all(db.engine)
    try:

        print("Fetching mails from Gmail\n")
        mails = fetch_mails(limit=20)

        print(f"Total mails fetched: {len(mails)}\n")
        clean_mail_data = build_mail_data(mails)
        query.insert_bulk_mail(session, clean_mail_data)
        print(f"Total mails to inserted: {len(clean_mail_data)}\n")
        
        mails_from_db = query.get_mails(db=session)
        print("Applying rules to mails fetched from db\n")
        rules.apply_rules(session,mails_from_db)
    except Exception as e:
        print("Error: ", str(e))
    finally:
        ## Clean up the db
        delete_mails_from_db(session)
        session.close()

def build_mail_data(mails: list) -> list[dict]:
    """Build mail data."""
    mail_data = []
    for mail in mails:
        headers = mail.get('payload', {}).get('headers', [{}])
        sender = get_key_value_from_headers(headers, 'From')
        reciever = get_key_value_from_headers(headers, 'To')
        subject = get_key_value_from_headers(headers, 'Subject')
        timestamp = get_key_value_from_headers(headers, 'Date')
        # date format = Sat, 06 Jul 2024 13:23:14 +0530
        if '<' in sender:
            sender = sender.split('<')[1].split('>')[0]
        if '<' in reciever:
            reciever = reciever.split('<')[1].split('>')[0]
        try:
            sent_at = utils.parse_date(timestamp)
        except Exception as e:
            print(str(e), "Failed to parse date for mail: ", timestamp)
            continue
        mail_data.append({
            'mail_id': mail.get('id'),
            'sender': sender,
            'subject': subject,
            'body': mail.get('snippet', ''),
            'sent_at': sent_at,
            'labels': mail.get('labelIds', []),
            'reciever': reciever
        })
    return mail_data

def get_key_value_from_headers(headers: list, key: str) -> str:
    """Get key value from headers."""
    for header in headers:
        if header.get('name') == key:
            return header.get('value')
    return ''

def delete_mails_from_db(session: Session):
    """Delete mails from db."""
    session.query(Mail).delete()
    session.commit()

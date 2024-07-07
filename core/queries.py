"""DB queries for the core app."""
from sqlalchemy import select, or_, and_
from core.models import Mail
from core.utils import RULES_FILED_MAP, get_condition_datetime
from sqlalchemy.orm import Session
import json

def insert_bulk_mail(db: Session, mail_data: list[dict]):
    """Insert mail into the database."""
    bulk_mail_data = []
    for mail in mail_data:
        mail_data = Mail(
            mail_id=mail.get('mail_id'),
            sender=mail.get('sender'),
            reciever=mail.get('reciever'),
            subject=mail.get('subject'),
            body=mail.get('body'),
            sent_at=mail.get('sent_at'),
            labels=json.dumps(mail.get('labels'))
        )
        bulk_mail_data.append(mail_data)
    db.bulk_save_objects(bulk_mail_data)
    db.commit()

def get_mails(db: Session) -> list[Mail]:
    """Get mails from the database."""
    result = db.query(Mail).all()
    return result

def get_mails_by_rule(db: Session, rule: dict) -> list[Mail]:
    """Get mails by rule."""
    queries = []
    for conition in rule.get('conditions', []):
        field = RULES_FILED_MAP.get(conition.get('field'))
        value = conition.get('value')
        if conition.get('operator') == 'contains':
            queries.append(getattr(Mail, field).ilike('%'+value+'%'))
        elif conition.get('operator') == 'equals':
            queries.append(getattr(Mail, field) == value)
        elif conition.get('operator') == 'notContain':
            queries.append(getattr(Mail, field).notlike('%'+value+'%'))
        elif conition.get('operator') == 'notEqual':
            queries.append(getattr(Mail, field) != value)
        elif conition.get('operator') == 'greaterThan':
            datetime = get_condition_datetime(value, less_than=False)
            queries.append(getattr(Mail, field) > datetime)
        elif conition.get('operator') == 'lessThan':
            datetime = get_condition_datetime(value, less_than=True)
            queries.append(getattr(Mail, field) < datetime)
    predicate = rule.get('predicate', 'any').lower()
    if predicate == 'all':
        query = select(Mail).where(and_(*queries))
    elif predicate == 'any':
        query = select(Mail).where((or_(*queries)))
    result = db.execute(query).scalars().all()
    return result

def update_mail_labels(db, mail: Mail, label: str):
    """Update mail labels."""
    mail_id = mail.id
    mail = db.query(Mail).filter(Mail.id == mail_id).first()
    current_labels = json.loads(mail.labels)
    current_labels.append(label)
    current_labels = list(set(current_labels))
    mail.labels = json.dumps(current_labels)
    db.commit()

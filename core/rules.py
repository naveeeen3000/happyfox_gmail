"""Applying rules for mails."""
from gmail.api import move_mail, mark_read, mark_unread
from core import queries
from sqlalchemy.orm import Session
import json

def apply_rules(db: Session, rules_nums=None):
    """Apply rules."""
    try:
        rules = get_rules().get('rules', [])
        if rules_nums:
            rules = rules[:rules_nums]
        for rule in rules:
            print(f'Applying rule: {rule.get("name")}')
            mails = queries.get_mails_by_rule(db, rule)
            actions = rule.get('actions', [])
            perform_action(db, mails, actions)
        return 1
    except Exception as e:
        print("Error applying rules: ", str(e))
        return 0

def get_rules() -> dict:
    """Get rules."""
    with open('rules.json', 'r') as file:
        return json.load(file)
    
def perform_action(db, mails: list[dict], actions: list):
    """Perform action."""
    for mail in mails:
        labels = json.loads(mail.labels or '[]')
        for action in actions:
            print(f'Performing action: {action.get("type")}')
            label = ''
            if action.get('type') == 'move' and action.get('destination') not in labels:
                label = action.get('destination')
                move_mail(mail, action.get('destination'), labels=labels)
            elif action.get('type') == 'mark_as_read' and 'READ' not in labels:
                label = 'READ'
                mark_read(mail)
            elif action.get('type') == 'mark_as_unread' and 'UNREAD' in labels:
                label = 'UNREAD'
                mark_unread(mail)
            if label:
                queries.update_mail_labels(db, mail, label)

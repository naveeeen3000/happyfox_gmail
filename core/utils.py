"""CORE UTILS"""
from datetime import datetime, timedelta
from dateutil import parser
import pytz

RULES_FILED_MAP = {
    'From': 'sender',
    'To': 'reciever',
    'Subject': 'subject',
    'dateTime': 'sent_at'
}

def get_context(**kwargs):
    """Return a dictionary of context variables."""
    return kwargs

def get_condition_datetime(value: str, less_than=False):
    """Get condition datetime."""
    val = value.split(' ')
    count = val[0]
    unit = val[1]
    if less_than:
        count = -count
    if unit == 'years':
        return datetime.now() + timedelta(years=count)
    elif unit == 'months':
        return datetime.now() + timedelta(months=count)
    elif unit == 'days':
        return datetime.now() + timedelta(days=count)
    elif unit == 'hours':
        return datetime.now() + timedelta(hours=count)
    elif unit == 'minutes':
        return datetime.now() + timedelta(minutes=count)
    elif unit == 'seconds':
        return datetime.now() + timedelta(seconds=count)
    return datetime.now()

def parse_date(date_str):
    # Handle specific known timezones
    if "(IST)" in date_str:
        return parser.parse(date_str).replace(tzinfo=pytz.timezone('Asia/Kolkata'))
    elif "(UTC)" in date_str:
        return parser.parse(date_str).replace(tzinfo=pytz.UTC)
    else:
        return parser.parse(date_str)

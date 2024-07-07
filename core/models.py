"""DB Models for the core app."""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from core.database import Database

Base = Database().base

class Mail(Base):
    """Mail model."""
    __tablename__ = 'mails'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mail_id = Column(String(length=255), nullable=False)
    reciever = Column(String(length=255), nullable=False)
    sender = Column(String(length=255), nullable=False)
    subject = Column(String(length=255), nullable=False)
    body = Column(Text, nullable=False)
    sent_at = Column(DateTime, nullable=False)
    labels = Column(JSON)

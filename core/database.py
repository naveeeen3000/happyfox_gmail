"""Datanase for storing mails."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

class Database:
    """Database class."""
    _instance = None

    def __new__(cls, db_name='mails.db'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(f'sqlite:///{db_name}')
            cls._instance.session = sessionmaker(bind=cls._instance.engine)()
            cls._instance.base = declarative_base()
        return cls._instance
    
    def get_session(self) -> Session:
        """Return session."""
        return self.session

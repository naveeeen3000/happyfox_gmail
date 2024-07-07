import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.queries import insert_bulk_mail
from core.models import Mail
from core.database import Database
from gmail.gmail import fetch_mails
from main import build_mail_data

class TestBulkInsert(unittest.TestCase):
    """Test bulk insert."""
    
    @classmethod
    def setUpClass(cls):
        """Setup class."""
        cls.engine = create_engine('sqlite:///test.db')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.db = Database(db_name='test.db')
        cls.db.base.metadata.create_all(cls.engine)
    
    @classmethod
    def tearDownClass(cls):
        """Tear down class."""
        cls.session.query(Mail).delete()
        cls.session.commit()
        cls.session.close()
        cls.db.engine.dispose()
    
    def setUp(self):
        """Setup."""
        self.session = self.Session()
    
    def test_insert_bulk_mail(self):
        """Test insert bulk mail."""
        mail_data = fetch_mails(limit=5)
        clean_mail_data = build_mail_data(mail_data)
        insert_bulk_mail(self.session, clean_mail_data)
        mails = self.session.query(Mail).all()
        self.assertEqual(len(mails), 5, "Failed to insert mails")
    
    def tearDown(self):
        """Tear down."""
        self.session.rollback()
        self.session.close()

if __name__ == '__main__':
    unittest.main()

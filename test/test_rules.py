import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.rules import apply_rules
from core.models import Mail
from core.database import Database
from core.queries import insert_bulk_mail, get_mails
from gmail.gmail import fetch_mails
from main import build_mail_data

class TestRules(unittest.TestCase):
    """Test rules."""

    @classmethod
    def setUpClass(cls):
        """Setup class."""
        cls.engine = create_engine('sqlite:///test.db')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.db = Database(db_name='test.db')
        cls.db.base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Tear down class."""
        cls.db.base.metadata.drop_all(cls.engine)
        cls.db.engine.dispose()

    def setUp(self):
        """Setup."""
        self.session = self.Session()

    def test_apply_rules(self):
        """Test apply rules."""
        mail_data = fetch_mails(limit=2)
        clean_mail_data = build_mail_data(mail_data)
        insert_bulk_mail(self.session, clean_mail_data)
        mails = get_mails(self.session)
        status = apply_rules(self.session, mails)
        self.assertTrue(status, "Failed to apply rules")

    def tearDown(self):
        """Tear down."""
        self.session.rollback()
        self.session.close()

if __name__ == '__main__':
    unittest.main()

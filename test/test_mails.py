import unittest
from gmail import gmail

class TestExample(unittest.TestCase):

    def test_fetch_mail(self):
        mails = gmail.fetch_mails(limit=3)
        self.assertEqual(len(mails), 3, "Failed to fetch mails from gmail")
    

if __name__ == "__main__":
    unittest.main()

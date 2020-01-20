import unittest

class TestCodeRuns(unittest.TestCase):
    def setUp(self):
        self.server = Server_foundongithub.py

    def test_home(self):
        result = self.app.get('/')
        # Make your assertions
import os
import sys
sys.path.insert(1, os.path.join(os.path.abspath('.'), '../../lib'))
import flaskr
import unittest
import tempfile
import os

class TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_hola_mundo(self):
        assert True

if __name__ == '__main__':
    unittest.main()
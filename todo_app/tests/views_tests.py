import logging
from tests.test import AppengineTestCase

class IndexTestCase(AppengineTestCase):
    def test_index(self):
        logging.info("Starting ")
        resp = self.app.get('/')
        self.assertEquals(resp.status,"200 OK","Error")

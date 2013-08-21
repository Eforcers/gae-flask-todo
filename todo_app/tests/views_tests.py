import logging
from main import app
from google.appengine.ext import testbed
from tests.test import AppengineTestCase

class IndexTestCase(AppengineTestCase):
    def testIndex(self):
        logging.info("Starting ")
        resp = self.app.get('/')
        self.assertEquals(resp.status,"200 OK","Error")

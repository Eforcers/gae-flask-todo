APP_ENGINE_PATH = '/home/alessandro/google_appengine'
APP_ENGINE_LIBS_PATH = '/home/alessandro/google_appengine/lib/'

LIBS = ['yaml']

import sys
sys.path.insert(1, APP_ENGINE_PATH)

for LIB in LIBS:
    sys.path.insert(1, APP_ENGINE_LIBS_PATH +LIB)

import unittest
from models import TestModel
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class AppEngineTestCase(unittest.TestCase):

    def test_insert_entity(self):
        TestModel().put()
        self.assertEqual(1, len(TestModel.all().fetch(2)))

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
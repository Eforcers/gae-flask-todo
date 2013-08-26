import os
import sys

APP_ENGINE_SDK = 'C:\Program Files (x86)\Google\google_appengine'
LIBS = ['yaml-3.10',
        'protorpc',
        'simplejson',
        'antlr3',
        'fancy_urllib',
        'ipaddr',
        'jinja2-2.6'
        ]
SEPARATOR = "\\"
sys.path.insert(1, APP_ENGINE_SDK)
sys.path.insert(2, os.path.join(os.path.abspath('.'), 'lib'))
for LIB in LIBS:
    sys.path.append('%s%slib%s%s' % (APP_ENGINE_SDK,SEPARATOR,SEPARATOR,LIB))

from google.appengine.tools import dev_appserver
from google.appengine.tools.dev_appserver_main import ParseArguments

args, option_dict = ParseArguments(sys.argv) # Otherwise the option_dict isn't populated.
dev_appserver.SetupStubs('local', **option_dict)
os.environ['SERVER_NAME'] = 'local'
os.environ['SERVER_PORT'] = '8080'

import unittest
#from tests.views_tests import *
from tests.api_test import *

if __name__ == '__main__':
    unittest.main()
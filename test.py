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

sys.path.insert(1, APP_ENGINE_SDK)
for LIB in LIBS:
    sys.path.append(os.path.join(APP_ENGINE_SDK,'lib',LIB))

from google.appengine.tools import dev_appserver
from google.appengine.tools.dev_appserver_main import ParseArguments

args, option_dict = ParseArguments(sys.argv) # Otherwise the option_dict isn't populated.
dev_appserver.SetupStubs('local', **option_dict)
os.environ['SERVER_NAME'] = 'local'
os.environ['SERVER_PORT'] = '8080'

import unittest
from tests.views_tests import *
from tests.api_test import *


test_gui = True
if test_gui:
    from tests.gui_test import *
    GuiTest.APP_ENGINE_SDK = APP_ENGINE_SDK
    GuiTest.PROJECT_PATH = os.path.dirname(__file__)


if __name__ == '__main__':
    unittest.main()
import os
import sys
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))
from google.appengine.ext import endpoints
from todo_app.apis import TodoApi

from main import app
api = endpoints.api_server([TodoApi], restricted=False)
from flask.app import Flask
from flask.ext.admin.base import MenuLink
import settings
from todo_app.admin_views import AdminIndex
from werkzeug.debug import DebuggedApplication
from flask_admin import Admin
from google.appengine.api import users


flask_app = Flask(__name__)
flask_app.config.from_object(settings)

admin = Admin(flask_app, name='TODO', index_view=AdminIndex(url='/admin', name='Home'), )
admin.add_link(MenuLink(name='Logout',url = users.create_logout_url('/')))

if flask_app.config['DEBUG']:
    flask_app.debug = True
    app = DebuggedApplication(flask_app, evalex=True)

app = flask_app

from todo_app import admin_views
from todo_app import views
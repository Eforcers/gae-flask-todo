from google.appengine.api import users
from flask.ext.admin import BaseView, expose
from flask.ext.admin.base import AdminIndexView
from werkzeug.routing import RequestRedirect
import logging


class AuthView(BaseView):
    def is_accessible(self):
        if users.is_current_user_admin():
            return True
        else:
            raise RequestRedirect(users.create_login_url(self.url))

class AdminIndex(AuthView, AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('index.html')

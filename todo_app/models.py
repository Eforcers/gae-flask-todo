import logging
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb.model import EndpointsModel, EndpointsAliasProperty


class TodoModel(EndpointsModel):
    title = ndb.StringProperty()
    completed = ndb.BooleanProperty()

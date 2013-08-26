import logging
from apis import TodoApi
from endpoints_proto_datastore.ndb.model import EndpointsModel, properties
from protorpc.messages import Field
from models import TodoModel
from tests.test import AppengineTestCase
import mock

class TestCase(AppengineTestCase):
    TITLE = "Todo 1"
    IS_COMPLETED = False
    ###############################################
    #mock is made to the methods validate_element and  _CopyFromEntity because in testing environment  throws exception because classes are not the same
    def copy_from_entity(self, entity):
        for prop in entity._EndpointsPropertyItervalues():
          attr_name = prop._code_name
          value = getattr(entity, attr_name)
          if value is not None:
            if isinstance(prop, properties.EndpointsAliasProperty):
              value_set = getattr(self, attr_name) is not None
            else:
              value_set = prop._name in self._values
            if not value_set:
              setattr(self, attr_name, value)

    def validate_element(self, value):
        pass
    ##############################################

    def test_insert(self):
        todoApi = TodoApi()
        #gets an instance of the message that is generated dynamically by the library endpoints_proto_datastore
        request = todoApi.TodoInsert.remote.request_type()
        request.title = self.TITLE
        todoApi.TodoInsert(request)
        query = TodoModel.query().fetch()
        self.assertEqual(1, len(query))
        result = query[0]
        self.assertEquals(self.TITLE, result.title)
        self.assertEquals(self.IS_COMPLETED, result.completed)

    @mock.patch.object(EndpointsModel, '_CopyFromEntity', copy_from_entity)
    def test_delete(self):
        todoModel = TodoModel(title = self.TITLE).put()
        todoApi = TodoApi()
        request = todoApi.TodoDelete.remote.request_type()
        request.id = 1
        todoApi.TodoDelete(request)

    @mock.patch.object(EndpointsModel, '_CopyFromEntity', copy_from_entity)
    def test_toggle(self):
        todoModel = TodoModel(title = self.TITLE).put()
        todoApi = TodoApi()
        request = todoApi.TodoToggle.remote.request_type()
        request.id = 1
        todoApi.TodoToggle(request)

    @mock.patch.object(Field, 'validate_element', validate_element)
    def test_list(self):
        todoModel = TodoModel(title = self.TITLE, completed = self.IS_COMPLETED).put()
        todoApi = TodoApi()
        request = todoApi.TodosList.remote.request_type()
        todos_list = todoApi.TodosList(request).items

        self.assertEqual(1, len(todos_list))
        result = todos_list[0]
        self.assertEquals(self.TITLE, result.title)
        self.assertEquals(self.IS_COMPLETED, result.completed)
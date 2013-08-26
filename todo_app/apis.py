import logging
from google.appengine.ext import endpoints
from protorpc import remote
from todo_app.models import TodoModel


@endpoints.api(name='todo', version='v1', description='Eforcers TODO API')
class TodoApi(remote.Service):

    @TodoModel.method(request_fields=('title',),
                      response_fields=('completed','title','id'),
                      path='todo',
                      http_method='POST',
                      name='todo.insert')
    def TodoInsert(self, todo):
        logging.info(todo)
        todo.completed = False
        todo.put()
        return todo

    @TodoModel.method(request_fields=('id',),
                      path='todo/{id}',
                      http_method='DELETE',
                      name='todo.delete')
    def TodoDelete(self, todo):
        todo.key.delete()
        return todo

    @TodoModel.method(request_fields=('id',),
                      response_fields=('completed','title','id'),
                      path='todo/{id}',
                      name='todo.toggle')
    def TodoToggle(self, todo):
        todo.completed = not todo.completed
        todo.put()
        return todo

    @TodoModel.query_method(query_fields=('limit', 'order', 'pageToken'),
                            collection_fields=('completed','title','id'),
                            path='todos',
                            name='todos.list')
    def TodosList(self, query):
        return query


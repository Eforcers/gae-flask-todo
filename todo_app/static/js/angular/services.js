Todo_app.service('TodoService',function($q, $rootScope) {
	
  this.listTodos = function() {
	  var deferred = $q.defer();
	  gapi.client.todo.todos.list().execute(function(resp) {
		 $rootScope.$apply(deferred.resolve(resp.items));
	  });
	  return deferred.promise;
  };
  
  this.insertTodo = function(title) {
	  var deferred = $q.defer();
	  gapi.client.todo.todo.insert({'title':title}).execute(function(resp) {
		 $rootScope.$apply(deferred.resolve(resp));
	  });
	  return deferred.promise;
  };


  this.toggleTodo = function(id) {
	  var deferred = $q.defer();
	  gapi.client.todo.todo.toggle({'id':id}).execute(function(resp) {
		 $rootScope.$apply(deferred.resolve(resp));
	  });
	  return deferred.promise;
  };

  this.removeTodo = function(id) {
	  var deferred = $q.defer();
	  gapi.client.todo.todo.delete({'id':id}).execute(function(resp) {
		 $rootScope.$apply(deferred.resolve(resp));
	  });
	  return deferred.promise;
  };
});
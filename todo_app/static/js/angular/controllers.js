
todoCtrl = Todo_app.controller('todoCtrl', function ($window, $scope, TodoService) {
    $window.init = function() {
      $scope.$apply($scope.load_todo_api);
    };

    $scope.$watch(TodoService.isLoaded, function(loaded) {
        $scope.loaded = loaded;
    });

    $scope.load_todo_api = function() {
        var apiRoot = '//' + window.location.host + '/_ah/api';
        gapi.client.load('todo', 'v1', function() {
            $scope.is_api_ready = true;
            $scope.loadTodos();
        }, apiRoot);
    };


	$scope.loadTodos = function(){
		var promise = TodoService.listtodos();
		promise.then(function(resp) {
			$scope.todos = resp.items
		});
	};
	
	$scope.addTodo = function(){
		var promise = TodoService.inserttodo({'title':$scope.newTitle});
		promise.then(function(todo) {
			$scope.newTitle = ""
            setTimeout(function(){
                $scope.loadTodos();
            }, 500);

		});
		
	};

    $scope.changeTodo = function(todo){
		var promise = TodoService.toggletodo({'id':todo.id});
		promise.then(function(todo) {
			console.log("task was toggle",todo);
		});
	};

    $scope.delTodo = function(todo){
		var promise = TodoService.deletetodo({'id':todo.id});
		promise.then(function(todo) {
			setTimeout(function(){
                $scope.loadTodos();
            }, 500);
		});
	};


	
	//$scope.loadTodos();
});

todoCtrl.$inject = ['$window','$scope','TodoService'];
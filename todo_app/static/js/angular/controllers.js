todoCtrl = Todo_app.controller('todoCtrl', function ($scope, TodoService) {
	$scope.loadTodos = function(){
		var promise = TodoService.listTodos();
		promise.then(function(todos) {
			$scope.todos = todos
		});
	};
	
	$scope.addTodo = function(){
		var promise = TodoService.insertTodo($scope.newTitle);
		promise.then(function(todo) {
			$scope.newTitle = ""
            setTimeout(function(){
                $scope.loadTodos();
            }, 500);

		});
		
	};

    $scope.changeTodo = function(todo){
		var promise = TodoService.toggleTodo(todo.id);
		promise.then(function(todo) {
			console.log("task was toggle",todo);
		});
	};

    $scope.delTodo = function(todo){
		var promise = TodoService.removeTodo(todo.id);
		promise.then(function(todo) {
			setTimeout(function(){
                $scope.loadTodos();
            }, 500);
		});
	};
	
	
	$scope.loadTodos();
});

todoCtrl.$inject = ['$scope','TodoService'];
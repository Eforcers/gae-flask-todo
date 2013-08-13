
todoCtrl = Todo_app.controller('todoCtrl', function ($window, $scope, EndpointService) {
    $window.init = function() {
      $scope.$apply($scope.load_todo_api);
    };

    $scope.load_todo_api = function() {
        EndpointService.loadService('todo', 'v1');
    };

    $scope.$watch(EndpointService.isLoaded, function(loaded) {
        $scope.loaded = loaded;
        if (loaded){
            $scope.loadTodos();
        }
    });

    $scope.loadTodos = function(){
        var promise = EndpointService.listTodos();
        promise.then(function(resp) {
            $scope.todos = resp.items
        });
    };

    $scope.addTodo = function(){
        var promise = EndpointService.insertTodo({'title':$scope.newTitle});
        promise.then(function(todo) {
            $scope.newTitle = ""
            setTimeout(function(){
                $scope.loadTodos();
            }, 500);

        });
    };

    $scope.changeTodo = function(todo){
        var promise = EndpointService.toggleTodo({'id':todo.id});
        promise.then(function(todo) {
            console.log("task was toggle",todo);
        });
    };

    $scope.delTodo = function(todo){
        var promise = EndpointService.deleteTodo({'id':todo.id});
        promise.then(function(todo) {
            setTimeout(function(){
                $scope.loadTodos();
            }, 500);
        });
    };
});

todoCtrl.$inject = ['$window','$scope','EndpointService'];
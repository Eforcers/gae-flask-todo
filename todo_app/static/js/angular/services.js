Todo_app.service('TodoService',function($q, $rootScope,$http) {

    var service = this;
    var builder = function (api, resource, method){
        return function (args) {
              var deferred = $q.defer();
              gapi.client[api][resource][method](args).execute(function(resp) {
                 $rootScope.$apply(deferred.resolve(resp));
              });
              return deferred.promise;
        };
    }
    var loaded = false;
    this.isLoaded = function() { return loaded; };
    $http.get('/_ah/api/discovery/v1/apis/todo/v1/rest').success( function(data) {
        console.log(data);
        for (resource in data.resources){
            for(method in data.resources[resource].methods){
                service[method+resource] = builder('todo',resource,  method);
                 console.log("Method "+method+resource+" created");
            }
        }
        loaded = true;
        $rootScope.$$phase || $rootScope.$apply();
    });
});
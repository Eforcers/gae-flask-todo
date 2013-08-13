Todo_app.service('EndpointService',function($q, $rootScope,$http) {

    var service = this;
    var http = $http;

    /**
     * build service methods from discovery document
     * @param api
     * @param resource
     * @param method
     * @returns {Function}
     */
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

    /**
     * brings the discovery document and adds methods in the service built from the information brought
     * @param api
     * @param version
     */
    this.loadService = function(api, version){
        service.apiName = api;
        service.apiVersion = version;
        var apiRoot = '//' + window.location.host + '/_ah/api';
        gapi.client.load(service.apiName, service.apiVersion, function() {
            var apiUrl = '';
            http.get(apiRoot+'/discovery/v1/apis/'+service.apiName+'/'+service.apiVersion+'/rest').success( function(data) {
                console.log(data);
                for (resource in data.resources){
                    for(method in data.resources[resource].methods){
                        var capitalizedResource = resource[0].toUpperCase() + resource.substring(1);
                        service[method+capitalizedResource] = builder(service.apiName,resource,  method);
                        console.log("Method "+method+capitalizedResource+" created");
                    }
                }
                loaded = true;
                //$rootScope.$$phase || $rootScope.$apply();
            });
            $rootScope.$$phase || $rootScope.$apply();
        }, apiRoot);
    }
});
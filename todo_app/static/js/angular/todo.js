initialize = function(apiRoot) {
	var apisToLoad;
	var callback = function() {
		if (--apisToLoad == 0) {
			//bootstrap manually angularjs after our api are loaded
			angular.bootstrap(document, [ "todo_app" ]);
		}
	}
	apisToLoad = 1; // must match number of calls to gapi.client.load()
	gapi.client.load('todo', 'v1', callback, apiRoot);
    //gapi.client.load('discovery', 'v1', function(){console.log(gapi.client)}, apiRoot);
};

var Todo_app = angular.module('todo_app', []);

Todo_app.config(function($interpolateProvider) {
	  $interpolateProvider.startSymbol('{[{');
	  $interpolateProvider.endSymbol('}]}');
});

function init() {
  window.init();
}

var Todo_app = angular.module('todo_app', []);

Todo_app.config(function($interpolateProvider) {
	  $interpolateProvider.startSymbol('{[{');
	  $interpolateProvider.endSymbol('}]}');
});

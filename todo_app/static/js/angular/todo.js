/**
 * function called after loading of endpoint client
 */
function init() {
  window.init();
//  console.log('Endpoints client loaded.');
}


/**
 * The main Todo app module
 *
 * @type {angular.Module}
 */
var Todo_app = angular.module('todo_app', []);

/**
 * changes the symbols of open and close for compatibility problems with Jinja2
 */
Todo_app.config(function($interpolateProvider) {
	  $interpolateProvider.startSymbol('{[{');
	  $interpolateProvider.endSymbol('}]}');
});

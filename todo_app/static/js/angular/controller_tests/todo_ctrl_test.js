/*
 Test for the To-do model controller.
 */

describe('Todo model controller tests', function () {

    console.log('Starting todo controller test...')

    var $scope = null;
    var ctrl = null;

    //you need to indicate your module in a test
    beforeEach(module('todo_app'));

    //Create a mock To-do service
    var mockService = {
        someAsyncCall: function (x) {
            data = {
                "items": [
                    {
                        "completed": false,
                        "id": "1",
                        "title": "todo 2"
                    },
                    {
                        "completed": false,
                        "id": "2",
                        "title": "todo 1"
                    },
                    {
                        "completed": false,
                        "id": "3",
                        "title": "todo 3"
                    }
                ]
            }
            return data;
        }
    }

    /*
    Inject the mock service in the controller.
    */
    beforeEach(inject(function($rootScope, $controller) {
        //create a scope object for us to use.
        $scope = $rootScope.$new();
        //now run that scope through the controller function,
        //injecting any services or other injectables we need.
        ctrl = $controller('todoCtrl', {
          $scope: $scope,
          service: mockService
        });
      }));

    /*
     Tests for the CRUD operations on the to-do model.
     */
    it('This should retrieve 3 todo objects from the mock API service.', function () {
        spyOn(mockService, 'someAsyncCall').andCallThrough();
        //expect($scope.name).toEqual('World');
    });

});
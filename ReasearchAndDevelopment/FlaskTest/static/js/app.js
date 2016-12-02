var app = angular.module('collectorApp', [
  'angular-json-tree'
]);

app.factory("Data", function($http) {
  return {
    getSample: function(name) {
      console.log(name);
      return $http.get("http://127.0.0.1:5000/sample?name=" + name)
    }
  }
})


app.controller("MainCtrl", ['Data', '$scope', function(Data, $scope) {


  $scope.$watch('name', function(newValue, oldValue) {
    if(newValue != oldValue) {
      $scope.sample = Data.getSample($scope.name)
      console.log("Name Updated");
    }
  })
}])

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
  $scope.sample = {
    d: 1,
    c: 1,
    r: {
      j: 1,
      k: 'a'
    }
  }

  $scope.$watch('name', function(newValue, oldValue) {
    if(newValue != oldValue) {
      Data.getSample($scope.name).success(function(data) {
        console.log(data);
        $scope.sample = data
        console.log($scope.sample);
      }).error(function(er) {
        console.log(er);
      })


      //console.log($scope.sample);
      //console.log("Name Updated");
    }
  })
}])

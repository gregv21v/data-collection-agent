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
      Data.getSample($scope.name).success(function(data) {
        $scope.sample = JSON.stringify({"name":"TRAINIER SEEKS NEW CLIENTS. RUN FASTER, HIT HARDER, VELOCITY!!","has_image":true,"url":"http://boston.craigslist.org/gbs/act/5883300818.html","has_map":true,"price":null,"geotag":null,"where":null,"id":"5883300818","datetime":"2016-12-06 13:09"})
        console.log($scope.sample);
      }).error(function(er) {
        console.log(er);
      })


      //console.log($scope.sample);
      //console.log("Name Updated");
    }
  })
}])

var app = angular.module('collectorApp', [
  'angular-json-tree',
  'ngSanitize',
  'listGroup',
  'ui.bootstrap'
]);

app.factory("Data", function($http) {
  return {
    getSample: function(name) {
      return $http.get("http://127.0.0.1:5000/sample?name=" + name)
    },
    scheduleScrape: function(start, end) {
      return $http.get("http://127.0.0.1:5000/scheduleScrape?start=" + start + "&end=" + end)
    }
  }
})


app.controller("MainCtrl", ['Data', '$scope', function(Data, $scope) {
  $scope.sample = {}
  $scope.startTime = {minutes: 0, seconds: 0}
  $scope.endTime = {minutes: 0, seconds: 0}



  // a list of a all the scrapes that have
  // been scheduled
  $scope.scheduledScrapes = [
    {
      start: "12:30",
      end: "1:00"
    },
    {
      start: "6:30",
      end: "1:00"
    },
    {
      start: "1:30",
      end: "1:00"
    },
    {
      start: "3:30",
      end: "1:00"
    }
  ]

  // TODO: info at the top 
  $scope.sampleInfo = "Test"


  $scope.schedule = function() {
    console.log("Scheduling...");
    $scope.scheduledScrapes.push({
      start: $scope.startTime.minutes + ":" + $scope.startTime.seconds,
      end: $scope.endTime.minutes + ":" + $scope.endTime.seconds
    })
    console.log($scope.scheduledScrapes);
  }

  $scope.scheduleItemTpt = '<div>Start: {{item.start}} End: {{item.end}}</div>'


  $scope.$watch('name', function(newValue, oldValue) {
    if(newValue != oldValue) {
      if($scope.name == "craigslist") {
        $scope.sampleInfo = "Boston, Activities"
        $scope.$digest()
      }
      Data.getSample($scope.name).then(function(res) {
        $scope.sample = res.data
      })
    }
  })
}])

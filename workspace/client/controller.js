//Copyright (c) 2015 Victor Graf
//Author: Victor Graf
//Hillary's Emails Web Client

angular.module('app.hillary.emails', ['ngAnimate', 'ui.bootstrap']);
angular.module('app.hillary.emails').controller('EmailController', function ($scope, $window, $http) {
  
  var emails = [];
  var filterEmails = [];
  $scope.displayEmails = [];
  $scope.page = 1;
  $scope.pages = [];
  $scope.itemsPerPage = 25;
  $scope.cluster = '';
  
  $scope.images = {
		'0': ["/img/sad/0.jpg", "/img/sad/1.jpg", "/img/sad/2.jpg", "/img/sad/3.jpg", "/img/sad/4.jpg", "/img/sad/5.jpg", "/img/sad/6.jpg", "/img/sad/7.jpg", "/img/sad/8.jpg", "/img/sad/9.jpg"],
		'1': ["/img/happy/0.jpg", "/img/happy/1.jpg", "/img/happy/2.jpg", "/img/happy/3.jpg", "/img/happy/4.jpg", "/img/happy/5.jpg", "/img/happy/6.jpg", "/img/happy/7.jpg", "/img/happy/8.jpg", "/img/happy/9.jpg", "/img/happy/10.jpg" ]
	}

  $scope.selectCluster = function(cluster) {
      $scope.cluster = cluster;
	  if(cluster == '') filterEmails = emails;
	  else{
		filterEmails = [];
		for(var i=0; i<emails.length; i++){
			if(emails[i].cluster == cluster){
				filterEmails.push(emails[i]);
			}
		}
	  }
	  $scope.setPage(1);
  };
  
  $scope.setPage = function(pg) {
	$scope.page = pg;
	$scope.displayEmails = filterEmails.slice((pg-1)*$scope.itemsPerPage, pg*$scope.itemsPerPage);
	$scope.pages = [];
	for(var i=1; i<=Math.ceil(filterEmails.length/$scope.itemsPerPage); i++){
		$scope.pages.push(i);
	}
  }
  
  $scope.extractContent = function(email){
	if(email.ExtractedSubject == "") {
		if(email.RawText.indexOf("Subject:") <= -1){
			return email.RawText;
		}
		return email.RawText.split("Subject:").slice(1).join("");
	}
	return email.RawText.split(email.ExtractedSubject).slice(1).join("");
  }
  
  $scope.getImage = function(classification, index) {
	var arr = $scope.images[classification];
	return arr[index % arr.length];
  };
  
  $scope.getEmails = function() {
	$http({
	  method: 'GET',
	  url: '/emails'
	}).then(function successCallback(response) {
		emails = emails.concat(response.data.results);
		$scope.selectCluster('');
	  }, function errorCallback(response) {
		alert("Error getting emails");
	  });
  };
  
  $scope.getEmails();
});

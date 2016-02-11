'use strict';
var cuControllers = angular.module('cuControllers', [
    'cuLoginController'
]);


/*
 * Controller for tadding active class to the menu*/
cuControllers.controller('menuBar', ['$scope', '$location' , '$modal', '$cookies', 'Login', '$log', '$routeParams',
    function ($scope, $location, $modal, $cookies, Login, $log, $routeParams) {
        $scope.isActive = function (viewLocation) {
            if ($scope.active == viewLocation.split('/')[1]) {
                return true;
            }


        };
        $scope.modal = function () {
            $modal.open({
                templateUrl: '/static/partials/login.html',
                controller: 'LoginController',
                size: 'sm',
                backdrop: 'static'
            });

        };

        $scope.logout = function () {
            Login.logout($cookies.get('cloudUser')).then(function (value) {
                $scope.login_cookie = '';
                $cookies.remove('cloudAdminCookie');
                $cookies.remove('cloudUser');
                $cookies.put('cloudAdminCookie', '');
                $cookies.put('cloudUser', '');
                $scope.user = '';
                window.location.reload();
                $log.info('Logout Complete');
            }, function (reason) {

                $log.error('Reason for Failure ---', reason);
            }, function (update) {
                $log.info('Update  ---', update);
            });

        }

    }]);
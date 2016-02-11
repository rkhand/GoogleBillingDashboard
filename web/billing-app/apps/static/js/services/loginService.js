
'use strict';

/* Services */

var loginService = angular.module('loginService', []);

/* Login services*/

loginService.factory('Login', ['$http', '$timeout', '$q', '$log' , function ($http, $timeout, $q, $log) {

    var login = {
        time_stamp: Date.now(),
        submitForm: function (user) {
            var login_url = CU.login_url + '?time_stamp=',
                full_url,
                deferred = $q.defer();
            login_url += login.time_stamp;

            $log.info(login_url);
            $http.post(encodeURI(login_url), {'username': user.username, 'password': user.password}).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        logout: function (user) {
            var login_url = CU.logout_url + '?time_stamp=',
                full_url,
                deferred = $q.defer();
            login_url += login.time_stamp;

            $log.info(login_url);
            $http.post(encodeURI(login_url), {'username': user}).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        }
    };
    return login;

}]);
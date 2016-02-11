
'use strict';

/* Services */

var billingService = angular.module('billingService', []);
/* Usage Cost Services*/

billingService.factory('UsageCost', ['$http', '$timeout', '$q', '$log' , function ($http, $timeout, $q, $log) {
    var usages = {
        baseUrl: '',
        getProjectList: function () {
            var url = CU.billing_url + 'projects?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.get(url).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        getResourceList: function () {
            var url = CU.billing_url + 'resources?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.get(url).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        getUrl: function (year, month, costCenter, project, resource) {
            var url = CU.billing_url ,
                month_value, project_value, resource_value, cost_center_value;
            month_value = (month == 'all') ? '' : 'month=' + month + '&';
            project_value = (project == 'all') ? '' : '&project=' + project;
            resource_value = (resource == 'all') ? '' : '&resource=' + resource;
            cost_center_value = (costCenter == 'all') ? '' : '&cost_center=' + costCenter;
            url = url + year + '?' + month_value + cost_center_value + project_value + resource_value + '&time_stamp=' + Date.now();
            return url;
        },
        getData: function (year, month, costCenter, project, resource) {
            var billing_url = usages.getUrl(year, month, costCenter, project, resource),
                deferred = $q.defer();
            $log.info(billing_url);
            $http.get(encodeURI(billing_url)).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        getCostCenterList: function (unique) {
            var url = CU.billing_url + 'cost_center?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            if (unique) {
                url += '&unique=true';
            }
            $log.info(url);
            $http.get(encodeURI(url)).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        deleteProject: function (project) {
            var url = CU.billing_url + 'cost_center/delete?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.post(encodeURI(url), project).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        },
        addProject: function (project) {
            var url = CU.billing_url + 'cost_center?time_stamp=',
                deferred = $q.defer();
            url += Date.now();
            $log.info(url);
            $http.post(encodeURI(url), project).success(function (data) {
                deferred.resolve(data);
            }).error(function () {
                deferred.reject("error");
            });
            return deferred.promise;
        }
    };
    return usages;
}]);
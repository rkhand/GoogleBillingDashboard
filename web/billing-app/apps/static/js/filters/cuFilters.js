
'use strict';

/* Services */

var cuFilters = angular.module('cuFilters', []);

cuFilters.filter('bytes', [function () {
    return function (bytes, precision) {

        if (bytes === 0) {
            return '0';
        } else if (isNaN(bytes) || !isFinite(bytes)) {
            return '-';
        }
        var k = 1000;
        var dm = precision + 1 || 3;
        var sizes = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'];
        var i = Math.floor(Math.log(bytes) / Math.log(k));
        return (bytes / Math.pow(k, i)).toPrecision(dm) + ' ' + sizes[i];
    };

}]);


cuFilters.filter('split', function () {
    return function (input, splitChar, splitIndex) {
        // do some bounds checking here to ensure it has that index
        return input.split(splitChar)[splitIndex];
    }
});

'use strict';


var cuLoginController = angular.module('cuLoginController', []);

cuLoginController.controller('LoginController', ['$scope', '$log', '$sce', 'Login', '$modalInstance', '$rootScope', '$cookies',
    function ($scope, $log, $sce, Login, $modalInstance, $rootScope, $cookies) {

        /* loading img*/
        $scope.msg = false;
        $scope.displayForm = true;
        $scope.displayOk = false;
        $scope.ok = function () {

            /* Make a call to the git create project and then upon promise close the modal*/

            // check to make sure the form is completely valid
            if ($scope.userForm.$valid) {
                $scope.displayForm = false;
                $scope.msg = false;
                $scope.loading = true;
                $log.info($scope.user);
                Login.submitForm($scope.user).then(function (value) {
                    $scope.loading = false;
                    var msg = '';
                    $scope.msg = true;
                    // if cookie there then login success else mismatch
                    if (value['login_cookie']) {
                        $scope.class_name = 'blue';
                        msg = value['username'] + ' has successfully logged in !!';
                        $scope.message = $sce.trustAsHtml(msg);
                        $scope.displayOk = true;
                        $cookies.put('cloudAdminCookie', value['login_cookie']);
                        $cookies.put('cloudUser', value['username']);
                        $scope.login_cookie = value['login_cookie'];
                        $scope.user = value;
                        //code to call instance list load
                        $rootScope.$broadcast("getInstanceList");
                        $rootScope.$broadcast("getSSHList");
                        $rootScope.$broadcast("initVersions");

                    } else {
                        $scope.displayForm = true;
                        $scope.class_name = 'red';
                        if (value['login_error'] == 'Wrong Password') {
                            msg = 'There is a password mismatch. Try again !!';
                            $('form input[type=password]').focus();
                            $('form input[type=password]').val('');
                        } else {
                            msg = value['login_error'] + 'Try again !!';
                            $('form input[type=text]').focus();
                            $('form input[type=text]').val('');
                            $('form input[type=password]').val('');
                        }
                        $scope.message = $sce.trustAsHtml(msg);
                        $scope.login_cookie = '';
                        $scope.user = '';
                    }


                    $log.info('Login Complete');
                }, function (reason) {
                    var msg = (reason.data && reason.data.message) ? reason.data.message : CU.login_error_msg;
                    $scope.msg = true;
                    $scope.class_name = 'red';
                    $scope.loading = false;
                    $scope.displayOk = true;
                    $log.error('Reason for Failure ---', msg);
                    $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);
                }, function (update) {
                    $log.info('Update  ---', update);
                });

            } else {
                $log.info('CLICKED SUBMIT  -- FORM INCOMPLETE');
            }

        };
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };

    }]);

'use strict';

/* Controllers */

var cuBillingControllers = angular.module('cuBillingControllers', []);


/*
 * Controller for Biiling per Cost Center View page
 * */
cuBillingControllers.controller('CostCenterController', ['$scope', '$location' , '$cookies',
    'UsageCost', '$log', '$sce',
    function ($scope, $location, $cookies, UsageCost, $log, $sce) {
        var init = function () {
            $scope.costCenterList = [];
            $scope.fail = false;
            $scope.loading = true;
            $scope.totalCost = 0;
            $scope.getCostCenterList();
        };
        $scope.getCostCenterList = function () {
            var date = new Date();
            $scope.current_month = date.getMonth() + 1;
            //$scope.current_month = 9;

            $scope.current_year = date.getFullYear();
            UsageCost.getData($scope.current_year, $scope.current_month, 'all', 'all', 'all').then(function (value) {
                $scope.loading = false;
                $scope.costCenterList = value.usage_data;
                $scope.totalCost = 0;
                $.each(value.usage_data, function (k, v) {
                    $scope.totalCost += v.cost;
                });
                $log.info('Cost Center Data -- ', $scope.costCenterList);
            }, function (reason) {
                var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
                $log.error('Reason for Failure ---', msg);
                $scope.fail = true;
                $scope.class_name = 'red';
                $scope.loading = false;
                $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);

            }, function (update) {
                $log.info('Update  ---', update);
            });

        };

        $scope.centerURL = function (center) {
            var url = 'cost_center/#?year=' + $scope.current_year + '&month=all' + '&cost_center=' + center + '&project=all&resource=all';
            return url;
        };

        init();

    }]);


/*
 * controller for getting the usage nad billing data and display it as a chart
 * Dependencies -- $log, UsageServices
 * variables -- list for year, month, project and resource
 *
 * functions -- getYearList  --> liet of years
 *              getProjectList  --> list of projects -- name
 *              getResourceList  --> list of resources
 *              getURLparams --> to get the url params and set the filters and data accordingly
 *              updateURL -->     Called to update the url params based on the filter change and on initial page load
 *              filterChange --> based on the dropdwon change this will be called when updateURL is triggered
 *              getData  --> calls the Service to get the data from backend
 *              barChart  --> bar chart is displayed for cost
 *              multiChart --> cost nad usage
 *              monthName  --> for table get the
 *              projectURL -- create urls for the project
 *              export --> export toexcel
 *
 *
 * */
cuBillingControllers.controller('UsageController', ['$scope', '$log', '$sce', 'UsageCost', '$location',
    function ($scope, $log, $sce, UsageCost, $location) {
        $log.info(' ~~~~~~~~~~~~~UsageController Loaded ~~~~~~~~~~~~');
        $scope.init = function () {
            $scope.fail = false;
            $scope.totalCost = 0;

            /* get the year list and update the year dropdown*/
            var startYear = 2015,
                date = new Date();
            $scope.currentYear = date.getFullYear();
            $scope.monthList = [
                {'value': 'all', 'displayName': 'All'},
                {'value': '1', 'displayName': 'January'},
                {'value': '2', 'displayName': 'February'},
                {'value': '3', 'displayName': 'March'},
                {'value': '4', 'displayName': 'April'},
                {'value': '5', 'displayName': 'May'},
                {'value': '6', 'displayName': 'June'},
                {'value': '7', 'displayName': 'July'},
                {'value': '8', 'displayName': 'August'},
                {'value': '9', 'displayName': 'September'},
                {'value': '10', 'displayName': 'October'},
                {'value': '11', 'displayName': 'November'},
                {'value': '12', 'displayName': 'December'}
            ];
            $scope.yearList = [startYear];
            $scope.getYearList(startYear, $scope.currentYear);

            $scope.display_table = false;
            $('select').attr('disabled', true);
            $('#d3-container').html('<div class="text-center panel-body">' + CU.Loading + '</div>');

            $scope.getCostCenterList();


        };

        /*  Based on the url params call update params and call filterchange  function that calls to get the data
         * */
        var getURLParams = function () {
            $scope.urlParams = $location.search();
            if ($scope.urlParams['year']) {
                $.each($scope.urlParams, function (k, v) {
                    if (k == 'year') {
                        $scope.yearSelected = v;
                    } else if (k == 'month') {
                        $scope.monthSelected = v;
                    } else if (k == 'cost_center') {
                        $scope.costCenterSelected = v;
                    } else if (k == 'project') {
                        $scope.projectSelected = v;
                    } else if (k == 'resource') {
                        $scope.resourceSelected = v;
                    }
                });
                $scope.updateURL();

            } else {
                /* first time while coming form home page*/
                $scope.yearSelected = $scope.currentYear.toString();
                /* update the months dropdown*/
                $scope.monthSelected = 'all';
                $scope.costCenterSelected = 'all';
                $scope.projectSelected = 'all';
                $scope.resourceSelected = 'all';
                $scope.updateURL();
            }
            /* by default show data for current month and year*/
            $log.info('getURLParams -- after setting');
            $log.info($scope.currentYear, $scope.monthSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);
            $scope.filterChange($scope.yearSelected, $scope.monthSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);


        };
        /* Called to update the url params based on the filter change and on initial page load
         * need to look into this*/
        $scope.updateURL = function (apply, centerchange) {

            if (apply) {
                $scope.$apply(function () {
                    $location.search('year', $scope.yearSelected);
                    $location.search('month', $scope.monthSelected);
                    $location.search('cost_center', $scope.costCenterSelected);
                    $location.search('project', $scope.projectSelected);
                    $location.search('resource', $scope.resourceSelected);
                    $log.info('UPDATE URL');
                    $log.info($scope.currentYear, $scope.monthSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);

                });
            } else if (centerchange) {
                $location.search('year', $scope.yearSelected);
                $location.search('month', $scope.monthSelected);
                $location.search('cost_center', $scope.costCenterSelected);
                $scope.projectSelected = 'all';
                $scope.resourceSelected = 'all';
                $location.search('project', $scope.projectSelected);
                $location.search('resource', $scope.resourceSelected);
                $log.info('UPDATE URL');
                $log.info($scope.currentYear, $scope.monthSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);


            } else {
                $location.search('year', $scope.yearSelected);
                $location.search('month', $scope.monthSelected);
                $location.search('cost_center', $scope.costCenterSelected);
                $location.search('project', $scope.projectSelected);
                $location.search('resource', $scope.resourceSelected);
                $log.info('UPDATE URL');
                $log.info($scope.currentYear, $scope.monthSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);

            }


        };
        /* on location change call filter change with the updated params
         * */
        $scope.$on('$locationChangeSuccess', function (next, current) {
            $log.info('Location Change Called');
            var params = $location.search();
            if (params['year']) {
                $scope.yearSelected = params['year'];
                $scope.monthSelected = params['month'];
                $scope.costCenterSelected = params['cost_center'];
                $scope.projectSelected = params['project'];
                $scope.resourceSelected = params['resource'];
            }

            $scope.filterChange($scope.yearSelected, $scope.monthSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);

        });
        /**
         * Get CostCenterList
         */
        $scope.getCostCenterList = function () {
            var unique = true;
            UsageCost.getCostCenterList(unique).then(function (value) {

                /* populate the project list*/
                $scope.costCenterList = value.cost_center_list;
                $log.info('Cost Center List -- ', $scope.costCenterList);

                /* get the start values based on the url params*/
                getURLParams();

            }, function (reason) {
                var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
                $log.error('Reason for Failure ---', msg);
                $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);
            }, function (update) {
                $log.info('Update  ---', update);
            });


        };


        /* Create a year list with 2015 as the start and current year as the end*/
        $scope.getYearList = function (startYear, currentYear) {
            // create a list of years with 2015 as the start
            while (startYear != currentYear) {

                $scope.yearList.push(++startYear);
            }
            $log.debug('+++ YEAR LIST +++++++++ ', $scope.yearList);
        };

        /* API call function to get data
         * if resource is clicke do then display multichart else bar chart*/
        $scope.getData = function (yearSelected, monthSelected, costCenterSelected, projectSelected, resourceSelected) {
            $scope.fail = false;
            $('select').attr('disabled', true);
            //$('#container').html('<div class="text-center">' + CU.Loading + '</div>');

            $scope.totalCost = 0;
            $scope.costData = [];
            $scope.display_table = false;
            $('#d3-container').html('<div class="text-center panel-body">' + CU.Loading + '</div>');
            $('.nvtooltip').css('opacity', '0');


            UsageCost.getData(yearSelected, monthSelected, costCenterSelected, projectSelected, resourceSelected).then(function (value) {

                $('select').attr('disabled', false);

                /*if data is empty display message*/
                if (typeof(value.usage_data) != 'undefined' && value.usage_data.length > 0 && (value.usage ? value.usage.length > 0 : true)) {
                    $scope.display_table = true;

                    /* display the chart
                     * -- if resource is clicked then its day based*/
                    if (resourceSelected != 'all' && monthSelected != 'all') {
                        $scope.multid3(value.d3_json);
                        $scope.projectList = value.project_list;
                        $log.debug('PROJECT LIST --', $scope.projectList);
                        $scope.resourceList = value.resource_list;
                        $log.debug('Resource LIST --', $scope.resourceList);
                    }
                    else {
                        var data = value.usage_data;
                        $scope.projectList = [];
                        $scope.resourceList = [];
                        if ($scope.costCenterSelected != 'all') {

                            $scope.projectList = (value.project_list) ? value.project_list : [];
                            $log.debug('PROJECT LIST --', $scope.projectList);
                            $scope.resourceList = (value.resource_list) ? value.resource_list : [];
                            $log.debug('Resource LIST --', $scope.resourceList);
                        }
                        $scope.d3bar(value.usage_data);

                    }
                    $scope.costData = value.usage_data;

                    $.each(value.usage_data, function (k, v) {
                        $scope.totalCost += v.cost;
                    });

                    $scope.totalCost = parseFloat($scope.totalCost).toFixed(2);
                    $scope.fail = false;
                    $scope.monthName();

                } else {
                    $scope.fail = true;
                    $scope.loading = false;
                    $('#d3-container').html('');
                    $scope.class_name = 'blue';
                    $scope.message = $sce.trustAsHtml('No data available for the selected options.');
                    $('#container').html('');
                }

            }, function (reason) {
                $('select').attr('disabled', false);
                var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
                $log.error('Reason for Failure ---', msg);
                $scope.fail = true;
                $scope.class_name = 'red';
                $('#container').html('');
                $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);

            }, function (update) {
                $log.info('Update  ---', update);
            });

        };

        /* On year,month change
         * -- get the month,project and resource value
         * -- based on these make an api call to get  the data and display the chart*/

        $scope.filterChange = function (yearSelected, monthSelected, costCenterSelected, projectSelected, resourceSelected) {
            $log.info(' ++ FILTER CHANGE ++ ');
            $log.info(yearSelected, monthSelected, costCenterSelected, projectSelected, resourceSelected);

            $scope.getData(yearSelected, monthSelected, costCenterSelected, projectSelected, resourceSelected);

        };


        $scope.d3bar = function (data) {
            $('#d3-container').html('');
            var margin = {top: 20, right: 20, bottom: 30, left: 40}, width = 750 - margin.left - margin.right, height = 500 - margin.top - margin.bottom;

            var svg = d3.select("#d3-container").append("svg").attr('height', '600').style('height', '600px');

            var d3_data = [
                {
                    key: "Cumulative Return",
                    values: data
                }
            ];

            function Idlink(d) {
                if (d.indexOf('ID') != -1 || d.indexOf('hd') != -1) {
                    d3.selectAll(".nv-x .nv-axis .tick text").style('pointer-events', 'auto');
                    d3.selectAll(".nv-x .nv-axis .tick text").style('cursor', 'pointer');
                } else {
                    d3.selectAll(".nv-x .nv-axis .tick text").style('pointer-events', 'none');
                }
                return d;

            }

            nv.addGraph(function () {
                var chart = nv.models.discreteBarChart()
                    .x(function (d) {
                        return d.name
                    })
                    .y(function (d) {
                        return d.cost
                    })
                    .staggerLabels(true)
                    //.staggerLabels(historicalBarChart[0].values.length > 8)
                    .showValues(true)
                    .duration(250);


                chart.xAxis.tickFormat(function (d) {
                    return Idlink(d);
                });

                chart.rotateLabels(-45);
                chart.margin().bottom = 200;


                chart.yAxis.tickFormat(function (d) {
                    return d3.format("$,.2f")(d)
                });

                d3.select('#d3-container svg')
                    .datum(d3_data)
                    .call(chart);


                nv.utils.windowResize(chart.update);
                return chart;
            }, function () {
                d3.selectAll(".nv-bar").on('click',
                    function (e) {
                        /* make a call with this project id*/
                        var self = this;
                        var project_clicked = ($scope.monthSelected != 'all' && $scope.projectSelected =='all' && $scope.resourceSelected =='all' );
                        var resource_clicked = ($scope.monthSelected != 'all' && $scope.projectSelected !='all' && $scope.resourceSelected =='all' );
                        var month_clicked = ($scope.monthSelected == 'all');
                        /* month on the x-axis*/
                        if ($scope.costCenterSelected == 'all' && $scope.monthSelected != 'all') {
                            $scope.costCenterSelected = e.name;
                            $scope.projectSelected = 'all';
                            $scope.resourceSelected = 'all';
                            $log.debug('CENTER CLICKED');

                        } else if (month_clicked){
                            $.each($scope.monthList, function (k, valueOf) {
                                if (valueOf.displayName === e.name) {
                                    $scope.monthSelected = valueOf.value;
                                    return false;
                                }
                            });
                            $log.debug('MONTH CLICKED');
                        } else if ( project_clicked) {
                            $scope.projectSelected = e.name;
                            $log.debug('PROJECT CLICKED');


                        } else if (resource_clicked) {
                            $scope.resourceSelected = e.name;
                            $log.debug('RESOURCE CLICKED');

                        }

                        //$scope.getData($scope.yearSelected, $scope.monthSelected, $scope.projectSelected, $scope.resourceSelected);
                        $log.debug($scope.yearSelected, $scope.monthSelected, $scope.costCenterSelected, $scope.projectSelected, $scope.resourceSelected);
                        $scope.updateURL(true);

                    });
                d3.selectAll(".nv-bar").style('cursor', 'pointer');
                /*
                 id links
                 */
                var project = false;
                d3.selectAll('.nv-x .nv-axis .tick text').on('click', function (e) {
                    var name, url, win;
                    if (e.indexOf('ID') != -1) {
                        name = e.split('-')[1];
                    } else {
                        name = e;
                    }
                    url = 'https://console.developers.google.com/project/' + name;
                    win = window.open(url, '_blank');
                    win.focus();
                }).on("mouseover", function () {
                    d3.select(this).style("fill", "blue");
                    d3.select(this).style("text-decoration", "underline");
                }).on("mouseout", function () {
                    d3.select(this).style("fill", "black");
                    d3.select(this).style("text-decoration", "none");
                });


            });

        };
        $scope.multid3 = function (data) {
            $('#d3-container').html('');
            var testdata = data.map(function (series) {
                series.values = series.values.map(function (d) {
                    return {x: d[0], y: d[1] }
                });
                return series;
            });
            var margin = {top: 20, right: 20, bottom: 30, left: 40}, width = 750 - margin.left - margin.right, height = 500 - margin.top - margin.bottom;

            var svg = d3.select("#d3-container").append("svg").attr('height', '600').style('height', '600px');
            var chart;
            nv.addGraph(function () {
                chart = nv.models.linePlusBarChart()
                    .margin({top: 50, right: 60, bottom: 30, left: 70})
                    .legendRightAxisHint(' [Using Right Axis]')
                    .color(d3.scale.category10().range())
                    .options({focusEnable: false});


                chart.y1Axis.tickFormat(function (d) {
                    return d3.format("$,.2f")(d)
                });
                chart.y2Axis
                    .tickFormat(function (d) {

                        return $scope.format(d);
                    });


                chart.bars.forceY([0]).padData(false);

                /* chart.x2Axis.tickFormat(function (d) {
                 return d3.time.format('%x')(new Date(d))
                 }).showMaxMin(false);*/

                d3.select('#d3-container svg')
                    .datum(testdata)
                    .transition().duration(500).call(chart);

                nv.utils.windowResize(chart.update);

                return chart;
            });


        };
        $scope.format = function (d) {
            var isNeg = d < 0;
            if (d == 0) return '0';
            if (isNeg) {
                d = -d;
            }
            var k = 1000;
            var dm = 3;
            var sizes = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'];
            var i = Math.floor(Math.log(d) / Math.log(k));
            if (i < 0) {
                return d;
            }
            if (isNeg) {
                return -(d / Math.pow(k, i)).toPrecision(dm) + ' ' + sizes[i];
            } else {
                return (d / Math.pow(k, i)).toPrecision(dm) + ' ' + sizes[i];
            }
        };

        $scope.usage_display = function () {
            return ($scope.monthSelected != 'all' && $scope.resourceSelected != 'all');
        };

        $scope.export = function () {
            var json = $scope.costData;
            var csv = $scope.JSON2CSV(json);

            var file_name = $scope.costCenterSelected + '_' + $scope.yearSelected + '_' + $scope.monthSelectedName + '.csv';
            //window.open("data:text/csv;charset=utf-8;filename=filename.csv," + escape(csv))
            $('a#export').attr('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
            $('a#export').attr('download', file_name);
        };
        $scope.JSON2CSV = function (objArray) {
            var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;

            var str = '';
            var line = '';
            // get the header info, we need only month,cost,usage and not the angular stuff
            for (var index in array[0]) {
                if (index == 'name' || index == 'cost' || index == 'usage') {
                    var header = (index == 'name') ? 'TYPE' : index.toUpperCase();
                    line += header + ',';
                }
            }
            line = line.slice(0, -1);
            str += line + '\r\n';


            for (var i = 0; i < array.length; i++) {
                var line = '';

                for (var index in array[i]) {
                    if (index == 'name' || index == 'cost' || index == 'usage') {
                        var data = (index == 'cost') ? ('$ ' + array[i][index]) :
                            (index == 'usage') ? (  $scope.format(array[i][index]) +' ' + array[i]['unit']) :
                                array[i][index];
                        line += data + ',';
                    }
                }


                line = line.slice(0, -1);
                str += line + '\r\n';
            }
            return str;


        };
        $scope.monthName = function () {
            $.each($scope.monthList, function (k, valueOf) {
                if (valueOf.value === $scope.monthSelected) {
                    $scope.monthSelectedName = valueOf.displayName;
                    return false;
                }
            });
        };


        /* init
         -- for setting all models
         -- get the data for current year and month -- yearChange*/
        $scope.init();
    }]);


/*
 * Controller for Cost Center View page*/
cuBillingControllers.controller('ProjectsController', ['$scope', '$location' , '$modal', '$cookies',
    'UsageCost', '$log', '$sce',
    function ($scope, $location, $modal, $cookies, UsageCost, $log, $sce) {
        var init = function () {

            $scope.getCostCenterList();
            $scope.projectList = [];
            $scope.message = false;
            $scope.add = false;
            $scope.project_id = '';
            $scope.project_name = '';
            $scope.cost_center = '';
            $scope.director = '';

        };
        $scope.getCostCenterList = function () {
            UsageCost.getCostCenterList().then(function (value) {

                $log.info(value);
                $scope.projectList = value.cost_center_list;
            }, function (reason) {
                var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
                $log.error('Reason for Failure ---', msg);
                $scope.fail = true;
                $scope.class_name = 'red';
                $('#container').html('');
                $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);

            }, function (update) {
                $log.info('Update  ---', update);
            });

        };

        $scope.addOne = function (project) {
            $scope.add = true;


            if (project) {
                $scope.projectInfo = angular.copy(project);
                $scope.projectInfo.project_id = ($scope.projectInfo.project_id).indexOf('ID') == 0 ? $scope.projectInfo.project_id.split('-')[1] : $scope.projectInfo.project_id;


            } else {
                $scope.projectInfo = {'project_id': '', 'project_name': '', 'director': '', 'cost_center': ''};

            }

            $log.info($scope.projectInfo);

            $log.debug(project);
            $('html, body').animate({
                scrollTop: 0
            }, 800);

        };
        $scope.close_add = function () {
            $scope.add = false;
            $scope.loading = false;
            $log.debug('Close --', $scope.projectInfo);

            $scope.projectInfo = {'project_id': '', 'project_name': '', 'director': '', 'cost_center': ''};
        };
        $scope.add_save = function () {
            $log.info($scope.projectInfo);
            if ($scope.projectInfo.project_id != 'Not Available') {
                $scope.projectInfo.project_id = 'ID-' + $scope.projectInfo.project_id;
            }
            var project = {'projects': [$scope.projectInfo]};
            var id = $scope.projectInfo.project_name;

            var container = $('table thead'),
                element = $("tr#" + id + "");
            $scope.loading = true;

            UsageCost.addProject(project).then(function (value) {

                $log.info(value);
                $scope.getCostCenterList();
                $scope.close_add();
                $('html, body').animate({
                    scrollTop: element.offset().top - container.offset().top + container.scrollTop()
                });
                element.addClass

            }, function (reason) {
                var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
                $log.error('Reason for Failure ---', msg);
                $scope.fail = true;
                $scope.class_name = 'red';
                $('#container').html('');
                $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);
                $scope.close_add();
            }, function (update) {
                $log.info('Update  ---', update);
            });

        };
        $scope.clear = function () {
            $scope.message = false;
        };

        $scope.delete = function (project) {
            $scope.showModal('delete', project);
        };
        $scope.showModal = function (type, project) {

            $modal.open({
                templateUrl: '/static/partials/billing/projectInfo.html',
                controller: 'ProjectInfoController',
                size: 'lg',
                backdrop: 'static',
                resolve: {
                    project: function () {
                        return project;
                    },
                    type: function () {
                        return type;
                    }

                }});

        };

        $scope.$on("getCostCenterList", function (event, args) {

            $scope.getCostCenterList();

        });
        init();

    }]);


/**
 * Project Delete  Modal Controller
 */
cuBillingControllers.controller('ProjectInfoController', ['$scope', '$modalInstance' , 'project', '$log', 'type', '$rootScope',
    'UsageCost', '$sce',
    function ($scope, $modalInstance, project, $log, type, $rootScope, UsageCost, $sce) {
        $scope.fail = false;
        $scope.project = project;
        $scope.type = type;


        $scope.close = function () {
            $modalInstance.dismiss('cancel');

        };
        $scope.delete = function () {
            var project = {'projects': [$scope.project.project_id]};
            $scope.loading = true;

            UsageCost.deleteProject(project).then(function (value) {
                $log.info(value);
                $scope.loading = false;
                $modalInstance.dismiss('cancel');
                $rootScope.$broadcast('getCostCenterList');
            }, function (reason) {
                var msg = (reason.data && reason.data.message) ? reason.data.message : CU.usage_error_msg;
                $log.error('Reason for Failure ---', msg);
                $scope.fail = true;
                $scope.loading = false;
                $scope.class_name = 'red';
                $('#container').html('');
                $scope.message = $sce.trustAsHtml('Reason for Failure ---' + msg);
                $rootScope.$broadcast('getCostCenterList', {'message': $scope.message});

            }, function (update) {
                $log.info('Update  ---', update);
            });

        };

    }]);



__author__    =	"Ashwini Chandrasekar(@sriniash)"
__email__     =	"ASHWINI_CHANDRASEKAR@homedepot.com"
__version__   =	"1.0"
__doc__       = "Billing View API/HTML layer"

from flask import Blueprint, request
from flask.templating import render_template
from flask.wrappers import Response

import json
from apps.billing.billingData import get_project_list_data, get_center_list, get_costs_per_month, \
    get_costs_per_cost_month, get_costs_per_center_year, get_costs_per_center_month, get_costs_per_resource_month_center, \
    get_costs_per_project_year, get_costs_per_resource, get_costs_per_resource_per_project, \
    get_costs_per_resource_per_project_per_day, get_costs_per_resource_all_project_per_day,log,table_create,get_project_by_id, update_project_data, \
    create_project_data, delete_project_by_id

from apps.config.apps_config import log_output

mod = Blueprint('billing', __name__, url_prefix='/billing')


'''
    BILLING PAGE LANDING PAGE , COST CENTER PAGE AND API's
'''
# route handles for /admin and /admin/page
@mod.route('/')
def billing():
    url = 'billing/index.html'
    return render_template(url, title="Cloud Admin Tool")


# route handles for /admin and /admin/page
@mod.route('/cost_center/')
def cost_center_data():
    url = 'billing/cost_center_data.html'
    return render_template(url, title="Cloud Admin Tool")


# route handles for /admin and /admin/page
@mod.route('/projects')
def projects_cost_center():
    url = 'billing/projects.html'
    return render_template(url, title="Cloud Admin Tool")


# route handles for creating table for first time
@mod.route('/table')
def table():
    response = table_create()
    resp = Response(response=json.dumps(response),
                    status=200,
                    mimetype="application/json")

    return resp




'''

    API to get the list of distinct projects

'''


@mod.route('/usage/projects', methods=['GET'])
def get_project_list():
    project_list_data = get_project_list_data()
    data = {
        'project_list': project_list_data
    }
    resp = Response(response=json.dumps(data),
                    status=200,
                    mimetype="application/json")
    return resp


'''
    API that acts as a router to all the other calls based on the filter values year, month, project and resource
    Main entry point
    inputs : Year in the url
    params: month,cost_center,project,resource
    output : JSON with usage_data for all calls, project_list and resource_list in calls that need them

    /billing/usage/2015
        --> get_costs_per_month(year)
    /billing/usage/2015?month=11
        --> get_costs_per_cost_month(year, monthselected)
    /billing/usage/2015?month=11&&cost_center=<center-name>
        -->  get_costs_per_center_month(year, monthselected, costcenterselected)
    /billing/usage/2015?&cost_center=<center-name>
        --> get_costs_per_center_year(year, costcenterselected)
    /billing/usage/2015?month=11&cost_center=<center-name>&project=<project-name>
        --> get_costs_per_resource_month_center(year, monthselected, costcenterselected, projectselected)
    /billing/usage/2015?&cost_center=<center-name>&project=<project-name>
        --> get_costs_per_project_year(year, costcenterselected, projectselected)
    /billing/usage/2015?month=11&&cost_center=<center-name>&project=<project-name>&resource=<resource-name>
        -->  get_costs_per_resource_per_project_per_day(year, monthselected, costcenterselected, projectselected, resourceselected)


'''


@mod.route('/usage/<int:year>', methods=['GET'])
def get_costs(year):
    log_output('-----------In get_costs-----------------------')
    log_output(year)
    project_list_local = {}

    cost_center_list = get_center_list(False)

    log_output('COST CENTER LIST ---')
    log_output(cost_center_list)

    for project_info in cost_center_list:
        project_list_local[project_info['project_id']] = project_info['project_name']

    log_output('Project_list_local')
    log_output(project_list_local)

    monthselected = request.args.get('month')
    projectselected = request.args.get('project')
    resourceselected = request.args.get('resource')
    costcenterselected = request.args.get('cost_center')

    data = dict(usage_data=[])

    log.info('get_costs called')
    log.info('yearSelected {0}'.format(year))
    log.info('monthSelected {0}'.format(monthselected))
    log.info('projectSelected {0}'.format(projectselected))
    log.info('resourceSelected {0}'.format(resourceselected))
    log.info('costcenterselected {0}'.format(costcenterselected))

    for project in project_list_local:
        if project_list_local[project] == projectselected:
            projectselected = project
    try:
        if monthselected is None and costcenterselected is None and projectselected is None and resourceselected is None:
            log.info('per year --> get_costs_per_month  called')
            data = get_costs_per_month(year)

        elif monthselected is not None and costcenterselected is None and projectselected is None and resourceselected is None:
            log.info('per month --> get_costs_per_cost_month called')
            data = get_costs_per_cost_month(year, monthselected)

        elif monthselected is None and costcenterselected is not None and projectselected is None and resourceselected is None:
            log.info('per year per cost --> get_costs_per_center_year called')
            data = get_costs_per_center_year(year, costcenterselected)

        elif monthselected is not None and costcenterselected is not None and projectselected is None and resourceselected is None:
            log.info('per month --> get_costs_per_center_month called')
            data = get_costs_per_center_month(year, monthselected, costcenterselected)

        elif monthselected is not None and costcenterselected is not None and projectselected is not None and resourceselected is None:
            log.info('per month per per center per project--resource --> get_costs_per_resource_month_center called ')
            data = get_costs_per_resource_month_center(year, monthselected, costcenterselected, projectselected)

        elif monthselected is None and projectselected is not None and resourceselected is None:
            log.info('per month per project --> get_costs_per_project_year called')
            data = get_costs_per_project_year(year, costcenterselected, projectselected)

        elif monthselected is None and projectselected is None and resourceselected is not None:
            log.info('per month all project -- resource --> get_costs_per_resource ')
            data = get_costs_per_resource(year, costcenterselected, resourceselected)

        elif monthselected is None and projectselected is not None and resourceselected is not None:
            log.info('per month one project -- resource  --> get_costs_per_resource_per_project called')
            data = get_costs_per_resource_per_project(year, costcenterselected, projectselected, resourceselected)

        elif monthselected is not None and projectselected is not None and resourceselected is not None:
            log.info('a month one project -- resource  --> get_costs_per_resource_per_project_per_day')
            data = get_costs_per_resource_per_project_per_day(year, monthselected, costcenterselected, projectselected,
                                                              resourceselected)

        elif monthselected is not None and projectselected is None and resourceselected is not None:
            log.info('a month all project -- resource  --> get_costs_per_resource_all_project_per_day')
            data = get_costs_per_resource_all_project_per_day(year, monthselected, costcenterselected, resourceselected)

        else:
            log.info('Outside all conditions')
            log.info('yearSelected {0}'.format(year))
            log.info('monthSelected {0}'.format(monthselected))
            log.info('projectSelected {0}'.format(projectselected))
            log.info('resourceSelected {0}'.format(resourceselected))
            log.info('costcenterselected {0}'.format(costcenterselected))

        resp = Response(response=json.dumps(data),
                        status=200,
                        mimetype="application/json")

    except Exception as e:
        log_output(e)
        data = dict()
        data['message'] = e[0]
        resp = Response(response=json.dumps(data),
                        status=500,
                        mimetype="application/json")

    return resp



'''
            PROJECT INFO CREATION PAGE AND API's
'''

'''
    API for the adding project into cost_center or getting Cost Center Data

    GET -- /usage/cost_center?unique=true --> for array of unique cost_center names
    GET -- /usage/cost_center--> list of dict of projects details

    POST -- /usage/cost_center-->
           I/P:
                json:
                {
                    "projects" :[
                    {"project_id":"ID-12345","project_name":"lab","cost_center":"Aurora","director":""},
                    {"project_id":"ID-123456","project_name":"demo","cost_center":"Aurora","director":""},
                    {"project_id":"ID-1234567","project_name":"dev","cost_center":"Aurora","director":""},
                    {"project_id":"ID-12345678","project_name":"prod","cost_center":"Aurora","director":""}
                    ]

                }
            O/P:
                 {
                    'message': ' cost_center_list Created/Updated'
                 }



'''


@mod.route('/usage/cost_center', methods=['POST', 'GET'])
def get_cost_center_list():
    cost_center_list = []

    if request.method == 'GET':
        unique = request.args.get('unique', False)

        try:
            if unique:
                cost_center_list = get_center_list(unique)
            else:
                cost_center_list = get_center_list(False)

            status = 200
            response = {
                'cost_center_list': cost_center_list
            }

        except Exception as e:
            log.error('Error in getting  group List -- {0}'.format(e))
            status = 500
            response = {
                'message': str(e)
            }

    else:
        try:
            projects = request.json['projects']

            for project in projects:
                project_id = project['project_id']
                project_name = project['project_name'].lower()
                cost_center = project['cost_center'].lower()
                director = project['director'].lower()

                if not director.strip():
                    director = 'None'

                '''
                    Check if project already in the table
                '''
                query_data = get_project_by_id(project_id)

                if len(query_data) > 0:
                    log_output('DATA IN TABLE - SO UPDATE')
                    query_data = update_project_data(cost_center, project_id, project_name, director)

                else:
                    log_output('DATA NOT IN TABLE - SO INSERT')
                    query_data = create_project_data(cost_center, project_id, project_name, director)

            status = 200
            response = {
                'message': ' cost_center_list Created/Updated'
            }
        except Exception as e:
            log.error('Error in creating  group List -- {0}'.format(e))
            status = 500
            response = {
                'message': str(e),
                'cost_center_list': cost_center_list
            }

    resp = Response(response=json.dumps(response),
                    status=status,
                    mimetype="application/json")

    return resp



'''
    API for the deleting project into cost_center
    POST -- /usage/cost_center/delete -->
           I/P:
                json:
              {
                "projects" :["ID-12345","ID-123456","ID-1234567"]

                }
            O/P:
                 {
                    'message': ' Projects Deleted'
                 }



'''


@mod.route('/usage/cost_center/delete', methods=['POST'])
def delete_cost_center_project():
    cost_center_list = []
    try:
        projects = request.json['projects']

        for project_id in projects:
            query = delete_project_by_id(project_id)

        status = 200
        response = {
            'message': ' cost_center_list Deleted'
        }
    except Exception as e:
        log.error('Error in creating  group List -- {0}'.format(e))
        status = 500
        response = {
            'message': str(e),
            'cost_center_list': cost_center_list
        }

    resp = Response(response=json.dumps(response),
                    status=status,
                    mimetype="application/json")

    return resp

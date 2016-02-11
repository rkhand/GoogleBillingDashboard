

__author__    =	"Ashwini Chandrasekar(@sriniash)"
__email__     =	"ASHWINI_CHANDRASEKAR@homedepot.com"
__version__   =	"1.0"
__doc__       = "Data Layer that is used by view and this makes call to the billingDBQuery"


import calendar
import json
from httplib2 import Http
from apps.config.apps_config import log_error, log_output, log

from apps.billing.models import get_distinct_projects, get_resource_list_per_project, get_billing_data_per_year, \
    get_billing_data_per_year_per_month, get_billing_data_per_year_per_center, get_billing_data_per_project_year, \
    get_billing_data_per_resource_month_center, get_billing_data_per_resource, get_billing_data_per_resource_per_project, \
    get_billing_data_per_resource_per_project_per_month, get_billing_data_per_resource_all_project_per_day, \
    get_cost_centers,create_table, get_project, update_project, create_project, delete_project,AlchemyEncoder



'''
 Utility to get the access token
'''


def get_access_token():
    token_data = dict()

    token_uri = 'http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token'
    http = Http()
    # Request an access token from the metadata server.
    resp_access, content_access = http.request(token_uri, method='GET', body=None,
                                               headers={'Metadata-Flavor': 'Google'})

    token_data['resp_access'] = resp_access
    token_data['content_access'] = content_access

    return token_data


'''
 utility to get project data
 params -- project_id
        -- access_token
'''


def get_project_data(project_id, access_token):
    project_data = dict()
    http = Http()
    project_url = 'https://www.googleapis.com/compute/v1/projects/' + project_id
    # log.debug('Project_URL : {0}'.format(project_url))
    resp, content = http.request(project_url, \
                                 body=None, \
                                 headers={'Authorization': 'Bearer ' + access_token})

    project_data['resp'] = resp
    project_data['content'] = content
    return project_data


'''
    get the list of projects
'''

def get_project_list_data():
    log.info('In Project List Data ----')
    data = dict()
    project_list = dict()
    try:
        projects = get_distinct_projects()

        for (project) in projects:
            project_list[project[0]] = project[0]

        log_output('PROJECT LIST')
        log_output(project_list)
        for (project) in project_list:
            log.info('INSIDE LOOP')
            # Request an access token from the metadata server.
            token_data = get_access_token()
            resp_access = token_data['resp_access']
            content_access = token_data['content_access']

            if resp_access.status == 200:

                # Extract the access token from the response.
                d = json.loads(content_access)
                access_token = d['access_token']  # Save the access token
                # log.debug('access_token -- {0}'.format(access_token))
                # Construct the request to Google Cloud Storage
                if project != 'Not Available':
                    project_id = project.split('-')[1]
                else:
                    project_id = 'Not Available'

                project_data = get_project_data(project_id, access_token)
                resp = project_data['resp']
                content = project_data['content']
                if resp.status == 200:
                    # log.debug('Project_data {0} -- {1}'.format(project_id, content))
                    data = json.loads(content)
                    project_list[project] = data['name']
                else:
                    log.error('Project_data  Error {0} -- {1}'.format(project_id, resp.status))


            else:
                log.error('Access Token Error {0}'.format(resp_access.status))

    except Exception as e:
        log_error(e)

    return project_list




'''
 Get project list based on the center
 input -- center
 output --> dict with lists array and id string

'''


def project_list_per_center(center):
    log.info(' IN PROJECT LIST PER CENTER __ {0}'.format(center))
    cost_center_list = get_center_list(False)

    log.info('COST_CENTER_LIST == {0}'.format(cost_center_list))

    project_list_center = ''
    project_list_center_arr = []
    project_list_center_arr_id = []
    project_center_all_list = []

    for project in cost_center_list:
        project_center_all_list.append(project['project_id'])
        if project['cost_center'] == center:
            project_list_center += ",'" + project['project_id'] + "'"
            if center.lower() == 'other' and project['project_name'] == project['project_id']:
                project_list_center_arr.append(project['project_id'])
            else:
                project_list_center_arr.append(project['project_name'])

            project_list_center_arr_id.append(project['project_id'])

    log_output('Cost Center List')
    log_output(project_list_center_arr)
    project_list_local = project_list_center_arr

    log_output('local list project')
    log_output(project_list_local)

    return {'list': project_list_local, 'ids': project_list_center_arr_id}


'''
  get resource list based on project id

  if project_name is used the n get the id from the cost center else id will be sent
'''


def resource_list_per_project(center, project):
    resource_list = []
    project_list_local = {}

    log.info('IN RESOURCE_LIST_PER_PROJECT -- {0} -- {1}'.format(center,project))

    cost_center_list = get_center_list(False)
    log.info('COST_CENTER_LIST == {0}'.format(cost_center_list))

    for project_info in cost_center_list:
        project_list_local[project_info['project_id']] = project_info['project_name']

    if project is not None:

        for project_id in project_list_local:
            if project_list_local[project_id] == project:
                project = str(project_id)

        query_data = get_resource_list_per_project([project])
        log_output(query_data)
    else:
        project_ids = project_list_per_center(center)['ids']
        query_data = get_resource_list_per_project(project_ids)
        log_output(query_data)

    log_output('In resource List')
    log_output(query_data)

    for (resource) in query_data:
        resource_list.append(resource[0])

    log_output('local list resource')
    log_output(resource_list)

    return resource_list


'''
  utility to get month based data
'''

def get_per_month_cost(query_data):

     log.info('get_per_month_cost == {0}'.format(query_data))

     per_month_data =  [{'cost': float(0), 'name': 'January','month':'1'},
            {'cost': float(0), 'name': 'February','month':'2'},
            {'cost': float(0), 'name': 'March','month':'3'},
            {'cost': float(0), 'name': 'April','month':'4'},
            {'cost': float(0), 'name': 'May','month':'5'},
            {'cost': float(0), 'name': 'June','month':'6'},
            {'cost': float(0), 'name': 'July','month':'7'},
            {'cost': float(0), 'name': 'August','month':'8'},
            {'cost': float(0), 'name': 'September','month':'9'},
            {'cost': float(0), 'name': 'October','month':'10'},
            {'cost': float(0), 'name': 'November','month':'11'},
            {'cost': float(0), 'name': 'December','month':'12'}]

     for (month, cost) in query_data:
        for val in per_month_data:
            if val['month'] == str(month):
                val['cost'] = float(cost)

     log.info('per_month_data == {0}'.format(per_month_data))

     return per_month_data

'''
  For getting costs of projects per month

'''


def get_costs_per_month(year):
    data = {}
    log.info(' In get_costs_per_month == {0}'.format(year))
    try:

        query_data = get_billing_data_per_year(str(year))
        log_output(query_data)

        usage_data = get_per_month_cost(query_data)

        log.info(' get_costs_per_month  DATA == {0}'.format(usage_data))
        data = {
            'usage_data': usage_data
        }
    except Exception as e:
        log_error(e)
    return data


'''
     for getting aggregated cost of each project for that month
'''


def get_costs_per_cost_month(year, month):
    log.info('get_costs_per_cost_month == {0}--{1}'.format(year,month))
    month_json = {}

    cost_center_list = get_center_list(False)
    log.info('COST_CENTER_LIST == {0}'.format(cost_center_list))

    log_output('In cost per month for a year')
    log_output(year)
    log_output(month)

    try:
        month_data = []
        query_data = get_billing_data_per_year_per_month(str(year), str(month))
        log_output(query_data)

        new_dict = dict()
        projects_list = []

        if query_data is not None:
            for project_info in cost_center_list:
                projects_list.append(str(project_info['project_id']))

            log.info('Project_Cost_center_list_global {0}'.format(cost_center_list))
            log.info('Project_Cost_center_list {0}'.format(projects_list))

            for (project, cost) in query_data:
                for project_info in cost_center_list:
                    cost_center = str(project_info['cost_center'])
                    project_id = str(project_info['project_id'])

                    if project == project_id:
                        new_dict[cost_center] = new_dict.get(cost_center, {})
                        new_dict[cost_center]['cost'] = new_dict[cost_center].get('cost', 0.0)
                        new_dict[cost_center]['project'] = new_dict[cost_center].get('project', [])
                        new_dict[cost_center]['project'].append(str(project))
                        new_dict[cost_center]['cost'] += cost

            log.info('new_dic --1 {0}'.format(new_dict))

            for key, value in new_dict.items():
                each_month = dict(name=key, cost=value['cost'])
                month_data.append(each_month)

            log.info('MONTH_DATA {0}'.format(month_data))

        month_json = {
            'usage_data': month_data
        }

    except Exception as e:

        log_error(e)
    return month_json


'''
     for getting aggregated cost of each cost center  for that year
'''


def get_costs_per_center_year(year, center):
    data = {}
    log.info('get_costs_per_CENTER_YEAR_month == {0} --{1}'.format(year,center))
    log_output(year)
    log_output(center)
    try:
        project_list_local = project_list_per_center(center)['list']
        project_ids = project_list_per_center(center)['ids']

        log_output('Project_list_local')
        log_output(project_list_local)

        query_data = get_billing_data_per_year_per_center(str(year), project_ids)
        log_output(query_data)

        log.info('get_billing_data_per_year_per_center == {0}'.format(query_data))
        usage_data = get_per_month_cost(query_data)

        data = {
            'usage_data': usage_data,
            'project_list': project_list_local
        }
    except Exception as e:
        log_error(e)
        log.info(e)
    return data


'''
     for getting aggregated cost of each cost center  for that month
'''


def get_costs_per_center_month(year, month, center):
    center_json = {}
    cost_center_list = get_center_list(False)
    try:

        cost_center_projects_id = []
        cost_center_projects_name = []
        cost_center_projects_all_id = []
        cost_center_projects_all_name = []

        for project_info in cost_center_list:
            cost_center_projects_all_id.append(project_info['project_id'])
            cost_center_projects_all_name.append(project_info['project_name'])
            if project_info['cost_center'] == center:
                cost_center_projects_id.append(project_info['project_id'])
                cost_center_projects_name.append(project_info['project_name'])


        month_data = []

        query_data = get_billing_data_per_year_per_month(str(year), str(month))
        log_output(query_data)

        for (project, cost) in query_data:
            if project in cost_center_projects_id:
                if cost_center_projects_name[cost_center_projects_id.index(project)].lower() == 'none':
                    name = project
                else:
                    name = cost_center_projects_name[cost_center_projects_id.index(project)]
                each_month = {'name': name,
                              'cost': float(cost)}
                month_data.append(each_month)

        project_list_local = project_list_per_center(center)['list']

        log.info('MonthData {0}'.format(month_data))
        log.info('Project List {0}'.format(project_list_local))

        center_json = {
            'usage_data': month_data,
            'project_list': project_list_local

        }
    except Exception as e:
        log_error(e)
    return center_json


'''
    for getting aggregated cost of each project for each month
'''


def get_costs_per_project_year(year, center, project):
    month_json = {}

    project_list_local = project_list_per_center(center)['list']

    try:

        month_data = []
        query_data = get_billing_data_per_project_year(str(year), str(project))
        log_output(query_data)

        for (project, cost) in query_data:
            each_month = {'name': project, 'cost': float(cost)}
            month_data.append(each_month)
        month_json = {
            'usage_data': month_data,
            'project_list': project_list_local
        }
    except Exception as e:
        log_error(e)
    return month_json


'''
    API for getting aggregated cost of each resource for a project for that month
'''


def get_costs_per_resource_month_center(year, month, center, project):
    project_json = {}

    try:
        project_data = []
        resource_list = []
        query_data = get_billing_data_per_resource_month_center(str(year), str(month), str(project))
        log_output(query_data)

        for (resource, cost) in query_data:
            each_project = {'name': resource, 'cost': float(cost)}
            resource_list.append(resource)
            project_data.append(each_project)

        resource_list_local = resource_list_per_project(center, project)

        project_list_local = project_list_per_center(center)['list']

        project_json = {
            'usage_data': project_data,
            'resource_list': resource_list_local,
            'project_list': project_list_local
        }
    except Exception as e:
        log_error(e)
    return project_json


'''
    API for getting  cost of a resource all months

'''


def get_costs_per_resource(year, center, resource):
    resource_json = {}

    project_list_local = project_list_per_center(center)['list']
    project_ids = project_list_per_center(center)['ids']
    resource_list_local = resource_list_per_project(center, None)

    try:
        query_data = get_billing_data_per_resource(str(year), project_ids, str(resource))
        log_output(query_data)

        usage_data = get_per_month_cost(query_data)

        resource_json = {
            'usage_data': usage_data,
            'project_list': project_list_local,
            'resource_list': resource_list_local
        }
        log_output('JSON')
        log_output(resource_json)
    except Exception as e:
        log_error(e)
    return resource_json


'''
    API for getting  cost of a resource for a project for all months
'''


def get_costs_per_resource_per_project(year, center, project, resource):
    resource_json = {}

    project_list_local = project_list_per_center(center)['list']
    resource_list_local = resource_list_per_project(center, project)

    try:
        query_data = get_billing_data_per_resource_per_project(str(year), str(project), str(resource))
        log_output(query_data)

        usage_data = get_per_month_cost(query_data)
        resource_json = {
            'usage_data': usage_data,
            'project_list': project_list_local,
            'resource_list': resource_list_local

        }
    except Exception as e:
        log_error(e)
    return resource_json


'''
    API for getting  cost of a resource for a project for a month
'''


def get_costs_per_resource_per_project_per_day(year, month, center, project, resource):
    resource_json = {}
    try:
        query_data = get_billing_data_per_resource_per_project_per_month(str(year), str(month), str(project),
                                                                         str(resource))
        log_output(query_data)
        month_int = int(month)
        days = calendar.monthrange(year, month_int)[1] + 1
        each_day = []

        for x in range(1, days):
            each_day.append({'name': x, 'cost': 0, 'usage': 0, 'unit': ''})

        d3_json = [{'key': 'Cost', 'values': [], 'bar': True}, {'key': 'Usage', 'values': []}]

        for (day, cost, use, unit) in query_data:
            for val in each_day:
                if val['name'] == day:
                    val['cost'] = float(cost)
                    val['usage'] = float(use)
                    val['unit'] = str(unit)

            value = []
            value.append(day)
            value.append(float(cost))
            value.append('$')
            d3_json[0]['values'].append(value)
            value = []
            value.append(day)
            value.append(float(use))
            value.append(str(unit))
            d3_json[1]['values'].append(value)

        project_list_local = project_list_per_center(center)['list']
        resource_list_local = resource_list_per_project(center, project)

        resource_json = {'usage_data': each_day, 'd3_json': d3_json, 'project_list': project_list_local,
                         'resource_list': resource_list_local}
    except Exception as e:
        log_error(e)
    return resource_json


'''
    API for getting  cost of a resource for all project for a month

'''


def get_costs_per_resource_all_project_per_day(year, month, center, resource):
    resource_json = {}
    try:
        project_list_local = project_list_per_center(center)['list']
        project_list_ids = project_list_per_center(center)['ids']

        month_int = int(month)
        days = calendar.monthrange(year, month_int)[1] + 1
        each_day = []

        query_data = get_billing_data_per_resource_all_project_per_day(str(year), str(month), project_list_ids,
                                                                       str(resource))
        log_output(query_data)

        for x in range(1, days):
            each_day.append({'name': x, 'cost': 0, 'usage': 0, 'unit': ''})

        d3_json = [{'key': 'Cost', 'values': [], 'bar': True}, {'key': 'Usage', 'values': []}]

        for (day, cost, use, unit) in query_data:
            for val in each_day:
                if val['name'] == day:
                    val['cost'] = float(cost)
                    val['usage'] = float(use)
                    val['unit'] = str(unit)

            value = []
            value.append(day)
            value.append(float(cost))
            value.append('$')
            d3_json[0]['values'].append(value)
            value = []
            value.append(day)
            value.append(float(use))
            value.append(str(unit))
            d3_json[1]['values'].append(value)

        resource_list_local = resource_list_per_project(center, None)


        resource_json = {'usage_data': each_day, 'd3_json': d3_json, 'project_list': project_list_local,
                         'resource_list': resource_list_local}
    except Exception as e:
        log_error(e)
    return resource_json



'''
    get cost_center data
'''


'''
    function to get the cost_center list
'''


def get_center_list(unique):
    log_output('in get center list ------')
    log_output(unique)
    cost_center_list = []

    project_unique_ids = []

    if unique:
        center_list = get_cost_centers(unique)
        log_output(center_list)

        for (cost_center) in center_list:
            cost_center_list.append(cost_center[0])

        cost_center_list.append('other')
    else:
        center_list = get_cost_centers(unique)
        log_output(center_list)

        for center in center_list:
            project = dict()
            center_data = json.loads(json.dumps(center, cls=AlchemyEncoder))
            project['cost_center'] = center_data['cost_center']
            project['project_id'] = center_data['project_id']
            project['project_name'] = center_data['project_name']
            project['director'] = center_data['director']

            project_unique_ids.append(center_data['project_id'])

            cost_center_list.append(project)

        project_list = get_distinct_projects()

        log_output('In Project List')
        log_output(project_list)

        for project in project_list:
            if project[0] not in project_unique_ids:
                cost_center_list.append(
                    dict(cost_center='other', project_id=project[0], project_name=project[0], director='None'))

    return cost_center_list



def table_create():
    return create_table()

def get_project_by_id(project_id):
    return get_project(project_id)

def update_project_data(cost_center, project_id, project_name, director):
    return update_project(cost_center, project_id, project_name, director)

def create_project_data(cost_center, project_id, project_name, director):
    return create_project(cost_center, project_id, project_name, director)

def delete_project_by_id(project_id):
    return delete_project(project_id)


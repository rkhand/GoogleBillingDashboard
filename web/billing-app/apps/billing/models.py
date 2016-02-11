__author__ = "Ashwini Chandrasekar(@sriniash)"
__email__ = "ASHWINI_CHANDRASEKAR@homedepot.com"
__version__ = "1.0"
__doc__ = "Models relating to the DB tables"

import json

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from apps.config.apps_config import Base,db_session

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DATETIME, FLOAT, DECIMAL



from sqlalchemy.sql import func

'''
   Models :
     Projects Table with : ID, cost_center, project_id,project_name,director
'''


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    cost_center = Column(String(100))
    project_id = Column(String(16))
    project_name = Column(String(100))
    director = Column(String(100))

    def __init__(self, cost_center, project_id, project_name, director):
        self.cost_center = cost_center
        self.project_id = project_id
        self.project_name = project_name
        self.director = director

    def __repr__(self):
        return '<Project %r %r %r %r>' % (self.cost_center, self.project_id, self.project_name, self.director)


'''
  Usage table with : id,usage_date,cost,project_id,resource_type,account_id,usage_value,measurement_unit
  project_id is the reference between this table and Projects table to get the cost center for that project
'''


class Usage(Base):
    __tablename__ = 'usage'
    id = Column(Integer, primary_key=True)
    usage_date = Column(DATETIME)
    cost = Column(FLOAT)
    project_id = Column(String(16))
    resource_type = Column(String(128))
    account_id = Column(String(24))
    usage_value = Column(DECIMAL(25, 4))
    measurement_unit = Column(String(16))

    def __init__(self, usage_date, cost, project_id, resource_type, account_id, usage_value, measurement_unit):
        self.usage_date = usage_date
        self.cost = cost
        self.project_id = project_id
        self.resource_type = resource_type
        self.account_id = account_id
        self.usage_value = usage_value
        self.measurement_unit = measurement_unit

    def __repr__(self):
        return '<Usage %r %r %r %r %r %r %r >' % (
        self.usage_date, self.cost, self.project_id, self.resource_type, self.account_id, self.usage_value,
        self.measurement_unit)


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)



'''
    __doc__ = "Any DB connection or query is executed here"
'''



'''
    Create tables for the first time
'''


def create_table():
    db_session.create_all()
    return True


'''
    Get the list of distinct projects from usage table

    SELECT  DISTINCT(project_id) FROM reporting.usage;
'''


def get_distinct_projects():
    project_list = db_session.query(Usage.project_id).distinct()

    return project_list


'''
    Get the list of cost centers from project table

    SELECT distinct(cost_center) FROM reporting.projects;
'''


def get_cost_centers(unique):
    if unique:
        center_list = db_session.query(Projects.cost_center).distinct()
    else:
        center_list = db_session.query(Projects).all()
    return center_list


'''
    Get the list of projects already in projects table

    "SELECT project_id as project_id FROM reporting.projects where project_id = '12345';"
'''


def get_project(project_id):
    project = Projects.query.filter_by(project_id=project_id).all()

    return project


'''
    Update project info in projects table

'''


def update_project(cost_center, project_id, project_name, director):
    project = Projects.query.filter_by(project_id=project_id).first()
    project.cost_center = cost_center
    project.project_name = project_name
    project.director = director

    db_session.commit()

    return project


'''
    Insert project info in projects table

'''


def create_project(cost_center, project_id, project_name, director):
    project = Projects(cost_center, project_id, project_name, director)
    db_session.add(project)
    db_session.commit()

    return project


'''
    Delete project info in projects table
'''


def delete_project(project_id):
    project = Projects.query.filter_by(project_id=project_id).first()

    db_session.delete(project)
    db_session.commit()

    return project


'''
    Get the list of resource_list from  usage table

    SELECT  DISTINCT(resource_type) FROM reporting.usage where project_id in (" + project_ids + ");

'''


def get_resource_list_per_project(project_ids):
    resource_list = db_session.query(Usage.resource_type). \
        filter(Usage.project_id.in_(project_ids)). \
        distinct()
    return resource_list


'''
    Get billing data per year

    SELECT monthname(usage.usage_date) AS monthname_1, sum(usage.cost) AS sum_1 FROM usage
    WHERE EXTRACT(year FROM usage.usage_date) = '2015' GROUP BY monthname(usage.usage_date)

'''


def get_billing_data_per_year(year):
    billing_data = db_session.query(func.extract('month',Usage.usage_date), func.sum(Usage.cost)). \
        filter(func.extract('year', Usage.usage_date) == year).group_by(func.extract('month',Usage.usage_date))
    return billing_data


'''
    Get billing data per year per month

    SELECT usage.project_id AS usage_project_id, sum(usage.cost) AS sum_1 FROM usage
    WHERE EXTRACT(year FROM usage.usage_date) = '2015'  AND
    EXTRACT(month FROM usage.usage_date) = '11' GROUP BY usage.project_id

'''


def get_billing_data_per_year_per_month(year, month):
    billing_data = db_session.query(Usage.project_id, func.sum(Usage.cost)). \
        filter(func.extract('year', Usage.usage_date) == year,
               func.extract('month', Usage.usage_date) == month).group_by(Usage.project_id)

    return billing_data


'''
    Get billing data per year per center
    ( project ids will be passed that will belong to a center)

    SELECT monthname(usage.usage_date) AS monthname_1, sum(usage.cost) AS sum_1 FROM usage
    WHERE EXTRACT(year FROM usage.usage_date) = :param_1 AND usage.project_id IN (:project_id_1, :project_id_2,
    :project_id_3, :project_id_4, :project_id_5, :project_id_6, :project_id_7) GROUP BY monthname(usage.usage_date)

'''


def get_billing_data_per_year_per_center(year, project_ids):
    billing_data = db_session.query(func.extract('month',Usage.usage_date), func.sum(Usage.cost)). \
        filter(func.extract('year', Usage.usage_date) == year, Usage.project_id.in_(project_ids)). \
        group_by(func.extract('month',Usage.usage_date))

    return billing_data


'''
    Get billing data of each project for a year

'''


def get_billing_data_per_project_year(year, project_id):
    billing_data = db_session.query(func.extract('month',Usage.usage_date), func.sum(Usage.cost)). \
        filter(func.extract('year', Usage.usage_date) == year, Usage.project_id == project_id). \
        group_by(func.extract('month',Usage.usage_date))

    return billing_data


'''
    Get aggregated cost of each resource for a project for that month

     SELECT usage.resource_type AS usage_resource_type, sum(usage.cost) AS sum_1 FROM usage
      WHERE EXTRACT(year FROM usage.usage_date) = :param_1 AND
       EXTRACT(month FROM usage.usage_date) = :param_2 AND usage.project_id = :project_id_1
        GROUP BY month(usage.usage_date)

'''


def get_billing_data_per_resource_month_center(year, month, project_id):
    billing_data = db_session.query(Usage.resource_type, func.sum(Usage.cost)). \
        filter(func.extract('year', Usage.usage_date) == year, func.extract('month', Usage.usage_date) == month,
               Usage.project_id == project_id, ). \
        group_by(Usage.resource_type)

    return billing_data


'''
    Get aggregated cost of each resource for a resource


'''


def get_billing_data_per_resource(year, project_ids, resource):
    billing_data = db_session.query(func.extract('month',Usage.usage_date), func.sum(Usage.cost)). \
        filter(func.extract('year', Usage.usage_date) == year, Usage.project_id.in_(project_ids),
               Usage.resource_type == resource). \
        group_by(func.extract('month',Usage.usage_date))

    return billing_data


'''
    Get aggregated  cost of a resource for a project for all months

'''


def get_billing_data_per_resource_per_project(year, project_id, resource):

    billing_data = db_session.query(func.extract('month',Usage.usage_date), func.sum(Usage.cost)). \
        filter(func.extract('year', Usage.usage_date) == year, Usage.project_id == project_id,
               Usage.resource_type == resource). \
        group_by(func.month(Usage.usage_date))

    return billing_data


'''
    Get aggregated   cost of a resource for a project for a month

     SELECT day(usage.usage_date) AS day_1, sum(usage.cost) AS sum_1, usage.usage_value AS usage_usage_value,
      usage.measurement_unit AS usage_measurement_unit FROM usage
      WHERE EXTRACT(year FROM usage.usage_date) = :param_1 AND
       usage.project_id = :project_id_1 AND usage.resource_type = :resource_type_1
       AND EXTRACT(month FROM usage.usage_date) = :param_2 GROUP BY day(usage.usage_date)

'''


def get_billing_data_per_resource_per_project_per_month(year,month,project_id, resource):


    billing_data = db_session.query(func.extract('day',Usage.usage_date), func.sum(Usage.cost),Usage.usage_value,Usage.measurement_unit). \
        filter(func.extract('year', Usage.usage_date) == year, Usage.project_id == project_id,
               Usage.resource_type == resource,func.extract('month', Usage.usage_date) == month). \
        group_by(func.extract('day',Usage.usage_date))

    return billing_data



'''
    Get aggregated cost of a resource for all project for a month


'''


def get_billing_data_per_resource_all_project_per_day(year,month,project_ids, resource):


    billing_data = db_session.query(func.extract('day',Usage.usage_date), func.sum(Usage.cost),Usage.usage_value,Usage.measurement_unit). \
        filter(func.extract('year', Usage.usage_date) == year,  Usage.project_id.in_(project_ids),
               Usage.resource_type == resource,func.extract('month', Usage.usage_date) == month). \
        group_by(func.extract('day',Usage.usage_date))

    return billing_data





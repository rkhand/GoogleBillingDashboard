
import logging

from flask.ext.sqlalchemy import SQLAlchemy
import os


from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.pool import NullPool


file_path = os.path.abspath(os.getcwd()) + "/reporting.db"
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_RECORD_QUERIES = True

'''
  SQL DB

'''
# SQLALCHEMY_DATABASE_URI = 'mysql://username:password@ip-address/db_name'
SQLALCHEMY_DATABASE_URI = 'mysql://reporter:gener@te@127.0.0.1/reporting'


log_file = '/tmp/usagereport.log'

log = logging.getLogger()

engine = create_engine(SQLALCHEMY_DATABASE_URI, poolclass=NullPool)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


'''
    query error logging
'''


def log_error(e):
    return log.error('Error -- {0}'.format(e))


'''
    query output logging
'''


def log_output(data):
    return log.info('Data -- {0}'.format(data))

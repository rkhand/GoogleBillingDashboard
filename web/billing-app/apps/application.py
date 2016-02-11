import logging
from flask.app import Flask
from apps.config.apps_config import db_session, log_file


app = Flask(__name__)


from apps.billing.views import mod as billingModule
from apps.login.views import mod as loginModule

app.register_blueprint(billingModule)
app.register_blueprint(loginModule)



@app.teardown_appcontext
def shutdown_session(exception=None):
    log.info('----------------- IN Shutdown session --------------')
    db_session.remove()
    log.info('----------------- AFter RemoveShutdown session --------------')


logging.basicConfig(filename=log_file, level=logging.DEBUG)
log = logging.getLogger()









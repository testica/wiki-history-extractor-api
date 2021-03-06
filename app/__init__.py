from flask import Flask

from celery import Celery
from config import config, Config
from vendors.db_connector import RevisionDB
import os

env_name = os.getenv('FLASK_CONFIG') or 'default'
celery = Celery(__name__, backend=config[env_name].CELERY_RESULT_BACKEND, broker=config[env_name].CELERY_BROKER_URL,include=[__name__+'.tasks'])

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    config['default'] = config[config_name]

    celery.conf.update(app.config)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1')

    #from .api_1_0 import auto
    #auto.init_app(app)

    return app

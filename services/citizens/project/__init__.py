# services/citizens/project/__init__.py

import os

from flask import Flask


CONNSTR = 'couchbase://couch/analitycDB'


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    from project.api.citizens import citizens_blueprint
    app.register_blueprint(citizens_blueprint)

    return app

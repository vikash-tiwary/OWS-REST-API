"""Application.

The API application is a `flask` application. It provides simple features such
as registering a url for a specific handlers.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from owslogger import flask_logger
from owsrequest import flask_request

from restapi import config

app = Flask(config.SERVICE_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = config.SQLALCHEMY_ENGINE_OPTIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)
flask_logger.setup(
    app,
    config.LOGGER_DSN,
    config.ENVIRONMENT,
    config.LOGGER_NAME,
    config.LOGGER_LEVEL,
    config.SERVICE_NAME,
    config.SERVICE_VERSION,
    exclude_paths=[config.HEALTH_CHECK],
)
flask_request.setup(app, config.ENVIRONMENT)

if config.ENVIRONMENT == config.DEV_ENVIRONMENT:
    from flasgger import Swagger

    app.config["SWAGGER"] = {
        "title": "ows-REST-Api Documentation",
        "uiversion": 2,
    }
    try:
        Swagger(app, template_file=config.SWAGGER_FILE_PATH)
    except FileNotFoundError:
        print("Could not find swagger file at {}".format(config.SWAGGER_FILE_PATH))
elif config.ENVIRONMENT in [config.QA_ENVIRONMENT, config.PROD_ENVIRONMENT]:
    if not config.SENTRY:
        raise Exception(f'Sentry is not configured in {config.ENVIRONMENT}')

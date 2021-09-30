"""Application configuration."""

import logging
import os
from os.path import abspath, dirname, join, pardir
from secrets_manager.flask_ext import FlaskSecretsManager
from sqlalchemy.pool import QueuePool
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

# Load environment variables from a .env file if present
dotenv_path = abspath(join(dirname(__file__), pardir, ".env"))
load_dotenv(dotenv_path)

# Service information
SERVICE_NAME = "ows-REST-Api"
SERVICE_VERSION = "1.0.0"

# Production environment
PROD_ENVIRONMENT = "prod"
DEV_ENVIRONMENT = "dev"
QA_ENVIRONMENT = "qa"
TEST_ENVIRONMENT = "test-1"
ENVIRONMENT = os.environ.get("Environment") or DEV_ENVIRONMENT

secrets_manager_client = FlaskSecretsManager(
    application_context=False, environment=ENVIRONMENT,
    service_name=SERVICE_NAME)

# Database config
if ENVIRONMENT == TEST_ENVIRONMENT:
    DB_URL = 'sqlite://'
    POOL_CLASS = StaticPool
    CONNECT_ARGS = {'check_same_thread': False}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}
else:
    #DB_URL = os.environ.get('DB_URL')
    # DB_URL = (
    #     'mysql+pymysql://{user}:{password}@{host}/{db}?charset={charset}'
    #     .format(
    #         user=secrets_manager_client.get_cred('root'),
    #         password=secrets_manager_client.get_cred('root'),
    #         host=secrets_manager_client.get_cred('localhost'),
    #         db=secrets_manager_client.get_cred('restapi'),
    #         charset='utf8'))
    DB_URL = 'mysql+pymysql://root:root@localhost/restapi?charset=utf8'
    POOL_CLASS = QueuePool
    POOL_MAX_OVERFLOW = -1
    POOL_PRE_PING = False  # not needed as long as connections not stale
    POOL_RECYCLE_MS = 3600  # Avoids connections going stale
    POOL_SIZE = 15  # match the number of uwsgi threads
    CONNECT_ARGS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': POOL_SIZE,
        'pool_recycle': POOL_RECYCLE_MS,
        'max_overflow': POOL_MAX_OVERFLOW
    }

# Errors and loggers
SENTRY = os.environ.get("SENTRY_DSN") or None
LOGGER_DSN = os.environ.get("LOGGER_DSN") or None
LOGGER_LEVEL = logging.INFO
LOGGER_NAME = "ows1"

# Generic handlers
HEALTH_CHECK = "/hello/"

# Swagger documentation path
SWAGGER_FILE_PATH = "spec/ows_api-1.0.0.yaml"

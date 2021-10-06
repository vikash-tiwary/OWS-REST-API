"""Utility functions to support database interactions in tests."""

from contextlib import contextmanager
from functools import wraps
import sys
from unittest import mock

from restapi import config
from restapi.connectors import mysql
from restapi.models import post

CREATE_POST_TABLE = """
CREATE TABLE `post`
(
    `id` TEXT NOT NULL PRIMARY KEY,
    `title` TEXT NOT NULL,
    `description` varchar(2) DEFAULT NULL
)
"""

DROP_POST_TABLE = 'DROP TABLE IF EXISTS `post`'


def execute_sql(*args):
    """Run a series of queries safely within the test environment."""
    with mysql.db_session() as session:
        _exit_if_not_test_environment(session)

        for query in args:
            session.execute(query)


def seed_models(models):
    """Save the given model(s) to the DB.

    Args:
        models (list): list of model instances to save.
    """
    if not hasattr(models, '__iter__'):
        models = [models]

    with mysql.db_session() as session:
        _exit_if_not_test_environment(session)
        for model in models:
            session.add(model)
        session.flush()

        # detach the objects from this session so tests can interrogate them
        for model in models:
            session.expunge(model)


def test_schema(function):
    """Test schema.

    Decorator that creates the test DB schema before a function call and
    tears the schema down after the function call has finished.

    This just creates the schema and does not seed data. Individual test cases
    can use factories to seed data as needed.

    Args:
        function (func): function to be called after creating the test schema.

    Returns:
        Function: The decorated function.
    """
    @wraps(function)
    def call_function_within_db_context(*args, **kwargs):
        execute_sql(
            CREATE_POST_TABLE)

        try:
            function_return = function(*args, **kwargs)
        finally:
            execute_sql(
                DROP_POST_TABLE)

        return function_return
    return call_function_within_db_context


def _exit_if_not_test_environment(session):
    """For safety, only run tests in test environment pointed to sqlite.

    Exit immediately if not in test environment or not pointed to sqlite.
    """
    if config.ENVIRONMENT != config.TEST_ENVIRONMENT:
        sys.exit('Environment must be set to {}.'.format(
            config.TEST_ENVIRONMENT))
    if 'sqlite' not in session.bind.url.drivername:
        sys.exit('Tests must point to sqlite database.')


def mock_db_session(mocker):
    """Create a mock database sesssion.

    Also mock the db_session context manager to use the mock session.
    """
    mock_session = mock.Mock(query=mock.Mock())

    @contextmanager
    def fake_session_manager():
        yield mock_session

    mocker.patch.object(mysql, 'db_session', fake_session_manager)

    return mock_session


INSERT_DATA = [
    {
        'id': 1,
        'title': 'title-1',
        'description': 'description-1'
    },
    {
        'id': 2,
        'title': 'title-2',
        'description': 'description-2'
    }
]


def insert_post_data():
    """Insert data to post_priority table."""
    with mysql.db_session() as session:
        session.bulk_insert_mappings(
            post.Post, INSERT_DATA)

"""MySQL Connector.

Manages interactions with MySQL.
"""

from contextlib import contextmanager
import functools

from oto import response
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy import pool
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from restapi import config
from restapi.utils import error_handling


def _create_engine(db_url):
    """Create engine based on configuration settings."""
    if config.POOL_CLASS != pool.QueuePool:
        return create_engine(
            db_url, poolclass=config.POOL_CLASS,
            connect_args=config.CONNECT_ARGS)
    result = create_engine(
        db_url, pool_size=config.POOL_SIZE,
        max_overflow=config.POOL_MAX_OVERFLOW,
        connect_args=config.CONNECT_ARGS,
        pool_recycle=config.POOL_RECYCLE_MS)

    # SQLAlchemy 1.2 supports pessimistic disconnect handling out of box.
    # Once version 1.2 is out of beta, it is recommended to use
    # the `pool_pre_ping` param for `create_engine` and remove any code
    # in this file related to `_ping_connection`
    # See http://docs.sqlalchemy.org/en/latest/core/pooling.html
    if config.POOL_PRE_PING:
        event.listen(result, 'engine_connect', _ping_connection)
    return result


def _ping_connection(connection, branch):
    """Ping database connection after engine_connect event.

    This function is copied verbatim from
    http://docs.sqlalchemy.org/en/latest/core/pooling.html
    """
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise
    finally:
        # restore "close with result"
        connection.should_close_with_result = save_should_close_with_result


# please don't use the following private variables directly;
# use db_session
_db_engine = _create_engine(config.DB_URL)
_db_session = sessionmaker(bind=_db_engine)

BaseModel = declarative_base()


@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations.

    Taken from http://docs.sqlalchemy.org/en/latest/orm/session_basics.html.
    This handles rollback and closing of session, so there is no need
    to do that throughout the code.

    Usage:
        with db_session() as session:
            session.execute(query)
    """
    session = _db_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def wrap_db_errors(function):
    """Decorate the given function with logic to handle SQLAlchemy errors.

    If a SQLAlchemy exception is thrown, it will be caught and logged and the
    function will return a fatal response.

    Args:
        function (func): the function to decorate

    Returns:
        func: function decorated with error-handling logic
    """
    @functools.wraps(function)
    def call_function_with_error_handling(*args, **kwargs):
        try:
            function_return = function(*args, **kwargs)
        except exc.SQLAlchemyError as exception:
            error_handling.log_db_exception(exception)
            return response.create_fatal_response()

        return function_return
    return call_function_with_error_handling

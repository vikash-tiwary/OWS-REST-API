"""Error handler functions for specific types of failures."""

from flask import g

from restapi.connectors import sentry


def log_db_exception(exception):
    """Log a DB exception to Sentry and Loggly."""
    sentry.sentry_client.captureMessage(exception, stack=True)
    g.ows.log.error('DB error: {}'.format(exception))


def log_unexpected_response(service_name, bad_response):
    """Log an error message about an unexpected service response status.

    Args:
        service_name (str): name of the service that returned the response.
        bad_response(requests.Response): response object from the service.
    """
    error_message = '{} returned unexpected status {}'.format(
        service_name, bad_response.status_code)
    if bad_response.text:
        error_message += ' with body: {}'.format(bad_response.text)

    sentry.sentry_client.captureMessage(error_message, stack=True)
    g.ows.log.error(error_message)


def non_deadlock_error(pymysql_internal_error):
    """Determine whether a pymysql.err.InternalError is a deadlock error.

    Args:
        error: pymysql.err.InternalError instance.
    Return:
        bool: True if pymysql.err.InternalError not deadlock, False otherwise.
    """
    code, msg = pymysql_internal_error.args
    if code != 1213:
        return True
    return False

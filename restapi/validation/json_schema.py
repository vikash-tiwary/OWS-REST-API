"""JSON Draft3 Schema Validator Wrapper."""

from functools import wraps
import flask
from flask import request

from oto import response
from oto.adaptors import flask as oto_flask

from restapi.constants import error as error_constants
from restapi.constants import header
from restapi.validation.schema import json_validators


def _filter(data):
    """Sanitize a dictionary of request input data (e.g. headers or body).

    This is done before applying JSON schema validations to the data.
    Sanitization includes:
    1.) Stripping leading or trailing space from strings
    2.) Replacing empty strings with None

    Args:
        data (dict): the data to be sanitized

    Returns:
        dict: a sanitized version of the given data
    """
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()
        if data[key] == '':
            data[key] = None
    return data


def _format_error(error):
    return {
        'validator': error.validator,
        'validator_value': error.validator_value,
        'message': error.message,
        'error_code': f'{error.error_code}_{error.validator}',
    }


def validate(data, validator, failure_status=400):
    """Generic JSON Draft3 Schema Validation.

    Args:
        data (dict): the JSON to be validated.
        validator (Draft3Validator): the JSON Draft3 Schema to validate against
        failure_status (int): failure status code

    Returns:
        Response: the result of the validation.
    """
    errors = {}
    data = _filter(data)
    for error in sorted(validator.iter_errors(data), key=str):
        if error.relative_path:
            error_code = error.relative_path.pop()
            error.error_code = error_code
            errors[error_code] = _format_error(error)
        elif error.absolute_schema_path:
            error_code = error.absolute_schema_path.pop()
            error.error_code = error_code
            errors[error_code] = _format_error(error)

    if errors:
        return response.create_error_response(
            code=error_constants.ERROR_CODE_BAD_REQUEST,
            message=errors,
            status=failure_status)

    return response.Response(message={'status': 'ok'}, status=200)


def _wrap_request_validation(request_validation):
    """Decorate a route handler with the given validation function.

    If validation fails, the route will return an error response and the
    handler will not be executed. If validation succeeds, the hander will be
    executed.

    Sample usage:
        @app.route('/resource', methods=['POST'])
        @json_schema.wrap_request_validation(
            json_schema.validate_request_headers)
        @json_schema.wrap_request_validation(
            json_schema.validate_request_body)
        def handle_resource_request():
            # handler code here...

    Args:
        request_validation (callable): the validation function to execute.

    Returns:
        callable: decorator that wraps the given route handler with validation.
    """
    def decorator(func):
        @wraps(func)
        def validate_request(*args, **kwargs):
            validation_response = request_validation()
            if validation_response.status != 200:
                return oto_flask.flaskify(validation_response)
            return func(*args, **kwargs)
        return validate_request
    return decorator


def validate_request_args(func):
    """Validate the query args in the given request against the RAML spec.

    Args:
        func (callable): function to wrap with validator.

    Returns:
        callable: decorated function.
    """
    def _check_request_args():
        return validate(
            request.args.to_dict(), json_validators.query_args_validator())
    return _wrap_request_validation(_check_request_args)(func)


def validate_request_body(func):
    """Validate the JSON payload of the given request against the RAML spec.

    The method will generally be "post" or "put".

    Args:
        func (callable): function to wrap with validator.

    Returns:
        callable: decorated function.
    """
    def _check_request_body():
        print(request.get_json())
        return validate(
            request.get_json(), json_validators.body_validator())
    return _wrap_request_validation(_check_request_body)(func)


def validate_request_headers(func):
    """Validate the headers of the given request against the RAML spec.

    Args:
        func (callable): function to wrap with validator.

    Returns:
        callable: decorated function.
    """
    def _check_request_headers():
        return validate(
            dict(request.headers), json_validators.headers_validator())
    return _wrap_request_validation(_check_request_headers)(func)


def reject_grass_headers(func):
    """Decorator that rejects grass headers.

    Args:
        func (callable): function to decorate

    Returns:
        callable: the wrapped function.
    """
    @wraps(func)
    def _validate(*args, **kwargs):
        account_type = request.headers.get(header.GRASS_ACCOUNT_TYPE)
        account_id = request.headers.get(header.GRASS_ACCOUNT_ID)
        error_msg = error_constants.ERROR_MESSAGE_GRASS_REJECT_VALIDATION
        if account_type or account_id:
            return flask.Response(
                response=error_msg, status=400, mimetype='text/plain')

        return func(*args, **kwargs)
    return _validate

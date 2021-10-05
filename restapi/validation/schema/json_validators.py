"""JSON Draft3 Schema Validators."""

from flask import request
from jsonschema import Draft3Validator

from restapi import config


def raml_header_to_json_schema(raml_headers):
    """Convert a RAML header spec to a JSON schema.

    NOTE: we have to filter out props with None as the value :(

    Args:
        raml_headers (collections.OrderedDict): the headers part of a RAML
            endpoint descriptor.

    Returns:
        dict: the dict representing JSON validation schema snippet.
    """
    properties = {}
    for item in raml_headers:
        raw_props = raml_headers[item]
        props = {}
        for prop in raw_props.__dict__:
            if raw_props.__dict__[prop] is not None:
                props[prop] = raw_props.__dict__[prop]
        properties[item] = props

    schema = {
        '$schema': 'http://json-schema.org/draft-03/schema',
        'type': 'object',
        'required': True,    
        'properties': properties
    }
    return schema


def get_method_spec():
    """Extract the RAML spec section for current request resource and method.

    Returns:
        pyraml.entities.RamlMethod: spec for the given resource and method.
    """
    resource = request.url_rule.rule
    method = request.method.lower()
    return config.API_DEFINITION.resources[resource].methods[method]


def query_args_validator():
    """Construct a JSON validator based on the query args from RAML spec.

    Returns:
        Draft3Validator: schema validator object for query args
    """
    method_spec = get_method_spec()
    return Draft3Validator(
        raml_header_to_json_schema(method_spec.queryParameters))


def headers_validator():
    """Construct a JSON validator based on headers from RAML spec.

    Returns:
        Draft3Validator: schema validator object for headers
    """
    method_spec = get_method_spec()
    return Draft3Validator(
        raml_header_to_json_schema(method_spec.headers))


def body_validator():
    """Construct a JSON validator based on request body schema from RAML spec.

    Returns:
        Draft3Validator: schema validator object for request body
    """
    method_spec = get_method_spec()
    return Draft3Validator(method_spec.body['application/json'].schema)

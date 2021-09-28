"""Integration tests."""

import requests

from tests.integration.consts import api


def test_get_hello():
    """Get Hello Endpoint."""
    response = requests.get(api.HEALTH_CHECK)
    assert response.status_code == 200, "\nReason: {}\nURL: {}".format(
        response.reason, response.url
    )
    response_body = response.json()

    assert "status" in response_body
    assert "ok" in response_body["status"]

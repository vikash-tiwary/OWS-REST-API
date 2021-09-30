import application
import pytest


@pytest.fixture
def client():
    """Return flask test client.

    Returns:
        flask client: flask test client
    """
    return application.app.test_client()


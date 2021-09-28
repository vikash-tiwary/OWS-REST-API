"""Constants for api tests."""

from tests.integration import config

# urls
HEALTH_CHECK = "{qa_base_url}/hello/".format(qa_base_url=config.QA_BASE_URL)

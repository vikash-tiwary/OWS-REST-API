"""Application."""
from flask import Flask  # noqa: F401

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from restapi import api
from restapi import config
from restapi import handlers  # noqa:F401

if config.SENTRY:
    sentry_sdk.init(
        dsn=config.SENTRY,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )

app = api.app

import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from config.helpers.env import env

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR,
)

sentry_sdk.init(
    dsn=env.sentry_sdk_dsn,
    integrations=[sentry_logging, DjangoIntegration(), RedisIntegration()],
    environment=env.environment,
    traces_sample_rate=0.0,
)

import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from config.helpers.env import env

# Configure Sentry logging integration
# https://docs.sentry.io/platforms/python/integrations/logging/
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

# Initialize Sentry SDK
# https://docs.sentry.io/platforms/python/configuration/options/
sentry_sdk.init(
    dsn=env.sentry_sdk_dsn,
    # Integrations
    integrations=[
        sentry_logging,
        DjangoIntegration(),
        RedisIntegration(),
    ],
    # Environment tracking
    environment=env.environment,
    # Performance monitoring (0.0 = disabled, 1.0 = 100% of transactions)
    # Set to small value like 0.1 to sample 10% of transactions in production
    traces_sample_rate=0.0,
    # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions
    # We recommend adjusting this value in production
    profiles_sample_rate=0.0,
    # Send default PII (Personally Identifiable Information)
    # Set to True only if you need user IP, cookies, etc. in error reports
    send_default_pii=False,
    # Maximum number of breadcrumbs
    max_breadcrumbs=50,
    # Attach stack traces to messages
    attach_stacktrace=True,
    # Sample rate for error events (1.0 = 100%)
    sample_rate=1.0,
    # Before send callback - filter or modify events before sending
    # before_send=lambda event, hint: event,
)

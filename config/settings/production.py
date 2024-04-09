# Base imports and environment setup
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .base import *  # noqa
from .base import env

# GENERAL SETTINGS
# ------------------------------------------------------------------------------

print("loading production settings")
SECRET_KEY = env("DJANGO_SECRET_KEY")
domain_url = env("DOMAIN")

ALLOWED_HOSTS = [domain_url]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# CACHE CONFIGURATION
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

# SECURITY SETTINGS
# ------------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 518400
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)

# ADMIN SETTINGS
# ------------------------------------------------------------------------------
ADMIN_URL = env("DJANGO_ADMIN_URL")

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {"level": "ERROR", "handlers": ["console"], "propagate": False},
    },
}

# SENTRY CONFIGURATION
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)
sentry_logging = LoggingIntegration(level=SENTRY_LOG_LEVEL, event_level=logging.ERROR)
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[sentry_logging, DjangoIntegration(), RedisIntegration()],
    environment=env("SENTRY_ENVIRONMENT", default="production"),
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
)



# django-rest-framework
SPECTACULAR_SETTINGS["SERVERS"] = [{"url": f"https://{domain_url}", "description": "Production server"}]



# MEDIA + STATIC SETTINGS
# ------------------------------------------------------------------------------
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
AWS_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"

INSTALLED_APPS += ["storages"]
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",
}
AWS_S3_MAX_MEMORY_SIZE = env.int(
    "DJANGO_AWS_S3_MAX_MEMORY_SIZE",
    default=100_000_000,  # 100MB
)

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "media",
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "static",
        },
    },
}

COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS
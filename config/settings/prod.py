# ruff: noqa

from .base import *  # noqa
from ..helpers.env import env

print("loading production settings")  # noqa: T201

DEBUG = False

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = [env.domain_name]
# If using subdomain cookie domain (e.g., .example.com), add it to ALLOWED_HOSTS
if env.cookie_domain and env.cookie_domain.startswith("."):
    ALLOWED_HOSTS.append(env.cookie_domain)


# ------------------------------------------------------------------------------
# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# SSL and Proxy Security
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = True

# Production-specific Cookie Security (overrides base.py defaults)
# Session Cookie Security
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = "__Secure-sessionid"

# CSRF Cookie Security
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = "__Secure-csrftoken"

# Note: CORS, CSRF domain, and trusted origins are configured in base.py
# using environment variables. This ensures consistent configuration across
# all environments (local, staging, production) with only env var differences.

# HSTS (HTTP Strict Transport Security)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# Start with 60 seconds, then increase to 518400 (6 months) after testing
SECURE_HSTS_SECONDS = 518400
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = True

# Additional Security Headers
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# ------------------------------------------------------------------------------
# AWS S3 STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["storages"]  # type: ignore

# AWS S3 Settings
AWS_STORAGE_BUCKET_NAME = env.s3_bucket_name
AWS_S3_REGION_NAME = env.aws_region_name
AWS_QUERYSTRING_AUTH = False
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",
}
AWS_S3_MAX_MEMORY_SIZE = 100_000_000

# AWS Domain Configuration
AWS_S3_CUSTOM_DOMAIN = (
    f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
    if AWS_S3_REGION_NAME
    else ""
)
aws_s3_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Storage Backends
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "media",
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "static",
        },
    },
}

# Media and Static URLs
MEDIA_URL = f"https://{aws_s3_domain}/media/"
STATIC_URL = f"https://{aws_s3_domain}/static/"
COLLECTFASTA_STRATEGY = "collectfasta.strategies.boto3.Boto3Strategy"

# ------------------------------------------------------------------------------
# ADDITIONAL APPS AND SETTINGS
# ------------------------------------------------------------------------------
# Add collectfasta to the beginning of INSTALLED_APPS
INSTALLED_APPS = ["collectfasta", *INSTALLED_APPS]

# DRF Spectacular Production Server Configuration
SPECTACULAR_SETTINGS["SERVERS"] = [
    {"url": f"https://{env.domain_name}", "description": "Production server"}  # type: ignore[list-item]
]

# ------------------------------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# Override base logging for production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry_sdk": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.request": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# ------------------------------------------------------------------------------
# EXTERNAL INTEGRATIONS
# ------------------------------------------------------------------------------
from config.integrations.sentry import *  # noqa

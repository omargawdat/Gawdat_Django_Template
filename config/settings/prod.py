# ruff: noqa

from .base import *  # noqa
from ..helpers.env import env

print("loading production settings")

DEBUG = False
ALLOWED_HOSTS = [env.domain_name]  # todo: ensure this is correct

# ------------------------------------------------------------------------------
# CACHE CONFIGURATION
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
}

# ------------------------------------------------------------------------------
# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# SSL and Cookie Security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

# Session and CSRF Settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME = "__Secure-sessionid"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = "__Secure-csrftoken"


# HSTS Settings
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

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
# ADMIN CONFIGURATION
# ------------------------------------------------------------------------------
ADMIN_URL = "pYeLUByN7zfgE5YlXsRsaferWlZF"

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
# EXTERNAL INTEGRATIONS
# ------------------------------------------------------------------------------
from config.integrations.sentry import *  # noqa

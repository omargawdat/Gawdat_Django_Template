# ruff: noqa: F405

from .base import *  # noqa

DEBUG = False

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
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

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

# AWS Credentials
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME", default="")

# AWS S3 Settings
AWS_QUERYSTRING_AUTH = False
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",
}
AWS_S3_MAX_MEMORY_SIZE = env.int("DJANGO_AWS_S3_MAX_MEMORY_SIZE", default=100_000_000)
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default=None)

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
            "default_acl": "public-read",
        },
    },
}

# Media and Static URLs
MEDIA_URL = f"https://{aws_s3_domain}/media/"
STATIC_URL = f"https://{aws_s3_domain}/static/"

# ------------------------------------------------------------------------------
# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="Temp-Project <noreply@example.com>"
)
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[Temp-Project] ")
ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX

INSTALLED_APPS += ["anymail"]  # type: ignore
ANYMAIL = {}

# ------------------------------------------------------------------------------
# ADMIN CONFIGURATION
# ------------------------------------------------------------------------------
ADMIN_URL = env("DJANGO_ADMIN_URL")

# ------------------------------------------------------------------------------
# ADDITIONAL APPS AND SETTINGS
# ------------------------------------------------------------------------------
# Add collectfasta to the beginning of INSTALLED_APPS
INSTALLED_APPS = ["collectfasta", *INSTALLED_APPS]

# DRF Spectacular Production Server Configuration
SPECTACULAR_SETTINGS["SERVERS"] = [
    {"url": f"https://{DOMAIN_NAME}", "description": "Production server"}  # type: ignore[list-item]
]


# ------------------------------------------------------------------------------
# EXTERNAL INTEGRATIONS
# ------------------------------------------------------------------------------
from config.integrations.sentry import *  # noqa

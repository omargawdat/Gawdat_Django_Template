from pathlib import Path

import dj_database_url
from corsheaders.defaults import default_headers
from django.utils.translation import gettext_lazy as _

from config.helpers.env import env

print("loading base settings")  # noqa: T201

# ==============================================================================
# PATHS
# ==============================================================================
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# ==============================================================================
# CORE SETTINGS
# ==============================================================================
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False  # Always False by default for security

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env.django_secret_key.get_secret_value()

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# ==============================================================================
# INTERNATIONALIZATION & LOCALIZATION
# ==============================================================================
TIME_ZONE = "Asia/Riyadh"
LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("ar", _("Arabic")),
    ("en", _("English")),
]
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(ASSETS_DIR / "locale")]

# Location-specific settings
SUPPORTED_COUNTRY_CODES = ["EG", "SA", "AE", "KW", "QA", "OM", "BH", "JO", "LB"]

# ==============================================================================
# URLS & WSGI
# ==============================================================================
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ==============================================================================
# DATABASE
# ==============================================================================
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        **dj_database_url.config(
            default=env.database_url,
            conn_max_age=600,
            conn_health_checks=True,
        ),
        "ATOMIC_REQUESTS": True,
    },
}

# ==============================================================================
# APPLICATIONS
# ==============================================================================
# Third-party applications
THIRD_PARTY_APPS = [
    "unfold",
    "unfold.contrib.import_export",
    "import_export",
    "unfold.contrib.simple_history",
    "simple_history",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.constance",
    "fcm_django",
    "rules",
    "imagekit",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_gis",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_spectacular",
    "solo",
    "drf_standardized_errors",
    "djmoney",
    "mapwidgets",
    "constance",
]

# Django core applications
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
    "django_model_suite",
    "modeltranslation",
    "django.contrib.gis",
    # Django-allauth
    "allauth",
    "allauth.account",
    "allauth.headless",
]

# Project applications
LOCAL_APPS = [
    "common",
    "apps.users",
    "apps.channel",
    "apps.appInfo",
    "apps.location",
    "apps.payment",
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

# ==============================================================================
# MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangorestframework_camel_case.middleware.CamelCaseMiddleWare",
    "config.middleware.AllauthErrorFormatterMiddleware",
]

# ==============================================================================
# AUTHENTICATION
# ==============================================================================
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Required for Django admin
    "allauth.account.auth_backends.AuthenticationBackend",  # For API/customer auth
]
AUTH_USER_MODEL = "users.User"

# Password hashers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================================================
# DJANGO-ALLAUTH HEADLESS CONFIGURATION
# ==============================================================================
# Authentication: Email only (simple and secure)
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Email must be verified before login
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Signup: Email + Password (minimal signup)
# Note: Use 'email*' only for headless API (password is handled separately)
# Profile-specific fields are collected in a separate profile completion step
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_SIGNUP_FORM_CLASS = "apps.users.forms.signup.CustomSignupForm"
ACCOUNT_ADAPTER = "apps.users.adapters.account.CustomAccountAdapter"

# Headless API configuration
HEADLESS_ADAPTER = "apps.users.adapters.headless.CustomHeadlessAdapter"
HEADLESS_ONLY = True
HEADLESS_SERVE_SPECIFICATION = True  # Enable OpenAPI spec at /_allauth/openapi.json

# Frontend URLs for email links (uses default frontend URL from env)
# Note: For mobile apps, these URLs can be deep links (e.g., myapp://password-reset/{key})
# Configure FRONTEND_DEFAULT_URL in .env to use your app's deep link scheme
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": f"{env.frontend_default_url}/verify-email/{{key}}",
    "account_reset_password": f"{env.frontend_default_url}/password/reset",
    "account_reset_password_from_key": f"{env.frontend_default_url}/password/reset/key/{{key}}",
    "account_signup": f"{env.frontend_default_url}/signup",
}


# ==============================================================================
# SECURITY
# ==============================================================================
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# Parse allowed frontend origins from environment variable (comma-separated)
FRONTEND_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in env.frontend_allowed_origins.split(",")
    if origin.strip()
]

# ==============================================================================
# CSRF CONFIGURATION (Django-Allauth Headless)
# ==============================================================================
# Store CSRF token in cookie (not session) so JavaScript can access it
CSRF_USE_SESSIONS = False
# CSRF cookie must be readable by JavaScript for headless API
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"
# Set cookie domain from environment (None for localhost, .example.com for subdomains)
CSRF_COOKIE_DOMAIN = env.cookie_domain if env.cookie_domain else None
# Trusted origins for CSRF validation
CSRF_TRUSTED_ORIGINS = FRONTEND_ALLOWED_ORIGINS

# ==============================================================================
# SESSION CONFIGURATION
# ==============================================================================
SESSION_COOKIE_SAMESITE = "Lax"
# Set cookie domain from environment (None for localhost, .example.com for subdomains)
SESSION_COOKIE_DOMAIN = env.cookie_domain if env.cookie_domain else None

# ==============================================================================
# CORS CONFIGURATION
# ==============================================================================
# https://github.com/adamchainz/django-cors-headers#configuration
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = FRONTEND_ALLOWED_ORIGINS
CORS_ALLOW_CREDENTIALS = True  # Required for session cookies and CSRF
# Only allow CORS on API endpoints, not admin or other pages
CORS_URLS_REGEX = r"^/api/.*$"

# Django-allauth headless requires custom headers for authentication flows

CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-session-token",
    "x-email-verification-key",
    "x-password-reset-key",
)

# ==============================================================================
# ADMIN
# ==============================================================================
ADMIN_URL = env.django_admin_url
BASE_MODEL_ADMIN_PATH = "common.base.admin"

# ==============================================================================
# STATIC FILES
# ==============================================================================
STATIC_ROOT = str(ASSETS_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(ASSETS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ==============================================================================
# MEDIA FILES
# ==============================================================================
MEDIA_ROOT = str(ASSETS_DIR / "media")
MEDIA_URL = "/media/"

# File upload settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024

# ==============================================================================
# TEMPLATES
# ==============================================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(ASSETS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================================================================
# EMAIL
# ==============================================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_TIMEOUT = 5
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.email_host_user
EMAIL_HOST_PASSWORD = env.email_host_password.get_secret_value()

# ==============================================================================
# CACHING
# ==============================================================================
# Note: Using database cache for AWS App Runner compatibility
# Consider using Redis cache in production for better performance
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
        "TIMEOUT": 300,
        "OPTIONS": {
            "MAX_ENTRIES": 10000,
            "CULL_FREQUENCY": 3,
        },
    }
}

# ==============================================================================
# REDIS
# ==============================================================================
REDIS_URL = "redis://redis:6379/0"
REDIS_SSL = REDIS_URL.startswith("rediss://")

# ==============================================================================
# LOGGING
# ==============================================================================
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for more details
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# ==============================================================================
# OTP (ONE-TIME PASSWORD) SETTINGS
# ==============================================================================
OTP_EXPIRY_SECONDS = 300
OTP_LENGTH = 5
OTP_MAX_ATTEMPTS = 3
OTP_HOURLY_LIMIT = 5
OTP_EMAIL_SECONDS = 600

# ==============================================================================
# GOOGLE MAPS INTEGRATION
# ==============================================================================
GOOGLE_MAP_API_KEY = env.google_map_api_key.get_secret_value()

MAP_WIDGETS = {
    "GoogleMap": {
        "apiKey": GOOGLE_MAP_API_KEY,
        "PointField": {
            "interactive": {
                "mapOptions": {
                    "zoom": 15,
                    "streetViewControl": False,
                },
                "GooglePlaceAutocompleteOptions": {
                    "componentRestrictions": {"country": "sa"}
                },
            }
        },
    },
    "Leaflet": {
        "PointField": {
            "interactive": {"mapOptions": {"zoom": 12, "scrollWheelZoom": False}}
        },
        "markerFitZoom": 14,
    },
}

# ==============================================================================
# THIRD-PARTY INTEGRATIONS
# ==============================================================================
# Import configurations from separate integration modules
from config.integrations.drf import *  # noqa
from config.integrations.djmoney import *  # noqa
from config.integrations.unfold import *  # noqa
from config.integrations.fcm import *  # noqa

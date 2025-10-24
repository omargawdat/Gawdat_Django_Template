from pathlib import Path

import dj_database_url
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
    "allauth.socialaccount",
    "allauth.socialaccount.providers.dummy",
    "allauth.socialaccount.providers.google",
    "allauth.headless",
    "allauth.usersessions",
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
    # add django default auth backend
    "django.contrib.auth.backends.ModelBackend",
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
# AUTHENTICATION MODE: Choose one configuration block below
# Note: Phone and email authentication cannot be used together
# Uncomment the desired mode and comment out the other
# ==============================================================================

# ┌─────────────────────────────────────────────────────────────────────────────
# │ OPTION 1: PHONE NUMBER AUTHENTICATION (CURRENTLY ACTIVE)
# └─────────────────────────────────────────────────────────────────────────────
ACCOUNT_LOGIN_METHODS = {"phone"}
ACCOUNT_SIGNUP_FIELDS = ["phone"]
ACCOUNT_LOGIN_BY_CODE_ENABLED = True
ACCOUNT_PHONE_VERIFICATION_ENABLED = True
ACCOUNT_PHONE_VERIFICATION_MAX_ATTEMPTS = 3
ACCOUNT_PHONE_VERIFICATION_TIMEOUT = 900  # 15 minutes
ACCOUNT_PHONE_VERIFICATION_SUPPORTS_CHANGE = False
ACCOUNT_PHONE_VERIFICATION_SUPPORTS_RESEND = True

# ┌─────────────────────────────────────────────────────────────────────────────
# │ OPTION 2: EMAIL AUTHENTICATION (COMMENTED OUT)
# │ To switch: Comment out Option 1 above, then uncomment all lines below
# └─────────────────────────────────────────────────────────────────────────────
# ACCOUNT_LOGIN_METHODS = {"email"}
# ACCOUNT_SIGNUP_FIELDS = ["email"]  # email is required
# ACCOUNT_LOGIN_BY_CODE_ENABLED = False  # Password-based login
#
# # Phone verification settings (disabled for email-only mode)
# ACCOUNT_PHONE_VERIFICATION_ENABLED = False
# ACCOUNT_PHONE_VERIFICATION_MAX_ATTEMPTS = 3
# ACCOUNT_PHONE_VERIFICATION_TIMEOUT = 900
# ACCOUNT_PHONE_VERIFICATION_SUPPORTS_CHANGE = False
# ACCOUNT_PHONE_VERIFICATION_SUPPORTS_RESEND = True
#
# # Email verification settings
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Users must verify email before login
# ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True  # Use link-based verification
# ACCOUNT_EMAIL_REQUIRED = True

# ==============================================================================
# COMMON SETTINGS (apply to both modes)
# ==============================================================================
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False

# Custom adapters for signup and user data serialization
ACCOUNT_ADAPTER = "apps.users.adapters.account.CustomAccountAdapter"
# SOCIALACCOUNT_ADAPTER = "apps.users.adapters.socialaccount.CustomSocialAccountAdapter"
# ACCOUNT_SIGNUP_FORM_CLASS = "apps.users.forms.signup.CustomSignupForm"  # Removed - using default allauth signup

# Headless API configuration (matching demo exactly)
# HEADLESS_ADAPTER = "apps.users.adapters.headless.CustomHeadlessAdapter"
HEADLESS_ONLY = True
# Build frontend URLs dynamically from environment variable
# This allows different URLs for local/dev/staging/production deployments
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": "/account/verify-email/{key}",
    "account_reset_password": "/account/password/reset",
    "account_reset_password_from_key": "/account/password/reset/key/{key}",
    "account_signup": "/account/signup",
    "socialaccount_login_error": "/account/provider/callback",
}
HEADLESS_SERVE_SPECIFICATION = True

# Social Account Providers (matching demo exactly)
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env.google_oauth2_client_id,
            "secret": env.google_oauth2_client_secret.get_secret_value(),
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}


# ==============================================================================
# SECURITY
# ==============================================================================
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# ==============================================================================
# CORS CONFIGURATION
# ==============================================================================
# Allow origins from environment variable (comma-separated)
# This enables frontend developers to work locally against dev/staging backend
# Example: "https://app.example.com,http://localhost:3000,http://127.0.0.1:3000"
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in env.frontend_allowed_origins.split(",")
    if origin.strip()
]
# Enable credentials (cookies, authorization headers) in CORS requests
CORS_ALLOW_CREDENTIALS = True

# ==============================================================================
# CSRF CONFIGURATION
# ==============================================================================
# Trust same origins as CORS for CSRF validation
# This allows cross-origin POST requests from trusted frontend origins
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Cookie domain configuration (for cross-subdomain authentication)
# Leave empty for localhost development, use ".example.com" for production
if env.cookie_domain:
    SESSION_COOKIE_DOMAIN = env.cookie_domain
    CSRF_COOKIE_DOMAIN = env.cookie_domain

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
# EMAIL_BACKEND is configured in local.py/prod.py
# Base configuration for SMTP (used by production)
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

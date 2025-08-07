from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _

from config.helpers.env import env

print("loading base settings")  # noqa: T201

# ------------------------------------------------------------------------------
# Fields Settings
# ------------------------------------------------------------------------------
# PATH CONFIGURATION
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"
# SECURITY CONFIGURATION
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
CORS_ALLOW_ALL_ORIGINS = True
# ADMIN CONFIGURATION
ADMIN_URL = env.django_admin_url
# EMAIL CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_TIMEOUT = 5
# REDIS CONFIGURATION
REDIS_URL = "redis://redis:6379/0"
REDIS_SSL = REDIS_URL.startswith("rediss://")
# FILE UPLOAD CONFIGURATION
DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024
# Generator Package
BASE_MODEL_ADMIN_PATH = "common.base.admin"
# CORE SETTINGS
SECRET_KEY = env.django_secret_key.get_secret_value()
# OTP Settings
OTP_EXPIRY_SECONDS = 300
OTP_LENGTH = 5
OTP_MAX_ATTEMPTS = 3
OTP_HOURLY_LIMIT = 5
# INTERNATIONALIZATION SETTINGS
TIME_ZONE = "Asia/Riyadh"
LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("ar", _("Arabic")),
    ("en", _("English")),
]
SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(ASSETS_DIR / "locale")]
# APPLICATION CONFIGURATION
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
# DATABASE CONFIGURATION
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        **dj_database_url.parse(str(env.database_url)),
        "ATOMIC_REQUESTS": True,
        "OPTIONS": {
            "pool": {
                "min_size": 0,
                "max_size": 5,
                "timeout": 30,
                "max_lifetime": 1800,
                "max_idle": 120,
            },
        },
    },
}

# ------------------------------------------------------------------------------
# Third-party applications
# ------------------------------------------------------------------------------
THIRD_PARTY_APPS = [
    "unfold",
    "unfold.contrib.import_export",
    "import_export",
    "unfold.contrib.simple_history",
    "simple_history",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
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
    "django_tasks",
    "django_tasks.backends.database",
    "django.contrib.gis",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.apple",
    "dj_rest_auth",
    "dj_rest_auth.registration",
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

# ------------------------------------------------------------------------------
# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"

# Password settings
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

# ------------------------------------------------------------------------------
# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
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
]

TASKS = {"default": {"BACKEND": "django_tasks.backends.database.DatabaseBackend"}}

# ------------------------------------------------------------------------------
# STATIC AND MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ASSETS_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(ASSETS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
MEDIA_ROOT = str(ASSETS_DIR / "media")
MEDIA_URL = "/media/"

# ------------------------------------------------------------------------------
# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# todo: is that needed when using docker and app runner or local?
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
}


# Google Map Widget
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


# Oauth Configure
REST_USE_JWT = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_ADAPTER = "config.helpers.oauth_adapter.CustomerSocialAccountAdapter"


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env.google_oauth2_client_id,
            "secret": env.google_oauth2_client_secret.get_secret_value(),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    },
    "facebook": {
        "METHOD": "oauth2",
        "SCOPE": ["email", "public_profile"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "FIELDS": ["id", "email", "name", "first_name", "last_name", "picture"],
        "APP": {
            "client_id": env.facebook_oauth2_client_id,
            "secret": env.facebook_oauth2_client_secret.get_secret_value(),
            "key": "",
        },
    },
    "apple": {
        "APP": {
            "client_id": env.apple_oauth2_client_id,
            "secret": {
                "key": env.apple_oauth2_client_secret.get_secret_value(),
                "key_id": env.key_id,
                "team_id": env.team_id,
            },
        },
    },
}


# ------------------------------------------------------------------------------
# THIRD-PARTY INTEGRATIONS
# ------------------------------------------------------------------------------
from config.integrations.drf import *  # noqa
from config.integrations.djmoney import *  # noqa
from config.integrations.unfold import *  # noqa
from config.integrations.fcm import *  # noqa

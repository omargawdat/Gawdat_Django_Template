from pathlib import Path

from django.utils.translation import gettext_lazy as _

from config.env import env

# ------------------------------------------------------------------------------
# PATH CONFIGURATION
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION SETTINGS
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        **env.db("DATABASE_URL"),
        "ATOMIC_REQUESTS": True,
        "OPTIONS": {
            "pool": {
                "min_size": 5,
                "max_size": 20,
                "timeout": 30,
                "max_lifetime": 1800,
                "max_idle": 300,
            },
        },
    },
}

# ------------------------------------------------------------------------------
# APPLICATION CONFIGURATION
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Third-party applications
THIRD_PARTY_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.inlines",
    "fcm_django",
    "rules",
    "imagekit",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_spectacular",
    "solo",
    "drf_standardized_errors",
    "djmoney",
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
]

# Project applications
LOCAL_APPS = [
    "common",
    "apps.users",
    "apps.notification",
    "apps.appInfo",
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

# ------------------------------------------------------------------------------
# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
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
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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
# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
CORS_ALLOW_ALL_ORIGINS = True

# ------------------------------------------------------------------------------
# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_TIMEOUT = 5

# ------------------------------------------------------------------------------
# ADMIN CONFIGURATION
# ------------------------------------------------------------------------------
ADMIN_URL = "admin/"
ADMINS = [
    (
        env("DJANGO_ADMIN_NAME", default="admin"),
        env("DJANGO_ADMIN_EMAIL", default="admin@example.com"),
    )
]
MANAGERS = ADMINS

# ------------------------------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# REDIS CONFIGURATION
# ------------------------------------------------------------------------------
REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")

# ------------------------------------------------------------------------------
# FILE UPLOAD CONFIGURATION
# ------------------------------------------------------------------------------
DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024

# ------------------------------------------------------------------------------
# THIRD-PARTY INTEGRATIONS
# ------------------------------------------------------------------------------
from config.integrations.drf import *  # noqa
from config.integrations.djmoney import *  # noqa
from config.integrations.unfold import *  # noqa
from config.integrations.firebase import *  # noqa

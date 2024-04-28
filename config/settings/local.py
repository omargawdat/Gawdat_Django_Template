from .base import *  # noqa
from .base import env

# GENERAL SETTINGS
DEBUG = True
SECRET_KEY = env("DJANGO_SECRET_KEY", default="VR4IdxzB77oZgqvAOj64PN8v5S9EC9Jz8OXbsMFWCA4ycMaF8SD178UzLpZvpyrn")
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "my-dev-env.local"]  # Host/domain names that this site can serve

# CACHE SETTINGS
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL CONFIGURATION
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

# DEBUG TOOLBAR SETTINGS
INSTALLED_APPS += ["silk", "debug_toolbar", "django_extensions"]

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}  # Configuration for debug toolbar to ensure it's always shown

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]  # Internal IPs for use with debug toolbar
if env("USE_DOCKER") == "yes":  # Conditionally add Docker-related IPs to INTERNAL_IPS
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# SECURITY SETTINGS
# ------------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


STATIC_ROOT = os.path.join(BASE_DIR, "assets", "staticfiles")

STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "assets", "media")
MEDIA_URL = "/media/"

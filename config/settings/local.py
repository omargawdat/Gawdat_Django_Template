import socket

from .base import *  # noqa

print("loading local settings")  # noqa: T201

# ------------------------------------------------------------------------------
# DEBUG TOOLBAR CONFIGURATION
# ------------------------------------------------------------------------------
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ------------------------------------------------------------------------------
# CORS CONFIGURATION (Development Only)
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# Internal IPs Configuration
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# Docker-specific IP configuration
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [".".join([*ip.split(".")[:-1], "1"]) for ip in ips]

# ------------------------------------------------------------------------------
# DEVELOPMENT TOOLS
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]

# ------------------------------------------------------------------------------
# EMAIL CONFIGURATION (Development - Real Email via Gmail SMTP)
# ------------------------------------------------------------------------------
# Use real Gmail SMTP for testing (configured in base.py)
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # Disabled

# ------------------------------------------------------------------------------
# CORS CONFIGURATION (Development - Allow localhost frontend)
# ------------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True  # Required for CSRF cookies
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]
# Allow CSRF cookie to be read by JavaScript
CSRF_COOKIE_HTTPONLY = False  # Only for development!
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

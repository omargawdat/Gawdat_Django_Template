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
# CORS & CSRF CONFIGURATION
# ------------------------------------------------------------------------------
# Note: CORS and CSRF settings are configured in base.py using environment variables
# Local development uses the same configuration as production, just with different
# environment variable values (localhost URLs, no cookie domain, etc.)
# See: dummy.env for local development configuration examples

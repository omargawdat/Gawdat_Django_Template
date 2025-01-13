# ruff: noqa: F405

import socket

from .base import *  # noqa

# ------------------------------------------------------------------------------
# CORE DEVELOPMENT SETTINGS
# ------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = env("DJANGO_SECRET_KEY", default="local-secret-key")
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ------------------------------------------------------------------------------
# CACHING CONFIGURATION
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

# ------------------------------------------------------------------------------
# DEBUG TOOLBAR CONFIGURATION
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # Example if profiling panel is incompatible with your local python:
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# Internal IPs Configuration
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# Docker-specific IP configuration
if env("USE_DOCKER", default="no") == "yes":
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# ------------------------------------------------------------------------------
# DEVELOPMENT TOOLS
# ------------------------------------------------------------------------------
# Django Extensions
INSTALLED_APPS += ["django_extensions"]

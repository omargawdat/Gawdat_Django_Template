# ruff: noqa: F405

import socket

from .base import *  # noqa

print("loading local settings")

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
DEBUG = True
ALLOWED_HOSTS = ["*"]
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
INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# ------------------------------------------------------------------------------
# DEVELOPMENT TOOLS
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]

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
# EMAIL CONFIGURATION (Development - Console Output)
# ------------------------------------------------------------------------------
# Print emails to console instead of sending via SMTP (no rate limits!)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ------------------------------------------------------------------------------
# CORS & CSRF CONFIGURATION
# ------------------------------------------------------------------------------
# Note: CORS and CSRF settings are configured in base.py using environment variables
# Local development uses the same configuration as production, just with different
# environment variable values (localhost URLs, no cookie domain, etc.)
# See: dummy.env for local development configuration examples

# CSRF settings for local development (direct frontend-to-backend)
CSRF_COOKIE_SAMESITE = "Lax"  # Lax for OAuth compatibility
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read the CSRF cookie
# Note: CSRF_TRUSTED_ORIGINS now configured in base.py from env.frontend_allowed_origins

# Session cookie settings for local development
SESSION_COOKIE_SAMESITE = "Lax"  # Lax for OAuth compatibility

# Disable CSRF for allauth headless API endpoints in local development
# This is necessary because:
# 1. Frontend runs on localhost:3000, backend on localhost:8000
# 2. Different ports = different origins for browser security
# 3. JavaScript on :3000 cannot read cookies set by :8000
# 4. Therefore frontend can't send X-CSRFToken header
# 5. In production, use same domain or proper CSRF handling

# Exempt allauth endpoints from CSRF checking (local development only)
CSRF_EXEMPT_URLS = [r"^/api/_allauth/"]

# Add CSRF exempt middleware before CSRF middleware
MIDDLEWARE.insert(
    MIDDLEWARE.index("django.middleware.csrf.CsrfViewMiddleware"),
    "config.middleware.csrf_exempt.CSRFExemptMiddleware",
)

# ruff: noqa: F405

from .base import *  # noqa

# ------------------------------------------------------------------------------
# CORE TEST SETTINGS
# ------------------------------------------------------------------------------
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# ------------------------------------------------------------------------------
# SECURITY AND AUTHENTICATION
# ------------------------------------------------------------------------------
# Use fast password hashing for tests
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# ------------------------------------------------------------------------------
# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
# Store emails in memory for testing
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# ------------------------------------------------------------------------------
# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# Enable template debugging during tests
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

# ------------------------------------------------------------------------------
# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# Use a test server for media files
MEDIA_URL = "http://media.testserver"

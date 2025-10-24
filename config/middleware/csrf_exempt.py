"""Middleware to exempt specific URLs from CSRF protection."""

import re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CSRFExemptMiddleware(MiddlewareMixin):
    """Exempt specific URL patterns from CSRF validation."""

    def process_request(self, request):
        """Mark request as CSRF exempt if URL matches configured patterns."""
        if hasattr(settings, "CSRF_EXEMPT_URLS"):
            path = request.path_info.lstrip("/")
            for pattern in settings.CSRF_EXEMPT_URLS:
                if re.match(pattern, f"/{path}"):
                    request._dont_enforce_csrf_checks = True
                    break

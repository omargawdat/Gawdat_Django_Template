"""Middleware to check user profile completion status."""

import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class ProfileCompletionMiddleware(MiddlewareMixin):
    """
    Middleware to enforce profile completion for authenticated users.

    This middleware checks if authenticated users have completed their profile
    by checking if they have a related profile (customer, adminuser). If not,
    it blocks access to protected endpoints except for:
    - Profile completion endpoints
    - Profile status check
    - Allauth endpoints
    - Admin endpoints
    - Static/media files
    - API schema/docs

    Usage:
        Add to MIDDLEWARE in settings:
        MIDDLEWARE = [
            ...
            'apps.users.middleware.ProfileCompletionMiddleware',
        ]
    """

    # Paths that don't require profile completion
    EXEMPT_PATHS = [
        "/api/users/complete-profile/",
        "/api/users/profile-status/",
        "/_allauth/",
        "/admin/",
        "/api/schema/",
        "/api/docs/",
        "/media/",
        "/static/",
        "/i18n/",
    ]

    def process_request(self, request):
        """
        Check if user needs to complete profile before accessing protected endpoints.

        Returns:
            None: Allow request to proceed
            JsonResponse: Block request with 403 error
        """
        # Skip check for non-API requests or exempt paths
        if not request.path.startswith("/api/"):
            return None

        for exempt_path in self.EXEMPT_PATHS:
            if request.path.startswith(exempt_path):
                return None

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return None  # Let authentication middleware handle this

        # Check if user has completed profile by checking for related profiles
        has_profile = hasattr(request.user, "customer") or hasattr(
            request.user, "adminuser"
        )

        if not has_profile:
            logger.warning(
                f"User {request.user.email} attempted to access {request.path} "
                f"without completing profile"
            )

            return JsonResponse(
                {
                    "error": "Profile incomplete",
                    "message": "Please complete your profile before accessing this resource",
                    "action_required": "complete_profile",
                    "endpoint": "/api/users/complete-profile/",
                },
                status=403,
            )

        return None

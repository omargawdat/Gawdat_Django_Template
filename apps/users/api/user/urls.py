# JWT authentication URLs have been removed.
# Authentication is now handled by django-allauth headless at /api/_allauth/
# See: https://docs.allauth.org/en/latest/headless/openapi-specification.html

from django.urls import path

from apps.users.api.user.views import CheckEmailExistsView

urlpatterns = [
    path("check-email/", CheckEmailExistsView.as_view(), name="check-email-exists"),
]

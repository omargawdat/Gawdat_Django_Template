"""URLs for customer profile completion endpoints."""

from django.urls import path

from .views import CustomerProfileCompletionView
from .views import ProfileStatusView

urlpatterns = [
    path(
        "complete-profile/",
        CustomerProfileCompletionView.as_view(),
        name="complete-profile",
    ),
    path("profile-status/", ProfileStatusView.as_view(), name="profile-status"),
]

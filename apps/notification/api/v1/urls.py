from django.urls import include
from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from apps.notification.api.v1 import views

router = DefaultRouter()
router.register("devices", FCMDeviceAuthorizedViewSet, basename="fcmdevice")

urlpatterns = [
    path("", include(router.urls)),
    path("notifications/", views.NotificationListView.as_view(), name="list_notifications"),
    path(
        "notifications/<int:pk>/",
        views.NotificationDeleteView.as_view(),
        name="delete_notification",
    ),
    path(
        "notifications/bulk-delete/",
        views.NotificationBulkDeleteView.as_view(),
        name="delete_all_notifications",
    ),
]

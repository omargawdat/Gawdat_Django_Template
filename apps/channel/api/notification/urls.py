from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.channel.api.notification import views
from apps.channel.api.notification.views import CustomFCMDeviceViewSet

router = DefaultRouter()
router.register("devices", CustomFCMDeviceViewSet, basename="fcmdevice")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "notifications/",
        views.NotificationListView.as_view(),
        name="notifications-list",
    ),
    path(
        "notifications/<int:notification_id>/",
        views.NotificationDeleteView.as_view(),
        name="notifications-delete",
    ),
    path(
        "notifications/bulk-delete/",
        views.NotificationBulkDeleteView.as_view(),
        name="notifications-bulk-delete",
    ),
]

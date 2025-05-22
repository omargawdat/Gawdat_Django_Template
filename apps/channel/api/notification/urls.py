from django.urls import include
from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

from apps.channel.api.notification import views

router = DefaultRouter()
router.register("devices", FCMDeviceAuthorizedViewSet, basename="fcmdevice")

urlpatterns = [
    path("/", include(router.urls)),
    path(
        "notifications/",
        views.NotificationListView.as_view(),
        name="notifications-list",
    ),
    path(
        "notifications/<int:pk>/",
        views.NotificationDeleteView.as_view(),
        name="notifications-delete",
    ),
    path(
        "notifications/bulk-delete/",
        views.NotificationBulkDeleteView.as_view(),
        name="notifications-bulk-delete",
    ),
]

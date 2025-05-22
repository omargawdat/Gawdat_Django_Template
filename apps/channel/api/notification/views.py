from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.channel.api.notification.serializers import NotificationDetailedSerializer
from apps.channel.domain.selectors.notification import NotificationSelector
from apps.channel.models.notification import Notification

from .pagination import NotificationCursorPagination


@extend_schema(
    tags=["FCM/Devices"],
)
class CustomFCMDeviceViewSet(FCMDeviceAuthorizedViewSet):
    pass


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationCursorPagination

    @extend_schema(
        tags=["FCM/Notification"],
        operation_id="listNotifications",
        responses={200: NotificationDetailedSerializer(many=True)},
    )
    def get(self, request):
        queryset = NotificationSelector.get_notifications_by_user(request.user)

        # Apply pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)

        # Serialize the paginated data
        serializer = NotificationDetailedSerializer(paginated_queryset, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class NotificationDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["FCM/Notification"],
        operation_id="deleteNotification",
        responses={204: None},
    )
    def delete(self, request, pk):
        notification = get_object_or_404(Notification, id=pk, users=request.user)
        notification.users.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationBulkDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["FCM/Notification"],
        operation_id="bulkDeleteNotifications",
        responses={204: None},
    )
    def delete(self, request):
        notifications = Notification.objects.filter(users=request.user)
        for notification in notifications:
            notification.users.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

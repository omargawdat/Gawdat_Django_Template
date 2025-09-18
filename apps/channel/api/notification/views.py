from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationCursorPagination

    @extend_schema(
        tags=["FCM/Notification"],
        operation_id="listNotifications",
        responses={200: NotificationDetailedSerializer(many=True)},
    )
    def get(self, request):
        queryset = NotificationSelector.get_notifications_by_user(request.user)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)

        serializer = NotificationDetailedSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)


class NotificationDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["FCM/Notification"],
        operation_id="deleteNotification",
        responses={204: None},
    )
    def delete(self, request, notification_id):
        notification = get_object_or_404(
            Notification, id=notification_id, users=request.user
        )
        notification.users.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationBulkDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
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


class NotificationMarkAsReadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["FCM/Notification"],
        operation_id="markNotificationAsRead",
        request=None,
        responses={
            200: OpenApiResponse(description="All notifications marked as read")
        },
    )
    def post(self, request):
        Notification.objects.filter(users=request.user, is_read=False).update(
            is_read=True
        )
        return Response(
            {"message": "All notifications marked as read"}, status=status.HTTP_200_OK
        )

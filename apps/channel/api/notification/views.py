from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.channel.api.notification.serializers import NotificationDetailedSerializer
from apps.channel.domain.selectors.notification import NotificationSelector
from apps.channel.models.notification import Notification

from .pagination import NotificationCursorPagination


class NotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationDetailedSerializer
    pagination_class = NotificationCursorPagination

    def get_queryset(self):
        return NotificationSelector.get_notifications_by_user(self.request.user)


class NotificationDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        notification = get_object_or_404(Notification, id=pk, users=request.user)
        notification.users.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationBulkDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        notifications = Notification.objects.filter(users=request.user)
        for notification in notifications:
            notification.users.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

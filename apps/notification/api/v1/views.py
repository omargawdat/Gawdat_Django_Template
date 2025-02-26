from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notification.models.notification import Notification

from .serializers import NotificationOutputSerializer


class NotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationOutputSerializer

    def get_queryset(self):
        return Notification.objects.filter(users=self.request.user)


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

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.domain.services.user import UserServices


class LogoutView(GenericAPIView):
    def post(self, request):
        user = request.user
        UserServices.user_logout_all_devices(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

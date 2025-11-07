from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.user.serializers import CheckEmailSerializer
from apps.users.api.user.serializers import EmailExistsResponseSerializer
from apps.users.models.user import User


class CheckEmailExistsView(APIView):
    """Check if a user exists with the given email."""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication/Account"],
        operation_id="CheckEmailExists",
        description="Check if a user account exists with the provided email address.",
        request=CheckEmailSerializer,
        responses={
            200: EmailExistsResponseSerializer,
            400: {"description": "Invalid email format"},
        },
    )
    def post(self, request):
        """Check if user exists by email."""
        serializer = CheckEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        exists = User.objects.filter(email=email).exists()

        return Response(
            {"exists": exists, "email": email},
            status=status.HTTP_200_OK,
        )

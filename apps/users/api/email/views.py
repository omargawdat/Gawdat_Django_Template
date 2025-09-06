from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.email.serializers import CheckEmailSerializer
from apps.users.models.customer import Customer


class CheckEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CheckEmailSerializer

    @extend_schema(
        tags=["User/Email"],
        operation_id="checkEmail",
        description="Check if an email is registered, verified, and has a password set.",
        request=CheckEmailSerializer,
        responses={
            200: OpenApiResponse(
                description="Email is registered",
                response={
                    "properties": {
                        "is_registered": {"type": "boolean", "example": True},
                        "is_verified": {"type": "boolean", "example": True},
                        "has_password": {"type": "boolean", "example": True},
                    }
                },
            ),
            404: OpenApiResponse(
                description="Email is not registered",
                response={
                    "properties": {
                        "is_registered": {"type": "boolean", "example": False},
                        "is_verified": {"type": "boolean", "example": False},
                        "has_password": {"type": "boolean", "example": False},
                    }
                },
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            customer = Customer.objects.get(email=email)
            return Response(
                {
                    "is_registered": True,
                    "is_verified": customer.is_verified,
                    "has_password": bool(customer.password),
                },
                status=status.HTTP_200_OK,
            )

        except Customer.DoesNotExist:
            return Response(
                {"is_registered": False, "is_verified": False, "has_password": False},
                status=status.HTTP_404_NOT_FOUND,
            )

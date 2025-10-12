from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.api.customer.serializers import CustomerDetailedSerializer
from apps.users.api.customer.serializers import CustomerUpdateSerializer
from apps.users.domain.services.user import UserServices


class CustomerUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Profile"],
        operation_id="UpdateCustomer",
        description="Update the authenticated customer's profile information.",
        parameters=[
            OpenApiParameter(
                name="Accept-Language",
                type=OpenApiTypes.STR,
                location="header",
                required=False,
                description="Language preference for the response",
                examples=[
                    OpenApiExample(
                        name="English (US)",
                        value="en",
                        description="English with US locale preference",
                    ),
                ],
            ),
        ],
        request={
            "multipart/form-data": CustomerUpdateSerializer,
        },
        examples=[
            OpenApiExample(
                name="Complete Profile Update",
                description="Update all profile fields including image",
                value={
                    "fullName": "Mezo Doe",
                    "email": "john.doe@example.com",
                    "birthDate": "2011-01-02",
                    "primaryAddress": "1",
                    "gender": "M",
                    "language": "en",
                    "image": "default_image.png",
                    "country": "SA",
                },
                request_only=True,
                media_type="multipart/form-data",
            )
        ],
        responses={
            200: CustomerDetailedSerializer,
            400: OpenApiResponse(
                description="Validation Error",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Validation Error",
                        value={
                            "field_name": ["Error message for this field"],
                            "image": ["File size should not exceed 5MB"],
                        },
                        response_only=True,
                    )
                ],
            ),
        },
    )
    def patch(self, request):
        serializer = CustomerUpdateSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            CustomerDetailedSerializer(request.user, context={"request": request}).data
        )


class CustomerDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Profile"],
        operation_id="GetCustomerDetails",
        responses={
            200: CustomerDetailedSerializer,
        },
    )
    def get(self, request):
        customer = request.user
        serializer = CustomerDetailedSerializer(customer, context={"request": request})
        return Response(serializer.data)


class CustomerDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Profile"],
        operation_id="DeleteCustomer",
        parameters=[
            OpenApiParameter(
                name="Accept-Language",  # todo: it should be for all endpoints
                type=OpenApiTypes.STR,
                location="header",
                required=False,
                description="Language preference for the response",
                examples=[
                    OpenApiExample(
                        name="English (US)",
                        value="en",
                        description="English with US locale preference",
                    ),
                ],
            ),
        ],
        responses={
            204: OpenApiResponse(description="Account successfully deactivated."),
        },
    )
    def delete(self, request):
        customer = request.user
        customer.is_active = False
        UserServices.user_logout_all_devices(customer)
        customer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

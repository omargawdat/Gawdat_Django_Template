from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.location.domain.selector.address import AddressSelector

from ...domain.validators.address import AddressValidator
from ...domain.validators.region import RegionValidator
from .serializers import AddressCreateSerializer
from .serializers import AddressDetailedSerializer
from .serializers import AddressUpdateSerializer


class AddressListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Location/Address"],
        operation_id="ListAddresses",
        responses={200: AddressDetailedSerializer(many=True)},
    )
    def get(self, request):
        queryset = AddressSelector.get_all_customer_addresses(customer=request.user)
        serializer = AddressDetailedSerializer(queryset, many=True)
        return Response(serializer.data)


class AddressCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Location/Address"],
        operation_id="CreateAddress",
        request={"multipart/form-data": AddressCreateSerializer},
        responses={201: AddressDetailedSerializer},
        examples=[
            # todo: this code isn't loaded correctly into apidog but working in postman  so just keep it to know how to deal with example values in form-data requests
            OpenApiExample(
                "Create Address Example",
                value={
                    "point": '{"type": "Point", "coordinates": [31.235712, 30.044420]}',
                    "description": "My home address",
                    "map_description": "Near the main square",
                    "location_type": "home",
                    "map_image": "select a file",
                },
                media_type="multipart/form-data",
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = AddressCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        point = serializer.validated_data["point"]

        RegionValidator.validate_user_location(point=point, user=user)

        address = serializer.save(customer=user)
        user.primary_address = address
        user.save()

        detailed_serializer = AddressDetailedSerializer(address)
        return Response(detailed_serializer.data, status=status.HTTP_201_CREATED)


class AddressUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Location/Address"],
        operation_id="UpdateAddress",
        request={"multipart/form-data": AddressUpdateSerializer},
        responses={200: AddressDetailedSerializer},
    )
    def patch(self, request, address_id):
        user_addresses = AddressSelector.get_all_customer_addresses(
            customer=request.user
        )
        address = get_object_or_404(user_addresses, pk=address_id)

        serializer = AddressUpdateSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # [EXPLAIN]: as the endpoint is patch so point is optional to update
        if "point" in serializer.validated_data:
            point = serializer.validated_data["point"]
            RegionValidator.validate_user_location(point=point, user=request.user)

        address = serializer.save()

        detailed_serializer = AddressDetailedSerializer(address)
        return Response(detailed_serializer.data)


class AddressDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Location/Address"],
        operation_id="DeleteAddress",
        responses={
            204: OpenApiResponse(description="Address successfully deleted"),
            404: OpenApiResponse(description="Address not found"),
        },
    )
    def delete(self, request, address_id):
        queryset = AddressSelector.get_all_customer_addresses(customer=request.user)

        address = get_object_or_404(queryset, pk=address_id)

        AddressValidator.validate_not_primary_address(
            address=address, customer=request.user
        )

        address.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.location.domain.selector.address import AddressSelector

from ...domain.validators.address import AddressValidator
from ...domain.validators.region import RegionValidator
from ...models.address import Address
from .serializers import AddressCreateSerializer
from .serializers import AddressDetailedSerializer
from .serializers import AddressUpdateSerializer


@extend_schema(
    tags=["Location/Address"],
    operation_id="ListAddresses",
    responses={200: AddressDetailedSerializer(many=True)},
)
class AddressListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressDetailedSerializer

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)


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
class AddressCreateView(APIView):
    permission_classes = []
    parser_classes = [MultiPartParser]

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


@extend_schema(
    tags=["Location/Address"],
    operation_id="UpdateAddress",
    request=AddressUpdateSerializer,
    responses={200: AddressDetailedSerializer},
)
class AddressUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)

    def patch(self, request, pk, *args, **kwargs):
        address = get_object_or_404(Address, pk=pk)
        serializer = AddressUpdateSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # [EXPLAIN]: as the endpoint is patch so point is optional to update
        if "point" in serializer.validated_data:
            point = serializer.validated_data["point"]
            RegionValidator.validate_user_location(point=point, user=user)

        address = serializer.save()

        detailed_serializer = AddressDetailedSerializer(address)
        return Response(detailed_serializer.data)


@extend_schema(
    tags=["Location/Address"],
    operation_id="DeleteAddress",
    responses={204: None},
)
class AddressDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)

    def perform_destroy(self, instance):
        AddressValidator.validate_not_primary_address(
            address=instance, customer=self.request.user
        )
        super().perform_destroy(instance)

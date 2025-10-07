from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.utils import OpenApiTypes
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
        tags=["Account/Address"],
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
        tags=["Account/Address"],
        operation_id="CreateAddress",
        request={"multipart/form-data": AddressCreateSerializer},
        examples=[
            OpenApiExample(
                name="Create Address Example",
                description="An example of creating a new address.",
                value={
                    "country": "SA",
                    "point": {"type": "Point", "coordinates": [45.0792, 23.8859]},
                    "description": "123 Main St, Springfield, USA",
                    "mapDescription": "Near the big park",
                    "locationType": "HOME",
                    "mapImage": "map_image.png",
                },
                request_only=True,
                media_type="multipart/form-data",
            )
        ],
        responses={201: AddressDetailedSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = AddressCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        country = serializer.validated_data["country"]
        point = serializer.validated_data["point"]

        RegionValidator.validate_country_for_address(country=country, point=point)

        address = serializer.save(customer=user)
        user.primary_address = address
        user.save()

        detailed_serializer = AddressDetailedSerializer(address)
        return Response(detailed_serializer.data, status=status.HTTP_201_CREATED)


class AddressRetrieveView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Address"],
        operation_id="RetrieveAddress",
        parameters=[
            OpenApiParameter(
                name="address_id",
                description="ID of the address to retrieve",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: AddressDetailedSerializer,
            404: OpenApiResponse(description="Address not found"),
        },
    )
    def get(self, request, address_id):
        user_addresses = AddressSelector.get_all_customer_addresses(
            customer=request.user
        )
        address = get_object_or_404(user_addresses, pk=address_id)
        serializer = AddressDetailedSerializer(address)
        return Response(serializer.data)


class AddressUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Address"],
        operation_id="UpdateAddress",
        parameters=[
            OpenApiParameter(
                name="address_id",
                description="ID of the address to update",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            )
        ],
        request={"multipart/form-data": AddressUpdateSerializer},
        examples=[
            OpenApiExample(
                "Update Address Example",
                summary="Update Address Example",
                description="An example of updating an address.",
                value={
                    "country": "SA",
                    "point": {"type": "Point", "coordinates": [45.0792, 23.8859]},
                    "description": "123 Main St, Springfield, USA",
                    "mapDescription": "Near the big park",
                    "locationType": "HOME",
                    "mapImage": "map_image.png",
                },
                request_only=True,
            )
        ],
        responses={200: AddressDetailedSerializer},
    )
    def patch(self, request, address_id):
        user_addresses = AddressSelector.get_all_customer_addresses(
            customer=request.user
        )
        address = get_object_or_404(user_addresses, pk=address_id)

        serializer = AddressUpdateSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # [EXPLAIN]: as the endpoint is patch so country and point are optional to update
        if (
            "country" in serializer.validated_data
            or "point" in serializer.validated_data
        ):
            country = serializer.validated_data.get("country", address.country)
            point = serializer.validated_data.get("point", address.point)
            RegionValidator.validate_country_for_address(country=country, point=point)

        address = serializer.save()

        detailed_serializer = AddressDetailedSerializer(address)
        return Response(detailed_serializer.data)


class AddressDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Account/Address"],
        operation_id="DeleteAddress",
        parameters=[
            OpenApiParameter(
                name="address_id",
                description="ID of the address to delete",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            )
        ],
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

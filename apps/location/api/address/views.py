from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
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


class AddressListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressDetailedSerializer

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)


class AddressCreateView(APIView):
    permission_classes = []

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)

    def patch(self, request, pk, *args, **kwargs):
        address = get_object_or_404(Address, pk=pk)
        serializer = AddressUpdateSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if "point" in serializer.validated_data:
            point = serializer.validated_data["point"]
            RegionValidator.validate_user_location(point=point, user=user)

        address = serializer.save()

        detailed_serializer = AddressDetailedSerializer(address)
        return Response(detailed_serializer.data)


class AddressDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)

    def perform_destroy(self, instance):
        AddressValidator.validate_not_primary_address(
            address=instance, customer=self.request.user
        )
        super().perform_destroy(instance)

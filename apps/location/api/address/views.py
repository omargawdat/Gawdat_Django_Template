from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.location.domain.selector.address import AddressSelector
from apps.location.models.address import Address

from ...domain.validators.region import RegionValidator
from .serializers import AddressCreateSerializer
from .serializers import AddressListSerializer
from .serializers import AddressUpdateSerializer


class AddressListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressListSerializer

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)


class AddressCreateView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer
    permission_classes = []

    def perform_create(self, serializer):
        user = self.request.user
        point = serializer.validated_data["point"]

        RegionValidator.validate_user_location(point=point, user=user)
        address = serializer.save(customer=user)
        user.primary_address = address
        user.save()


class AddressUpdateView(generics.UpdateAPIView):
    serializer_class = AddressUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        point = serializer.validated_data["point"]

        RegionValidator.validate_user_location(point=point, user=user)
        serializer.save()


class AddressDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddressSelector.get_all_customer_addresses(customer=self.request.user)

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...domain.selector.cart_item import CartItemSelector
from ...domain.services.cart_item import CartItemService
from ...models.cart import Cart
from .serializers import CartItemCreateSerializer
from .serializers import CartItemListSerializer
from .serializers import CartItemMinimalSerializer
from .serializers import CartItemUpdateSerializer


class CartItemListAPIView(generics.ListAPIView):
    serializer_class = CartItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItemSelector.get_cart_items(customer=self.request.user.customer)


class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        cart = Cart.objects.get(customer=user)
        product = serializer.validated_data["product"]

        cart_item = CartItemService.create_cart_item(
            cart=cart, product=product, quantity=1
        )

        response_serializer = CartItemMinimalSerializer(cart_item)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CartItemUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CartItemUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItemSelector.get_cart_items(customer=self.request.user.customer)


class CartItemDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItemSelector.get_cart_items(customer=self.request.user.customer)

from rest_framework import serializers

from apps.cart.models.cart_item import CartItem


class CartItemMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "quantity",
            "product",
            "created_at",
        ]


class CartItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            *CartItemMinimalSerializer.Meta.fields,
        ]


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product"]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

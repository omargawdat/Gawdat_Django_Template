from decimal import Decimal

from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.payment.models.wallet import Wallet


class WalletMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["balance", "balance_currency", "is_use_wallet_in_payment"]


class WalletDetailedSerializer(WalletMinimalSerializer):
    class Meta(WalletMinimalSerializer.Meta):
        fields = WalletMinimalSerializer.Meta.fields


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Enable Wallet",
            value={"is_use_wallet_in_payment": True},
        ),
    ]
)
class WalletUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["is_use_wallet_in_payment"]


class WalletRechargeSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("1.00")
    )

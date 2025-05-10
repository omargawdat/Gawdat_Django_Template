from rest_framework import serializers

from apps.payment.models.wallet import Wallet
from apps.payment.models.wallet_transaction import WalletTransaction


class WalletMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["balance", "balance_currency", "is_use_wallet_in_payment"]


class WalletDetailedSerializer(WalletMinimalSerializer):
    class Meta(WalletMinimalSerializer.Meta):
        fields = WalletMinimalSerializer.Meta.fields


class WalletUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["is_use_wallet_in_payment"]


class WalletTransactionMinimalSerializer(serializers.ModelSerializer):
    transaction_type_display = serializers.SerializerMethodField()

    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "transaction_type",
            "transaction_type_display",
            "amount",
            "created_at",
            "action_by",
            "transaction_note",
            "attachment",
        ]

    def get_transaction_type_display(self, obj):
        return obj.get_transaction_type_display()


class WalletTransactionDetailedSerializer(WalletTransactionMinimalSerializer):
    class Meta(WalletTransactionMinimalSerializer.Meta):
        fields = WalletTransactionMinimalSerializer.Meta.fields

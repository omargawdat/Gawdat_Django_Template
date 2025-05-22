from rest_framework import serializers

from apps.payment.models.wallet_transaction import WalletTransaction


class WalletTransactionMinimalSerializer(serializers.ModelSerializer):
    transaction_type_text = serializers.SerializerMethodField()

    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "transaction_type",
            "transaction_type_text",
            "amount",
            "created_at",
        ]

    def get_transaction_type_text(self, obj) -> str:
        return obj.get_transaction_type_display()


class WalletTransactionDetailedSerializer(WalletTransactionMinimalSerializer):
    class Meta(WalletTransactionMinimalSerializer.Meta):
        fields = WalletTransactionMinimalSerializer.Meta.fields

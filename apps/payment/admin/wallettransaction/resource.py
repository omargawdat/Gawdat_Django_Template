from import_export import resources

from apps.payment.models.wallet_transaction import WalletTransaction


class WalletTransactionResource(resources.ModelResource):
    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "customer",
            "amount",
            "transaction_type",
            "created_at",
            "action_by",
        ]

from import_export import resources

from apps.payment.models.wallet import Wallet


class WalletResource(resources.ModelResource):
    class Meta:
        model = Wallet
        fields = []

from import_export import resources

from apps.payment.models.wallet import Wallet


class WalletResource(resources.ModelResource):
    class Meta:
        model = Wallet
        fields = ("user", "balance", "is_use_wallet_in_payment", "last_update")

    def dehydrate_user(self, wallet: Wallet):
        return str(wallet.user.username)

    def dehydrate_balance(self, wallet: Wallet):
        return f"{wallet.balance.amount} {wallet.balance.currency}"

    def dehydrate_is_use_wallet_in_payment(self, wallet: Wallet):
        return "Yes" if wallet.is_use_wallet_in_payment else "No"

    def dehydrate_last_update(self, wallet: Wallet):
        return wallet.last_update.strftime("%Y-%m-%d %H:%M:%S")

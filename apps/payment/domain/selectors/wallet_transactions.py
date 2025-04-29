from apps.payment.models.wallet_transaction import WalletTransaction
from apps.users.models.user import User


class WalletTransactionSelector:
    @staticmethod
    def user_wallet_transactions(user: User) -> list[WalletTransaction]:
        return WalletTransaction.objects.filter(wallet__user=user)

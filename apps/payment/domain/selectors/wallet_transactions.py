from django.db.models import Sum
from django.utils import timezone

from apps.payment.constants import WalletTransactionType
from apps.payment.models.wallet_transaction import WalletTransaction
from apps.users.models.user import User

# Transaction types that add money to wallet
CREDIT_TYPES = [
    WalletTransactionType.REFUND,
    WalletTransactionType.CHARGING,
    WalletTransactionType.CANCEL_ORDER,
    WalletTransactionType.SHARE,
    WalletTransactionType.CASH_RECEIVE,
    WalletTransactionType.REFERRAL,
    WalletTransactionType.REFERRAL_APP_INSTALL_INVITER,
    WalletTransactionType.REFERRAL_APP_INSTALL_INVITEE,
    WalletTransactionType.REFERRAL_ORDER_INVITER,
    WalletTransactionType.REFERRAL_ORDER_INVITEE,
]

# Transaction types that deduct money from wallet
DEBIT_TYPES = [
    WalletTransactionType.FINE,
    WalletTransactionType.PAYOUT,
    WalletTransactionType.ORDER_PAYMENT,
]


class WalletTransactionSelector:
    @staticmethod
    def user_wallet_transactions(user: User) -> list[WalletTransaction]:
        return WalletTransaction.objects.filter(wallet__user=user)

    @staticmethod
    def get_transactions_today() -> int:
        """Count of transactions created today."""
        today = timezone.now().date()
        return WalletTransaction.objects.filter(created_at__date=today).count()

    @staticmethod
    def get_money_added_today() -> str:
        """Sum of credit transactions today."""
        today = timezone.now().date()
        result = WalletTransaction.objects.filter(
            created_at__date=today,
            transaction_type__in=CREDIT_TYPES,
        ).aggregate(total=Sum("amount"))
        total = result["total"]
        if total is None:
            return "0.00 SAR"
        return f"{total:,.2f} SAR"

    @staticmethod
    def get_money_deducted_today() -> str:
        """Sum of debit transactions today."""
        today = timezone.now().date()
        result = WalletTransaction.objects.filter(
            created_at__date=today,
            transaction_type__in=DEBIT_TYPES,
        ).aggregate(total=Sum("amount"))
        total = result["total"]
        if total is None:
            return "0.00 SAR"
        return f"{total:,.2f} SAR"

    @staticmethod
    def get_net_change_today() -> str:
        """Net balance change today (added - deducted)."""
        today = timezone.now().date()
        today_transactions = WalletTransaction.objects.filter(created_at__date=today)

        added = (
            today_transactions.filter(transaction_type__in=CREDIT_TYPES).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        deducted = (
            today_transactions.filter(transaction_type__in=DEBIT_TYPES).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        net = float(added) - float(deducted)
        sign = "+" if net >= 0 else ""
        return f"{sign}{net:,.2f} SAR"

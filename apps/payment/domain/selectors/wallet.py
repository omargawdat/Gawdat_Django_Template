from django.db.models import Avg
from django.db.models import Sum

from apps.payment.models.wallet import Wallet


class WalletSelector:
    @staticmethod
    def get_total_balance() -> str:
        """Sum of all wallet balances."""
        result = Wallet.objects.aggregate(total=Sum("balance"))
        total = result["total"]
        if total is None:
            return "0.00 SAR"
        return f"{total:,.2f} SAR"

    @staticmethod
    def get_average_balance() -> str:
        """Average balance per wallet."""
        result = Wallet.objects.aggregate(avg=Avg("balance"))
        avg = result["avg"]
        if avg is None:
            return "0.00 SAR"
        return f"{float(avg):,.2f} SAR"

    @staticmethod
    def get_wallet_usage_rate() -> str:
        """Percentage of wallets with is_use_wallet_in_payment=True."""
        total = Wallet.objects.count()
        if total == 0:
            return "0%"
        using_wallet = Wallet.objects.filter(is_use_wallet_in_payment=True).count()
        rate = (using_wallet / total) * 100
        return f"{rate:.0f}%"

    @staticmethod
    def get_active_wallets_count() -> int:
        """Count of wallets with balance > 0."""
        return Wallet.objects.filter(balance__gt=0).count()

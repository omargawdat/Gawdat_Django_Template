from django.contrib.auth.models import User
from django.core.files.base import File
from djmoney.money import Money

from apps.payment.models.wallet import Wallet
from apps.payment.models.wallet_transaction import WalletTransaction


class WalletTransactionService:
    @staticmethod
    def create_transaction(
        *,
        wallet: Wallet,
        amount: Money,
        transaction_type: str,
        transaction_note="SYSTEM ACTION",
        action_by: User | None = None,
        attachment: File | None = None,
    ) -> WalletTransaction:
        # [Important]: Update wallet balance directly with the amount (positive or negative)
        wallet.balance += amount
        wallet.save()

        return WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=transaction_type,
            amount=amount,
            action_by=action_by,
            transaction_note=transaction_note,
            attachment=attachment,
        )

from django.contrib.auth.models import User
from django.core.files.base import File
from djmoney.money import Money

from apps.channel.constants import NotificationType
from apps.channel.domain.services.notification import NotificationService
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
        notification_type: NotificationType | None = None,
    ) -> WalletTransaction:
        # [Important]: Update wallet balance directly with the amount (positive or negative)
        wallet.balance += amount
        wallet.save()

        transaction = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=transaction_type,
            amount=amount,  # Positive for credit, negative for debit
            action_by=action_by,
            transaction_note=transaction_note,
            attachment=attachment,
        )

        if amount.amount > 0 and not notification_type:
            notification_type = NotificationType.MONEY_ADDED

        if notification_type:
            NotificationService.create_action_notifications(
                users=[wallet.user],
                notification_type=notification_type,
                send_fcm=True,
                send_sms=False,
                amount=str(amount),
                new_balance=str(wallet.balance),
            )
        return transaction

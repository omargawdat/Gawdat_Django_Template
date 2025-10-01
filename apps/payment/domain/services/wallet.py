import logging

from djmoney.models.fields import Money

from apps.channel.constants import NotificationType
from apps.payment.constants import ReferralType
from apps.payment.constants import WalletTransactionType
from apps.payment.domain.services.wallet_transaction import WalletTransactionService
from apps.payment.models.wallet import Wallet
from apps.users.models.customer import Customer

logger = logging.getLogger(__name__)


class WalletService:
    @staticmethod
    def create_wallet_for_customer(user: Customer, currency: str) -> Wallet:
        wallet = Wallet.objects.create(
            user=user,
            balance=Money(0, currency),
            is_use_wallet_in_payment=False,
        )
        return wallet

    @staticmethod
    def add_referral_points(
        *,
        inviter_customer: Customer,
        invitee_customer: Customer,
        referral_type: ReferralType,
    ) -> None:
        if not inviter_customer or not inviter_customer:
            return

        if invitee_customer.id == inviter_customer.id:
            return

        referrer_wallet = Wallet.objects.get(user=inviter_customer)
        invitee_wallet = Wallet.objects.get(user=invitee_customer)

        country = inviter_customer.country

        if referral_type == ReferralType.APP_INSTALL:
            inviter_amount = country.app_install_money_inviter
            invitee_amount = country.app_install_money_invitee
            inviter_transaction_type = (
                WalletTransactionType.REFERRAL_APP_INSTALL_INVITER
            )
            invitee_transaction_type = (
                WalletTransactionType.REFERRAL_APP_INSTALL_INVITEE
            )
            notification_type = NotificationType.REFERRAL_APP_INSTALL
        elif referral_type == ReferralType.FIRST_ORDER:
            inviter_amount = country.order_money_inviter
            invitee_amount = country.order_money_invitee
            inviter_transaction_type = WalletTransactionType.REFERRAL_ORDER_INVITER
            invitee_transaction_type = WalletTransactionType.REFERRAL_ORDER_INVITEE
            notification_type = NotificationType.REFERRAL_FIRST_ORDER
        else:
            logger.error(f"Unknown referral type: {referral_type}")
            return

        if invitee_amount.amount > 0:
            WalletTransactionService.create_transaction(
                wallet=referrer_wallet,
                amount=invitee_amount,
                transaction_type=inviter_transaction_type,
                notification_type=notification_type,
            )

        if inviter_amount.amount > 0:
            WalletTransactionService.create_transaction(
                wallet=invitee_wallet,
                amount=inviter_amount,
                transaction_type=invitee_transaction_type,
                notification_type=notification_type,
            )

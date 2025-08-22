import logging

from djmoney.models.fields import Money

from apps.location.models.country import Country
from apps.payment.constants import WalletTransactionType
from apps.payment.domain.services.wallet_transaction import WalletTransactionService
from apps.payment.models.wallet import Wallet
from apps.users.models.customer import Customer
from apps.users.models.user import User

logger = logging.getLogger(__name__)


class WalletService:
    @staticmethod
    def create_wallet_for_user(user: User) -> Wallet:
        country = Country.objects.get(pk="UNSELECTED")  # TODO remove it
        # country = CountrySelector.country_by_phone(user.phone_number)
        currency = country.currency

        wallet = Wallet.objects.create(
            user=user,
            balance=Money(0, currency),
            is_use_wallet_in_payment=False,
        )
        return wallet

    @staticmethod
    def add_referral_points(
        *, referral_customer_id: int, request_customer: Customer
    ) -> None:
        if not referral_customer_id:
            return

        referrer_user = Customer.objects.filter(
            id=referral_customer_id, is_active=True
        ).first()

        if not referrer_user or request_customer.id == referrer_user.id:
            return

        wallet = Wallet.objects.filter(user=referrer_user).first()
        referral_points = referrer_user.country.referral_points
        points = Money(referral_points.amount, wallet.balance.currency)

        WalletTransactionService.create_transaction(
            wallet=wallet,
            amount=points,
            transaction_type=WalletTransactionType.REFERRAL,
        )

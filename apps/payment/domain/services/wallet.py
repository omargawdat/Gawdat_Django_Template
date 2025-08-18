import logging

from djmoney.models.fields import Money

from apps.appInfo.models.system_config import SystemConfig
from apps.location.models.country import Country
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

        if not currency:
            raise ValueError(f"Country {country.code} has no currency set")

        wallet, created = Wallet.objects.get_or_create(
            user=user,
            defaults={
                "balance": Money(0, currency),
                "is_use_wallet_in_payment": False,
            },
        )
        return wallet

    @staticmethod
    def update_wallet_points(*, referral_id: int, request_customer: Customer) -> None:
        referrer_user = Customer.objects.filter(id=referral_id, is_active=True).first()

        if not referrer_user or request_customer.id == referrer_user.id:
            return

        wallet = Wallet.objects.get(user=referrer_user)
        points_value = SystemConfig.get_solo().referral_points

        # Convert the integer points to a Money object with the wallet's currency
        points = Money(points_value, wallet.balance.currency)

        WalletTransactionService.create_transaction(
            wallet=wallet,
            amount=points,
            transaction_type="REFERRAL",
            transaction_note=f"Referral points added for user {referrer_user.id}",
        )

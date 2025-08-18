import logging

from apps.location.models.country import Country
from apps.payment.models.wallet import Wallet
from apps.users.models.user import User

logger = logging.getLogger(__name__)


class WalletService:
    @staticmethod
    def create_wallet_for_user(user: User) -> Wallet:
        country = Country.objects.get(pk="UNSELECTED")  # TODO remove it
        currency = country.currency
        wallet, _ = Wallet.objects.get_or_create(
            user=user,
            defaults={
                "balance": 0,
                "is_use_wallet_in_payment": False,
                "balance_currency": currency,
            },
        )
        return wallet

import logging

from apps.location.domain.selector.country import CountrySelector
from apps.payment.models.wallet import Wallet
from apps.users.models.user import User

logger = logging.getLogger(__name__)


class WalletService:
    @staticmethod
    def create_wallet_for_user(user: User) -> Wallet:
        country = CountrySelector.country_by_phone(user.phone_number)
        currency = country.currency
        return Wallet.objects.create(
            user=user,
            balance=0,
            is_use_wallet_in_payment=False,
            balance_currency=currency,
        )

from rest_framework.exceptions import AuthenticationFailed

from apps.location.models.country import Country
from apps.users.domain.validators.user import UserValidator
from apps.users.models.customer import Customer


class CustomerService:
    @staticmethod
    def get_or_create_active_customer(phone_number: str) -> tuple[Customer, bool]:
        customer, created = Customer.objects.get_or_create(
            user__phone_number=phone_number
        )
        UserValidator.validate_user_is_active(customer.user)
        return customer, created

    @staticmethod
    def create_customer(
        *,
        email: str,
        phone_number: str | None = None,
        username: str,
        password: str | None = None,
    ) -> Customer:
        from apps.payment.domain.services.wallet import WalletService
        from apps.users.models import User

        # The Default country
        country = Country.objects.get(code="SA")

        # Create user first
        user = User.objects.create(
            email=email,
            username=username,
            phone_number=phone_number,
        )
        if password:
            user.set_password(password)
        user.save()

        # Create customer
        customer = Customer(
            user=user,
            country=country,
            is_verified=False,
        )
        customer.full_clean()
        customer.save()

        # Create wallet for new user
        WalletService.create_wallet_for_user(user, country.currency)

        return customer

    @staticmethod
    def change_password(
        *, customer: Customer, old_password: str, new_password: str
    ) -> None:
        if not customer.user.check_password(old_password):
            raise AuthenticationFailed("Old password is incorrect")

        if old_password == new_password:
            raise AuthenticationFailed(
                "New password must be different from the old password"
            )

        customer.user.set_password(new_password)
        customer.user.save()

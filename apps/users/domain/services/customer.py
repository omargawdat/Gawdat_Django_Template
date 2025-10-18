from django.db import transaction
from rest_framework.exceptions import AuthenticationFailed

from apps.channel.data_class import DeviceData
from apps.channel.domain.services.device import DeviceService
from apps.location.domain.selector.country import CountrySelector
from apps.location.models.country import Country
from apps.payment.domain.services.wallet import WalletService
from apps.users.domain.validators.user import UserValidator
from apps.users.models.customer import Customer
from apps.users.models.user import User


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

    @staticmethod
    @transaction.atomic
    def complete_customer_profile(
        *,
        user: User,
        country: Country,
        phone_number: str | None = None,
        language: str | None = None,
        fcm_token: str | None = None,
        device_id: str | None = None,
        device_type: str | None = None,
    ) -> User:
        """Complete customer profile after initial signup."""
        # Update User
        if phone_number:
            user.phone_number = phone_number
            CountrySelector.country_by_phone(phone_number)

        if language:
            user.language = language
        user.save()

        # Create Customer profile
        Customer.objects.create(user=user, country=country)

        # Create wallet
        WalletService.create_wallet_for_user(user=user)

        # Register device if provided
        if fcm_token and device_type:
            device_data = DeviceData(
                registration_id=fcm_token,
                device_id=device_id,
                type=device_type,
            )
            DeviceService.register_device(user=user, device_data=device_data)

        return user

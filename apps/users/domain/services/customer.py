from rest_framework.exceptions import AuthenticationFailed

from apps.location.models.country import Country
from apps.users.domain.validators.user import UserValidator
from apps.users.models.customer import Customer


class CustomerService:
    @staticmethod
    def get_or_create_active_customer(phone_number: str) -> tuple[Customer, bool]:
        customer, created = Customer.objects.get_or_create(phone_number=phone_number)
        UserValidator.validate_user_is_active(customer)
        return customer, created

    @staticmethod
    def update_or_create_customer(
        *,
        phone_number: str,
        language: str,
        country: Country,
        inviter: int | None = None,
    ) -> tuple[Customer, bool]:
        from apps.payment.constants import ReferralType
        from apps.payment.domain.services.wallet import WalletService

        defaults = {
            "username": str(phone_number),
            "language": language,
            "country": country,
            "inviter": inviter,
        }

        customer, created = Customer.objects.update_or_create(
            phone_number=phone_number, defaults=defaults
        )

        customer.clean()
        customer.save()

        # Handle wallet creation for new customers
        if created:
            WalletService.create_wallet_for_customer(customer, country.currency)

            # Handle referral rewards for new customers
            if inviter:
                inviter_customer = Customer.objects.filter(
                    id=inviter, is_active=True
                ).first()
                if inviter_customer:
                    WalletService.add_referral_points(
                        inviter_customer=inviter_customer,
                        invitee_customer=customer,
                        referral_type=ReferralType.APP_INSTALL,
                    )

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

        # The Default country
        country = Country.objects.get(code="SA")

        customer = Customer(
            email=email,
            phone_number=phone_number,
            username=username,
            country=country,
        )
        if password:
            customer.set_password(password)
        customer.full_clean()
        customer.is_verified = False
        customer.save()

        # Create wallet for new customer
        WalletService.create_wallet_for_customer(customer, country.currency)

        return customer

    @staticmethod
    def change_password(
        *, customer: Customer, old_password: str, new_password: str
    ) -> None:
        if not customer.check_password(old_password):
            raise AuthenticationFailed("Old password is incorrect")

        if old_password == new_password:
            raise AuthenticationFailed(
                "New password must be different from the old password"
            )

        customer.set_password(new_password)
        customer.save()

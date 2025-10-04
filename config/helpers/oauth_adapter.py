from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth.hashers import make_password

from apps.location.models.country import Country
from apps.users.models.customer import Customer
from apps.users.models.user import User


class CustomerSocialAccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin: SocialLogin) -> Customer:
        data = sociallogin.account.extra_data or {}

        email = data.get("email", "")
        username = data.get("given_name") or data.get("first_name") or "unknown"

        # Get full name from provider data
        full_name = (
            data.get("name")
            or f"{data.get('first_name', '')} {data.get('last_name', '')}"
        ).strip()

        country = Country.objects.filter(is_active=True).first()

        customer = Customer(
            username=username,
            phone_number=None,
            email=email,
            full_name=full_name,
            country=country,
        )
        sociallogin.user = customer
        return customer

    def save_user(self, request, sociallogin: SocialLogin, form=None) -> Customer:
        customer: Customer = sociallogin.user
        if not customer.password:
            customer.password = make_password(None)
        customer.save()
        sociallogin.account.user = customer
        sociallogin.account.save()
        return customer

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.username:
            email = data.get("email", "unknown@example.com")
            user.username = email.split("@")[0]
        return user

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return
        email = sociallogin.account.extra_data.get("email")
        if email:
            try:
                existing_user = User.objects.get(email=email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass

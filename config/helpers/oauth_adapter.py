from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth.hashers import make_password

from apps.location.models.country import Country
from apps.users.models.customer import Customer


class CustomerSocialAccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin: SocialLogin) -> Customer:
        data = sociallogin.account.extra_data or {}
        email = data.get("email", "")
        name = data.get("name", "")
        username = (
            email.split("@")[0] if email else super().generate_unique_username([name])
        )
        country = Country.objects.get(pk="UNSELECTED")  # TODO remove it
        customer = Customer(
            username=username,
            email=email,
            full_name=name,
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

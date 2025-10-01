"""
Simple factories using factory_boy + Faker
"""

import factory
from django.contrib.gis.geos import Point
from djmoney.money import Money
from factory import fuzzy

from apps.appInfo.models.app_info import AppInfo
from apps.appInfo.models.banner import Banner
from apps.appInfo.models.banner_group import BannerGroup
from apps.appInfo.models.contact_us import ContactUs
from apps.appInfo.models.faq import FAQ
from apps.appInfo.models.onboarding import Onboarding
from apps.appInfo.models.popup import PopUpBanner
from apps.appInfo.models.social import SocialAccount
from apps.appInfo.other.constants import ContactCategory
from apps.channel.constants import NotificationType
from apps.channel.models.notification import Notification
from apps.location.constants import CountryChoices
from apps.location.constants import CurrencyCode
from apps.location.constants import LocationNameChoices
from apps.location.models.address import Address
from apps.location.models.country import Country
from apps.location.models.region import Region
from apps.payment.constants import WalletTransactionType
from apps.payment.models.wallet import Wallet
from apps.payment.models.wallet_transaction import WalletTransaction
from apps.users.constants import GenderChoices
from apps.users.models.admin import AdminUser
from apps.users.models.customer import Customer


class CountryFactory(factory.django.DjangoModelFactory):
    code = fuzzy.FuzzyChoice(
        [choice[0] for choice in CountryChoices.choices if choice[0] != "UN"]
    )
    name = factory.LazyAttribute(lambda obj: dict(CountryChoices.choices)[obj.code])
    currency = fuzzy.FuzzyChoice([choice[0] for choice in CurrencyCode.choices])
    flag = factory.django.ImageField(color="blue", width=100, height=100)
    is_active = True
    phone_code = factory.Faker("numerify", text="###")

    app_install_money_inviter = factory.LazyAttribute(
        lambda obj: Money(10, obj.currency)
    )
    app_install_money_invitee = factory.LazyAttribute(
        lambda obj: Money(10, obj.currency)
    )
    order_money_inviter = factory.LazyAttribute(lambda obj: Money(20, obj.currency))
    order_money_invitee = factory.LazyAttribute(lambda obj: Money(20, obj.currency))

    class Meta:
        model = Country
        django_get_or_create = ("code",)


class CustomerFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user_{n}")  # Unique usernames
    email = factory.Sequence(lambda n: f"user{n}@example.com")  # Unique emails
    phone_number = factory.Faker("phone_number")
    full_name = factory.Faker("name")
    image = factory.django.ImageField(color="green", width=800, height=800)
    gender = fuzzy.FuzzyChoice([choice[0] for choice in GenderChoices.choices])
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=80)
    country = factory.SubFactory(CountryFactory)
    is_verified = factory.Faker("boolean", chance_of_getting_true=70)

    class Meta:
        model = Customer


class BannerGroupFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("words", nb=3)
    order = factory.Sequence(lambda n: n)
    is_active = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = BannerGroup


class BannerFactory(factory.django.DjangoModelFactory):
    image = factory.django.ImageField(color="red", width=1200, height=800)
    group = factory.SubFactory(BannerGroupFactory)
    is_active = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = Banner


# Users
class AdminUserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"admin_{n}")  # Unique usernames
    email = factory.Sequence(lambda n: f"admin{n}@example.com")  # Unique emails
    image = factory.django.ImageField(color="purple", width=800, height=800)
    can_access_money = factory.Faker("boolean", chance_of_getting_true=30)
    is_staff = True

    class Meta:
        model = AdminUser


# Channel
class NotificationFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=5)
    message_body = factory.Faker("text", max_nb_chars=200)
    notification_type = fuzzy.FuzzyChoice(
        [choice[0] for choice in NotificationType.choices]
    )
    send_sms = factory.Faker("boolean", chance_of_getting_true=50)
    send_fcm = factory.Faker("boolean", chance_of_getting_true=80)
    object_id = factory.Faker("random_int", min=1, max=1000)
    is_read = factory.Faker("boolean", chance_of_getting_true=30)

    class Meta:
        model = Notification
        skip_postgeneration_save = True

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.users.add(user)
        else:
            # Add 1-3 random customers
            from apps.users.models.customer import Customer

            customers = Customer.objects.all()[:3]
            if customers:
                self.users.add(*customers)


# Location
class RegionFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    code = factory.Sequence(lambda n: f"REG{n:05d}")  # More unique codes
    name = factory.Faker("city")
    geometry = factory.LazyAttribute(
        lambda obj: Point(-74.0, 40.7)
    )  # Simple default point

    class Meta:
        model = Region
        django_get_or_create = ("code",)


class AddressFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    point = factory.LazyAttribute(
        lambda obj: Point(-74.0, 40.7)
    )  # Simple default point
    description = factory.Faker("address")
    map_description = factory.Faker("sentence")
    location_type = fuzzy.FuzzyChoice(
        [choice[0] for choice in LocationNameChoices.choices]
    )
    map_image = factory.django.ImageField(color="orange", width=600, height=400)

    class Meta:
        model = Address


# AppInfo
class FAQFactory(factory.django.DjangoModelFactory):
    question = factory.Faker("sentence", nb_words=8)
    answer = factory.Faker("text", max_nb_chars=300)
    order = factory.Sequence(lambda n: n + 1000)  # Start from 1000 to avoid conflicts

    class Meta:
        model = FAQ
        django_get_or_create = ("order",)


class PopUpBannerFactory(factory.django.DjangoModelFactory):
    image = factory.django.ImageField(color="yellow", width=1200, height=800)
    count_per_user = factory.Faker("random_int", min=1, max=5)
    is_active = factory.Faker("boolean", chance_of_getting_true=70)

    class Meta:
        model = PopUpBanner


class SocialAccountFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    phone_number = factory.Faker("numerify", text="+###########")  # Max 15 chars
    twitter = factory.Faker("url")
    instagram = factory.Faker("url")
    tiktok = factory.Faker("url")
    website = factory.Faker("url")

    class Meta:
        model = SocialAccount


class ContactUsFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    contact_type = fuzzy.FuzzyChoice([choice[0] for choice in ContactCategory.choices])
    description = factory.Faker("text", max_nb_chars=500)
    has_checked = factory.Faker("boolean", chance_of_getting_true=40)

    class Meta:
        model = ContactUs


class OnboardingFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=4)
    image = factory.django.ImageField(color="cyan", width=1200, height=800)
    text = factory.Faker("text", max_nb_chars=75)
    sub_text = factory.Faker("text", max_nb_chars=50)
    order = factory.Sequence(lambda n: n)
    is_active = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = Onboarding


class AppInfoFactory(factory.django.DjangoModelFactory):
    about_us = factory.Faker("text", max_nb_chars=1000)
    terms = factory.Faker("text", max_nb_chars=1000)
    policy = factory.Faker("text", max_nb_chars=1000)

    class Meta:
        model = AppInfo


class WalletFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(CustomerFactory)
    balance = factory.LazyFunction(lambda: Money(100, "USD"))
    is_use_wallet_in_payment = True

    class Meta:
        model = Wallet
        django_get_or_create = ("user",)  # Get or create based on user


class WalletTransactionFactory(factory.django.DjangoModelFactory):
    wallet = factory.LazyAttribute(
        lambda obj: WalletFactory()
    )  # Always create new wallet (with new user)
    transaction_type = fuzzy.FuzzyChoice(
        [choice[0] for choice in WalletTransactionType.choices]
    )
    amount = factory.LazyFunction(lambda: Money(50, "USD"))
    action_by = factory.SubFactory(AdminUserFactory)
    transaction_note = factory.Faker("sentence")

    class Meta:
        model = WalletTransaction

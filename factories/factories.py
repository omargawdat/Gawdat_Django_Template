"""
Simple factories using factory_boy + Faker
"""

import factory
from django.contrib.gis.geos import Point
from djmoney.money import Money
from faker import Faker
from faker_e164.providers import E164Provider

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

# Mapping of country codes to their currency and phone prefix
COUNTRY_DATA = {
    "EG": {"currency": "EGP", "phone_code": "20"},
    "SA": {"currency": "SAR", "phone_code": "966"},
    "AE": {"currency": "AED", "phone_code": "971"},
    "KW": {"currency": "KWD", "phone_code": "965"},
    "QA": {"currency": "QAR", "phone_code": "974"},
    "OM": {"currency": "OMR", "phone_code": "968"},
    "BH": {"currency": "BHD", "phone_code": "973"},
}

# Initialize Faker with E164 provider for valid phone numbers
fake = Faker()
fake.add_provider(E164Provider)


class CountryFactory(factory.django.DjangoModelFactory):
    code = factory.Iterator(list(COUNTRY_DATA.keys()))
    name = factory.LazyAttribute(lambda obj: dict(CountryChoices.choices)[obj.code])
    currency = factory.LazyAttribute(lambda obj: COUNTRY_DATA[obj.code]["currency"])
    phone_code = factory.LazyAttribute(lambda obj: COUNTRY_DATA[obj.code]["phone_code"])
    flag = factory.django.ImageField(color="blue", width=100, height=100)
    is_active = True

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
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    full_name = factory.Faker("name")
    image = factory.django.ImageField(color="green", width=800, height=800)
    gender = factory.Iterator([choice[0] for choice in GenderChoices.choices])
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=80)
    is_verified = factory.Faker("boolean", chance_of_getting_true=70)
    country = factory.SubFactory(CountryFactory)
    password = "testpass123"  # pragma: allowlist secret  # noqa: S105

    # ✅ Generate valid E.164 phone number for the country
    phone_number = factory.LazyAttribute(
        lambda obj: fake.e164(region_code=obj.country.code, valid=True, possible=True)
    )

    class Meta:
        model = Customer

    class Params:
        verified = factory.Trait(is_verified=True)
        unverified = factory.Trait(is_verified=False)

    @factory.post_generation
    def hash_password(self, create, extracted, **kwargs):
        """Hash the password after creation"""
        if not create:
            return
        password = extracted if extracted else self.password
        self.set_password(password)
        self.save()

    @factory.post_generation
    def wallet(self, create, extracted, **kwargs):
        """Automatically create wallet for customer"""
        if not create:
            return
        if extracted is False:
            return
        WalletFactory(user=self)


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


class AdminUserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"admin_{n}")
    email = factory.Sequence(lambda n: f"admin{n}@example.com")
    image = factory.django.ImageField(color="purple", width=800, height=800)
    can_access_money = factory.Faker("boolean", chance_of_getting_true=30)
    is_staff = True
    password = "adminpass123"  # pragma: allowlist secret  # noqa: S105

    class Meta:
        model = AdminUser

    @factory.post_generation
    def hash_password(self, create, extracted, **kwargs):
        """Hash the password after creation"""
        if not create:
            return
        password = extracted if extracted else self.password
        self.set_password(password)
        self.save()


class NotificationFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=5)
    message_body = factory.Faker("text", max_nb_chars=200)
    notification_type = factory.Iterator(
        [choice[0] for choice in NotificationType.choices]
    )
    send_sms = False
    send_fcm = False
    object_id = factory.Faker("random_int", min=1, max=1000)
    is_read = factory.Faker("boolean", chance_of_getting_true=30)

    class Meta:
        model = Notification


class RegionFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    code = factory.Sequence(lambda n: f"REG{n:05d}")
    name = factory.Faker("city")
    geometry = factory.LazyAttribute(lambda obj: Point(-74.0, 40.7))

    class Meta:
        model = Region
        django_get_or_create = ("code",)


class AddressFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    point = factory.LazyAttribute(lambda obj: Point(-74.0, 40.7))
    description = factory.Faker("address")
    map_description = factory.Faker("sentence")
    location_type = factory.Iterator(
        [choice[0] for choice in LocationNameChoices.choices]
    )
    map_image = factory.django.ImageField(color="orange", width=600, height=400)

    class Meta:
        model = Address


class FAQFactory(factory.django.DjangoModelFactory):
    question = factory.Faker("sentence", nb_words=8)
    answer = factory.Faker("text", max_nb_chars=300)
    order = factory.Sequence(lambda n: n)

    class Meta:
        model = FAQ


class PopUpBannerFactory(factory.django.DjangoModelFactory):
    image = factory.django.ImageField(color="yellow", width=1200, height=800)
    count_per_user = factory.Faker("random_int", min=1, max=5)
    is_active = factory.Faker("boolean", chance_of_getting_true=70)

    class Meta:
        model = PopUpBanner


class SocialAccountFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    phone_number = factory.Faker("numerify", text="+###########")
    twitter = factory.Faker("url")
    instagram = factory.Faker("url")
    tiktok = factory.Faker("url")
    website = factory.Faker("url")

    class Meta:
        model = SocialAccount


class ContactUsFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(CustomerFactory)
    contact_type = factory.Iterator([choice[0] for choice in ContactCategory.choices])
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
    user = factory.SubFactory(CustomerFactory, wallet=False)
    balance = factory.LazyAttribute(lambda obj: Money(100, obj.user.country.currency))
    is_use_wallet_in_payment = True

    class Meta:
        model = Wallet
        django_get_or_create = ("user",)


class WalletTransactionFactory(factory.django.DjangoModelFactory):
    wallet = factory.SubFactory(WalletFactory)
    transaction_type = factory.Iterator(
        [choice[0] for choice in WalletTransactionType.choices]
    )
    amount = factory.LazyAttribute(
        lambda obj: Money(50, obj.wallet.user.country.currency)
    )
    action_by = factory.SubFactory(AdminUserFactory)
    transaction_note = factory.Faker("sentence")

    class Meta:
        model = WalletTransaction

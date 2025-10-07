"""
Factory definitions using SubFactory pattern for explicit relationships.

Benefits:
- Explicit dependencies (no manual priority management)
- Self-documenting (clear relationships)
- factory_boy handles dependency order automatically

Usage:
    # Seed DB - creates full object graph
    CustomerFactory.create_batch(10)

    # Tests - override as needed
    address = AddressFactory(customer__username="john")
"""

import factory
from django.conf import settings
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
from apps.appInfo.models.popup import PopUpTracking
from apps.appInfo.models.social import SocialAccount
from apps.appInfo.other.constants import ContactCategory
from apps.channel.constants import NotificationType
from apps.channel.models.notification import Notification
from apps.location.constants import LocationNameChoices
from apps.location.domain.utils import CountryInfoUtil
from apps.location.models.address import Address
from apps.location.models.country import Country
from apps.location.models.region import Region
from apps.payment.constants import WalletTransactionType
from apps.payment.models.wallet import Wallet
from apps.payment.models.wallet_transaction import WalletTransaction
from apps.users.constants import GenderChoices
from apps.users.models.admin import AdminUser
from apps.users.models.customer import Customer

# Initialize Faker
fake = Faker()
fake.add_provider(E164Provider)


# ============================================================================
# INDEPENDENT FACTORIES (No dependencies)
# ============================================================================


class CountryFactory(factory.django.DjangoModelFactory):
    """
    Country factory - no dependencies.

    Uses iterator to cycle through supported countries.
    """

    code = factory.Iterator(settings.SUPPORTED_COUNTRY_CODES)
    flag = factory.django.ImageField(color="blue", width=100, height=100)
    is_active = True

    app_install_money_inviter = factory.LazyAttribute(
        lambda obj: Money(10, CountryInfoUtil.get_currency_code(obj.code))
    )
    app_install_money_invitee = factory.LazyAttribute(
        lambda obj: Money(10, CountryInfoUtil.get_currency_code(obj.code))
    )
    order_money_inviter = factory.LazyAttribute(
        lambda obj: Money(20, CountryInfoUtil.get_currency_code(obj.code))
    )
    order_money_invitee = factory.LazyAttribute(
        lambda obj: Money(20, CountryInfoUtil.get_currency_code(obj.code))
    )

    class Meta:
        model = Country
        django_get_or_create = ("code",)


class AppInfoFactory(factory.django.DjangoModelFactory):
    """Singleton factory for app info"""

    id = 1
    about_us = factory.Faker("text", max_nb_chars=1000)
    terms = factory.Faker("text", max_nb_chars=1000)
    policy = factory.Faker("text", max_nb_chars=1000)

    class Meta:
        model = AppInfo
        django_get_or_create = ("id",)


class SocialAccountFactory(factory.django.DjangoModelFactory):
    """Singleton factory for social accounts"""

    id = 1
    email = factory.Faker("email")
    phone_number = factory.Faker("numerify", text="+###########")
    twitter = factory.Faker("url")
    instagram = factory.Faker("url")
    tiktok = factory.Faker("url")
    website = factory.Faker("url")

    class Meta:
        model = SocialAccount
        django_get_or_create = ("id",)


class BannerGroupFactory(factory.django.DjangoModelFactory):
    """Banner group - no dependencies"""

    name = factory.Faker("words", nb=3)
    order = factory.Sequence(lambda n: n)
    is_active = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = BannerGroup


class FAQFactory(factory.django.DjangoModelFactory):
    """FAQ - no dependencies"""

    question = factory.Faker("sentence", nb_words=8)
    answer = factory.Faker("text", max_nb_chars=300)
    order = factory.Sequence(lambda n: n)

    class Meta:
        model = FAQ


class OnboardingFactory(factory.django.DjangoModelFactory):
    """Onboarding screen - no dependencies"""

    title = factory.Faker("sentence", nb_words=4)
    image = factory.django.ImageField(color="cyan", width=1200, height=800)
    text = factory.Faker("text", max_nb_chars=75)
    sub_text = factory.Faker("text", max_nb_chars=50)
    order = factory.Sequence(lambda n: n)
    is_active = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = Onboarding


class PopUpBannerFactory(factory.django.DjangoModelFactory):
    """Popup banner - no dependencies"""

    image = factory.django.ImageField(color="yellow", width=1200, height=800)
    count_per_user = factory.Faker("random_int", min=1, max=5)
    is_active = factory.Faker("boolean", chance_of_getting_true=70)

    class Meta:
        model = PopUpBanner


# ============================================================================
# USER FACTORIES (Depend on Country)
# ============================================================================


class AdminUserFactory(factory.django.DjangoModelFactory):
    """Admin user - no dependencies"""

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
        if not create:
            return
        password = extracted if extracted else self.password
        self.set_password(password)
        self.save()


class CustomerFactory(factory.django.DjangoModelFactory):
    """
    Customer factory - depends on Country.

    Creates wallet automatically via post_generation.
    Use wallet=False to skip wallet creation.
    """

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    full_name = factory.Faker("name")
    image = factory.django.ImageField(color="green", width=800, height=800)
    gender = factory.Iterator([choice[0] for choice in GenderChoices.choices])
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=80)
    is_verified = factory.Faker("boolean", chance_of_getting_true=70)
    password = "testpass123"  # pragma: allowlist secret  # noqa: S105

    # SubFactory: Automatically creates Country if needed
    country = factory.SubFactory(CountryFactory)

    # Generate phone number based on country
    phone_number = factory.LazyAttribute(
        lambda obj: fake.e164(region_code=obj.country.code, valid=True, possible=True)
        if obj.country
        else "+966501234567"
    )

    class Meta:
        model = Customer
        skip_postgeneration_save = True

    class Params:
        verified = factory.Trait(is_verified=True)
        unverified = factory.Trait(is_verified=False)

    @factory.post_generation
    def hash_password(self, create, extracted, **kwargs):
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


# ============================================================================
# DEPENDENT FACTORIES (Use SubFactory for relationships)
# ============================================================================


class WalletFactory(factory.django.DjangoModelFactory):
    """
    Wallet factory - depends on Customer.

    Note: Wallets are typically created via CustomerFactory post_generation.
    Only use this directly if you need standalone wallets.
    """

    # SubFactory: Creates Customer if not provided
    user = factory.SubFactory(CustomerFactory, wallet=False)

    balance = factory.LazyAttribute(
        lambda obj: Money(100, obj.user.country.currency)
        if hasattr(obj, "user") and obj.user
        else Money(100, "SAR")
    )
    is_use_wallet_in_payment = True

    class Meta:
        model = Wallet
        django_get_or_create = ("user",)


class AddressFactory(factory.django.DjangoModelFactory):
    """
    Address factory - depends on Customer and Country.

    Creates complete object graph:
    Address → Customer → Country
            → Wallet
    """

    # SubFactories: Automatically create related objects
    customer = factory.SubFactory(CustomerFactory, wallet=False)
    country = factory.SubFactory(CountryFactory)

    point = factory.LazyFunction(
        lambda: Point(float(fake.longitude()), float(fake.latitude()))
    )
    description = factory.Faker("address")
    map_description = factory.Faker("sentence")
    location_type = factory.Iterator(
        [choice[0] for choice in LocationNameChoices.choices]
    )
    map_image = factory.django.ImageField(color="orange", width=600, height=400)

    class Meta:
        model = Address


class ContactUsFactory(factory.django.DjangoModelFactory):
    """Contact us - depends on Customer"""

    customer = factory.SubFactory(CustomerFactory, wallet=False)
    contact_type = factory.Iterator([choice[0] for choice in ContactCategory.choices])
    description = factory.Faker("text", max_nb_chars=500)
    has_checked = factory.Faker("boolean", chance_of_getting_true=40)

    class Meta:
        model = ContactUs


class RegionFactory(factory.django.DjangoModelFactory):
    """Region - depends on Country"""

    country = factory.SubFactory(CountryFactory)
    code = factory.Sequence(lambda n: f"REG{n:05d}")
    name = factory.Faker("city")
    geometry = factory.LazyFunction(
        lambda: Point(float(fake.longitude()), float(fake.latitude()))
    )

    class Meta:
        model = Region
        django_get_or_create = ("code",)


class BannerFactory(factory.django.DjangoModelFactory):
    """Banner - depends on BannerGroup"""

    image = factory.django.ImageField(color="red", width=1200, height=800)
    group = factory.SubFactory(BannerGroupFactory)
    is_active = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = Banner


class NotificationFactory(factory.django.DjangoModelFactory):
    """Notification - no FK dependencies (M2M handled separately)"""

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
        skip_postgeneration_save = True

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        """Assign users to notification (M2M)"""
        if not create:
            return

        if extracted:
            # Use provided users
            for user in extracted:
                self.users.add(user)
        else:
            # Add existing customers (if any)
            customers = Customer.objects.all()[:3]
            if customers:
                self.users.add(*customers)


class PopUpTrackingFactory(factory.django.DjangoModelFactory):
    """Popup tracking - depends on Customer and PopUpBanner"""

    customer = factory.SubFactory(CustomerFactory, wallet=False)
    popup = factory.SubFactory(PopUpBannerFactory)
    view_count = factory.Faker("random_int", min=1, max=20)

    class Meta:
        model = PopUpTracking


class WalletTransactionFactory(factory.django.DjangoModelFactory):
    """Wallet transaction - depends on Wallet and AdminUser"""

    wallet = factory.SubFactory(WalletFactory)
    transaction_type = factory.Iterator(
        [choice[0] for choice in WalletTransactionType.choices]
    )
    amount = factory.LazyAttribute(
        lambda obj: Money(50, obj.wallet.user.country.currency)
        if obj.wallet
        else Money(50, "SAR")
    )
    action_by = factory.SubFactory(AdminUserFactory)
    transaction_note = factory.Faker("sentence")

    class Meta:
        model = WalletTransaction

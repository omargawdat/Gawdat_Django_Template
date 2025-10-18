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
from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
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
from apps.payment.constants import PaymentType
from apps.payment.constants import WalletTransactionType
from apps.payment.models.payment import Payment
from apps.payment.models.wallet import Wallet
from apps.payment.models.wallet_transaction import WalletTransaction
from apps.users.constants import GenderChoices
from apps.users.models import User
from apps.users.models.admin import AdminUser
from apps.users.models.customer import Customer

# Initialize Faker
fake = Faker()
fake.add_provider(E164Provider)


# ============================================================================
# SHARED IMAGE (Generated once, reused everywhere)
# ============================================================================

# Generate one image at module load time and reuse it
_shared_image_field = factory.django.ImageField(color="blue", width=100, height=100)
_shared_image_bytes = _shared_image_field._make_data({})
_shared_image_name = "shared_test_image.png"

# Pre-save the shared image to storage once
if not default_storage.exists(_shared_image_name):
    default_storage.save(_shared_image_name, ContentFile(_shared_image_bytes))


def get_shared_image():
    """Return the path to the pre-saved shared image."""
    return _shared_image_name


# ============================================================================
# SHARED PASSWORD HASH (Generated once, reused everywhere)
# ============================================================================

# Pre-hash password once to avoid expensive re-hashing for test data

_SHARED_PASSWORD_HASH = make_password("testpass123")  # pragma: allowlist secret


# ============================================================================
# INDEPENDENT FACTORIES (No dependencies)
# ============================================================================


class CountryFactory(factory.django.DjangoModelFactory):
    """
    Country factory - no dependencies.

    Uses iterator to cycle through supported countries.
    """

    code = factory.Iterator(settings.SUPPORTED_COUNTRY_CODES)
    flag = factory.LazyFunction(get_shared_image)
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

    @classmethod
    def create_batch_bulk(cls, count, **kwargs):
        """Create Countries in bulk for better performance."""
        countries = [cls.build(**kwargs) for _ in range(count)]
        return Country.objects.bulk_create(countries, ignore_conflicts=True)


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

    name = factory.Sequence(lambda n: f"Banner Group {n}")
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

    @classmethod
    def create_batch_bulk(cls, count, **kwargs):
        """Create FAQs in bulk for better performance."""
        faqs = [cls.build(**kwargs) for _ in range(count)]
        return FAQ.objects.bulk_create(faqs)


class OnboardingFactory(factory.django.DjangoModelFactory):
    """Onboarding screen - no dependencies"""

    title = factory.Faker("sentence", nb_words=4)
    image = factory.LazyFunction(get_shared_image)
    text = factory.Faker("text", max_nb_chars=75)
    sub_text = factory.Faker("text", max_nb_chars=50)
    order = factory.Sequence(lambda n: n)
    is_active = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = Onboarding

    @classmethod
    def create_batch_bulk(cls, count, **kwargs):
        """Create Onboarding screens in bulk for better performance."""
        onboardings = [cls.build(**kwargs) for _ in range(count)]
        return Onboarding.objects.bulk_create(onboardings)


class PopUpBannerFactory(factory.django.DjangoModelFactory):
    """Popup banner - no dependencies"""

    image = factory.LazyFunction(get_shared_image)
    count_per_user = factory.Faker("random_int", min=1, max=5)
    is_active = factory.Faker("boolean", chance_of_getting_true=70)

    class Meta:
        model = PopUpBanner

    @classmethod
    def create_batch_bulk(cls, count, **kwargs):
        """Create PopUp Banners in bulk for better performance."""
        popups = [cls.build(**kwargs) for _ in range(count)]
        return PopUpBanner.objects.bulk_create(popups)


# ============================================================================
# USER FACTORIES (Depend on Country)
# ============================================================================


class UserFactory(factory.django.DjangoModelFactory):
    """Base User factory - for creating plain User instances."""

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone_number = factory.Sequence(lambda n: f"+96655{n:07d}")
    is_staff = False
    is_active = True
    password = "testpass123"  # pragma: allowlist secret  # noqa: S105

    class Meta:
        model = User
        skip_postgeneration_save = True

    @factory.post_generation
    def hash_password(self, create, extracted, **kwargs):
        if not create:
            return
        # Use pre-hashed password to avoid expensive re-hashing
        self.password = _SHARED_PASSWORD_HASH
        self.save(update_fields=["password"])


class AdminUserFactory(factory.django.DjangoModelFactory):
    """Admin user - no dependencies"""

    username = factory.Sequence(lambda n: f"admin_{n}")
    email = factory.Sequence(lambda n: f"admin{n}@example.com")
    image = factory.LazyFunction(get_shared_image)
    can_access_money = factory.Faker("boolean", chance_of_getting_true=30)
    is_staff = True
    password = "adminpass123"  # pragma: allowlist secret  # noqa: S105

    class Meta:
        model = AdminUser
        skip_postgeneration_save = True

    @factory.post_generation
    def hash_password(self, create, extracted, **kwargs):
        if not create:
            return
        # Use pre-hashed password to avoid expensive re-hashing
        self.password = _SHARED_PASSWORD_HASH
        self.save(update_fields=["password"])


class CustomerFactory(factory.django.DjangoModelFactory):
    """Customer factory - depends on Country and User."""

    # SubFactory: Automatically creates Country if needed
    country = factory.SubFactory(CountryFactory)

    # Create User with SubFactory including phone_number
    user = factory.SubFactory(
        "factories.factories.UserFactory",
        email=factory.Sequence(lambda n: f"customer{n}@example.com"),
        phone_number=factory.LazyAttribute(
            lambda obj: fake.e164(
                region_code=obj.factory_parent.country.code, valid=True, possible=True
            )
        ),
    )

    full_name = factory.Faker("name")
    image = factory.LazyFunction(get_shared_image)
    gender = factory.Iterator([choice[0] for choice in GenderChoices.choices])
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=80)
    is_verified = factory.Faker("boolean", chance_of_getting_true=70)

    class Meta:
        model = Customer
        skip_postgeneration_save = True

    class Params:
        verified = factory.Trait(is_verified=True)
        unverified = factory.Trait(is_verified=False)

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        if not create:
            return
        # Set password on the user model
        password = extracted if extracted else "testpass123"  # pragma: allowlist secret
        self.user.set_password(password)
        self.user.save(update_fields=["password"])

    @factory.post_generation
    def create_wallet(self, create, extracted, **kwargs):
        """Auto-create wallet for customer"""
        if not create:
            return
        WalletFactory.create(user=self.user)

    @factory.post_generation
    def create_addresses(self, create, extracted, **kwargs):
        """Auto-create addresses for customer"""
        if not create:
            return
        count = extracted if extracted is not None else 2
        AddressFactory.create_batch(count, customer=self)

    @factory.post_generation
    def create_contact_us(self, create, extracted, **kwargs):
        """Auto-create contact us entry for customer"""
        if not create:
            return
        if extracted is not False:  # Allow explicit skip with False
            ContactUsFactory.create(customer=self)


# ============================================================================
# DEPENDENT FACTORIES (Use SubFactory for relationships)
# ============================================================================


class WalletFactory(factory.django.DjangoModelFactory):
    """Wallet factory - depends on User."""

    # SubFactory: Creates User if not provided
    user = factory.SubFactory(UserFactory)

    balance = factory.LazyAttribute(
        lambda obj: Money(100, obj.user.customer.country.currency)
        if hasattr(obj.user, "customer")
        else Money(100, "USD")
    )
    is_use_wallet_in_payment = True

    class Meta:
        model = Wallet

    @factory.post_generation
    def create_transactions(self, create, extracted, **kwargs):
        """Auto-create wallet transactions"""
        if not create:
            return
        count = extracted if extracted is not None else 3
        if count > 0:
            WalletTransactionFactory.create_batch(count, wallet=self)


class AddressFactory(factory.django.DjangoModelFactory):
    """
    Address factory - depends on Customer and Country.

    Creates complete object graph:
    Address → Customer → Country
            → Wallet
    """

    # SubFactories: Automatically create related objects
    customer = factory.SubFactory(CustomerFactory)
    country = factory.SubFactory(CountryFactory)

    # Generate realistic coordinates based on country (with fallback)
    point = factory.LazyAttribute(
        lambda obj: (
            Point(float(coords[1]), float(coords[0]))
            if (coords := fake.local_latlng(country_code=obj.country.code))
            else Point(float(fake.longitude()), float(fake.latitude()))
        )
    )
    description = factory.Faker("address")
    map_description = factory.Faker("sentence")
    location_type = factory.Iterator(
        [choice[0] for choice in LocationNameChoices.choices]
    )
    map_image = factory.LazyFunction(get_shared_image)

    class Meta:
        model = Address


class ContactUsFactory(factory.django.DjangoModelFactory):
    """Contact us - depends on Customer"""

    customer = factory.SubFactory(CustomerFactory)
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
    # Generate realistic coordinates based on country (with fallback)
    geometry = factory.LazyAttribute(
        lambda obj: (
            Point(float(coords[1]), float(coords[0]))
            if (coords := fake.local_latlng(country_code=obj.country.code))
            else Point(float(fake.longitude()), float(fake.latitude()))
        )
    )

    class Meta:
        model = Region
        django_get_or_create = ("code",)

    @classmethod
    def create_batch_bulk(cls, count, **kwargs):
        """Create Regions in bulk for better performance."""
        regions = [cls.build(**kwargs) for _ in range(count)]
        return Region.objects.bulk_create(regions)


class BannerFactory(factory.django.DjangoModelFactory):
    """Banner - depends on BannerGroup"""

    image = factory.LazyFunction(get_shared_image)
    group = factory.SubFactory(BannerGroupFactory)
    is_active = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = Banner


class NotificationFactory(factory.django.DjangoModelFactory):
    """Notification - M2M relationships handled explicitly in seed_db"""

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

    @classmethod
    def create_batch_bulk(cls, count, **kwargs):
        """Create Notifications in bulk for better performance."""
        notifications = [cls.build(**kwargs) for _ in range(count)]
        return Notification.objects.bulk_create(notifications)


class PopUpTrackingFactory(factory.django.DjangoModelFactory):
    """Popup tracking - depends on Customer and PopUpBanner"""

    customer = factory.SubFactory(CustomerFactory)
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
        lambda obj: Money(
            50,
            obj.wallet.user.customer.country.currency
            if hasattr(obj.wallet.user, "customer")
            else obj.wallet.balance.currency,
        )
    )
    action_by = factory.SubFactory(AdminUserFactory)
    transaction_note = factory.Faker("sentence")

    class Meta:
        model = WalletTransaction


class PaymentFactory(factory.django.DjangoModelFactory):
    """Payment factory - depends on Customer"""

    # Reuse existing customer randomly, create one if none exist
    customer = factory.LazyAttribute(
        lambda obj: Customer.objects.order_by("?").first() or CustomerFactory()
    )
    price_before_discount = factory.LazyAttribute(
        lambda obj: Money(
            fake.random_int(min=50, max=500),
            obj.customer.country.currency if obj.customer else "SAR",
        )
    )
    price_after_discount = factory.LazyAttribute(
        lambda obj: Money(
            int(
                obj.price_before_discount.amount
                * fake.pydecimal(
                    left_digits=1,
                    right_digits=2,
                    positive=True,
                    min_value=0.7,
                    max_value=1.0,
                )
            ),
            obj.price_before_discount.currency,
        )
    )
    payment_type = factory.Iterator([choice[0] for choice in PaymentType.choices])
    is_paid = factory.Faker("boolean", chance_of_getting_true=70)
    payment_charge_id = factory.Faker("uuid4")
    bank_transaction_response = factory.LazyFunction(
        lambda: {
            "status": fake.random_element(["success", "pending", "failed"]),
            "transaction_id": fake.uuid4(),
            "gateway": fake.random_element(["stripe", "paypal", "visa"]),
            "timestamp": fake.iso8601(),
        }
    )

    class Meta:
        model = Payment

    @classmethod
    def create_batch_bulk(cls, count, customers=None, **kwargs):
        """Create Payments in bulk (pass customers list to avoid queries)."""
        import random

        if customers:
            payments = [
                cls.build(customer=random.choice(customers), **kwargs)  # noqa: S311
                for _ in range(count)
            ]
        else:
            payments = [cls.build(**kwargs) for _ in range(count)]
        return Payment.objects.bulk_create(payments)

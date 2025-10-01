"""
Simple factories using factory_boy + Faker
"""

import factory
from djmoney.money import Money
from factory import fuzzy

from apps.appInfo.models.banner import Banner
from apps.appInfo.models.banner_group import BannerGroup
from apps.location.constants import CountryChoices
from apps.location.constants import CurrencyCode
from apps.location.models.country import Country
from apps.users.constants import GenderChoices
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
    username = factory.Faker("user_name")
    email = factory.Faker("email")
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

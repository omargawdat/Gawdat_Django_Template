from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from simple_history.models import HistoricalRecords

from apps.location.domain.selector.country import CountrySelector
from apps.location.models.country import Country
from apps.users.constants import GenderChoices

from .user import User


class CustomerManager(models.Manager):
    """Custom manager that automatically optimizes queries with select_related."""

    def get_queryset(self):
        return super().get_queryset().select_related("user", "country")


class Customer(models.Model):
    # Field declarations
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer",
        verbose_name=_("User"),
        primary_key=True,
    )
    history = HistoricalRecords()
    image = ProcessedImageField(
        upload_to="users/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        null=True,
        blank=True,
        verbose_name=_("Image"),
    )
    full_name = models.CharField(
        max_length=255, default="", blank=True, verbose_name=_("Full Name")
    )
    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        default=GenderChoices.NOT_SELECTED,
        verbose_name=_("Gender"),
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth Date"))
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        verbose_name=_("Country"),
        related_name="customers",
    )
    primary_address = models.OneToOneField(
        "location.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",  # [important]: for solving the conflict of bidirectional relationship
        verbose_name=_("Primary Address"),
    )
    is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified"))
    inviter = models.PositiveIntegerField(
        null=True, blank=True, db_index=True, verbose_name=_("Referral Customer ID")
    )

    # Custom manager
    objects = CustomerManager()

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return str(self.phone_number)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        from apps.users.domain.validators.customer import CustomerValidator

        super().clean()
        # [WHY]: to ensure the country for this phone exists before trying to save
        CountrySelector.country_by_phone(self.phone_number)
        CustomerValidator.validate_address_belongs_to_customer(
            address=self.primary_address, customer=self
        )

    # Proxy properties for User fields
    @property
    def email(self) -> str:
        return self.user.email

    @email.setter
    def email(self, value) -> None:
        self.user.email = value

    @property
    def username(self) -> str:
        return self.user.username

    @username.setter
    def username(self, value) -> None:
        self.user.username = value

    @property
    def language(self) -> str:
        return self.user.language

    @language.setter
    def language(self, value) -> None:
        self.user.language = value

    @property
    def is_active(self) -> bool:
        return self.user.is_active

    @is_active.setter
    def is_active(self, value) -> None:
        self.user.is_active = value

    @property
    def date_joined(self) -> str:
        return self.user.date_joined

    @property
    def phone_number(self) -> str:
        return self.user.phone_number

    @phone_number.setter
    def phone_number(self, value) -> None:
        self.user.phone_number = value

    @property
    def is_profile_completed(self) -> bool:
        from apps.users.domain.selectors.customer import CustomerSelector

        return CustomerSelector.is_profile_completed(self)

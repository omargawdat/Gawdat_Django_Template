from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from apps.location.domain.selector.country import CountrySelector
from apps.location.models.country import Country
from apps.payment.domain.services.wallet import WalletService
from apps.users.constants import GenderChoices

from .user import User


class Customer(User):
    history = HistoricalRecords()
    phone_number = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        help_text="Should start with country code as (+966)",
        verbose_name=_("Phone Number"),
    )
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
        related_name="users",
    )
    primary_address = models.OneToOneField(
        "location.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",  # [important]: for solving the conflict of bidirectional relationship
        verbose_name=_("Primary Address"),
    )

    def __str__(self):
        return str(self.phone_number)

    @property
    def is_profile_completed(self) -> bool:
        from apps.users.domain.selectors.customer import CustomerSelector

        return CustomerSelector.is_profile_completed(self)

    def clean(self):
        from apps.location.domain.validators.country import CountryValidator
        from apps.users.domain.validators.customer import CustomerValidator

        super().clean()
        # [WHY]: to ensure the country for this phone exists before trying to save
        CountrySelector.country_by_phone(self.phone_number)

        if self.pk:
            CountryValidator.validate_match_country_phone(
                phone_number=self.phone_number, country=self.country
            )
        CustomerValidator.validate_address_belongs_to_customer(
            address=self.primary_address, customer=self
        )

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            WalletService.create_wallet_for_user(self)

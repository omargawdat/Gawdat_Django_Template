from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from .user import User


class ProviderManager(models.Manager):
    """Custom manager that automatically optimizes queries with select_related."""

    def get_queryset(self):
        return super().get_queryset().select_related("user")


class Provider(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider",
        verbose_name=_("User"),
        primary_key=True,
    )
    history = HistoricalRecords()
    company_name = models.CharField(
        max_length=255, default="", blank=True, verbose_name=_("Company Name")
    )

    # Custom manager
    objects = ProviderManager()

    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")

    def __str__(self):
        return self.email or f"Provider {self.pk}"

    # Proxy properties for User fields
    @property
    def email(self) -> str:
        return self.user.email

    @email.setter
    def email(self, value) -> None:
        self.user.email = value

    @property
    def is_active(self) -> bool:
        return self.user.is_active

    @is_active.setter
    def is_active(self, value) -> None:
        self.user.is_active = value

    @property
    def date_joined(self):
        return self.user.date_joined

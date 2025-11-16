from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from apps.users.models.user import User


class NotificationAdminForm(forms.ModelForm):
    """Custom form for Notification with separate customer and provider selection."""

    customers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(customer__isnull=False).select_related("customer"),
        required=False,
        label=_("Customers"),
        widget=FilteredSelectMultiple(verbose_name=_("Customers"), is_stacked=False),
    )

    providers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(provider__isnull=False).select_related("provider"),
        required=False,
        label=_("Providers"),
        widget=FilteredSelectMultiple(verbose_name=_("Providers"), is_stacked=False),
    )

    class Meta:
        fields = ["notification_type", "title", "message_body", "send_sms", "send_fcm"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customers"].label_from_instance = self._customer_label
        self.fields["providers"].label_from_instance = self._provider_label

        if self.instance.pk:
            self.fields["customers"].initial = self.instance.users.filter(
                customer__isnull=False
            )
            self.fields["providers"].initial = self.instance.users.filter(
                provider__isnull=False
            )

    @staticmethod
    def _customer_label(user):
        """Display name for customer users."""
        return user.customer.full_name or user.email

    @staticmethod
    def _provider_label(user):
        """Display name for provider users."""
        return user.provider.company_name or user.email

    def save(self, commit=True):
        """Save notification and set users from customers and providers fields."""
        instance = super().save(commit=commit)

        if commit:
            self._save_users(instance)
        else:
            self.save_m2m = lambda: self._save_users(instance)

        return instance

    def _save_users(self, instance):
        """Combine customers and providers into users M2M field."""
        customers = self.cleaned_data.get("customers", [])
        providers = self.cleaned_data.get("providers", [])
        instance.users.set(list(customers) + list(providers))


class NotificationChangeView:
    form = NotificationAdminForm
    filter_horizontal = ()
    compressed_fields = True
    autocomplete_fields = []

    fieldsets = (
        (
            _("Notification 📢"),
            {
                "fields": ("notification_type", "title", "message_body"),
            },
        ),
        (
            _("Customers 👥"),
            {
                "fields": ("customers",),
            },
        ),
        (
            _("Providers 🏢"),
            {
                "fields": ("providers",),
            },
        ),
        (
            _("Delivery Options 📬"),
            {
                "fields": ("send_sms", "send_fcm"),
            },
        ),
    )

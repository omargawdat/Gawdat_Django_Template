from django import forms
from django.core.exceptions import ValidationError

from apps.users.domain.validators.phone import PhoneValidator
from apps.users.models.provider import Provider


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get("phone_number"):
            self.initial["phone_number"] = "+966"
        if not self.instance.pk:
            self.initial["is_phone_verified"] = True

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not PhoneValidator.is_phone_in_working_country(phone_number):
            raise ValidationError("Phone number must be from a Working Country")
        return phone_number

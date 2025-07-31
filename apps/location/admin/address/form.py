from django import forms
from mapwidgets.widgets import GoogleMapPointFieldWidget

from apps.location.models.address import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("point",)
        widgets = {
            "point": GoogleMapPointFieldWidget,
        }

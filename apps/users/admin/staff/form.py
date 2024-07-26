from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm

from apps.users.models.staff import StaffUser


class StaffForm(ModelForm):
    class Meta:
        model = StaffUser
        fields = "__all__"

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password, user=self.instance)
        return password

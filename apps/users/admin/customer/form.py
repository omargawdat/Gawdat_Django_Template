from django.forms import ModelForm

from apps.users.models.customer import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.users.helpers.hash_password import HashPasswordMixin
from apps.users.models.staff import StaffUser


class StaffForm(forms.ModelForm):
    class Meta:
        model = StaffUser
        fields = [
            "username",
            "phone_number",
            "image",
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
        ]

    def save(self, commit=True):
        staff: StaffUser = super().save(commit=False)
        staff.is_staff = True
        if commit:
            staff.save()
            self.save_m2m()
        return staff


@admin.register(StaffUser)
class StaffUserAdmin(HashPasswordMixin, ModelAdmin):
    form = StaffForm
    list_display = ("display_header", "is_active", "is_superuser", "date_joined")
    fieldsets = (
        (
            "Information",
            {"fields": ("username", "phone_number", "password", "image", "date_joined")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_superuser", "groups", "user_permissions")},
        ),
    )

    add_fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "username",
                    "password",
                    "phone_number",
                    "image",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    search_fields = ["username"]
    list_filter = (
        "is_active",
        "is_superuser",
        "groups",
    )
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("date_joined", "is_superuser")

    @display(description=_("Staff"), header=True)
    def display_header(self, instance: StaffUser):
        return [
            instance,
            instance.phone_number,
            "ST",
            {
                "path": instance.image.url if instance.image else None,
            },
        ]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_superuser=False)

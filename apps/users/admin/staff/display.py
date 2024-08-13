from unfold.decorators import display

from apps.users.models.staff import StaffUser


class StaffDisplayMixin:
    @display(description="Staff", label=True, ordering="username")
    def display_username(self, staff: StaffUser):
        return [staff.username]

    @display(
        description="Is Active?",
        label={"True": "success", "False": "danger"},
        ordering="-is_active",
    )
    def display_is_active(self, staff: StaffUser):
        return "True" if staff.is_active else "False"

    @display(
        description="Is Superuser?",
        label={"True": "success", "False": "danger"},
        ordering="is_superuser",
    )
    def display_is_superuser(self, staff: StaffUser):
        return "True" if staff.is_superuser else "False"

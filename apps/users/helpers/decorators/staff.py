from unfold.decorators import display

from apps.users.models.staff import StaffUser


class StaffDisplay:
    @display(description="Staff", header=True)
    def display_header(self, staff: StaffUser):
        return [
            staff,
            staff.phone_number,
            "ST",
            {
                "path": staff.image.url if staff.image else None,
            },
        ]

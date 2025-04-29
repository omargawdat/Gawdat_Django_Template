from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from apps.users.models import User


class AdminUser(User):
    image = ProcessedImageField(
        upload_to="users/",
        processors=[ResizeToFit(1200, 800)],
        options={"quality": 90, "optimize": True},
        verbose_name=_("Image"),
        null=True,
    )
    can_access_money = models.BooleanField(
        default=False,
        verbose_name=_("Can access money"),
        help_text=_("Allow this user to access money like process wallet money"),
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = True
        super().save(*args, **kwargs)

from django.contrib import admin
from django.contrib import messages
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from unfold.decorators import action
from unfold.enums import ActionVariant

from apps.appInfo.models.contact_us import ContactUs
from common.base.admin import BaseModelAdmin

from .change_view import ContactUsChangeView
from .display import ContactUsDisplayMixin
from .list_view import ContactUsListView
from .permissions import ContactUsAdminPermissions


@admin.register(ContactUs)
class ContactUsAdmin(
    ContactUsDisplayMixin,
    ContactUsListView,
    ContactUsChangeView,
    ContactUsAdminPermissions,
    BaseModelAdmin,
):
    inlines = []

    actions_detail = [
        "mark_as_checked",
    ]

    def has_changeform_submitline_action_permission(
        self, request: HttpRequest, object_id: str | int
    ):
        contact = get_object_or_404(ContactUs, id=object_id)
        return not contact.has_checked

    @action(
        description=_("Checked"),
        icon="check",
        variant=ActionVariant.SUCCESS,
        permissions=["changeform_submitline_action"],
    )
    def mark_as_checked(self, request: HttpRequest, object_id: int):
        contact_us = get_object_or_404(ContactUs, id=object_id)
        contact_us.has_checked = True
        contact_us.save(update_fields=["has_checked"])
        messages.success(request, _("Marked as checked."))
        admin_change_url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=[object_id],
        )
        return HttpResponseRedirect(admin_change_url)

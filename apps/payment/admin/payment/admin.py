from django.contrib import admin
from import_export.formats.base_formats import XLSX
from unfold.contrib.import_export.forms import ExportForm

from apps.payment.models.payment import Payment
from common.base.admin import BaseModelAdmin

from .change_view import PaymentChangeView
from .display import PaymentDisplayMixin
from .list_view import PaymentListView
from .permissions import PaymentAdminPermissions
from .resource import PaymentResource


@admin.register(Payment)
class PaymentAdmin(
    PaymentDisplayMixin,
    PaymentListView,
    PaymentChangeView,
    PaymentAdminPermissions,
    BaseModelAdmin,
):
    resource_class = PaymentResource
    export_form_class = ExportForm
    formats = [XLSX]

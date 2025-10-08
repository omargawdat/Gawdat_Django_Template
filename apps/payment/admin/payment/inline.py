from apps.payment.models.payment import Payment
from common.base.admin import BaseTabularInline

from .permissions import PaymentInlinePermissions


class PaymentInline(PaymentInlinePermissions, BaseTabularInline):
    model = Payment
    extra = 0
    show_change_link = True
    tab = True
    fields = ()
    autocomplete_fields = ()

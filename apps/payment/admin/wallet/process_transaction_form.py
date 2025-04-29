from decimal import Decimal

from django import forms
from django.utils.translation import gettext_lazy as _
from unfold.widgets import UnfoldAdminFileFieldWidget
from unfold.widgets import UnfoldAdminSelectWidget
from unfold.widgets import UnfoldAdminTextareaWidget
from unfold.widgets import UnfoldAdminTextInputWidget

from apps.payment.constants import WalletTransactionType


class WalletTransactionForm(forms.Form):
    transaction_type = forms.ChoiceField(
        label=_("Transaction Type"),
        choices=WalletTransactionType.choices,
        widget=UnfoldAdminSelectWidget,
    )
    amount = forms.DecimalField(
        label=_("Amount"),
        widget=UnfoldAdminTextInputWidget,
        decimal_places=2,
        min_value=Decimal("-5000.00"),
        max_value=Decimal("5000.00"),
        help_text=_("negative to deduct - positive to add."),
    )
    note = forms.CharField(
        label=_("Transaction Note"),
        widget=UnfoldAdminTextareaWidget,
        max_length=1500,
    )
    attachment = forms.FileField(
        label=_("Attachment"),
        required=False,
        widget=UnfoldAdminFileFieldWidget,
    )

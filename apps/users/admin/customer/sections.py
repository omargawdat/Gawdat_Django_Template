from django.contrib.admin.utils import display_for_field
from django.contrib.admin.utils import label_for_field
from django.contrib.admin.utils import lookup_field
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.sections import TableSection


class ClientTableSection(TableSection):
    verbose_name = _("The Latest 7 Client's Payments")
    related_name = "payments"
    height = 300
    fields = [
        "id",
        "price_after_discount",
        "payment_type",
        "status",
        "created_at",
        "view_detail",
    ]

    def status(self, instance):
        """Display is_paid with color."""
        if instance.is_paid:
            return format_html(
                '<span style="color: green;">Paid</span>',
            )
        return format_html(
            '<span style="color: red;">Unpaid</span>',
        )

    status.short_description = _("Status")

    def created_at(self, instance):
        """Format created_at datetime."""
        return instance.created_at.strftime("%Y-%m-%d %H:%M")

    created_at.short_description = _("Created At")

    def view_detail(self, instance):
        """Link to payment detail."""
        url = reverse("admin:payment_payment_change", args=[instance.pk])
        return format_html('<a href="{}">👁</a>', url)

    view_detail.short_description = _("Detail")

    def render(self) -> str:
        results = getattr(self.instance, self.related_name)
        headers = []
        rows = []

        for field_name in self.fields:
            if hasattr(self, field_name):
                if hasattr(getattr(self, field_name), "short_description"):
                    headers.append(getattr(self, field_name).short_description)
                else:
                    headers.append(field_name)
            else:
                headers.append(label_for_field(field_name, results.model))

        # Get latest 7 payments
        filtered_results = results.order_by("-created_at")[:7]

        for result in filtered_results:
            row = []
            for field_name in self.fields:
                if hasattr(self, field_name):
                    row.append(getattr(self, field_name)(result))
                else:
                    field, _attr, value = lookup_field(field_name, result)
                    row.append(display_for_field(value, field, "-"))
            rows.append(row)

        context = {
            "request": self.request,
            "table": {
                "headers": headers,
                "rows": rows,
            },
        }

        if hasattr(self, "verbose_name") and self.verbose_name:
            context["title"] = self.verbose_name

        if hasattr(self, "height") and self.height:
            context["height"] = self.height

        return render_to_string(
            "unfold/components/table.html",
            context=context,
        )

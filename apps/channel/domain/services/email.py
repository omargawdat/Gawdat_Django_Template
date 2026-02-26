from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailService:
    """Handles sending templated HTML emails."""

    @staticmethod
    def send_email(
        *,
        subject: str,
        recipient_list: list[str],
        template_name: str,
        context: dict | None = None,
    ) -> None:
        """Send an HTML email using a Django template."""
        html_message = render_to_string(template_name, context or {})
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)

    @staticmethod
    def schedule_email(
        *,
        subject: str,
        recipient_list: list[str],
        template_name: str,
        context: dict | None = None,
    ) -> None:
        """Enqueue email delivery as a background task."""
        from apps.channel.tasks import send_email_task

        send_email_task.enqueue(
            subject=subject,
            recipient_list=recipient_list,
            template_name=template_name,
            context=context,
        )

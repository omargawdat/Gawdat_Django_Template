from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config.helpers.env import env


class EmailService:
    def __init__(self):
        self.from_email = env.email_host_user

    def send_email(
        self,
        subject,
        message,
        recipient_list,
        template_name=None,
        context=None,
        attachments=None,
    ):
        email = EmailMultiAlternatives(
            subject=subject, body=message, from_email=self.from_email, to=recipient_list
        )

        if template_name:
            html_message = render_to_string(template_name, context or {})
            email.attach_alternative(html_message, "text/html")

        if attachments:
            for attachment in attachments:
                email.attach(*attachment)

        email.send(fail_silently=False)

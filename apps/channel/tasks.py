import logging

from django_tasks import task

logger = logging.getLogger(__name__)


@task()
def send_email_task(
    *,
    subject: str,
    recipient_list: list[str],
    template_name: str,
    context: dict | None = None,
) -> None:
    """Background task for sending templated HTML emails."""
    from apps.channel.domain.services.email import EmailService

    try:
        EmailService.send_email(
            subject=subject,
            recipient_list=recipient_list,
            template_name=template_name,
            context=context,
        )
    except Exception:
        logger.exception(
            "Failed to send email to %s with subject '%s'",
            recipient_list,
            subject,
        )
        raise

import logging

from django.core.cache import cache
from django.dispatch import receiver
from django_tasks.signals import task_finished

logger = logging.getLogger(__name__)


@receiver(task_finished)
def retry_failed_tasks(sender, task_result, **kwargs):
    if task_result.status != "FAILED":
        return

    cache_key = f"task_retry_count_{task_result.id}"
    retry_count = cache.get(cache_key, 0)

    MAX_RETRY = 2
    if retry_count >= MAX_RETRY:
        logger.info(f"Task {task_result.id} has reached the maximum retries.")
        return

    new_task_result = task_result.task.enqueue()

    new_cache_key = f"task_retry_count_{new_task_result.id}"
    cache.set(new_cache_key, retry_count + 1, timeout=86400)
    cache.delete(cache_key)

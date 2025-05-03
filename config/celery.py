from celery import Celery

from config.redis import REDIS_CELERY_DB, REDIS_HOST, REDIS_PORT
from config.utils import is_test_environment

# https://docs.celeryq.dev/en/latest/userguide/configuration.html#new-lowercase-settings
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
NUMBER_PRIORITIES = 5
DEFAULT_QUEUE_NAME = "celery"
DEFAULT_TASK_PRIORITY = NUMBER_PRIORITIES // 2
DEFAULT_SERIALIZER = "pickle"


# https://docs.celeryq.dev/en/latest/userguide/application.html#example-3-using-a-configuration-class-object
class CeleryConfig:
    # Broker settings
    broker_url = CELERY_BROKER_URL
    result_backend = CELERY_BROKER_URL
    broker_connection_retry_on_startup = True
    task_time_limit = 60 * 60 * 1  # 1 hour
    result_expires = 60 * 60 * 24  # 1 day
    # Serialization settings
    accept_content = {"pickle", "json"}
    event_serializer = DEFAULT_SERIALIZER
    result_serializer = DEFAULT_SERIALIZER
    task_serializer = DEFAULT_SERIALIZER
    worker_send_task_events = True
    # Queue priority settings
    task_default_queue = DEFAULT_QUEUE_NAME
    broker_transport_options = {
        # 20 minutes - send task to another worker if not acked
        "visibility_timeout": 60 * 20,
        "sep": "-prio-",
        "priority_steps": list(range(NUMBER_PRIORITIES)),
        "queue_order_strategy": "priority",
    }
    task_default_priority = DEFAULT_TASK_PRIORITY
    # Settings to prevent losing tasks
    task_acks_late = False
    task_reject_on_worker_lost = True
    worker_prefetch_multiplier = 2
    task_store_errors_even_if_ignored = True
    # Force eager (synchronous) execution of Celery tasks for CI environment
    task_always_eager = is_test_environment()
    task_eager_propagates = is_test_environment()
    # Import tasks from modules other than tasks.py
    imports = ["experiments.tasks"]


# Initialize Celery app
app = Celery("experiments_api", config_source=CeleryConfig)


# Auto load tasks.py modules from all registered Django apps.
app.autodiscover_tasks()


if __name__ == "__main__":
    """
    Allow to launch celery worker with autoreload.
    Just replace normal celery launch command with:
        python -m config.celery <args>
    The args are exactly the same.

    For example:
        celery -A config.celery worker -Q celeryQ -l info --autoscale 2,1
    should become:
        python -m config.celery worker -Q celeryQ -l info --autoscale 2,1
    """
    import sys

    import django

    django.setup()

    from django.utils import autoreload

    args = sys.argv[1:]
    print(f"Starting celery worker with autoreload: {args=}")
    autoreload.run_with_reloader(app.worker_main, args)

# This will make sure the Celery app is always imported
# when Django starts so that shared_task will use this app.
from .celery import app as celery_app

__version__ = "v0.0.0"
__date__ = "2025-04-26"
__all__ = (
    "__version__",
    "celery_app",
)

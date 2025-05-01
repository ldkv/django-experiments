import os
import time

from gunicorn.http.message import Request
from gunicorn.workers.gthread import ThreadWorker

API_PORT = int(os.environ.get("API_PORT", "8000"))
LONG_API_REQUEST_THRESHOLD_SECONDS = int(os.environ.get("LONG_API_REQUEST_THRESHOLD_SECONDS", "2"))
GUNICORN_WORKERS = int(os.environ.get("GUNICORN_WORKERS", "5"))
GUNICORN_WORKER_TIMEOUT = int(os.environ.get("GUNICORN_WORKER_TIMEOUT", "30"))

# Gunicorn settings
# https://docs.gunicorn.org/en/stable/settings.html
wsgi_app = "config.wsgi:application"
bind = f"0.0.0.0:{API_PORT}"
worker_class = "sync"
workers = GUNICORN_WORKERS
threads = 1
timeout = GUNICORN_WORKER_TIMEOUT
access_log_format = '%({x-forwarded-for}i)s %(u)s %(p)s - "%(r)s" %(M)sms %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = "-"
errorlog = "-"
capture_output = True
loglevel = "info"


def worker_abort(worker: ThreadWorker):
    """
    This hook is called when a Gunicorn worker is aborted, which is most likely due to a timeout.
    This is useful to catch the worker stack trace.

    Guide: https://amalgjose.com/2021/03/23/how-to-configure-hooks-in-python-gunicorn/
    """
    raise Exception(f"Gunicorn worker aborted: {worker}")


def pre_request(worker: ThreadWorker, request: Request) -> None:
    """Log requests timestamp before processing."""
    request.start_time = time.time()
    worker.log.info(f"pre_request: {request.method} {request.uri}")


def post_request(worker: ThreadWorker, request: Request) -> None:
    """Log requests with long duration."""
    end_time = time.time()
    duration = end_time - request.start_time
    if duration > LONG_API_REQUEST_THRESHOLD_SECONDS:
        worker.log.warning(f"{request.method} {request.uri} took {duration:.2f} s.")

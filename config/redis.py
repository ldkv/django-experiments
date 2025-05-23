import os
from functools import lru_cache

from redis import Redis

from config.utils import is_test_environment

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_DJANGO_DB = 0
REDIS_CELERY_DB = 1
REDIS_CACHE_DB = 2
MAX_CACHED_REDIS_CLIENTS = 3  # Number of defined Redis DBs above


@lru_cache(maxsize=MAX_CACHED_REDIS_CLIENTS)
def get_redis_client(host: str = REDIS_HOST, port: int = REDIS_PORT, db: int = REDIS_CACHE_DB) -> Redis:
    # Use fakeredis for CI environment
    if is_test_environment():
        import fakeredis

        return fakeredis.FakeStrictRedis()

    return Redis(host=host, port=port, db=db)

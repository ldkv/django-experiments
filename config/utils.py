import os

TEST_ENV_KEY = "PYTEST_VERSION"


def is_test_environment() -> bool:
    return os.environ.get(TEST_ENV_KEY) is not None

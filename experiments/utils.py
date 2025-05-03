import json
import time
from typing import Any

from faker import Faker

fake = Faker()


def timeit(func):
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"{func.__name__} took {duration:.2f} seconds")
        return result

    return wrapper


def generate_fake_profile(columns: list[str] | None = None) -> dict[str, Any]:
    profile = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "age": fake.random_int(min=18, max=90),
        "email": fake.email(),
    }
    if columns:
        profile = {column: profile[column] for column in columns}

    return profile


def generate_random_inputs(number_of_inputs: int, columns: list[str]) -> list[tuple]:
    full_profiles = [generate_fake_profile(columns) for _ in range(number_of_inputs)]
    return [tuple(full_profile[column] for column in columns) for full_profile in full_profiles]


def save_query(query_str: str, filename: str = "query.sql"):
    with open(filename, "w") as f:
        f.write(str(query_str))


def save_to_json(data: dict, filename: str):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

import logging
import random
import time
from typing import Callable

from django.db import models
from django.db.models import Avg, BooleanField, Q
from django.db.models.expressions import RawSQL
from django.db.models.fields.tuple_lookups import Tuple, TupleIn

from experiments.utils import generate_fake_profile, generate_random_inputs, timeit

logger = logging.getLogger(__name__)

DEFAULT_INPUT_SIZE = 100
DEFAULT_NUMBER_RUNS = 2
DEFAULT_BULK_SIZE = 10_000
DEFAULT_FAKE_INPUTS_PERCENT = 10
ALL_INPUT_COLUMNS = ["first_name", "last_name", "age", "email"]


class ExperimentBase(models.Model):
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    age = models.IntegerField(db_index=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["first_name", "last_name"], name="%(class)s_name_index"),
        ]
        abstract = True

    objects: models.Manager["ExperimentBase"]

    # Must be set by subclass
    _max_count = -1

    @classmethod
    def submodels_by_size(cls) -> dict[str, type["ExperimentBase"]]:
        submodels = {}
        for submodel in cls.__subclasses__():
            if submodel._max_count == -1:
                continue
            key = f"{submodel._max_count // 1_000_000}M"
            submodels[key] = submodel

        return submodels

    @classmethod
    def run_experiments(
        cls, input_size: int = DEFAULT_INPUT_SIZE, number_runs: int = DEFAULT_NUMBER_RUNS
    ) -> dict[str, float]:
        duration_by_method = {}
        logger.info(f"Testing {cls.__name__} with {input_size} inputs and {number_runs} runs...")
        for method in cls.experiment_methods():
            logger.info(f"Testing {method.__name__}...")
            total_duration = 0.0
            for i in range(number_runs):
                logger.info(f"Run {i + 1}/{number_runs}...")
                inputs = cls.generate_inputs(input_size)
                # Only measure the experiment method
                start_time = time.perf_counter()
                method(inputs)
                total_duration += time.perf_counter() - start_time

            average_duration = total_duration / number_runs
            duration_by_method[method.__name__] = average_duration
            logger.info(f"Average runtime for {method.__name__}: {average_duration:.2f} s")

        return duration_by_method

    @classmethod
    def experiment_methods(cls) -> list[Callable]:
        return [
            cls.filter_rows_with_in_tuples,
            cls.filter_rows_with_conditions,
        ]

    @classmethod
    def bulk_generate_rows(cls, number_of_rows: int | None = None, bulk_size: int = DEFAULT_BULK_SIZE) -> None:
        """Generate rows in bulk until the table reach its maximum number of rows.

        :param number_of_rows: limit the number of rows to generate if provided.
        :param bulk_size: customizable bulk size for each creation.
        """
        current_count = cls.objects.count()
        max_rows_to_create = cls._max_count - current_count
        number_of_rows = number_of_rows or max_rows_to_create
        number_to_create = min(number_of_rows, max_rows_to_create)
        logger.info(f"Generating rows for {cls.__name__}: {current_count=} | {number_to_create=}")
        while number_to_create > 0:
            bulk_size = min(number_to_create, bulk_size)
            cls.objects.bulk_create([cls(**generate_fake_profile()) for _ in range(bulk_size)])
            number_to_create -= bulk_size
            logger.info(f"Number to create remaining: {number_to_create}")

    @classmethod
    def generate_inputs(
        cls,
        number_of_inputs: int = DEFAULT_INPUT_SIZE,
        columns: list[str] | None = None,
        max_offset: int | None = None,
        fake_percent: int = DEFAULT_FAKE_INPUTS_PERCENT,
    ) -> list[tuple[str, str]]:
        columns = columns or ["first_name", "last_name"]
        number_fake_inputs = int(number_of_inputs * fake_percent / 100)
        fake_inputs = generate_random_inputs(number_fake_inputs, columns)

        # Get inputs from the database
        number_real_inputs = number_of_inputs - number_fake_inputs
        max_offset = max_offset or cls._max_count
        random_offset = random.randint(0, max_offset - number_real_inputs)
        real_inputs = cls.objects.values_list(*columns)[random_offset : random_offset + number_real_inputs]

        # Combine real and fake inputs
        return list(real_inputs) + list(fake_inputs)

    @classmethod
    def filter_rows_with_conditions(cls, inputs: list[tuple], input_columns: list[str]) -> float:
        """
        Equivalent SQL:

        SELECT AVG(age)
        FROM experiments
        WHERE (first_name = 'John' AND last_name = 'Doe')
            OR (first_name = 'Jane'AND last_name = 'Doe')
            OR (first_name = 'John' AND last_name = 'Smith')
            OR (first_name = 'Jane' AND last_name = 'Smith')
            ...
        ;
        """
        conditions = Q()
        for input_tuple in inputs:
            conditions |= Q(**dict(zip(input_columns, input_tuple, strict=True)))

        query = cls.objects.filter(conditions)
        average_age = query.aggregate(Avg("age"))["age__avg"]
        return average_age

    @classmethod
    def filter_rows_with_in_tuples(cls, inputs: list[tuple], input_columns: list[str]) -> float:
        """
        Equivalent SQL:

        SELECT AVG(age)
        FROM experiments
        WHERE (first_name, last_name) IN (
            ('John', 'Doe'),
            ('Jane', 'Doe'),
            ('John', 'Smith'),
            ('Jane', 'Smith'),
            ...
        );
        """
        query = cls.objects.filter(TupleIn(Tuple(*input_columns), inputs))
        average_age = query.aggregate(Avg("age"))["age__avg"]
        return average_age

    @timeit
    @classmethod
    def filter_rows_with_in_tuples_legacy(cls, inputs: list[tuple[str, str]]) -> float:
        qs = cls.objects.filter(RawSQL("(first_name, last_name) in %s", (inputs,), output_field=BooleanField()))
        # save_query(qs.query, "query_with_in_tuples_legacy.sql")
        average_age = qs.aggregate(Avg("age"))["age__avg"]
        return average_age


class Experiment5M(ExperimentBase):
    _max_count = 5_000_000


class Experiment10M(ExperimentBase):
    _max_count = 10_000_000


class Experiment20M(ExperimentBase):
    _max_count = 20_000_000


class Experiment50M(ExperimentBase):
    _max_count = 50_000_000

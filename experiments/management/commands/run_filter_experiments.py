import time

from django.core.management.base import BaseCommand

from experiments.graph import plot_graph
from experiments.models import (
    ALL_INPUT_COLUMNS,
    DEFAULT_FAKE_INPUTS_PERCENT,
    DEFAULT_INPUT_SIZE,
    DEFAULT_NUMBER_RUNS,
    ExperimentBase,
)
from experiments.utils import save_to_json


def run_experiment(
    input_size: int,
    input_columns: int,
    number_runs: int,
    fake_inputs_percent: int = DEFAULT_FAKE_INPUTS_PERCENT,
    reverse_order: bool = False,
):
    columns = ALL_INPUT_COLUMNS[:input_columns]
    results = {
        "input_size": input_size,
        "columns": columns,
        "number_runs": number_runs,
        "fake_inputs_percent": fake_inputs_percent,
    }
    experiment_methods = ExperimentBase.experiment_methods()
    if reverse_order:
        experiment_methods.reverse()
    for base_method in experiment_methods:
        method_name = base_method.__name__
        for experiment_table in ExperimentBase.submodels_by_size().values():
            table_name = experiment_table.__name__
            print(f"Testing {method_name} for {table_name}...")
            method = getattr(experiment_table, method_name)
            total_duration = 0.0
            for i in range(number_runs):
                print(f"Run {i + 1}/{number_runs}...")
                inputs = experiment_table.generate_inputs(input_size, columns, fake_percent=fake_inputs_percent)
                # Only measure the experiment method
                start_time = time.perf_counter()
                method(inputs, columns)
                total_duration += time.perf_counter() - start_time

            average_duration_ms = (total_duration / number_runs) * 1000
            print(f"Average runtime for {method_name}/{table_name}: {average_duration_ms:.2f} ms")

            if table_name not in results:
                results[table_name] = {}
            results[table_name][method_name] = average_duration_ms  # type: ignore[index]

    # Save final results to JSON
    json_filename = f"experiments_{number_runs}runs_{fake_inputs_percent}fake_{input_size}size_{input_columns}cols.json"
    save_to_json(results, json_filename)

    # Generate graph
    plot_graph(json_filename)

    print(f"Experiments completed. Results saved to {json_filename}")


class Command(BaseCommand):
    help = "Run filter experiments. Example: python manage.py run_filter_experiments --input-size 100 --input-columns 2"

    def add_arguments(self, parser):
        parser.add_argument("--input-size", type=int, default=DEFAULT_INPUT_SIZE)
        parser.add_argument("--input-columns", type=int, default=2)
        parser.add_argument("--number-runs", type=int, default=DEFAULT_NUMBER_RUNS)
        parser.add_argument("--fake-inputs-percent", type=int, default=DEFAULT_FAKE_INPUTS_PERCENT)
        parser.add_argument("--reverse-order", action="store_true", default=False)

    def handle(self, *args, **options):
        input_size = options.get("input_size")
        input_columns = options.get("input_columns")
        number_runs = options.get("number_runs")
        fake_inputs_percent = options.get("fake_inputs_percent")
        reverse_order = options.get("reverse_order")

        for input_size in [100, 200, 500, 1000]:
            for input_columns in [2, 3, 4]:
                run_experiment(input_size, input_columns, number_runs, fake_inputs_percent, reverse_order)

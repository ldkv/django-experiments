import random

import pytest

from experiments.models import ALL_INPUT_COLUMNS, ExperimentBase


@pytest.mark.django_db
def test_same_output_for_experiment_methods() -> None:
    experiment_table = random.choice(list(ExperimentBase.submodels_by_size().values()))
    # Generate random rows
    random_rows = random.randint(1, 100)
    experiment_table.bulk_generate_rows(number_of_rows=random_rows)

    # Test with random inputs
    random_input_size = random.randint(1, 20)
    input_columns = ALL_INPUT_COLUMNS[: random.randint(2, 4)]
    inputs = experiment_table.generate_inputs(random_input_size, input_columns, max_offset=random_rows)
    outputs = []
    for method in experiment_table.experiment_methods():
        outputs.append(method(inputs, input_columns))

    number_methods = len(experiment_table.experiment_methods())
    assert len(outputs) == number_methods, (
        f"Different number of outputs than experiment methods: {len(outputs)=} | {number_methods=}"
    )
    assert len(set(outputs)) == 1, f"Outputs are not exactly the same: {outputs=}"

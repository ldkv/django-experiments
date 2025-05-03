import json

import matplotlib.pyplot as plt

BAR_SIZE = 0.3


def plot_graph(filename: str) -> str:
    with open(filename) as f:
        experiments_data: dict = json.load(f)

    # Prepare data for plotting
    experiments = [k for k in experiments_data.keys() if k.startswith("Experiment")]
    methods = sorted(experiments_data[experiments[0]].keys())
    runtime_by_method = {method: [experiments_data[exp][method] for exp in experiments] for method in methods}

    y = range(len(experiments))
    height = BAR_SIZE

    _, ax = plt.subplots()
    for i, method in enumerate(methods):
        ax.barh([j - height / 2 + i * height for j in y], runtime_by_method[method], height, label=method)

    ax.set_yticks(y)
    ax.set_yticklabels([exp.replace("Experiment", "") for exp in experiments])
    ax.set_xlabel("Average runtime (ms) - lower is better")
    ax.set_ylabel("Table size (Millions)")
    graph_title = f"runs={experiments_data['number_runs']} || input_size={experiments_data['input_size']} || columns={len(experiments_data['columns'])}"
    ax.set_title(graph_title)
    # Reverse the order of the legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])
    plt.tight_layout()

    # Add value labels to bars
    max_width = 0
    for container in ax.containers:
        for bar in container:
            width = bar.get_width()
            height = bar.get_y() + bar.get_height() / 2
            max_width = max(max_width, width)
            ax.text(width, height, f"{width:.2f}", ha="left", va="center")

    # Add padding to the x-axis so text fits
    ax.set_xlim(right=max_width * 1.10)  # 10% padding

    output_filename = f"plot_{filename.replace('.json', '')}.png"
    plt.savefig(output_filename)

    return output_filename


if __name__ == "__main__":
    filenames = [
        "experiments_200runs_10fake_100size_2cols.json",
        "experiments_200runs_10fake_100size_3cols.json",
        "experiments_200runs_10fake_100size_4cols.json",
    ]
    for filename in filenames:
        plot_graph(filename)

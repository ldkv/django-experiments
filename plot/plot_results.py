import matplotlib.pyplot as plt

data_200runs_10fake_100size = {
    "2 Columns": {
        "5M": {"tuples": 40.37, "conditions": 47.17},
        "10M": {"tuples": 67.86, "conditions": 73.25},
        "20M": {"tuples": 118.68, "conditions": 120.98},
        "50M": {"tuples": 311.60, "conditions": 271.15},
    },
    "3 Columns": {
        "5M": {"tuples": 41.27, "conditions": 39.84},
        "10M": {"tuples": 85.86, "conditions": 97.60},
        "20M": {"tuples": 186.11, "conditions": 208.38},
        "50M": {"tuples": 888.73, "conditions": 894.51},
    },
    "4 Columns": {
        "5M": {"tuples": 40.74, "conditions": 46.88},
        "10M": {"tuples": 91.80, "conditions": 96.88},
        "20M": {"tuples": 199.40, "conditions": 205.20},
        "50M": {"tuples": 904.46, "conditions": 1027.91},
    },
}

data_200runs_10fake_200size = {
    "2 Columns": {
        "5M": {"tuples": 16.00, "conditions": 47.09},
        "10M": {"tuples": 75.47, "conditions": 118.30},
        "20M": {"tuples": 220.84, "conditions": 204.22},
        "50M": {"tuples": 457.63, "conditions": 439.38},
    },
    "3 Columns": {
        "5M": {"tuples": 78.35, "conditions": 81.92},
        "10M": {"tuples": 183.72, "conditions": 187.51},
        "20M": {"tuples": 515.70, "conditions": 499.34},
        "50M": {"tuples": 6330.45, "conditions": 6019.89},
    },
    "4 Columns": {
        "5M": {"tuples": 79.60, "conditions": 88.23},
        "10M": {"tuples": 183.50, "conditions": 204.45},
        "20M": {"tuples": 537.60, "conditions": 551.31},
        "50M": {"tuples": 6132.87, "conditions": 5892.50},
    },
}


data_200runs_10fake_500size = {
    "2 Columns": {
        "5M": {"tuples": 101.41, "conditions": 88.00},
        "10M": {"tuples": 445.00, "conditions": 453.16},
        "20M": {"tuples": 874.98, "conditions": 894.18},
        "50M": {"tuples": 1612.65, "conditions": 1813.69},
    },
    "3 Columns": {
        "5M": {"tuples": 498.82, "conditions": 511.50},
        "10M": {"tuples": 875.42, "conditions": 870.41},
        "20M": {"tuples": 6873.76, "conditions": 6816.49},
        "50M": {"tuples": 28418.94, "conditions": 28647.71},
    },
    "4 Columns": {
        "5M": {"tuples": 631.32, "conditions": 641.60},
        "10M": {"tuples": 976.52, "conditions": 987.06},
        "20M": {"tuples": 7014.91, "conditions": 7167.83},
        "50M": {"tuples": 30605.16, "conditions": 31366.24},
    },
}

data_200runs_10fake_1000size = {
    "2 Columns": {
        "5M": {"tuples": 840.32, "conditions": 824.89},
        "10M": {"tuples": 3151.48, "conditions": 3291.13},
        "20M": {"tuples": 5561.74, "conditions": 5348.29},
        "50M": {"tuples": 14645.16, "conditions": 14064.40},
    },
    "3 Columns": {
        "5M": {"tuples": 1342.87, "conditions": 1350.06},
        "10M": {"tuples": 15590.67, "conditions": 15975.14},
        "20M": {"tuples": 40603.01, "conditions": 40385.59},
        "50M": {"tuples": 104363.03, "conditions": 109039.78},
    },
}
table_sizes = ["5M", "10M", "20M", "50M"]
# Set up the y-axis positions
y = range(len(table_sizes))
bar_height = 0.12  # Height of each bar
# Calculate the offset for each column configuration
offsets = [-bar_height * 2, 0, bar_height * 2]
# Define colors for each column configuration
colors = {
    "2 Columns": "#2ecc71",  # Green
    "3 Columns": "#3498db",  # Blue
    "4 Columns": "#e74c3c",  # Red
}


def plot_results(experiments_data: dict, input_size: int):
    # Set up the figure and axis
    _, ax = plt.subplots(figsize=(15, 8))

    max_value = max(
        experiments_data[config][table_size][metric]
        for config in experiments_data.keys()
        for table_size in table_sizes
        for metric in ["tuples", "conditions"]
    )
    # Plot bars for each table size
    for i, table_size in enumerate(table_sizes):
        for j, config in enumerate(experiments_data.keys()):
            # Get values for this table size and configuration
            tuples_value = experiments_data[config][table_size]["tuples"]
            conditions_value = experiments_data[config][table_size]["conditions"]

            # Plot bars
            ax.barh(
                y[i] + offsets[j],
                tuples_value,
                bar_height,
                label=f"{config} - Tuples" if i == 0 else None,
                color=colors[config],
            )
            ax.barh(
                y[i] + offsets[j] + bar_height,
                conditions_value,
                bar_height,
                label=f"{config} - Conditions" if i == 0 else None,
                color=colors[config],
                alpha=0.5,
            )  # Slightly transparent for conditions

            # Add value labels to the right of the bars
            ax.text(
                tuples_value + 5 * max_value / 1000,
                y[i] + offsets[j],
                f"{tuples_value:.1f}",
                ha="left",
                va="center",
                fontsize=9,
            )
            ax.text(
                conditions_value + 5 * max_value / 1000,
                y[i] + offsets[j] + bar_height,
                f"{conditions_value:.1f}",
                ha="left",
                va="center",
                fontsize=9,
            )

    # Customize the plot
    ax.set_ylabel("Table Size")
    ax.set_xlabel("Runtime (ms) - smaller is better")
    ax.set_title(f"Input Size: {input_size} - 200 runs - 10% fake inputs")
    ax.set_yticks(y)
    ax.set_yticklabels(table_sizes)

    # Add legend with reversed order
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])

    # Add grid for better readability
    ax.grid(True, axis="x", linestyle="--", alpha=0.7)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save the plot
    plt.savefig(f"performance_comparison_input{input_size}.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    plot_results(data_200runs_10fake_100size, 100)
    plot_results(data_200runs_10fake_200size, 200)
    plot_results(data_200runs_10fake_500size, 500)
    plot_results(data_200runs_10fake_1000size, 1000)

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from reportlab.platypus import Image
from io import BytesIO

def generate_plots(employee_data, kpis):
    buffers = []
    attribute_stats = []

    for kpi in kpis:
        fig, ax = plt.subplots(figsize=(6, 4))

        # Calculate statistics
        max_value = employee_data[kpi].max()
        min_value = employee_data[kpi].min()
        avg_value = employee_data[kpi].mean()

        attribute_stats.append({
            'kpi': kpi,
            'Max Value': max_value,
            'Min Value': min_value,
            'Average Value': avg_value
        })

        # Plot horizontal bars for max, min, and average values
        bar_heights = [max_value, min_value, avg_value]
        color_mapping = ['red' if value <= 3 else 'orange' if 4 <= value <= 6 else 'green' for value in bar_heights]

        # Adjust bar_width to reduce the size of the bars
        bar_width = 0.5

        bars = ax.barh(['Max', 'Min', 'Average'], bar_heights, color=color_mapping, height=bar_width)

        # Annotate the bars with values inside the bars
        for bar, value in zip(bars, bar_heights):
            bar_width = bar.get_width()
            bar_center = bar.get_x() + bar_width / 2
            ax.text(bar_center, bar.get_y() + bar.get_height() / 2, f'{value:.2f}', ha='center', va='center', color='black')

        # Create a custom legend
        legend_elements = [
            Patch(color='red', label='Critical'),
            Patch(color='orange', label='Neutral'),
            Patch(color='green', label='Excellent')
        ]

        ax.legend(handles=legend_elements, loc='upper right')

        ax.set_title(kpi)
        ax.set_xlabel('Score')
        ax.set_xlim(0, 10)
        ax.set_ylim(-0.5, 2.5)  # Adjust ylim to reduce empty space

        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffers.append(buffer)

    plot_images = [Image(buffer) for buffer in buffers]
    plt.close('all')
    return plot_images, buffers

"""
Generate CI regression heatmap using GradientBoostingRegressor explicitly.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)
os.environ.setdefault("MPLCONFIGDIR", os.path.join(project_root, ".mplconfig"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.output_paths import heatmap_image_dir
from src.visualization import create_styled_heatmap_pipeline, create_zone_pastel_colormap


def main():
    data_path = os.path.join(project_root, "data", "cleaned_data.csv")
    output_dir = heatmap_image_dir(project_root, "ci_gb")
    output_path = os.path.join(output_dir, "heatmap_ci_regression.png")

    print("=" * 60)
    print("   CI GB HEATMAP GENERATION   ")
    print("   Model: GradientBoostingRegressor")
    print("=" * 60)

    if not os.path.exists(data_path):
        print(f"Error: Data file not found: {data_path}")
        print("Please run scripts/run_analysis.py first to generate cleaned_data.csv")
        return

    df = pd.read_csv(data_path)

    _model, _fig, _ax = create_styled_heatmap_pipeline(
        df,
        target_col="CI",
        model_kind="GB",
        x1_range=(0, 100),
        x2_range=(0, 100),
        resolution=100,
        save_path=output_path,
        show_data_points=False,
        colorbar_label="CI",
        cmap=create_zone_pastel_colormap(),
        vmin=0.0,
        vmax=1.0,
        threshold=0.1,
        contour_threshold=0.1,
        contour_color="black",
        contour_linewidth=2.0,
        font_scale=2.0,
        bold=False,
        tick_step=20,
        colorbar_integer_ticks=False,
        colorbar_tick_format="%.1f",
    )

    print(f"Output file: {output_path}")
    plt.show()


if __name__ == "__main__":
    main()

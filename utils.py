import kagglehub
from pathlib import Path
import plotly.express as px
from plotly.subplots import make_subplots
import math


def download_data_from_kaggle(
    dataset: str, target_dir: str = None, force_download: bool = True
) -> None:
    print(f"Fetching {dataset}")
    cache = Path(kagglehub.dataset_download(dataset, force_download=force_download))
    target_dir = Path(target_dir)

    target_dir.mkdir(exist_ok=True)

    for each_file in cache.glob("*.csv"):
        print(f"Moving {each_file.name} to {target_dir}")

        if (existing_file := target_dir / each_file.name).exists():
            existing_file.unlink()

        each_file.rename(target_dir / each_file.name)


def box_plot(data, feature, target, width=600, height=350):
    return px.box(data, x=target, y=feature, color=target).update_layout(
        width=width,
        height=height,
        title=f"{feature.title().replace('_', ' ')} vs {target.title().replace('_', ' ')}",
    )


def plot_many(
    data,
    features,
    target,
    n_row=None,
    n_col=None,
    width=600,
    height=400,
    margins={"t": 50, "b": 50, "l": 50, "r": 50},
):
    num_features = len(features)
    if not n_row and not n_col:
        n_row = math.ceil(math.sqrt(num_features))
        n_col = math.ceil(num_features / n_row)

    plots = [box_plot(data, feature, target) for feature in features]
    titles = [each_plot.layout.title.text for each_plot in plots]
    figure = make_subplots(n_row, n_col, subplot_titles=titles)

    for i, each_plot in enumerate(plots):
        for plot_data in each_plot.data:
            figure.add_trace(plot_data, row=(i // n_col) + 1, col=(i % n_col) + 1)
    return figure.update_layout(
        width=width, height=height, margin=margins, showlegend=False
    )

import kagglehub
from pathlib import Path


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

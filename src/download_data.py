"""
Step 1: download the raw data file.

Run from the project root:
    python src/download_data.py

The file (~9 MB) is saved to data/raw/. It is NOT committed to Git
(see .gitignore) because anyone can re-download it with this script.
"""

import sys
import urllib.request

import config


def download(force: bool = False) -> None:
    """Download the OWID energy CSV unless we already have it."""
    config.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if config.RAW_DATA_FILE.exists() and not force:
        print(f"Already downloaded: {config.RAW_DATA_FILE}")
        print("Use  python src/download_data.py --force  to download again.")
        return

    print(f"Downloading {config.DATA_URL} ...")
    urllib.request.urlretrieve(config.DATA_URL, config.RAW_DATA_FILE)
    size_mb = config.RAW_DATA_FILE.stat().st_size / 1_000_000
    print(f"Saved {size_mb:.1f} MB to {config.RAW_DATA_FILE}")


if __name__ == "__main__":
    # sys.argv is the list of words typed after "python".
    download(force="--force" in sys.argv)

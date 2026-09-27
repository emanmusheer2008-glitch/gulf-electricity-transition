"""
Run the whole project from start to finish:

    python run_all.py

Steps:
    1. download the data (skipped if already downloaded)
    2. clean it
    3. calculate the summary and target tables
    4. draw the charts
"""

import sys
from pathlib import Path

# Let Python find the files inside src/
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import analysis  # noqa: E402
import clean_data  # noqa: E402
import download_data  # noqa: E402
import make_figures  # noqa: E402


def main() -> None:
    print("\n== 1. Download ==")
    download_data.download()

    print("\n== 2. Clean ==")
    clean_data.clean()

    print("\n== 3. Analyse ==")
    df = analysis.load_clean()
    latest = analysis.latest_year_rows(df)
    summary = analysis.summary_table(df)
    targets = analysis.target_check(df)
    print(summary.to_string(index=False))
    print()
    print(targets.to_string(index=False))
    analysis.write_findings(summary, targets)

    print("\n== 4. Charts ==")
    make_figures.fig_mix_over_time(df)
    make_figures.fig_latest_ranking(latest)
    make_figures.fig_per_capita(latest)
    make_figures.fig_carbon_intensity(df, latest)
    make_figures.fig_targets(df, targets)

    print("\nDone. See reports/findings.md and reports/figures/.")


if __name__ == "__main__":
    main()

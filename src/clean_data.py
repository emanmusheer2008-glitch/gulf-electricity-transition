"""
Step 2: clean the raw data and keep only what we need.

Run from the project root:
    python src/clean_data.py

What "cleaning" means here:
  1. Keep only the six GCC countries plus the World average.
  2. Keep only years from START_YEAR onwards.
  3. Keep only the columns listed in config.COLUMNS.
  4. Flag rows whose values are exactly the same as the year before.
     This is a POTENTIAL data-quality anomaly (for example, a value carried
     forward until new data is published). We flag it for review and leave
     it out; we do not claim it is a confirmed error.
  5. Save a small, tidy CSV to data/processed/.
"""

import pandas as pd

import config

# The main numeric columns we use to detect a "copied" year.
CHECK_COLUMNS = [
    "electricity_generation",
    "renewables_share_elec",
    "low_carbon_share_elec",
]


def load_raw() -> pd.DataFrame:
    """Read the raw CSV into a DataFrame (a table)."""
    if not config.RAW_DATA_FILE.exists():
        raise FileNotFoundError(
            f"{config.RAW_DATA_FILE} not found. Run  python src/download_data.py  first."
        )
    return pd.read_csv(config.RAW_DATA_FILE)


def filter_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Keep the countries, years and columns we care about."""
    places = config.GCC_COUNTRIES + ["World"]
    df = raw[raw["country"].isin(places)]
    df = df[df["year"] >= config.START_YEAR]
    df = df[config.COLUMNS].copy()
    # Drop rows with no electricity data at all (e.g. years not covered yet).
    df = df.dropna(subset=["electricity_generation", "low_carbon_share_elec"])
    return df.sort_values(["country", "year"]).reset_index(drop=True)


def flag_repeated_years(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a column 'repeated_from_previous_year'.

    It is True when every value in CHECK_COLUMNS is exactly the same as the
    previous year for the same country. Real data almost never repeats
    exactly, so this is flagged as a potential anomaly for review.
    """
    df = df.copy()
    # groupby("country") so we only compare a country with itself.
    # shift(1) moves each value down one row, giving "last year's value".
    previous = df.groupby("country")[CHECK_COLUMNS].shift(1)
    same_as_before = (df[CHECK_COLUMNS] == previous).all(axis=1)
    df["repeated_from_previous_year"] = same_as_before
    return df


def clean() -> pd.DataFrame:
    """Run all cleaning steps and save the result."""
    raw = load_raw()
    df = filter_data(raw)
    df = flag_repeated_years(df)

    flagged = df[df["repeated_from_previous_year"]]
    if not flagged.empty:
        print("Potential data-quality anomaly: these rows repeat the previous year exactly.")
        print("Flagged for review and excluded from the analysis:")
        print(flagged[["country", "year"]].to_string(index=False))

    config.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.CLEAN_DATA_FILE, index=False)
    print(f"Saved {len(df)} rows to {config.CLEAN_DATA_FILE}")
    return df


if __name__ == "__main__":
    clean()

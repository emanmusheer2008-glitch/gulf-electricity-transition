"""
Small tests that check the calculations with tiny made-up tables.

Run from the project root:
    python -m pytest

Why made-up data? Because we know the correct answer in advance, so if a
test fails we know the code (not the data) is wrong. These tests do NOT
need the internet or the downloaded file.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from analysis import latest_year_rows, recent_pace  # noqa: E402
from clean_data import flag_repeated_years  # noqa: E402


def test_recent_pace_is_average_change_per_year():
    years = pd.Series([2021, 2022, 2023, 2024])
    values = pd.Series([2.0, 3.0, 4.0, 5.0])
    # From 2.0 (2021) to 5.0 (2024) over 3 years = 1.0 point per year
    assert recent_pace(values, years, window=3) == pytest.approx(1.0)


def test_recent_pace_needs_both_years():
    years = pd.Series([2023, 2024])
    values = pd.Series([1.0, 2.0])
    with pytest.raises(ValueError):
        recent_pace(values, years, window=3)  # there is no 2021 value


def test_repeated_year_is_flagged():
    df = pd.DataFrame(
        {
            "country": ["A", "A", "A"],
            "year": [2023, 2024, 2025],
            "electricity_generation": [10.0, 11.0, 11.0],
            "renewables_share_elec": [1.0, 2.0, 2.0],
            "low_carbon_share_elec": [1.0, 2.0, 2.0],
        }
    )
    flags = flag_repeated_years(df)["repeated_from_previous_year"].tolist()
    assert flags == [False, False, True]


def test_first_row_of_each_country_is_never_flagged():
    df = pd.DataFrame(
        {
            "country": ["A", "B"],
            "year": [2024, 2024],
            "electricity_generation": [5.0, 5.0],
            "renewables_share_elec": [1.0, 1.0],
            "low_carbon_share_elec": [1.0, 1.0],
        }
    )
    # B has the same numbers as A, but they are different countries.
    assert not flag_repeated_years(df)["repeated_from_previous_year"].any()


def test_latest_year_rows_picks_most_recent_year():
    df = pd.DataFrame({"country": ["A", "A", "B"], "year": [2020, 2024, 2023], "value": [1, 2, 3]})
    latest = latest_year_rows(df).set_index("country")["year"].to_dict()
    assert latest == {"A": 2024, "B": 2023}

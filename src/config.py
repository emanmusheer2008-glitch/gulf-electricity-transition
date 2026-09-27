"""
Settings used by every other file in this project.

Keeping these values in one place means that if you want to add a country,
change the years, or update a target, you only edit this file.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Folders
# ---------------------------------------------------------------------------
# Path(__file__) is this file. .parent is the src/ folder, and .parent again
# is the project root. Building paths this way means the code works no matter
# which folder you run it from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
REPORTS_DIR = PROJECT_ROOT / "reports"

# ---------------------------------------------------------------------------
# Data source: Our World in Data (OWID) energy dataset, CC BY 4.0
# https://github.com/owid/energy-data
# ---------------------------------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
RAW_DATA_FILE = RAW_DATA_DIR / "owid-energy-data.csv"
CLEAN_DATA_FILE = PROCESSED_DATA_DIR / "gcc_electricity.csv"

# The six Gulf Cooperation Council (GCC) countries, spelled exactly as OWID spells them.
GCC_COUNTRIES = [
    "Saudi Arabia",
    "United Arab Emirates",
    "Qatar",
    "Kuwait",
    "Oman",
    "Bahrain",
]

# Short names make chart labels easier to read.
SHORT_NAMES = {
    "Saudi Arabia": "Saudi Arabia",
    "United Arab Emirates": "UAE",
    "Qatar": "Qatar",
    "Kuwait": "Kuwait",
    "Oman": "Oman",
    "Bahrain": "Bahrain",
    "World": "World",
}

START_YEAR = 2010

# Columns we keep from the ~130 columns in the original file.
# The meaning of each one is in docs/data_dictionary.md.
COLUMNS = [
    "country",
    "year",
    "population",
    "electricity_generation",   # terawatt-hours (TWh)
    "renewables_share_elec",    # % of electricity from renewables
    "solar_share_elec",         # % from solar
    "wind_share_elec",          # % from wind
    "nuclear_share_elec",       # % from nuclear
    "low_carbon_share_elec",    # % from renewables + nuclear
    "gas_share_elec",           # % from gas
    "oil_share_elec",           # % from oil
    "per_capita_electricity",   # kilowatt-hours per person
    "carbon_intensity_elec",    # grams of CO2-equivalent per kilowatt-hour
]

# ---------------------------------------------------------------------------
# Official targets (only the ones we could check against a government source)
# ---------------------------------------------------------------------------
# Each target says which column in our data it is compared with.
# IMPORTANT: government definitions are not always identical to OWID's
# definitions. See the "Limitations" section of the README.
TARGETS = [
    {
        "country": "Saudi Arabia",
        "column": "renewables_share_elec",
        "target_percent": 50.0,
        "target_year": 2030,
        "description": "Renewables ~50% of the electricity generation mix by 2030",
        "source": "Saudi Ministry of Energy, Renewable Energy programme page",
        "source_url": "https://www.moenergy.gov.sa/en/eco-system/programs/renewable-energy",
    },
    {
        "country": "United Arab Emirates",
        "column": "low_carbon_share_elec",
        "target_percent": 35.0,
        "target_year": 2031,
        "description": "Clean energy 35% of electricity generation by 2031",
        "source": "UAE Government portal, UAE Energy Strategy 2050 (updated 2023)",
        "source_url": "https://u.ae/en/about-the-uae/strategies-initiatives-and-awards/strategies-plans-and-visions/environment-and-energy/uae-energy-strategy-2050",
        # Shown on the chart: why the "recent pace" line is misleading for the UAE.
        "note": "Recent growth came mostly from the four Barakah\nnuclear reactors (the last began operating in 2024).\nThat jump will not repeat, so the dotted line\noverstates future progress.",
    },
]

# How many recent years to use when measuring the "recent pace" of change.
PACE_WINDOW_YEARS = 3

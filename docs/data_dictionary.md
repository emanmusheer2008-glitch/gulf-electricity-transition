# Data dictionary

Descriptions come from the official OWID codebook (`owid-energy-codebook.csv`). Electricity columns are sourced from Ember.

| Column | Unit | Meaning |
|---|---|---|
| `country` | — | Country or region name (e.g. "Saudi Arabia", "World") |
| `year` | — | Year of the observation |
| `population` | people | Population |
| `electricity_generation` | terawatt-hours (TWh) | Total electricity generated in the country |
| `renewables_share_elec` | % | Share of electricity from renewables (solar, wind, hydro, bioenergy, other) |
| `solar_share_elec` | % | Share of electricity from solar |
| `wind_share_elec` | % | Share of electricity from wind |
| `nuclear_share_elec` | % | Share of electricity from nuclear |
| `low_carbon_share_elec` | % | Share from renewables **plus** nuclear (sources with much lower greenhouse-gas emissions) |
| `gas_share_elec` | % | Share of electricity from gas |
| `oil_share_elec` | % | Share of electricity from oil |
| `per_capita_electricity` | kWh per person | Electricity generated divided by population |
| `carbon_intensity_elec` | g CO₂-equivalent per kWh | Greenhouse gases emitted for each kilowatt-hour of electricity generated |

## Column added by this project

| Column | Meaning |
|---|---|
| `repeated_from_previous_year` | `True` if generation, renewables share and low-carbon share are all *exactly* equal to the previous year for that country. This is a potential data-quality anomaly (the values may have been carried forward), so the row is flagged for review and excluded from the analysis. It is not treated as a confirmed error. |

## Units in plain words

- **1 kWh** (kilowatt-hour) = running a 1,000-watt device for one hour, about one hour of a small air-conditioner.
- **1 TWh** (terawatt-hour) = 1,000,000,000 kWh.
- **Percentage points** = the difference between two percentages. Going from 2% to 5% is **+3 percentage points** (but +150%).

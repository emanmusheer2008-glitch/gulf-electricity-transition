# Data folder

These files are **not stored in Git** (see `.gitignore`). They are recreated when you run the project.

| Folder | What goes here | How it is created |
|---|---|---|
| `raw/` | `owid-energy-data.csv` (~9 MB, all countries, all years) | `python src/download_data.py` |
| `processed/` | `gcc_electricity.csv` (~110 rows, GCC + World, 2010 onwards) | `python src/clean_data.py` |

## Source

- **Our World in Data — Energy dataset**
  Repository: https://github.com/owid/energy-data
  Direct file: https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv
  Codebook (meaning of every column): https://github.com/owid/energy-data/blob/master/owid-energy-codebook.csv
- The electricity columns used here come from **Ember — Yearly Electricity Data**: https://ember-energy.org/data/yearly-electricity-data/

## Licence

OWID: *"All visualizations, data, and code produced by Our World in Data are completely open access under the Creative Commons BY license."* Ember content is also released under CC BY 4.0.
This means you may use and share the data **if you give credit**. Credit is given in the README and at the bottom of every chart.

## Manual download (if the script fails)

1. Open the "Direct file" link above in your browser. The file will download.
2. Move it to `data/raw/owid-energy-data.csv`. The name must match exactly.
3. Run `python run_all.py`.

## Date accessed

September 2026. The dataset is updated regularly, so the latest year may change when you download it again.

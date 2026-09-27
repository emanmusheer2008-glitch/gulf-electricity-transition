# Learning Guide — Gulf Electricity Transition Tracker

This guide explains the project in simple English so you can understand it, run it, change it and **explain it in an interview**. Read it slowly, with the code open next to it.

---

## 1. What does this project do?

It answers one main question: **How much of the Gulf's electricity comes from clean (low-carbon) sources, and is it growing fast enough?**

In five steps it:
1. downloads a public dataset about energy in every country,
2. keeps only the six Gulf countries (plus the world average),
3. checks the data for problems,
4. calculates a few simple numbers (shares, changes, the pace needed to reach targets),
5. draws five charts.

## 2. Why does it exist?

- **Real-world relevance:** Saudi Arabia and the UAE have official clean-energy targets. Checking progress against them is a real question that governments, researchers and journalists ask.
- **Portfolio value:** it shows data sourcing, cleaning, quality checking, analysis, visualisation, testing and honest writing. It is more than a tutorial copied from the internet.
- **Learning value:** every part uses basic Python and pandas that you will use again in bigger projects (including TrafficFlowBench).

## 3. Where does the data come from?

| Layer | Who | What |
|---|---|---|
| Original measurements | Governments and utilities report electricity data | raw national statistics |
| Collector | **Ember** (an independent energy think tank) | cleans and publishes yearly electricity data for every country |
| Combiner | **Our World in Data (OWID)**, a non-profit research publication | combines Ember with other sources into one easy CSV file on GitHub |
| This project | you | downloads OWID's file and analyses the Gulf |

**Licence: CC BY 4.0.** You can use the data freely **as long as you credit the source**. That is why every chart has a "Data:" line at the bottom.

## 4. What does every folder and file do?

| File / folder | Job |
|---|---|
| `run_all.py` | The "start button". Runs every step in order. |
| `src/config.py` | Settings: country list, start year, targets, file paths. **Change settings here only.** |
| `src/download_data.py` | Step 1: downloads the CSV into `data/raw/`. Skips it if already there. |
| `src/clean_data.py` | Step 2: filters rows and columns, flags suspicious rows, saves a small CSV. |
| `src/analysis.py` | Step 3: makes the summary table and the target-check table, and writes `reports/findings.md`. |
| `src/make_figures.py` | Step 4: draws the five charts into `reports/figures/`. |
| `notebooks/01_exploration.ipynb` | Where the data was first explored. Shows the "thinking" part. |
| `tests/test_analysis.py` | Checks the calculations with tiny made-up tables. |
| `data/` | Downloaded and processed data. **Not uploaded to GitHub** (too big and can be re-downloaded). |
| `reports/` | Results: tables and charts. These **are** uploaded, so people can see them on GitHub. |
| `docs/data_dictionary.md` | What every column means, with units. |
| `requirements.txt` | The list of libraries to install. |
| `.gitignore` | Tells Git which files NOT to upload (data, caches, secrets). |
| `LICENSE` | Says others may reuse the code (MIT) and that the data has its own licence. |

## 5. Important Python concepts used

| Concept | Where | Simple explanation |
|---|---|---|
| **Functions** (`def`) | every file | A named block of code you can run again and again. `recent_pace(...)` calculates one thing and returns the answer. |
| **Modules and `import`** | `run_all.py` | Each `.py` file is a module. `import analysis` lets one file use the functions of another. |
| **`if __name__ == "__main__":`** | bottom of files | "Only run this part if the file was started directly, not when it is imported." |
| **Lists and dictionaries** | `config.py` | `GCC_COUNTRIES` is a list. Each target is a dictionary (`{"country": ..., "target_percent": ...}`). |
| **`for` loops and `zip()`** | `make_figures.py` | `zip(axes.flat, countries)` pairs each small chart panel with a country. |
| **f-strings** | everywhere | `f"{value:.1f}%"` puts a number into text with 1 decimal place. |
| **`pathlib.Path`** | `config.py` | Builds file paths that work on Windows, Mac and Linux. |
| **Exceptions** (`raise`) | `clean_data.py`, `analysis.py` | Stops the program with a clear message when something is wrong (e.g. file missing). |
| **Type hints** (`-> pd.DataFrame`) | function definitions | Notes saying what type a function returns. Python does not enforce them; they help humans read the code. |

## 6. Important libraries

| Library | Used for | Key functions in this project |
|---|---|---|
| **pandas** | tables of data (DataFrames) | `read_csv`, filtering with `df[condition]`, `groupby`, `shift`, `idxmax`, `pivot`, `to_csv`, `to_markdown` |
| **matplotlib** | charts | `plt.subplots`, `stackplot`, `barh`, `scatter`, `plot`, `axvline`, `savefig` |
| **urllib** (built into Python) | downloading a file | `urllib.request.urlretrieve` |
| **pytest** | testing | `assert`, `pytest.approx`, `pytest.raises` |
| **tabulate** | helper that lets pandas write Markdown tables | used by `to_markdown` |

## 7. How the program works, from beginning to end

```
run_all.py
   │
   ├─ 1. download_data.download()      internet ──► data/raw/owid-energy-data.csv   (23,000+ rows × 130 columns)
   │
   ├─ 2. clean_data.clean()            keep 7 places, years ≥ 2010, 13 columns
   │                                   flag rows identical to last year (Kuwait 2025)
   │                                   ──► data/processed/gcc_electricity.csv      (109 rows)
   │
   ├─ 3. analysis.*                    drop flagged rows
   │                                   summary_table()  ► first year vs latest year per country
   │                                   target_check()   ► required pace vs recent pace
   │                                   ──► reports/findings.md
   │
   └─ 4. make_figures.*                five charts ──► reports/figures/*.png
```

### The key calculation explained

**Required pace** = how much the share must grow each year to reach the target.

```
Saudi Arabia: target 50% in 2030, now 2.2% in 2024
required pace = (50 − 2.2) ÷ (2030 − 2024) = 47.8 ÷ 6 ≈ 8.0 percentage points per year
```

**Recent pace** = how much it actually grew per year recently.

```
Saudi Arabia: 0.25% in 2021 → 2.16% in 2024
recent pace = (2.16 − 0.25) ÷ 3 ≈ 0.64 points per year
```

So Saudi Arabia would need a pace roughly **12 times faster** than 2021–2024. That does *not* mean it will fail. Big solar farms can switch on in a single year. It means the growth has to speed up a lot.

### The data-quality check explained

`flag_repeated_years()` compares each row with the **same country's previous year**:
- `groupby("country")` keeps countries separate.
- `.shift(1)` moves values down one row, so each row can "see" last year's value.
- If generation, renewables share and low-carbon share are *all exactly equal*, the row is flagged.

Kuwait 2025 was flagged. Its values are identical to 2024, which is unusual for real measurements. We call it a **potential data-quality anomaly, flagged for review**, not a confirmed error. We cannot know *why* the numbers repeat (a placeholder until new data arrives? a genuine coincidence?) unless the source says so. Leaving it out is the cautious choice. Always describe what you **observed**, not what you **guess**.

## 8. How to run it

```bash
# 1. go into the project folder
cd gulf-electricity-transition

# 2. create a virtual environment (a private box for this project's libraries)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac / Linux

# 3. install libraries
pip install -r requirements.txt

# 4. run everything
python run_all.py

# 5. run the tests
python -m pytest

# 6. (optional) open the notebook
jupyter notebook notebooks/01_exploration.ipynb
```

## 9. Common errors and fixes

| Error message | Why it happens | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Libraries not installed, or virtual environment not activated | Activate `.venv`, then `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'config'` | You ran a file from the wrong folder | Run commands from the project root folder, e.g. `python src/clean_data.py` |
| `FileNotFoundError: ... not found. Run python src/download_data.py first` | The data has not been downloaded yet | Run `python run_all.py` (it downloads automatically) |
| `urllib.error.URLError` | No internet, or a firewall blocked the download | Check your internet, or follow "Manual download" in `data/README.md` |
| `ImportError: Missing optional dependency 'tabulate'` | `tabulate` not installed | `pip install tabulate` |
| `ValueError: Need data for both ... and ...` | A country is missing a year needed for the recent pace | Change `PACE_WINDOW_YEARS` in `config.py` or check the data |
| Numbers differ from the README | OWID updated the dataset | Normal. Rerun and update the README numbers. |

## 10. Questions you should be able to answer

Practise answering these **out loud, without looking**:

1. What question does this project answer, and why does it matter for the Gulf?
2. Where does the data come from? What is the difference between Ember and Our World in Data?
3. What does CC BY 4.0 allow you to do, and what must you do in return?
4. What is the difference between "renewables" and "low-carbon"? Why did you use low-carbon for the UAE?
5. What is the difference between a *percentage* and a *percentage point*?
6. Why is the raw data not uploaded to GitHub?
7. What anomaly did your code flag in the data, how did it detect it, and why do you call it an *anomaly* rather than an *error*?
8. Explain the required-pace calculation for Saudi Arabia with the actual numbers.
9. Why is the UAE's "if recent pace continued" line misleading?
10. Why didn't you use machine learning? When *would* machine learning make sense for this topic?
11. What does `groupby("country")["year"].idxmax()` do?
12. What do the tests check, and why do they use made-up data?
13. Name three limitations of your analysis.
14. If you had one more week, what would you add, and why?

## 11. Before calling this "my project"

Do these yourself. It is the difference between *having* a project and *owning* it.

- [ ] Run it on your own computer from a fresh clone.
- [ ] Change `START_YEAR` to 2000 in `config.py`, rerun, and explain what changed.
- [ ] Add "World" or another country (e.g. "Egypt") to the charts and explain the result.
- [ ] Write one new test yourself.
- [ ] Rewrite the "Key findings" section of the README in your own words.
- [ ] Answer all 14 questions above without notes.

"""
Step 4: draw the charts and save them as PNG images in reports/figures/.

Every function below makes ONE chart. They all follow the same pattern:
    1. create a figure with plt.subplots()
    2. draw the data
    3. add titles, labels and source text
    4. save with save(fig, "name.png")
"""

import matplotlib

matplotlib.use("Agg")  # draw to files, no window needed (works on servers too)
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

import config

# A small, consistent colour scheme (checked for colour-blind readability).
BLUE = "#2a78d6"     # renewables / main series
ORANGE = "#eb6834"   # nuclear
GREY = "#8a8985"     # reference lines, older values
INK = "#0b0b0b"      # main text
MUTED = "#52514e"    # secondary text
GRID = "#e4e3df"

SOURCE_NOTE = "Data: Our World in Data energy dataset, based on Ember yearly electricity data (both CC BY 4.0)"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.edgecolor": GRID,
        "axes.labelcolor": MUTED,
        "axes.titlecolor": INK,
        "axes.titlesize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "figure.dpi": 110,
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
        "figure.facecolor": "white",
    }
)


def short(name: str) -> str:
    return config.SHORT_NAMES.get(name, name)


def finish(fig, title: str, subtitle: str) -> None:
    """Lay out the panels, leaving fixed room at the top for the title and
    subtitle and at the bottom for the source note, so text never overlaps."""
    height = fig.get_size_inches()[1]
    top = 1 - 0.85 / height      # keep ~0.85 inch free at the top
    bottom = 0.35 / height       # keep ~0.35 inch free at the bottom
    fig.tight_layout(rect=(0, bottom, 1, top))
    fig.text(0.01, 1 - 0.18 / height, title, ha="left", va="top",
             fontsize=14, fontweight="bold", color=INK)
    fig.text(0.01, 1 - 0.52 / height, subtitle, ha="left", va="top",
             fontsize=10, color=MUTED)
    fig.text(0.01, 0.08 / height, SOURCE_NOTE, ha="left", va="bottom",
             fontsize=8, color=MUTED)


def save(fig, filename: str) -> None:
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = config.FIGURES_DIR / filename
    fig.savefig(path)
    plt.close(fig)
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# Figure 1: low-carbon electricity over time, one small panel per country
# ---------------------------------------------------------------------------
def fig_mix_over_time(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(11, 6), sharex=True, sharey=True)
    ymax = df[df["country"].isin(config.GCC_COUNTRIES)]["low_carbon_share_elec"].max()

    # zip() pairs each axis with a country.
    for ax, country in zip(axes.flat, config.GCC_COUNTRIES):
        c = df[df["country"] == country]
        # stackplot draws renewables first, then nuclear on top of it.
        ax.stackplot(
            c["year"],
            c["renewables_share_elec"],
            c["nuclear_share_elec"],
            colors=[BLUE, ORANGE],
            edgecolor="white",
            linewidth=0.8,
        )
        latest = c.iloc[-1]
        ax.set_title(f"{short(country)}", loc="left", fontweight="bold")
        ax.text(
            latest["year"], latest["low_carbon_share_elec"] + 1.2,
            f"{latest['low_carbon_share_elec']:.1f}%",
            ha="right", va="bottom", fontsize=9, color=INK,
        )
        ax.set_ylim(0, ymax * 1.18)
        ax.set_xlim(config.START_YEAR, c["year"].max())

    for ax in axes[:, 0]:
        ax.set_ylabel("% of electricity")

    # A single legend for the whole figure.
    handles = [plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Rectangle((0, 0), 1, 1, color=ORANGE)]
    axes.flat[0].legend(handles, ["Renewables (mostly solar)", "Nuclear"],
                        loc="upper left", frameon=False, fontsize=8)
    finish(fig, "Low-carbon electricity in the Gulf is still small — except in the UAE",
              f"Share of electricity generated from renewables and nuclear, {config.START_YEAR}–latest year")
    save(fig, "01_low_carbon_share_over_time.png")


# ---------------------------------------------------------------------------
# Figure 2: latest low-carbon share, ranked
# ---------------------------------------------------------------------------
def fig_latest_ranking(latest: pd.DataFrame) -> None:
    d = latest[latest["country"].isin(config.GCC_COUNTRIES + ["World"])]
    d = d.sort_values("low_carbon_share_elec")
    labels = [f"{short(c)} ({y})" for c, y in zip(d["country"], d["year"])]
    colors = [GREY if c == "World" else BLUE for c in d["country"]]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(labels, d["low_carbon_share_elec"], color=colors, height=0.6)
    for i, v in enumerate(d["low_carbon_share_elec"]):
        ax.text(v + 0.6, i, f"{v:.1f}%", va="center", fontsize=9, color=INK)
    ax.set_xlabel("% of electricity from renewables + nuclear")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, d["low_carbon_share_elec"].max() * 1.15)
    finish(fig, "Every GCC country is below the world average",
              "Low-carbon share of electricity in the latest year with reliable data (world shown in grey)")
    save(fig, "02_latest_low_carbon_ranking.png")


# ---------------------------------------------------------------------------
# Figure 3: electricity generated per person vs the world average
# ---------------------------------------------------------------------------
def fig_per_capita(latest: pd.DataFrame) -> None:
    d = latest[latest["country"].isin(config.GCC_COUNTRIES)]
    d = d.sort_values("per_capita_electricity")
    world = latest.loc[latest["country"] == "World", "per_capita_electricity"].iloc[0]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh([short(c) for c in d["country"]], d["per_capita_electricity"], color=BLUE, height=0.6)
    for i, v in enumerate(d["per_capita_electricity"]):
        ax.text(v + 300, i, f"{v/world:.1f}× world", va="center", fontsize=9, color=INK)
    ax.axvline(world, color=GREY, linestyle="--", linewidth=1.5)
    ax.set_ylim(-0.6, len(d) + 0.3)   # leave space above the top bar for the label
    ax.text(world + 250, len(d) - 0.35, f"World average: {world:,.0f} kWh", fontsize=8, color=MUTED, va="center")
    ax.xaxis.set_major_formatter(lambda x, pos: f"{x:,.0f}")
    ax.set_xlabel("Electricity generated per person (kWh per year)")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, d["per_capita_electricity"].max() * 1.2)
    finish(fig, "GCC countries generate 2.5–6 times more electricity per person than the world",
              "Electricity generation per person, latest year with reliable data")
    save(fig, "03_electricity_per_person.png")


# ---------------------------------------------------------------------------
# Figure 4: carbon intensity, first year vs latest year ("dumbbell" chart)
# ---------------------------------------------------------------------------
def fig_carbon_intensity(df: pd.DataFrame, latest: pd.DataFrame) -> None:
    first_year = config.START_YEAR
    first = df[df["year"] == first_year].set_index("country")["carbon_intensity_elec"]
    last = latest.set_index("country")["carbon_intensity_elec"]
    order = last[config.GCC_COUNTRIES].sort_values().index[::-1]

    fig, ax = plt.subplots(figsize=(8, 4))
    for i, c in enumerate(order):
        ax.plot([first[c], last[c]], [i, i], color=GRID, linewidth=3, zorder=1)
        ax.scatter(first[c], i, color=GREY, s=60, zorder=2, edgecolor="white", linewidth=1.5)
        ax.scatter(last[c], i, color=BLUE, s=60, zorder=3, edgecolor="white", linewidth=1.5)
        change = 100 * (last[c] / first[c] - 1)
        label = "no change" if abs(change) < 0.5 else f"{change:+.0f}%"
        ax.text(max(first[c], last[c]) + 12, i, label, va="center", fontsize=9, color=INK)
    ax.set_yticks(range(len(order)), [short(c) for c in order])
    ax.set_xlabel("Grams of CO₂-equivalent per kWh of electricity (lower is cleaner)")
    ax.grid(axis="y", visible=False)
    ax.scatter([], [], color=GREY, s=60, label=str(first_year))
    ax.scatter([], [], color=BLUE, s=60, label="Latest year")
    ax.legend(frameon=False, loc="upper right")
    finish(fig, "The UAE cut the carbon intensity of its electricity by almost a third",
              f"Greenhouse gases emitted per unit of electricity generated, {first_year} vs latest year")
    save(fig, "04_carbon_intensity_change.png")


# ---------------------------------------------------------------------------
# Figure 5: progress towards official targets
# ---------------------------------------------------------------------------
def fig_targets(df: pd.DataFrame, targets: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, len(config.TARGETS), figsize=(11, 4.6), sharey=True)

    for ax, t in zip(axes, config.TARGETS):
        c = df[df["country"] == t["country"]]
        row = targets[targets["country"] == short(t["country"])].iloc[0]
        last_year = row["latest_year"]
        current = row["current_%"]

        ax.plot(c["year"], c[t["column"]], color=BLUE, linewidth=2, label="Actual")
        # Path needed to reach the target
        ax.plot([last_year, t["target_year"]], [current, t["target_percent"]],
                color=INK, linestyle="--", linewidth=1.5, label="Path needed to reach target")
        # Straight line if the recent pace continued
        ax.plot([last_year, t["target_year"]], [current, row["if_recent_pace_continued_%"]],
                color=GREY, linestyle=":", linewidth=2, label="If recent pace continued")
        ax.scatter([t["target_year"]], [t["target_percent"]], color=INK, s=50, zorder=3)
        ax.annotate(f"Target {t['target_percent']:.0f}%", (t["target_year"], t["target_percent"]),
                    textcoords="offset points", xytext=(-8, 8), ha="right", fontsize=9)
        label = "renewables" if t["column"] == "renewables_share_elec" else "renewables + nuclear"
        ax.set_title(f"{short(t['country'])}: {label} share", loc="left", fontweight="bold")
        ax.set_ylim(0, 60)   # the grey dotted line may run off the top: that is intended
        ax.set_xlim(config.START_YEAR, t["target_year"] + 1)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        if "note" in t:
            ax.text(0.02, 0.97, t["note"], transform=ax.transAxes, fontsize=8,
                    color=MUTED, va="top", ha="left", wrap=True)

    axes[0].set_ylabel("% of electricity")
    axes[0].legend(frameon=False, loc="upper left", fontsize=8)
    for ax in axes.flat:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    finish(fig, "Saudi Arabia needs a much faster pace; the UAE is close to its target",
              "Actual share vs the straight-line path to each official target (not a forecast)")
    save(fig, "05_target_progress.png")

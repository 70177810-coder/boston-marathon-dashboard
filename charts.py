"""
charts.py — Premium Chart Functions for Boston Marathon Dashboard
Noon-inspired: Deep black + warm amber/gold/orange glow theme
"""

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

# ═══════════════════════════════════════════════════════════════
# NOON THEME — Deep Black + Warm Amber/Gold
# ═══════════════════════════════════════════════════════════════

BG_DEEP = "#08080a"
BG_CARD = "#0e0e12"
BG_CARD2 = "#121216"
BORDER = "#1f1d1a"
BORDER_WARM = "#2a2520"

TEXT_WHITE = "#f5f0e8"
TEXT_LIGHT = "#d4cfc5"
TEXT_DIM = "#8a847a"
TEXT_MUTED = "#5a5650"

AMBER = "#e8933a"
AMBER_LIGHT = "#f0a852"
AMBER_DARK = "#c47520"
GOLD = "#d4a850"
GOLD_LIGHT = "#e8c86a"
ORANGE = "#e07830"
ORANGE_DEEP = "#c85a18"
WARM_WHITE = "#f0e8d8"
COPPER = "#c88040"
BRONZE = "#b07038"
RUST = "#a85830"

MALE_COLOR = AMBER
FEMALE_COLOR = "#e86850"

PALETTE = [AMBER, ORANGE, GOLD, COPPER, BRONZE, RUST, AMBER_LIGHT, ORANGE_DEEP, GOLD_LIGHT, "#d06838"]

# Custom warm colormap
WARM_CMAP = LinearSegmentedColormap.from_list("noon_warm",
    ["#08080a", "#2a1a0a", "#5a3010", AMBER_DARK, AMBER, GOLD_LIGHT], N=256)


def _setup():
    matplotlib.rcParams.update({
        "figure.facecolor": BG_DEEP,
        "axes.facecolor": BG_CARD,
        "axes.edgecolor": BORDER,
        "axes.labelcolor": TEXT_DIM,
        "text.color": TEXT_LIGHT,
        "xtick.color": TEXT_MUTED,
        "ytick.color": TEXT_MUTED,
        "grid.color": BORDER,
        "grid.alpha": 0.4,
        "grid.linewidth": 0.3,
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 9.5,
        "legend.facecolor": BG_CARD,
        "legend.edgecolor": BORDER_WARM,
        "legend.labelcolor": TEXT_DIM,
        "legend.fontsize": 8.5,
        "figure.dpi": 130,
    })

_setup()


def _style(ax, title, xlabel="", ylabel="", grid_axis="both"):
    ax.set_title(title, fontsize=12.5, fontweight="bold", color=TEXT_WHITE,
                 pad=16, loc="left")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9, color=TEXT_DIM, labelpad=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9, color=TEXT_DIM, labelpad=10)
    ax.grid(True, alpha=0.25, color=BORDER_WARM, linewidth=0.3, axis=grid_axis)
    ax.tick_params(colors=TEXT_MUTED, labelsize=8, length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_facecolor(BG_CARD)


# ═══════════════════════════════════════════════════════════════
# 1. PIE CHART
# ═══════════════════════════════════════════════════════════════
def plot_pie_chart(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    country_counts = df["Country"].value_counts()
    top = country_counts.head(7)
    if len(country_counts) > 7:
        top["Others"] = country_counts.iloc[7:].sum()

    colors = PALETTE[:len(top)]
    wedges, texts, autotexts = ax.pie(
        top.values, labels=None, autopct="%1.1f%%",
        colors=colors, startangle=140, pctdistance=0.82,
        wedgeprops=dict(edgecolor=BG_DEEP, linewidth=2.5, width=0.42),
        textprops={"fontsize": 8, "color": TEXT_WHITE, "fontweight": "600"}
    )
    for at in autotexts:
        at.set_fontsize(7.5)
        at.set_color(WARM_WHITE)
        at.set_fontweight("bold")

    centre = plt.Circle((0, 0), 0.58, fc=BG_DEEP)
    ax.add_artist(centre)
    ax.text(0, 0.08, f"{len(df)}", ha="center", va="center",
            fontsize=18, fontweight="900", color=AMBER)
    ax.text(0, -0.15, "winners", ha="center", va="center",
            fontsize=8, fontweight="500", color=TEXT_DIM)

    ax.legend(top.index, loc="center left", bbox_to_anchor=(0.92, 0.5),
              fontsize=7.5, frameon=True, facecolor=BG_CARD, edgecolor=BORDER_WARM,
              labelcolor=TEXT_DIM, borderpad=1, handlelength=1.2)

    ax.set_title("Winners by Country", fontsize=12.5, fontweight="bold",
                 color=TEXT_WHITE, pad=12, loc="left")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 2. HISTOGRAM
# ═══════════════════════════════════════════════════════════════
def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    data = df["Time_Minutes"].dropna()
    n, bins, patches = ax.hist(data, bins=18, color=AMBER, edgecolor=BG_DEEP,
                                alpha=0.85, linewidth=1.2, zorder=3)

    max_val = max(n) if len(n) > 0 and max(n) > 0 else 1
    for count, patch in zip(n, patches):
        intensity = count / max_val
        r = 0.91 * (0.4 + intensity * 0.6)
        g = 0.58 * (0.3 + intensity * 0.7)
        b = 0.23 * (0.2 + intensity * 0.8)
        patch.set_facecolor((r, g, b, 0.5 + intensity * 0.45))

    mean_val = data.mean()
    ax.axvline(mean_val, color=GOLD_LIGHT, linestyle="--", linewidth=1.5, alpha=0.7, zorder=4)
    ax.text(mean_val + 1.5, max(n) * 0.9, f"Mean: {mean_val:.1f} min",
            color=GOLD_LIGHT, fontsize=8, fontweight="600",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_CARD, edgecolor=BORDER_WARM, alpha=0.9))

    _style(ax, "Finishing Time Distribution", "Time (Minutes)", "Frequency")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 3. LINE CHART
# ═══════════════════════════════════════════════════════════════
def plot_line_chart(df):
    fig, ax = plt.subplots(figsize=(14, 5.2))
    fig.patch.set_facecolor(BG_DEEP)

    for gender, color, lbl in [("Male", AMBER, "Men"), ("Female", FEMALE_COLOR, "Women")]:
        subset = df[df["Gender"] == gender].sort_values("Year")
        if not subset.empty:
            ax.plot(subset["Year"], subset["Time_Minutes"], color=color,
                    linewidth=2, alpha=0.85, label=lbl, zorder=3)
            ax.scatter(subset["Year"], subset["Time_Minutes"], color=color,
                       s=14, alpha=0.5, edgecolors="none", zorder=4)
            ax.fill_between(subset["Year"], subset["Time_Minutes"],
                            alpha=0.04, color=color, zorder=2)

    ax.legend(fontsize=9, loc="upper right", framealpha=0.85)
    _style(ax, "Winning Times Trend Over the Years", "Year", "Time (Minutes)")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 4. BAR CHART
# ═══════════════════════════════════════════════════════════════
def plot_bar_chart(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    top_countries = df["Country"].value_counts().head(10)
    values = top_countries.values[::-1]
    labels = top_countries.index[::-1]
    max_val = values.max() if len(values) > 0 else 1

    colors = []
    for v in values:
        ratio = v / max_val
        if ratio > 0.8: colors.append(AMBER)
        elif ratio > 0.5: colors.append(ORANGE)
        elif ratio > 0.3: colors.append(COPPER)
        else: colors.append(BRONZE)

    bars = ax.barh(range(len(values)), values, color=colors, height=0.52,
                   edgecolor="none", zorder=3, alpha=0.85)

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max_val * 0.025, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=8.5, color=AMBER_LIGHT, fontweight="700")

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlim(0, max_val * 1.18)
    _style(ax, "Top 10 Countries by Wins", "Number of Wins", "", grid_axis="x")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 5. SCATTER PLOT
# ═══════════════════════════════════════════════════════════════
def plot_scatter(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    for gender, color, lbl in [("Male", AMBER, "Men"), ("Female", FEMALE_COLOR, "Women")]:
        subset = df[df["Gender"] == gender].dropna(subset=["Time_Minutes"])
        if not subset.empty:
            ax.scatter(subset["Year"], subset["Time_Minutes"], c=color,
                       s=32, alpha=0.6, edgecolors="white", linewidths=0.2,
                       label=lbl, zorder=3)
            if len(subset) > 2:
                z = np.polyfit(subset["Year"], subset["Time_Minutes"], 2)
                p = np.poly1d(z)
                x_line = np.linspace(subset["Year"].min(), subset["Year"].max(), 100)
                ax.plot(x_line, p(x_line), color=color, linestyle="--",
                        alpha=0.35, linewidth=1.5, zorder=2)

    ax.legend(fontsize=9, framealpha=0.85)
    _style(ax, "Year vs Finishing Time", "Year", "Time (Minutes)")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 6. BOX PLOT
# ═══════════════════════════════════════════════════════════════
def plot_boxplot(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    genders = df["Gender"].unique()
    data_by_gender = [df[df["Gender"] == g]["Time_Minutes"].dropna() for g in genders]
    bp = ax.boxplot(data_by_gender, labels=genders, patch_artist=True, widths=0.4,
                    medianprops=dict(color=GOLD_LIGHT, linewidth=2.2),
                    whiskerprops=dict(color=TEXT_MUTED, linewidth=1),
                    capprops=dict(color=TEXT_MUTED, linewidth=1),
                    flierprops=dict(marker="o", markerfacecolor=ORANGE, markersize=5,
                                    alpha=0.5, markeredgecolor="none"))

    box_colors = [AMBER, FEMALE_COLOR]
    for patch, color in zip(bp["boxes"], box_colors[:len(bp["boxes"])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.45)
        patch.set_edgecolor(color)
        patch.set_linewidth(1.5)

    _style(ax, "Time Distribution by Gender", "Gender", "Time (Minutes)", grid_axis="y")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 7. HEATMAP
# ═══════════════════════════════════════════════════════════════
def plot_heatmap(df):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    numeric_cols = ["Year", "Time_Minutes", "Distance (Miles)", "Distance (KM)",
                    "Pace_Per_Mile", "Pace_Per_KM", "Speed_MPH"]
    available = [c for c in numeric_cols if c in df.columns]
    corr = df[available].corr()

    label_map = {"Time_Minutes": "Time", "Distance (Miles)": "Dist (mi)",
                 "Distance (KM)": "Dist (km)", "Pace_Per_Mile": "Pace/mi",
                 "Pace_Per_KM": "Pace/km", "Speed_MPH": "Speed"}
    corr = corr.rename(index=label_map, columns=label_map)
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    sns.heatmap(corr, mask=mask, annot=True, cmap=WARM_CMAP, fmt=".2f", ax=ax,
                linewidths=2, linecolor=BG_DEEP, cbar_kws={"shrink": 0.75, "pad": 0.02},
                annot_kws={"fontsize": 9, "fontweight": "600", "color": WARM_WHITE},
                vmin=-1, vmax=1, square=True)

    ax.tick_params(labelsize=8.5, length=0, colors=TEXT_DIM)
    _style(ax, "Feature Correlation Matrix", "", "")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 8. AREA CHART
# ═══════════════════════════════════════════════════════════════
def plot_area_chart(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    for gender, color, lbl in [("Male", AMBER, "Men"), ("Female", FEMALE_COLOR, "Women")]:
        subset = df[df["Gender"] == gender].sort_values("Year")
        if not subset.empty:
            subset = subset.copy()
            subset["Cumulative"] = range(1, len(subset) + 1)
            ax.fill_between(subset["Year"], 0, subset["Cumulative"],
                            alpha=0.12, color=color, zorder=2)
            ax.plot(subset["Year"], subset["Cumulative"], color=color,
                    linewidth=2, label=lbl, zorder=3, alpha=0.85)

    ax.legend(fontsize=9, framealpha=0.85)
    _style(ax, "Cumulative Wins Over Time", "Year", "Cumulative Wins")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 9. COUNT PLOT
# ═══════════════════════════════════════════════════════════════
def plot_countplot(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    order = sorted(df["Decade_Label"].unique())
    sns.countplot(data=df, x="Decade_Label", hue="Gender",
                  palette={"Male": AMBER, "Female": FEMALE_COLOR},
                  edgecolor="none", linewidth=0, ax=ax, order=order, alpha=0.8)

    for container in ax.containers:
        ax.bar_label(container, fontsize=6.5, color=TEXT_MUTED, padding=2, fontweight="600")

    ax.legend(fontsize=8.5, framealpha=0.85, labels=["Men", "Women"])
    _style(ax, "Winners per Decade", "Decade", "Count")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# 10. VIOLIN PLOT
# ═══════════════════════════════════════════════════════════════
def plot_violin(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    sns.violinplot(data=df, x="Gender", y="Time_Minutes", hue="Gender",
                   palette={"Male": AMBER, "Female": FEMALE_COLOR},
                   inner="quart", linewidth=1, ax=ax, alpha=0.65, legend=False)

    _style(ax, "Time Distribution Density", "Gender", "Time (Minutes)", grid_axis="y")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# BONUS 1: PAIR PLOT
# ═══════════════════════════════════════════════════════════════
def plot_pairplot(df):
    _setup()
    plot_df = df[["Year", "Time_Minutes", "Speed_MPH", "Gender"]].dropna()
    if len(plot_df) < 3:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Not enough data", ha="center", va="center",
                color=TEXT_WHITE, fontsize=14)
        return fig

    g = sns.pairplot(plot_df, hue="Gender",
                     palette={"Male": AMBER, "Female": FEMALE_COLOR},
                     diag_kind="kde", plot_kws={"alpha": 0.5, "s": 22, "edgecolors": "none"},
                     height=2.2)
    g.figure.patch.set_facecolor(BG_DEEP)
    for axi in g.axes.flatten():
        axi.set_facecolor(BG_CARD)
        for spine in axi.spines.values():
            spine.set_visible(False)
        axi.tick_params(colors=TEXT_MUTED, labelsize=6.5, length=0)
        axi.xaxis.label.set_color(TEXT_DIM)
        axi.yaxis.label.set_color(TEXT_DIM)
        axi.xaxis.label.set_fontsize(7.5)
        axi.yaxis.label.set_fontsize(7.5)
        axi.grid(True, alpha=0.15, color=BORDER_WARM, linewidth=0.3)

    g.figure.suptitle("Pair Plot — Multi-Feature Relationships", fontsize=12.5,
                      fontweight="bold", color=TEXT_WHITE, y=1.02)
    return g.figure


# ═══════════════════════════════════════════════════════════════
# BONUS 2: BUBBLE CHART
# ═══════════════════════════════════════════════════════════════
def plot_bubble_chart(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    plot_df = df.dropna(subset=["Speed_MPH", "Time_Minutes"])
    if plot_df.empty:
        ax.text(0.5, 0.5, "Not enough data", ha="center", va="center", color=TEXT_WHITE)
        return fig

    for gender, color, lbl in [("Male", AMBER, "Men"), ("Female", FEMALE_COLOR, "Women")]:
        sub = plot_df[plot_df["Gender"] == gender]
        if not sub.empty:
            sizes = ((sub["Speed_MPH"] - plot_df["Speed_MPH"].min() + 0.5) * 25)
            ax.scatter(sub["Year"], sub["Time_Minutes"], s=sizes, c=color,
                       alpha=0.45, edgecolors=color, linewidths=0.6,
                       label=lbl, zorder=3)

    ax.legend(fontsize=9, framealpha=0.85)
    _style(ax, "Bubble Chart — Speed as Size", "Year", "Time (Minutes)")
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
# BONUS 3: FUNNEL CHART
# ═══════════════════════════════════════════════════════════════
def plot_funnel_chart(df):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG_DEEP)

    bins = [0, 130, 140, 150, 160, 170, 180, 300]
    labels = ["< 2:10", "2:10–2:20", "2:20–2:30", "2:30–2:40",
              "2:40–2:50", "2:50–3:00", "3:00+"]
    df_copy = df.copy()
    df_copy["Bracket"] = pd.cut(df_copy["Time_Minutes"], bins=bins, labels=labels)
    counts = df_copy["Bracket"].value_counts().reindex(labels).fillna(0)

    colors_f = [AMBER_DARK, AMBER, ORANGE, COPPER, BRONZE, RUST, ORANGE_DEEP]
    max_val = counts.max() if counts.max() > 0 else 1

    for i, (label, val) in enumerate(zip(counts.index, counts.values)):
        ax.barh(i, val, height=0.55, color=colors_f[i % len(colors_f)],
                edgecolor="none", alpha=0.8, zorder=3)
        if val > 0:
            ax.text(val + max_val * 0.025, i, str(int(val)), va="center",
                    fontsize=8.5, color=AMBER_LIGHT, fontweight="700")

    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(counts.index, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, max_val * 1.2)
    _style(ax, "Time Bracket Distribution", "Number of Winners", "", grid_axis="x")
    fig.tight_layout()
    return fig

"""
charts.py — Premium Chart Functions for Boston Marathon Dashboard
Noon-inspired: Deep black + warm amber/gold/orange glow theme
Memory-optimized: All figures closed after rendering to bytes.
"""

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — lower memory
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import io
import gc

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

WARM_CMAP = LinearSegmentedColormap.from_list("noon_warm",
    ["#08080a", "#2a1a0a", "#5a3010", AMBER_DARK, AMBER, GOLD_LIGHT], N=128)

# Reduced DPI for memory savings
_DPI = 100
_SMALL = (6.5, 4.8)
_WIDE = (12, 4.5)

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
        "figure.dpi": _DPI,
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


def _fig_to_bytes(fig):
    """Convert figure to PNG bytes, close figure, and free memory."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=_DPI, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none", pad_inches=0.15)
    plt.close(fig)
    del fig
    gc.collect()
    buf.seek(0)
    return buf.getvalue()


def _empty_bytes(msg="Not enough data to display"):
    """Return styled empty figure as bytes."""
    fig, ax = plt.subplots(figsize=_SMALL)
    fig.patch.set_facecolor(BG_DEEP)
    ax.set_facecolor(BG_CARD)
    ax.text(0.5, 0.5, msg, ha="center", va="center",
            color=TEXT_DIM, fontsize=13, fontweight="500",
            transform=ax.transAxes)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    return _fig_to_bytes(fig)


# ═══════════════════════════════════════════════════════════════
# 1. PIE CHART
# ═══════════════════════════════════════════════════════════════
def plot_pie_chart(df):
    try:
        if df.empty or "Country" not in df.columns:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_SMALL)
        fig.patch.set_facecolor(BG_DEEP)

        country_counts = df["Country"].value_counts()
        if country_counts.empty:
            plt.close(fig)
            return _empty_bytes()

        top = country_counts.head(7)
        if len(country_counts) > 7:
            top = top.copy()
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
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering pie chart")


# ═══════════════════════════════════════════════════════════════
# 2. HISTOGRAM
# ═══════════════════════════════════════════════════════════════
def plot_histogram(df):
    try:
        data = df["Time_Minutes"].dropna()
        if len(data) < 2:
            return _empty_bytes("Not enough time data")

        fig, ax = plt.subplots(figsize=_SMALL)
        fig.patch.set_facecolor(BG_DEEP)

        n_bins = min(18, max(5, len(data) // 3))
        n, bins, patches = ax.hist(data, bins=n_bins, color=AMBER, edgecolor=BG_DEEP,
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
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering histogram")


# ═══════════════════════════════════════════════════════════════
# 3. LINE CHART
# ═══════════════════════════════════════════════════════════════
def plot_line_chart(df):
    try:
        if df.empty:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_WIDE)
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
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering line chart")


# ═══════════════════════════════════════════════════════════════
# 4. BAR CHART
# ═══════════════════════════════════════════════════════════════
def plot_bar_chart(df):
    try:
        if df.empty or "Country" not in df.columns:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_SMALL)
        fig.patch.set_facecolor(BG_DEEP)

        top_countries = df["Country"].value_counts().head(10)
        if top_countries.empty:
            plt.close(fig)
            return _empty_bytes()

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
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering bar chart")


# ═══════════════════════════════════════════════════════════════
# 5. SCATTER PLOT
# ═══════════════════════════════════════════════════════════════
def plot_scatter(df):
    try:
        if df.empty:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_SMALL)
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
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering scatter plot")


# ═══════════════════════════════════════════════════════════════
# 6. BOX PLOT
# ═══════════════════════════════════════════════════════════════
def plot_boxplot(df):
    try:
        if df.empty:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_SMALL)
        fig.patch.set_facecolor(BG_DEEP)

        genders = df["Gender"].unique()
        data_by_gender = [df[df["Gender"] == g]["Time_Minutes"].dropna() for g in genders]
        valid = [(g, d) for g, d in zip(genders, data_by_gender) if len(d) > 0]
        if not valid:
            plt.close(fig)
            return _empty_bytes("No time data available")

        genders_valid, data_valid = zip(*valid)
        bp = ax.boxplot(data_valid, labels=genders_valid, patch_artist=True, widths=0.4,
                        medianprops=dict(color=GOLD_LIGHT, linewidth=2.2),
                        whiskerprops=dict(color=TEXT_MUTED, linewidth=1),
                        capprops=dict(color=TEXT_MUTED, linewidth=1),
                        flierprops=dict(marker="o", markerfacecolor=ORANGE, markersize=5,
                                        alpha=0.5, markeredgecolor="none"))

        box_colors = [AMBER, FEMALE_COLOR]
        for i, patch in enumerate(bp["boxes"]):
            color = box_colors[i % len(box_colors)]
            patch.set_facecolor(color)
            patch.set_alpha(0.45)
            patch.set_edgecolor(color)
            patch.set_linewidth(1.5)

        _style(ax, "Time Distribution by Gender", "Gender", "Time (Minutes)", grid_axis="y")
        fig.tight_layout()
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering box plot")


# ═══════════════════════════════════════════════════════════════
# 7. HEATMAP
# ═══════════════════════════════════════════════════════════════
def plot_heatmap(df):
    try:
        if df.empty:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor(BG_DEEP)

        numeric_cols = ["Year", "Time_Minutes", "Distance (Miles)", "Distance (KM)",
                        "Pace_Per_Mile", "Pace_Per_KM", "Speed_MPH"]
        available = [c for c in numeric_cols if c in df.columns]
        if len(available) < 2:
            plt.close(fig)
            return _empty_bytes("Not enough numeric features")

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
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering heatmap")


# ═══════════════════════════════════════════════════════════════
# 8. AREA CHART
# ═══════════════════════════════════════════════════════════════
def plot_area_chart(df):
    try:
        if df.empty:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_SMALL)
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
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering area chart")


# ═══════════════════════════════════════════════════════════════
# 9. COUNT PLOT
# ═══════════════════════════════════════════════════════════════
def plot_countplot(df):
    try:
        if df.empty or "Decade_Label" not in df.columns:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_SMALL)
        fig.patch.set_facecolor(BG_DEEP)

        order = sorted(df["Decade_Label"].unique())
        genders = ["Male", "Female"]
        gender_labels = {"Male": "Men", "Female": "Women"}
        gender_colors = {"Male": AMBER, "Female": FEMALE_COLOR}

        x = np.arange(len(order))
        width = 0.35

        for i, gender in enumerate(genders):
            counts = []
            for decade in order:
                c = len(df[(df["Decade_Label"] == decade) & (df["Gender"] == gender)])
                counts.append(c)
            offset = -width/2 + i * width
            bars = ax.bar(x + offset, counts, width, color=gender_colors[gender],
                          alpha=0.8, edgecolor="none", label=gender_labels[gender], zorder=3)
            for bar, val in zip(bars, counts):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                            str(val), ha="center", va="bottom",
                            fontsize=6.5, color=TEXT_MUTED, fontweight="600")

        ax.set_xticks(x)
        ax.set_xticklabels(order, rotation=45, ha="right", fontsize=8)
        ax.legend(fontsize=8.5, framealpha=0.85)
        _style(ax, "Winners per Decade", "Decade", "Count")
        fig.tight_layout()
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering count plot")


# ═══════════════════════════════════════════════════════════════
# 10. VIOLIN PLOT
# ═══════════════════════════════════════════════════════════════
def plot_violin(df):
    try:
        if df.empty:
            return _empty_bytes()

        valid_genders = []
        for g in df["Gender"].unique():
            if len(df[df["Gender"] == g]["Time_Minutes"].dropna()) >= 2:
                valid_genders.append(g)

        if not valid_genders:
            return _empty_bytes("Not enough data for violin plot")

        plot_df = df[df["Gender"].isin(valid_genders)]

        fig, ax = plt.subplots(figsize=_SMALL)
        fig.patch.set_facecolor(BG_DEEP)

        sns.violinplot(data=plot_df, x="Gender", y="Time_Minutes", hue="Gender",
                       palette={"Male": AMBER, "Female": FEMALE_COLOR},
                       inner="quart", linewidth=1, ax=ax, alpha=0.65, legend=False)

        _style(ax, "Time Distribution Density", "Gender", "Time (Minutes)", grid_axis="y")
        fig.tight_layout()
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering violin plot")


# ═══════════════════════════════════════════════════════════════
# BONUS 1: PAIR PLOT
# ═══════════════════════════════════════════════════════════════
def plot_pairplot(df):
    try:
        _setup()
        cols = ["Year", "Time_Minutes", "Speed_MPH", "Gender"]
        available = [c for c in cols if c in df.columns]
        if "Gender" not in available or len(available) < 3:
            return _empty_bytes("Not enough features for pair plot")

        plot_df = df[available].dropna()
        if len(plot_df) < 5:
            return _empty_bytes("Not enough data points")

        g = sns.pairplot(plot_df, hue="Gender",
                         palette={"Male": AMBER, "Female": FEMALE_COLOR},
                         diag_kind="kde", plot_kws={"alpha": 0.5, "s": 22, "edgecolors": "none"},
                         height=2.0)
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

        # Convert pairplot to bytes too
        buf = io.BytesIO()
        g.figure.savefig(buf, format="png", dpi=90, bbox_inches="tight",
                         facecolor=g.figure.get_facecolor(), edgecolor="none", pad_inches=0.15)
        plt.close(g.figure)
        del g
        gc.collect()
        buf.seek(0)
        return buf.getvalue()
    except Exception:
        return _empty_bytes("Error rendering pair plot")


# ═══════════════════════════════════════════════════════════════
# BONUS 2: BUBBLE CHART
# ═══════════════════════════════════════════════════════════════
def plot_bubble_chart(df):
    try:
        if df.empty:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_SMALL)
        fig.patch.set_facecolor(BG_DEEP)

        plot_df = df.dropna(subset=["Speed_MPH", "Time_Minutes"])
        if plot_df.empty or len(plot_df) < 2:
            plt.close(fig)
            return _empty_bytes("Not enough data")

        speed_min = plot_df["Speed_MPH"].min()

        for gender, color, lbl in [("Male", AMBER, "Men"), ("Female", FEMALE_COLOR, "Women")]:
            sub = plot_df[plot_df["Gender"] == gender]
            if not sub.empty:
                sizes = ((sub["Speed_MPH"] - speed_min + 0.5) * 25).clip(lower=10)
                ax.scatter(sub["Year"], sub["Time_Minutes"], s=sizes, c=color,
                           alpha=0.45, edgecolors=color, linewidths=0.6,
                           label=lbl, zorder=3)

        ax.legend(fontsize=9, framealpha=0.85)
        _style(ax, "Bubble Chart — Speed as Size", "Year", "Time (Minutes)")
        fig.tight_layout()
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering bubble chart")


# ═══════════════════════════════════════════════════════════════
# BONUS 3: FUNNEL CHART
# ═══════════════════════════════════════════════════════════════
def plot_funnel_chart(df):
    try:
        if df.empty or "Time_Minutes" not in df.columns:
            return _empty_bytes()

        fig, ax = plt.subplots(figsize=_SMALL)
        fig.patch.set_facecolor(BG_DEEP)

        time_data = df["Time_Minutes"].dropna()
        if len(time_data) < 2:
            plt.close(fig)
            return _empty_bytes("Not enough time data")

        bins = [0, 130, 140, 150, 160, 170, 180, 300]
        labels = ["< 2:10", "2:10-2:20", "2:20-2:30", "2:30-2:40",
                  "2:40-2:50", "2:50-3:00", "3:00+"]
        df_copy = df.copy()
        df_copy["Bracket"] = pd.cut(df_copy["Time_Minutes"], bins=bins, labels=labels)
        counts = df_copy["Bracket"].value_counts().reindex(labels).fillna(0)

        non_zero = counts[counts > 0]
        if non_zero.empty:
            plt.close(fig)
            return _empty_bytes("No data in time brackets")

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
        return _fig_to_bytes(fig)
    except Exception:
        return _empty_bytes("Error rendering funnel chart")

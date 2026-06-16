"""
charts.py — Professional Light Theme Charts
Google/McKinsey/UN Style - Clean, Vibrant, International Standard
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
import io

# ─── Professional Color Palette (Google/McKinsey style) ──────────────────────
PALETTE = [
    "#4285F4", "#EA4335", "#34A853", "#FBBC04", "#FF6D00",
    "#9C27B0", "#00ACC1", "#F06292", "#558B2F", "#1565C0",
    "#E64A19", "#00897B", "#F9A825", "#6A1B9A", "#2E7D32",
    "#0277BD", "#AD1457", "#00838F", "#EF6C00", "#4527A0",
]

BG       = "#FFFFFF"
CARD_BG  = "#F8F9FA"
GRID_C   = "#E8EAED"
TEXT_C   = "#202124"
SUB_TEXT = "#5F6368"
BLUE     = "#4285F4"
RED      = "#EA4335"
GREEN    = "#34A853"
YELLOW   = "#FBBC04"
ORANGE   = "#FF6D00"

def _style_ax(ax, title, xlabel="", ylabel=""):
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, color=TEXT_C, fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel(xlabel, color=SUB_TEXT, fontsize=11, labelpad=8)
    ax.set_ylabel(ylabel, color=SUB_TEXT, fontsize=11, labelpad=8)
    ax.tick_params(colors=SUB_TEXT, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_C)
        spine.set_linewidth(1)
    ax.grid(color=GRID_C, linestyle="-", linewidth=0.8, alpha=1)
    ax.set_axisbelow(True)

def _make_fig(figsize=(11, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD_BG)
    return fig, ax

def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches=None, facecolor=BG)
    buf.seek(0)
    return buf.getvalue()

# ─── 1. Pie Chart ────────────────────────────────────────────────────────────
def chart_pie_legendary(df):
    fig, ax = _make_fig(figsize=(11, 5))
    counts = df["Legendary"].value_counts()
    labels = ["Non-Legendary" if not k else "Legendary" for k in counts.index]
    colors = [BLUE, RED]
    wedges, texts, autotexts = ax.pie(
        counts, labels=labels, autopct="%1.1f%%",
        colors=colors, startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=3),
        shadow=False,
        radius=0.75,
    )
    for t in texts:
        t.set_color(TEXT_C); t.set_fontsize(12); t.set_fontweight("bold")
    for at in autotexts:
        at.set_color("white"); at.set_fontsize(12); at.set_fontweight("bold")
    ax.set_title("Legendary vs Non-Legendary Pokémon",
                 color=TEXT_C, fontsize=15, fontweight="bold", pad=16)
    fig.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.12)
    return fig

# ─── 2. Histogram ────────────────────────────────────────────────────────────
def chart_histogram_total(df):
    fig, ax = _make_fig()
    n, bins, patches = ax.hist(df["Total"], bins=30, edgecolor="white", linewidth=0.8, color=BLUE, alpha=0.85)
    cm = plt.cm.Blues
    norm_vals = (n - n.min()) / (n.max() - n.min() + 1e-9)
    for frac, patch in zip(norm_vals, patches):
        patch.set_facecolor(cm(0.4 + frac * 0.5))
    ax.axvline(df["Total"].mean(), color=RED, linestyle="--", linewidth=2,
               label=f"Mean: {df['Total'].mean():.0f}")
    ax.axvline(df["Total"].median(), color=GREEN, linestyle="--", linewidth=2,
               label=f"Median: {df['Total'].median():.0f}")
    _style_ax(ax, "Distribution of Total Base Stats", "Total Stats", "Frequency")
    ax.legend(fontsize=9, framealpha=0.95)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

# ─── 3. Line Chart ───────────────────────────────────────────────────────────
def chart_line_avg_stats_by_generation(df):
    fig, ax = _make_fig(figsize=(11, 5))
    stat_cols = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    line_colors = [BLUE, RED, GREEN, YELLOW, ORANGE, "#9C27B0"]
    gen_avg = df.groupby("Generation")[stat_cols].mean()
    for i, col in enumerate(stat_cols):
        ax.plot(gen_avg.index, gen_avg[col], marker="o", label=col,
                color=line_colors[i], linewidth=2.5, markersize=8,
                markerfacecolor="white", markeredgewidth=2.5)
    _style_ax(ax, "Average Stats per Generation", "Generation", "Avg Stat Value")
    ax.legend(fontsize=9, framealpha=0.95, ncol=3)
    ax.set_xticks(gen_avg.index)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

# ─── 4. Bar Chart ────────────────────────────────────────────────────────────
def chart_bar_avg_total_by_type(df):
    fig, ax = _make_fig(figsize=(11, 5))
    type_avg = df.groupby("Type 1")["Total"].mean().sort_values(ascending=False)
    bars = ax.bar(type_avg.index, type_avg.values,
                  color=PALETTE[:len(type_avg)], edgecolor="white", linewidth=1.2)
    _style_ax(ax, "Average Total Stats by Pokémon Type 1", "Type 1", "Average Total Stats")
    ax.tick_params(axis="x", rotation=45)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f"{bar.get_height():.0f}", ha="center", va="bottom",
                color=SUB_TEXT, fontsize=7, fontweight="bold")
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

# ─── 5. Scatter Plot ─────────────────────────────────────────────────────────
def chart_scatter_attack_vs_defense(df):
    fig, ax = _make_fig(figsize=(11, 5))
    types = df["Type 1"].unique()
    cmap = {t: PALETTE[i % len(PALETTE)] for i, t in enumerate(sorted(types))}
    for ptype in sorted(types):
        sub = df[df["Type 1"] == ptype]
        ax.scatter(sub["Attack"], sub["Defense"], c=cmap[ptype],
                   label=ptype, alpha=0.75, s=50, edgecolors="white", linewidth=0.5)
    _style_ax(ax, "Attack vs Defense by Type 1", "Attack", "Defense")
    ax.legend(fontsize=7, ncol=3, loc="upper left", framealpha=0.95)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

# ─── 6. Box Plot ─────────────────────────────────────────────────────────────
def chart_box_stats(df):
    fig, ax = _make_fig(figsize=(11, 5))
    stat_cols = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    data = [df[c].dropna().values for c in stat_cols]
    bp = ax.boxplot(data, labels=stat_cols, patch_artist=True,
                    medianprops=dict(color="white", linewidth=2.5),
                    whiskerprops=dict(color=SUB_TEXT, linewidth=1.2),
                    capprops=dict(color=SUB_TEXT, linewidth=1.5),
                    flierprops=dict(marker="o", alpha=0.5, markersize=4))
    for patch, color in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(color); patch.set_alpha(0.8)
    _style_ax(ax, "Distribution of All Base Stats", "Stat", "Value")
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

# ─── 7. Heatmap ──────────────────────────────────────────────────────────────
def chart_heatmap_correlation(df):
    fig, ax = _make_fig(figsize=(11, 5))
    num_cols = ["Total", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
                linewidths=1, linecolor="white", ax=ax,
                annot_kws={"size": 10, "weight": "bold"},
                vmin=-1, vmax=1)
    ax.set_title("Correlation Heatmap of Base Stats",
                 color=TEXT_C, fontsize=15, fontweight="bold", pad=16)
    ax.tick_params(colors=TEXT_C, labelsize=10)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

# ─── 8. Area Chart ───────────────────────────────────────────────────────────
def chart_area_pokemon_count_by_generation(df):
    fig, ax = _make_fig(figsize=(11, 5))
    gen_counts = df.groupby("Generation").size().sort_index()
    cumulative = gen_counts.cumsum()
    ax.fill_between(cumulative.index, cumulative.values, color=BLUE, alpha=0.15)
    ax.fill_between(gen_counts.index, gen_counts.values, color=GREEN, alpha=0.25)
    ax.plot(cumulative.index, cumulative.values, color=BLUE,
            linewidth=2.5, marker="o", markersize=8,
            markerfacecolor="white", markeredgewidth=2.5, label="Cumulative Total")
    ax.plot(gen_counts.index, gen_counts.values, color=GREEN,
            linewidth=2, marker="s", markersize=7, linestyle="--", label="Per Generation")
    _style_ax(ax, "Pokémon Count by Generation", "Generation", "Count")
    ax.set_xticks(cumulative.index)
    ax.legend(fontsize=10, framealpha=0.95)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

# ─── 9. Count Plot ───────────────────────────────────────────────────────────
def chart_count_type1(df):
    fig, ax = _make_fig(figsize=(11, 5))
    order = df["Type 1"].value_counts().index
    sns.countplot(data=df, y="Type 1", order=order,
                  hue="Type 1", palette=PALETTE[:len(order)],
                  ax=ax, edgecolor="white", linewidth=0.8, legend=False)
    _style_ax(ax, "Pokémon Count by Type 1", "Count", "Type 1")
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

# ─── 10. Violin Plot ─────────────────────────────────────────────────────────
def chart_violin_speed_by_type(df):
    fig, ax = _make_fig(figsize=(11, 5))
    top_types = df["Type 1"].value_counts().head(8).index
    sub = df[df["Type 1"].isin(top_types)]
    sns.violinplot(data=sub, x="Type 1", y="Speed", order=top_types,
                   hue="Type 1", palette=PALETTE[:8], ax=ax,
                   inner="quartile", linewidth=1.5, legend=False)
    _style_ax(ax, "Speed Distribution by Type 1 (Top 8)", "Type 1", "Speed")
    fig.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.12)
    return fig

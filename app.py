"""
app.py — Pokemon EDA Dashboard
Power BI Style — Professional Light Theme, Blue Color Scheme
"""

import streamlit as st
import pandas as pd

from filters import load_data, apply_filters, get_kpi_stats
from charts import (
    chart_pie_legendary, chart_histogram_total,
    chart_line_avg_stats_by_generation, chart_bar_avg_total_by_type,
    chart_scatter_attack_vs_defense, chart_box_stats,
    chart_heatmap_correlation, chart_area_pokemon_count_by_generation,
    chart_count_type1, chart_violin_speed_by_type, fig_to_bytes,
)

st.set_page_config(page_title="Pokémon EDA Dashboard", page_icon="",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&family=Roboto:wght@300;400;500;700&display=swap');

* { font-family: 'Roboto', 'Segoe UI', sans-serif; }

/* ── Page Background ── */
.stApp { background-color: #F0F2F5; color: #1E2432; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1E2D4D;
    border-right: none;
    width: 220px !important;
}
[data-testid="stSidebar"] * { color: #B8C7E0 !important; font-size: 13px !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong { color: #FFFFFF !important; font-size: 13px !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: #26375A !important;
    border: 1px solid #3A4E72 !important;
    color: #E8EEF7 !important;
    border-radius: 6px !important;
}

/* Sidebar nav icons */
.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 16px; border-radius: 6px;
    margin: 2px 8px; cursor: pointer;
    color: #B8C7E0; font-size: 13px; font-weight: 500;
    transition: background 0.2s;
}
.nav-item:hover, .nav-item.active {
    background: #2E4270; color: white;
}
.nav-icon { font-size: 16px; width: 20px; text-align: center; }

/* ── Top Bar ── */
.top-bar {
    background: white;
    border-radius: 10px;
    padding: 16px 24px;
    margin-bottom: 16px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.top-bar-title { font-size: 22px; font-weight: 700; color: #1E2432; }
.top-bar-sub   { font-size: 12px; color: #6B7A99; margin-top: 2px; }
.top-bar-badges { display: flex; gap: 8px; }
.tb-badge {
    background: #EEF2FF; border: 1px solid #C7D2FE;
    border-radius: 6px; padding: 4px 12px;
    font-size: 11px; color: #4338CA; font-weight: 600;
}

/* ── KPI Cards — Power BI Style ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.kpi-card {
    background: white;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    border-bottom: 3px solid #2563EB;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 60px; height: 60px;
    background: linear-gradient(135deg, transparent 50%, #EEF2FF 50%);
    border-radius: 0 10px 0 0;
}
.kpi-label { font-size: 11px; color: #6B7A99; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.kpi-value { font-size: 28px; font-weight: 700; color: #1E2432; margin: 6px 0 2px 0; }
.kpi-sub   { font-size: 11px; color: #2563EB; font-weight: 500; }
.kpi-card-2 { border-bottom-color: #0891B2; }
.kpi-card-2 .kpi-sub { color: #0891B2; }
.kpi-card-3 { border-bottom-color: #059669; }
.kpi-card-3 .kpi-sub { color: #059669; }
.kpi-card-4 { border-bottom-color: #7C3AED; }
.kpi-card-4 .kpi-sub { color: #7C3AED; }

/* Second row of KPI */
.kpi-row-2 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}

/* ── Section Header ── */
.sec-head {
    font-size: 15px; font-weight: 700; color: #1E2432;
    margin: 20px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #E2E8F0;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.sec-head span {
    color: #2563EB;
    margin-right: 8px;
}

/* ── Chart Cards ── */
.chart-card {
    background: white;
    border-radius: 10px;
    padding: 16px 18px 12px 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}
.chart-title {
    font-size: 13px; font-weight: 700; color: #1E2432;
    margin-bottom: 2px;
}
.chart-desc {
    font-size: 11px; color: #6B7A99;
    margin-bottom: 10px; line-height: 1.5;
}

/* ── Insight Box ── */
.insight {
    background: #EFF6FF;
    border-left: 3px solid #2563EB;
    border-radius: 0 6px 6px 0;
    padding: 8px 12px;
    margin-top: 8px;
    font-size: 11px; color: #1E40AF; line-height: 1.5;
}
.insight b { color: #1D4ED8; }

/* ── Divider ── */
.divider { height: 1px; background: #E2E8F0; margin: 4px 0 16px 0; }

/* ── Download Button ── */
.stDownloadButton > button {
    background: #2563EB !important;
    border: none !important;
    color: white !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    padding: 6px 14px !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #1D4ED8 !important;
}

/* ── Streamlit overrides ── */
.stButton > button[kind="primary"] {
    background: #2563EB !important;
    border: none !important;
    color: white !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1D4ED8 !important;
}

h1,h2,h3,h4 { color: #1E2432 !important; }
.stDataFrame { border-radius: 10px !important; }

/* ── Footer ── */
.footer {
    background: white;
    border-radius: 10px;
    padding: 20px 28px;
    margin-top: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data("pokemon.csv")
df_raw = get_data()

# ── Session State Defaults (must be BEFORE any widget is created) ─────────────
_DEFAULTS = {
    "tmin": 180, "tmax": 780,
    "hmin": 1,   "hmax": 255,
    "amin": 5,   "amax": 190,
    "search_text": "", "sel_type1": [],
    "sel_type2": [], "sel_gens": [],
    "legendary_filter": "All",
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 16px 16px 16px; border-bottom:1px solid #2E4270;'>
        <div style='font-size:20px; font-weight:800; color:white; letter-spacing:1px;'>POKÉDEX</div>
        <div style='font-size:11px; color:#6B8CC4; margin-top:2px;'>EDA Dashboard</div>
    </div>
    <div style='padding:12px 8px 4px 8px;'>
        <div style='font-size:10px; color:#6B8CC4; text-transform:uppercase; letter-spacing:1px; padding:0 8px; margin-bottom:8px;'>Navigation</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='nav-item active'>
        <span class='nav-icon'>▣</span> Dashboard
    </div>
    <div class='nav-item'>
        <span class='nav-icon'>◈</span> Analysis
    </div>
    <div class='nav-item'>
        <span class='nav-icon'>◎</span> Reports
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:16px 8px 4px 8px; border-top:1px solid #2E4270; margin-top:8px;'>
        <div style='font-size:10px; color:#6B8CC4; text-transform:uppercase; letter-spacing:1px; padding:0 8px; margin-bottom:8px;'>Filters</div>
    </div>""", unsafe_allow_html=True)

    search_text = st.text_input("Search Pokemon", placeholder="Type name...", key="search_text")

    all_type1 = sorted(df_raw["Type 1"].unique())
    selected_type1 = st.multiselect("Primary Type", all_type1, key="sel_type1")

    all_type2 = sorted(df_raw["Type 2"].unique())
    selected_type2 = st.multiselect("Secondary Type", all_type2, key="sel_type2")

    all_gens = sorted(df_raw["Generation"].unique())
    selected_gens = st.multiselect("Generation", all_gens, key="sel_gens")

    legendary_filter = st.selectbox("Legendary", ["All","Legendary Only","Non-Legendary Only"], key="legendary_filter")

    st.markdown("<div style='padding:8px 8px 0 8px; font-size:11px; color:#6B8CC4;'>Stat Ranges</div>", unsafe_allow_html=True)

    tc1, tc2 = st.columns(2)
    with tc1:
        total_min_val = st.number_input("Tot Min", min_value=180, max_value=780, step=10, key="tmin")
    with tc2:
        total_max_val = st.number_input("Tot Max", min_value=180, max_value=780, step=10, key="tmax")
    total_range = (int(st.session_state["tmin"]), int(st.session_state["tmax"]))

    hc1, hc2 = st.columns(2)
    with hc1:
        hp_min_val = st.number_input("HP Min", min_value=1, max_value=255, step=5, key="hmin")
    with hc2:
        hp_max_val = st.number_input("HP Max", min_value=1, max_value=255, step=5, key="hmax")
    hp_range = (int(st.session_state["hmin"]), int(st.session_state["hmax"]))

    ac1, ac2 = st.columns(2)
    with ac1:
        atk_min_val = st.number_input("Atk Min", min_value=5, max_value=190, step=5, key="amin")
    with ac2:
        atk_max_val = st.number_input("Atk Max", min_value=5, max_value=190, step=5, key="amax")
    attack_range = (int(st.session_state["amin"]), int(st.session_state["amax"]))

    st.markdown("---")

    def _do_reset():
        for k, v in _DEFAULTS.items():
            st.session_state[k] = v

    st.button("Reset All Filters", use_container_width=True, type="primary", on_click=_do_reset)

    st.markdown("""
    <div style='position:fixed; bottom:0; left:0; width:220px;
                background:#162036; padding:14px 16px; border-top:1px solid #2E4270;'>
        <div style='font-size:10px; color:#6B8CC4; line-height:1.8;'>
            Exploratory Data Analysis<br>
            <b style='color:#B8C7E0;'>Ali Hassan Sherazi</b><br>
            Submission: 05-June-2026
        </div>
    </div>""", unsafe_allow_html=True)

# ── Apply Filters ─────────────────────────────────────────────────────────────
_t1  = st.session_state.get("sel_type1", [])
_t2  = st.session_state.get("sel_type2", [])
_gen = st.session_state.get("sel_gens", [])
_leg = st.session_state.get("legendary_filter", "All")
_src = st.session_state.get("search_text", "")
_tmin = int(st.session_state.get("tmin", 180))
_tmax = int(st.session_state.get("tmax", 780))
_hmin = int(st.session_state.get("hmin", 1))
_hmax = int(st.session_state.get("hmax", 255))
_amin = int(st.session_state.get("amin", 5))
_amax = int(st.session_state.get("amax", 190))

df = apply_filters(df_raw,
    search_text=_src,
    selected_type1=_t1 if _t1 else None,
    selected_type2=_t2 if _t2 else None,
    selected_generations=_gen if _gen else None,
    legendary_filter=_leg,
    total_range=(_tmin, _tmax),
    hp_range=(_hmin, _hmax),
    attack_range=(_amin, _amax))

# ── Top Bar ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
    <div>
        <div class="top-bar-title">Pokemon EDA Dashboard</div>
        <div class="top-bar-sub">Exploratory Data Analysis &nbsp;·&nbsp; 800 Pokemon &nbsp;·&nbsp; 6 Generations &nbsp;·&nbsp; 13 Features</div>
    </div>
    <div class="top-bar-badges">
        <span class="tb-badge">Python</span>
        <span class="tb-badge">Pandas</span>
        <span class="tb-badge">Matplotlib</span>
        <span class="tb-badge">Seaborn</span>
        <span class="tb-badge">Streamlit</span>
        <span class="tb-badge">{len(df)} Records</span>
    </div>
</div>""", unsafe_allow_html=True)

if len(df) == 0:
    active = []
    if search_text:
        active.append('Search: "' + search_text + '"')
    if selected_type1:
        active.append('Primary Type: ' + ', '.join(selected_type1))
    if selected_type2:
        active.append('Secondary Type: ' + ', '.join(selected_type2))
    if selected_gens:
        active.append('Generation: ' + ', '.join(str(g) for g in selected_gens))
    if legendary_filter != 'All':
        active.append('Legendary: ' + legendary_filter)
    active_str = ' | '.join(active) if active else 'check filters'
    st.error('No Pokemon match your current filters. Active filters: ' + active_str + '. These may be conflicting — use Reset All Filters in the sidebar.')
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
kpi = get_kpi_stats(df)
strongest = str(kpi["strongest_pokemon"])
if len(strongest) > 12: strongest = strongest[:12] + "…"

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-label">Total Pokemon</div>
        <div class="kpi-value">{kpi["total_records"]}</div>
        <div class="kpi-sub">in filtered dataset</div>
    </div>
    <div class="kpi-card kpi-card-2">
        <div class="kpi-label">Avg Total Stats</div>
        <div class="kpi-value">{kpi["avg_total"]}</div>
        <div class="kpi-sub">average base stat sum</div>
    </div>
    <div class="kpi-card kpi-card-3">
        <div class="kpi-label">Avg HP</div>
        <div class="kpi-value">{kpi["avg_hp"]}</div>
        <div class="kpi-sub">average health points</div>
    </div>
    <div class="kpi-card kpi-card-4">
        <div class="kpi-label">Avg Attack</div>
        <div class="kpi-value">{kpi["avg_attack"]}</div>
        <div class="kpi-sub">average attack power</div>
    </div>
</div>
<div class="kpi-row-2">
    <div class="kpi-card">
        <div class="kpi-label">Highest Total</div>
        <div class="kpi-value">{kpi["max_total"]}</div>
        <div class="kpi-sub">max base stat total</div>
    </div>
    <div class="kpi-card kpi-card-2">
        <div class="kpi-label">Legendary Count</div>
        <div class="kpi-value">{kpi["legendary_count"]}</div>
        <div class="kpi-sub">rare pokemon</div>
    </div>
    <div class="kpi-card kpi-card-3">
        <div class="kpi-label">Strongest Pokemon</div>
        <div class="kpi-value" style="font-size:18px;">{strongest}</div>
        <div class="kpi-sub">by total base stats</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── Helper ────────────────────────────────────────────────────────────────────
def show_chart(fig, filename, title, desc, insight):
    st.markdown(f"""<div class="chart-card">
        <div class="chart-title">{title}</div>
        <div class="chart-desc">{desc}</div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(fig, use_container_width=True, bbox_inches=None)
    st.download_button(
        label="Download Chart",
        data=fig_to_bytes(fig),
        file_name=filename,
        mime="image/png",
        key=filename,
    )
    st.markdown(f'<div class="insight"><b>Insight:</b> {insight}</div>', unsafe_allow_html=True)

# ═══ SECTION 1 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>01</span>Distribution &amp; Composition</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    show_chart(chart_pie_legendary(df), "pie_legendary.png",
        "Pie Chart — Legendary vs Non-Legendary",
        "Proportional split between Legendary and Non-Legendary Pokemon. Legendary Pokemon are extremely rare — only about 8% of all Pokemon but have significantly higher stats.",
        "The vast majority are Non-Legendary. Legendary Pokemon make up only ~8% of the dataset but dominate in terms of raw power and total base stats.")
with col2:
    show_chart(chart_histogram_total(df), "histogram_total.png",
        "Histogram — Total Base Stats Distribution",
        "Frequency distribution of Total Base Stats across all Pokemon. Blue dashed line shows Mean, green shows Median. Reveals overall power distribution across stat ranges.",
        "Most Pokemon have 300–550 total stats. The right tail (600+) represents powerful Legendaries and Mega Evolutions, showing intentional power tiers in game design.")

# ═══ SECTION 2 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>02</span>Trends Across Generations</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    show_chart(chart_line_avg_stats_by_generation(df), "line_generations.png",
        "Line Chart — Average Stats per Generation",
        "Tracks how each base stat changes across Generations 1–6. Each line represents one stat. Open circle markers show exact values per generation.",
        "Stats remained relatively balanced across generations. Generation 4 and 6 show slight spikes due to powerful Legendaries introduced in those games.")
with col4:
    show_chart(chart_area_pokemon_count_by_generation(df), "area_cumulative.png",
        "Area Chart — Cumulative Pokemon Count by Generation",
        "Cumulative growth in total Pokemon from Gen 1–6 (blue) vs per-generation count (green dashed). Shaded areas make growth trends easy to see at a glance.",
        "Generation 1 introduced the most Pokemon (151). Later generations added fewer new species, suggesting designers became more selective over time.")

# ═══ SECTION 3 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>03</span>Type-Based Analysis</div>', unsafe_allow_html=True)

show_chart(chart_bar_avg_total_by_type(df), "bar_type_total.png",
    "Bar Chart — Average Total Stats by Pokemon Type 1",
    "Compares the average Total Base Stats for each primary Pokemon type. Bar height shows average combined stat power. Numbers on top show exact averages. Reveals which types tend to have the strongest Pokemon overall.",
    "Dragon-type Pokemon have the highest average Total Stats, followed by Steel and Psychic. Normal and Bug types have the lowest averages, partly because they include many early-game unevolved Pokemon.")

col5, col6 = st.columns(2)
with col5:
    show_chart(chart_count_type1(df), "count_type1.png",
        "Count Plot — Pokemon Count by Type 1",
        "Number of Pokemon belonging to each primary type. Reveals the diversity and popularity of different types. Some types were introduced in later generations while others have been staples since Generation 1.",
        "Water is the most common type (112 Pokemon), followed by Normal (98). Ice and Flying are the rarest primary types, reflecting their selective use in the game design.")
with col6:
    show_chart(chart_violin_speed_by_type(df), "violin_speed.png",
        "Violin Plot — Speed Distribution by Type (Top 8)",
        "Full distribution and probability density of Speed stats for the top 8 Pokemon types. Wider violin = more Pokemon at that speed. Inner lines show quartiles (25%, 50%, 75%).",
        "Electric and Dragon types show the widest speed ranges. Normal types cluster around medium speeds showing more consistency within the type category.")

# ═══ SECTION 4 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>04</span>Relationships &amp; Stat Spread</div>', unsafe_allow_html=True)

col7, col8 = st.columns(2)
with col7:
    show_chart(chart_scatter_attack_vs_defense(df), "scatter_atk_def.png",
        "Scatter Plot — Attack vs Defense by Type 1",
        "Every Pokemon mapped by Attack (x-axis) vs Defense (y-axis), colored by primary type. Reveals whether types tend to be offensive, defensive, or balanced. Clusters reveal type-specific stat strategies.",
        "Rock and Steel types cluster in the high-Defense area. Fighting and Dragon types lean toward high Attack. Most types scatter broadly showing individual Pokemon can have very different roles.")
with col8:
    show_chart(chart_box_stats(df), "box_stats.png",
        "Box Plot — Distribution of All Base Stats",
        "Statistical spread of all 6 base stats simultaneously. Box = middle 50% (IQR), white line = median, whiskers = min/max, dots = outliers. Comparing boxes shows variability differences between stats.",
        "Attack has the widest spread and most outliers. HP and Defense are more tightly clustered. Speed has notable outliers representing extremely fast Pokemon like Deoxys-Speed Form (180 Speed).")

# ═══ SECTION 5 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>05</span>Correlation Heatmap</div>', unsafe_allow_html=True)

show_chart(chart_heatmap_correlation(df), "heatmap_correlation.png",
    "Heatmap — Correlation Matrix of All Numerical Features",
    "Pearson correlation coefficient between every pair of numerical features. Values from -1 to +1. Green = strongly positively correlated, Red = negatively correlated. One of the most important charts in EDA — reveals hidden relationships between stats.",
    "Total is highly correlated with all individual stats (expected — it is their sum). Sp.Atk and Sp.Def are moderately correlated (0.5+). Attack and Speed have surprisingly low correlation — fast Pokemon are not always strong attackers.")

# ═══ SECTION 6 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>06</span>Filtered Data Table</div>', unsafe_allow_html=True)

st.dataframe(df.reset_index(drop=True), use_container_width=True, height=300)

col_info, col_dl = st.columns([3,1])
with col_info:
    st.markdown(f"<p style='color:#6B7A99; font-size:12px; margin-top:6px;'>Showing <b style='color:#2563EB;'>{len(df)}</b> of <b style='color:#2563EB;'>{len(df_raw)}</b> Pokemon records</p>", unsafe_allow_html=True)
with col_dl:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "filtered_pokemon.csv", "text/csv", key="csv_dl")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style='font-size:15px; font-weight:700; color:#1E2432;'>Pokemon EDA Dashboard</div>
    <div style='font-size:11px; color:#6B7A99; margin-top:8px; line-height:2;'>
        <b>Course:</b> Exploratory Data Analysis &nbsp;|&nbsp;
        <b>Instructor:</b> Ali Hassan Sherazi &nbsp;|&nbsp;
        <b>Submission:</b> 05-June-2026<br>
        <b>Dataset:</b> 800 Pokemon · 6 Generations · 18 Types · 13 Features &nbsp;|&nbsp;
        <b>Stack:</b> Python · Pandas · Matplotlib · Seaborn · Streamlit
    </div>
    <div style='margin-top:20px; padding-top:16px; border-top:1px solid #E2E8F0; text-align:left;'>
        <div style='font-size:13px; font-weight:700; color:#1E2432; margin-bottom:10px;'>Building Effective Dashboards</div>
        <p style='font-size:12px; color:#4B5563; line-height:1.8; margin-bottom:12px;'>
            Building a professional dashboard requires a foundation of actionable insights, visual hierarchy, and customization.
            To build an effective, at-a-glance dashboard, consider these five core requirements:
        </p>
        <div style='display:grid; grid-template-columns: repeat(5,1fr); gap:12px;'>
            <div style='background:#EFF6FF; border-radius:8px; padding:12px 14px; border-top:3px solid #2563EB;'>
                <div style='font-size:11px; font-weight:700; color:#1D4ED8; margin-bottom:4px;'>① Relevant Metrics Only</div>
                <div style='font-size:11px; color:#4B5563; line-height:1.6;'>Limit the display to your highest-impact KPIs. A crowded dashboard defeats the purpose of at-a-glance clarity.</div>
            </div>
            <div style='background:#EFF6FF; border-radius:8px; padding:12px 14px; border-top:3px solid #0891B2;'>
                <div style='font-size:11px; font-weight:700; color:#0E7490; margin-bottom:4px;'>② Visual Hierarchy</div>
                <div style='font-size:11px; color:#4B5563; line-height:1.6;'>Use size, color, and positioning to emphasize primary metrics. Place top-level data at the top left of the screen.</div>
            </div>
            <div style='background:#EFF6FF; border-radius:8px; padding:12px 14px; border-top:3px solid #059669;'>
                <div style='font-size:11px; font-weight:700; color:#047857; margin-bottom:4px;'>③ Real-Time Data Updates</div>
                <div style='font-size:11px; color:#4B5563; line-height:1.6;'>Ensure the dashboard pulls and refreshes data automatically in real time.</div>
            </div>
            <div style='background:#EFF6FF; border-radius:8px; padding:12px 14px; border-top:3px solid #7C3AED;'>
                <div style='font-size:11px; font-weight:700; color:#6D28D9; margin-bottom:4px;'>④ Customization &amp; Interactivity</div>
                <div style='font-size:11px; color:#4B5563; line-height:1.6;'>Allow users to drag-and-drop widgets, filter by specific date ranges, and drill down into granular details.</div>
            </div>
            <div style='background:#EFF6FF; border-radius:8px; padding:12px 14px; border-top:3px solid #EA580C;'>
                <div style='font-size:11px; font-weight:700; color:#C2410C; margin-bottom:4px;'>⑤ Responsive Design</div>
                <div style='font-size:11px; color:#4B5563; line-height:1.6;'>The layout must scale perfectly across desktop monitors, tablets, and mobile devices.</div>
            </div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

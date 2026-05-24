"""
app.py — Boston Marathon Data Visualization Dashboard
Noon-inspired premium dark theme: Deep black + warm amber/gold/orange glow.
Single continuous scroll layout.
"""

import streamlit as st
import pandas as pd
import numpy as np
from filters import load_and_merge_data, apply_filters
from charts import (
    plot_pie_chart, plot_histogram, plot_line_chart, plot_bar_chart,
    plot_scatter, plot_boxplot, plot_heatmap, plot_area_chart,
    plot_countplot, plot_violin, plot_pairplot, plot_bubble_chart,
    plot_funnel_chart
)

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Boston Marathon Dashboard",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# NOON-INSPIRED PREMIUM CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-deep: #08080a;
        --bg-card: #0e0e12;
        --bg-card-hover: #121216;
        --border: #1a1815;
        --border-warm: #2a2318;
        --amber: #e8933a;
        --amber-light: #f0a852;
        --amber-dark: #c47520;
        --gold: #d4a850;
        --gold-light: #e8c86a;
        --orange: #e07830;
        --text-white: #f5f0e8;
        --text-light: #c8c0b0;
        --text-dim: #7a7468;
        --text-muted: #4a4540;
    }

    /* ── Global ── */
    .stApp {
        background: var(--bg-deep) !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"] {
        background: var(--bg-deep) !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0e 0%, #0e0d10 100%) !important;
        border-right: 1px solid rgba(232, 147, 58, 0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h4 {
        color: var(--amber) !important;
        font-weight: 600 !important;
        font-size: 0.7rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.85;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(232, 147, 58, 0.08) !important;
    }

    /* ── KPI Cards ── */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(14,14,18,0.98), rgba(18,18,22,0.95));
        border: 1px solid rgba(232, 147, 58, 0.08);
        border-radius: 16px;
        padding: 24px 22px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4),
                    0 0 1px rgba(232, 147, 58, 0.1),
                    inset 0 1px 0 rgba(255,255,255,0.02);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    div[data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(232,147,58,0.15), transparent);
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(232, 147, 58, 0.2);
        box-shadow: 0 8px 35px rgba(0,0,0,0.5),
                    0 0 60px rgba(232, 147, 58, 0.04),
                    inset 0 1px 0 rgba(255,255,255,0.03);
        transform: translateY(-3px);
    }
    div[data-testid="stMetric"] label {
        color: var(--text-dim) !important;
        font-size: 0.68rem !important;
        font-weight: 600 !important;
        letter-spacing: 1.8px;
        text-transform: uppercase;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--text-white) !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        white-space: nowrap;
        overflow: visible;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        color: var(--amber) !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
    }

    /* ── Dashboard Header ── */
    .noon-header {
        text-align: center;
        padding: 50px 0 10px 0;
        position: relative;
    }
    .noon-header::before {
        content: '';
        position: absolute;
        top: 0; left: 50%;
        transform: translateX(-50%);
        width: 300px; height: 200px;
        background: radial-gradient(ellipse, rgba(232,147,58,0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    .noon-badge {
        display: inline-block;
        background: rgba(232, 147, 58, 0.06);
        border: 1px solid rgba(232, 147, 58, 0.12);
        color: var(--amber);
        padding: 5px 18px;
        border-radius: 100px;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 18px;
        font-family: 'Inter', sans-serif;
    }
    .noon-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        color: var(--text-white) !important;
        letter-spacing: -1px;
        margin: 0 !important;
        line-height: 1.15 !important;
    }
    .noon-title span {
        background: linear-gradient(135deg, #f0a852, #e8933a, #d4a850);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .noon-sub {
        text-align: center;
        color: var(--text-dim);
        font-size: 0.88rem;
        margin: 12px 0 40px 0;
        font-weight: 400;
        line-height: 1.6;
        letter-spacing: 0.2px;
    }

    /* ── Section Dividers ── */
    .noon-section {
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 55px 0 28px 0;
    }
    .noon-section-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--amber);
        box-shadow: 0 0 12px rgba(232,147,58,0.3);
        flex-shrink: 0;
    }
    .noon-section-info {
        flex-shrink: 0;
    }
    .noon-section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-white);
        margin: 0;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }
    .noon-section-sub {
        font-size: 0.72rem;
        color: var(--text-dim);
        margin: 3px 0 0 0;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    .noon-section-line {
        flex-grow: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(232,147,58,0.15) 0%, transparent 100%);
    }

    /* ── Chart wrapper ── */
    .noon-chart {
        background: linear-gradient(145deg, rgba(12,12,16,0.98), rgba(16,15,18,0.95));
        border: 1px solid rgba(232, 147, 58, 0.05);
        border-radius: 18px;
        padding: 8px;
        margin-bottom: 18px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.3);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    .noon-chart::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(232,147,58,0.08) 50%, transparent 100%);
    }
    .noon-chart:hover {
        border-color: rgba(232, 147, 58, 0.12);
        box-shadow: 0 6px 35px rgba(0,0,0,0.4),
                    0 0 50px rgba(232, 147, 58, 0.02);
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #c47520, #e8933a) !important;
        color: #08080a !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        padding: 8px 22px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #e8933a, #f0a852) !important;
        box-shadow: 0 0 30px rgba(232, 147, 58, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Inputs ── */
    .stSlider > div > div > div > div { background: var(--amber) !important; }
    .stSlider label, .stSelectbox label, .stMultiSelect label, .stTextInput label {
        color: var(--text-dim) !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
    }
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(14,14,18,0.95) !important;
        border-color: rgba(232,147,58,0.1) !important;
        color: var(--text-light) !important;
        border-radius: 10px !important;
    }
    .stTextInput > div > div > input {
        background: rgba(14,14,18,0.95) !important;
        border-color: rgba(232,147,58,0.1) !important;
        color: var(--text-light) !important;
        border-radius: 10px !important;
    }

    /* ── Expander ── */
    details {
        background: rgba(12,12,16,0.95) !important;
        border: 1px solid rgba(232, 147, 58, 0.06) !important;
        border-radius: 14px !important;
    }
    details summary {
        color: var(--amber) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    /* ── Dataframe ── */
    .stDataFrame {
        border: 1px solid rgba(232, 147, 58, 0.06) !important;
        border-radius: 14px !important;
    }

    /* ── Footer ── */
    .noon-footer {
        text-align: center;
        padding: 35px 0;
        margin-top: 50px;
        border-top: 1px solid rgba(232, 147, 58, 0.06);
    }
    .noon-footer p {
        color: var(--text-muted);
        font-size: 0.75rem;
        letter-spacing: 0.5px;
    }
    .noon-footer span.highlight {
        color: var(--amber);
    }

    /* ── Hide defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ── Smooth scrolling ── */
    html { scroll-behavior: smooth; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def get_data():
    return load_and_merge_data()

df = get_data()


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style='text-align:center; padding: 22px 0 14px 0;'>
    <div style='width: 48px; height: 48px; margin: 0 auto 12px auto;
         background: radial-gradient(circle, rgba(232,147,58,0.12), transparent);
         border: 1px solid rgba(232,147,58,0.15); border-radius: 14px;
         display: flex; align-items: center; justify-content: center;'>
        <span style='font-size: 1.5rem;'>🏃</span>
    </div>
    <h2 style='margin:0; font-family: Playfair Display, serif;
        color: #f5f0e8; font-size: 1.15rem; font-weight: 700;
        letter-spacing: -0.3px;'>Boston Marathon</h2>
    <p style='color: #4a4540; font-size: 0.65rem; margin: 5px 0 0 0;
       letter-spacing: 2.5px; text-transform: uppercase; font-weight: 600;'>Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

filtered_df = apply_filters(df)

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='background: rgba(14,14,18,0.95); border: 1px solid rgba(232,147,58,0.08);
     border-radius: 14px; padding: 16px; text-align: center;
     position: relative; overflow: hidden;'>
    <div style='position:absolute; top:0; left:0; right:0; height:1px;
         background: linear-gradient(90deg, transparent, rgba(232,147,58,0.1), transparent);'></div>
    <span style='color: #4a4540; font-size: 0.62rem; text-transform: uppercase;
           letter-spacing: 2px; font-weight: 600;'>Active Records</span><br>
    <span style='color: #e8933a; font-size: 2rem; font-weight: 800;
           letter-spacing: -1px;'>{len(filtered_df)}</span>
    <span style='color: #3a3530; font-size: 0.85rem; font-weight: 500;'> / {len(df)}</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="noon-header">
    <div class="noon-badge">Data Visualization Project</div><br>
    <span class="noon-title">Boston <span>Marathon</span></span><br>
    <span class="noon-title" style="font-size: 2.2rem !important; opacity: 0.7;">Dashboard</span>
</div>
<p class="noon-sub">
    Comprehensive historical analysis of Boston Marathon winners<br>
    <span style="color: #e8933a; font-weight: 500;">Men's (1897–2024)</span> &
    <span style="color: #e86850; font-weight: 500;">Women's (1966–2024)</span> —
    Performance, Trends & Insights
</p>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════
def mins_to_hms(m):
    h = int(m // 60)
    mi = int(m % 60)
    s = int((m % 1) * 60)
    return f"{h}:{mi:02d}:{s:02d}"

def section(title, subtitle):
    st.markdown(f"""
    <div class="noon-section">
        <div class="noon-section-dot"></div>
        <div class="noon-section-info">
            <p class="noon-section-title">{title}</p>
            <p class="noon-section-sub">{subtitle}</p>
        </div>
        <div class="noon-section-line"></div>
    </div>
    """, unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No data matches the current filters. Adjust the filter criteria.")
    st.stop()


# ═══════════════════════════════════════════════════════════════
# KPI CARDS
# ═══════════════════════════════════════════════════════════════
avg_time = filtered_df["Time_Minutes"].mean()
fastest_time = filtered_df["Time_Minutes"].min()
slowest_time = filtered_df["Time_Minutes"].max()
fastest_row = filtered_df.loc[filtered_df["Time_Minutes"].idxmin()]
total_countries = filtered_df["Country"].nunique()
avg_speed = filtered_df["Speed_MPH"].mean()
year_span = f"{int(filtered_df['Year'].min())}-{int(filtered_df['Year'].max())}"

k1, k2, k3 = st.columns(3)
k1.metric("Total Records", f"{len(filtered_df)}", delta=f"{len(filtered_df['Gender'].unique())} categories")
k2.metric("Year Span", year_span)
k3.metric("Avg Finish Time", mins_to_hms(avg_time))

k4, k5, k6 = st.columns(3)
k4.metric("Fastest Record", mins_to_hms(fastest_time), delta=f"{fastest_row['Winner']}")
k5.metric("Countries", f"{total_countries}")
k6.metric("Avg Speed", f"{avg_speed:.2f} mph")


# ═══════════════════════════════════════════════════════════════
# SECTION 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════
section("Overview & Composition", "Country distribution and time frequency analysis")

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_pie_chart(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_histogram(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECTION 2 — TRENDS
# ═══════════════════════════════════════════════════════════════
section("Performance Trends", "How winning times have evolved across decades")

st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
st.pyplot(plot_line_chart(filtered_df))
st.markdown('</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_scatter(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_area_chart(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECTION 3 — COMPARISONS
# ═══════════════════════════════════════════════════════════════
section("Comparisons & Rankings", "Country standings and decade-wise breakdowns")

col5, col6 = st.columns(2)
with col5:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_bar_chart(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)
with col6:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_countplot(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECTION 4 — STATISTICAL
# ═══════════════════════════════════════════════════════════════
section("Statistical Distribution", "Spread, density, and correlation analysis")

col7, col8 = st.columns(2)
with col7:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_boxplot(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)
with col8:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_violin(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
st.pyplot(plot_heatmap(filtered_df))
st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECTION 5 — BONUS
# ═══════════════════════════════════════════════════════════════
section("Advanced Visualizations", "Bubble chart, funnel analysis, and pair plot")

col9, col10 = st.columns(2)
with col9:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_bubble_chart(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)
with col10:
    st.markdown('<div class="noon-chart">', unsafe_allow_html=True)
    st.pyplot(plot_funnel_chart(filtered_df))
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("🔗 Pair Plot — Multi-Feature Relationship Analysis", expanded=False):
    st.pyplot(plot_pairplot(filtered_df))


# ═══════════════════════════════════════════════════════════════
# DATA TABLE
# ═══════════════════════════════════════════════════════════════
section("Data Explorer", "Browse and inspect the filtered dataset")

display_cols = ["Year", "Winner", "Country", "Gender", "Time", "Distance (Miles)",
                "Distance (KM)", "Time_Minutes", "Pace_Per_Mile", "Speed_MPH", "Decade_Label"]
st.dataframe(
    filtered_df[display_cols].reset_index(drop=True),
    width="stretch",
    height=420,
)


# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="noon-footer">
    <p>
        Boston Marathon Data Visualization Dashboard<br>
        Built with <span class="highlight">Streamlit</span> ·
        <span class="highlight">Pandas</span> ·
        <span class="highlight">Matplotlib</span> ·
        <span class="highlight">Seaborn</span>
    </p>
</div>
""", unsafe_allow_html=True)

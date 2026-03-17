import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dashboard_utils import (
    inject_sidebar_style,
    load_income_status_data,
)

total_indicators = 22  # Update later if indicator list becomes dynamic
year_range = "1987–2024"
total_districts = 64 + 36

st.set_page_config(
    page_title="South Asia Data Observatory",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_sidebar_style()

# ---------- Theme Styling ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Spline+Sans:wght@400;500;600;700&display=swap');
:root {
    --bd-green: #22c55e;
    --bd-red: #f43f5e;
    --in-saffron: #ffb454;
    --in-navy: #1e3a8a;
    --in-green: #34d399;
    --ink: #e2e8f0;
    --muted: #94a3b8;
    --paper: #0b1220;
    --card: rgba(15, 23, 42, 0.85);
    --accent: #60a5fa;
    --accent-2: #38bdf8;
}
html, body, [class*="css"]  {
    font-family: "Spline Sans", system-ui, -apple-system, sans-serif;
}
body {
    color: var(--ink);
    background: linear-gradient(135deg, #0b1220 0%, #0f172a 45%, #111827 100%);
}
h1, h2, h3, h4 {
    font-family: "Fraunces", "Times New Roman", serif;
    color: var(--ink);
    letter-spacing: 0.2px;
}
.block-container { padding-top: 2.2rem; }
.hero {
    background: linear-gradient(135deg, rgba(12, 18, 32, 0.98), rgba(15, 23, 42, 0.96));
    border-radius: 26px;
    padding: 44px 48px;
    color: white;
    text-align: left;
    box-shadow: 0 22px 50px rgba(2, 6, 23, 0.2);
    margin: 10px 0 28px 0;
    position: relative;
    overflow: hidden;
}
.hero-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 0.2px;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 17px;
    opacity: 0.92;
    max-width: 700px;
    line-height: 1.65;
}
.hero-accent {
    width: 72px;
    height: 6px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(96, 165, 250, 0.9), rgba(34, 197, 94, 0.9));
    margin: 14px 0 16px 0;
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.45);
}
.hero-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 18px;
}
.hero-stat {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(148, 163, 184, 0.18);
    border: 1px solid rgba(148, 163, 184, 0.25);
    font-size: 12px;
    font-weight: 600;
    color: var(--ink);
}
.hero-pill {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(255,255,255,0.18);
    font-weight: 600;
    font-size: 12px;
    margin-bottom: 10px;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    color: white;
}
.hero-grid {
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    gap: 22px;
    align-items: center;
}
.hero-panel {
    background: rgba(255, 255, 255, 0.14);
    border-radius: 18px;
    padding: 16px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.hero-metric {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.1);
    margin-bottom: 10px;
}
.hero-metric:last-child { margin-bottom: 0; }
.hero-metric strong { font-size: 16px; }
.hero-metric span { font-size: 12px; opacity: 0.85; }
.card {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
    transition: all 0.3s ease;
}
.card-title { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
.card-sub { color: var(--muted); font-size: 14px; margin-bottom: 10px; }
.section-kicker {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
}
.section-title {
    font-size: 30px;
    font-weight: 800;
    margin: 6px 0 8px 0;
}
.section-sub {
    color: var(--muted);
    max-width: 760px;
    line-height: 1.6;
}
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi-card {
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 16px;
    border: 1px solid rgba(148, 163, 184, 0.25);
    transition: all 0.25s ease;
}
.kpi-label { font-size: 12px; color: var(--muted); margin-bottom: 6px; }
.kpi-value { font-size: 22px; font-weight: 800; color: var(--ink); }
.map-card {
    background: var(--card);
    border-radius: 18px;
    border: 1px solid rgba(15, 23, 42, 0.08);
    box-shadow: 0 14px 36px rgba(15, 23, 42, 0.1);
    padding: 18px;
    margin-bottom: 12px;
}
.map-title { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.map-sub { color: var(--muted); font-size: 13px; margin-bottom: 0; }
.feature-list { margin: 8px 0 0 0; }
.feature-list li { margin-bottom: 6px; }
.source-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(148, 163, 184, 0.12);
    border: 1px solid rgba(148, 163, 184, 0.2);
    font-size: 12px;
    font-weight: 600;
    color: #e2e8f0;
}
.source-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #138808;
}
.flag-row { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.flag {
    width: 48px;
    height: 32px;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 6px 12px rgba(15, 23, 42, 0.18);
}
.stButton > button {
    width: 100%;
    font-weight: 700;
    border-radius: 10px;
}
.card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 18px 40px rgba(0,0,0,0.18);
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.15);
}
.nav-card {
    background: var(--card);
    border-radius: 16px;
    border: 1px solid rgba(15, 23, 42, 0.08);
    padding: 16px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
}
.nav-card h4 { margin: 0 0 6px 0; }
.nav-card p { margin: 0 0 12px 0; color: var(--muted); font-size: 13px; }
.nav-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(96, 165, 250, 0.2);
    color: #bfdbfe;
    font-size: 12px;
    font-weight: 600;
}
.trust-section {
    background: radial-gradient(900px 420px at 10% -20%, rgba(15, 118, 110, 0.35), transparent 60%),
        radial-gradient(800px 400px at 90% 0%, rgba(2, 132, 199, 0.35), transparent 55%),
        #0b1220;
    border-radius: 24px;
    padding: 36px;
    color: #f8fafc;
    box-shadow: 0 20px 50px rgba(2, 6, 23, 0.45);
}
.trust-kicker {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(248, 250, 252, 0.08);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
.trust-title {
    font-size: 32px;
    font-weight: 800;
    margin: 12px 0 10px 0;
}
.trust-sub {
    font-size: 15px;
    color: #cbd5f5;
    max-width: 760px;
}
.trust-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-top: 24px;
}
.trust-card {
    background: #111827;
    color: #e2e8f0;
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 12px 30px rgba(2, 6, 23, 0.18);
}
.trust-stat {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 6px;
}
.trust-text {
    font-size: 13px;
    color: #cbd5f5;
    line-height: 1.6;
}
.trust-chip {
    display: inline-block;
    padding: 3px 6px;
    border-radius: 6px;
    background: rgba(96, 165, 250, 0.2);
    color: #bfdbfe;
    font-weight: 600;
}
.trust-sources {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 16px;
    padding: 16px 18px;
    margin-top: 18px;
    color: #e2e8f0;
    border: 1px solid rgba(148, 163, 184, 0.2);
}
.trust-sources h4 {
    margin: 0 0 8px 0;
    font-size: 15px;
}
.trust-sources ul {
    margin: 0;
    padding-left: 18px;
    color: #cbd5f5;
    font-size: 13px;
}
.region-section {
    background: radial-gradient(900px 420px at 10% -20%, rgba(14, 116, 144, 0.35), transparent 60%),
        radial-gradient(800px 400px at 90% 0%, rgba(15, 118, 110, 0.35), transparent 55%),
        #0b1220;
    padding: 32px;
    border-radius: 22px;
    margin-bottom: 20px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    box-shadow: 0 20px 50px rgba(2, 6, 23, 0.45);
}
.region-title { font-size: 28px; font-weight: 800; color: #f8fafc; text-align: center; }
.region-sub { color: #cbd5f5; margin: 6px auto 24px auto; text-align: center; max-width: 720px; }
.region-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.region-card {
    padding: 22px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 14px;
    background-color: rgba(15, 23, 42, 0.75);
    box-shadow: 0 12px 30px rgba(2, 6, 23, 0.4);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.region-card:hover { transform: translateY(-6px); border-color: #38bdf8; box-shadow: 0 16px 34px rgba(2, 6, 23, 0.6); }
.region-icon {
    font-size: 28px;
    margin-bottom: 10px;
    width: 44px;
    height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: rgba(56, 189, 248, 0.15);
    color: #7dd3fc;
}
.region-meta {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #94a3b8;
    margin-top: 16px;
    padding-top: 10px;
    border-top: 1px solid rgba(148, 163, 184, 0.2);
}
[data-testid="stImage"] img {
    width: 100%;
    max-width: 900px;
    display: block;
    margin: 0 auto;
    border-radius: 12px;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.18);
    filter: saturate(1.05) contrast(1.06) brightness(1.02);
}
[data-testid="stImage"] img:hover {
    transform: scale(1.01);
    box-shadow: 0 20px 45px rgba(15, 23, 42, 0.25);
    transition: all 0.3s ease-in-out;
}
@media (max-width: 900px) {
    .hero { padding: 28px; }
    .hero-title { font-size: 30px; }
    .hero-grid { grid-template-columns: 1fr; }
    .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    .trust-grid { grid-template-columns: repeat(1, 1fr); }
    .region-grid { grid-template-columns: repeat(1, 1fr); }
}
</style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
st.sidebar.title("📊 Data Explorer")
st.sidebar.markdown("Navigation")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Bangladesh.py", label="Bangladesh")
st.sidebar.page_link("pages/1_India.py", label="India")
st.sidebar.markdown("---")

# ---------- Hero Section ----------
st.markdown(
    f"""
<div class="hero">
    <div>
        <div class="hero-pill">South Asia Data Observatory</div>
        <div class="hero-title">🌏 Mapping the Pulse of South Asian Development</div>
        <div class="hero-accent"></div>
        <div class="hero-subtitle">
            An interactive analytics platform for exploring population, health,
            education, infrastructure, and economic indicators across Bangladesh
            and India — enabling evidence-driven research and policy insight.
        </div>
        <div class="hero-stats">
            <div class="hero-stat">📊 {total_indicators} Indicators</div>
            <div class="hero-stat">🗺️ {total_districts} Regions</div>
            <div class="hero-stat">📅 {year_range} Data</div>
        </div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------- South Asia Focus Map ----------
# st.markdown(
#     """
#     <div class="map-card">
#         <div class="map-title">South Asia Focus</div>
#         <div class="map-sub">Highlighted focus countries within the South Asia region.</div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )
img_col_left, img_col_center, img_col_right = st.columns([1, 6, 1])
with img_col_center:
    st.image("south-asia-map.jpg", width=900)

st.divider()

# ---------- Dashboard Selection ----------
st.markdown(
    """
    <section class="region-section">
        <div class="region-title">Explore by Region</div>
        <div class="region-sub">Dive into comprehensive data for countries and divisions across Bangladesh and India.</div>
        <div class="region-grid">
            <div class="region-card">
                <div class="region-icon">🌍</div>
                <h4>Countries</h4>
                <p>Compare national indicators and rankings across Bangladesh and India.</p>
                <div class="region-meta">
                    <span>2 countries</span>
                    <span>→</span>
                </div>
            </div>
            <div class="region-card">
                <div class="region-icon">🏛️</div>
                <h4>Divisions & Districts</h4>
                <p>Explore regional disparities with division and district-level analytics.</p>
                <div class="region-meta">
                    <span>8 divisions · 64 districts</span>
                    <span>→</span>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.container():
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown(
            """
            <div class="nav-card">
                <div class="nav-pill">🇧🇩 Country profile</div>
                <h4>Bangladesh</h4>
                <p>National indicators, rankings, and progress trends.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/2_Bangladesh.py", label="Open Bangladesh dashboard")
    with c2:
        st.markdown(
            """
            <div class="nav-card">
                <div class="nav-pill">🇮🇳 Country profile</div>
                <h4>India</h4>
                <p>State-level comparisons and development snapshots.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/1_India.py", label="Open India dashboard")
    with c3:
        st.markdown(
            """
            <div class="nav-card">
                <div class="nav-pill">🧭 Sub-national</div>
                <h4>Divisions & Districts</h4>
                <p>Granular disparities across divisions and districts.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/3_District.py", label="Open district dashboard")

st.divider()

# ---------- Income Status Comparison ----------
st.subheader("🏦 Income Classification Comparison")
income_status_df = load_income_status_data()
if {"Year", "Bangladesh", "India"}.issubset(income_status_df.columns):
    income_tmp = income_status_df.copy()
    income_tmp["Year"] = pd.to_numeric(income_tmp["Year"], errors="coerce")
    income_tmp = income_tmp.dropna(subset=["Year"]).sort_values("Year")

    def _segments(series: pd.Series) -> list[tuple[int, int, str]]:
        segs: list[tuple[int, int, str]] = []
        if series.empty:
            return segs
        start_year = int(series.index[0])
        prev = series.iloc[0]
        for year, status in series.iloc[1:].items():
            if status != prev:
                segs.append((start_year, int(year), str(prev)))
                start_year = int(year)
                prev = status
        segs.append((start_year, int(series.index[-1]) + 1, str(prev)))
        return segs

    colors = {
        "Low-income countries": "#ef4444",
        "Lower-middle-income countries": "#f59e0b",
        "Upper-middle-income countries": "#10b981",
        "High-income countries": "#3b82f6",
    }

    fig_income = go.Figure()
    lane_y = {"Bangladesh": 1, "India": 0}
    lane_height = 0.35

    for country in ["Bangladesh", "India"]:
        series = income_tmp.set_index("Year")[country].dropna()
        for start, end, status in _segments(series):
            fig_income.add_shape(
                type="rect",
                x0=start,
                x1=end,
                y0=lane_y[country] - lane_height,
                y1=lane_y[country] + lane_height,
                line=dict(width=0),
                fillcolor=colors.get(status, "#94a3b8"),
                layer="below",
            )
            fig_income.add_trace(
                go.Scatter(
                    x=[(start + end - 1) / 2],
                    y=[lane_y[country]],
                    mode="markers",
                    marker=dict(size=18, color="rgba(0,0,0,0)"),
                    hovertemplate=f"{country}<br>{start}–{end-1}<br>{status}<extra></extra>",
                    showlegend=False,
                )
            )
            fig_income.add_trace(
                go.Scatter(
                    x=[(start + end - 1) / 2],
                    y=[lane_y[country]],
                    mode="text",
                    text=[status],
                    textfont=dict(size=11, color="white"),
                    showlegend=False,
                    hovertemplate=f"{country}<br>{start}–{end-1}<br>{status}<extra></extra>",
                )
            )

    upgrade_bd = 2014
    upgrade_in = 2007
    fig_income.add_vline(x=upgrade_bd, line_dash="dash", line_color="#006a4e", annotation_text="BD upgrade")
    fig_income.add_vline(x=upgrade_in, line_dash="dash", line_color="#ff9933", annotation_text="India upgrade")

    fig_income.update_yaxes(
        tickmode="array",
        tickvals=[lane_y["Bangladesh"], lane_y["India"]],
        ticktext=["Bangladesh", "India"],
        range=[-0.8, 1.8],
        showgrid=False,
        zeroline=False,
    )
    fig_income.update_xaxes(showgrid=False)
    fig_income.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title="Income Status Progress",
    )
    st.plotly_chart(fig_income, use_container_width=True)
else:
    st.info("Income classification chart skipped. Missing Year/Bangladesh/India columns.")

# ---------- Coverage Stats ----------
st.subheader("📈 Current Coverage")

st.markdown(
    """
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Districts (BD)</div>
            <div class="kpi-value">64 / 64</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">States + UTs (IN)</div>
            <div class="kpi-value">36 / 36</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Core Indicators</div>
            <div class="kpi-value">22</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Last Major Update</div>
            <div class="kpi-value">2024–25</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# st.caption("Sources: BBS, MoHFW BD, NITI Aayog, MoSPI India, Census, NFHS, SRS, DISE, etc.")

st.divider()

# ---------- Data Authenticity ----------
st.subheader("✅ Data Authenticity & Sources")
st.markdown(
    """
    <section class="trust-section">
        <div class="trust-kicker">Verified sources</div>
        <div class="trust-title">We went deep into the data so you don't have to.</div>
        <div class="trust-sub">
            Official national datasets and international institutions are reconciled and cross-checked
            before visualization to deliver reliable, decision-grade indicators.
        </div>
        <div class="trust-grid">
            <div class="trust-card">
                <div class="trust-stat">20+ Indicators</div>
                <div class="trust-text">
                    Harmonized across districts and states, covering demographics, health,
                    education, and infrastructure with consistent definitions.
                </div>
            </div>
            <div class="trust-card">
                <div class="trust-stat">1987–2024</div>
                <div class="trust-text">
                    Time-series coverage for income classification and national macro indicators
                    spanning multiple census and survey cycles.
                </div>
            </div>
            <div class="trust-card">
                <div class="trust-stat">Trusted Global Sources</div>
                <div class="trust-text">
                    Our analytics engine pulls and reconciles data from
                    <span class="trust-chip">UNDP</span>,
                    <span class="trust-chip">World Population Review</span>,
                    <span class="trust-chip">Data Pandas</span>,
                    <span class="trust-chip">World Bank</span>
                    and official national ministries to ensure absolute provenance.
                </div>
            </div>
        </div>
        <div class="trust-sources">
            <h4>Primary sources</h4>
            <ul>
                <li>BBS (Bangladesh), MoHFW BD, NITI Aayog, MoSPI India</li>
                <li>UNDP, World Population Review, SRS, DISE, World Bank</li>
            </ul>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# ---------- About ----------
with st.expander("📊 About This Project", expanded=False):

    st.markdown(
        """
**Purpose**  
Make complex regional development data accessible and comparable through interactive visualizations.

**Key features**
<ul class="feature-list">
    <li>🗺️ <b>Interactive Maps:</b> Choropleth & bubble visualizations</li>
    <li>📊 <b>Deep Analytics:</b> Radar charts & HDI-like composites</li>
    <li>📈 <b>Time Trends:</b> Year-on-year change & comparisons</li>
    <li>🧮 <b>Advanced Metrics:</b> Gini, Theil, and composite scoring</li>
    <li>⬇️ <b>Downloads:</b> Filtered tables & exports</li>
</ul>

**Currently available**
- Bangladesh district profiles
- India state & UT comparisons

Built with **Streamlit, Altair/Pydeck/Plotly, Pandas & GeoPandas**.
        """,
        unsafe_allow_html=True,
    )

st.caption("Regional Development Intelligence Dashboard • Last updated March 2026")

import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

from dashboard_utils import (
    inject_sidebar_style,
    load_bangladesh_data,
    load_bangladesh_gdp_data,
    load_bangladesh_literacy_data,
    load_bangladesh_population_growth_data,
    load_income_status_data,
    render_income_status_chart,
    render_country_page,
)

st.set_page_config(page_title="Bangladesh Analytics", page_icon="🇧🇩", layout="wide")

inject_sidebar_style()

# ---------- THEME (DARK) ----------
st.markdown(
    """
    <style>
    :root {
        --brand-green: #2ECC71;
        --brand-red: #E74C3C;
        --brand-blue: #3498DB;
        --brand-dark: #0b1220;
        --brand-card: #0f172a;
        --brand-text: #e2e8f0;
        --brand-muted: #94a3b8;
    }
    .section-header {
        font-size: 22px;
        font-weight: 600;
        border-left: 5px solid var(--brand-green);
        padding-left: 14px;
        margin-top: 18px;
        margin-bottom: 16px;
        color: var(--brand-text);
        letter-spacing: 0.2px;
    }
    .premium-card {
        background: var(--brand-card);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.35);
        margin-bottom: 16px;
    }
    .premium-card h4 {
        margin: 0 0 10px 0;
        color: var(--brand-text);
        font-weight: 600;
    }
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(1200px 600px at 10% -10%, rgba(46,204,113,0.15), transparent 60%),
                    radial-gradient(900px 500px at 100% 0%, rgba(52,152,219,0.18), transparent 55%),
                    var(--brand-dark);
    }
    [data-testid="stSidebar"] {
        background: #0a0f1c;
        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }
    [data-testid="stMarkdownContainer"] p, 
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: var(--brand-text);
    }
    .stTabs [role="tablist"] {
        background: rgba(15, 23, 42, 0.65);
        border-radius: 12px;
        padding: 6px;
        border: 1px solid rgba(148, 163, 184, 0.18);
    }
    .stTabs [role="tab"] {
        color: var(--brand-muted);
        font-weight: 600;
        border-radius: 10px;
        padding: 8px 14px;
    }
    .stTabs [aria-selected="true"] {
        color: #0b1220 !important;
        background: linear-gradient(120deg, #2ECC71, #38bdf8);
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------
st.sidebar.title("📊 Data Explorer")
st.sidebar.markdown("Navigation")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Bangladesh.py", label="Bangladesh")
st.sidebar.page_link("pages/1_India.py", label="India")
st.sidebar.markdown("---")
st.sidebar.markdown("🌍 Regional Dashboard")

# ---------- LOAD DATA ----------
bangladesh_df = load_bangladesh_data()
bangladesh_gdp_df = load_bangladesh_gdp_data()
bangladesh_literacy_df = load_bangladesh_literacy_data()
bangladesh_population_df = load_bangladesh_population_growth_data()
income_status_df = load_income_status_data()

size_params = [
    "population",
    "population_density",
    "working_age_pop",
    "area_km2",
]

color_params = [
    "development_score",
    "poverty_rate",
    "extreme_poverty_rate",
    "literacy_rate",
    "school_attendance",
    "electricity_access",
    "tap_water_access",
    "flush_toilet_access",
    "health_index",
]


# ---------- HELPERS ----------
def _to_numeric(series: pd.Series) -> pd.Series:
    # স্ট্রিং থেকে নিরাপদভাবে সংখ্যায় রূপান্তর করে
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


# ---------- KPI ----------
def _render_bangladesh_kpis(*, plot_df: pd.DataFrame) -> None:
    # বাংলাদেশ কিপিআই কার্ডগুলো রেন্ডার করে
    districts = plot_df["Name"].dropna().nunique() if "Name" in plot_df.columns else len(plot_df)
    total_population = (
        _to_numeric(plot_df["population"]).fillna(0).sum()
        if "population" in plot_df.columns
        else 0
    )
    latest_literacy = 0
    if {"Year", "Literacy Rate(%)"}.issubset(bangladesh_literacy_df.columns):
        lita = bangladesh_literacy_df.copy()
        lita["Year"] = _to_numeric(lita["Year"])
        lita["Literacy Rate(%)"] = _to_numeric(lita["Literacy Rate(%)"])
        lita = lita.dropna(subset=["Year", "Literacy Rate(%)"]).sort_values("Year")
        if not lita.empty:
            latest_literacy = float(lita.iloc[-1]["Literacy Rate(%)"])
    avg_poverty = (
        _to_numeric(plot_df["poverty_rate"]).mean()
        if "poverty_rate" in plot_df.columns
        else 0
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Districts", f"{int(districts):,}")
    with k2:
        st.metric("Population", f"{int(total_population):,}")
    with k3:
        st.metric("Literacy", f"{latest_literacy:.2f}%")
    with k4:
        st.metric("Poverty", f"{avg_poverty:.2f}%")


# ---------- HERO HEADER ----------
def _render_bangladesh_overall_header(*, plot_df: pd.DataFrame) -> None:
    # বাংলাদেশ ড্যাশবোর্ডের হিরো হেডার রেন্ডার করে
    st.markdown(
        """
        <style>
        .country-hero {
            background: #eaf3f1;
            padding: 32px;
            border-radius: 16px;
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 32px;
            align-items: start;
            margin-bottom: 25px;
        }
        .country-crumb {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .country-title {
            font-size: 36px;
            font-weight: 700;
            color: #0f172a;
        }
        .country-flag {
            width: 120px;
            height: 80px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 14px rgba(0,0,0,0.12);
        }
        .country-meta {
            font-size: 15px;
            color: #334155;
            line-height: 1.7;
        }
        .country-desc {
            font-size: 16px;
            color: #334155;
            line-height: 1.7;
        }
        [data-testid="stMetric"] {
            background: white;
            padding: 16px;
            border-radius: 14px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
        [data-testid="stMetricValue"] {
            font-size: 30px;
            font-weight: 700;
        }
        @media (prefers-color-scheme: dark) {
            .country-hero {
                background: #0b1220;
                border: 1px solid rgba(148, 163, 184, 0.18);
            }
            .country-crumb { color: #94a3b8; }
            .country-title { color: #e2e8f0; }
            .country-meta { color: #cbd5f5; }
            .country-desc { color: #cbd5f5; }
            .country-meta b { color: #f1f5f9; }
            [data-testid="stMetric"] {
                background: #0f172a;
                box-shadow: 0 6px 20px rgba(0,0,0,0.45);
                border: 1px solid rgba(148, 163, 184, 0.18);
            }
            [data-testid="stMetricValue"] { color: #f8fafc; }
            [data-testid="stMetricLabel"] { color: #cbd5f5; }
        }
        @media (max-width: 900px) {
            .country-hero { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    flag_svg = """
    <svg viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="80" fill="#006a4e"/>
        <circle cx="52" cy="40" r="20" fill="#f42a41"/>
    </svg>
    """

    st.markdown(
        f"""
        <div class="country-hero">
            <div>
                <div class="country-crumb">Countries &nbsp;›&nbsp; Bangladesh</div>
                <div style="display:flex;align-items:center;gap:16px;margin-bottom:12px;">
                    <div class="country-flag">{flag_svg}</div>
                    <div class="country-title">Bangladesh</div>
                </div>
                <div class="country-meta">
                    <b>Capital:</b> Dhaka<br/>
                    <b>Continent:</b> Asia<br/>
                    <b>Region:</b> Southern Asia<br/>
                    <b>Largest Cities:</b> Dhaka, Chittagong, Sylhet<br/>
                    <b>Abbreviation:</b> BGD
                </div>
            </div>
            <div class="country-desc">
                Bangladesh is a country in Asia, known for the Sundarbans mangroves and Bengal Delta. It has a population of nearly 178 million, making it the 8th largest country in the world. Its capital is Dhaka. Bangladesh has a export-oriented economy with strong garment sector.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- ANALYTICS ----------
def _render_data_quality_alerts(
    *,
    district_df: pd.DataFrame,
    gdp_df: pd.DataFrame,
    literacy_df: pd.DataFrame,
    population_df: pd.DataFrame,
    income_df: pd.DataFrame,
) -> None:
    # চার্ট দেখানোর আগে ডাটা কোয়ালিটি সম্পর্কে সতর্কতা দেখায়
    issues: list[str] = []

    def _missing_cols(df: pd.DataFrame, cols: set[str]) -> list[str]:
        return sorted(cols - set(df.columns))

    district_missing = _missing_cols(
        district_df, {"Name", "division", "literacy_rate", "population", "poverty_rate"}
    )
    if district_missing:
        issues.append(f"District data missing columns: {', '.join(district_missing)}.")

    gdp_missing = _missing_cols(gdp_df, {"Country Name", "Year", "GDP"})
    if gdp_missing:
        issues.append(f"GDP data missing columns: {', '.join(gdp_missing)}.")

    inflation_missing = _missing_cols(literacy_df, {"Year", "Inflation Rate (%)"})
    if inflation_missing:
        issues.append(f"Inflation data missing columns: {', '.join(inflation_missing)}.")

    literacy_missing = _missing_cols(literacy_df, {"Year", "Literacy Rate(%)"})
    if literacy_missing:
        issues.append(f"Literacy data missing columns: {', '.join(literacy_missing)}.")

    population_missing = _missing_cols(population_df, {"latitude", "longitude", "population", "popGrowth"})
    if population_missing:
        issues.append(f"Population data missing columns: {', '.join(population_missing)}.")

    income_missing = _missing_cols(income_df, {"Year", "Bangladesh"})
    if income_missing:
        issues.append(f"Income status data missing columns: {', '.join(income_missing)}.")

    if issues:
        st.warning("Data Quality Alert")
        for item in issues:
            st.write(f"• {item}")


def render_bangladesh_overall_analysis(*, plot_df: pd.DataFrame) -> None:
    # বাংলাদেশ জাতীয় অ্যানালিটিক্স সেকশন রেন্ডার করে
    # ডাটা কোয়ালিটি চেক করে প্রাথমিক সতর্কতা দেখায়
    _render_data_quality_alerts(
        district_df=plot_df,
        gdp_df=bangladesh_gdp_df,
        literacy_df=bangladesh_literacy_df,
        population_df=bangladesh_population_df,
        income_df=income_status_df,
    )
    required_cols = {"Name", "division", "literacy_rate", "population", "poverty_rate"}
    missing = sorted(required_cols - set(plot_df.columns))
    if missing:
        st.info(f"National analytics skipped. Missing columns: {', '.join(missing)}.")
        st.subheader("Data Table")
        st.dataframe(
            plot_df,
            use_container_width=True,
            hide_index=True,
        )
        return

    temp = plot_df.copy()
    temp["literacy_rate"] = _to_numeric(temp["literacy_rate"])
    temp["population"] = _to_numeric(temp["population"])
    temp["poverty_rate"] = _to_numeric(temp["poverty_rate"])

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Economy", "Education & Poverty", "Population"])

    with tab1:
        st.markdown('<div class="section-header">Economic Performance & Market Stability</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="premium-card"><h4>Bangladesh GDP Trend</h4>', unsafe_allow_html=True)
            gdp_required_cols = {"Country Name", "Year", "GDP"}
            gdp_missing = sorted(gdp_required_cols - set(bangladesh_gdp_df.columns))
            if gdp_missing:
                st.info(f"GDP trend skipped. Missing columns: {', '.join(gdp_missing)}.")
            else:
                gdp_temp = bangladesh_gdp_df.copy()
                gdp_temp = gdp_temp[gdp_temp["Country Name"].astype(str).str.strip() == "Bangladesh"]
                gdp_temp["Year"] = _to_numeric(gdp_temp["Year"])
                gdp_temp["GDP"] = _to_numeric(gdp_temp["GDP"])
                gdp_temp = gdp_temp.dropna(subset=["Year", "GDP"]).sort_values("Year")

                if gdp_temp.empty:
                    st.info("GDP trend skipped. No Bangladesh records found.")
                else:
                    fig_gdp = px.line(
                        gdp_temp,
                        x="Year",
                        y="GDP",
                        markers=True,
                        hover_name="Country Name",
                        title=None,
                        height=330,
                    )
                    fig_gdp.update_traces(line=dict(color="#3498DB"), marker=dict(color="#3498DB"))
                    fig_gdp.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
                    st.plotly_chart(fig_gdp, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="premium-card"><h4>Inflation Rate</h4>', unsafe_allow_html=True)
            inflation_required_cols = {"Year", "Inflation Rate (%)"}
            inflation_missing = sorted(inflation_required_cols - set(bangladesh_literacy_df.columns))
            if inflation_missing:
                st.info(f"Inflation trend skipped. Missing columns: {', '.join(inflation_missing)}.")
            else:
                lita = bangladesh_literacy_df.copy()
                lita["Year"] = _to_numeric(lita["Year"])
                lita["Inflation Rate (%)"] = _to_numeric(lita["Inflation Rate (%)"])
                lita = lita.dropna(subset=["Year", "Inflation Rate (%)"]).sort_values("Year")

                if lita.empty:
                    st.info("Inflation trend skipped. No records found.")
                else:
                    fig_inflation = px.line(
                        lita,
                        x="Year",
                        y="Inflation Rate (%)",
                        title=None,
                        height=330,
                    )
                    fig_inflation.update_traces(
                        mode="lines+markers",
                        line=dict(color="#E74C3C"),
                        marker=dict(color="#E74C3C"),
                        hovertemplate="Year: %{x}<br>Inflation Rate: %{y:.2f}%<extra></extra>",
                    )
                    fig_inflation.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
                    st.plotly_chart(fig_inflation, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="premium-card" style="margin-bottom: 25px;"><h4>World Bank Income Classification</h4></div>', unsafe_allow_html=True)
    
        fig_income = None
        if {"Year", "Bangladesh"}.issubset(income_status_df.columns):
            fig_income = render_income_status_chart(
                income_status_df,
                selected_countries=["Bangladesh"],
                title="Income Classification Journey (1987–2024)",
            )

        if fig_income is not None:
            fig_income.update_layout(margin=dict(l=0, r=0, t=60, b=0), template="plotly_dark")
            title_pad=dict(t=10, b=10)
            st.plotly_chart(fig_income, use_container_width=True)

            transition_year = income_status_df[
                income_status_df["Bangladesh"] == "Lower-middle-income countries"
            ]["Year"].min()
            if pd.notna(transition_year):
                st.success(
                    f"**Key Milestone:** Bangladesh transitioned to **Lower-middle-income** status in **{int(transition_year)}**."
                )
            else:
                st.info("Income classification data is empty.")
        else:
            st.warning("⚠️ Data missing: Ensure 'Year' and 'Bangladesh' columns are present in the dataset.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-header">Education & Poverty Lens</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)

        with c3:
            st.markdown('<div class="premium-card"><h4>Literacy Trend</h4>', unsafe_allow_html=True)
            if {"Year", "Literacy Rate(%)"}.issubset(bangladesh_literacy_df.columns):
                lita = bangladesh_literacy_df.copy()
                lita["Year"] = _to_numeric(lita["Year"])
                lita["Literacy Rate(%)"] = _to_numeric(lita["Literacy Rate(%)"])
                lita = lita.dropna(subset=["Year", "Literacy Rate(%)"]).sort_values("Year")

                if not lita.empty:
                    fig_lit = px.line(
                        lita,
                        x="Year",
                        y="Literacy Rate(%)",
                        title=None,
                        height=330,
                    )
                    fig_lit.update_traces(
                        mode="lines+markers",
                        line=dict(color="#2ECC71"),
                        marker=dict(color="#2ECC71"),
                        hovertemplate="Year: %{x}<br>Literacy Rate: %{y:.2f}%<extra></extra>",
                    )
                    fig_lit.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
                    st.plotly_chart(fig_lit, use_container_width=True)
            else:
                st.info("Literacy trend skipped. Missing columns: Year, Literacy Rate(%).")
            st.markdown("</div>", unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="premium-card"><h4>Poverty Hotspots</h4>', unsafe_allow_html=True)
            top_poor = temp.nlargest(10, "poverty_rate")
            fig4 = px.bar(
                top_poor,
                x="Name",
                y="poverty_rate",
                title=None,
                color="poverty_rate",
                color_continuous_scale=["#E74C3C", "#F39C12"],
                height=330,
            )
            fig4.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        c5, c6 = st.columns(2)
        with c5:
            st.markdown('<div class="premium-card"><h4>Top Literacy Districts</h4>', unsafe_allow_html=True)
            top_lit = temp.nlargest(10, "literacy_rate")
            fig1 = px.bar(
                top_lit,
                x="Name",
                y="literacy_rate",
                title=None,
                color="literacy_rate",
                color_continuous_scale=["#2ECC71", "#9AE6B4"],
                height=330,
            )
            fig1.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c6:
            st.markdown('<div class="premium-card"><h4>Lowest Literacy Districts</h4>', unsafe_allow_html=True)
            low_lit = temp.nsmallest(10, "literacy_rate")
            fig2 = px.bar(
                low_lit,
                x="Name",
                y="literacy_rate",
                title=None,
                color="literacy_rate",
                color_continuous_scale=["#E74C3C", "#F7B7A3"],
                height=330,
            )
            fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="premium-card"><h4>Division Averages: Literacy vs Poverty</h4>', unsafe_allow_html=True)
        division_summary = (
            temp.groupby("division")[["literacy_rate", "poverty_rate"]]
            .mean()
            .reset_index()
            .sort_values("division")
        )
        division_long = division_summary.melt(
            id_vars="division",
            value_vars=["literacy_rate", "poverty_rate"],
            var_name="Metric",
            value_name="Value",
        )
        division_long["Metric"] = division_long["Metric"].str.replace("_", " ").str.title()
        fig_division = px.bar(
            division_long,
            x="division",
            y="Value",
            color="Metric",
            barmode="group",
            title=None,
            height=360,
        )
        fig_division.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
        st.plotly_chart(fig_division, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-header">Demographic Distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="premium-card"><h4>Population Hotspots</h4>', unsafe_allow_html=True)
        label_col = "division" if "division" in bangladesh_population_df.columns else "city"
        required_cols = {"latitude", "longitude", "population", "popGrowth", label_col}
        missing = sorted(required_cols - set(bangladesh_population_df.columns))

        if missing:
            st.info(f"Population map skipped. Missing columns: {', '.join(missing)}.")
        else:
            city_df = bangladesh_population_df.copy()
            city_df["latitude"] = _to_numeric(city_df["latitude"])
            city_df["longitude"] = _to_numeric(city_df["longitude"])
            city_df["population"] = _to_numeric(city_df["population"])
            city_df["popGrowth"] = _to_numeric(city_df["popGrowth"])
            city_df = city_df.dropna(subset=["latitude", "longitude", "population", "popGrowth"])

            fig = px.density_mapbox(
                temp,
                lat="lat",
                lon="lon",
                z=np.log1p(temp["population"]),
                radius=36,
                zoom=6,
                center=dict(lat=23.7, lon=90.3),
                height=520,
                mapbox_style="carto-positron",
                color_continuous_scale="YlOrRd",
                hover_name=temp["Name"],
                title=None,
                opacity=0.85,
            )

            fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
            fig.update_coloraxes(colorbar_title="Population Intensity")
            fig.add_scattermapbox(
                lat=temp["lat"],
                lon=temp["lon"],
                mode="markers+text",
                text=temp["Name"],
                textposition="top center",
                marker=dict(size=8, color="#3838f8"),
                hovertext=(
                    temp["Name"]
                    + "<br>Population: "
                    + temp["population"].map("{:,}".format)
                ),
                name="Name",
            )

            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        r2, r3 = st.columns(2)
        with r2:
            st.markdown('<div class="premium-card"><h4>Population Growth Rate</h4>', unsafe_allow_html=True)
            label_col = "division" if "division" in bangladesh_population_df.columns else "city"
            if {label_col, "popGrowth"}.issubset(bangladesh_population_df.columns):
                city_df = bangladesh_population_df.copy()
                city_df["popGrowth"] = _to_numeric(city_df["popGrowth"])
                city_df = city_df.dropna(subset=["popGrowth"]).sort_values("popGrowth", ascending=False)

                fig = px.bar(
                    city_df,
                    x=label_col,
                    y="popGrowth",
                    color="popGrowth",
                    title=None,
                    color_continuous_scale=["#3498DB", "#38bdf8"],
                    height=330,
                )
                fig.update_layout(
                    xaxis_title="Region",
                    yaxis_title="Growth Rate",
                    margin=dict(l=0, r=0, t=10, b=0),
                    template="plotly_dark",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"Population growth chart skipped. Missing columns: {label_col}, popGrowth.")
            st.markdown("</div>", unsafe_allow_html=True)

        with r3:
            st.markdown('<div class="premium-card"><h4>Population Distribution</h4>', unsafe_allow_html=True)
            if {"Name", "population"}.issubset(temp.columns):
                top_pop = temp.nlargest(10, "population")
                fig3 = px.pie(
                    top_pop,
                    values="population",
                    names="Name",
                    title=None,
                    hole=0.45,
                    height=330,
                    color_discrete_sequence=["#2ECC71", "#38bdf8", "#f59e0b", "#ef4444", "#a855f7"],
                )
                fig3.update_traces(textinfo="percent+label")
                fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("Population pie chart skipped. Missing Name or population column.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="premium-card"><h4>Data Table</h4>', unsafe_allow_html=True)
        st.dataframe(
            temp.sort_values("Name"),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ---------- MAP ----------
def _get_auto_center_zoom(df: pd.DataFrame, lat_col: str, lon_col: str) -> tuple[float, float, int]:
    # ম্যাপের জন্য সেন্টার ও জুম স্বয়ংক্রিয়ভাবে নির্ধারণ করে
    if df.empty or lat_col not in df.columns or lon_col not in df.columns:
        return 23.685, 90.356, 6

    lat = _to_numeric(df[lat_col]).dropna()
    lon = _to_numeric(df[lon_col]).dropna()
    if lat.empty or lon.empty:
        return 23.685, 90.356, 6
    if len(lat) < 2 or len(lon) < 2:
        return float(lat.mean()), float(lon.mean()), 7

    lat_rng = float(lat.max() - lat.min())
    lon_rng = float(lon.max() - lon.min())
    zoom = 7 if lat_rng < 4 else 6
    if lat_rng < 1.5 or lon_rng < 1.5:
        zoom = 9
    return float(lat.mean()), float(lon.mean()), zoom


def render_bangladesh_plot(
    *,
    plot_df: pd.DataFrame,
    primary: str,
    secondary: str,
    lat_column: str,
    lon_column: str,
    zoom: int,
    title: str,
) -> None:
    # বাংলাদেশ ম্যাপ‑ভিত্তিক প্লট রেন্ডার করে
    secondary_l = secondary.lower()
    if any(word in secondary_l for word in ["poverty_rate", "underweight", "stunted"]):
        color_scale = "Reds"
    elif any(
        word in secondary_l
        for word in ["development_score", "literacy_rate", "school_attendance", "edu", "health_index"]
    ):
        color_scale = "RdYlGn"
    elif any(word in secondary_l for word in ["electricity_access", "tap_water_access", "flush_toilet_access"]):
        color_scale = "YlGn"
    elif any(word in secondary_l for word in ["population", "population_density"]):
        color_scale = "Blues"
    else:
        color_scale = "Viridis"

    center_lat, center_lon, auto_zoom = _get_auto_center_zoom(plot_df, lat_column, lon_column)
    hover_data = {
        "Name": True,
        primary: ":.0f",
        secondary: ":.2f",
    }
    if "population_density" in plot_df.columns:
        hover_data["population_density"] = ":.0f"

    fig = px.scatter_mapbox(
        plot_df,
        lat=lat_column,
        lon=lon_column,
        size=primary,
        color=secondary,
        size_max=20,
        hover_name="Name",
        hover_data=hover_data,
        opacity=0.85,
        zoom=auto_zoom,
        center=dict(lat=center_lat, lon=center_lon),
        height=680,
        mapbox_style="carto-positron",
        color_continuous_scale=color_scale,
        title=title,
    )
    fig.update_traces(
        marker=dict(
            opacity=0.8,
            sizemin=6,
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(
            title=secondary.replace("_", " ").title(),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------- PAGE ----------
render_country_page(
    country_name="Bangladesh",
    df=bangladesh_df,
    area_column="division",
    subarea_column="Name",
    lat_column="lat",
    lon_column="lon",
    overall_label="Overall Bangladesh",
    primary_options=size_params,
    secondary_options=color_params,
    render_plot_fn=render_bangladesh_plot,
    render_overall_post_map_fn=render_bangladesh_overall_analysis,
    render_overall_header_fn=_render_bangladesh_overall_header,
    render_kpi_fn=_render_bangladesh_kpis,
    navigate_on_subarea_select=True,
    subarea_page_path="pages/3_District.py",
    subarea_state_key="bd_selected_district",
    area_state_key="bd_selected_division",
    title_override="",
    header_description=None,
    map_section_title="Map Section",
    map_section_description="Interactive district bubble map for comparing indicators.",
)

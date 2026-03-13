import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard_utils import (
    inject_sidebar_style,
    load_bangladesh_data,
    load_bangladesh_gdp_data,
    load_bangladesh_literacy_data,
    render_country_page,
)

st.set_page_config(page_title="Bangladesh Analytics", page_icon="????", layout="wide")

inject_sidebar_style()
st.sidebar.title("📊 Data Explorer")
st.sidebar.markdown("Navigation")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Bangladesh.py", label="Bangladesh")
st.sidebar.page_link("pages/1_India.py", label="India")
st.sidebar.markdown("---")
st.sidebar.markdown("🌍 Regional Dashboard")


# বাংলাদেশ ডেটা লোড করা
bangladesh_df = load_bangladesh_data()
bangladesh_gdp_df = load_bangladesh_gdp_data()
bangladesh_literacy_df = load_bangladesh_literacy_data()

# বাংলাদেশ পেজে নির্দিষ্ট (ম্যানুয়াল) সাইজ/কালার প্যারামিটার ব্যবহার করা হচ্ছে।
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

# সংখ্যার মতো মানগুলোকে নিরাপদভাবে সংখ্যায় রূপান্তর করে।
def _to_numeric(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(cleaned, errors="coerce")

# বাংলাদেশ ডেটাসেটের জন্য কাস্টম KPI রো।
def _render_bangladesh_kpis(*, plot_df: pd.DataFrame) -> None:
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


# সামগ্রিক বাংলাদেশ ভিউয়ের জন্য হেডার/হিরো সেকশন।
def _render_bangladesh_overall_header(*, plot_df: pd.DataFrame) -> None:
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
                Bangladesh is a country in South Asia known for the Bengal Delta and the Sundarbans.
                This dashboard provides district-level analytics for population, education,
                poverty, infrastructure access, and development indicators.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )




# সামগ্রিক বাংলাদেশ ভিউয়ের জন্য ন্যাশনাল-লেভেল অ্যানালিটিক্স।
def render_bangladesh_overall_analysis(*, plot_df: pd.DataFrame) -> None:
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
    

    st.subheader("Economic Trend")
    k1, k2 = st.columns(2)

    with k1:
        st.markdown("#### Bangladesh GDP Trend (Line Graph)")
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
                    title="Bangladesh GDP Over Time",
                )
                fig_gdp.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_gdp, use_container_width=True)

    with k2:
        st.markdown("#### Bangladesh Inflation Rate (Line Graph)")
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
                    title="Bangladesh Inflation rate",
                )
                fig_inflation.update_traces(
                    mode="lines+markers",
                    line=dict(color="#f97316"),
                    marker=dict(color="#f97316"),
                    hovertemplate="Year: %{x}<br>Inflation Rate: %{y:.2f}%<extra></extra>",
                )
                fig_inflation.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_inflation, use_container_width=True)

    st.subheader("Education Insights")
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
                title="Bangladesh literacy rate",
            )
            fig_lit.update_traces(
                mode="lines+markers",
                hovertemplate="Year: %{x}<br>Literacy Rate: %{y:.2f}%<extra></extra>",
            )
            fig_lit.update_layout(margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_lit, use_container_width=True)
    else:
        st.info("Literacy trend skipped. Missing columns: Year, Literacy Rate(%).")

    col1, col2 = st.columns(2)

    with col1:
        top_lit = temp.nlargest(10, "literacy_rate")
        fig1 = px.bar(
            top_lit,
            x="Name",
            y="literacy_rate",
            title="Top 10 Literacy Districts",
            color="literacy_rate",
            color_continuous_scale="Greens",
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        low_lit = temp.nsmallest(10, "literacy_rate")
        fig2 = px.bar(
            low_lit,
            x="Name",
            y="literacy_rate",
            title="Lowest Literacy Districts",
            color="literacy_rate",
            color_continuous_scale="Reds",
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Population")
    top_pop = temp.nlargest(10, "population")
    fig3 = px.pie(
        top_pop,
        values="population",
        names="Name",
        title="Population Distribution (Top 10 Districts)",
        hole=0.4,
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Poverty Analysis")
    top_poor = temp.nlargest(10, "poverty_rate")
    fig4 = px.bar(
        top_poor,
        x="Name",
        y="poverty_rate",
        title="Top 10 Poorest Districts",
        color="poverty_rate",
        color_continuous_scale="Purples",
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Regional Comparison")
    st.markdown("### Division Averages (Literacy vs Poverty)")
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
        title="Division Averages: Literacy vs Poverty",
    )
    fig_division.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_division, use_container_width=True)

    st.subheader("Data Table")
    st.dataframe(
        temp.sort_values("Name"),
        use_container_width=True,
        hide_index=True,
    )

# বাংলাদেশ পেজের মূল চার্ট ও KPI রেন্ডার
# বাংলাদেশের জন্য কাস্টম বুদ্বুদ (বাবল) ম্যাপ স্টাইলিং।
def render_bangladesh_plot(
    *,
    plot_df,
    primary: str,
    secondary: str,
    lat_column: str,
    lon_column: str,
    zoom: int,
    title: str,
) -> None:
    # সেকেন্ডারি প্যারামিটার দেখে কালার স্কেল নির্বাচন
    secondary_l = secondary.lower()
    if any(word in secondary_l for word in ["poverty_rate", "underweight", "stunted"]):
        color_scale = "Reds"
    elif any(word in secondary_l for word in ["development_score", "literacy_rate", "school_attendance", "edu","health_index"]):
        color_scale = "RdYlGn"
    elif any(word in secondary_l for word in ["electricity_access", "tap_water_access", "flush_toilet_access"]):
        color_scale = "YlGn"
    elif any(word in secondary_l for word in ["population", "population_density"]):
        color_scale = "Blues"
    else:
        color_scale = "Viridis"

    fig = px.scatter_mapbox(
        plot_df,
        lat=lat_column,
        lon=lon_column,
        size=primary,
        color=secondary,
        size_max=20,
        hover_name="Name",
        zoom=zoom,
        height=650,
        mapbox_style="open-street-map",
        color_continuous_scale=color_scale,
        title=title,
    )
    fig.update_traces(
        marker=dict(
            opacity=0.8,
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(
            title=secondary.replace("_", " ").title(),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


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
    navigate_on_subarea_select=True,
    subarea_page_path="pages/3_District.py",
    subarea_state_key="bd_selected_district",
    area_state_key="bd_selected_division",
    title_override="",
    header_description=None,
    map_section_title="Map Section",
    map_section_description="Interactive district bubble map for comparing indicators.",
    render_kpi_fn=_render_bangladesh_kpis,
)

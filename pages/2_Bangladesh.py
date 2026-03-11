import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard_utils import inject_sidebar_style, load_bangladesh_data, render_country_page

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

def _to_numeric(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


def render_bangladesh_overall_analysis(*, plot_df: pd.DataFrame) -> None:
    required_cols = {"Name", "division", "literacy_rate", "population", "poverty_rate"}
    missing = sorted(required_cols - set(plot_df.columns))
    if missing:
        st.info(f"National analytics skipped. Missing columns: {', '.join(missing)}.")
        return

    temp = plot_df.copy()
    temp["literacy_rate"] = _to_numeric(temp["literacy_rate"])
    temp["population"] = _to_numeric(temp["population"])
    temp["poverty_rate"] = _to_numeric(temp["poverty_rate"])

    st.markdown("---")
    st.header("Deep Dive: National Analytics")

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

    col3, col4 = st.columns(2)

    with col3:
        top_pop = temp.nlargest(10, "population")
        fig3 = px.pie(
            top_pop,
            values="population",
            names="Name",
            title="Population Distribution (Top 10 Districts)",
            hole=0.4,
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
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

    st.markdown("### Division Averages (Literacy vs Poverty)")
    division_summary = (
        temp.groupby("division")[["literacy_rate", "poverty_rate"]]
        .mean()
        .reset_index()
        .sort_values("division")
    )
    st.dataframe(
        division_summary,
        use_container_width=True,
        hide_index=True,
    )

# বাংলাদেশ পেজের মূল চার্ট ও KPI রেন্ডার
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
    render_overall_pre_map_fn=render_bangladesh_overall_analysis,
    navigate_on_subarea_select=True,
    subarea_page_path="pages/3_District.py",
    subarea_state_key="bd_selected_district",
    area_state_key="bd_selected_division",
)

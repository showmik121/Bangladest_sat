import plotly.express as px
import streamlit as st

from dashboard_utils import load_bangladesh_data, render_country_page

st.set_page_config(page_title="Bangladesh Analytics", page_icon="????", layout="wide")

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
)

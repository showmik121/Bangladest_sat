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
render_country_page(
    country_name="Bangladesh",
    df=bangladesh_df,
    area_column="division",
    lat_column="lat",
    lon_column="lon",
    overall_label="Overall Bangladesh",
    primary_options=size_params,
    secondary_options=color_params,
)

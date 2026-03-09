import streamlit as st

from dashboard_utils import load_india_data, render_country_page

st.set_page_config(page_title="India Analytics", page_icon="????", layout="wide")

india_df = load_india_data()

render_country_page(
    country_name="India",
    df=india_df,
    area_column="State",
    lat_column="Latitude",
    lon_column="Longitude",
    overall_label="Overall India",
)

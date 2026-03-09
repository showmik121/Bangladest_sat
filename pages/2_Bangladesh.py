import streamlit as st

from dashboard_utils import load_bangladesh_data, render_country_page

st.set_page_config(page_title="Bangladesh Analytics", page_icon="????", layout="wide")

bangladesh_df = load_bangladesh_data()

render_country_page(
    country_name="Bangladesh",
    df=bangladesh_df,
    area_column="division",
    lat_column="lat",
    lon_column="lon",
    overall_label="Overall Bangladesh",
)

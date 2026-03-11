import streamlit as st

from dashboard_utils import inject_sidebar_style, load_india_data, render_country_page

st.set_page_config(page_title="India Analytics", page_icon="????", layout="wide")

inject_sidebar_style()
st.sidebar.title("📊 Data Explorer")
st.sidebar.markdown("Navigation")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Bangladesh.py", label="Bangladesh")
st.sidebar.page_link("pages/1_India.py", label="India")
st.sidebar.markdown("---")
st.sidebar.markdown("🌍 Regional Dashboard")

india_df = load_india_data()

render_country_page(
    country_name="India",
    df=india_df,
    area_column="State",
    lat_column="Latitude",
    lon_column="Longitude",
    overall_label="Overall India",
)

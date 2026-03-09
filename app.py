import streamlit as st

from dashboard_utils import load_bangladesh_data, load_india_data

st.set_page_config(page_title="Country Dashboard", page_icon="??", layout="wide")

st.title("Country Data Dashboard")
st.caption("Use the left sidebar to open India or Bangladesh specific analysis pages.")

india_df = load_india_data()
bd_df = load_bangladesh_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("India Snapshot")
    st.metric("Rows", f"{len(india_df):,}")
    st.metric("States", f"{india_df['State'].nunique():,}" if "State" in india_df.columns else "N/A")

with col2:
    st.subheader("Bangladesh Snapshot")
    st.metric("Rows", f"{len(bd_df):,}")
    st.metric("Divisions", f"{bd_df['division'].nunique():,}" if "division" in bd_df.columns else "N/A")

st.info("Open pages from sidebar: India or Bangladesh.")

import streamlit as st

from dashboard_utils import inject_sidebar_style, load_bangladesh_data, load_india_data

st.set_page_config(page_title="Country Dashboard", page_icon="??", layout="wide")

inject_sidebar_style()
st.sidebar.title("📊 Data Explorer")
st.sidebar.markdown("Navigation")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Bangladesh.py", label="Bangladesh")
st.sidebar.page_link("pages/1_India.py", label="India")
st.sidebar.markdown("---")

st.title("Country Data Dashboard")
st.caption("Use the left sidebar to open India or Bangladesh specific analysis pages.")

st.subheader("Quick Navigation")
selected_country = st.sidebar.selectbox("Go to country page", ["Select", "Bangladesh", "India"])
if selected_country == "Bangladesh":
    st.switch_page("pages/2_Bangladesh.py")
elif selected_country == "India":
    st.switch_page("pages/1_India.py")

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

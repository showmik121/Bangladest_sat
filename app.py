import streamlit as st
from dashboard_utils import inject_sidebar_style

st.set_page_config(
    page_title="Regional Development Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_sidebar_style()

# ---------- Sidebar ----------
st.sidebar.title("📊 Data Explorer")
st.sidebar.markdown("Navigation")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Bangladesh.py", label="Bangladesh")
st.sidebar.page_link("pages/1_India.py", label="India")
st.sidebar.markdown("---")

# ---------- Small Styling ----------
st.markdown("""
<style>
h1 { color: #1e40af; }
.stButton > button {
    width: 100%;
    font-weight: 600;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("🌍 Regional Development Intelligence Dashboard")

st.markdown("""
Explore **socioeconomic indicators** across regions and districts.  
Compare population, literacy, poverty, infrastructure, health, education and more.
""")

st.divider()

# ---------- Dashboard Selection ----------
st.subheader("🌏 Explore Dashboards")

with st.container(border=True):

    c1, c2 = st.columns(2, gap="large", vertical_alignment="center")

    with c1:
        st.markdown("### 🇧🇩 Bangladesh")
        st.write("64 districts — granular view")
        st.caption("District rankings • Maps • Time trends 2011–2022/23")

        if st.button("Open Bangladesh Dashboard", type="primary", use_container_width=True):
            st.switch_page("pages/2_Bangladesh.py")

    with c2:
        st.markdown("### 🇮🇳 India")
        st.write("36 states & union territories")
        st.caption("State comparisons • Regional disparities • SDG alignment")

        if st.button("Open India Dashboard", type="primary", use_container_width=True):
            st.switch_page("pages/1_India.py")

st.divider()

# ---------- Coverage Stats ----------
st.subheader("📈 Current Coverage")

colA, colB, colC, colD = st.columns(4)

colA.metric("Districts (BD)", "64 / 64")
colB.metric("States + UTs (IN)", "36 / 36")
colC.metric("Core Indicators", "22")
colD.metric("Last Major Update", "2024–25")

st.caption("Sources: BBS, MoHFW BD, NITI Aayog, MoSPI India, Census, NFHS, SRS, DISE, etc.")

st.divider()

# ---------- About ----------
with st.expander("📊 About This Project", expanded=False):

    st.markdown("""
**Purpose**  
Make complex regional development data accessible and comparable through interactive visualizations.

**Main features**
- Choropleth & bubble maps
- Parallel coordinates & radar charts for multi-dimensional comparison
- Time-series trends & year-on-year change
- Custom rankings & inequality measures (Gini, Theil, HDI-like composite)
- Downloadable filtered tables

**Currently available**
- Bangladesh district profiles
- India state & UT comparisons

Built with **Streamlit, Altair/Pydeck/Plotly, Pandas & GeoPandas**.
""")

st.caption("Regional Development Intelligence Dashboard • Last updated March 2026")
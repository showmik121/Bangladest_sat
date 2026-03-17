import streamlit as st

from dashboard_utils import inject_sidebar_style, render_top_navbar

st.set_page_config(page_title="About • South Asia Data Observatory", page_icon="ℹ️", layout="wide")

inject_sidebar_style(hide_sidebar=True)
render_top_navbar(active="About Us")

st.markdown(
    """
<div class="card">
  <div class="card-title">About This Project</div>
  <div class="card-sub">South Asia Data Observatory</div>
  <p>
    This dashboard brings together regional indicators for Bangladesh and India,
    making it easy to explore population, health, education, and economic trends
    through interactive maps and visual analytics.
  </p>
  <ul>
    <li>Curated national and sub‑national datasets</li>
    <li>Interactive map exploration with KPI snapshots</li>
    <li>Story‑ready visuals for policy and research</li>
  </ul>
</div>
    """,
    unsafe_allow_html=True,
)

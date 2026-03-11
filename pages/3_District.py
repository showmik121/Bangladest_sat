import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard_utils import inject_sidebar_style, load_bangladesh_data

st.set_page_config(page_title="District Development Dashboard", page_icon="????", layout="wide")

inject_sidebar_style()
st.sidebar.title("📊 Data Explorer")
st.sidebar.markdown("Navigation")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Bangladesh.py", label="Bangladesh")
st.sidebar.page_link("pages/1_India.py", label="India")
st.sidebar.markdown("---")
st.sidebar.markdown("🌍 Regional Dashboard")


bangladesh_df = load_bangladesh_data()

def _to_numeric(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


def _metric_value(row: pd.Series, column: str, default: str = "N/A") -> str:
    if column not in row:
        return default
    value = row[column]
    if pd.isna(value):
        return default
    if isinstance(value, (int, float)):
        if column == "population":
            return f"{int(value):,}"
        return f"{value:.2f}"
    return str(value)


st.title("District Development Dashboard")

st.markdown("---")

divisions = sorted(bangladesh_df["division"].dropna().unique().tolist())
default_division = st.session_state.get("bd_selected_division")
if default_division not in divisions:
    default_division = divisions[0] if divisions else None

selected_division = st.sidebar.selectbox("Division", divisions, index=divisions.index(default_division) if default_division else 0)

districts = sorted(
    bangladesh_df[bangladesh_df["division"] == selected_division]["Name"].dropna().unique().tolist()
)
district_options = ["All Districts"] + districts
default_district = st.session_state.get("bd_selected_district")
if default_district not in district_options:
    default_district = "All Districts"
selected_district = st.sidebar.selectbox(
    "District",
    district_options,
    index=district_options.index(default_district),
)

bubble_size_options = ["population", "population_density", "working_age_pop", "area_km2"]
bubble_color_options = [
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
size_choice = st.sidebar.selectbox("Bubble Size", bubble_size_options)
color_choice = st.sidebar.selectbox("Bubble Color", bubble_color_options)

st.sidebar.markdown("---")
st.sidebar.caption("Use filters to explore district-level insights.")

filtered_df = bangladesh_df[bangladesh_df["division"] == selected_division].copy()
if selected_district != "All Districts":
    filtered_df = filtered_df[filtered_df["Name"] == selected_district].copy()

if filtered_df.empty:
    st.error("No data found for the selected filters.")
    st.stop()

district_row = filtered_df.iloc[0]
division_name = selected_division or district_row.get("division", "Unknown")

st.markdown("---")
st.subheader("KPI Row")

for column in ["literacy_rate", "poverty_rate", "development_score", "population"]:
    if column in filtered_df.columns:
        filtered_df[column] = _to_numeric(filtered_df[column])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Population", _metric_value(district_row, "population"))
with col2:
    st.metric("Literacy", _metric_value(district_row, "literacy_rate"))
with col3:
    st.metric("Poverty", _metric_value(district_row, "poverty_rate"))
with col4:
    st.metric("Development Score", _metric_value(district_row, "development_score"))

st.markdown("---")
st.subheader("Interactive District Map")

map_df = bangladesh_df.copy()
for column in [
    "population",
    "poverty_rate",
    "literacy_rate",
    "development_score",
    "population_density",
    "working_age_pop",
    "area_km2",
    "electricity_access",
    "tap_water_access",
    "flush_toilet_access",
    "health_index",
    "lat",
    "lon",
]:
    if column in map_df.columns:
        map_df[column] = _to_numeric(map_df[column])

center_lat = filtered_df["lat"].iloc[0] if "lat" in filtered_df.columns else None
center_lon = filtered_df["lon"].iloc[0] if "lon" in filtered_df.columns else None

map_fig = px.scatter_mapbox(
    map_df,
    lat="lat",
    lon="lon",
    size=size_choice if size_choice in map_df.columns else None,
    color=color_choice if color_choice in map_df.columns else None,
    hover_name="Name",
    zoom=7 if pd.notna(center_lat) else 4,
    height=520,
    mapbox_style="open-street-map",
    title=f"{selected_district} (Division: {division_name})",
)

if pd.notna(center_lat) and pd.notna(center_lon):
    map_fig.update_layout(mapbox=dict(center=dict(lat=center_lat, lon=center_lon)))

st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")
st.subheader("District Profile")

profile_cols = st.columns(2)
with profile_cols[0]:
    if "development_score" in filtered_df.columns and pd.notna(filtered_df["development_score"].iloc[0]):
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=float(filtered_df["development_score"].iloc[0]),
                title={"text": "Development Score"},
                gauge={"axis": {"range": [0, 100]}},
            )
        )
        fig.update_layout(height=260, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Development score not available for this district.")

with profile_cols[1]:
    profile_metrics = ["literacy_rate", "poverty_rate", "health_index", "school_attendance"]
    available = [m for m in profile_metrics if m in filtered_df.columns]
    if available:
        profile_view = filtered_df[available].copy()
        for col in available:
            profile_view[col] = _to_numeric(profile_view[col])
        st.dataframe(profile_view, use_container_width=True, hide_index=True)
    else:
        st.info("No additional indicators available.")

st.markdown("---")
st.subheader("Comparison Analysis")

comparison_cols = ["literacy_rate", "poverty_rate", "development_score"]
available_comp = [c for c in comparison_cols if c in bangladesh_df.columns]
if available_comp:
    comparison_df = bangladesh_df.copy()
    for col in available_comp:
        comparison_df[col] = _to_numeric(comparison_df[col])

    division_avg = comparison_df[comparison_df["division"] == division_name][available_comp].mean()
    national_avg = comparison_df[available_comp].mean()
    district_vals = comparison_df[comparison_df["Name"] == selected_district][available_comp].iloc[0]

    compare_table = pd.DataFrame(
        {
            "District": district_vals,
            "Division": division_avg,
            "National": national_avg,
        }
    ).reset_index().rename(columns={"index": "Metric"})

    compare_fig = px.bar(
        compare_table.melt(id_vars="Metric", var_name="Scope", value_name="Value"),
        x="Metric",
        y="Value",
        color="Scope",
        barmode="group",
        title="District vs Division vs National",
    )
    st.plotly_chart(compare_fig, use_container_width=True)
else:
    st.info("Not enough metrics available for comparison.")

st.markdown("---")
st.subheader("Top Districts")

if "development_score" in bangladesh_df.columns:
    top_metric = "development_score"
elif "literacy_rate" in bangladesh_df.columns:
    top_metric = "literacy_rate"
else:
    top_metric = None

if top_metric:
    top_df = bangladesh_df.copy()
    top_df[top_metric] = _to_numeric(top_df[top_metric])
    top_df = top_df.nlargest(10, top_metric)
    top_fig = px.bar(
        top_df,
        x="Name",
        y=top_metric,
        title=f"Top 10 Districts by {top_metric.replace('_', ' ').title()}",
        color=top_metric,
        color_continuous_scale="Blues",
    )
    st.plotly_chart(top_fig, use_container_width=True)
else:
    st.info("No metric available for top district ranking.")

st.markdown("---")
st.subheader("Regional Insights")

if "division" in bangladesh_df.columns and division_name:
    regional_df = bangladesh_df[bangladesh_df["division"] == division_name].copy()
    if "literacy_rate" in regional_df.columns:
        regional_df["literacy_rate"] = _to_numeric(regional_df["literacy_rate"])
        regional_df = regional_df.nlargest(8, "literacy_rate")
        regional_fig = px.bar(
            regional_df,
            x="Name",
            y="literacy_rate",
            title=f"Top Literacy Districts in {division_name}",
            color="literacy_rate",
            color_continuous_scale="Greens",
        )
        st.plotly_chart(regional_fig, use_container_width=True)
    else:
        st.info("Literacy data not available for regional insights.")
else:
    st.info("Division information not available for regional insights.")

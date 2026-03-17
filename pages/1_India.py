import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard_utils import inject_sidebar_style, load_india_data, render_country_page

st.set_page_config(page_title="India Analytics", page_icon="🇮🇳", layout="wide")

inject_sidebar_style()
st.sidebar.title("📊 Data Explorer")
st.sidebar.markdown("Navigation")
st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/2_Bangladesh.py", label="Bangladesh")
st.sidebar.page_link("pages/1_India.py", label="India")
st.sidebar.markdown("---")
st.sidebar.markdown("🌍 Regional Dashboard")

india_df = load_india_data()

size_params = [
    "Population",
    "Households_with_Internet",
    "Housholds_with_Electric_Lighting",
    "LPG_or_PNG_Households",
]

color_params = [
    "literacy_rate",
    "sex_ratio",
    "Graduate_rate",
]

# ---------- MAP ----------
def _get_auto_center_zoom(df: pd.DataFrame, lat_col: str, lon_col: str) -> tuple[float, float, int]:
    if df.empty or lat_col not in df.columns or lon_col not in df.columns:
        return 22.8, 79.0, 4

    lat = pd.to_numeric(df[lat_col], errors="coerce").dropna()
    lon = pd.to_numeric(df[lon_col], errors="coerce").dropna()
    if lat.empty or lon.empty:
        return 22.8, 79.0, 4
    if len(lat) < 2 or len(lon) < 2:
        return float(lat.mean()), float(lon.mean()), 5

    lat_rng = float(lat.max() - lat.min())
    lon_rng = float(lon.max() - lon.min())
    zoom = 5 if lat_rng < 8 else 4
    if lat_rng < 4 or lon_rng < 4:
        zoom = 6
    return float(lat.mean()), float(lon.mean()), zoom


def render_india_plot(
    *,
    plot_df: pd.DataFrame,
    primary: str,
    secondary: str,
    lat_column: str,
    lon_column: str,
    zoom: int,
    title: str,
) -> None:
    secondary_l = secondary.lower()
    if "literacy" in secondary_l or "graduate" in secondary_l:
        color_scale = "RdYlGn"
    elif "sex_ratio" in secondary_l:
        color_scale = "Blues"
    elif "population" in secondary_l or "household" in secondary_l:
        color_scale = "YlGnBu"
    else:
        color_scale = "Viridis"

    center_lat, center_lon, auto_zoom = _get_auto_center_zoom(plot_df, lat_column, lon_column)
    hover_name = "District" if "District" in plot_df.columns else "State"
    hover_data = {
        primary: ":.0f",
        secondary: ":.2f",
    }

    fig = px.scatter_mapbox(
        plot_df,
        lat=lat_column,
        lon=lon_column,
        size=primary,
        color=secondary,
        size_max=20,
        hover_name=hover_name,
        hover_data=hover_data,
        opacity=0.85,
        zoom=auto_zoom,
        center=dict(lat=center_lat, lon=center_lon),
        height=680,
        mapbox_style="carto-positron",
        color_continuous_scale=color_scale,
        title=title,
    )
    fig.update_traces(marker=dict(opacity=0.8, sizemin=6))
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(
            title=secondary.replace("_", " ").title(),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


# সামগ্রিক ভারতের জন্য হেডার/হিরো সেকশন।
def _render_india_overall_header(*, plot_df) -> None:
    st.markdown(
        """
        <style>
        .country-hero {
            background: #eaf3f1;
            padding: 32px;
            border-radius: 16px;
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 32px;
            align-items: start;
            margin-bottom: 25px;
        }
        .country-crumb {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .country-title {
            font-size: 36px;
            font-weight: 700;
            color: #0f172a;
        }
        .country-flag {
            width: 120px;
            height: 80px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 14px rgba(0,0,0,0.12);
        }
        .country-meta {
            font-size: 15px;
            color: #334155;
            line-height: 1.7;
        }
        .country-desc {
            font-size: 16px;
            color: #334155;
            line-height: 1.7;
        }
        [data-testid="stMetric"] {
            background: white;
            padding: 16px;
            border-radius: 14px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
        [data-testid="stMetricValue"] {
            font-size: 30px;
            font-weight: 700;
        }
        @media (prefers-color-scheme: dark) {
            .country-hero {
                background: #0b1220;
                border: 1px solid rgba(148, 163, 184, 0.18);
            }
            .country-crumb { color: #94a3b8; }
            .country-title { color: #e2e8f0; }
            .country-meta { color: #cbd5f5; }
            .country-desc { color: #cbd5f5; }
            .country-meta b { color: #f1f5f9; }
            [data-testid="stMetric"] {
                background: #0f172a;
                box-shadow: 0 6px 20px rgba(0,0,0,0.45);
                border: 1px solid rgba(148, 163, 184, 0.18);
            }
            [data-testid="stMetricValue"] { color: #f8fafc; }
            [data-testid="stMetricLabel"] { color: #cbd5f5; }
        }
        @media (max-width: 900px) {
            .country-hero { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    flag_svg = """
    <svg viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="26.67" y="0" fill="#ff9933"/>
        <rect width="120" height="26.67" y="26.67" fill="#ffffff"/>
        <rect width="120" height="26.67" y="53.33" fill="#138808"/>
        <circle cx="60" cy="40" r="10" fill="#000088"/>
    </svg>
    """

    st.markdown(
        f"""
        <div class="country-hero">
            <div>
                <div class="country-crumb">Countries &nbsp;›&nbsp; India</div>
                <div style="display:flex;align-items:center;gap:16px;margin-bottom:12px;">
                    <div class="country-flag">{flag_svg}</div>
                    <div class="country-title">India</div>
                </div>
                <div class="country-meta">
                    <b>Capital:</b> New Delhi<br/>
                    <b>Continent:</b> Asia<br/>
                    <b>Region:</b> Southern Asia<br/>
                    <b>Largest Cities:</b> Delhi, Mumbai, Bengaluru<br/>
                    <b>Abbreviation:</b> IND
                </div>
            </div>
            <div class="country-desc">
                India is a diverse South Asian country with rapidly growing urban centers and
                varied regional development. This dashboard compares states and union territories
                across population, literacy, poverty, and infrastructure indicators.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

render_country_page(
    country_name="India",
    df=india_df,
    area_column="State",
    lat_column="Latitude",
    lon_column="Longitude",
    overall_label="Overall India",
    primary_options=size_params,
    secondary_options=color_params,
    render_plot_fn=render_india_plot,
    render_overall_header_fn=_render_india_overall_header,
    title_override="",
    header_description=None,
    map_section_title="Map Section",
    map_section_description="Interactive state bubble map for comparing indicators.",
)

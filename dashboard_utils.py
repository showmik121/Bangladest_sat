from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

INDIA_FILE = "india"
# BANGLADESH_FILE = "bangladesh_sat.csv"
# BANGLADESH_FILE = "Up_Ban"
BANGLADESH_FILE = "final_ban"
BANGLADESH_GDP_FILE = "Gdp"
BANGLADESH_LITERACY_RATE="litracy"


# পরিষ্কার কাস্টম ন্যাভের জন্য Streamlit-এর ডিফল্ট সাইডবার ন্যাভ লুকানো।
def inject_sidebar_style() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def load_country_data(file_path: str, name: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        st.session_state[f"{name}_data_loaded"] = True
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.stop()
    except Exception as exc:
        st.error(f"Error loading {name} data: {exc}")
        st.stop()


# ইন্ডিয়া ডেটাসেটের জন্য ক্যাশড লোডার।
@st.cache_data
def load_india_data() -> pd.DataFrame:
    return load_country_data(INDIA_FILE, "india")


# বাংলাদেশ জেলা ডেটাসেটের জন্য ক্যাশড লোডার।
@st.cache_data
def load_bangladesh_data() -> pd.DataFrame:
    return load_country_data(BANGLADESH_FILE, "bangladesh")


# বাংলাদেশ GDP টাইম-সিরিজ ডেটাসেটের জন্য ক্যাশড লোডার।
@st.cache_data
def load_bangladesh_gdp_data() -> pd.DataFrame:
    return load_country_data(BANGLADESH_GDP_FILE, "bd_gdp")


# Bangladesh literacy time series loader.
@st.cache_data
def load_bangladesh_literacy_data() -> pd.DataFrame:
    return load_country_data(BANGLADESH_LITERACY_RATE, "bd_literacy")

# সংখ্যার মতো স্ট্রিংকে সংখ্যায় রূপান্তর করে (কমা, স্পেসসহ)।
def _coerce_numeric(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return series
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


# প্রথম ম্যাচ হওয়া কলাম থেকে মোট যোগফল বের করে, না পেলে ডিফল্ট।
def _safe_metric_value(df: pd.DataFrame, column_candidates: list[str], default: float = 0.0) -> float:
    for column in column_candidates:
        if column in df.columns:
            series = _coerce_numeric(df[column])
            return float(series.fillna(0).sum())
    return float(default)


# প্রথম ম্যাচ হওয়া কলাম বা সব নিউমেরিক কলাম থেকে গড় বের করে।
def _safe_mean_value(df: pd.DataFrame, column_candidates: list[str], fallback_to_numeric: bool = True) -> float:
    for column in column_candidates:
        if column in df.columns:
            series = _coerce_numeric(df[column])
            return float(series.mean(skipna=True))

    if fallback_to_numeric:
        numeric_df = df.select_dtypes(include=np.number)
        if not numeric_df.empty:
            return float(numeric_df.mean(numeric_only=True).mean())

    return 0.0


def render_country_page(
    *,
    country_name: str,
    df: pd.DataFrame,
    area_column: str,
    lat_column: str,
    lon_column: str,
    overall_label: str,
    subarea_column: str | None = None,
    primary_options: list[str] | None = None,
    secondary_options: list[str] | None = None,
    render_plot_fn: Callable[..., None] | None = None,
    render_overall_pre_map_fn: Callable[..., None] | None = None,
    render_overall_post_map_fn: Callable[..., None] | None = None,
    render_overall_header_fn: Callable[..., None] | None = None,
    navigate_on_subarea_select: bool = False,
    subarea_page_path: str | None = None,
    subarea_state_key: str | None = None,
    area_state_key: str | None = None,
    title_override: str | None = None,
    header_description: str | None = None,
    render_kpi_fn: Callable[..., None] | None = None,
    map_section_title: str | None = None,
    map_section_description: str | None = None,
) -> None:
    title_text = title_override if title_override is not None else f"{country_name} Analytics"
    if title_text:
        st.title(title_text)
    if header_description:
        st.markdown(header_description)

    locations = sorted(df[area_column].dropna().unique().tolist())
    locations.insert(0, overall_label)

    selected_location = st.sidebar.selectbox("Select Area", locations)

    numeric_cols = [
        c for c in df.select_dtypes(include=np.number).columns.tolist() if c not in {lat_column, lon_column}
    ]

    if primary_options is not None:
        primary_candidates = [c for c in primary_options if c in df.columns]
    else:
        primary_candidates = numeric_cols

    if secondary_options is not None:
        secondary_candidates = [c for c in secondary_options if c in df.columns]
    else:
        secondary_candidates = numeric_cols

    if not primary_candidates or not secondary_candidates:
        st.error("No valid columns available for plotting.")
        return

    primary = st.sidebar.selectbox("Primary Parameter (Size)", primary_candidates)
    secondary = st.sidebar.selectbox("Secondary Parameter (Color)", secondary_candidates)

    if selected_location == overall_label:
        plot_df = df
        zoom = 4 if country_name == "Bangladesh" else 3
        display_location = overall_label
    else:
        division_df = df[df[area_column] == selected_location]
        zoom = 6
        if subarea_column and subarea_column in df.columns:
            districts_by_division = df.groupby(area_column)[subarea_column].apply(list).to_dict()
            if selected_location in districts_by_division:
                district_list = sorted(
                    pd.Series(districts_by_division[selected_location]).dropna().unique().tolist()
                )
                overall_subarea_label = f"Overall {selected_location}"
                district_list.insert(0, overall_subarea_label)
                selected_subarea = st.sidebar.selectbox(
                    f"Districts in {selected_location}",
                    district_list,
                )
                if selected_subarea == overall_subarea_label:
                    plot_df = division_df
                    display_location = selected_subarea
                else:
                    plot_df = df[df[subarea_column] == selected_subarea]
                    zoom = 8
                    display_location = selected_subarea
                    if subarea_state_key is None:
                        safe_name = country_name.lower().replace(" ", "_")
                        subarea_state_key = f"{safe_name}_selected_subarea"
                    if area_state_key is None:
                        safe_name = country_name.lower().replace(" ", "_")
                        area_state_key = f"{safe_name}_selected_area"
                    st.session_state[subarea_state_key] = selected_subarea
                    st.session_state[area_state_key] = selected_location
                    if navigate_on_subarea_select and subarea_page_path:
                        st.switch_page(subarea_page_path)
            else:
                plot_df = division_df
                display_location = selected_location
        else:
            plot_df = division_df
            display_location = selected_location

    if selected_location == overall_label and render_overall_header_fn is not None:
        render_overall_header_fn(plot_df=plot_df)

    if render_kpi_fn is not None:
        render_kpi_fn(plot_df=plot_df)
    

    st.markdown("---")
    
    st.header("Deep Dive: National Analytics")
    st.markdown("---")

    if selected_location == overall_label and render_overall_pre_map_fn is not None:
        render_overall_pre_map_fn(plot_df=plot_df)

    if map_section_title:
        st.header(map_section_title)
        if map_section_description:
            st.caption(map_section_description)

    st.subheader(f"{primary} vs {secondary} ({display_location})")

    plot_df = plot_df.copy()
    plot_df[primary] = _coerce_numeric(plot_df[primary])
    plot_df[secondary] = _coerce_numeric(plot_df[secondary])
    plot_df[lat_column] = _coerce_numeric(plot_df[lat_column])
    plot_df[lon_column] = _coerce_numeric(plot_df[lon_column])

    if render_plot_fn is not None:
        render_plot_fn(
            plot_df=plot_df,
            primary=primary,
            secondary=secondary,
            lat_column=lat_column,
            lon_column=lon_column,
            zoom=zoom,
            title=f"{country_name}: {display_location}",
        )
    else:
        fig = px.scatter_mapbox(
            plot_df,
            lat=lat_column,
            lon=lon_column,
            size=primary,
            color=secondary,
            size_max=16,
            zoom=zoom,
            height=650,
            mapbox_style="open-street-map",
            title=f"{country_name}: {display_location}",
        )
        st.plotly_chart(fig, use_container_width=True)

    if selected_location == overall_label and render_overall_post_map_fn is not None:
        render_overall_post_map_fn(plot_df=plot_df)

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

INDIA_FILE = "india"
# BANGLADESH_FILE = "bangladesh_sat.csv"

# BANGLADESH_FILE="Up_Ban"

BANGLADESH_FILE="final_ban"

@st.cache_data
def load_india_data() -> pd.DataFrame:
    return pd.read_csv(INDIA_FILE)


@st.cache_data
def load_bangladesh_data() -> pd.DataFrame:
    return pd.read_csv(BANGLADESH_FILE)


def _coerce_numeric(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return series
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


def _safe_metric_value(df: pd.DataFrame, column_candidates: list[str], default: float = 0.0) -> float:
    for column in column_candidates:
        if column in df.columns:
            series = _coerce_numeric(df[column])
            return float(series.fillna(0).sum())
    return float(default)


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
) -> None:
    st.title(f"{country_name} Analytics")

    locations = sorted(df[area_column].dropna().unique().tolist())
    locations.insert(0, overall_label)

    st.sidebar.header(f"{country_name} Filters")
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

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        total_pop = _safe_metric_value(df, ["Population", "population"])
        st.metric("Total Population", f"{int(total_pop):,}")

    with kpi2:
        literacy_avg = _safe_mean_value(df, ["literacy_rate"])
        st.metric("Avg Literacy Rate", f"{literacy_avg:.2f}%")

    with kpi3:
        st.metric("Total Records", f"{len(df):,}")

    st.markdown("---")

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
            else:
                plot_df = division_df
                display_location = selected_location
        else:
            plot_df = division_df
            display_location = selected_location

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

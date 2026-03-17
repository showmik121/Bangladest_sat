from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

INDIA_FILE = "india.csv"
# BANGLADESH_FILE = "bangladesh_sat.csv"
# BANGLADESH_FILE = "Up_Ban"
BANGLADESH_FILE = "final_ban.csv"
BANGLADESH_GDP_FILE = "Gdp.csv"
BANGLADESH_LITERACY_RATE="litracy.csv"
DIVISION_POPULATION="population.csv"
INCOME_SATUS="income.csv"

# পরিষ্কার কাস্টম ন্যাভের জন্য Streamlit-এর ডিফল্ট সাইডবার ন্যাভ লুকানো।
def inject_sidebar_style(*, hide_sidebar: bool = False) -> None:
    sidebar_css = """
        :root {
            --sidebar-width: 260px;
            --sidebar-gap: 20px;
        }
        [data-testid="stSidebarNav"] { display: none; }
        /* SIDEBAR (NOT FIXED) */
        section[data-testid="stSidebar"] {
            position: relative;
            top: 0;
            left: 0;
            width: var(--sidebar-width);
            height: auto;
            background: rgba(15, 23, 42, 0.72);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-radius: 18px;
            border: 1px solid rgba(148, 163, 184, 0.25);
            box-shadow: 0 20px 50px rgba(2, 6, 23, 0.35);
            padding: 10px;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        section[data-testid="stSidebar"] > div:first-child {
            background: transparent;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
        }
        .block-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        section[data-testid="stSidebar"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 60px rgba(2, 6, 23, 0.45);
        }
        section[data-testid="stSidebar"] .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        section[data-testid="stSidebar"] h1 {
            font-size: 18px;
            margin-bottom: 10px;
        }
        /* Sidebar text tones for glass background */
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a {
            color: #e2e8f0;
        }
        section[data-testid="stSidebar"] .stMarkdown hr {
            border-color: rgba(148, 163, 184, 0.25);
        }
    """
    hide_css = """
        section[data-testid="stSidebar"] { display: none; }
        [data-testid="stAppViewContainer"] { margin-left: 0 !important; }
        .block-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    """
    css = hide_css if hide_sidebar else sidebar_css
    st.markdown(
        f"""
        <style>
        {css}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_navbar(*, active: str = "Home") -> None:
    st.markdown(
        """
        <style>
        .top-nav {
            position: sticky;
            top: 0;
            z-index: 999;
            background: rgba(11, 18, 32, 0.9);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(148, 163, 184, 0.2);
            padding: 10px 16px;
            margin-bottom: 14px;
            border-radius: 16px;
            box-shadow: 0 12px 28px rgba(2, 6, 23, 0.35);
        }
        .top-nav-title {
            font-weight: 700;
            letter-spacing: 0.3px;
            color: #e2e8f0;
            font-size: 16px;
        }
        .top-nav-link button {
            width: 100%;
            border-radius: 10px;
            font-weight: 600;
            background: rgba(148, 163, 184, 0.12);
            color: #e2e8f0;
            border: 1px solid rgba(148, 163, 184, 0.25);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="top-nav">', unsafe_allow_html=True)
    title_col, home_col, bd_col, in_col, about_col = st.columns(
        [2.2, 1, 1, 1, 1], gap="small"
    )
    with title_col:
        st.markdown('<div class="top-nav-title">🌏 South Asia Data Observatory</div>', unsafe_allow_html=True)
    with home_col:
        st.page_link("app.py", label="Home")
    with bd_col:
        st.page_link("pages/2_Bangladesh.py", label="Bangladesh")
    with in_col:
        st.page_link("pages/1_India.py", label="India")
    with about_col:
        st.page_link("pages/4_About.py", label="About Us")
    st.markdown("</div>", unsafe_allow_html=True)





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


# Bangladesh division/city population growth loader.
@st.cache_data
def load_bangladesh_population_growth_data() -> pd.DataFrame:
    return load_country_data(DIVISION_POPULATION, "bd_division_population")


# Income status time series loader.
@st.cache_data
def load_income_status_data() -> pd.DataFrame:
    return load_country_data(INCOME_SATUS, "income_status")

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


def render_income_status_chart(
    df: pd.DataFrame,
    *,
    selected_countries: list[str] | None = None,
    title: str = "World Bank Income Classification (1987–2024)",
) -> go.Figure | None:
    if df is None or df.empty:
        return None

    temp = df.copy()
    if "Year" in temp.columns:
        temp["Year"] = pd.to_numeric(temp["Year"], errors="coerce")
        temp = temp.dropna(subset=["Year"]).sort_values("Year").set_index("Year")

    if selected_countries is None:
        preferred = ["Bangladesh", "India"]
        selected_countries = [c for c in preferred if c in temp.columns]
    else:
        selected_countries = [c for c in selected_countries if c in temp.columns]

    if not selected_countries:
        return None

    fig = go.Figure()
    line_colors = {
        "Bangladesh": "#27ae60",
        "India": "#3498db",
    }

    for country in selected_countries:
        fig.add_trace(
            go.Scatter(
                x=temp.index,
                y=temp[country],
                name=country,
                mode="lines+markers",
                line_shape="hv",
                line=dict(width=4, color=line_colors.get(country, "#6b7280")),
                marker=dict(size=8, symbol="diamond"),
                hovertemplate="<b>Year: %{x}</b><br>Status: %{y}<extra></extra>",
            )
        )

    default_order = [
        "Low-income countries",
        "Lower-middle-income countries",
        "Upper-middle-income countries",
        "High-income countries",
    ]
    present = pd.unique(temp[selected_countries].values.ravel())
    category_order = [c for c in default_order if c in present]

    fig.update_layout(
        title=f"<b>{title}</b>",
        xaxis_title="Year",
        yaxis_title="Economic Classification",
        height=500,
        showlegend=True,
    )
    if category_order:
        fig.update_layout(
            yaxis=dict(
                categoryorder="array",
                categoryarray=category_order,
            )
        )

    return fig

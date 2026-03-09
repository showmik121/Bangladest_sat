import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# ডেটা লোড করার সময় error হ্যান্ডেল করার জন্য try-except ব্যবহার করা ভালো
df_india = pd.read_csv('india')
df_bd = pd.read_csv('bangladesh_sat.csv')

# --- সাইডবার (Navigation) ---
st.sidebar.title('Country Data Visualization')
country = st.sidebar.selectbox('Select a country', ['India', 'Bangladesh'])

# দেশ অনুযায়ী ভেরিয়েবল সেট করা
if country == 'India':
    main_df = df_india
    list_of_locations = list(main_df['State'].unique())
    list_of_locations.sort()
    list_of_locations.insert(0, 'Overall India')
    location_label = "State/Province"
    # ল্যাটিচিউড-লঙ্গিচিউড কলামের নাম আপনার ফাইল অনুযায়ী চেক করে নিন
    lat_col, lon_col = "Latitude", "Longitude"

else:  # Bangladesh
    main_df = df_bd
    list_of_locations = list(main_df['division'].unique())
    list_of_locations.sort()
    list_of_locations.insert(0, 'Overall Bangladesh')
    location_label = "Division"
    # বাংলাদেশের ফাইলের জন্য কলাম নাম (নিশ্চিত হয়ে নিন এগুলো আপনার CSV তে আছে কি না)
    lat_col, lon_col = "lat", "lon"

# --- মেইন ড্যাশবোর্ড (KPI Section) ---
st.title(f"{country} Data Overview")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    # Population কলামটি আপনার ফাইলের নাম অনুযায়ী মিলিয়ে নিন
    total_pop = main_df['Population'].sum() if 'Population' in main_df.columns else 0
    st.metric(label="👥 Total Population", value=f"{total_pop:,}")

with kpi2:
    # লিটারেসি রেট গড় করা হয়েছে
    lit_col = 'literacy_rate' if 'literacy_rate' in main_df.columns else main_df.columns[-1]
    avg_lit = main_df[lit_col].mean()
    st.metric(label="🎓 Avg Literacy/Parameter Rate", value=f"{avg_lit:.2f}%")

with kpi3:
    st.metric(label="📍 Total Areas/Districts", value=len(main_df))

st.markdown("---")

# --- ডাইনামিক ফিল্টার (Sidebar) ---
selected_location = st.sidebar.selectbox(location_label, list_of_locations)

# শুধুমাত্র সংখ্যাসূচক কলামগুলো প্যারামিটার হিসেবে দেখানো
if country == "India":
    numeric_cols = sorted(main_df.columns[5:])
else:
    numeric_cols = sorted(main_df.select_dtypes(include=np.number).columns)
    numeric_cols = [c for c in numeric_cols if c not in ["lat", "lon"]]

primary = st.sidebar.selectbox('Select Primary Parameter (Size)', numeric_cols)
secondary = st.sidebar.selectbox('Select Secondary Parameter (Color)', numeric_cols)

plot = st.sidebar.button('Plot Graph')

if plot:
    st.subheader(f"{primary} vs {secondary} in {selected_location}")

    # ফিল্টারিং লজিক
    if "Overall" in selected_location:
        display_df = main_df
        zoom_val = 4 if country == 'Bangladesh' else 3
    else:
        area_col = 'State' if country == 'India' else 'division'
        display_df = main_df[main_df[area_col] == selected_location]
        zoom_val = 6

    # ম্যাপ তৈরি
    fig = px.scatter_mapbox(
        display_df,
        lat=lat_col,
        lon=lon_col,
        size=primary,
        color=secondary,
        size_max=15,
        zoom=zoom_val,
        height=600,
        mapbox_style="open-street-map",
        title=f"Analysis of {selected_location}"
    )

    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

df=pd.read_csv('india')
# print(df.head())
list_of_state=list(df['State'].unique())
list_of_state.insert(0,'Overall India')

# --- মেইন ড্যাশবোর্ড (KPI Section) ---
st.title("India Census Overview")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    total_pop = df['Population'].sum()
    st.metric(label="👥 Total Population", value=f"{total_pop:,}")

with kpi2:
    # এখানে ভুল ছিল, গড় লিটারেসি রেট বের করার সঠিক নিয়ম:
    avg_lit = df['literacy_rate'].mean()
    st.metric(label="🎓 Avg Literacy Rate", value=f"{avg_lit:.2f}%")

with kpi3:
    st.metric(label="📍 Total Districts", value=len(df))

st.markdown("---")


st.sidebar.title('Country Data Visualization')
st.sidebar.selectbox('Select a country',['Bangladesh','India','Pakistan'])

selected_state=st.sidebar.selectbox('State/Province',list_of_state)

primary=st.sidebar.selectbox('Select Primary Parameter',sorted(df.columns[5:]))
secondary=st.sidebar.selectbox('Select secondary Parameter',sorted(df.columns[5:]))

plot=st.sidebar.button('Plot Graph')
if plot:
    st.subheader(f"{primary} vs {secondary} Visualization")

    if selected_state == 'Overall India':
        fig = px.scatter_map(df,
                     lat="Latitude", lon="Longitude",
                     size=primary, color=secondary,
                     zoom=3, height=600,
                     title="Overall India Analysis")
        st.plotly_chart(fig, width='stretch')
    else:
        #plot for state
        state_df = df[df['State'] == selected_state]
        fig = px.scatter_map(state_df,
                     lat="Latitude", lon="Longitude",
                     size=primary, color=secondary,
                     zoom=3, height=600,
                     title="Overall India Analysis")
        st.plotly_chart(fig, width='stretch')


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Hackaton2026 RIPCS",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

"""
# :material/query_stats: Hackaton2026 RIPCS

GTA VI is going
"""

""  # Add some space.

df = pd.read_csv('./data/outputs.csv')
df = df.groupby(['risk_category']).size().reset_index(name='Total')

fig = px.pie(df, values='Total', names='risk_category', title="Risk Category",)

colors = ['gold', 'mediumturquoise', 'darkorange']
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color="#00F0DC", width=2)))
st.plotly_chart(fig, theme=None)

""
""

"""
## Raw data
"""

df

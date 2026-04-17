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

DEFAULT_RULE = ["R1", "R2", "R3", "R6", "R7", "R8", "R10", "R12", "R13", "R17", "R18", "R21", "R22", "R24"]
df = pd.read_csv('./data/outputs.csv')
dfTotal = df.groupby(['risk_category']).size().reset_index(name='Total')

fig1 = px.pie(dfTotal, values='Total', names='risk_category', title="Risk Category",)

colors = ['gold', 'mediumturquoise', 'darkorange']
fig1.update_traces(hoverinfo='label+percent', textinfo='value', hole=.3, textfont_size=20,
                  marker=dict(colors=colors, line=dict(color="#00F0DC", width=2)))
st.plotly_chart(fig1, theme=None)

"""
## Total Risk Category
"""
dfTotal

""

dfRules = df['triggered_rules'].str.split(';').explode().to_frame()
dfRules = dfRules.groupby(['triggered_rules']).size().reset_index(name='Total')

fig2 = px.bar(dfRules, x='triggered_rules', y='Total')
st.plotly_chart(fig2, theme=None)

"""
## Total Rules
"""
dfRules
""
""


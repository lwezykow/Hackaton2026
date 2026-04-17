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

DEFAULT_RULE = ["ALL", "R1", "R2", "R3", "R6", "R7", "R8", "R10", "R12", "R13", "R17", "R18", "R21", "R22", "R24"]
outputsDf = pd.read_csv('./data/outputs.csv')
outputAllDf = pd.read_csv('./data/output_all_rules.csv')

with st.sidebar:
    st.header("Settings")
    ruleType = st.selectbox("Rule type", DEFAULT_RULE, index=0)

if ruleType != 'ALL':
    outputsDf = outputsDf[outputsDf["triggered_rules"].str.endswith((ruleType, ruleType+";"))]
    outputAllDf = outputAllDf[outputAllDf["rule_id"] == ruleType]

dfTotal = outputsDf.groupby(['risk_category']).size().reset_index(name='Total')

fig1 = px.pie(dfTotal, values='Total', names='risk_category', title="Risk Category",)

colors = ['gold', 'mediumturquoise', 'darkorange']
fig1.update_traces(hoverinfo='label+percent', textinfo='value', hole=.3, textfont_size=20,
                  marker=dict(colors=colors, line=dict(color="#00F0DC", width=2)))
st.plotly_chart(fig1, theme=None)

""

if ruleType != 'ALL':
    dfRules = outputAllDf.groupby(['channel']).size().reset_index(name='Total')
    fig2 = px.pie(dfRules, values='Total', names='channel', title="Risk Channel",)
    with st.expander("View Rules"):
        st.dataframe(outputAllDf, use_container_width=True)
else:
    dfRules = outputAllDf.groupby(['rule_id']).size().reset_index(name='Count')
    fig2 = px.bar(dfRules, x='rule_id', y='Count')

st.plotly_chart(fig2, theme=None)

""


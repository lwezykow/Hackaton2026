import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html

htmlText = "<div class='content--canvas' style='border-radius: 25px;'>"
htmlText += "<div style='font-size: 30px; top:30px; font-family:verdana; color:rgb(250, 250, 250); text-align: center; position: relative; vertical-align: middle;z-index: 100;'><b>Hackaton2026 RIPCS</b></div></div>"

htmlText += "<script src='https://tympanus.net/Development/AmbientCanvasBackgrounds/js/noise.min.js'></script>"
htmlText += "<script src='https://tympanus.net/Development/AmbientCanvasBackgrounds/js/coalesce.js'></script>"
htmlText += "<script src='https://tympanus.net/Development/AmbientCanvasBackgrounds/js/util.js'></script>"
html(htmlText)

st.set_page_config(
    page_title="Hackaton2026 RIPCS",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

"""
# :material/query_stats: Hackaton2026 RIPCS
"""

""  # Add some space.

DEFAULT_RULE = ["ALL", "R1", "R2", "R3", "R6", "R7", "R8", "R10", "R12", "R13", "R17", "R18", "R21", "R22", "R24"]
outputsDf = pd.read_csv('./data/outputs.csv')
outputAllDf = pd.read_csv('./data/output_all_rules.csv')

categoryHighDf = outputsDf[outputsDf["risk_category"] == 'HIGH']
categoryHighNewDf = pd.DataFrame({'transaction': ['Not set'], 'name': ['Not set']})

for index, row in categoryHighDf.iterrows():
    categoryHighNewDf.loc[-1] = [outputAllDf[outputAllDf["transaction_id"] == row['transaction_id']].iloc[-1].transaction_id, outputAllDf[outputAllDf["transaction_id"] == row['transaction_id']].iloc[-1].entered_beneficiary_name]
    categoryHighNewDf.index = categoryHighNewDf.index + 1 

categoryHighNewDf = categoryHighNewDf.drop_duplicates(subset=["name"])

with st.sidebar:
    st.header("Settings")
    ruleType = st.selectbox("Rule type", DEFAULT_RULE, index=0)
    categoryHigh = st.selectbox("Category High", categoryHighNewDf['name'], index=0)
""
if categoryHigh != 'Not set':
    st.title('Category High - ' + categoryHigh, text_alignment="center")
    outputAllDf[outputAllDf["entered_beneficiary_name"] == categoryHigh][['transaction_id', 'rule_id', 'remarks', 'channel', 'amount', 'official_beneficiary_account_name']]

if ruleType != 'ALL':
    outputAllDf = outputAllDf[outputAllDf["rule_id"] == ruleType]
    dfRules = outputAllDf.groupby(['channel']).size().reset_index(name='Count')
    ruleFig = px.pie(dfRules, values='Count', names='channel', title="Risk Channel",)
    st.plotly_chart(ruleFig, theme=None)

    dfCustomer = outputAllDf.groupby(['entered_beneficiary_name']).size().reset_index(name='Count')
    dfCustomer = dfCustomer[dfCustomer["Count"] > 1]
    beneficiaryFig = px.pie(dfCustomer, values='Count', names='entered_beneficiary_name', title="Beneficiary Name",)
    st.plotly_chart(beneficiaryFig, theme=None)

    with st.expander("View Rules"):
        st.dataframe(outputAllDf, use_container_width=True)
else:
    dfCount = outputsDf.groupby(['risk_category']).size().reset_index(name='Count')
    totalFig = px.pie(dfCount, values='Count', names='risk_category', title="Risk Category",)
    colors = ['red', 'green', 'blue']
    totalFig.update_traces(hoverinfo='label+percent', textinfo='value', hole=.3, textfont_size=20,
                  marker=dict(colors=colors, line=dict(color="#00F0DC", width=2)))
    st.plotly_chart(totalFig, theme=None)
    
    dfRules = outputAllDf.groupby(['rule_id']).size().reset_index(name='Count')
    ruleFig = px.bar(dfRules, x='rule_id', y='Count')
    st.plotly_chart(ruleFig, theme=None)

    dfCustomer = outputAllDf.groupby(['entered_beneficiary_name']).size().reset_index(name='Count')
    dfCustomer = dfCustomer.sort_values(by=["Count"])
    dfCustomer = dfCustomer.iloc[-1]

    htmlText = "<div style='font-size: 22px; position: relative; text-align: center;'><img src='https://www.api.moski.pl/gallery/cs/cs.png' style='width:400px;'><div style='position: absolute;top: 55%;left: 50%;transform: translate(-50%, -50%);'><b>" + dfCustomer['entered_beneficiary_name']
    htmlText += "<br/>"
    htmlText += "Rules count: "
    htmlText += str(dfCustomer['Count'])
    htmlText += "!</b></div></div>"
    st.html(htmlText)
""


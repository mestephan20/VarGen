import streamlit as st, requests

st.header('VAR Generator')
commodities=['Light Crude','Brent Crude','Natural Gas','Gasoline (RBOB)','S&P 500 Index']
confidence=['90%','95%','99%']
direction=['Long','Short']
var_lkbk=['7D','30D','90D','180D']
chart_range=['1M','3M','6M','YTD','1Y','2Y']

commodities_dropdown=st.selectbox('Specify Commodity', commodities)
confidence_dropdown=st.selectbox('Specify Confidence Level', confidence)
direction_dropdown=st.selectbox('Specify Direction', direction)
var_lkbk_dropdown=st.selectbox('Specify VAR Lookback', var_lkbk)
chart_range_dropdown=st.selectbox('Specify Chart Range', chart_range)

if st.button('Generate VAR'):
  st.write(commodities_dropdown)

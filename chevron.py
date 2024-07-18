import streamlit as st
from streamlit_echarts import st_echarts
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

st.sidebar.header('VAR Generator 📈')
commodities=['WTI Crude','Brent Crude','Heating Oil','Gasoline (RBOB)','Natural Gas','S&P 500 Index']
confidence=['90%','95%','99%'] #2.33, 1.64, 1.28
direction=['Long','Short']
var_lkbk=['10D','25D','50D','75D','150D','300D','600D']
var_weighting = ['Equal WMA','Exponential WMA']

commodities_dropdown=st.sidebar.selectbox('Commodity', commodities)
confidence_dropdown=st.sidebar.selectbox('Confidence Level', confidence)
direction_dropdown=st.sidebar.selectbox('Direction', direction)
var_lkbk_dropdown=st.sidebar.selectbox('VAR Lookback', var_lkbk)
var_weight_dropdown=st.sidebar.selectbox('VAR Weighting', var_weighting)
st.sidebar.radio('Chart Type',['Candle Chart','Line Chart'])

if st.sidebar.button('Generate VAR'):
  st.write('Loading...')

#options: CL=F BZ=F & RB=F & HO=F & NG=F & ES=F
ticker = 'CL=F'
data = yf.download(ticker, period='10mo').round(2)
data = data.drop(data.columns[4],axis=1)
data1 = data.reset_index()
stringg = data1['Date'].tolist()
date_stringg = pd.to_datetime(stringg,format='%Y-%m-%d')
date_stringg1 = date_stringg.strftime('%Y-%m-%d').tolist()
data1['Date'] = date_stringg1
exit()


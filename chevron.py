import streamlit as st
from streamlit_echarts import st_echarts
import time
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
pio.templates.default = 'plotly' 

st.sidebar.header('VAR Generator 📈')
commodities=['WTI Crude','Brent Crude','Heating Oil','Gasoline (RBOB)','Natural Gas','S&P 500 Index']
confidence=['90%','95%','97%','99%'] #1.28, 1.64, 1.88, 2.33
var_lkbk=['10D','25D','50D','75D','150D','300D','600D']
var_weighting = ['Equal WMA','Exponential WMA']

commodities_dropdown=st.sidebar.selectbox('Commodity', commodities)
position = st.sidebar.number_input('Position Size', min_value=-1000000, max_value=1000000, value=1000, step=1)
conf_drop=st.sidebar.selectbox('Confidence Level', confidence)
var_lkbk_dropdown=st.sidebar.selectbox('VaR Lookback', var_lkbk)
var_weight_dropdown=st.sidebar.selectbox('VaR Weighting', var_weighting)
varunits = st.sidebar.radio('VaR Units',['Dollars ($)','Percent (%)'])
# st.sidebar.radio('Chart Type',['Candle Chart','Line Chart'])

#options: CL=F BZ=F & RB=F & HO=F & NG=F & ES=F
def ticker1(commodities_dropdown):
  if commodities_dropdown == 'WTI Crude':
    return 'CL=F'
  elif commodities_dropdown == 'Brent Crude':
    return 'BZ=F'
  elif commodities_dropdown == 'Heating Oil':
    return 'HO=F'
  elif commodities_dropdown == 'Gasoline (RBOB)':
    return 'RB=F'
  elif commodities_dropdown == 'Natural Gas':
    return 'NG=F'
  elif commodities_dropdown == 'S&P 500 Index':
    return 'ES=F'
ticker = ticker1(commodities_dropdown)

def tradesize(commodities_dropdown):
  if commodities_dropdown == 'WTI Crude':
    return 1000
  elif commodities_dropdown == 'Brent Crude':
    return 1000
  elif commodities_dropdown == 'Heating Oil':
    return 42000
  elif commodities_dropdown == 'Gasoline (RBOB)':
    return 42000
  elif commodities_dropdown == 'Natural Gas':
    return 10000
  elif commodities_dropdown == 'S&P 500 Index':
    return 50
commsize = tradesize(commodities_dropdown)

data = yf.download(ticker, start='2019-08-05').round(2)
data = data.drop(data.columns[4],axis=1)
data1 = data.reset_index()
stringg = data1['Date'].tolist()
date_stringg = pd.to_datetime(stringg,format='%Y-%m-%d')
date_stringg1 = date_stringg.strftime('%Y-%m-%d').tolist()
data1['Date'] = date_stringg1

data2 = data1
def lookback_spec(var_lkbk_dropdown):
  if var_lkbk_dropdown == '10D':
    return 10
  elif var_lkbk_dropdown == '25D':
    return 25
  elif var_lkbk_dropdown == '50D':
    return 50
  elif var_lkbk_dropdown == '75D':
    return 75
  elif var_lkbk_dropdown == '150D':
    return 150
  elif var_lkbk_dropdown == '300D':
    return 300
  elif var_lkbk_dropdown == '600D':
    return 600
varlookback = lookback_spec(var_lkbk_dropdown)

def conf(conf_drop): 
  if conf_drop == '90%':
    return 1.28 
  elif conf_drop == '95%':
    return 1.64 
  elif conf_drop == '97%': 
    return 1.88 
  elif conf_drop == '99%':
    return 2.33

#HO size 42000, NG size 10000, CL size 1000, ES=F x50, RB size 42000
data2['Perf%'] = data2['Close'].pct_change().round(4)
data2['Rolling_Mean'] = data2['Perf%'].rolling(window=varlookback).mean().round(5)
data2['Rolling_Variance'] = data2['Perf%'].rolling(window=varlookback).var().round(5)
data2['Rolling_StdDev'] = data2['Rolling_Variance'].apply(np.sqrt).round(5)
if varunits == 'Dollars ($)':
    data2['PVaR'] = round(data2['Close'] * data2['Rolling_StdDev'] * conf(conf_drop) * abs(position) * commsize, 0)
else:
    data2['PVaR'] = round(data2['Rolling_StdDev'] * conf(conf_drop) * 100, 2)
data2['MA'] = data2['Close'].rolling(window=200).mean().round(5)

data2 = data2.tail(993)

def get_candlestick_plot(
        df: pd.DataFrame,
        ticker: str
):
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = .01,
        subplot_titles = (f'{ticker} Price', ''),
        row_width = [.4, .8]
    )
    fig.add_trace(
        go.Candlestick(
            x = df['Date'],
            open = df['Open'], 
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )

    fig.add_trace(
          go.Scatter(x = df['Date'], y = df['MA'], name = '200 MA', line=dict(color='#FFFFFF', width=1)),
          row = 1,
          col = 1,
      )

    # fig.add_trace(
    #     go.Line(x = df['Date'], y = df['PVaR'], name = 'PVaR'),
    #     row = 2,
    #     col = 1,)

    fig.add_trace(
        go.Scatter(x = df['Date'], y = df['PVaR'], name = 'PVaR', line=dict(color='#4a86e8', width=2)),
        row = 2,
        col = 1,
    )

    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'VaR'

    fig.update_xaxes(
        rangebreaks = [{'bounds': ['sat', 'mon']}],
        rangeslider_visible = False,
    )

    fig.data[0].increasing.fillcolor = '#4ca690'
    fig.data[0].increasing.line.color = '#4ca690'
    fig.data[0].decreasing.fillcolor = '#ef3b4a'
    fig.data[0].decreasing.line.color = '#ef3b4a'

    return fig

if st.sidebar.button('Generate VaR'):
  with st.spinner("Calculating VaR..."): 
    time.sleep(1.8)
  with st.spinner("Loading Figures..."): 
    time.sleep(.8)
#random.uniform(1.8, 2.0)

  st.plotly_chart(
    get_candlestick_plot(data2, ticker),
    use_container_width = True,)

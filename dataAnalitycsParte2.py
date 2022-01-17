# -*- coding: utf-8 -*-
import warnings

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as py
import requests
import seaborn as sns
import statsmodels.api as sm
import yfinance as yf
from pylab import rcParams
from sklearn.metrics import mean_squared_error

url = "https://investnews.com.br/financas/veja-a-lista-completa-dos-bdrs-disponiveis-para-pessoas-fisicas-na-b3/"
r = requests.get(url)
html = r.text
df_names_tickers = pd.read_html(html, header=0)[0]
df_names_tickers.head(10)

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
matplotlib.rcParams['axes.labelsize']=14
matplotlib.rcParams['xtick.labelsize']=12
matplotlib.rcParams['ytick.labelsize']=12

dados_series = yf.download("PETR4.SA", start="2018-01-01", end="2022-01-16")

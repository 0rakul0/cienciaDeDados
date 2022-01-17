# -*- coding: utf-8 -*-
import pandas as pd
import requests
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import warnings
import plotly.io as pio
import plotly.offline as py
import plotly.graph_objs as go
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns
from pylab import rcParams

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

with pd.option_context('display.max_rows', 10):
    print(df_names_tickers)
    print(dados_series)

sns.set_theme(style="darkgrid")
sns.displot(dados_series['Close'].dropna())

pio.renderers

dados_grafico = [go.Scatter(x=dados_series.index, y=dados_series['Close'])]
py.plot(dados_grafico)

df = dados_series.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)

df.plot(figsize=(19, 4))
plt.show

rcParams['figure.figsize']=18, 8

decomposition = sm.tsa.seasonal_decompose(x=df, period=20, model='Additive')
fig = decomposition.plot()
plt.show()

"""Modelo de medidas móveis ( suavilização )"""

mm = pd.DataFrame.rolling(df, window=12, center=False).mean()
orig = plt.plot(df, color='blue', label='Original')
mean = plt.plot(mm, color='red', label='Média')
plt.legend(loc='best')
plt.show

# aplica o metodo para obter previsões para até 12 passos à frente -> horizonte
def medias_moveis(series, n):
  '''
      Calcula a media da ultima n observações
  '''
  return np.average(series[-n:])

medias_moveis(df, 12)

"""Metodo ARIMA ( p,q,d)

a base de dados é o data_frame com 70% das informações começando da linha 0 e vai até o final.

inicio >> df[0:int(len(df)*0.7)]

final >> df[int(len(df)*0.7):]
"""

dados_treinamento, dados_teste = df[0:int(len(df)*0.7)], df[int(len(df)*0.7):]

"""para criar um banco de treinamento"""

dados_treinamento = dados_treinamento['Close'].values

"""para criar o banco de testes"""

dados_teste = dados_teste['Close'].values

"""Histórico"""

historico = [x for x in dados_treinamento]

"""Modelo preditivo"""

modelo_preditivo = []

N_observacoes_teste = len(dados_teste)
for ponto_de_teste in range (N_observacoes_teste):
  modelo = sm.tsa.arima.ARIMA(historico, order=(1,1,0))
  """histórico ( AR = 1, 1 diferença, 0 medias moveis)"""
  modelo_fit = modelo.fit()
  """o fit extrai as caracteristicas dos dados"""
  saida = modelo_fit.forecast()
  """# após o treino ele já pode ser encaminhado para fazer as previsões"""
  yhat = saida[0]
  """# valor obtivo pelo modelo"""
  modelo_preditivo.append(yhat)
  """ # guarda a lista yhat"""
  valor_real_teste = dados_teste[ponto_de_teste]
  """ # pega o dado Real"""
  historico.append(valor_real_teste)
  """# combina com o valor de cima"""

erroMSE = mean_squared_error(dados_teste, modelo_preditivo)
"""# comparativo de qualidade"""
print('O erro Médio Quadrado (MSE) é {}'.format(erroMSE))
"""# quanto mais proximo de 0 melhor"""

intervalo_dos_dados_de_teste = df[int(len(df)*0.7):].index

plt.plot(intervalo_dos_dados_de_teste,
         modelo_preditivo,
         color='blue',
         marker='o',
         linestyle='dashed',
         label='Preco_Estimado')

plt.plot(intervalo_dos_dados_de_teste,
         dados_teste,
         color='green',
         label='Preco_Real')

plt.title('Predição dos da Petrobras')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.legend()
plt.show()

look_back = 1
plt.figure(figsize=(50,10))

plt.plot(list(np.arange(len(intervalo_dos_dados_de_teste))),
         dados_teste,
         marker='.',
         label="Real")

plt.plot(list(np.arange(len(intervalo_dos_dados_de_teste))-look_back),
         modelo_preditivo,
         'r',
         label='Estimação do modelo')
plt.xlabel('periodo', size=15)
plt.ylabel('valores', size=15)
plt.legend(fontsize=15)
plt.show

modelo = sm.tsa.arima.ARIMA(historico, order=(1,1,0))
modelo_fit = modelo.fit()
saida = modelo_fit.forecast()
yhat = saida[0]
print('Valor Previsto:{}'.format(yhat))
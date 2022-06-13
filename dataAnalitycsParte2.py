# -*- coding: utf-8 -*-
import warnings

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import requests
import seaborn as sns
import tensorflow as tf
import yfinance as yf
from keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential

url = "https://investnews.com.br/financas/veja-a-lista-completa-dos-bdrs-disponiveis-para-pessoas-fisicas-na-b3/"
r = requests.get(url)
html = r.text
df_names_tickers = pd.read_html(html, header=0)[0]
df_names_tickers.head(10)

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12

dados_series = yf.download("PETR4.SA", start="2020-01-01", end="2022-03-20")

with pd.option_context('display.max_rows', 10):
    print(df_names_tickers)
    print(dados_series)

sns.set_theme(style="darkgrid")
sns.displot(dados_series['Close'].dropna())

render = pio.renderers

dados_grafico = [go.Scatter(x=dados_series.index, y=dados_series['Close'])]

df = dados_series.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)

"""Carrega os dados """
y = []
for a in df['Close']:
    print(a)
    y.append(a)

"""Vetor do fechamento"""
x = np.arange(1, len(y) + 1, 1)
"""
print('x: {}'.format(x))
print('Y: {}'.format(y))
"""
"""Normalização variação de 0 a 1"""
minimo = np.min(y)
maximo = np.max(y)
y = (y - minimo) / (maximo - minimo)
"""
print(y)
"""
"""dentro de uma rede neural podemos ter funções de atiavação (podendo ser 0 a 1)"""

"""outra forma de normalizar

norma = np.linalg.norm(y)
y = y/norma
print('dados_normalizados: {}'.format(y))

"""
# plt.title('Serie Temporal - Normalizada')
# plt.xlabel('Periodo')
# plt.ylabel('Valor')
# plt.plot(x, y)
# plt.show()

"""Para treinamento é necessario separar para historico e teste"""
percentual_treinamento = 0.8
qtd_treinamento = int(percentual_treinamento * (len(x)))
"""80% dos dados do historico são usados"""

x_treino = x[0:qtd_treinamento]
x_teste = x[qtd_treinamento:]
"""80% <- treino, 20% testes """

y_treino = y[0:qtd_treinamento]
y_teste = y[qtd_treinamento:]
"""80% <- treino, 20% testes """

treino = np.array(list(zip(x_treino, y_treino)))
teste = np.array(list(zip(x_teste, y_teste)))
"""A função zip agrupa dados, logo zip(x_treino, y_treino) fica como par ordenado (x,y)"""

"""
for i in range(5):
    print('Treino[{}]: {}'.format(i+1, treino[i]))
"""
"""essa fução tem a mesma caracteristica de fibronacci olha dados para trás """


def create_dataset(n_X, look_back):
    dataX = []
    dataY = []
    for i in range(len(n_X) - look_back):
        a = n_X[i:(i + look_back), ]
        print('a: {}'.format(a))
        dataX.append(a)
        dataY.append(n_X[i + look_back])
    print('dataX: {}'.format(dataX))
    return np.array(dataX), np.array(dataY)


"""Ajuste de dados"""

def prepara_dados(dados_serie, look_back):
    x, y = [], []
    n = len(dados_serie)
    for i in range(n - look_back):
        posicao_fim = i + look_back
        if posicao_fim <= n:
            seq_x = dados_serie[i:posicao_fim, 1]
            seq_y = dados_serie[i:posicao_fim, 1]
            x.append(seq_x)
            y.append(seq_y)
    return np.array(x), np.array(y)


look_back = 2
x_treino, y_treino = prepara_dados(treino, look_back)
x_teste, y_teste = prepara_dados(teste, look_back)

n_caracteristicas = 1  # serie monovariada

"""
    é necessario estruturar não pode tacar numero direto no tensorflow
    ná pratica é uma matriz
"""
x_treino = x_treino.reshape((x_treino.shape[0],
                             x_treino.shape[1],
                             n_caracteristicas))

x_teste = x_teste.reshape((x_teste.shape[0],
                           x_teste.shape[1],
                           n_caracteristicas))

"""matriz gerada com as informações de saida"""
for i in range(5):
    print('treino[{}]: {} -> {}'.format(i + 1, x_treino[i], y_treino[i]))

"""rede neural do tipo LSTM de camada densa"""
""" 
    o dorpout basicamente desliga alguns neuronios ( baias, nós )
    para que o apredizado não fique viciado
 """

n_etapas = x_treino.shape[1]  # dados atrás para treino
n_caracteristicas = x_treino.shape[2]  # numero de caracteristicas
epocas = 20  # quantidade de ciclos de treinamentos
n_unidades = 100  # numero de nós -> bais -> neuroninios

tf.random.set_seed(8888)  # semente para garantir a reprodutibilidade

"""modelo da rede"""
modelo = Sequential()
camada_de_entrada = (n_etapas, n_caracteristicas)  # info das etapas e caracteristicas
modelo.add(LSTM(n_unidades,
                return_sequences=True,
                input_shape=camada_de_entrada))
modelo.add(Dropout(0.2))  # ele deslida de maneira aletória 20% dos nós
modelo.add(LSTM(128,
                input_shape=camada_de_entrada))
modelo.add(Dense(1))

"""mostra o tipo de modelo que está sendo usado"""
modelo.summary()

"""após a criação da rede neural é necessário compilar o modelo para usa-lo"""

modelo.compile(loss='mean_squared_error',
               optimizer='adam')

"""usando dados na rede"""
historico = modelo.fit(x_treino, y_treino,
                       epochs=epocas,
                       batch_size=70,
                       verbose=2,
                       shuffle=False,
                       validation_split=0.3)

"""esse metodo ainda usa validação usando 30% do todo histórico"""
"""bactch_size <- tamanho dos dados para estudo"""
"""para imprimir os dados"""
hist = pd.DataFrame(historico.history)
hist.head()

loss = modelo.evaluate(x_teste, y_teste, batch_size=64)
print("loss: {}".format(loss))

"""grafico"""
# plt.title('Cálculo de Erro ao longo do treinamento')
# plt.ylabel('Erro')
# plt.xlabel('Época')
# plt.plot(historico.history['loss'])
# plt.plot(historico.history['val_loss'])
# plt.legend(['loss (treinamento)', 'val_loss (validação)'], loc='upper right')
# plt.show()

"""modelo de predição"""
predicao = modelo.predict(x_teste)

escala = 1
look_back = 1
valores_reais_y = y_teste * escala
plt.figure(figsize=(50, 10))
plt.plot(list(range(len(valores_reais_y))),
         valores_reais_y,
         marker='.',
         label="Real")

lst_dados_predicao = [w[0] * escala for w in predicao]
plt.plot(list(range(len(predicao))),
         lst_dados_predicao,
         'r',
         label="Estimação do modelo")

plt.ylabel('Valores', size=15)
plt.xlabel('Período', size=15)
plt.legend(fontsize=15)
plt.show()

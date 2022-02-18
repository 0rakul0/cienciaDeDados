"""
o objetivo aqui é achar o melhor valor para a costante e o coeficiente

y   <- previsão de custo
b¹  <- costante
b²  <- coeficiente
x   <- timeLine

y = b+b¹*x¹ <- simples
y = b+b¹*x¹ + b²*n² + b³*x³ ... bn * xn <- multipla

é necessario também enteder o erro de distancia da linha
tecnica mais usada é o MSE <- Mean square error

Soma tudo i=1 até n (xi-yi)² / n

após o treinamento é necessario ajustar os parametros

"""
#regressão linear simples
#importações
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression


#obtenção de dados
base_casa = pd.read_csv('data/house_prices.csv')
#print(base_casa)

#describe dos dados
base_casa = base_casa.describe()
#print(base_casa)

#removendo valores null
base_casa.isnull().sum()

#correlações
figura = plt.figure(figsize=(20, 20))
correlacao = sns.heatmap(base_casa.corr(), annot=True);
#plt.show()

#analise
x_casas = base_casa.iloc[:, 5:6].values
y_casas = base_casa.iloc[:, 2].values
#print(x_casa)
#print(y_casa)

#usando o sklearn
"""
usa treinamento de x e y 
usa teste de x e y
proporção   0.7 treinamento
            0.3 teste
"""
X_casas_treinamento, X_casas_teste, y_casas_treinamento, y_casas_teste = train_test_split(x_casas, y_casas, test_size = 0.3, random_state = 0)

#vizualizando o treinamento
X_casas_treinamento.shape, y_casas_treinamento.shape
#print(X_casas_treinamento, y_casas_treinamento)

#vizualizando teste
X_casas_teste.shape, y_casas_teste.shape
#print(X_casas_teste, y_casas_teste)

#modelo de regressão linear com sns
regressor_simples_casas = LinearRegression()
regressor_simples_casas.fit(X_casas_treinamento, y_casas_treinamento)

#b0
b0 = regressor_simples_casas.intercept_
print(b0)
#b1
b1 = regressor_simples_casas.coef_
print(b1)

regressor_simples_casas.score(X_casas_treinamento, y_casas_treinamento)
regressor_simples_casas.score(X_casas_teste, y_casas_teste)

#previsões
previsoes = regressor_simples_casas.predict(X_casas_treinamento)
print(previsoes)

#grafico
grafico = px.scatter(x = X_casas_treinamento.ravel(), y = previsoes)
grafico1 = px.scatter(x = X_casas_treinamento.ravel(), y = y_casas_treinamento)
grafico2 = px.line(x = X_casas_treinamento.ravel(), y = previsoes)
grafico2.data[0].line.color = 'red'
grafico3 = go.Figure(data=grafico1.data + grafico2.data)
grafico3
grafico.show()
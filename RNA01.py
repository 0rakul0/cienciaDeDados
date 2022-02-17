"""
o objetivo aqui é achar o melhor valor para a costante e o coeficiente

y   <- previsão de custo
b0  <- costante
b¹  <- coeficiente
x¹  <- timeLine

y = b0+b¹*x¹ <- simples
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
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

#obtenção de dados
base_plano_saude = pd.read_csv('data/plano_saude.csv')

#representação das colunas
idade = 0
custo = 1

x = idade
y = custo
"""o iloc seleciona um conjunto de registros, 
: <- significa todas as linhas 
x <- representa a coluna desejada
.values <- converte para estrutura de array
"""
x_plano_saude = base_plano_saude.iloc[:, x].values
y_plano_saude = base_plano_saude.iloc[:, y].values

print(x_plano_saude)
print(y_plano_saude)

#coeficiente de correlação
correlacao = np.corrcoef(x_plano_saude, y_plano_saude)
print(correlacao)

"""como os dados obtido estão proximo de 1 significa que
 regressão linear funciona muito bem"""

#vizualizando o formato
x_plano_saude = x_plano_saude.reshape(-1, 1)
# temos 10 e 1 coluna
#print(x_plano_saude.shape)

#sklearn com linear regression
regressor_plano_saude = LinearRegression()
#treinamento
regressor_plano_saude.fit(x_plano_saude, y_plano_saude)

# y = b0+b¹*x¹ <- simples
#b0
b0 = regressor_plano_saude.intercept_
print(b0)

#b1
b1 = regressor_plano_saude.coef_
print(b1)

#previssor
previsoes = regressor_plano_saude.predict(x_plano_saude)
print(previsoes)

#tirando o formato de matriz
#x_plano_saude.ravel()


#grafico
grafico = px.scatter(x= x_plano_saude.ravel(), y=y_plano_saude)
grafico.show()
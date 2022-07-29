# etapas
#1 entendendo o problema
#2 regra de negocio
#3 extração e tratamento
#4 analise exploratória
#5 modelagem

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score


tabela = pd.read_csv('./data/advertising.csv')
# print(tabela)
tabela.info()
# print(tabela.describe())

# analise exploratória
# - correlação
# print(tabela.corr())

#criar o grafico
sns.heatmap(tabela.corr(), cmap='Wistia', annot=True)
# exibir o grafico
plt.show()

#serparação dos dados
#quando é mais de uma coluna usa colchetes duas vezes a interna é a lista de colunas a externa é a coluna mesmo
x = tabela[['TV', 'Radio', 'Jornal']]
y = tabela['Vendas']

# o parametro test_size=    calcula o percentual
treino_X, teste_X, treino_Y, teste_y = train_test_split(x, y, random_state=1)

# regressão Linear
modelo_ressaolinear = LinearRegression()
# arvore de decisão
modelo_arvoredecisao = RandomForestRegressor()

# treinamento do modelo
modelo_ressaolinear.fit(treino_X, treino_Y)
modelo_arvoredecisao.fit(treino_X, treino_Y)

#resultado previsão
previsao_regressaolinear = modelo_ressaolinear.predict(teste_X)
previsao_arvoredecisao = modelo_arvoredecisao.predict(teste_X)

#escolhendo o melhor modelo
print(" regressão Linear ",r2_score(teste_y, previsao_regressaolinear))
print(" arvore de decisão", r2_score(teste_y, previsao_arvoredecisao))

# Vizualização grafica do modelo
tabela_grafica = pd.DataFrame()
tabela_grafica['teste_y'] = teste_y
tabela_grafica['arvore_decisao'] = previsao_arvoredecisao
tabela_grafica['regressaoLinear']= previsao_regressaolinear

plt.figure(figsize=(15,6))
sns.lineplot(data=tabela_grafica)
plt.show()

# modelo vencedor
# arvore de decisao

novos = pd.read_csv('./data/novos.csv')
print(novos)

print(modelo_arvoredecisao.predict(novos))

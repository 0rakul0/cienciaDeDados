# grafico statistico boxplot
import lsm as lsm
import pandas as pd
import io
from pyod.models.knn import KNN
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import statistics as st

# geração de outliers
tabela = pd.read_excel("data/tx_bruta_mort1.xlsx")

# verificando se há valores nullos
tabela.isnull().sum()

# caso houver valores nullos >> tabela.dropna(inplace=True)
tabela.dropna(inplace=True)

# toda a tabela
print(tabela)

#soma das colunas
soma_ano = tabela.sum()
print("A soma_ano: {}".format(soma_ano))

# tabala com só que iremos usar 2021
tabela_mun_2021 = tabela[['Município', '2021']]
tabela_mun_2021.columns = ['Município', 'taxa']
tabela_mun_2021.head(10)
with pd.option_context('display.max_rows', 10, 'display.max_columns', 2):
    print(tabela_mun_2021)

#detector com knn
detector = KNN()
detector.fit(tabela.iloc[:,19:23])

#gerando previsores
previsao = detector.labels_
possiveis_outliers = np.unique(previsao, return_counts=True)
print(possiveis_outliers)

#confiança
confianca_previsoes = detector.decision_scores_
print(confianca_previsoes)

#gerando uma saida para analise
outliers = []
for i in range(len(previsao)):
    if previsao[i] == 1:
        outliers.append(i)

#indices
print(outliers)

#indices com nomes
lista_outliers = tabela_mun_2021.iloc[outliers,:]
print(lista_outliers)

lista_outliers.to_excel('data/taxaBrutaMortalidade.xlsx', index=False)

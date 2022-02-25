# grafico statistico boxplot
import lsm as lsm
import pandas as pd
import io
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

# tabala com só que iremos usar 2021
tabela_mun_2021 = tabela[['Município', '2021']]
tabela_mun_2021.columns = ['Município', 'taxa']
tabela_mun_2021.head(10)
with pd.option_context('display.max_rows', 10, 'display.max_columns', 2):
    print(tabela_mun_2021)

#para o grafico de dispersão é necessario um x e um y como um plano cartesiano
#grafico = px.scatter(x=tabela_mun_2021['Município'], y=tabela_mun_2021['taxa'])
#grafico.show()

#caso queira combinar anos como 2020 com 2021
#grafico = px.scatter(x=tabela['2020'], y=tabela['2021'])
#grafico.show()

q1 = tabela_mun_2021['taxa'].quantile(0.25)
q2 = tabela_mun_2021['taxa'].quantile(0.5)
q3 = tabela_mun_2021['taxa'].quantile(0.75)
q4 = q3-q1
print('Primeiro quartil ', q1)
print('Segundo quartil', q2)
print('Terceiro quartil ', q3)
print('Diferença interquartílica ', q4)
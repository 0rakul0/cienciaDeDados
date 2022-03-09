# grafico statistico boxplot
import warnings

import pandas as pd
import plotly.express as px

warnings.filterwarnings('ignore')

"""
Crie uma rotina para classificar a **taxa_mort_2021 dos municípios** em 4 categorias correspondentes aos quartis. 
Adicione esse indicador a última coluna do Data Frame original.
Gere indicadores numéricos e gráficos que permitam avaliar a distribuição desse indicador.\n",
"Pode fazer em grupo."

#################################

Jefferson Silva dos Anjos: 2016200130 
Bruno Rocha:    2015101850
João victor costa da cruz: 2015101476
Paulo henrique: 2015101631

"""

# geração de outliers
tabela = pd.read_excel("data/tx_bruta_mort1.xlsx")

# verificando se há valores nullos
tabela.isnull().sum()

# caso houver valores nullos >> tabela.dropna(inplace=True)
tabela.dropna(inplace=True)

# toda a tabela
print(tabela)
print("##############################")
# tabala com só que iremos usar 2021
tabela_mun_2021 = tabela[['Município', '2021']]
tabela_mun_2021.columns = ['Município', 'taxa']
tabela_mun_2021.head(10)
with pd.option_context('display.max_rows', 10, 'display.max_columns', 2):
    print(tabela_mun_2021)
print("##############################")
#para o grafico de dispersão é necessario um x e um y como um plano cartesiano
grafico = px.box(tabela_mun_2021, x=tabela_mun_2021['Município'], y=tabela_mun_2021['taxa'])
grafico.show()

#caso queira combinar anos como 2020 com 2021
#grafico = px.histogram(tabela_mun_2021, x=tabela_mun_2021['Município'], y=tabela_mun_2021['taxa'])
#grafico.show()

q1 = tabela_mun_2021['taxa'].quantile(0.25)
q2 = tabela_mun_2021['taxa'].quantile(0.5)
q3 = tabela_mun_2021['taxa'].quantile(0.75)
q4 = tabela_mun_2021['taxa'].quantile(1)
diferenca = q4-q1

print("##############################")
print('Primeiro quartil ', q1)
print('Segundo quartil', q2)
print('Terceiro quartil ', q3)
print('Quarto quartil', q4)
print('Diferença interquartílica ', diferenca)
print("##############################")

tabela_nova = []

for x in tabela_mun_2021['taxa'].values:
    if x <= q1:
        #print(f"{x} pertence ao q1 ")
        tabela_nova.append("q1")
    elif q1 < x <= q2:
        #print(f"{x} pertence ao q2")
        tabela_nova.append("q2")
    elif q2 < x <= q3:
        #print(f"{x} pertence ao q3")
        tabela_nova.append("q3")
    else:
        #print(f"{x} pertence ao q4")
        tabela_nova.append("q4")

tabela_mun_2021['quartile'] = tabela_nova
print(tabela_mun_2021)

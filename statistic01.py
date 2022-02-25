# grafico statistico boxplot
import pandas as pd
import plotly.express as px

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

outliers_2021 = tabela_mun_2021[tabela['2021'] < 6]

#outliers
grafico = px.box(tabela_mun_2021,y='taxa')
grafico.show()
print(outliers_2021)
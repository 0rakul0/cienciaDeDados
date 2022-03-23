# Preparar uma apresentação usando storytelling sobre:
# • Há alguma região de saúde mais preocupante?
# • Há alguma região de saúde que não precisa de atenção?
# • Há uma relação entre morbidade e faixas etárias?
# • Há uma relação entre morbidade e sexo?


# Objetivos:
# • Como estamos hoje (por região, faixa etária, sexo)?
# • Como a situação vem evoluindo (por região, faixa etária, sexo)?

# foco saúde
import pandas as pd

#import das tabelas
df_distribuicao_da_populacao = pd.read_excel('data/baiana/Distribuicao da populacao (em relacao a coluna) por Regiao de Saude segundo Municipio 2020.xlsx')
df_tme_ano_regiao = pd.read_excel('data/baiana/Indicadores de mortalidade por DCNT - TME diabete melito por Ano segundo Regiao de Saude 2011 a 2021.xlsx')
df_tme_sexo = pd.read_excel('data/baiana/Indicadores de mortalidade por DCNT - TME diabete melito por Ano segundo Sexo.xlsx')


print(df_tme_sexo)



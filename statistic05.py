# Preparar uma apresentação usando storytelling sobre:
# • Há alguma região de saúde mais preocupante?
# • Há alguma região de saúde que não precisa de atenção?
# • Há uma relação entre morbidade e faixas etárias?
# • Há uma relação entre morbidade e sexo?

# Objetivos:
# • Como estamos hoje (por região, faixa etária, sexo)? ok
# • Como a situação vem evoluindo (por região, faixa etária, sexo)? ok

# foco saúde
import pandas as pd

#import das tabelas
df_distribuicao_da_populacao = pd.read_excel('data/baiana/Distribuicao da populacao (em relacao a coluna) por Regiao de Saude segundo Municipio 2020.xlsx')
df_tme_ano_regiao_2011_2021 = pd.read_excel('data/baiana/Indicadores de mortalidade por DCNT - TME diabete melito por Ano segundo Regiao de Saude 2011 a 2021.xlsx')
df_tme_sexo = pd.read_excel('data/baiana/Indicadores de mortalidade por DCNT - TME diabete melito por Ano segundo Sexo.xlsx')
df_tme_faixa_etaria = pd.read_excel('data/baiana/Indicadores de mortalidade por DCNT - TME diabete melito por Faixa etaria DCNT segundo Ano 2011 a 2021.xlsx')
df_tme_comparativo_2020_2021 = pd.read_excel('data/baiana/Indicadores de mortalidade por DCNT - TME diabete melito por Sexo segundo Ano 2011 a 2021.xlsx')
df_tme_ano_regiao_2021 = pd.read_excel('data/baiana/Indicadores de mortalidade por DCNT - TME diabete melito por Sexo segundo Regiao de Saude 2021.xlsx')
df_indice_envelhecimento = pd.read_excel('data/baiana/indice de envelhecimento por Regiao de Saude segundo Sexo.xlsx')
df_proporcao_idosos_2020 = pd.read_excel('data/baiana/Proporcao de idosos na populacao por Regiao de Saude segundo Municipio 2020.xlsx')

print(df_distribuicao_da_populacao)

df_distribuicao = pd.DataFrame(df_distribuicao_da_populacao, columns=("Baia da Ilha Grande", ""))



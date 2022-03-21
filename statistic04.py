import numpy as np
import pandas as pd

"""
participantes
Jefferson Silva dos Anjos: 2016200130 
Bruno Rocha:    2015101850
João victor costa da cruz: 2015101476
Paulo henrique: 2015101631
"""

# importando planilha
tabela = pd.read_excel("data/trabalho_02.xlsx")

# verificando se há valores nullos
tabela.isnull().sum()

# caso houver valores nullos >> tabela.dropna(inplace=True)
tabela.dropna(inplace=True)

# toda a tabela
# print(tabela)

# tabela que será trabalhada
nova_tabela = pd.DataFrame(tabela, columns=['Nome', 'altura'])
print(nova_tabela)

"""
obtendo dados
01- Determinar um INTERVALO DE CONFIANÇA para a ALTURA dos alunos da turma.
•	Nível de confiança - 95%
•	Tamanho da População - 46 alunos
•	Tamanho da Amostra - 21 alunos
•	Media da Amostra - 1.7
"""
tamanho_populacao = 46
amostra = 21
media = nova_tabela['altura'].mean()
desvio_padrao = np.std(nova_tabela['altura'])
erro_padrao = (desvio_padrao / np.sqrt(amostra))
intervalo_confianca = 1.96
e = intervalo_confianca * erro_padrao
min_intervalo = media - e
max_intervalo = media + e

print(f"desvio padrão: {desvio_padrao}")
print(f"erro padrão: {erro_padrao}")
print(f"media: {media}")
print("LIMITES")
print(f"{min_intervalo} < {media} < {max_intervalo}")

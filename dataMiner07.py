import tabula
import pandas as pd

#etapa 1 <- dados do pdf

#capturando tabelas por paginas especificas
lista_tabela_dias = tabula.read_pdf("data/extracao_ipea.pdf", pages=("2", "4", "5"))

#numero de tabelas escaneadas
print(len(lista_tabela_dias))

#conteudo
for tabela in lista_tabela_dias:
    print(tabela)


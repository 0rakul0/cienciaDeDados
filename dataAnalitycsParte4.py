import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter
from scipy.optimize import linprog
from scipy.stats import norm

n = int(input("digite o numero de dias: "))
df = pd.DataFrame(dict(data=pd.date_range("2020-1-1", periods=n),
                       valor=np.abs(np.random.normal(100, 5, n))
                       ))

with pd.option_context('display.max_rows', 10):
    print(df)

retorno = (df['valor'] / df['valor'].shift(1)) - 1
retorno.dropna(inplace=True)

print("aplicando a formula")
print('-----------------------')
with pd.option_context('display.max_rows', 10):
    print(retorno)

print("graficos")
retorno.describe()
retorno.plot(title="retorno",
             xlabel="Data",
             ylabel="percentual")

fig = plt.figure()
plt.title('HISTOGRAMA dos retornos')
plt.xlabel('Retorno %')
plt.ylabel('Frequencia')
ax = fig.add_subplot(111)
ax.hist(retorno, bins=20, density=False, rwidth=0.9, color='#607c8e')
ax.yaxis.set_major_formatter(PercentFormatter(xmax=100))
plt.show()

"""var < operações de risco"""
print("Operação de rico com VAR")
nivelDeConfianca = float(input("digite o nivel de confiança, exemplo: 0.04"))
media = np.mean(retorno)
desvio_padrao = np.std(retorno)
nivel_de_confianca = nivelDeConfianca
VaR = norm.ppf(nivel_de_confianca, media, desvio_padrao)
print(VaR)

print("para corte minimo de perdas")
nivelDoVar = int(input("digite entre 90 à 100: "))
nivel_do_var = nivelDoVar
var_n = np.percentile(retorno, 100 - nivel_do_var)
print('O Var({}) é de: {}%'.format(nivel_do_var, 100 * var_n))
print('-----------------------')
print('-----------------------')
print("CVaR < estimativa esperada no pior (1-x)% de cenarios")
print("para corte minimo de perdas")
nivelDoCVar = int(input("digite entre 90 à 100: "))
nivel_do_var = nivelDoCVar
var_cn = np.percentile(retorno, 100 - nivel_do_var)
Cvar_cn = retorno[retorno <= var_cn].mean()
print('O CVar({}) é de: {}%'.format(nivel_do_var, 100 * Cvar_cn))
print('-----------------------')

"""implementação"""


def resolverPL(c, A_eq, b_eq, A_ub, b_ub):
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=(0, None))
    return res

def exemplo():
    A_ub = np.array([[-1.5, 0, -1, 0, -1, 1],
                     [0, -1.3, 0, -1, -1, 1]])
    b_ub = np.array([0, 0])
    A_eq = np.array([[1, 1, 0, 0, 0, 0]])
    b_eq = np.array([1])
    c = np.array([0, 0, 10, 1, -1])
    return c, A_eq, A_ub, b_eq, b_ub

def carregar(opcao):
    if(opcao==1):
       return exemplo()

opcao=1
[c, A_eq, b_eq, A_ub, b_ub] = carregar(opcao)
resultado=resolverPL(c, A_eq, A_ub, b_eq, b_ub)
print('-----------------------')
print("os valores de x são: ")
print("Percentual de ativo 1: {0: .4g}%".format(100 * resultado.x[0]))
print("Percentual de ativo 2: {0: .4g}%".format(100 * resultado.x[1]))
print("O VaR do portifolio é: {0: .4g}%".format(resultado.x[4] - resultado.x[5]))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import norm

n = int(input("digite o numero de dias: "))
df = pd.DataFrame(dict(data=pd.date_range("2020-1-1", periods=n),
                       valor=np.abs(np.random.normal(100, 5, n))
                       ))

with pd.option_context('display.max_rows', 10):
    print(df)

retorno = (df['valor']/df['valor'].shift(1))-1
retorno.dropna(inplace=True)

print("aplicando a formula")

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
var_n = np.percentile(retorno, 100-nivel_do_var)
print('O Var({}) é de: {}%'.format(nivel_do_var, 100*var_n))

print("CVaR < estimativa esperada no pior (1-x)% de cenarios")
print("para corte minimo de perdas")
nivelDoCVar = int(input("digite entre 90 à 100: "))
nivel_do_var = nivelDoCVar
var_cn = np.percentile(retorno, 100-nivel_do_var)
Cvar_cn = retorno[retorno <= var_cn].mean()
print('O CVar({}) é de: {}%'.format(nivel_do_var, 100*Cvar_cn))


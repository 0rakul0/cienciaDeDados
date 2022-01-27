import numpy as np
from scipy.optimize import linprog
from numpy.linalg import solve

""" etapa de funções """

def resolucaoIgualdade(c,A_eq,b_eq):
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
    return res

def exemploIgualdade01():
    A_eq = np.array([[1,1,1],[1,4,2],[3,-1,4]])
    b_eq = np.array([100, 235, 225])
    c = np.array([70, 80, 85])
    return c, A_eq, b_eq

def exemploIgualdade02():
    A_eq = np.array([[1,1,1],[1,-3,2]])
    b_eq = np.array([100, 25])
    c = np.array([1, 10, -1])
    return c, A_eq, b_eq

def carregar_intancia_igualdade(opcao):
    if(opcao==1):
       return exemploIgualdade01()
    else:
       return exemploIgualdade02()

id_instancia = int(input("digite a opçao para resolução de igualdade você tem 1 e 2: "))
[c, A_eq, b_eq] = carregar_intancia_igualdade(id_instancia)
resultado = resolucaoIgualdade(c, A_eq, b_eq)

print("Valor otimo:", resultado.fun)
print("os valores de x são: ")
nelem = len(resultado.x)
for i in range(nelem):
    print("x[", i+1,"]", resultado.x[i])

def resolverDesigualdade(c, A_ub, b_ub):
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=(0, None))
    return res

def exemploDesigualdade01():
    A_ub = np.array([[1, 1, 1], [-1, -4, -2]])
    b_ub = np.array([100, -235])
    c = np.array([70, 80, 85])
    return c, A_ub, b_ub


def exemploDesigualdade02():
    A_ub = np.array([[-1, -1, -1], [1, -3, 2]])
    b_ub = np.array([-100, 25])
    c = np.array([1, 10, -1])
    return c, A_ub, b_ub

def carregar_intancia_desigualdade(opcao):
    if(opcao==1):
       return exemploDesigualdade01()
    else:
       return exemploDesigualdade02()

id_instancia = int(input("digite a opçao para resolução de des1igualdade você tem 1 e 2: "))
[c, A_ub, b_ub] = carregar_intancia_desigualdade(id_instancia)
resultado = resolucaoIgualdade(c, A_ub, b_ub)

print("Valor otimo:", resultado.fun)
print("os valores de x são: ")
nelem = len(resultado.x)
for i in range(nelem):
    print("x[", i+1,"]", resultado.x[i])
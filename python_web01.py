# integrando o firebase ao python
import requests
import json

link = "https://python-com-firebase-4df85-default-rtdb.firebaseio.com/"
lista_raiz = ["produtos", "vendedores"]

# metodo POST
# for x in lista_raiz:
#     dados = {"nome": "valor"}
#     requisicao = requests.post(f'{link}/{x}/.json', data=json.dumps(dados))
#     print(requisicao.text)

# Criar uma venda (POST)
# dados = {'cliente': 'alon', 'preco': 150, 'produto': 'teclado'}
# requisicao = requests.post(f'{link}/Vendas/.json', data=json.dumps(dados))
# print(requisicao)
# print(requisicao.text)

# dados = {"nome": "smartphone"}
# requisicao = requests.post(f'{link}/produtos/.json', data=json.dumps(dados))
# print(requisicao.text)

# metodo para atualizar pacth
# dados = {"nome": "mouse"}
# requisicao = requests.patch(f'{link}/produtos/-MybwXMjAM42AOO8wIbd/.json', data=json.dumps(dados))
# print(requisicao.text)

# metodo get por bloco produtos
# requisicao = requests.get(f'{link}/produtos/.json')
# print(requisicao)
# dic_requisicao = requisicao.json()
# id_item = None
# for id_produto in dic_requisicao:
#     item = dic_requisicao[id_produto]['nome']
#     if item == "teclado":
#         print(id_produto)
#         id_item = id_produto

# metodo get por bloco vendedores
# requisicao = requests.get(f'{link}/vendedores/.json')
# dicio_link = requisicao.json()
# print(dicio_link)

# #metodo get para localizar o id para ser deletado
requisicao = requests.get(f'{link}/Vendas/.json')
print(requisicao)
dic_requisicao = requisicao.json()
id_alon = None
for id_venda in dic_requisicao:
    cliente = dic_requisicao[id_venda]['cliente']
    if cliente == "alon":
        print(id_venda)
        id_alon = id_venda

# # Deletar uma venda (DELETE)
requisicao = requests.delete(f'{link}/Vendas/{id_alon}/.json')
print(requisicao)
print(f"id apagado: {id_alon}")
print(requisicao.text)
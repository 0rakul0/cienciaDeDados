#minerando dados site estadão
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

#o link do arquivo está na pasta html
html_votos = "http://127.0.0.1:5500/votosDeputados2021.html"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
site = requests.get(html_votos, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

votos = []
for deputado in soup.find_all("div", attrs={"class": "custom-representative"}):
    dados_deputado = []
    #voto_deputado = deputado['data-choice']
    dados_deputado.append(deputado['data-choice'])  # voto
    #pegamos o alt pois nele temos o nome do deputado, vale lembrar que usaremos expressões regulares para pegar a informação só desejada
    resultado_nome = re.search(r'.*Federal (.*)\((.*?)–(.*?)\)', deputado.img['alt'])
    #print(resultado_nome.group(1))
    #print(resultado_nome.group(2))
    #print(resultado_nome.group(3))

    dados_deputado.append(resultado_nome.group(1))  # nome
    dados_deputado.append(resultado_nome.group(2))  # partido
    dados_deputado.append(resultado_nome.group(3))  # estado
    #link da imagem
    #img_deputado = deputado.img['src']
    dados_deputado.append(deputado.img['src'])  # link
    # agora temos uma lista de listas
    votos.append(dados_deputado)

votos_df = pd.DataFrame(votos, columns=['voto', 'dep. federal', 'partido', 'estado', 'img'])
#votos_df.to_csv('data/votos_presidente_camara.csv', index=False)

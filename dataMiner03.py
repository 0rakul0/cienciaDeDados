from urllib import response
import requests
from bs4 import BeautifulSoup
import pandas as pd


lista_noticias = []

url = 'https://g1.globo.com/'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
"""
dadas as configurações iniciais
começãmos a estração de dados do site
"""
## todos os dados da página
#print(soup) # print de todo o codigo
#print(soup.prettify()) # <- deixa estruturado

"""para uma extração eficaz em um site que não muda suas tags
usamos o inspect do navegador para setar de onde irá vir os dados"""

""" para extrair os dados de uma tag específica """
#HTML pega tudo que tem dentro dessa classe
noticias = soup.findAll('div', attrs={'class':'feed-post-body'})
# link especifico dentro do HTML
for noticia in noticias:
    """faz uma lista de informações"""
    titulo = noticia.find('a', attrs={'class': 'feed-post-link'}).getText()
    link = noticia.find('a')
    sub_titulo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})

    if(sub_titulo):
        lista_noticias.append([titulo, sub_titulo.text, link['href']])
    else:
        lista_noticias.append([titulo,'', link['href']])

"""lista com todas as noticias"""
news = pd.DataFrame(lista_noticias, columns=['titulo', 'sub titulo', 'link'])

"""exportando os dados"""
news.to_csv('noticias.csv', index=False)
news.to_excel('noticias.xlsx', index=False)

print(news)

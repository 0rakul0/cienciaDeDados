from urllib import response
import requests
from bs4 import BeautifulSoup

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
#HTML
noticia = soup.find('div', attrs={'class':'feed-post-body'})
# link especifico dentro do HTML
#print(noticia.prettify())
titulo = noticia.find('a', attrs={'class':'feed-post-link'}).getText()
#print(titulo)
sub_titulo = noticia.find('div', attrs={'class':'feed-post-body-resumo'}).getText()
#print(sub_titulo)
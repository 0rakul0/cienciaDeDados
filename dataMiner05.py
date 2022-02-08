"""
usando o selenium, vale lembrar que ele vai simular você usando o navegador.
como clicks e rolagem de mouse
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

"""importando o chromedriver caso não tenha baixar o chromedriver.exe"""
ser = Service("./chromedriver/chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

url = 'https://www.walissonsilva.com/blog'
driver.get(url)

input_busca = driver.find_element(By.TAG_NAME, 'input')

input_busca.send_keys('data')
"""o sleep tem a função de delay em segundos"""
sleep(5)
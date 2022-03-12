import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

ser = Service("./chromedriver/chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

pesquisa = ["dolar", "euro"]
criptos = {"bitcoin": "pid-1057391-last", "ethereum": "pid-1061443-last", "Bitcoin Cash": "pid-1061410-last"}

tabela_moeda = []
tabela_cotacao = []

def cotacao():
    for x in pesquisa:
        driver.get("https://www.google.com/")
        driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(
            f"cotação {x}")
        driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(
            Keys.ENTER)
        cotacao = driver.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div['
                                                '2]/span[1]').get_attribute('data-value')
        tabela_moeda.append(x)
        tabela_cotacao.append(float(cotacao))
        print(f"{x}: {cotacao}")

    for x in criptos.keys():
        url = ("https://br.investing.com/crypto/currencies")
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 97.0.4692.99 Safari/537.36"}
        site = requests.get(url, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        cotacao = soup.find("a", attrs={"class": criptos[x]}).text
        cotacao = cotacao.replace(".", "")
        cotacao = cotacao.replace(",", ".")

        tabela_moeda.append(x)
        tabela_cotacao.append(float(cotacao))
        print(f"{x}: {cotacao}")

def data():
    df = pd.DataFrame((zip(tabela_moeda, tabela_cotacao)), columns=["moeda", "valor"])
    df.to_csv('data/cotacaoValores.csv', index=False)
    print(df)

if __name__ == "__main__":
    cotacao()
    data()

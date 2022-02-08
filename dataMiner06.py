from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    """para ver o navegador 
     browser = p.chromium.launch(headless=False)
    """
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.google.com/")
    #pega o titulo da pagina
    print(page.title())
    """
    para ações temos algumas opções, basta pedir o page.
    e usar utilizar como no seletores do css  #, ., tag[atributo='identificador'] e pepois o valor
    """
    page.fill("input[name='q']", '0rakul0')
    """page.click faz a ação do mouse"""
    page.click("input[name='btnK']")
    """para por delay usamos o wait_for_timeout"""
    page.wait_for_timeout(5000)
    #fecha o navegador
    browser.close()
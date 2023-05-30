from selenium import webdriver 
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


class PageRender:

    def downloadCode(url):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=firefox_options)
        driver.get(url)
        page_source = driver.page_source
        driver.quit()
        return page_source
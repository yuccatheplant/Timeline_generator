import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def getVolcanoName():
    url = "https://www.fantasynamegenerators.com/volcano-names.php"

    driver = webdriver.Chrome('./chromedriver') 
    driver.get(url) 
    
    time.sleep(0.5)
    
    html = driver.page_source
    
    html = html.split('<div id="result">')[1]
    html = html.split('</div>')[0]
    html = html.split('<br>')[3]
    
    return html
    
def getVolcanoNameFasta():
    url = "https://www.fantasynamegenerators.com/volcano-names.php"

    driver = webdriver.Chrome('./chromedriver') 
    driver.get(url) 
    
    time.sleep(0.5)
    
    html = driver.page_source
    
    html = html.split('<div id="result">')[1]
    html = html.split('</div>')[0]
    html = html.split('<br>')[3]
    
    return html
    
    
print(getVolcanoNameFasta())
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def scrapeUrlSelenium(url):
    driver = webdriver.Chrome('./chromedriver') 
    driver.get(url) 
    
    time.sleep(1)
    
    html = str(driver.page_source)
    
    return html
#===========================================================================================================================================================================
def getVolcanoName():
    volcano = getVolcanoNames(1)
    return volcano[0]

def getVolcanoNames(number):
    count = 0
    url = "https://www.fantasynamegenerators.com/volcano-names.php"
    
    result = []
    while(count < number):
        html = scrapeUrlSelenium(url)
        count = count + 4
        html = html.split('<div id="result">')[1]
        html = html.split('</div>')[0]
        html = html.split('<br>')
        for i in range(3, 7):
            result.append(html[i])
        
    return result
#===========================================================================================================================================================================
def getRiverName():
    river = getRiverNames(1)
    return river[0]

def getRiverNames(number):
    count = 0
    url = "https://www.fantasynamegenerators.com/river-names.php"
    
    result = []
    while(count < number):
        html = scrapeUrlSelenium(url)
        count = count + 10
        html = html.split('<div id="result">')[1]
        html = html.split('</div>')[0]
        html = html.split('<br>')
        for i in range(0, 10):
            result.append(html[i])
        
    return result
    
  
    
#print(getRiverNames(10))
#print(getVolcanoName())





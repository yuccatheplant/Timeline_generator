from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random


def scrapeUrlSelenium(url):
    driver = webdriver.Chrome('./chromedriver') 
    driver.get(url) 
    driver.minimize_window()
    
    #time.sleep(5)
    
    html = str(driver.page_source)
    
    driver.close()
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
        try:
            html = html.split('<div id="result">')[1]
            html = html.split('</div>')[0]
            html = html.split('<br>')
            for i in range(3, 7):
                result.append(html[i])
        except:
            count = count - 4
        
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
        try:
            html = html.split('<div id="result">')[1]
            html = html.split('</div>')[0]
            html = html.split('<br>')
            for i in range(0, 10):
                result.append(html[i])
        except:
            count = count - 10
        print(count)
        
    return result
    
def getWaterfallNames(number):
    count = 0
    url = "https://www.fantasynamegenerators.com/waterfall-names.php"
    
    result = []
    while(count < number):
        html = scrapeUrlSelenium(url)
        count = count + 10
        try:
            html = html.split('<div id="result">')[1]
            html = html.split('</div>')[0]
            html = html.split('<br>')
            for i in range(0, 10):
                result.append(html[i])
        except:
            count = count - 10
        print(count)
        
    return result
#===========================================================================================================================================================================
def distinctNames(inputFile):
    file = open(inputFile, "r")
    lines = file.readlines()
    file.close()
    
    #file = open(inputFile+'_distinct', "w")
    file = open(inputFile, "w")
    array = []
    for line in lines:
        if not line in array:
            array.append(line)
            file.write(line)
    file.close()

def scrapeStuff(number):
    array = getWaterfallNames(number)
    filepath1 = "waterfall1.txt"
    filepath2 = "waterfall2.txt"
    
    file1 = open(filepath1, "w")
    file2 = open(filepath2, "w")
    
    for line in array:
        lineArray = line.rsplit(' ', 1)
        
        file1.write(lineArray[0]+'\n')
        file2.write(lineArray[1]+'\n')
    
    file1.close()
    file2.close()
    
    distinctNames(filepath1)
    distinctNames(filepath2)
#===========================================================================================================================================================================    
def getGeneratedName(filepaths):
    result = ''
    firstTime=True
    for filepath in filepaths:
        file = open(filepath, "r")
        lines = file.readlines()
        file.close()
        
        line = lines[random.randint(0, len(lines)-1)]
        if '\n' in line:
            line = line.split('\n')[0]
        
        if not firstTime:
            result = result + ' '
        firstTime=False
        
        result = result + line
        
        
    return result
#===========================================================================================================================================================================    


#scrapeStuff(500)
#print(getGeneratedName(['resources/generators/volcano1.txt', 'resources/generators/volcano2.txt']))






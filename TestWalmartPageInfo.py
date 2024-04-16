import requests #Gets the information
import os
from bs4 import BeautifulSoup #Parses through information
from selenium import webdriver 
import time
from selenium.common import exceptions  
from WalmartPageInfo import WalmartPageInfo


URL = 'https://www.walmart.com/ip/Sceptre-32-Class-720P-HD-LED-TV-X322BV-SR/55427159'

driver = webdriver.Chrome()
driver.get(URL)
allPages = []
try:
    allPages.append(WalmartPageInfo(driver.current_url, driver)) #Scrapes info and adds object to all pages
    driver.implicitly_wait(5) #Used so that everything has time to load
except exceptions.StaleElementReferenceException:
        print("no link")
# allPages[0].toString()

print("")
print("The specs are")
for spec in allPages[0].specifications:
    print(spec)
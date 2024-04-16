import requests #Gets the information
import os
from bs4 import BeautifulSoup #Parses through information
from selenium import webdriver 
import time
from WalmartPageInfo import WalmartPageInfo
from selenium.common import exceptions  
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from openpyxl import Workbook
from openpyxl import load_workbook
import traceback
import urllib
import re
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from ebaysdk.trading import Connection
import random

def quick(api):
    activeList = api.execute('GetMyeBaySelling', {"ActiveList": {"Include" :True} })

    soup = BeautifulSoup(activeList.content, 'lxml')

    titles = soup.find_all("title")
    ids = soup.find_all("itemid")
    itemID = ""
    getIds = []

    #Using this to get the Item ID and Store it
    for i in range(len(titles)):
        itemID = str(ids[i])
        itemID = itemID.replace("<itemid>", "")
        itemID = itemID.replace("</itemid>", "")
        getIds.append(itemID)
    print()
    print(str(len(getIds)))
    print()
    for i in range(len(titles)):
        request = {
            "ItemID": getIds[i],
            "ShippingPackageDetails":{
                "PackageDepth" :  random.randint(6,12),
                "PackageLength" :  random.randint(6,12),
                "PackageWidth" :  random.randint(6,12),
                "WeightMajor" : random.randint(5,8),
            }
        }
        print("here")
        api.execute("ReviseFixedPriceItem", {"item" : request})



########################################################   UN COMMENT DOWN   ###################################################
def removeEbay(workbook):
    app = "JustinKl-test-PRD-1e65479d5-c023ee1b"
    dev = "1823c83f-e9e2-467b-8a66-54bb1917eb6c"
    cert = "PRD-e65479d53db2-e6ec-4713-b426-9429"
    toke = "AgAAAA**AQAAAA**aAAAAA**829+Xw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6MFlYGgCpGLogudj6x9nY+seQ**F3sGAA**AAMAAA**bwfjK8RqAGZYQ30CA3UapNkqeE4InpfhlfTM8dHhAPh/bF0RUAoKKBIVGHBNhN+EMdyvLOkVugCJtlo4FREbxKLh7aSE0NcNIwLbzjLJ5N9Ln1dzfmRo6pU9+AhHvygDxIRBJAbTunirpTjps+z4TghRo/ZkvevGAsmWe0SK9+0r6Z8p728AGvd47IeM1MrvD9dFJ/aUsQNeDR9gveNseY3Y7j+Wqa6CQiBH78hQcFgdoPkyvpGOe1FnslDQ5F2vy4H79n6yyN1cgbQVRJ78362OnY17BE7wdwmZOmiIW6ZEvXf8JYBAUAPeuoEUZo8AkZ6vKrX/PxlpWGVkS4RpIIe3lPUpaXccwzdz4n58XAVzSSq4e0q5srxXiiK7kkLXJGhTRWNacDFsnlyt6AFVgJ7N01Ic5fQ+zW516tF1KRpST/Tv41gTEFaM1BmWpZQXnPH6XhJtLQw07U+8g52qDNf+0PFRPGV2aIV1zTumWawuFw3zrLXPDiti9xf+XRZGIHjlNoxir05/oxA2jBai1PiLPYOm62Rlvv2tOdinH0AznDbMlX+DKyyLxXb5I31mZN+GjyNXzygmwfBOkrXlk2UzcQv070/yWXuq9EO91i7hMxaT4K+2Mk2VxBYERs5Bvbv8gBPFn8sDDMlN/nOvyYm6QiwQdF6XkTfpfJcG44qZbXfspnlHh2rasZQ5Ygmd7eVnzQFnBj+BqnoaFNmM2NlVl6ToNdAQu0ObtUggrYKw/FjqDrpWnvlalneGVHUK"

    api = Connection(appid=app, devid=dev, certid=cert, token=toke, config_file=None, debug = True, escape_xml=True)
    activeList = api.execute('GetMyeBaySelling', {"ActiveList": {"Include" :True} })

    soup = BeautifulSoup(activeList.content, 'lxml')
    items = soup.find_all("itemid")
    sheet = workbook[workbook.sheetnames[0]]
    
    request = {
        "ItemID": sheet['B23'].value,
        "EndingReason":"NotAvailable"
    }
    print("here")
    api.execute("EndFixedPriceItem", request)
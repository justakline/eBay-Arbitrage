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
import math
import random


def getGalleryURL(sheet):
    for link in sheet['D']:
        if(link.value == None):
            pass
        else:  
            l = (((link.value).replace("&", "&amp;")).strip())
            ((l.replace("<", "&lt;")).replace(">", "&gt;"))
            ((l.replace("'", "&apos;")).replace('"', "&quot;"))
            if ("jpeg" in l):
                l = (l.split("jpeg")[0]) + "jpeg"
            if ("png" in l):
                l = (l.split("png")[0]) + "png"
            return l

    return None

def getPicturesURL(sheet):
    links = []
    
    

    #Getting the links, and because this python gets transformed int XML,
    #I am getting rid of the special charaachters. I also take off the ending of the link
    #Because the link merely gets me to the webpage... So taking off the ending 
    #Gets me to the image itself
    for link in sheet['D']:
        if(link.value == None):
            pass
        else:  
            l = (((link.value).replace("&", "&amp;")).strip())
            ((l.replace("<", "&lt;")).replace(">", "&gt;"))
            ((l.replace("'", "&apos;")).replace('"', "&quot;"))
            if ("jpeg" in l):
                l = (l.split("jpeg")[0]) + "jpeg"
            if ("png" in l):
                l = (l.split("png")[0]) + "png"

            links.append(l)
        if(len(links) >= 11):
            break
    return links


def getSpecifics(sheet):

    print("in specs")
    smartTVFeatures = []
    for row in sheet['H']:
        if(row == None):
            break
        else:
            smartTVFeatures.append(getGoodXMLString(row.value))
    audioVideo = []
    for row in sheet['J']:
        if(row == None):
            break
        else:
            audioVideo.append(getGoodXMLString(row.value))


    return {
        
        "NameValueList": [
            {"Name" : "Smart TV Features" , "Value": smartTVFeatures},
            {"Name":"Audio/Video Inputs", "Value" : audioVideo},#Takes a dict like {HDMI, USB}
            {"Name" : "Display Technology", "Value" : getGoodXMLString(sheet['B10'].value)  },
            {"Name" : "Model", "Value" : getGoodXMLString(sheet['B7'].value)  },
            {"Name" :"Maximum Resolution" ,"Value" : sheet['B8'].value  },
            {"Name" :"Screen Size" ,"Value" : getGoodXMLString(sheet["B9"].value ) },
            {"Name" :"Refresh Rate" ,"Value" : getGoodXMLString(sheet['B11'].value)  },
            {"Name" : "Brand", "Value" : getGoodXMLString(sheet['B6'].value)  },
        ]
    }
def getPrice(sheet):
    B15 = float(sheet['B15'].value)
    return str( math.ceil(1.3* B15) - 0.01)

def getGoodXMLString(str):
    if(str is None):
        return None
    str = (((str).replace("&", "&amp;")).strip())
    ((str.replace("<", "&lt;")).replace(">", "&gt;"))
    ((str.replace("'", "&apos;")).replace('"', "&quot;"))
    return str


########################################################   UN COMMENT DOWN   ###################################################
def addEbay(workbook):
    app = "JustinKl-test-PRD-1e65479d5-c023ee1b"
    dev = "1823c83f-e9e2-467b-8a66-54bb1917eb6c"
    cert = "PRD-e65479d53db2-e6ec-4713-b426-9429"
    toke = "AgAAAA**AQAAAA**aAAAAA**829+Xw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6MFlYGgCpGLogudj6x9nY+seQ**F3sGAA**AAMAAA**bwfjK8RqAGZYQ30CA3UapNkqeE4InpfhlfTM8dHhAPh/bF0RUAoKKBIVGHBNhN+EMdyvLOkVugCJtlo4FREbxKLh7aSE0NcNIwLbzjLJ5N9Ln1dzfmRo6pU9+AhHvygDxIRBJAbTunirpTjps+z4TghRo/ZkvevGAsmWe0SK9+0r6Z8p728AGvd47IeM1MrvD9dFJ/aUsQNeDR9gveNseY3Y7j+Wqa6CQiBH78hQcFgdoPkyvpGOe1FnslDQ5F2vy4H79n6yyN1cgbQVRJ78362OnY17BE7wdwmZOmiIW6ZEvXf8JYBAUAPeuoEUZo8AkZ6vKrX/PxlpWGVkS4RpIIe3lPUpaXccwzdz4n58XAVzSSq4e0q5srxXiiK7kkLXJGhTRWNacDFsnlyt6AFVgJ7N01Ic5fQ+zW516tF1KRpST/Tv41gTEFaM1BmWpZQXnPH6XhJtLQw07U+8g52qDNf+0PFRPGV2aIV1zTumWawuFw3zrLXPDiti9xf+XRZGIHjlNoxir05/oxA2jBai1PiLPYOm62Rlvv2tOdinH0AznDbMlX+DKyyLxXb5I31mZN+GjyNXzygmwfBOkrXlk2UzcQv070/yWXuq9EO91i7hMxaT4K+2Mk2VxBYERs5Bvbv8gBPFn8sDDMlN/nOvyYm6QiwQdF6XkTfpfJcG44qZbXfspnlHh2rasZQ5Ygmd7eVnzQFnBj+BqnoaFNmM2NlVl6ToNdAQu0ObtUggrYKw/FjqDrpWnvlalneGVHUK"

    api = Connection(appid=app, devid=dev, certid=cert, token=toke, config_file=None, debug = True, escape_xml=True)
    activeList = api.execute('GetMyeBaySelling', {"ActiveList": {"Include" :True} })

    soup = BeautifulSoup(activeList.content, 'lxml')
    items = soup.find_all("item")
    sheet = workbook[workbook.sheetnames[0]]
    if(not (sheet['B16'].value is None)):
        if("." in sheet['B16'].value ):
            major = ((sheet['B16'].value).split("."))[0]
        else:
            major = (sheet['B16'].value).split(" ")[0]
        major =getGoodXMLString(major)
    else:
        major = 0
    request = {
        "Item": {
            "Title": getGoodXMLString(sheet['B3'].value),
            "SKU": getGoodXMLString(sheet['B23'].value),
            "Country": "US",
            "Location": "US",
            "Site": "US",
            "ConditionID": "1000",
            "PaymentMethods": "PayPal",
            "PayPalEmailAddress": "justakline@gmail.com",
            "AutoPay" : True,
            "PrimaryCategory": {"CategoryID": "11071"}, #the number means tv
            "Description": getGoodXMLString(sheet['B14'].value),
            "ItemSpecifics":getSpecifics(sheet),
            "PictureDetails": {
                "GalleryURL" : getGalleryURL(sheet),
                'PictureURL': getPicturesURL(sheet)
            },
            "ListingDuration": "GTC",
            "StartPrice": getGoodXMLString(getPrice(sheet)),
            "Currency": "USD",
            "ShippingPackageDetails":{
                "PackageDepth" :  sheet["B17"].value,
                "PackageLength" :  sheet["B18"].value,
                "PackageWidth" :  sheet["B19"].value,
                "WeightMajor" : major,
                "WeightMinor" : "0"
            },
            "ReturnPolicy": {
                "ReturnsAcceptedOption": "ReturnsAccepted",
                "RefundOption": "MoneyBack",
                "ReturnsWithinOption": "Days_30",
                "Description": "If you are not satisfied, please return the tv",
                "ShippingCostPaidByOption": "Buyer"
            },
            "ShippingDetails": {
                "ShippingType": "Calculated",
                "CalculatedShippingRate" : {
                    "OriginatingPostalCode" : "21153",
                    "MeasurementUnit" : "English"
                },
                "ShippingServiceOptions": {
                    "ShippingServicePriority": "1",
                    "ShippingService": "USPSPriority",
                }
            },
            "DispatchTimeMax": "5"
        }
    }
    api.execute("AddFixedPriceItem", request)
    

    activeList = api.execute('GetMyeBaySelling', {"ActiveList": {"Include" :True} })

    soup = BeautifulSoup(activeList.content, 'lxml')
    
    titles = soup.find_all("title")
    ids = soup.find_all("itemid")
    itemID = ""

    #Using this to get the Item ID and Store it
    for i in range(len(titles)):
        tit = str(titles[i]) + ""
        tit = tit.replace("<title>", "")
        tit = tit.replace("</title>", "")
        tit = (tit).replace("&amp;", "&")
        tit = (((tit.replace("&lt;", "<")).replace("&gt;", ">")).replace("&apos;", "'")).replace('&quot;', '"')
        
        if(tit == sheet['B3'].value):
            itemID = str(ids[i])
            itemID = itemID.replace("<itemid>", "")
            itemID = itemID.replace("</itemid>", "")
            break
    sheet['B23'] = itemID
    workbook.save(filename = "item.xlsx")
    workbook.save(filename = "eBay.xlsx")
    


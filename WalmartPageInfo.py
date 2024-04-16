import requests #Gets the information
import os
from bs4 import BeautifulSoup #Parses through information
from selenium import webdriver 
import time
from selenium.common import exceptions  
import traceback
import math

class WalmartPageInfo:
    def __init__(self, URL, driver):
        self.URL = URL
        self.driver = driver
        self.driver.implicitly_wait(2)
        self.title = ""
        self.price = ""
        self.outOfStock = ""
        self.body = ""
        self.specifications = {}
        self.pictures = []
        self.everything = []
        self.everything.append(self.URL)
        try :
            self.title = self.driver.find_element_by_tag_name('h1').text
            if (len(self.title) > 79):
                self.title = (self.title)[0,80]
            self.body = self.driver.find_element_by_id('about-product-section').text
            self.everything.append(self.title)
            self.everything.append(self.body)
        except:
             exceptions.NoSuchElementException
        try: #If the item is out of stock, then I wont bother putting in the price, thereby in everything it wont be there
            self.outOfStock = self.driver.find_element_by_class_name('display-block-xs').text
            # self.price = "Out of Stock" 
            print("outOfStock")
            self.price = 0
            self.everything.append(self.price)
        except:
            exceptions.NoSuchElementException
            self.outOfStock = "In Stock"
            self.price = self.driver.find_element_by_class_name('price-characteristic').text
            self.everything.append(self.price)
        if(self.outOfStock == "In Stock"):
            try :
                self.getPictures()
                self.everything.append(self.pictures)
            except: 
                exceptions.NoSuchElementException
                print("No pictures")
                print(self.URL)
                print(traceback.format_exc())
            self.totalCosts = "=1.219*B15"
            self.sellPrice = "=ROUNDUP((1.3*B15), 0)-0.01"
            self.totalProfits = "= B20 - B21"

            self.everything.append(self.sellPrice)
            self.everything.append(self.totalCosts)
            self.everything.append(self.totalProfits)
            try :
                self.getSpecifications()
                self.everything.append(self.specifications)
            except: 
                exceptions.NoSuchElementException
                print("No specifications")
                print(self.URL)
                print(traceback.format_exc())
            self.goodShipping = self.isGoodShipping()
        print("done creating")

    def isGoodShipping(self):
        box = self.driver.find_element_by_class_name("fulfillment-buy-box-update")
        box = box.find_elements_by_class_name("prod-fulfillment")
        temp = []
        pickupAndDelivery = []
        for thing in box:
            pick = thing.find_element_by_class_name("prod-fulfillment-messaging-text").text
            if("Free delivery" in pick):
                return True
        return False

    def toString(self):
        if (hasattr(self, 'title')):
            print("title = " + self.title)
        if (hasattr(self, 'body')):
            print ("body = " + self.body)
        if (hasattr(self, 'price')):
            print("price = $" + self.price)
        for pic in self.pictures:
            print (pic)
        for general, specific in self.specifications.items():
            print (general , specific)
        


    def getPictures(self):
        sliders = self.driver.find_elements_by_class_name("slider-list")
        toucher = sliders[0].find_elements_by_tag_name("li")
        buttons = []# This is the list of small icons on the side of the big picture, used for changing the big picture to the icon

        for touch in toucher:
            buttons += touch.find_elements_by_tag_name("button")
        arrowButton = self.getArrowButton()# Used to be able to access all of the buttons 

        heroImages = self.driver.find_elements_by_class_name("prod-hero-image")
        imgs = heroImages[0].find_elements_by_tag_name("img")

        i = 0
        for button in buttons:
            try: #try to get the link, if cant, then "Refresh the page"
                link = "https:" +(imgs[0].get_attribute('srcset').split(',')[1])[1:]
                link.strip()
                self.pictures.append(link)#get the link
            except:
                exceptions.StaleElementReferenceException
                heroImages = self.driver.find_elements_by_class_name("prod-hero-image")
                imgs = heroImages[0].find_elements_by_tag_name("img")
            try :
                button.click()#click on a new button
            except:
                exceptions.ElementNotInteractableException# if there is no clickable button, click the arrow button and try the button again
                arrowButton = self.getArrowButton()
                arrowButton[0].click()

    def getArrowButton(self):
        nextImage = self.driver.find_elements_by_class_name("slider-decorator-1")
        return nextImage[0].find_elements_by_tag_name("button")

    def getSpecifications(self):
        specsPage = self.driver.find_element_by_class_name("product-specifications")
        specsTable = specsPage.find_element_by_tag_name("table")
        specRows = specsTable.find_elements_by_tag_name("tr")
        specs = []

        for row in specRows:# Row.find... gives back a list of 2, first being the type, second being the specific
            specs.append(row.find_elements_by_tag_name("td"))
        i = 0
        while (i < len(specs)):
            self.specifications[specs[i][0].text] = specs[i][1].text
            i+=1

#Originally used to get all aspects of each page,
#But is now used to see if there were any errors
#In getting any aspect of the page, ie if the
#specifications ran into an error
    def getEverything(self):
        return self.everything

    def ebayRepresentation(self):
        all = []
        all.append(self.URL)
        all.append(self.title)
        all.append("New")
        all.append(self.outOfStock)
        all.append(self.specifications.get("Brand"))
        all.append(self.specifications.get("Model"))
        all.append(self.specifications.get("Maximum Resolution"))
        all.append(self.specifications.get("Screen Size"))
        all.append(self.specifications.get("Display Technology"))
        all.append(self.specifications.get("Refresh Rate"))
        all.append("")
        all.append("")
        all.append(self.body)
        all.append(self.price)
        all.append(self.specifications.get("Assembled Product Weight"))
        try:
            dimensions = self.specifications.get("Assembled Product Dimensions (L x W x H)")
            dimensions = dimensions.replace('x ', "")
            dimensions = dimensions.replace('Inches', "")
            dimensions = dimensions.split(" ")

            all.append(dimensions[0])#Length
            all.append(dimensions[1])#Width
            all.append(dimensions[2])#Height
            all.append(self.sellPrice)
            all.append(self.totalCosts)
            all.append(self.totalProfits)
        except:
            all.append("")
            all.append("")
            all.append("")

        all.append(self.pictures)
        try:
            all.append(self.specifications.get("Streaming Services").split(';'))
            all.append(self.specifications.get("Connector Type").split(";"))
        except AttributeError:
            all.append("")
            all.append("")
        return all
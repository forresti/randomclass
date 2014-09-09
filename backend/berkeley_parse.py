# sudo pip install -U selenium    #worked out of the box.
from bs4 import BeautifulSoup
import os
import math
from IPython import embed
import datetime
import urllib2
from pymongo import MongoClient
from carInventoryDB import insert_or_update_car #may need to symlink carInventoryDB

def getPage(pageUrl):
    return urllib2.urlopen(pageUrl).read()

def getNumPages(soup):
    header = soup.find('div', {'id':'resultsHeader'})    
    totalCars = header.find('h1').contents[0] # e.g. "43,107 cars found"
    totalCars = totalCars.split(' ')[0] # 43,107 cars found -> 43,107
    totalCars = int( totalCars.replace(',', '') ) # 43,107 -> 43107
    numPages = int( math.ceil(totalCars/50.0) ) # 50 cars per page in typical CarMax UI 
    return numPages

#@param soup = one page of search results
#@return list of HTML snippets -- one per car
def parseCars(soup):
    cars = soup.find_all('div', {'class':'car'})
    return cars

#@param carSoup = page snippet for one car 
#@return dictionary of this car's attributes 
def parseOneCar(carSoup):
    carDict = dict()
    carDict['stockNum'] = carSoup.get('sn')
    carDict['uniqueID'] = carDict['stockNum']
    carDict['url'] = 'http://www.carmax.com' + carSoup.get('data-details-url').split(' ')[0]
    carDict['makeModelYear'] = carSoup.find('div', {'class':'col_b'}).find('h1').contents[0]
    carDict['price'] = carSoup.find('div', {'class':'price'}).find_all('div')[1].contents[0].replace('*','')
    carDict['location'] = carSoup.find('div', {'class':'transfer'}).find('div', {'class':'section'}).find_all('div')[1].contents[0].strip() 
    carDict['dateTime'] = datetime.datetime.utcnow()
    #TODO: include miles on odometer
    return carDict

#initialization
pageUrl = 'http://www.carmax.com/search?ASc=8&PP=50&D=90&zip=98465&Q=ab336040-41ed-4684-bcbe-2b87971cf32c&Ep=search:results:results%20page'
page = getPage(pageUrl)
soup = BeautifulSoup(page)
numPages = getNumPages(soup)
print "found %d pages" %numPages
client = MongoClient()
db = client.carmax_inventory

carDicts = []
for pageIdx in xrange(0, numPages):
    pageUrl = 'http://www.carmax.com/search?ASc=8&PP=50&No=%d&D=90&zip=98465&Q=ab336040-41ed-4684-bcbe-2b87971cf32c&Ep=search:results:results%%20page' %(pageIdx*50) #50 cars per page
    page = getPage(pageUrl)  
    soup = BeautifulSoup(page) 
    cars = parseCars(soup)

    for c in cars:
        carDict = parseOneCar(c)
        carDicts.append(carDict)
        insert_or_update_car(db, carDict)
        #print carDict

    print "** FINISHED PARSING PAGE %d **" %pageIdx

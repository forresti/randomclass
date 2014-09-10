# sudo pip install -U selenium    #worked out of the box.
from bs4 import BeautifulSoup
import os
import math
from IPython import embed
import datetime
import urllib2
import json
from pymongo import MongoClient
from classDB import insert_or_update_class #may need to symlink classDB

def getPage(pageUrl):
    return urllib2.urlopen(pageUrl).read()

#for classNum in xrange(1, 1000):
for classNum in xrange(147, 148):
    url = 'https://apis-dev.berkeley.edu/cxf/asws/classoffering?classNumber=%d&_type=json&app_id=cfd7218b&app_key=66dc1dffbbff5cc9f9b6037d7608e070' %classNum
    page = getPage(url) 
    classes = json.loads(page)


    print [x['courseTitle'] for x in classes]


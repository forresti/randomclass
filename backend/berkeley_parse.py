# sudo pip install -U selenium    #worked out of the box.
from bs4 import BeautifulSoup
import os
import math
from IPython import embed
import datetime
import urllib2
import json
import random
from pymongo import MongoClient
from classDB import insert_or_update_class #may need to symlink classDB

def getPage(pageUrl):
    return urllib2.urlopen(pageUrl).read()
'''
#for classNum in xrange(1, 1000):
for classNum in xrange(147, 148):
    url = 'https://apis-dev.berkeley.edu/cxf/asws/classoffering?classNumber=%d&_type=json&app_id=cfd7218b&app_key=66dc1dffbbff5cc9f9b6037d7608e070' %classNum
    page = getPage(url) 
    classes = json.loads(page)
'''


def loadAllClasses():
    #downloaded from Berkeley class API:
    fname = 'classoffering?classNumber=1&_type=json&app_id=cfd7218b&app_key=66dc1dffbbff5cc9f9b6037d7608e070'
    json_data = open(fname)
    classes = json.load(json_data)
    classes = classes['ClassOffering']
    json_data.close()
    return classes

#prune away classes that might not be good for drop-ins
#start with 141k classes (as of FA14), prune down...
def primary_lec_only(classes):

    #some classes have wierd stuff in 'sections' ... 134k out of 141k classes pass the following test.
    classes_pri = [c for c in classes if  type(c['sections']) == type(dict()) ]

    #all classes in classes_pri should survive this test:
    classes_pri2 = [c for c in classes_pri if 'sectionType' in c['sections'].keys()]

    #prune 134k classes down to 102k (mainly lectures now)
    classes_pri3 = [c for c in classes_pri2 if c['sections']['sectionType']=='PRIMARY']
    # it looks like sectionType:'SECONDARY' typically corresponds with sectionFormat:DIS (discussion)

    #TODO: perhaps tweak the original Berkeley API query to request Fall.
    classes_fall = [c for c in classes_pri3 if 'Fall' in c['classUID']]

    #just for fun... all classes DO have 'Summer' or 'Spring' or 'Fall' in classUID.
    #classes_noseason = [c for c in classes_pri3 if 'Fall' not in c['classUID'] and 'Summer' not in c['classUID'] and 'Spring' not in c['classUID']]

    return classes_fall

'''
possible blacklist

courseTitle:
Special Study, Special Topics, Independent Study, (Research?), Directed Study
Group Studies, Group Research

sections: sectionMeetings: building: 'NO FACILITY'
'''

#prune away classes w/ blacklist words (e.g. Independent Study)
def blacklist_classes(classes):

    #before pruning: 25k classes, if input is from primary_lec_only()

    #21k classes
    classes2 = [c for c in classes if 'sectionMeetings' in c['sections'].keys() and type(c['sections']['sectionMeetings']) == type(dict())]
    
    #21k classes
    classes3 = [c for c in classes2 if 'building' in c['sections']['sectionMeetings'].keys()]

    #9k classes
    classes4 = [c for c in classes3 if c['sections']['sectionMeetings']['building'] != 'NO FACILITY']

    #9k classes (~25 fewer classes than classes4)
    classes5 = [c for c in classes4 if 'courseTitle' in c.keys()]

    #7.6k classes
    classes6 = [c for c in classes5 if 'Independent' not in c['courseTitle'] and 'Special' not in c['courseTitle'] and 'Directed' not in c['courseTitle']]

    return classes6

def parse_classes():
    classes = loadAllClasses()
    classes = primary_lec_only(classes)    
    classes = blacklist_classes(classes)
    return classes

classes = parse_classes()
#get random class:
#random.choice(classes)

with open('berkeley_fa14_pruned.json', 'w') as outfile:
    json.dump(classes, outfile)


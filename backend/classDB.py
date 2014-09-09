# we use these functions across various class data sources.

from pymongo import MongoClient

def insert_or_update_class(db, classDict):
    #TODO: assert that classDict has 'uniqueID' and 'dateTime'

    uniqueID = classDict['uniqueID'] #typically VIN, but not always.
    existingCar = db.classes.find_one({'uniqueID':uniqueID})

    if existingCar is  None: #if class is not yet in DB
        classDict['history'] = [classDict['dateTime']] #beginning of 'history' vector
        classDict.pop('dateTime') #dateTime is now rolled into history
        db.classes.insert(classDict)

    else: #class is already in db
        existingCar['url'] = classDict['url'] #TODO: remove (bandaid to handle old data that didnt include url)
        existingCar['history'].append(classDict['dateTime']) 
        #TODO: perhaps add incentivized price to history?

        db.classes.save(existingCar)    

def get_classes(db):
    return [x for x in db.classes.find()]


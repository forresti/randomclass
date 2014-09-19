import json
from pymongo import MongoClient

classes_fname = 'berkeley_fa14_pruned.json'
json_data = open(classes_fname)
classes = json.load(json_data)

client = MongoClient()
db = client.berkeley_classes
for c in classes:
    existingClass = db.classList.find_one({'courseUID':c['courseUID']})
    if existingClass is None:
        db.classList.insert(c)



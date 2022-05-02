import pymongo
import re
import json

'''
Run this AFTER cleaning up the data files and inserting
business and user datasets in the database
'''

# MongoDB Querying
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["yelpdata"]

# Reviews need to grab user's names and update them

# Embedding the check-in data
# db.business.update({"business_id": BUSINESS_ID}, {$set: CHECK-IN-FIELD})
mydb = myclient["test"]
mycol = mydb["business"]
checkin_ptr = open("cleaned_checkin.txt", "r")
bus_id = checkin_ptr.readline()
checkin_field = checkin_ptr.readline()
while(len(bus_id) > 0 and len(checkin_field) > 0):
    filter = {"business_id" : bus_id}
    new_val = json.loads(checkin_field)
    mycol.update_one(filter, new_val)


'''
Embedding reviews
for each business_id
	insert review into review array
	//db.data.updateOne({}, {})

Embedding check-ins
for each business_id
	insert array of check-ins
	
Embedding tips
for each BLANK_id
	insert array of tip objects
'''
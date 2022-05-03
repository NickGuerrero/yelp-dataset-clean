import pymongo
import re
import json

'''
Run this AFTER cleaning up the data files and inserting
business and user datasets in the database
'''

# Change according to what parts to need to run
# We're starting with the checkin queries
flags = [False, False, True]

# MongoDB Querying
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["yelpdata"]

# We'll do the same for tips
# Reviews need to grab user's names and update them
# Tips do the same thing
mydb = myclient["test"]
review_col = mydb["review"]
business_col = mydb["business"]
user_col = mydb["user"]
tips_col = mydb["tips"]

# Go to tips and fetch business_id and user_id
if flags[0]:
    for doc in tips_col.find():
        try:
            bus_name = business_col.find({"business_id": doc["business_id"]}, {"name": 1})["name"]
            use_name = user_col.find({"user_id": doc["user_id"]}, {"name": 1})["name"]
            tips_col.update_one({"_id": doc["_id"]}, {"$set": {"business_name": bus_name, "user_name": use_name}})
        except:
            print("bad query on tips")
    print("Finished updating tips")

# Update review
if flags[1]:
    for doc in review_col.find():
        try:
            bus_name = business_col.find({"business_id": doc["business_id"]}, {"name": 1})["name"]
            use_name = user_col.find({"user_id": doc["user_id"]}, {"name": 1})["name"]
            review_col.update_one({"_id": doc["_id"]}, {"$set": {"business_name": bus_name, "user_name": use_name}})
        except:
            print("bad query on review")
    print("Finished updating reviews")


# Embedding the check-in data
# db.business.update({"business_id": BUSINESS_ID}, {$set: CHECK-IN-FIELD})
if flags[2]:
    mydb = myclient["test"]
    mycol = mydb["business"]
    checkin_ptr = open("cleaned_checkin.txt", "r")
    bus_id = checkin_ptr.readline()
    checkin_field = checkin_ptr.readline()
    while(len(bus_id) > 0 and len(checkin_field) > 0):
        print(bus_id)
        filter = {"business_id" : bus_id}
        new_val = json.loads(checkin_field)
        content = {"$set": new_val}
        print(content)
        mycol.update_one(filter, content)
        bus_id = checkin_ptr.readline()
        if len(bus_id) > 0:
            checkin_field = checkin_ptr.readline()
        else:
            checkin_field = ""
        

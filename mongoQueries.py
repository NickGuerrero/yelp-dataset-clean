import pymongo
import re

'''
Run this AFTER cleaning up the data files and inserting
business and user datasets in the database
'''

# MongoDB Querying
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["yelpdata"]

# Embedding reviews
# review_file = OPEN THE REVIEW FILE
# EACH DOCUMENT SHOULD BE ON A NEW LINE



# Embedding user data

'''
Convert check-in from string of dates to array of date objects
{ "business_id": "STRING", "date": "STRING" }

Associated with each business id
"business_id"&&&&"check-in": [ {$date": "formatted"} , ... ]

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

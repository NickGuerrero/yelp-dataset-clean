import sys
import re
#import yelpConversion
'''
Convert two fields in a GeoJson object, replace fields
longitude: 213.4
latitude: 1213.1
location: {type: "Point", coordinates: [LO, LA] }
'''
def convertGeo(latString, longString):
    return '"location": {"type": "Point", "coordinates": [' + longString + ',' + latString +']}'

def geoRepl(matchobj):
    print(matchobj.group(0))
    print(matchobj.group(1))
    print(matchobj.group(2))
    return convertGeo(matchobj.group(1), matchobj.group(2))

def replaceGeo(text):
    return re.sub('"latitude"\s*:\s*(.*?)\s*,\s*"longitude"\s*:\s*(.*?),', geoRepl, text)

# DOCUMENT = re.sub('"latitude"\s*:\s*(.*?)\s*,\s*"longitude"\s*:\s*(.*?),', geoRepl, DOCUMENT)

'''
Split a string into a string of categories
categories: [...]
'''
def convertCategories(categoryString):
    tmp = re.sub('"categories":\s*|\s*|"', '', categoryString)
    tmp = tmp.split(",")
    for i in range(len(tmp)):
        tmp[i] = '"' + tmp[i] + '"'
    out = ",".join(tmp)
    return '"categories": [' + out + ']'

def catRepl(matchobj):
    return convertCategories(matchobj.group(0))

def replaceCategories(text):
    return re.sub('"categories"\s*:\s*"(.*?)"', catRepl, text)

# DOCUMENT = re.sub('"categories"\s*:\s*"(.*?)"', catRepl, DOCUMENT)

file_loc = sys.argv[1]  # yelp_academic_dataset_business.json
with open(file_loc, "r") as source:
    dest = open("cleaned_business.json", "w")
    for line in source:
        text = replaceCategories(replaceGeo(line))
        dest.write(text)
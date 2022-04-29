import re

# Share with the ec2 instance
# https://technoracle.com/copy-files-between-ec2-instances-easily/

# Testing the regex pipeline
DOCUMENT = ""

'''
Convert two fields in a GeoJson object, replace fields
longitude: 213.4
latitude: 1213.1
location: {type: "Point", coordinates: [LO, LA] }
'''
def convertGeo(latString, longString):
    return '"location": {"type": "Point", "coordinates": [' + longString + ',' + latString +']},'

def geoRepl(matchobj):
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

'''
Review date, yelping since
Convert date function:
"date": "2018-07-07 22:09:11" =>
"date": {$date: "2018-07-07T22:09:11"}
'''
def convertDate(dateString):
    ds = re.sub("\s", "T", dateString)
    return '{"$date": ' + ds + '}' # Note that the original string already has the " marks

def dateRepl(matchobj):
    return convertDate(matchobj.group(0))
    
def replaceDate(text):
    return re.sub('"[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"', dateRepl, text)

# In the document
# DOCUMENT = re.sub('"[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"', dateRepl, DOCUMENT)

'''
Special date transform, only use on the check-in json
'''
def convertDateSpecial(dateString):
    tmp = re.sub('\s', 'T', dateString)
    return '{"$date": "' + tmp + '"}'

def dateSPRepl(matchobj):
    return convertDateSpecial(matchobj.group(0))

def convertDateList(dateListString):
    ds = re.sub('[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9]', dateSPRepl, dateListString)
    return '"date": [' + ds + ']'

def dateLRepl(matchobj):
    return convertDateList(matchobj.group(1))

def replaceDateList(text):
    return re.sub('"date"\s*:\s*"(.*?)"', dateLRepl, DOCUMENT)

# In the document
# DOCUMENT = re.sub('"date"\s*:\s*"(.*?)"', dateLRepl, DOCUMENT)


# print(DOCUMENT)
# MongoDB tasks
'''
Convert check-in from string of dates to array of date objects
{ "business_id": "STRING", "date": "STRING" }

Associated with each business id
"business_id"&&&&"check-in": [ {$date": "formatted"} , ... ]
'''

'''
Link friends data across application
'''
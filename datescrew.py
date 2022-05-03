import sys
# import yelpConversion
import re

# We may need to change the friends field
# User & Review

'''
Review date, yelping since
Convert date function:
"date": "2018-07-07 22:09:11" =>
"date": {$date: "2018-07-07T22:09:11"}
'''
def convertDate(dateString):
    # Remove back " and insert Z"
    ds = dateString[:-1]
    return ds + 'Z"' # Note that the original string already has the " marks

def dateRepl(matchobj):
    return convertDate(matchobj.group(0))

def replaceDate(text):
    #return re.sub('"[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"', dateRepl, text)
    return re.sub('{\s*"$date"\s*:\s*"[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"', dateRepl, text)

file_loc = sys.argv[1]  # yelp_academic_dataset_tip.json
file_to = sys.argv[2] # cleaned_*.json
with open(file_loc, "r") as source:
    dest = open(file_to, "w")
    for line in source:
        text = replaceDate(line)
        dest.write(text)
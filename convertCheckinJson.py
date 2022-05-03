import sys
import re
# import yelpConversion

# User & Review

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
    return re.sub('"date"\s*:\s*"(.*?)"', dateLRepl, text)

'''
Convert to special string for update script
'''

def gridRepl(matchobj):
    return '"' + matchobj.group(1) + '"\n{"check-in": [' + matchobj.group(2) + ']}'

def replaceGrid(text):
    # group1 is the business_id, group2 is the array
    return re.sub('\s*{\s*"business_id"\s*:\s*"(.*?)"\s*,\s*"date"\s*:\s*\[(.*?)\]\s*}', gridRepl, text)

'''
{
  "business_id": "---kPU91CF4Lq2-WlRu9Lw",
  "date": "2020-03-13 21:10:56, 2020-06-02 22:18:06, 2020-07-24 22:42:27, 2020-10-24 21:36:13, 2020-12-09 21:23:33, 2021-01-20 17:34:57, 2021-04-30 21:02:03, 2021-05-25 21:16:54, 2021-08-06 21:08:08, 2021-10-02 15:15:42, 2021-11-11 16:23:50"
}
TO (kinda)
{
  "business_id": "---kPU91CF4Lq2-WlRu9Lw",
  "date": ["2020-03-13 21:10:56", "2020-06-02 22:18:06", "2020-07-24 22:42:27", "2020-10-24", "21:36:13", "2020-12-09 21:23:33", "2021-01-20 17:34:57", "2021-04-30 21:02:03", "2021-05-25 21:16:54", 2021-08-06 21:08:08, 2021-10-02 15:15:42, 2021-11-11 16:23:50"
}
TO
"BUSINESS_ID"
{"check-in": ["...", "..."]}

db.business.update({"business_id": BUSINESS_ID}, {$set: VAL2})
'''

file_loc = sys.argv[1]  # yelp_academic_dataset_checkin.json
file_to = sys.argv[2] # cleaned_checkin.txt
with open(file_loc, "r") as source:
    dest = open(file_to, "w")
    for line in source:
        text = replaceDateList(line)
        text = replaceGrid(line)
        dest.write(text)
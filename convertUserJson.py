import sys
# import yelpConversion

# We may need to change the friends field
# User & Review

#######################################
'''
Special date transform, only use on the check-in json
'''
def convertFriendList(friendListString):
    tmp = friendListString.split(",")
    for i in range(len(tmp)):
        tmp[i] = tmp[i].strip()
    return '"friends": ["' + '","'.join(tmp) + '"]'

def dateFriendRepl(matchobj):
    return convertFriendList(matchobj.group(1))

def replaceFriendList(text):
    return re.sub('"friends"\s*:\s*"(.*?)"', dateFriendRepl, DOCUMENT)

# We may need to change the friends field
# Friends need to be changed from string to array of strings
# User & Review

'''
{
  "user_id": "qVc8ODYU5SZjKXVBgXdI7w",
  "name": "Walker",
  "review_count": 585,
  "yelping_since": "2007-01-25 16:47:26",
  "useful": 7217,
  "funny": 1259,
  "cool": 5994,
  "elite": "2007",
  "friends": ["---", "---", "---", "---"]
}
'''

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

file_loc = sys.argv[1]  # yelp_academic_dataset_user.json
file_to = sys.argv[2] # cleaned_*.json
with open(file_loc, "r") as source:
    dest = open(file_to, "w")
    for line in source:
        text = replaceFriendList(replaceDate(line))
        dest.write(text)
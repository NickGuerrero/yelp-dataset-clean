import sys
import yelpConversion

# We may need to change the friends field
# User & Review

file_loc = sys.argv[1]  # yelp_academic_dataset_user.json
file_to = sys.argv[2] # cleaned_*.json
with open(file_loc, "r") as source:
    dest = open(file_to, "w")
    for line in source:
        text = replaceDate(line)
        dest.write(text)
import sys
import yelpConversion

file_loc = sys.argv[1]  # yelp_academic_dataset_business.json
with open(file_loc, "r") as source:
    dest = open("cleaned_business.json", "w")
    for line in source:
        text = replaceCategories(replaceGeo(line))
        dest.write(text)
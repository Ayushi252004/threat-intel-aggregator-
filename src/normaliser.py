#connection loader.py and parser.py
from loader import load_all_feeds
from parser import detect_type
def normalize_entry(entry,source):
    # Figure out the raw indicator value, depending on what shape this entry is in
    if isinstance(entry,dict): #checks for dictionary for csv and json
        #csv shows use "indicator" , json enrties use "value" -check both
        raw_value = entry.get("indicator") or entry.get("value")
    else:
        #txt lines are already just plain strings
        raw_value=entry
    if not raw_value:
        return None
    raw_value=raw_value.strip()
    indicator_type=detect_type(raw_value) #here parser plays role here we run our own type again because can't trust source data completely 

    return{
        "indicator" : raw_value,
        "type" : indicator_type,
        "source" : source,
    }
#actually calling the loader and feeding its results into normalize_entry, one by one, for every entry in every feed. That's exactly what normalize_all does — it's the "glue" connecting the two.
def normalize_all(feed_dict): #using loader(can read all the raw feed files, but the data comes back messy and inconsistent)
    feeds=load_all_feeds(feed_dict)
    normalised=[]
    for source,entries in feeds.items():
        for entry in entries:
            result=normalize_entry(entry,source)
            if result is not None:
                normalised.append(result)
    return normalised



if __name__ == "__main__":
    results = normalize_all("../feeds")
    for r in results:
        print(r)
    print(f"\nTotal normalized entries: {len(results)}")


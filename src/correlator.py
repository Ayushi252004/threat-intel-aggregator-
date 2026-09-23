# Basically this file will list or identify the severity main function will be of normalize_all as it  contains all feeds
from normaliser import normalize_all
from collections import defaultdict

def group_by_indicator(entries):
    grouped=defaultdict(list)  #creates a special dictionary where, if you access a key that doesn't exist yet, it automatically starts as an empty list [] instead of throwing an error. This is exactly what we need — we're about to build up lists of entries under each indicator, without knowing ahead of time which indicators exist.

    for entry in entries:
        key=entry["indicator"]  # pulls out just the indicator value 
        grouped[key].append(entry) # this acts like count the feed by  adding this into grouped 
#instead of 21 separate flat entries, we have them organized by indicator — which is exactly what we need to count "how many different sources reported this.
    return grouped


def calculate_severity(source_count):
    if source_count >= 3:
        return "High"
    elif source_count ==2:
        return "Medium"
    else:
        return "Low"

def correlate(entries):
    grouped= group_by_indicator(entries)
    correlated=[]

    for indicator,entry_list in grouped.items():
        sources=set(entry["source"] for entry in entry_list)
        indicator_type=entry_list[0]["type"]
        severity=calculate_severity(len(sources))

        correlated.append({
            "indicator" : indicator ,
            "type" : indicator_type,
            "sources" : list(sources),
            "source_count" : len(sources),
            "severity" : severity ,
        })
    return correlated

if __name__=="__main__":
    entries= normalize_all("../feeds")
    results=correlate(entries)

    for r in results:
        print(r)
        

import csv 
import json
import os
# we need something which opens file ,read it , and hand back the data 
def load_csv(filepath):
    rows=[]
    with open(filepath , mode="r" , encoding="utf-8") as f:
        reader=csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def load_txt(filepath):
    lines=[]
    with open(filepath , mode="r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if line and not line.startswith("#"): #this says "only keep this line if it's not empty AND it doesn't start with #" (comments)
                lines.append(line)
    return lines

def load_json(filepath):
    with open(filepath , mode="r" , encoding="utf-8") as f:
        data=json.load(f)
    return data.get("indicators",[])

#if you wanted to load a feed, you'd have to know which function to call (load_csv vs load_txt vs load_json). That's annoying — ideally, you just say "load this file" and the code figures out the format itself.
def load_feed(filepath):
    extensions=os.path.splitext(filepath)[1].lower()
    if extensions==".csv":
        return load_csv(filepath)
    elif(extensions==".txt"):
        return load_txt(filepath)
    elif(extensions==".json"):
        return load_json(filepath)
    else:
        return ValueError(f"Unsupported feed format: {extensions}")
#this is the one that loads every feed file in the feeds folder automatically, without us naming each file one by one.
def load_all_feeds(feeds_dir):
    all_feeds={}
    for filename in os.listdir(feeds_dir): #gives us a list of every filename inside the feeds folder.
        filepath=os.path.join(feeds_dir,filename) #builds the full path to that file (combines the folder path + filename correctly, works on any OS).
        if os.path.isfile(filepath):   #makes sure we're only trying to load actual files
            try:
                all_feeds[filename]=load_feed(filepath) #loads the feed and stores the result under its filename as the key.
            except ValueError as e:
                print(f"Skipping {filename}:{e}")
    return all_feeds


if __name__=="__main__":
    feeds = load_all_feeds("../feeds")
    for feed_name, entries in feeds.items():
        print(f"\n=== {feed_name} ({len(entries)} entries) ===")
        for entry in entries:
            print(entry)

#load_csv() → reads a CSV file into labeled rows
#load_txt() → reads a plain text file into clean lines
#load_json() → reads a JSON file into its indicator list
#load_feed() → picks the right function automatically based on file extension
#load_all_feeds() → loads every file in the feeds folder at once, no matter the format


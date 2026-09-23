import json  
import csv
import os # to make sure our output folder exist
from correlator import correlate #gives us the ranked severity tagged results
from normaliser import normalize_all
def split_by_type(correlated_results):
    buckets={
        "ip":[],
        "domain_url":[],
        "hash":[],
    }
    for item in correlated_results:
        indicator_type=item["type"]
        if indicator_type=="ip":
            buckets["ip"].append(item)
        elif indicator_type in ("domain","url"):
            buckets["domain_url"].append(item)
        elif indicator_type=="hash":
            buckets["hash"].append(item)
         # anything else (email, unknown) is intentionally skipped -
        # not useful for firewall/web-filter/EDR blocklists
    return buckets  

def ensure_output_dir(output_dir):
    os.makedirs(output_dir,exist_ok=True)   #creates folder if doesn't exist


#for text
def write_txt_blocklist(items,filepath):
    with open(filepath,mode="w",encoding="utf=8") as f:
        for item in items:
            f.write(item["indicator"]+"\n") #writes just the raw indicator value, one per line

#for csv blocklist
def write_csv_blocklist(items,filepath):
    with open(filepath,mode="w",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=["indicator","type","source_count","severity"])
        writer.writeheader()
        for item in items:
            writer.writerow({
                "indicator":item["indicator"],
                "type":item["type"],
                "source_count":item["source_count"],
                "severity":item["severity"]
            })

def write_json_blocklist(items,filepath):
    with open(filepath,mode="w",encoding="utf-8") as f:
        json.dump(items,f,indent=2)

#function that ties everything together
def generate_blocklists(feeds_dir,output_dir):
    ensure_output_dir(output_dir) #ensuring output folder exist
    entries=normalize_all(feeds_dir) #runs full pipeline from start 
    correlated=correlate(entries) #ranks by severity 
    buckets=split_by_type(correlated) #splits into ip/domain/url/hash groups
    for category,items in buckets.items( ): #looping
        if not items:
            continue #skip empty categories , nothing to add
        write_txt_blocklist(items, os.path.join(output_dir, f"{category}_blocklist.txt")) #builds the full file path correctly (works on any OS), and uses an f-string to name the file dynamically
        write_csv_blocklist(items, os.path.join(output_dir, f"{category}_blocklist.csv"))
        write_json_blocklist(items, os.path.join(output_dir, f"{category}_blocklist.json"))
        print(f"Generated blocklists for '{category}' ({len(items)} items)")

if __name__ == "__main__":
    generate_blocklists("../feeds", "../output")
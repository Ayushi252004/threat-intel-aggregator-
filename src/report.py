#summary of everything in presentable format
import os 
from correlator import correlate
from normaliser import normalize_all
from blocklist import split_by_type

def build_summary(feeds_dir):
    entries=normalize_all(feeds_dir)
    correlated=correlate(entries)
    buckets=split_by_type(correlated)
    #count how many distinct feeds files were processed 
    feed_files=set(entry["source"] for entry in entries )

    #finding high severity indicators 
    high_priority=[item for item in correlated if item["severity"]=="High"] #go through every item in correlated, and only keep the ones where severity equals High
    summary={
        "feeds_processed":len(feed_files),
        "feed_names":sorted(feed_files),
        "total_unique_indicators": len(correlated),
        "counts_by_category": {
            "ip": len(buckets["ip"]),
            "domain_url": len(buckets["domain_url"]),
            "hash": len(buckets["hash"]),
        },
        "high_priority_indicators": high_priority,

    }
    return summary 

#displaying summary
def format_report(summary):
    lines = []
    lines.append("=" * 50)
    lines.append("THREAT INTELLIGENCE AGGREGATOR - FINAL REPORT")
    lines.append("=" * 50)
    lines.append(f"\nFeeds Processed: {summary['feeds_processed']}")
    for name in summary["feed_names"]:
        lines.append(f"  - {name}")

    lines.append(f"\nTotal Unique Indicators: {summary['total_unique_indicators']}")
    lines.append("\nBreakdown by Category:")
    for category, count in summary["counts_by_category"].items():
        lines.append(f"  - {category}: {count}")

    lines.append(f"\nHigh Priority Indicators ({len(summary['high_priority_indicators'])}):")
    for item in summary["high_priority_indicators"]:
        lines.append(
            f"  - {item['indicator']} ({item['type']}) "
            f"seen in {item['source_count']} sources: {', '.join(item['sources'])}"
        )

    lines.append("\n" + "=" * 50)
    return "\n".join(lines)

#function that saves this report to file
def save_report(report_text,filepath):
    with open(filepath,mode="w",encoding="utf-8") as f:
        f.write(report_text)

if __name__ == "__main__":
    summary = build_summary("../feeds")
    report_text = format_report(summary)

    print(report_text)
    save_report(report_text, "../output/final_report.txt")


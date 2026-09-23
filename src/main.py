import argparse
from blocklist import generate_blocklists
from report import build_summary,format_report,save_report

def parse_arguments():
    parser=argparse.ArgumentParser(
        description="Threat Intelligence Aggregator - collects, normalizes, and correlates IOC feeds."
    )
    parser.add_argument(
        "--feeds",
        default="../feeds",
        help="path to the folder containing feed files(default:../feeds)"
    )
    parser.add_argument(
        "--output",
        default="../output",
        help="Path to the folder where blocklists and reports will be saved (default:../output)"
    )
    return parser.parse_args()

def run_pipeline(feeds_dir, output_dir):
    print("=" * 50)
    print("Threat Intelligence Aggregator - Starting")
    print("=" * 50)

    print("\n[1/2] Generating blocklists...")
    generate_blocklists(feeds_dir, output_dir)

    print("\n[2/2] Generating final report...")
    summary = build_summary(feeds_dir)
    report_text = format_report(summary)
    save_report(report_text, f"{output_dir}/final_report.txt")

    print("\n" + report_text)
    print(f"\nAll outputs saved to: {output_dir}")


if __name__ == "__main__":
    args = parse_arguments()
    run_pipeline(args.feeds, args.output)
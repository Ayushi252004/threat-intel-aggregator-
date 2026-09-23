# Threat Intelligence Aggregator (Non-AI)

A practical threat intelligence toolkit that collects, parses, normalizes, and correlates
Indicators of Compromise (IOCs) from multiple threat feeds — without using AI or machine
learning — and produces ready-to-deploy blocklists and a summary intelligence report.

## Overview

Security teams receive threat intelligence from many sources — OSINT platforms, community
feeds, CERT advisories, commercial providers — each in a different format. This tool solves
that problem end-to-end:

1. **Reads** feeds in CSV, TXT, and JSON formats
2. **Identifies** each indicator's type (IP, domain, URL, hash, email) using pattern matching
3. **Normalizes** everything into one consistent structure
4. **Correlates** indicators across feeds — the same IOC reported by multiple independent
   sources is treated as higher priority
5. **Generates blocklists** split by category (IP / domain & URL / hash), exported as
   TXT, CSV, and JSON — ready for firewalls, web filters, and EDR/antivirus tools
6. **Produces a final report** summarizing feeds processed, total unique indicators, and
   the highest-priority threats found

## Architecture

```
Load Feeds → Parse Indicators → Normalize → Correlate → Generate Blocklists → Generate Report
```

Each stage is a separate, independently-testable Python module:

| Module | Responsibility |
|---|---|
| `loader.py` | Reads CSV, TXT, and JSON feed files |
| `parser.py` | Detects indicator type (ip / domain / url / hash / email) via regex + `ipaddress` |
| `normaliser.py` | Cleans and unifies all feed data into one consistent structure |
| `correlator.py` | Groups indicators, counts unique sources, assigns severity (High/Medium/Low) |
| `blocklist.py` | Splits results by category and exports TXT/CSV/JSON blocklists |
| `report.py` | Builds and saves the final summary report |
| `main.py` | Single command-line entry point that runs the full pipeline |

## Requirements

- Python 3.8+
- No external dependencies — uses only Python's standard library
  (`csv`, `json`, `re`, `ipaddress`, `os`, `argparse`, `collections`)

## Setup

```bash
git clone <repository-url>
cd threat_intel_aggregator
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

## Usage

Run the entire pipeline with a single command:

```bash
cd src
python main.py
```

By default, this reads feeds from `../feeds` and writes blocklists/reports to `../output`.
Both can be customized:

```bash
python main.py --feeds path/to/feeds --output path/to/output
```

View all options:

```bash
python main.py --help
```

## Severity Rating Logic

An indicator's severity reflects how many **distinct feeds** independently reported it —
more independent confirmations means a stronger signal that it's a genuine threat:

| Distinct sources | Severity |
|---|---|
| 3 or more | High |
| 2 | Medium |
| 1 | Low |

## Output

Running the tool produces, inside the `output/` folder:

- `ip_blocklist.{txt,csv,json}` — malicious IP addresses
- `domain_url_blocklist.{txt,csv,json}` — malicious domains and URLs
- `hash_blocklist.{txt,csv,json}` — malicious file hashes
- `final_report.txt` — summary report with feed counts, totals, and high-priority indicators

## Sample Data

The `feeds/` folder includes three realistic sample feeds (CSV, TXT, JSON) with
deliberately overlapping indicators, used to demonstrate the correlation engine.

## Author

Built as part of a cybersecurity internship project, focused on practical
blue-team / SOC threat-intelligence workflows.

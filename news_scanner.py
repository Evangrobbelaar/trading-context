#!/usr/bin/env python3
"""
news_scanner.py — manages news_impact.json for the session loop.
Usage:
  python3 news_scanner.py clear
  python3 news_scanner.py set --events "key1,key2" --headlines "summary text"
  python3 news_scanner.py show
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

NEWS_FILE = Path(__file__).parent / "news_impact.json"


def cmd_clear():
    NEWS_FILE.write_text(json.dumps({"events": [], "headlines": "", "updated": datetime.now(timezone.utc).isoformat()}, indent=2))
    print("news_impact.json cleared.")


def cmd_set(events_str, headlines):
    events = [e.strip() for e in events_str.split(",") if e.strip()]
    data = {
        "events": events,
        "headlines": headlines,
        "updated": datetime.now(timezone.utc).isoformat()
    }
    NEWS_FILE.write_text(json.dumps(data, indent=2))
    print(f"news_impact.json updated — {len(events)} event(s).")


def cmd_show():
    if not NEWS_FILE.exists():
        print("No news_impact.json found.")
        return
    print(NEWS_FILE.read_text())


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("clear")
    set_p = sub.add_parser("set")
    set_p.add_argument("--events", required=True)
    set_p.add_argument("--headlines", required=True)
    sub.add_parser("show")
    args = p.parse_args()

    if args.cmd == "clear":
        cmd_clear()
    elif args.cmd == "set":
        cmd_set(args.events, args.headlines)
    elif args.cmd == "show":
        cmd_show()
    else:
        p.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

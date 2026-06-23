#!/usr/bin/env python3
"""
master_scan.py — manages watchlist.json for the session loop.
Usage:
  python3 master_scan.py clear
  python3 master_scan.py add --instrument X --direction buy/sell --score N --reason "text" --entry N --sl N --tp N
  python3 master_scan.py show
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WATCHLIST_FILE = Path(__file__).parent / "watchlist.json"


def cmd_clear():
    WATCHLIST_FILE.write_text(json.dumps({"watchlist": [], "scan_time": datetime.now(timezone.utc).isoformat()}, indent=2))
    print("watchlist.json cleared.")


def cmd_add(instrument, direction, score, reason, entry, sl, tp):
    if WATCHLIST_FILE.exists():
        data = json.loads(WATCHLIST_FILE.read_text())
    else:
        data = {"watchlist": [], "scan_time": datetime.now(timezone.utc).isoformat()}
    data["watchlist"].append({
        "instrument": instrument.upper(),
        "direction": direction.lower(),
        "score": score,
        "reason": reason,
        "entry_zone": entry,
        "sl": sl,
        "tp": tp,
        "added": datetime.now(timezone.utc).isoformat()
    })
    WATCHLIST_FILE.write_text(json.dumps(data, indent=2))
    print(f"Added {instrument.upper()} {direction} (score {score}) to watchlist.")


def cmd_show():
    if not WATCHLIST_FILE.exists():
        print("No watchlist.json found.")
        return
    print(WATCHLIST_FILE.read_text())


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("clear")
    add_p = sub.add_parser("add")
    add_p.add_argument("--instrument", required=True)
    add_p.add_argument("--direction", required=True, choices=["buy", "sell"])
    add_p.add_argument("--score", type=int, required=True)
    add_p.add_argument("--reason", required=True)
    add_p.add_argument("--entry", type=float, required=True)
    add_p.add_argument("--sl", type=float, required=True)
    add_p.add_argument("--tp", type=float, required=True)
    sub.add_parser("show")
    args = p.parse_args()

    if args.cmd == "clear":
        cmd_clear()
    elif args.cmd == "add":
        cmd_add(args.instrument, args.direction, args.score, args.reason, args.entry, args.sl, args.tp)
    elif args.cmd == "show":
        cmd_show()
    else:
        p.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SESSION TICK LOGGER
Writes one JSON line per trading loop tick to session_log.jsonl.
This file is the raw data source for the weekly review loop.
Every tick gets logged — pass, block, hold, or no-trade — so the review
has a complete, honest picture of what was seen and what was done.

Usage (Claude runs this at the end of every tick):
  python3 session_logger.py \
    --tick 1 \
    --sast_time "10:30" \
    --session london \
    --account_balance 352.85 \
    --open_positions "GBPUSD:sell:+R22" \
    --h4_trend "XAUUSD:bear GBPUSD:bear EURUSD:bull" \
    --candidate_trades "GBPUSD" \
    --enforcer_result "PASS" \
    --trade_placed "GBPUSD sell 0.02L" \
    --action_taken "Placed GBPUSD short. SL 1.34610 TP 1.34000." \
    --notes "H4 lower highs confirmed. M15 broke below 1.34362 support."
"""

import argparse
import json
import sys
from datetime import datetime, timezone


def main():
    p = argparse.ArgumentParser(description="Log one trading tick to session_log.jsonl")
    p.add_argument(
        "--tick",
        type=int,
        required=True,
        help="Tick number within this session (1, 2, 3...)",
    )
    p.add_argument(
        "--sast_time",
        required=True,
        help="Current SAST time as HH:MM (from market data, not system clock)",
    )
    p.add_argument(
        "--session",
        required=True,
        choices=["asian", "london", "london_ny", "ny", "off"],
        help="Trading session active this tick",
    )
    p.add_argument(
        "--account_balance",
        type=float,
        required=True,
        help="Demo account balance in ZAR at time of tick",
    )
    p.add_argument(
        "--open_positions",
        default="none",
        help="Pipe-delimited: SYMBOL:direction:floatingPnL or 'none'",
    )
    p.add_argument(
        "--h4_trend",
        default="na",
        help="Space-delimited per instrument: XAUUSD:bear GBPUSD:bull etc or 'na'",
    )
    p.add_argument(
        "--candidate_trades",
        default="none",
        help="Instruments that passed initial H4 trend gate this tick or 'none'",
    )
    p.add_argument(
        "--enforcer_result",
        default="na",
        help="PASS | BLOCKED:reason | na (no trade attempted)",
    )
    p.add_argument(
        "--trade_placed",
        default="none",
        help="'SYMBOL direction size' if order placed, else 'none'",
    )
    p.add_argument(
        "--action_taken",
        required=True,
        help="One-sentence summary of what happened this tick",
    )
    p.add_argument(
        "--notes",
        default="",
        help="Any notable market observation, pattern, or lesson candidate",
    )
    args = p.parse_args()

    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "tick": args.tick,
        "sast_time": args.sast_time,
        "session": args.session,
        "account_balance_zar": args.account_balance,
        "open_positions": args.open_positions,
        "h4_trend": args.h4_trend,
        "candidate_trades": args.candidate_trades,
        "enforcer_result": args.enforcer_result,
        "trade_placed": args.trade_placed,
        "action_taken": args.action_taken,
        "notes": args.notes,
    }

    with open("session_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(
        f"[TICK {args.tick} LOGGED] {args.sast_time} SAST | "
        f"Balance R{args.account_balance:.2f} | "
        f"Action: {args.action_taken}"
    )


def summarize(since_date: str | None = None):
    """Print a summary of session_log.jsonl for review. Optional: filter since ISO date."""
    try:
        with open("session_log.jsonl", "r", encoding="utf-8") as f:
            entries = [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        print("No session_log.jsonl found yet.")
        return

    if since_date:
        entries = [e for e in entries if e["timestamp_utc"] >= since_date]

    total = len(entries)
    trades_placed = [e for e in entries if e["trade_placed"] != "none"]
    blocked = [e for e in entries if "BLOCKED" in e.get("enforcer_result", "")]
    sessions = len({e["timestamp_utc"][:10] for e in entries})

    print("\n=== SESSION LOG SUMMARY ===")
    print(f"Total ticks logged: {total}")
    print(f"Trading days: {sessions}")
    print(f"Trades placed: {len(trades_placed)}")
    print(f"Trades blocked by enforcer: {len(blocked)}")
    if trades_placed:
        print("\nTrades placed:")
        for t in trades_placed:
            print(
                f"  {t['timestamp_utc'][:10]} {t['sast_time']} SAST — {t['trade_placed']}"
            )
    if blocked:
        print("\nBlocked trades (enforcer saved these):")
        for b in blocked:
            print(
                f"  {b['timestamp_utc'][:10]} {b['sast_time']} SAST — {b['enforcer_result']}"
            )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        since = sys.argv[2] if len(sys.argv) > 2 else None
        summarize(since)
    else:
        main()

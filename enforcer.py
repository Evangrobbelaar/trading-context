#!/usr/bin/env python3
"""
PRE-TRADE ENFORCER v2 — REBUILD PHASE (simplified June 25, 2026)

Per Evan's instruction: while the strategy is being rebuilt, every check
EXCEPT the two below is suspended on purpose. The old v1 logic (max risk %,
R:R minimum, instrument size caps, balance gates) is preserved in git
history (see `git log -- enforcer.py`) and can be restored once a new
strategy is validated — see "ENFORCER — REBUILD PHASE" in
EVAN_TRADING_CONTEXT.md.

Active checks:
  1. SESSION MAX LOSS — block all further trades once current balance has
     dropped to <= 50% of this session's starting balance.
  2. TIME VALIDITY — block if outside normal forex market hours
     (closed ~Sat 00:00 UTC -> Sun 21:00 UTC) or the supplied timestamp
     looks wrong.

Usage:
  # First call of a session — records the starting balance as the floor reference:
  python3 enforcer.py --account demo --account_id 41810679 --balance 500.00 --init

  # Every call before create_market_order:
  python3 enforcer.py --account demo --account_id 41810679 --balance 463.20
"""
import argparse
import sys
import json
import os
from datetime import datetime, timezone

STATE_FILE = "session_state.json"
AUDIT_FILE = "enforcer_audit.jsonl"
SESSION_MAX_LOSS_PCT = 0.50


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def check_time(now_utc):
    """Returns a block reason string, or None if time is valid."""
    weekday = now_utc.weekday()  # Mon=0 ... Sun=6
    hour = now_utc.hour
    if weekday == 5:  # Saturday
        return "Market closed — Saturday."
    if weekday == 6 and hour < 21:  # Sunday before 21:00 UTC
        return "Market closed — Sunday before 21:00 UTC reopen."
    if weekday == 4 and hour >= 21:  # Friday after 21:00 UTC
        return "Market closed — Friday after 21:00 UTC."
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--account", required=True, choices=["demo", "live"])
    p.add_argument("--account_id", required=True, help="e.g. 41810679")
    p.add_argument("--balance", type=float, required=True)
    p.add_argument("--init", action="store_true",
                    help="Record this balance as the session's starting balance.")
    p.add_argument("--now", default=None,
                    help="Override current UTC time for testing, ISO format.")
    args = p.parse_args()

    now_utc = datetime.now(timezone.utc)
    if args.now:
        try:
            now_utc = datetime.fromisoformat(args.now)
        except ValueError:
            pass

    blocks = []
    key = f"{args.account}_{args.account_id}"
    state = load_state()
    today = now_utc.strftime("%Y-%m-%d")

    if args.init or key not in state or state[key].get("date") != today:
        state[key] = {"session_start_balance": args.balance, "date": today}
        save_state(state)

    session_start = state[key]["session_start_balance"]
    loss_pct = 1 - (args.balance / session_start) if session_start > 0 else 0

    if loss_pct >= SESSION_MAX_LOSS_PCT:
        blocks.append(
            f"Session max loss hit: balance R{args.balance:.2f} is "
            f"{loss_pct*100:.1f}% down from session start R{session_start:.2f} "
            f"(limit {SESSION_MAX_LOSS_PCT*100:.0f}%). No more trades this session."
        )

    time_block = check_time(now_utc)
    if time_block:
        blocks.append(time_block)

    result = {
        "timestamp": now_utc.isoformat(),
        "account": args.account,
        "account_id": args.account_id,
        "balance": args.balance,
        "session_start_balance": session_start,
        "loss_pct": round(loss_pct * 100, 2),
        "verdict": "BLOCKED" if blocks else "PASS",
        "block_reasons": blocks,
        "enforcer_mode": "v2_rebuild_phase_simplified",
    }

    print(json.dumps(result, indent=2))

    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(result) + "\n")

    sys.exit(1 if blocks else 0)


if __name__ == "__main__":
    main()

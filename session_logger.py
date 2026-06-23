#!/usr/bin/env python3
"""
session_logger.py — appends a tick/session log entry to session_log.jsonl.
Usage:
  python3 session_logger.py \
    --tick 1 --session London --sast "08:50" \
    --account 41829612 --balance 5000 --equity 5065.47 \
    --open_trades "BRENT SHORT 109703539" \
    --actions "Trailed BRENT SL to 77.755 (breakeven)" \
    --watchlist "AUDUSD,XAUUSD,XAGUSD" \
    --news "FedHawkish,USIranPeaceDeal" \
    --trades_placed 0 --trades_closed 0 \
    --session_pnl 0 --notes "optional"
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path(__file__).parent / "session_log.jsonl"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tick", type=int, required=True)
    p.add_argument("--session", required=True)
    p.add_argument("--sast", required=True)
    p.add_argument("--account", required=True)
    p.add_argument("--balance", type=float, required=True)
    p.add_argument("--equity", type=float, required=True)
    p.add_argument("--open_trades", default="")
    p.add_argument("--actions", default="")
    p.add_argument("--watchlist", default="")
    p.add_argument("--news", default="")
    p.add_argument("--trades_placed", type=int, default=0)
    p.add_argument("--trades_closed", type=int, default=0)
    p.add_argument("--session_pnl", type=float, default=0)
    p.add_argument("--notes", default="")
    args = p.parse_args()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tick": args.tick,
        "session": args.session,
        "sast": args.sast,
        "account": args.account,
        "balance": args.balance,
        "equity": args.equity,
        "open_trades": args.open_trades,
        "actions": args.actions,
        "watchlist": args.watchlist,
        "news": args.news,
        "trades_placed": args.trades_placed,
        "trades_closed": args.trades_closed,
        "session_pnl": args.session_pnl,
        "notes": args.notes
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"Tick {args.tick} logged — {args.session} {args.sast} SAST — equity R{args.equity:.2f} — {args.trades_placed} trade(s) placed.")


if __name__ == "__main__":
    main()

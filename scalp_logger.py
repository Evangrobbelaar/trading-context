#!/usr/bin/env python3
"""
scalp_logger.py -- Tick and trade logger.
Appends to scalp_log.jsonl. Updates scalp_state.json on trade completion.

Usage:
  python scalp_logger.py tick --tick_num 5 --sast_time "15:23" \
      --symbol_checked "EURUSD,XAUUSD" --level_triggered "none" \
      --enforcer_result "na" --trade_placed "none" --notes "quiet"

  python scalp_logger.py trade --symbol EURUSD --direction short \
      --entry 1.14048 --exit 1.13855 --pnl_zar 35.20 \
      --exit_reason "TP hit" --duration_minutes 14
"""

import sys
import json
import argparse
import os
from datetime import datetime, timezone, timedelta

SCALP_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCALP_DIR, "scalp_log.jsonl")
STATE_FILE = os.path.join(SCALP_DIR, "scalp_state.json")

SAST = timezone(timedelta(hours=2))


def cmd_tick(args):
    now = datetime.now(SAST)
    entry = {
        "type": "tick",
        "timestamp_sast": now.isoformat(),
        "tick_num": args.tick_num,
        "sast_time": args.sast_time,
        "symbols_checked": [
            s.strip() for s in args.symbol_checked.split(",") if s.strip()
        ],
        "level_triggered": args.level_triggered,
        "enforcer_result": args.enforcer_result,
        "trade_placed": args.trade_placed,
        "notes": args.notes,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"TICK LOGGED: #{args.tick_num} at {args.sast_time} SAST")


def cmd_trade(args):
    now = datetime.now(SAST)
    symbol = args.symbol.upper()
    result = "WIN" if args.pnl_zar >= 0 else "LOSS"

    entry = {
        "type": "trade",
        "timestamp_sast": now.isoformat(),
        "symbol": symbol,
        "direction": args.direction,
        "entry": args.entry,
        "exit": args.exit,
        "pnl_zar": args.pnl_zar,
        "exit_reason": args.exit_reason,
        "duration_minutes": args.duration_minutes,
        "result": result,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Update session state counters
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)

            state["scalp_trades_today"] = state.get("scalp_trades_today", 0) + 1
            state["session_pnl_zar"] = round(
                state.get("session_pnl_zar", 0.0) + args.pnl_zar, 2
            )

            if args.pnl_zar < 0:
                state["consecutive_losses"] = state.get("consecutive_losses", 0) + 1
            else:
                state["consecutive_losses"] = 0

            # Auto-stop if session limits hit
            if state["consecutive_losses"] >= 2:
                state["loop_stopped"] = True
                state["stop_reason"] = "2 consecutive losses"
            elif state["scalp_trades_today"] >= 3:
                state["loop_stopped"] = True
                state["stop_reason"] = "3 scalp trades reached for session"
            elif state["session_pnl_zar"] < -200:
                state["loop_stopped"] = True
                state["stop_reason"] = (
                    f"Session drawdown R{state['session_pnl_zar']:.0f} exceeded R200"
                )

            with open(STATE_FILE, "w") as f:
                json.dump(state, f, indent=2)

            trades = state["scalp_trades_today"]
            cons = state["consecutive_losses"]
            pnl = state["session_pnl_zar"]
            print(
                f"TRADE LOGGED: {symbol} {args.direction} | {result} R{args.pnl_zar:.2f} | "
                f"{args.exit_reason} | {args.duration_minutes}min"
            )
            print(
                f"Session: {trades}/3 trades | {cons} consecutive losses | "
                f"P&L: R{pnl:+.2f}"
            )
            if state.get("loop_stopped"):
                print(f"LOOP STOPPED: {state['stop_reason']}")
        except Exception as e:
            print(f"WARNING: Could not update scalp_state.json — {e}")
    else:
        print(
            f"TRADE LOGGED: {symbol} {args.direction} | {result} R{args.pnl_zar:.2f} | "
            f"{args.exit_reason} | {args.duration_minutes}min"
        )
        print("WARNING: scalp_state.json not found — counters not updated")


def main():
    parser = argparse.ArgumentParser(description="Scalp tick and trade logger")
    sub = parser.add_subparsers(dest="command")

    tick_p = sub.add_parser("tick", help="Log a monitoring tick")
    tick_p.add_argument("--tick_num", type=int, required=True)
    tick_p.add_argument("--sast_time", required=True)
    tick_p.add_argument("--symbol_checked", default="")
    tick_p.add_argument("--level_triggered", default="none")
    tick_p.add_argument("--enforcer_result", default="na")
    tick_p.add_argument("--trade_placed", default="none")
    tick_p.add_argument("--notes", default="")

    trade_p = sub.add_parser("trade", help="Log a completed trade")
    trade_p.add_argument("--symbol", required=True)
    trade_p.add_argument("--direction", required=True, choices=["long", "short"])
    trade_p.add_argument("--entry", type=float, required=True)
    trade_p.add_argument("--exit", type=float, required=True)
    trade_p.add_argument("--pnl_zar", type=float, required=True)
    trade_p.add_argument("--exit_reason", required=True)
    trade_p.add_argument("--duration_minutes", type=int, required=True)

    args = parser.parse_args()

    if args.command == "tick":
        cmd_tick(args)
    elif args.command == "trade":
        cmd_trade(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

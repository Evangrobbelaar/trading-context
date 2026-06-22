#!/usr/bin/env python3
"""
PRE-TRADE ENFORCER — deterministic, cannot be argued around.

This script encodes ONLY the numeric/hard rules from EVAN_TRADING_CONTEXT.md
(max risk %, instrument size caps, SL buffers, min R:R, banned instruments,
indices balance gate). It does NOT judge trend, news, or structure — that
judgment still comes from Claude's analysis and must be logged separately
(see CHANGE 4 mandatory ping format in the context doc). This script exists
specifically because the June 11 catastrophic session proved a text rule
("enforcer cannot be bypassed") can still be talked around by an instruction.
A script either exits 0 (PASS) or 1 (BLOCKED). There is no instruction that
changes that.

Usage:
  python3 enforcer.py --instrument XAUUSD --direction buy --units 1 \
    --balance 352.85 --account demo --risk_amount 47 --reward_amount 93 \
    --sl_distance 18

Claude Code MUST run this before every create_market_order call and treat
exit code 1 as an absolute block — never re-run with adjusted inputs just to
get a PASS without genuinely changing the trade.
"""
import argparse
import sys
import json
from datetime import datetime, timezone

INSTRUMENT_RULES = {
    "XAUUSD":    {"max_units": 1, "min_sl": 15, "max_sl": 25, "unit": "pts"},
    "XAUUSD247": {"max_units": 1, "min_sl": 15, "max_sl": 25, "unit": "pts"},
    "EURUSD":    {"max_lots": 0.03, "min_sl": 15, "max_sl": 25, "unit": "pips"},
    "GBPUSD":    {"max_lots": 0.03, "min_sl": 15, "max_sl": 25, "unit": "pips"},
    "USDJPY":    {"max_lots": 0.03, "min_sl": 15, "max_sl": 25, "unit": "pips"},
    "NAS100":    {"blocked_below_balance": 5000, "min_sl": 80, "max_sl": 150, "unit": "pts"},
    "SPX500":    {"blocked_below_balance": 5000, "min_sl": 80, "max_sl": 150, "unit": "pts"},
    "US30":      {"blocked_below_balance": 5000, "min_sl": 80, "max_sl": 150, "unit": "pts"},
}
BANNED_ALWAYS = {"WTI", "BTCUSD", "ETHUSD"}

MAX_RISK_PCT = 0.20
MIN_RR = 1.2


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--instrument", required=True)
    p.add_argument("--direction", required=True, choices=["buy", "sell"])
    p.add_argument("--units", type=float, default=0)
    p.add_argument("--lots", type=float, default=0)
    p.add_argument("--balance", type=float, required=True)
    p.add_argument("--account", required=True, choices=["demo", "live"])
    p.add_argument("--risk_amount", type=float, required=True,
                    help="ZAR amount lost if SL hits")
    p.add_argument("--reward_amount", type=float, required=True,
                    help="ZAR amount gained if TP hits")
    p.add_argument("--sl_distance", type=float, required=True,
                    help="pts or pips, matching the instrument's unit")
    args = p.parse_args()

    blocks = []
    inst = args.instrument.upper()

    if inst in BANNED_ALWAYS:
        blocks.append(f"{inst} is on the permanent avoid list. No exceptions.")

    rule = INSTRUMENT_RULES.get(inst)
    if rule:
        if "blocked_below_balance" in rule and args.balance < rule["blocked_below_balance"]:
            blocks.append(
                f"{inst} blocked until balance >= R{rule['blocked_below_balance']} "
                f"(current R{args.balance:.2f})."
            )
        if "max_units" in rule and args.units > rule["max_units"]:
            blocks.append(f"{inst} max {rule['max_units']} unit(s). Requested {args.units}.")
        if "max_lots" in rule and args.lots > rule["max_lots"]:
            blocks.append(f"{inst} max {rule['max_lots']} lots. Requested {args.lots}.")
        if "min_sl" in rule and args.sl_distance < rule["min_sl"]:
            blocks.append(
                f"{inst} SL too tight: {args.sl_distance} < min {rule['min_sl']}{rule['unit']}."
            )
        if "max_sl" in rule and args.sl_distance > rule["max_sl"]:
            blocks.append(
                f"{inst} SL too wide: {args.sl_distance} > max {rule['max_sl']}{rule['unit']} "
                f"— check sizing, this is how June 11 happened."
            )

    risk_pct = (args.risk_amount / args.balance) if args.balance > 0 else 1.0
    if risk_pct > MAX_RISK_PCT:
        blocks.append(
            f"Risk {risk_pct*100:.1f}% of account exceeds {MAX_RISK_PCT*100:.0f}% max "
            f"(R{args.risk_amount:.2f} on R{args.balance:.2f})."
        )

    rr = (args.reward_amount / args.risk_amount) if args.risk_amount > 0 else 0
    if rr < MIN_RR:
        blocks.append(f"R:R {rr:.2f}:1 is below the {MIN_RR}:1 minimum.")

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "instrument": inst,
        "direction": args.direction,
        "account": args.account,
        "balance": args.balance,
        "risk_amount": args.risk_amount,
        "risk_pct": round(risk_pct * 100, 2),
        "rr": round(rr, 2),
        "sl_distance": args.sl_distance,
        "verdict": "BLOCKED" if blocks else "PASS",
        "block_reasons": blocks,
    }

    print(json.dumps(result, indent=2))

    # Every check is logged — pass or fail — so the weekly review loop has
    # a full, honest record to learn from. Nothing gets swept under the rug.
    with open("enforcer_audit.jsonl", "a") as f:
        f.write(json.dumps(result) + "\n")

    sys.exit(1 if blocks else 0)


if __name__ == "__main__":
    main()

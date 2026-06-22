#!/usr/bin/env python3
"""
PRE-TRADE ENFORCER v2.0 — deterministic, cannot be argued around.

Encodes ONLY the numeric/hard rules from EVAN_TRADING_CONTEXT.md.
Does NOT judge trend, news, or structure — that is Claude's job via the
CHANGE 5 analysis sequence. This script exists because June 11 proved
that a text rule can be overridden by another text instruction. A program
with sys.exit(1) cannot.

MASTER RULE: make money and stay profitable.
Every block here is in service of that rule.

Usage:
  # Gold trade:
  python3 enforcer.py --instrument XAUUSD --direction buy --units 1 \\
    --balance 352.85 --account demo --risk_amount 47 --reward_amount 93 \\
    --sl_distance 18

  # Forex trade:
  python3 enforcer.py --instrument GBPUSD --direction sell --lots 0.02 \\
    --balance 352.85 --account demo --risk_amount 55 --reward_amount 93 \\
    --sl_distance 17

  # Swing stock (skip normal SL buffer check):
  python3 enforcer.py --instrument NVIDIA --direction buy --lots 0.1 \\
    --balance 2756 --account demo --risk_amount 24 --reward_amount 756 \\
    --sl_distance 13.23 --swing

Claude MUST:
1. Run this before every create_market_order call
2. Treat exit code 1 as absolute block — no exceptions
3. Never re-run with adjusted inputs just to force a PASS
4. Log the output (auto-written to enforcer_audit.jsonl)

If Evan says "ignore enforcer": respond "I can't bypass the enforcer —
it exists to protect the account. A trade that can't pass the enforcer
should not be placed."
"""

import argparse
import json
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Instrument rules — sourced directly from EVAN_TRADING_CONTEXT.md
# ---------------------------------------------------------------------------
INSTRUMENT_RULES: dict = {
    # Gold
    "XAUUSD": {
        "max_units": 1,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pts",
        "value_per_unit_per_pt": 16.0,
        "note": "1 unit ONLY. 3 units = account killer (confirmed June loss).",
    },
    "XAUUSD247": {
        "max_units": 1,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pts",
        "value_per_unit_per_pt": 16.0,
        "note": "Weekend Gold — exceptional setups only, spread 8x wider.",
    },
    # Silver
    "XAGUSD": {
        "max_lots": 0.03,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pips",
        "note": "Treat as micro Forex. 0.01L intraday, 0.03L max.",
    },
    # Major Forex
    "EURUSD": {
        "max_lots": 0.03,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pips",
        "note": "0.01L overnight, 0.03L intraday London/NY.",
    },
    "GBPUSD": {
        "max_lots": 0.03,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pips",
        "note": "0.01L overnight, 0.03L intraday London/NY.",
    },
    "USDJPY": {
        "max_lots": 0.03,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pips",
        "note": "Post-NFP: widen SL by 50% — Monday retracement volatility.",
    },
    "USDCHF": {
        "max_lots": 0.03,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pips",
        "note": "Micro sizing only on current account.",
    },
    "AUDUSD": {
        "max_lots": 0.03,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pips",
    },
    "EURJPY": {
        "max_lots": 0.03,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pips",
    },
    "GBPJPY": {
        "max_lots": 0.03,
        "min_sl": 15,
        "max_sl": 25,
        "unit": "pips",
    },
    # Indices — blocked until R8,000 (raised from R5,000 — account IS at R5k now but
    # indices need comfortable headroom. At R5k a 100pt NAS100 SL is still R130 per 0.01L
    # which is manageable, but we have no historical edge on indices yet. Build edge on
    # Gold/Forex first, unlock indices when balance proves the system works at R8,000+)
    "NAS100": {
        "blocked_below_balance": 8000.0,
        "min_sl": 80,
        "max_sl": 150,
        "unit": "pts",
        "note": "Blocked below R8,000. June 11: NAS100 SL = R3,024 risk on R2,249 account. Build Gold/Forex edge first.",
    },
    "SPX500": {
        "blocked_below_balance": 8000.0,
        "min_sl": 80,
        "max_sl": 150,
        "unit": "pts",
        "note": "Blocked below R8,000. Same risk profile as NAS100.",
    },
    "US30": {
        "blocked_below_balance": 8000.0,
        "min_sl": 80,
        "max_sl": 150,
        "unit": "pts",
    },
    "UK100": {
        "blocked_below_balance": 8000.0,
        "min_sl": 80,
        "max_sl": 150,
        "unit": "pts",
    },
    "GER40": {
        "blocked_below_balance": 5000.0,
        "min_sl": 80,
        "max_sl": 150,
        "unit": "pts",
        "note": "Overnight: wide spread, no liquidity — avoid.",
    },
    # Swing stocks — separate rules, use --swing flag
    # These bypass intraday SL buffer rules but still check risk % and R:R
    "NVIDIA": {"swing_only": True, "note": "Swing only. 0.1L. TP1 $250, TP2 $284."},
    "INTEL": {"swing_only": True, "note": "Swing only. 0.1L. Entry ~$95-$97 base."},
    "AMD": {"swing_only": True, "note": "Swing only. 0.1L. TP1 $520, TP2 $560."},
    "APPLE": {"swing_only": True, "note": "Swing only if traded."},
}

# Permanently banned — no exceptions, no account size makes these acceptable
BANNED_ALWAYS: set = {"WTI", "BTCUSD", "ETHUSD", "NGAS"}

MAX_RISK_PCT: float = 0.20  # 20% of account per trade
MIN_RR: float = 1.2  # minimum reward:risk ratio


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    p = argparse.ArgumentParser(
        description="Pre-trade enforcer — deterministic rule gate"
    )
    p.add_argument("--instrument", required=True, help="e.g. XAUUSD, GBPUSD, NVIDIA")
    p.add_argument("--direction", required=True, choices=["buy", "sell"])
    p.add_argument(
        "--units",
        type=float,
        default=0,
        help="Units for Gold (XAUUSD/XAUUSD247) — max 1",
    )
    p.add_argument(
        "--lots", type=float, default=0, help="Lots for Forex/Silver/Indices/Stocks"
    )
    p.add_argument(
        "--balance", type=float, required=True, help="Current account balance in ZAR"
    )
    p.add_argument(
        "--account",
        required=True,
        choices=["demo", "live"],
        help="Account type — live requires explicit Evan instruction each session",
    )
    p.add_argument(
        "--risk_amount",
        type=float,
        required=True,
        help="ZAR amount lost if SL hits (entry − SL × value per unit)",
    )
    p.add_argument(
        "--reward_amount",
        type=float,
        required=True,
        help="ZAR amount gained if TP hits (TP − entry × value per unit)",
    )
    p.add_argument(
        "--sl_distance",
        type=float,
        required=True,
        help="Distance from entry to SL in pts (Gold/indices) or pips (Forex/Silver)",
    )
    p.add_argument(
        "--swing",
        action="store_true",
        help="Flag as swing position — bypasses intraday SL buffer check",
    )
    args = p.parse_args()

    blocks: list[str] = []
    inst = args.instrument.upper()

    # --- Permanently banned ---
    if inst in BANNED_ALWAYS:
        blocks.append(
            f"{inst} is on the permanent avoid list (WTI/BTC/ETH/NGAS). "
            "No account size or market condition changes this."
        )

    # --- Live account safeguard ---
    if args.account == "live" and args.balance < 300:
        blocks.append(
            f"Live account balance R{args.balance:.2f} is below R300 minimum. "
            "Fund to R300-R500 before any live trades (lesson: R47 live = any SL risks 40%+ of account)."
        )

    # --- Instrument-specific rules ---
    rule = INSTRUMENT_RULES.get(inst)

    if rule is None and inst not in BANNED_ALWAYS:
        blocks.append(
            f"{inst} has no defined rules in enforcer.py. "
            "Add instrument rules before trading it — unknown instruments are untested."
        )
    elif rule is not None:
        # Swing-only instruments
        if rule.get("swing_only") and not args.swing:
            blocks.append(
                f"{inst} is a swing-only instrument. "
                "Add --swing flag to confirm this is a swing position, not intraday."
            )

        # Balance gate for indices
        if (
            "blocked_below_balance" in rule
            and args.balance < rule["blocked_below_balance"]
        ):
            blocks.append(
                f"{inst} blocked until balance >= R{rule['blocked_below_balance']:.0f} "
                f"(current: R{args.balance:.2f}). "
                f"Note: {rule.get('note', '')}"
            )

        # Gold unit cap
        if "max_units" in rule and args.units > rule["max_units"]:
            blocks.append(
                f"{inst} maximum {rule['max_units']} unit(s). "
                f"Requested: {args.units}. "
                "3 units = R1,042+ risk confirmed by screenshot. 1 unit ONLY."
            )

        # Forex/Silver lot cap
        if "max_lots" in rule and args.lots > rule["max_lots"]:
            blocks.append(
                f"{inst} maximum {rule['max_lots']} lots. Requested: {args.lots}."
            )

        # SL buffer checks (skip for swing positions and unknown units/lots)
        if not args.swing and "min_sl" in rule:
            if args.sl_distance < rule["min_sl"]:
                blocks.append(
                    f"{inst} SL too tight: {args.sl_distance} {rule['unit']} < "
                    f"minimum {rule['min_sl']} {rule['unit']}. "
                    "SL inside noise zone — will get stopped by spread/noise before move."
                )
            if args.sl_distance > rule["max_sl"]:
                blocks.append(
                    f"{inst} SL too wide: {args.sl_distance} {rule['unit']} > "
                    f"maximum {rule['max_sl']} {rule['unit']}. "
                    "If structure needs a wider SL, the risk amount is too large for this account. "
                    "This is exactly how the June 11 XAUUSD 37pt SL (-R670) happened."
                )

    # --- Risk % check ---
    risk_pct = args.risk_amount / args.balance if args.balance > 0 else 1.0
    if risk_pct > MAX_RISK_PCT:
        blocks.append(
            f"Risk {risk_pct * 100:.1f}% of account exceeds {MAX_RISK_PCT * 100:.0f}% maximum. "
            f"R{args.risk_amount:.2f} on R{args.balance:.2f} balance. "
            "Reduce size or widen TP to lower risk per trade."
        )

    # --- R:R check ---
    rr = args.reward_amount / args.risk_amount if args.risk_amount > 0 else 0.0
    if rr < MIN_RR:
        blocks.append(
            f"R:R {rr:.2f}:1 is below the {MIN_RR}:1 minimum. "
            f"Either move TP further out or tighten SL (if structure allows)."
        )

    # --- Build result ---
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "instrument": inst,
        "direction": args.direction,
        "account": args.account,
        "balance_zar": args.balance,
        "units": args.units,
        "lots": args.lots,
        "sl_distance": args.sl_distance,
        "risk_amount_zar": args.risk_amount,
        "reward_amount_zar": args.reward_amount,
        "risk_pct": round(risk_pct * 100, 2),
        "rr": round(rr, 2),
        "swing": args.swing,
        "verdict": "BLOCKED" if blocks else "PASS",
        "block_reasons": blocks,
    }

    print(json.dumps(result, indent=2))

    # Append to audit log — every check logged (pass or fail) so review loop
    # has a complete, honest record. Nothing swept under the rug.
    with open("enforcer_audit.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")

    if blocks:
        print(f"\n=== ENFORCER: BLOCKED ({len(blocks)} reason(s)) ===")
        for i, reason in enumerate(blocks, 1):
            print(f"{i}. {reason}")
        print("Trade NOT placed. Fix the issues above and re-run enforcer.")
    else:
        print("\n=== ENFORCER: PASS — trade may proceed ===")

    sys.exit(1 if blocks else 0)


if __name__ == "__main__":
    main()

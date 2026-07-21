#!/usr/bin/env python3
"""
PRE-TRADE ENFORCER v3.0 — rewritten June 25 2026.

Philosophy: pass good trades fast, block genuinely bad ones.
Old version had too many invented thresholds. This version uses fewer,
better-justified rules so we stop missing trades on valid setups.

HARD RULES (cannot be bypassed):
  1. Never trade live account (without explicit session flag)
  2. Max 1 unit XAUUSD — June loss proved 3 units destroys account
  3. R:R must be ≥ 1.0 minimum (R:R < 1 is a guaranteed expected loser)
  4. SL must be > 0 (no SL = no trade)
  5. Risk ≤ 20% of balance per trade

SOFT RULES (relaxed by context flags):
  - SL limits adapt to instrument volatility and news_event flag
  - R:R requirement scales with macro confidence
  - Indices unlocked at R5,000 (not R8k — news trades are valid there)

Usage:
  python3 enforcer.py --instrument XAUUSD --direction buy --units 1 \\
    --balance 5088 --account demo --risk_amount 160 --reward_amount 480 \\
    --sl_distance 10 --mode change7

  python3 enforcer.py --instrument USDJPY --direction buy --lots 0.03 \\
    --balance 5088 --account demo --risk_amount 83 --reward_amount 171 \\
    --sl_distance 16 --mode change7 --macro_bias bull

  python3 enforcer.py --instrument EURUSD --direction sell --lots 0.03 \\
    --balance 5088 --account demo --risk_amount 55 --reward_amount 138 \\
    --sl_distance 10 --mode change7 --news_event --macro_bias bear
"""

import argparse
import json
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Instrument config — sl limits are baseline for normal market conditions
# news_event flag multiplies max_sl by 1.5 automatically
# ---------------------------------------------------------------------------
INSTRUMENTS: dict = {
    # Gold — 1 unit max, wide SL needed (100+ pt daily range)
    "XAUUSD": {
        "max_units": 1,
        "min_sl": 5,
        "max_sl": 50,
        "unit": "pts",
        "zar_per_unit": 16.0,
    },
    "XAUUSD247": {
        "max_units": 1,
        "min_sl": 5,
        "max_sl": 50,
        "unit": "pts",
        "zar_per_unit": 16.0,
    },
    # Silver
    "XAGUSD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 50, "unit": "pips"},
    # Major forex
    "EURUSD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "GBPUSD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "USDJPY": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "USDCHF": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "AUDUSD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "NZDUSD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "USDCAD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    # Minor forex
    "EURJPY": {"max_lots": 0.05, "min_sl": 5, "max_sl": 40, "unit": "pips"},
    "GBPJPY": {"max_lots": 0.05, "min_sl": 5, "max_sl": 40, "unit": "pips"},
    "EURGBP": {"max_lots": 0.05, "min_sl": 5, "max_sl": 30, "unit": "pips"},
    "AUDJPY": {"max_lots": 0.05, "min_sl": 5, "max_sl": 40, "unit": "pips"},
    "GBPAUD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 40, "unit": "pips"},
    "EURAUD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 40, "unit": "pips"},
    "EURCHF": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "EURCAD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "GBPCAD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 40, "unit": "pips"},
    "GBPCHF": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "AUDCHF": {"max_lots": 0.05, "min_sl": 5, "max_sl": 30, "unit": "pips"},
    "AUDNZD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 30, "unit": "pips"},
    "AUDCAD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 30, "unit": "pips"},
    "NZDCAD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 30, "unit": "pips"},
    "NZDCHF": {"max_lots": 0.05, "min_sl": 5, "max_sl": 30, "unit": "pips"},
    "NZDJPY": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "CADJPY": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    "CHFJPY": {"max_lots": 0.05, "min_sl": 5, "max_sl": 35, "unit": "pips"},
    # Oil (CFDs)
    "BRENT": {"max_lots": 0.05, "min_sl": 20, "max_sl": 200, "unit": "pips"},
    "WTI": {"max_lots": 0.05, "min_sl": 20, "max_sl": 200, "unit": "pips"},
    # Indices — unlocked at R5k (post-news trades are valid)
    "NAS100": {
        "min_balance": 5000,
        "max_lots": 0.01,
        "min_sl": 30,
        "max_sl": 200,
        "unit": "pts",
    },
    "SPX500": {
        "min_balance": 5000,
        "max_lots": 0.01,
        "min_sl": 20,
        "max_sl": 150,
        "unit": "pts",
    },
    "US30": {
        "min_balance": 5000,
        "max_lots": 0.01,
        "min_sl": 50,
        "max_sl": 250,
        "unit": "pts",
    },
    "UK100": {
        "min_balance": 5000,
        "max_lots": 0.01,
        "min_sl": 30,
        "max_sl": 200,
        "unit": "pts",
    },
    "GER40": {
        "min_balance": 5000,
        "max_lots": 0.01,
        "min_sl": 30,
        "max_sl": 200,
        "unit": "pts",
    },
    # Crypto — tradeable when structure is clear
    "BTCUSD": {"max_lots": 0.01, "min_sl": 100, "max_sl": 2000, "unit": "pts"},
    "ETHUSD": {"max_lots": 0.01, "min_sl": 20, "max_sl": 500, "unit": "pts"},
    # Platinum
    "XPTUSD": {"max_lots": 0.05, "min_sl": 5, "max_sl": 50, "unit": "pts"},
    # Swing stocks — require --swing flag
    "NVIDIA": {"swing_only": True},
    "INTEL": {"swing_only": True},
    "AMD": {"swing_only": True},
    "APPLE": {"swing_only": True},
    "MICROSOFT": {"swing_only": True},
    "META": {"swing_only": True},
    "AMAZON": {"swing_only": True},
    "TAIWANSEMI": {"swing_only": True},
    "LOCKHEED": {"swing_only": True},
    "NORTHROP": {"swing_only": True},
    "BOEING": {"swing_only": True},
    "EXXON": {"swing_only": True},
    "CHEVRON": {"swing_only": True},
    "BP": {"swing_only": True},
    "JPMORGAN": {"swing_only": True},
    "GOLDMAN": {"swing_only": True},
    "MICRON": {"swing_only": True},
}

# Instruments with known liquidity or structural issues — never trade
BANNED_ALWAYS: set = {"NGAS"}

# R:R thresholds by macro alignment
RR_MACRO_ALIGNED = (
    1.3  # trade direction matches macro bias (e.g. USD bull + buy USDJPY)
)
RR_MACRO_NEUTRAL = 1.5  # macro is neutral or unknown
RR_MACRO_AGAINST = 2.0  # trade direction opposes macro bias (counter-trend)
RR_POST_NEWS = 1.2  # within 30 min of news print — momentum setups get easier pass

MAX_RISK_PCT = 0.20  # 20% of balance max — hard limit
MAX_RISK_ZAR = 1200.0  # absolute ZAR cap regardless of balance


def main() -> None:
    p = argparse.ArgumentParser(description="Pre-trade enforcer v3.0")
    p.add_argument("--instrument", required=True)
    p.add_argument("--direction", required=True, choices=["buy", "sell"])
    p.add_argument("--units", type=float, default=0, help="Gold units (max 1)")
    p.add_argument("--lots", type=float, default=0, help="Forex/index/crypto lots")
    p.add_argument("--balance", type=float, required=True, help="Account balance ZAR")
    p.add_argument("--account", required=True, choices=["demo", "live"])
    p.add_argument(
        "--risk_amount", type=float, required=True, help="ZAR lost if SL hits"
    )
    p.add_argument(
        "--reward_amount", type=float, required=True, help="ZAR gained if TP hits"
    )
    p.add_argument("--sl_distance", type=float, required=True, help="SL in pts or pips")
    p.add_argument("--swing", action="store_true", help="Swing position flag")
    p.add_argument("--mode", default="standard", choices=["standard", "change7"])
    p.add_argument(
        "--macro_bias",
        default="neutral",
        choices=["bull", "bear", "neutral"],
        help="H4 macro direction. bull/bear = direction-aware R:R requirement",
    )
    p.add_argument(
        "--news_event",
        action="store_true",
        help="PCE/NFP/Fed day — widens SL limits by 50% for post-event setups",
    )
    p.add_argument(
        "--post_news",
        action="store_true",
        help="Entering within 30 min of news print — lowers R:R to 1.2",
    )
    args = p.parse_args()

    blocks: list[str] = []
    inst = args.instrument.upper()

    # 1. Permanently banned
    if inst in BANNED_ALWAYS:
        blocks.append(f"{inst} is banned (illiquid/structural issues). Not tradeable.")
        _exit(blocks, args)
        return

    # 2. Live account safeguard
    if args.account == "live":
        blocks.append(
            "Live account trading requires explicit 'use live account' instruction each session. "
            "Demo account is #41829612. Live is #43019560 — never touch without explicit instruction."
        )

    cfg = INSTRUMENTS.get(inst)
    if cfg is None:
        blocks.append(
            f"{inst} not in instrument config. Add it to enforcer.py before trading. "
            "Unknown instruments are unvetted for sizing and spread."
        )
        _exit(blocks, args)
        return

    # 3. Swing-only check
    if cfg.get("swing_only") and not args.swing:
        blocks.append(f"{inst} is swing-only. Add --swing flag to confirm.")

    # 4. Balance gate for indices/crypto
    if "min_balance" in cfg and args.balance < cfg["min_balance"]:
        blocks.append(
            f"{inst} requires balance ≥ R{cfg['min_balance']:.0f} "
            f"(current R{args.balance:.0f}). "
            "Post-news setups are valid but need headroom for margin + drawdown."
        )

    # 5. Gold unit cap — HARD RULE, never changes
    if "max_units" in cfg and args.units > cfg["max_units"]:
        blocks.append(
            f"{inst} max {cfg['max_units']} unit(s). Requested {args.units}. "
            "3 units = R1,042+ risk confirmed June loss. This cannot be increased."
        )

    # 6. Forex/other lot cap
    if "max_lots" in cfg and args.lots > cfg["max_lots"]:
        blocks.append(f"{inst} max {cfg['max_lots']} lots. Requested {args.lots}.")

    # 7. SL distance checks (skip for swing)
    if not args.swing and args.sl_distance > 0:
        sl_max = cfg.get("max_sl", 9999)
        sl_min = cfg.get("min_sl", 1)

        # News event day: widen SL caps by 50%
        if args.news_event:
            sl_max = sl_max * 1.5
            sl_min = max(1, sl_min * 0.5)  # noise floor still applies, halved

        # CHANGE7 mode: technical SL from pattern — min floor is just 1 to prevent nonsense
        if args.mode == "change7":
            sl_min = 1

        if args.sl_distance < sl_min:
            blocks.append(
                f"{inst} SL {args.sl_distance} {cfg.get('unit', 'units')} < "
                f"minimum {sl_min:.0f}. SL inside spread/noise — will be stopped immediately."
            )
        if args.sl_distance > sl_max:
            blocks.append(
                f"{inst} SL {args.sl_distance} {cfg.get('unit', 'units')} > "
                f"maximum {sl_max:.0f}{'×1.5 news_event' if args.news_event else ''}. "
                "SL too wide — risk amount too large for this account. "
                "Use a tighter entry point or smaller size."
            )

    # 8. SL = 0 hard block
    if args.sl_distance <= 0:
        blocks.append("SL distance is 0. No trade without a defined stop loss.")

    # 9. Risk % check
    risk_pct = args.risk_amount / args.balance if args.balance > 0 else 1.0
    if risk_pct > MAX_RISK_PCT:
        blocks.append(
            f"Risk {risk_pct * 100:.1f}% exceeds {MAX_RISK_PCT * 100:.0f}% maximum. "
            f"R{args.risk_amount:.0f} on R{args.balance:.0f} balance. Reduce size."
        )
    if args.risk_amount > MAX_RISK_ZAR:
        blocks.append(
            f"Risk R{args.risk_amount:.0f} exceeds R{MAX_RISK_ZAR:.0f} absolute cap. "
            "Max R1,200 per trade at current account size."
        )

    # 10. R:R check — adapts to macro alignment
    if args.post_news:
        min_rr = RR_POST_NEWS
        rr_context = "post_news momentum"
    elif args.macro_bias == "bull" and args.direction == "buy":
        min_rr = RR_MACRO_ALIGNED
        rr_context = "macro aligned (bull+buy)"
    elif args.macro_bias == "bear" and args.direction == "sell":
        min_rr = RR_MACRO_ALIGNED
        rr_context = "macro aligned (bear+sell)"
    elif args.macro_bias in ("bull", "bear"):
        min_rr = RR_MACRO_AGAINST
        rr_context = "macro opposed — counter-trend requires 2.0 R:R"
    else:
        min_rr = RR_MACRO_NEUTRAL
        rr_context = "neutral/unknown macro"

    rr = args.reward_amount / args.risk_amount if args.risk_amount > 0 else 0.0
    if rr < min_rr:
        blocks.append(
            f"R:R {rr:.2f}:1 below {min_rr}:1 minimum ({rr_context}). "
            "Move TP further out or tighten SL if structure allows."
        )

    _exit(blocks, args)


def _exit(blocks: list, args) -> None:
    rr = args.reward_amount / args.risk_amount if args.risk_amount > 0 else 0.0
    risk_pct = args.risk_amount / args.balance if args.balance > 0 else 1.0

    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "instrument": args.instrument.upper(),
        "direction": args.direction,
        "account": args.account,
        "mode": args.mode,
        "macro_bias": getattr(args, "macro_bias", "neutral"),
        "news_event": getattr(args, "news_event", False),
        "post_news": getattr(args, "post_news", False),
        "balance_zar": args.balance,
        "units": args.units,
        "lots": args.lots,
        "sl_distance": args.sl_distance,
        "risk_amount_zar": args.risk_amount,
        "reward_amount_zar": args.reward_amount,
        "risk_pct": round(risk_pct * 100, 2),
        "rr": round(rr, 2),
        "swing": getattr(args, "swing", False),
        "verdict": "BLOCKED" if blocks else "PASS",
        "block_reasons": blocks,
    }

    print(json.dumps(result, indent=2))

    with open("enforcer_audit.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")

    if blocks:
        print(f"\n=== ENFORCER: BLOCKED ({len(blocks)} reason(s)) ===")
        for i, b in enumerate(blocks, 1):
            print(f"{i}. {b}")
        print("Trade NOT placed.")
    else:
        print("\n=== ENFORCER: PASS — trade may proceed ===")

    sys.exit(1 if blocks else 0)


if __name__ == "__main__":
    main()

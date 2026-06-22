#!/usr/bin/env python3
"""
MASTER SCANNER v1.0
Runs at session start and every hour. Scores all tradeable instruments,
writes top-10 watchlist to watchlist.json for the monitoring loop.

Claude calls this by running the scan sequence via MCP, then passing
results here to score and persist. This script handles the scoring logic
and watchlist persistence — Claude handles the MCP data fetching.

Usage (Claude pipes JSON data in):
  python3 master_scan.py --mode score --data '[{"symbol":"XAUUSD","h4_trend":"bull","h4_strength":8,"h1_pullback":true,"news_catalyst":"war_escalation","news_direction":"long","session_fit":true,"rr_potential":2.5}]'
  python3 master_scan.py --mode read
  python3 master_scan.py --mode add --symbol XAUUSD --score 9 --direction long --reason "H4 bull + war catalyst" --entry 4181 --sl 4161 --tp 4220
  python3 master_scan.py --mode clear

Scoring system (0-10):
  H4 trend confirmed (CHANGE 2 standard):  +3
  H1 pullback/consolidation present:        +2
  News catalyst aligned with direction:     +3
  Session match:                            +1
  R:R potential >= 2:1:                     +1
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WATCHLIST_FILE = "watchlist.json"

# All tradeable instruments by category (from ThinkMarkets get_all_trading_instruments)
INSTRUMENT_UNIVERSE = {
    "forex_major": [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "USDCHF",
        "AUDUSD",
        "NZDUSD",
        "USDCAD",
        "EURGBP",
        "EURJPY",
        "GBPJPY",
        "AUDJPY",
        "EURAUD",
        "EURCHF",
        "GBPCHF",
        "GBPAUD",
        "USDSGD",
        "EURCAD",
        "GBPCAD",
        "NZDJPY",
        "AUDCAD",
    ],
    "forex_exotic": [
        "USDZAR",
        "EURZAR",
        "USDTRY",
        "USDMXN",
        "USDBRL",
        "USDCNH",
    ],
    "metals": [
        "XAUUSD",
        "XAGUSD",
        "XPTUSD",
    ],
    "indices": [
        "NAS100",
        "SPX500",
        "US30",
        "UK100",
        "GER40",
        "FRA40",
        "JPN225",
        "AUS200",
        "ZAR40",
        "HK50",
        "CHINA50",
    ],
    "energy": [
        "BRENT",
        "NGAS",
        # WTI permanently banned
    ],
    "tech_stocks": [
        "NVIDIA",
        "AMD",
        "APPLE",
        "MICROSOFT",
        "META",
        "AMAZON",
        "INTEL",
        "TAIWANSEMI",
    ],
    "defense_stocks": [
        "LOCKHEED",
        "NORTHROP",
        "BOEING",
    ],
    "energy_stocks": [
        "EXXON",
        "CHEVRON",
        "BP",
    ],
    "financial_stocks": [
        "JPMORGAN",
        "GOLDMAN",
    ],
}

# News event → affected instruments and direction
NEWS_IMPACT_MAP = {
    "war_escalation": {
        "long": [
            "XAUUSD",
            "XAGUSD",
            "USDJPY_inverse",
            "USDCHF",
            "LOCKHEED",
            "NORTHROP",
            "BOEING",
        ],
        "short": ["EURUSD", "GBPUSD", "EURJPY", "risk_indices"],
        "notes": "War escalation = safe haven demand. Gold, CHF, JPY up. Risk assets down.",
    },
    "peace_talks": {
        "long": ["EURUSD", "GBPUSD", "risk_indices", "BRENT"],
        "short": ["XAUUSD", "USDCHF"],
        "notes": "Peace progress = risk-on. Gold drops, risk assets rally.",
    },
    "sanctions": {
        "long": ["XAUUSD", "BRENT"],
        "short": ["affected_currency"],
        "notes": "Sanctions = commodity shock + safe haven. Depends on who is sanctioned.",
    },
    "cpi_hot": {
        "long": ["USDJPY", "USDCHF", "USDCAD"],
        "short": ["XAUUSD", "EURUSD", "GBPUSD", "NAS100", "SPX500"],
        "notes": "Hot CPI = rate hike fears. USD up, Gold down, indices down.",
    },
    "cpi_cool": {
        "long": ["XAUUSD", "EURUSD", "GBPUSD", "NAS100", "SPX500"],
        "short": ["USDJPY", "USDCAD"],
        "notes": "Cool CPI = rate cut hopes. Gold up, USD down, indices up.",
    },
    "nfp_beat": {
        "long": ["USDJPY", "USDCAD", "USDCHF"],
        "short": ["XAUUSD", "EURUSD", "GBPUSD"],
        "notes": "Strong jobs = USD up, Gold down. Do NOT trade INTO NFP — wait for M15 compression after.",
    },
    "nfp_miss": {
        "long": ["XAUUSD", "EURUSD", "GBPUSD"],
        "short": ["USDJPY", "USDCAD"],
        "notes": "Weak jobs = USD down, Gold up.",
    },
    "fed_hawkish": {
        "long": ["USDJPY", "USDCHF", "USDCAD"],
        "short": ["XAUUSD", "EURUSD", "GBPUSD", "NAS100"],
        "notes": "Rate hike signal = USD up, Gold down, tech stocks down.",
    },
    "fed_dovish": {
        "long": ["XAUUSD", "EURUSD", "GBPUSD", "NAS100", "SPX500"],
        "short": ["USDJPY", "USDCAD"],
        "notes": "Rate cut signal = Gold up, USD down, indices up.",
    },
    "oil_supply_shock": {
        "long": ["BRENT", "EXXON", "CHEVRON", "BP", "USDCAD"],
        "short": ["EURUSD", "GBPUSD"],
        "notes": "Oil supply cut = BRENT up, CAD up (oil exporter), EUR down.",
    },
    "tech_earnings_beat": {
        "long": ["NVIDIA", "AMD", "APPLE", "MICROSOFT", "META", "NAS100"],
        "short": [],
        "notes": "Earnings beat = long the stock + NAS100 halo effect.",
    },
    "tech_earnings_miss": {
        "long": [],
        "short": ["NVIDIA", "AMD", "APPLE", "MICROSOFT", "META", "NAS100"],
        "notes": "Earnings miss = short the stock + NAS100 drag.",
    },
    "defense_contract_win": {
        "long": ["LOCKHEED", "NORTHROP", "BOEING"],
        "short": [],
        "notes": "Major defense contract = long the winner.",
    },
    "ai_breakthrough": {
        "long": ["NVIDIA", "AMD", "MICROSOFT", "TAIWANSEMI", "NAS100"],
        "short": [],
        "notes": "AI news = GPU/chip stocks up, NAS100 up.",
    },
    "risk_off_generic": {
        "long": ["XAUUSD", "USDCHF", "USDJPY"],
        "short": ["EURUSD", "GBPUSD", "NAS100", "SPX500", "AUS200"],
        "notes": "General risk-off = safe havens up, risk assets down.",
    },
    "risk_on_generic": {
        "long": ["EURUSD", "GBPUSD", "NAS100", "SPX500", "AUDUSD"],
        "short": ["XAUUSD", "USDCHF"],
        "notes": "General risk-on = risk assets up, safe havens down.",
    },
}


def score_instrument(data: dict) -> int:
    score = 0
    if data.get("h4_trend_confirmed"):
        score += 3
    if data.get("h1_pullback"):
        score += 2
    if data.get("news_catalyst_aligned"):
        score += 3
    if data.get("session_fit"):
        score += 1
    if data.get("rr_potential", 0) >= 2.0:
        score += 1
    return score


def load_watchlist() -> dict:
    try:
        return json.loads(Path(WATCHLIST_FILE).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"generated_at": None, "watchlist": [], "news_events": []}


def save_watchlist(data: dict) -> None:
    Path(WATCHLIST_FILE).write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode")

    # Read current watchlist
    sub.add_parser("read", help="Print current watchlist")

    # Clear watchlist
    sub.add_parser("clear", help="Clear watchlist for new hour")

    # Add a scored instrument to watchlist
    add_p = sub.add_parser("add", help="Add instrument to watchlist")
    add_p.add_argument("--symbol", required=True)
    add_p.add_argument("--score", type=int, required=True)
    add_p.add_argument("--direction", required=True, choices=["long", "short"])
    add_p.add_argument("--reason", required=True)
    add_p.add_argument("--entry", type=float, required=True)
    add_p.add_argument("--sl", type=float, required=True)
    add_p.add_argument("--tp", type=float, required=True)
    add_p.add_argument("--category", default="unknown")

    # Set active news events
    news_p = sub.add_parser("news", help="Set current news events")
    news_p.add_argument(
        "--events",
        required=True,
        help="Comma-separated event keys from NEWS_IMPACT_MAP",
    )

    # Print the impact map for a news event
    impact_p = sub.add_parser("impact", help="Show market impact for a news event")
    impact_p.add_argument("--event", required=True)

    # Print full universe
    sub.add_parser("universe", help="Print all tradeable instruments by category")

    args = p.parse_args()

    if args.mode == "read":
        wl = load_watchlist()
        if not wl["watchlist"]:
            print("Watchlist is empty. Run master scan first.")
        else:
            print(f"\n=== WATCHLIST (generated {wl.get('generated_at', '?')}) ===")
            if wl.get("news_events"):
                print(f"Active news events: {', '.join(wl['news_events'])}")
            for i, item in enumerate(wl["watchlist"], 1):
                print(
                    f"{i:2}. [{item['score']:2}/10] {item['symbol']:12} "
                    f"{item['direction'].upper():5} | {item['reason']}"
                )
                print(
                    f"     Entry ~{item['entry']} | SL {item['sl']} | TP {item['tp']}"
                )

    elif args.mode == "clear":
        save_watchlist({"generated_at": None, "watchlist": [], "news_events": []})
        print("Watchlist cleared.")

    elif args.mode == "add":
        wl = load_watchlist()
        wl["generated_at"] = datetime.now(timezone.utc).isoformat()
        entry = {
            "symbol": args.symbol.upper(),
            "score": args.score,
            "direction": args.direction,
            "reason": args.reason,
            "entry": args.entry,
            "sl": args.sl,
            "tp": args.tp,
            "category": args.category,
            "added_at": datetime.now(timezone.utc).isoformat(),
        }
        # Remove existing entry for same symbol if present
        wl["watchlist"] = [
            x for x in wl["watchlist"] if x["symbol"] != args.symbol.upper()
        ]
        wl["watchlist"].append(entry)
        # Keep top 10 by score
        wl["watchlist"] = sorted(
            wl["watchlist"], key=lambda x: x["score"], reverse=True
        )[:10]
        save_watchlist(wl)
        print(
            f"Added {args.symbol} (score {args.score}/10) to watchlist. "
            f"Total: {len(wl['watchlist'])} instruments."
        )

    elif args.mode == "news":
        events = [e.strip() for e in args.events.split(",")]
        valid = [e for e in events if e in NEWS_IMPACT_MAP]
        invalid = [e for e in events if e not in NEWS_IMPACT_MAP]
        if invalid:
            print(f"Unknown events (ignored): {invalid}")
            print(f"Valid event keys: {list(NEWS_IMPACT_MAP.keys())}")
        wl = load_watchlist()
        wl["news_events"] = valid
        save_watchlist(wl)
        print(f"News events set: {valid}")
        for event in valid:
            impact = NEWS_IMPACT_MAP[event]
            print(f"\n  {event}:")
            print(f"    LONG:  {impact['long']}")
            print(f"    SHORT: {impact['short']}")
            print(f"    Notes: {impact['notes']}")

    elif args.mode == "impact":
        event = args.event
        if event not in NEWS_IMPACT_MAP:
            print(f"Unknown event: {event}")
            print(f"Valid keys: {list(NEWS_IMPACT_MAP.keys())}")
            sys.exit(1)
        impact = NEWS_IMPACT_MAP[event]
        print(f"\n=== NEWS IMPACT: {event} ===")
        print(f"LONG these:  {impact['long']}")
        print(f"SHORT these: {impact['short']}")
        print(f"Notes: {impact['notes']}")

    elif args.mode == "universe":
        print("\n=== TRADEABLE INSTRUMENT UNIVERSE ===")
        total = 0
        for category, symbols in INSTRUMENT_UNIVERSE.items():
            print(f"\n{category.upper()} ({len(symbols)}):")
            print("  " + ", ".join(symbols))
            total += len(symbols)
        print(
            f"\nTotal: {total} instruments across {len(INSTRUMENT_UNIVERSE)} categories"
        )

    else:
        p.print_help()


if __name__ == "__main__":
    main()

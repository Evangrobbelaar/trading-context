#!/usr/bin/env python3
"""
NEWS SCANNER v1.0
Live news fetcher and market impact categorizer.

Claude calls web_search to get news, then pipes results here to categorize
events using NEWS_IMPACT_MAP keys and persist to news_impact.json.
The master scan reads news_impact.json to boost scores for catalyst-aligned instruments.

Usage:
  # Set active events from web search results
  python3 news_scanner.py set --events "war_escalation,fed_hawkish"

  # Read current impact state
  python3 news_scanner.py read

  # Check if a specific instrument has a news catalyst right now
  python3 news_scanner.py check --symbol XAUUSD --direction long

  # Clear (called at start of each hourly master scan)
  python3 news_scanner.py clear

  # List all known event keys
  python3 news_scanner.py events
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

NEWS_IMPACT_FILE = "news_impact.json"

# Mirror of NEWS_IMPACT_MAP in master_scan.py — single source of truth here,
# master_scan.py imports these at runtime (or references its own copy).
NEWS_IMPACT_MAP: dict = {
    "war_escalation": {
        "long": ["XAUUSD", "XAGUSD", "USDCHF", "LOCKHEED", "NORTHROP", "BOEING"],
        "short": ["EURUSD", "GBPUSD", "EURJPY", "NAS100", "SPX500", "AUS200"],
        "notes": "War/conflict escalation = safe haven bid. Gold, CHF up. Risk assets, EUR down.",
        "urgency": "high",
    },
    "peace_talks": {
        "long": ["EURUSD", "GBPUSD", "NAS100", "SPX500", "AUS200"],
        "short": ["XAUUSD", "USDCHF", "BRENT", "LOCKHEED", "NORTHROP"],
        "notes": "Peace progress = risk-on. Gold and defense stocks drop, risk assets rally. BRENT SHORT: ME peace = Strait of Hormuz reopens = more supply = lower oil (confirmed June 22 2026: BRENT -1.7% on US-Iran deal).",
        "urgency": "medium",
    },
    "sanctions_announced": {
        "long": ["XAUUSD", "BRENT", "EXXON", "CHEVRON"],
        "short": [],
        "notes": "Sanctions = commodity shock + safe haven. Context-dependent on target.",
        "urgency": "high",
    },
    "cpi_hot": {
        "long": ["USDJPY", "USDCHF", "USDCAD"],
        "short": ["XAUUSD", "EURUSD", "GBPUSD", "NAS100", "SPX500"],
        "notes": "Hot CPI = rate hike fears. USD strengthens. Wait for M15 compression after print.",
        "urgency": "high",
    },
    "cpi_cool": {
        "long": ["XAUUSD", "EURUSD", "GBPUSD", "NAS100", "SPX500"],
        "short": ["USDJPY", "USDCAD"],
        "notes": "Cool CPI = rate cut hopes. Gold and indices rally. USD weakens.",
        "urgency": "high",
    },
    "nfp_beat": {
        "long": ["USDJPY", "USDCAD", "USDCHF"],
        "short": ["XAUUSD", "EURUSD", "GBPUSD"],
        "notes": "Strong NFP = USD up, Gold down. DO NOT trade INTO the print. Wait M15 settlement.",
        "urgency": "high",
    },
    "nfp_miss": {
        "long": ["XAUUSD", "EURUSD", "GBPUSD"],
        "short": ["USDJPY", "USDCAD"],
        "notes": "Weak NFP = USD down, Gold up. Wait for M15 structure after release.",
        "urgency": "high",
    },
    "fed_hawkish": {
        "long": ["USDJPY", "USDCHF", "USDCAD"],
        "short": ["XAUUSD", "EURUSD", "GBPUSD", "NAS100"],
        "notes": "Rate hike signal or hawkish Fed speak = USD up, tech and Gold down.",
        "urgency": "medium",
    },
    "fed_dovish": {
        "long": ["XAUUSD", "EURUSD", "GBPUSD", "NAS100", "SPX500"],
        "short": ["USDJPY", "USDCAD"],
        "notes": "Rate cut signal or dovish Fed speak = Gold and indices up, USD weakens.",
        "urgency": "medium",
    },
    "oil_supply_shock": {
        "long": ["BRENT", "EXXON", "CHEVRON", "BP", "USDCAD"],
        "short": ["EURUSD", "GBPUSD", "AUDUSD"],
        "notes": "OPEC cut, supply disruption = BRENT spikes, CAD and oil stocks up.",
        "urgency": "medium",
    },
    "tech_earnings_beat": {
        "long": ["NVIDIA", "AMD", "APPLE", "MICROSOFT", "META", "AMAZON", "NAS100"],
        "short": [],
        "notes": "Earnings beat = long the reporting stock + NAS100 halo. Check which company.",
        "urgency": "medium",
    },
    "tech_earnings_miss": {
        "long": [],
        "short": ["NVIDIA", "AMD", "APPLE", "MICROSOFT", "META", "AMAZON", "NAS100"],
        "notes": "Earnings miss = short the reporting stock + NAS100 drag effect.",
        "urgency": "medium",
    },
    "defense_contract_win": {
        "long": ["LOCKHEED", "NORTHROP", "BOEING"],
        "short": [],
        "notes": "Major defense contract awarded = long the winner. Check contract size.",
        "urgency": "low",
    },
    "ai_breakthrough": {
        "long": ["NVIDIA", "AMD", "MICROSOFT", "TAIWANSEMI", "NAS100"],
        "short": [],
        "notes": "AI product launch or breakthrough = GPU/chip stocks and NAS100 up.",
        "urgency": "medium",
    },
    "risk_off_generic": {
        "long": ["XAUUSD", "USDCHF", "USDJPY"],
        "short": ["EURUSD", "GBPUSD", "NAS100", "SPX500", "AUS200", "AUDUSD"],
        "notes": "Generic risk-off: market uncertainty, no specific catalyst identified.",
        "urgency": "medium",
    },
    "risk_on_generic": {
        "long": ["EURUSD", "GBPUSD", "NAS100", "SPX500", "AUDUSD"],
        "short": ["XAUUSD", "USDCHF"],
        "notes": "Generic risk-on: positive sentiment, no specific catalyst identified.",
        "urgency": "medium",
    },
    "ceasefire": {
        "long": ["EURUSD", "GBPUSD", "NAS100", "AUS200"],
        "short": ["XAUUSD", "LOCKHEED", "NORTHROP"],
        "notes": "Ceasefire = sharp risk-on, safe havens and defense stocks fall.",
        "urgency": "high",
    },
    "missile_strike": {
        "long": ["XAUUSD", "XAGUSD", "USDCHF", "LOCKHEED", "NORTHROP", "BRENT"],
        "short": ["EURUSD", "GBPUSD", "NAS100", "SPX500"],
        "notes": "Active strike or attack = immediate safe haven spike. High volatility — wait for M15 structure.",
        "urgency": "high",
    },
    "central_bank_rate_hike": {
        "long": ["the_hiking_currency_pairs"],
        "short": ["the_hiking_currency_pairs_inverse"],
        "notes": "Check which CB is hiking. USD hike = USD pairs up. ECB hike = EUR up. etc.",
        "urgency": "high",
    },
    "inflation_data_uk_eu": {
        "long": [],
        "short": [],
        "notes": "UK CPI = GBP impact. EU CPI = EUR impact. Map to cpi_hot or cpi_cool.",
        "urgency": "medium",
    },
}

# Instruments that are HIGH volatility around news — need wider SL or wait-for-structure
HIGH_VOLATILITY_ON_NEWS = {
    "XAUUSD": "Gold spikes 30-60pts in seconds on major news. DO NOT enter during spike.",
    "USDJPY": "JPY gaps on BoJ surprise decisions.",
    "GBPUSD": "Cable volatile on UK CPI/BOE decisions.",
    "NAS100": "Tech index spikes on Fed and earnings.",
    "BRENT": "Oil gaps on OPEC and geopolitical supply news.",
}


def load_impact() -> dict:
    try:
        return json.loads(Path(NEWS_IMPACT_FILE).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {
            "last_scan_utc": None,
            "active_events": [],
            "instruments_long": [],
            "instruments_short": [],
            "headlines": [],
            "high_impact_within_2h": False,
        }


def save_impact(data: dict) -> None:
    Path(NEWS_IMPACT_FILE).write_text(json.dumps(data, indent=2), encoding="utf-8")


def build_instrument_lists(active_events: list) -> tuple[list, list]:
    """Aggregate long/short lists across all active events."""
    longs: set = set()
    shorts: set = set()
    for event in active_events:
        if event in NEWS_IMPACT_MAP:
            longs.update(NEWS_IMPACT_MAP[event]["long"])
            shorts.update(NEWS_IMPACT_MAP[event]["short"])
    # Remove instruments that appear in both (conflicting signals = no edge)
    conflicted = longs & shorts
    longs -= conflicted
    shorts -= conflicted
    return sorted(longs), sorted(shorts)


def main() -> None:
    p = argparse.ArgumentParser(description="News Scanner — live event impact tracker")
    sub = p.add_subparsers(dest="cmd")

    # Set events
    set_p = sub.add_parser("set", help="Set active news events and rebuild impact list")
    set_p.add_argument(
        "--events",
        required=True,
        help="Comma-separated event keys (from 'events' subcommand)",
    )
    set_p.add_argument(
        "--headlines",
        default="",
        help="Brief summary of news headlines for the log",
    )
    set_p.add_argument(
        "--high_impact_2h",
        action="store_true",
        help="Flag if a high-impact scheduled event fires within 2 hours",
    )

    # Read current state
    sub.add_parser("read", help="Print current news impact state")

    # Clear
    sub.add_parser("clear", help="Clear news state (call at start of each hour)")

    # Check if an instrument/direction has news support
    check_p = sub.add_parser("check", help="Check if instrument has news catalyst")
    check_p.add_argument("--symbol", required=True)
    check_p.add_argument("--direction", required=True, choices=["long", "short"])

    # List known event keys
    sub.add_parser("events", help="List all known event keys and their impacts")

    # Volatility warning for instrument
    vol_p = sub.add_parser("volatility", help="Check if instrument is high-vol on news")
    vol_p.add_argument("--symbol", required=True)

    args = p.parse_args()

    if args.cmd == "set":
        events = [e.strip() for e in args.events.split(",") if e.strip()]
        valid = [e for e in events if e in NEWS_IMPACT_MAP]
        invalid = [e for e in events if e not in NEWS_IMPACT_MAP]

        if invalid:
            print(f"WARNING: Unknown events (ignored): {invalid}")
            print(f"Valid event keys: {list(NEWS_IMPACT_MAP.keys())}")

        longs, shorts = build_instrument_lists(valid)
        headlines = [h.strip() for h in args.headlines.split("|") if h.strip()]

        state = {
            "last_scan_utc": datetime.now(timezone.utc).isoformat(),
            "active_events": valid,
            "instruments_long": longs,
            "instruments_short": shorts,
            "headlines": headlines,
            "high_impact_within_2h": args.high_impact_2h,
        }
        save_impact(state)

        print("\n=== NEWS IMPACT UPDATED ===")
        print(f"Events: {valid}")
        print(f"LONG these instruments: {longs}")
        print(f"SHORT these instruments: {shorts}")
        if args.high_impact_2h:
            print("⚠ HIGH-IMPACT EVENT WITHIN 2 HOURS — wait for structure after print")
        if invalid:
            print(f"Ignored unknown events: {invalid}")

    elif args.cmd == "read":
        state = load_impact()
        if not state["active_events"]:
            print("No active news events. Run news_scanner.py set --events <keys>")
            return

        print(
            f"\n=== CURRENT NEWS IMPACT (scanned {state.get('last_scan_utc', '?')}) ==="
        )
        print(f"Active events: {', '.join(state['active_events'])}")
        if state.get("headlines"):
            print(f"Headlines: {' | '.join(state['headlines'])}")
        print(f"\nLONG catalyst: {state['instruments_long']}")
        print(f"SHORT catalyst: {state['instruments_short']}")
        if state.get("high_impact_within_2h"):
            print(
                "\n⚠ HIGH-IMPACT EVENT WITHIN 2 HOURS — wait for M15 structure after print"
            )

    elif args.cmd == "clear":
        save_impact(
            {
                "last_scan_utc": None,
                "active_events": [],
                "instruments_long": [],
                "instruments_short": [],
                "headlines": [],
                "high_impact_within_2h": False,
            }
        )
        print("News impact state cleared.")

    elif args.cmd == "check":
        state = load_impact()
        sym = args.symbol.upper()
        direction = args.direction.lower()

        key = "instruments_long" if direction == "long" else "instruments_short"
        has_catalyst = sym in state.get(key, [])

        if has_catalyst:
            events_supporting = [
                e
                for e in state["active_events"]
                if sym in NEWS_IMPACT_MAP.get(e, {}).get(direction, [])
            ]
            print(f"CATALYST: {sym} {direction.upper()} has news support")
            print(f"Supporting events: {events_supporting}")
            print("Score boost: +3 points (news_catalyst_aligned = True)")
        else:
            # Check if it's on the opposing side (conflicting catalyst)
            opposing_key = (
                "instruments_short" if direction == "long" else "instruments_long"
            )
            if sym in state.get(opposing_key, []):
                print(
                    f"CONFLICT: {sym} has news catalyst pointing AGAINST {direction.upper()}"
                )
                print("Do NOT trade this direction — news is against you.")
                sys.exit(2)
            else:
                print(f"NEUTRAL: {sym} has no news catalyst for {direction.upper()}")
                print("Score boost: +0 (no catalyst, not blocked)")

        if sym in HIGH_VOLATILITY_ON_NEWS and state.get("high_impact_within_2h"):
            print(f"\n⚠ {sym}: {HIGH_VOLATILITY_ON_NEWS[sym]}")

    elif args.cmd == "events":
        print("\n=== KNOWN NEWS EVENT KEYS ===")
        for key, data in NEWS_IMPACT_MAP.items():
            urgency = data.get("urgency", "medium").upper()
            print(f"\n[{urgency}] {key}")
            print(
                f"  LONG:  {data['long'][:5]}{'...' if len(data['long']) > 5 else ''}"
            )
            print(
                f"  SHORT: {data['short'][:5]}{'...' if len(data['short']) > 5 else ''}"
            )
            print(f"  Notes: {data['notes']}")

    elif args.cmd == "volatility":
        sym = args.symbol.upper()
        if sym in HIGH_VOLATILITY_ON_NEWS:
            print(f"⚠ {sym}: {HIGH_VOLATILITY_ON_NEWS[sym]}")
        else:
            print(f"{sym}: No special volatility warning on news events.")

    else:
        p.print_help()


if __name__ == "__main__":
    main()

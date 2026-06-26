#!/usr/bin/env python3
"""
H4 cache manager — saves Claude from re-fetching H4 candles on every tick.

H4 candles close every 4 hours (UTC: 00, 04, 08, 12, 16, 20).
Cache for a symbol is valid until the NEXT H4 boundary after it was written —
so a cache written at 09:15 UTC expires at 12:00 UTC (not 4 hours later).

Workflow:
  1. Claude runs: python h4_updater.py --check
     → See which symbols are stale and need fetching via MCP

  2. Claude fetches stale symbols via MCP get_symbol_history (timeframeMinutes=240, limit=6)
     → Writes bar strings to h4_temp.json  (format: list of "YYYY-MM-DD HH:MM|O|H|L|C|V")
     → Then calls: python h4_updater.py --write --symbol EURUSD --trend bear
                       --evidence "LH at 1.1440 vs HH 1.1487, swing low 1.1375 broken"

  3. Next tick: python h4_updater.py --read-all
     → Claude gets all trends without any MCP calls

Usage:
  python h4_updater.py --check
  python h4_updater.py --write --symbol EURUSD --trend bear --evidence "..."
  python h4_updater.py --read --symbol EURUSD
  python h4_updater.py --read-all
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

CACHE_FILE = Path("h4_cache.json")
TEMP_FILE = Path("h4_temp.json")

SCAN_LIST = [
    "XAUUSD",
    "XAGUSD",
    "BRENT",
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCHF",
    "AUDUSD",
    "NZDUSD",
    "NAS100",
    "SPX500",
]


def next_h4_boundary(dt: datetime) -> datetime:
    """Next H4 UTC candle close strictly after dt."""
    h4_hour = (dt.hour // 4 + 1) * 4
    base = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return base + timedelta(hours=h4_hour)


def load() -> dict:
    return (
        json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        if CACHE_FILE.exists()
        else {}
    )


def save(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def is_stale(entry: dict) -> bool:
    expires = datetime.fromisoformat(entry["expires_at"])
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) >= expires


def age_minutes(entry: dict) -> int:
    cached = datetime.fromisoformat(entry["cached_at"])
    if cached.tzinfo is None:
        cached = cached.replace(tzinfo=timezone.utc)
    return round((datetime.now(timezone.utc) - cached).total_seconds() / 60)


def main() -> None:
    p = argparse.ArgumentParser(description="H4 cache manager")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--check",
        action="store_true",
        help="Show stale/fresh status for all scan symbols",
    )
    g.add_argument(
        "--write",
        action="store_true",
        help="Write cache entry (reads bars from h4_temp.json)",
    )
    g.add_argument("--read", action="store_true", help="Read cache for one symbol")
    g.add_argument(
        "--read-all",
        action="store_true",
        dest="read_all",
        help="Read all cached symbols",
    )
    g.add_argument(
        "--invalidate",
        action="store_true",
        help="Force-expire a symbol so it gets re-fetched next tick",
    )

    p.add_argument("--symbol", default="")
    p.add_argument(
        "--trend",
        default="",
        choices=["bull", "bear", "ranging", ""],
        help="H4 trend direction (Claude's judgment after reading candles)",
    )
    p.add_argument(
        "--evidence",
        default="",
        help="One-line H4 evidence string, e.g. 'LH at 1.1440, swing low 1.1375 broken'",
    )
    args = p.parse_args()

    cache = load()
    now = datetime.now(timezone.utc)

    # --check
    if args.check:
        stale, fresh = [], []
        for sym in SCAN_LIST:
            e = cache.get(sym)
            (stale if (not e or is_stale(e)) else fresh).append(sym)
        out = {
            "stale": stale,
            "fresh": {
                s: {"trend": cache[s]["trend"], "age_min": age_minutes(cache[s])}
                for s in fresh
            },
            "stale_count": len(stale),
            "fresh_count": len(fresh),
            "action": f"Fetch H4 via MCP for: {', '.join(stale)}"
            if stale
            else "All H4 cache fresh — no MCP calls needed",
        }
        print(json.dumps(out, indent=2))

    # --write
    elif args.write:
        sym = args.symbol.upper()
        if not sym:
            print(json.dumps({"error": "--symbol required for --write"}))
            sys.exit(1)

        bars = []
        if TEMP_FILE.exists():
            raw = json.loads(TEMP_FILE.read_text(encoding="utf-8"))
            bars = raw if isinstance(raw, list) else raw.get(sym, raw.get("bars", []))

        expires = next_h4_boundary(now)
        cache[sym] = {
            "trend": args.trend,
            "evidence": args.evidence,
            "bars": bars,
            "cached_at": now.isoformat(),
            "expires_at": expires.isoformat(),
        }
        save(cache)
        print(
            json.dumps(
                {
                    "ok": True,
                    "symbol": sym,
                    "trend": args.trend,
                    "expires_at": expires.isoformat(),
                    "bars_stored": len(bars),
                }
            )
        )

    # --read
    elif args.read:
        sym = args.symbol.upper()
        e = cache.get(sym)
        if not e:
            print(
                json.dumps(
                    {"found": False, "symbol": sym, "action": "fetch_h4_via_mcp"}
                )
            )
        else:
            print(
                json.dumps(
                    {
                        "found": True,
                        "symbol": sym,
                        "trend": e["trend"],
                        "evidence": e["evidence"],
                        "bars": e.get("bars", []),
                        "age_min": age_minutes(e),
                        "expired": is_stale(e),
                    }
                )
            )

    # --read-all
    elif args.read_all:
        out = {}
        for sym, e in cache.items():
            out[sym] = {
                "trend": e["trend"],
                "evidence": e["evidence"],
                "age_min": age_minutes(e),
                "expired": is_stale(e),
            }
        print(json.dumps(out, indent=2))

    # --invalidate
    elif args.invalidate:
        sym = args.symbol.upper()
        if sym and sym in cache:
            cache[sym]["expires_at"] = now.isoformat()
            save(cache)
            print(
                json.dumps(
                    {
                        "ok": True,
                        "symbol": sym,
                        "message": "Force-expired — will re-fetch next tick",
                    }
                )
            )
        else:
            print(
                json.dumps(
                    {"ok": False, "symbol": sym, "message": "Symbol not in cache"}
                )
            )


if __name__ == "__main__":
    main()

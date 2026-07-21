#!/usr/bin/env python3
"""
M15 cache manager — saves Claude from re-fetching M15 candles on every tick.

M15 candles close every 15 minutes. Cache expires at the next 15-min boundary
after it was written, so a cache written at 09:12 UTC expires at 09:15 UTC.

Workflow:
  1. Claude runs: python m15_updater.py --check --symbols EURUSD,GBPUSD,AUDUSD
     → See which symbols have stale M15 cache

  2. Claude fetches stale symbols via MCP get_symbol_history (timeframeMinutes=15, limit=8)
     → Writes bar strings to m15_temp.json (format: {"EURUSD": ["bar1", "bar2", ...], ...})
     → Then calls: python m15_updater.py --write --symbol EURUSD

  3. Claude reads from cache instead of re-fetching:
     python m15_updater.py --read --symbol EURUSD
     → Returns last 8 bars + quick structure summary

Usage:
  python m15_updater.py --check --symbols EURUSD,GBPUSD,AUDUSD
  python m15_updater.py --write --symbol EURUSD
  python m15_updater.py --read --symbol EURUSD
  python m15_updater.py --invalidate --symbol EURUSD
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

CACHE_FILE = Path("m15_cache.json")
TEMP_FILE = Path("m15_temp.json")


def next_m15_boundary(dt: datetime) -> datetime:
    """Next 15-min UTC boundary strictly after dt."""
    minute = (dt.minute // 15 + 1) * 15
    base = dt.replace(minute=0, second=0, microsecond=0)
    return base + timedelta(minutes=minute)


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


def age_seconds(entry: dict) -> int:
    cached = datetime.fromisoformat(entry["cached_at"])
    if cached.tzinfo is None:
        cached = cached.replace(tzinfo=timezone.utc)
    return round((datetime.now(timezone.utc) - cached).total_seconds())


def parse_bar(bar_str: str) -> dict:
    """Parse 'YYYY-MM-DD HH:MM|O|H|L|C|V' into a dict."""
    try:
        ts, o, h, l, c, *v = bar_str.split("|")
        return {
            "time": ts,
            "open": float(o),
            "high": float(h),
            "low": float(l),
            "close": float(c),
        }
    except Exception:
        return {}


def quick_structure(bars: list) -> dict:
    """
    Compute a quick M15 structure summary from raw bar strings.
    Returns the most recent swing high, swing low, and direction of last 3 closes.
    Claude uses this to skip re-reading all 8 candles when nothing changed.
    """
    parsed = [parse_bar(b) for b in bars if b]
    parsed = [b for b in parsed if b]
    if len(parsed) < 3:
        return {"summary": "insufficient_bars"}

    highs = [b["high"] for b in parsed]
    lows = [b["low"] for b in parsed]
    closes = [b["close"] for b in parsed]

    recent_closes = closes[-3:]
    if recent_closes[-1] > recent_closes[0]:
        direction = "rising"
    elif recent_closes[-1] < recent_closes[0]:
        direction = "falling"
    else:
        direction = "flat"

    return {
        "last_bar_time": parsed[-1]["time"],
        "last_close": parsed[-1]["close"],
        "last_low": parsed[-1]["low"],
        "last_high": parsed[-1]["high"],
        "swing_high": max(highs),
        "swing_low": min(lows),
        "direction_3bar": direction,
        "bar_count": len(parsed),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="M15 cache manager")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="Show stale/fresh status")
    g.add_argument(
        "--write",
        action="store_true",
        help="Write cache entry (reads from m15_temp.json)",
    )
    g.add_argument("--read", action="store_true", help="Read cache for one symbol")
    g.add_argument("--invalidate", action="store_true", help="Force-expire a symbol")

    p.add_argument("--symbol", default="", help="Single symbol, e.g. EURUSD")
    p.add_argument(
        "--symbols",
        default="",
        help="Comma-separated list for --check, e.g. EURUSD,GBPUSD",
    )
    args = p.parse_args()

    cache = load()
    now = datetime.now(timezone.utc)

    # --check
    if args.check:
        syms = (
            [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
            if args.symbols
            else list(cache.keys())
        )
        stale, fresh = [], {}
        for sym in syms:
            e = cache.get(sym)
            if not e or is_stale(e):
                stale.append(sym)
            else:
                fresh[sym] = {
                    "age_sec": age_seconds(e),
                    "structure": e.get("structure", {}),
                }
        out = {
            "stale": stale,
            "fresh": fresh,
            "action": f"Fetch M15 via MCP for: {', '.join(stale)}"
            if stale
            else "M15 cache fresh",
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
            if isinstance(raw, list):
                bars = raw
            elif isinstance(raw, dict):
                bars = raw.get(sym, raw.get("bars", []))

        expires = next_m15_boundary(now)
        cache[sym] = {
            "bars": bars,
            "structure": quick_structure(bars),
            "cached_at": now.isoformat(),
            "expires_at": expires.isoformat(),
        }
        save(cache)
        print(
            json.dumps(
                {
                    "ok": True,
                    "symbol": sym,
                    "bars_stored": len(bars),
                    "structure": cache[sym]["structure"],
                    "expires_at": expires.isoformat(),
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
                    {"found": False, "symbol": sym, "action": "fetch_m15_via_mcp"}
                )
            )
        else:
            print(
                json.dumps(
                    {
                        "found": True,
                        "symbol": sym,
                        "bars": e.get("bars", []),
                        "structure": e.get("structure", {}),
                        "age_sec": age_seconds(e),
                        "expired": is_stale(e),
                    }
                )
            )

    # --invalidate
    elif args.invalidate:
        sym = args.symbol.upper()
        if sym and sym in cache:
            cache[sym]["expires_at"] = now.isoformat()
            save(cache)
            print(json.dumps({"ok": True, "symbol": sym, "message": "Force-expired"}))
        else:
            print(
                json.dumps(
                    {"ok": False, "symbol": sym, "message": "Symbol not in cache"}
                )
            )


if __name__ == "__main__":
    main()

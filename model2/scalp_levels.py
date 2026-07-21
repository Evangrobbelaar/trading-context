#!/usr/bin/env python3
"""
scalp_levels.py -- Pre-session H1 level calculator.
Run once before session. Reads scalp_candles_temp.json, writes scalp_state.json.

Workflow:
  1. Claude calls get_symbol_history (H1, 24 candles) for each symbol via MCP
  2. Claude writes the data to scalp_candles_temp.json
  3. Claude runs: python scalp_levels.py --symbol EURUSD --symbol XAUUSD ...
  4. Script writes scalp_state.json with key levels, SL/TP, status
"""

import json
import argparse
import os
from datetime import datetime, timezone, timedelta

SCALP_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCALP_DIR, "scalp_state.json")
CANDLES_TEMP = os.path.join(SCALP_DIR, "scalp_candles_temp.json")

SAST = timezone(timedelta(hours=2))

# Value of 1 pip/pt in price units
PIP = {
    "EURUSD": 0.0001,
    "GBPUSD": 0.0001,
    "USDJPY": 0.01,
    "AUDUSD": 0.0001,
    "NZDUSD": 0.0001,
    "XAUUSD": 1.0,
}

# Max distance from current price to keep a level (pips/pts)
MAX_DIST_PIPS = 30

# Default SL/TP in pips or pts
SL_PIPS = 5
TP_PIPS = 10

# Decimal places for price display
PRICE_DP = {"XAUUSD": 2}


def dp(symbol):
    return PRICE_DP.get(symbol, 5)


def pround(symbol, price):
    return round(price, dp(symbol))


def get_candle_field(candle, *keys, default=0.0):
    for k in keys:
        if k in candle:
            return float(candle[k])
    return default


def get_round_levels(symbol, price, count=4):
    """Key round numbers near current price."""
    levels = set()
    if symbol == "XAUUSD":
        for size in [10, 25, 50]:
            base = round(price / size) * size
            for i in range(-count, count + 1):
                levels.add(round(base + i * size, 2))
    elif symbol == "USDJPY":
        base = round(price * 2) / 2
        for i in range(-count, count + 1):
            levels.add(round(base + i * 0.5, 3))
    else:
        base = round(price / 0.0050) * 0.0050
        for i in range(-count, count + 1):
            levels.add(round(base + i * 0.0050, 5))
    return sorted(levels)


def count_touches(candles, level, pip, tolerance_pips=3):
    """Count H1 candles that tested this level within tolerance."""
    tol = tolerance_pips * pip
    return sum(
        1
        for c in candles
        if get_candle_field(c, "low", "l") - tol
        <= level
        <= get_candle_field(c, "high", "h") + tol
    )


def determine_h1_trend(candles):
    if len(candles) < 4:
        return "neutral"
    mid = len(candles) // 2
    closes = [get_candle_field(c, "close", "c") for c in candles]
    first_avg = sum(closes[:mid]) / mid
    last_avg = sum(closes[mid:]) / (len(candles) - mid)
    if last_avg > first_avg * 1.0002:
        return "bull"
    elif last_avg < first_avg * 0.9998:
        return "bear"
    return "neutral"


def build_level(symbol, level, direction, strength, current_price):
    pip = PIP.get(symbol, 0.0001)
    sl_dist = SL_PIPS * pip
    tp_dist = TP_PIPS * pip

    if direction == "short":
        sl = pround(symbol, level + sl_dist)
        tp = pround(symbol, level - tp_dist)
    else:
        sl = pround(symbol, level - sl_dist)
        tp = pround(symbol, level + tp_dist)

    distance_pips = round(abs(current_price - level) / pip, 1)
    rr = round(tp_dist / sl_dist, 1)

    return {
        "price": pround(symbol, level),
        "type": "resistance" if direction == "short" else "support",
        "direction": direction,
        "strength": strength,
        "distance_pips": distance_pips,
        "sl": sl,
        "tp": tp,
        "rr": rr,
        "status": "watching",
    }


def analyze_symbol(symbol, candle_data):
    candles = candle_data.get("candles", [])
    current_price = candle_data.get("current_price", 0.0)

    if not current_price and candles:
        current_price = get_candle_field(candles[-1], "close", "c")

    if not current_price:
        return {"current_price": 0.0, "h1_trend": "unknown", "levels": []}

    pip = PIP.get(symbol, 0.0001)
    max_dist = MAX_DIST_PIPS * pip
    h1_trend = determine_h1_trend(candles)

    candidates = {}  # level -> strength

    # Session H/L
    if candles:
        hi = max(get_candle_field(c, "high", "h") for c in candles)
        lo = min(get_candle_field(c, "low", "l") for c in candles)
        candidates[pround(symbol, hi)] = 2
        candidates[pround(symbol, lo)] = 2

    # Yesterday (first 12 candles ≈ 24-12h ago)
    if len(candles) >= 12:
        yday = candles[:12]
        yhi = max(get_candle_field(c, "high", "h") for c in yday)
        ylo = min(get_candle_field(c, "low", "l") for c in yday)
        candidates[pround(symbol, yhi)] = max(candidates.get(pround(symbol, yhi), 0), 2)
        candidates[pround(symbol, ylo)] = max(candidates.get(pround(symbol, ylo), 0), 2)

    # Overnight (last 8 candles)
    if len(candles) >= 8:
        overnight = candles[-8:]
        ohi = max(get_candle_field(c, "high", "h") for c in overnight)
        olo = min(get_candle_field(c, "low", "l") for c in overnight)
        candidates[pround(symbol, ohi)] = max(candidates.get(pround(symbol, ohi), 0), 1)
        candidates[pround(symbol, olo)] = max(candidates.get(pround(symbol, olo), 0), 1)

    # Round numbers
    for lvl in get_round_levels(symbol, current_price):
        if lvl not in candidates:
            candidates[lvl] = 1

    # Score each candidate
    scored = []
    for lvl, base_strength in candidates.items():
        dist = abs(current_price - lvl)
        if dist < pip * 0.5:  # skip levels sitting at current price
            continue
        if dist > max_dist:
            continue
        touches = count_touches(candles, lvl, pip)
        strength = max(base_strength, touches)
        direction = "short" if lvl > current_price else "long"
        scored.append((strength, dist, lvl, direction))

    # Best 3: highest strength, then closest
    scored.sort(key=lambda x: (-x[0], x[1]))

    levels = [
        build_level(symbol, lvl, direction, strength, current_price)
        for strength, _, lvl, direction in scored[:3]
    ]

    return {
        "current_price": current_price,
        "h1_trend": h1_trend,
        "levels": levels,
    }


def main():
    parser = argparse.ArgumentParser(description="Scalp H1 level calculator")
    parser.add_argument("--symbol", action="append", required=True)
    parser.add_argument(
        "--candles-file",
        default=CANDLES_TEMP,
        help=f"JSON file with H1 OHLCV data (default: {CANDLES_TEMP})",
    )
    args = parser.parse_args()

    # Load H1 candle data
    candles_data = {}
    if os.path.exists(args.candles_file):
        with open(args.candles_file, encoding="utf-8-sig") as f:
            candles_data = json.load(f)
        print(f"Loaded candle data: {args.candles_file}")
    else:
        print(f"WARNING: {args.candles_file} not found — round number levels only")
        print("  Write scalp_candles_temp.json with H1 OHLCV data for full analysis.")

    now_sast = datetime.now(SAST)

    # Preserve session counters when re-running mid-session
    state = {
        "updated_sast": now_sast.strftime("%H:%M"),
        "instruments": {},
        "scalp_trades_today": 0,
        "consecutive_losses": 0,
        "session_pnl_zar": 0,
        "loop_active": False,
        "loop_stopped": False,
        "stop_reason": None,
    }
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                existing = json.load(f)
            for key in ("scalp_trades_today", "consecutive_losses", "session_pnl_zar"):
                state[key] = existing.get(key, 0)
        except Exception:
            pass

    print()
    for sym in args.symbol:
        sym = sym.upper()
        data = candles_data.get(sym, {})
        if not data:
            print(f"{sym}: no candle data in temp file — round numbers only")
            data = {"candles": [], "current_price": 0.0}

        result = analyze_symbol(sym, data)
        state["instruments"][sym] = result

        print(f"{sym} | price={result['current_price']} | trend={result['h1_trend']}")
        if result["levels"]:
            for lvl in result["levels"]:
                print(
                    f"  {lvl['type'].upper()} @ {lvl['price']} | "
                    f"strength={lvl['strength']} | dist={lvl['distance_pips']}pips | "
                    f"SL={lvl['sl']} TP={lvl['tp']} R:R={lvl['rr']}"
                )
        else:
            print("  No levels within range.")

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    total = sum(len(v["levels"]) for v in state["instruments"].values())
    print(
        f"\nscalp_state.json written — {len(args.symbol)} instruments, {total} levels loaded"
    )


if __name__ == "__main__":
    main()

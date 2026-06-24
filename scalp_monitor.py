#!/usr/bin/env python3
"""
scalp_monitor.py -- Real-time level watcher and M1/M5 rejection checker.
Outputs JSON with trigger status for the nearest active level.

Workflow per tick:
  1. Claude calls get_symbol_price via MCP, updates scalp_state.json current_price
  2. Claude runs: python scalp_monitor.py --symbol EURUSD [--price 1.14047]
  3. If status=AT_LEVEL, Claude fetches 5 M5 candles, writes scalp_m5_temp.json
  4. Claude re-runs monitor (or monitor auto-reads m5 file if present)
"""

import sys
import json
import argparse
import os

SCALP_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCALP_DIR, "scalp_state.json")
M5_TEMP = os.path.join(SCALP_DIR, "scalp_m5_temp.json")

PIP = {
    "EURUSD": 0.0001,
    "GBPUSD": 0.0001,
    "USDJPY": 0.01,
    "AUDUSD": 0.0001,
    "NZDUSD": 0.0001,
    "XAUUSD": 1.0,
}

# Distance thresholds in pips/pts
THRESH_AT_LEVEL = 1.0
THRESH_NEAR = 3.0
THRESH_WATCHING = 5.0

SKIP_STATUSES = {"passed", "invalidated", "triggered"}


def get_field(candle, *keys, default=0.0):
    for k in keys:
        if k in candle:
            return float(candle[k])
    return default


def check_rejection_candle(candle, level, direction):
    """
    Rejection candle: close is >= 60% of the candle range away from the wick extreme.
    Short: wick touched level from below, close back below level.
    Long:  wick touched level from above, close back above level.
    """
    high = get_field(candle, "high", "h")
    low = get_field(candle, "low", "l")
    close = get_field(candle, "close", "c")

    candle_range = high - low
    if candle_range < 1e-8:
        return False, "zero-range candle"

    if direction == "short":
        if high < level * 0.9999:
            return False, f"wick {high} did not reach level {level}"
        if close >= level:
            return False, f"close {close} still above level {level}"
        rejection_ratio = (high - close) / candle_range
        ok = rejection_ratio >= 0.60
        notes = f"close={close} wick_high={high} rejection={rejection_ratio:.0%}"
    else:
        if low > level * 1.0001:
            return False, f"wick {low} did not reach level {level}"
        if close <= level:
            return False, f"close {close} still below level {level}"
        rejection_ratio = (close - low) / candle_range
        ok = rejection_ratio >= 0.60
        notes = f"close={close} wick_low={low} rejection={rejection_ratio:.0%}"

    return ok, notes


def classify_distance(distance_pips):
    if distance_pips <= THRESH_AT_LEVEL:
        return "AT_LEVEL"
    elif distance_pips <= THRESH_NEAR:
        return "NEAR"
    elif distance_pips <= THRESH_WATCHING:
        return "WATCHING"
    return "WATCHING"


def main():
    parser = argparse.ArgumentParser(description="Scalp level monitor")
    parser.add_argument("--symbol", required=True)
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Current price (overrides scalp_state.json if given)",
    )
    parser.add_argument(
        "--m5-file",
        default=M5_TEMP,
        help="Path to M5 candle JSON for confirmation check",
    )
    args = parser.parse_args()

    symbol = args.symbol.upper()
    pip = PIP.get(symbol, 0.0001)

    # Load state
    if not os.path.exists(STATE_FILE):
        out = {
            "symbol": symbol,
            "error": "scalp_state.json not found — run scalp_levels.py first",
        }
        print(json.dumps(out, indent=2))
        sys.exit(1)

    with open(STATE_FILE, encoding="utf-8-sig") as f:
        state = json.load(f)

    instruments = state.get("instruments", {})
    if symbol not in instruments:
        out = {"symbol": symbol, "error": f"{symbol} not in scalp_state.json"}
        print(json.dumps(out, indent=2))
        sys.exit(1)

    sym_state = instruments[symbol]
    current_price = (
        args.price if args.price is not None else sym_state.get("current_price", 0.0)
    )

    if not current_price:
        out = {
            "symbol": symbol,
            "error": "No current price — pass --price or update scalp_state.json",
        }
        print(json.dumps(out, indent=2))
        sys.exit(1)

    levels = sym_state.get("levels", [])
    active = [l for l in levels if l.get("status") not in SKIP_STATUSES]

    if not active:
        out = {
            "symbol": symbol,
            "current_price": current_price,
            "nearest_level": None,
            "distance_pips": None,
            "status": "WATCHING",
            "direction": None,
            "sl": None,
            "tp": None,
        }
        print(json.dumps(out, indent=2))
        return

    nearest = min(active, key=lambda l: abs(current_price - l["price"]))
    distance_pips = round(abs(current_price - nearest["price"]) / pip, 1)
    status = classify_distance(distance_pips)

    out = {
        "symbol": symbol,
        "current_price": current_price,
        "nearest_level": nearest["price"],
        "distance_pips": distance_pips,
        "status": status,
        "direction": nearest["direction"],
        "sl": nearest["sl"],
        "tp": nearest["tp"],
    }

    # M1/M5 confirmation check when price is at the level
    if status == "AT_LEVEL":
        m5_candles = []
        if os.path.exists(args.m5_file):
            try:
                with open(args.m5_file, encoding="utf-8-sig") as f:
                    m5_data = json.load(f)
                m5_candles = m5_data.get(symbol, {}).get("candles", [])[-5:]
            except Exception:
                pass

        if m5_candles:
            confirmed, notes = check_rejection_candle(
                m5_candles[-1], nearest["price"], nearest["direction"]
            )
            if confirmed:
                out["status"] = "TRIGGERED"
            out["m5_confirmation"] = confirmed
            out["m5_notes"] = notes
        else:
            out["m5_confirmation"] = False
            out["m5_notes"] = f"no M5 data — write {args.m5_file} and re-run"

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CHANGE 7 SCANNER — Big Run + Pullback + BOUNCE pattern detector.
Works across XAUUSD and all major/cross forex pairs.

CHANGE 7 (trend-continuation, per session report 2026-06-24):
  1. Big run: high-low range >= min_run in last 6 M15 bars
  2. Pullback: price retraced >= 20% from the run extreme (opposite direction)
  3. Resumption: last completed M15 bar closes in H4 direction

BOUNCE (counter-trend exhaustion — Tony's pattern, +R1,944 trade 2026-06-24):
  1. 5+ consecutive M15 bars in ONE direction
  2. First reversal bar closes opposite direction
  3. SL = beyond run extreme, TP = +15pt/pip
  4. Only fires if R:R >= 1.5 (run extreme must not be too far)

H4 direction gate (from last 3 completed H4 bars):
  BEAR: 2+ closes falling -> SHORT ONLY for CHANGE 7
  BULL: 2+ closes rising  -> LONG ONLY for CHANGE 7
  BOUNCE overrides H4 gate (exhaustion plays are counter-trend by definition)

Usage:
  python3 change7_scanner.py --symbol XAUUSD \\
    --h4_bars "2026-06-24 12:00|4046|4060|4040|4047|100;2026-06-24 08:00|4075|4090|4060|4075|100;2026-06-24 04:00|4063|4095|4050|4063|100" \\
    --m15_bars "2026-06-24 18:30|3989|3993|3980|3990|100;...;2026-06-24 20:00|3983|3989|3979|3983|100" \\
    --last_entry_bar "2026-06-24 17:45"

Exit codes:
  0 = signal detected (check result.signal for details)
  1 = no signal
  2 = instrument not supported
"""

import argparse
import json
import sys

# ---------------------------------------------------------------------------
# Instrument parameters for CHANGE 7
# min_run : minimum price move qualifying as "big run" (native price units)
# sl      : SL distance from entry (native price units)
# tp      : TP distance from entry (native price units)
# pip_size: 1 pip in native price (0.0001 for std forex, 0.01 for JPY, 1.0 for XAUUSD)
# units   : units/lots for MCP create_market_order
# zar_per_pip: ZAR P&L per pip per unit
# ---------------------------------------------------------------------------
INSTRUMENT_CONFIG: dict = {
    # Gold — primary
    "XAUUSD": {
        "min_run": 15.0,
        "sl": 6.0,
        "tp": 15.0,
        "pip_size": 1.0,
        "units": 1,
        "zar_per_pip": 16.0,
    },
    # Standard forex (pip = 0.0001)
    "EURUSD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "GBPUSD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "AUDUSD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "NZDUSD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "USDCAD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "USDCHF": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "EURGBP": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "EURAUD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "EURCHF": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "EURCAD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "GBPAUD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "GBPCAD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "GBPCHF": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "AUDCHF": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "AUDNZD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "AUDCAD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "NZDCAD": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    "NZDCHF": {
        "min_run": 0.0015,
        "sl": 0.0006,
        "tp": 0.0015,
        "pip_size": 0.0001,
        "units": 3000,
        "zar_per_pip": 5.46,
    },
    # JPY pairs (pip = 0.01)
    "USDJPY": {
        "min_run": 0.15,
        "sl": 0.06,
        "tp": 0.15,
        "pip_size": 0.01,
        "units": 3000,
        "zar_per_pip": 3.71,
    },
    "EURJPY": {
        "min_run": 0.15,
        "sl": 0.06,
        "tp": 0.15,
        "pip_size": 0.01,
        "units": 3000,
        "zar_per_pip": 3.71,
    },
    "GBPJPY": {
        "min_run": 0.15,
        "sl": 0.06,
        "tp": 0.15,
        "pip_size": 0.01,
        "units": 3000,
        "zar_per_pip": 3.71,
    },
    "AUDJPY": {
        "min_run": 0.15,
        "sl": 0.06,
        "tp": 0.15,
        "pip_size": 0.01,
        "units": 3000,
        "zar_per_pip": 3.71,
    },
    "CADJPY": {
        "min_run": 0.15,
        "sl": 0.06,
        "tp": 0.15,
        "pip_size": 0.01,
        "units": 3000,
        "zar_per_pip": 3.30,
    },
    "NZDJPY": {
        "min_run": 0.15,
        "sl": 0.06,
        "tp": 0.15,
        "pip_size": 0.01,
        "units": 3000,
        "zar_per_pip": 3.10,
    },
    "CHFJPY": {
        "min_run": 0.15,
        "sl": 0.06,
        "tp": 0.15,
        "pip_size": 0.01,
        "units": 3000,
        "zar_per_pip": 3.50,
    },
    # Silver
    "XAGUSD": {
        "min_run": 0.50,
        "sl": 0.20,
        "tp": 0.50,
        "pip_size": 0.01,
        "units": 1,
        "zar_per_pip": 18.5,
    },
}

SUPPORTED_SYMBOLS = list(INSTRUMENT_CONFIG.keys())


def parse_bars(bar_string: str) -> list:
    """Parse semicolon-separated bar strings: 'datetime|O|H|L|C|V;...'"""
    bars = []
    for b in bar_string.strip().split(";"):
        b = b.strip()
        if not b:
            continue
        parts = b.split("|")
        if len(parts) < 5:
            continue
        try:
            bars.append(
                {
                    "datetime": parts[0].strip(),
                    "open": float(parts[1]),
                    "high": float(parts[2]),
                    "low": float(parts[3]),
                    "close": float(parts[4]),
                }
            )
        except ValueError:
            continue
    return bars


def h4_direction(bars: list) -> str:
    """2 of last 3 H4 closes falling = bear. Rising = bull. Otherwise unclear."""
    if len(bars) < 3:
        return "unclear"
    closes = [b["close"] for b in bars[-3:]]
    falling = sum(1 for i in range(1, len(closes)) if closes[i] < closes[i - 1])
    rising = sum(1 for i in range(1, len(closes)) if closes[i] > closes[i - 1])
    if falling >= 2:
        return "bear"
    if rising >= 2:
        return "bull"
    return "unclear"


def _count_consecutive(bars: list, direction: str) -> int:
    """Count consecutive bars in direction from end of list."""
    count = 0
    for b in reversed(bars):
        is_match = (
            (b["close"] < b["open"])
            if direction == "bear"
            else (b["close"] > b["open"])
        )
        if is_match:
            count += 1
        else:
            break
    return count


def detect_change7(m15_bars: list, direction: str, cfg: dict) -> dict | None:
    """
    Detect CHANGE 7 signal in M15 bars.
    Needs >= 8 bars (6 lookback + 1 signal bar minimum).
    """
    if len(m15_bars) < 7:
        return None
    if direction not in ("bear", "bull"):
        return None

    window = m15_bars[-7:-1]  # 6-bar lookback
    signal = m15_bars[-1]  # last completed bar = signal bar

    win_high = max(b["high"] for b in window)
    win_low = min(b["low"] for b in window)
    run_size = win_high - win_low

    if run_size < cfg["min_run"]:
        return None

    if direction == "bear":
        # Signal bar must be bearish
        if signal["close"] >= signal["open"]:
            return None
        # Majority of window bars must be bearish (run was DOWN)
        bear_bars = sum(1 for b in window if b["close"] < b["open"])
        if bear_bars < 3:
            return None
        # Pullback: current price has bounced UP >= 20% from window low
        pullback = signal["close"] - win_low
        pullback_pct = pullback / run_size if run_size > 0 else 0
        if pullback_pct < 0.20:
            return None

        entry = signal["close"]
        sl_price = round(entry + cfg["sl"], 5)
        tp_price = round(entry - cfg["tp"], 5)
        sl_pips = cfg["sl"] / cfg["pip_size"]
        risk_zar = round(sl_pips * cfg["zar_per_pip"], 2)
        reward_zar = round((cfg["tp"] / cfg["pip_size"]) * cfg["zar_per_pip"], 2)

        return {
            "pattern": "CHANGE7",
            "direction": "short",
            "signal_bar": signal["datetime"],
            "entry": entry,
            "sl": sl_price,
            "tp": tp_price,
            "run_size_pips": round(run_size / cfg["pip_size"], 1),
            "pullback_pct": round(pullback_pct * 100, 1),
            "sl_pips": round(sl_pips, 1),
            "risk_zar": risk_zar,
            "reward_zar": reward_zar,
            "rr": round(reward_zar / risk_zar, 2) if risk_zar > 0 else 0,
            "units": cfg["units"],
        }

    else:  # bull
        # Signal bar must be bullish
        if signal["close"] <= signal["open"]:
            return None
        # Majority of window bars must be bullish
        bull_bars = sum(1 for b in window if b["close"] > b["open"])
        if bull_bars < 3:
            return None
        # Pullback: current price has dipped DOWN >= 20% from window high
        pullback = win_high - signal["close"]
        pullback_pct = pullback / run_size if run_size > 0 else 0
        if pullback_pct < 0.20:
            return None

        entry = signal["close"]
        sl_price = round(entry - cfg["sl"], 5)
        tp_price = round(entry + cfg["tp"], 5)
        sl_pips = cfg["sl"] / cfg["pip_size"]
        risk_zar = round(sl_pips * cfg["zar_per_pip"], 2)
        reward_zar = round((cfg["tp"] / cfg["pip_size"]) * cfg["zar_per_pip"], 2)

        return {
            "pattern": "CHANGE7",
            "direction": "long",
            "signal_bar": signal["datetime"],
            "entry": entry,
            "sl": sl_price,
            "tp": tp_price,
            "run_size_pips": round(run_size / cfg["pip_size"], 1),
            "pullback_pct": round(pullback_pct * 100, 1),
            "sl_pips": round(sl_pips, 1),
            "risk_zar": risk_zar,
            "reward_zar": reward_zar,
            "rr": round(reward_zar / risk_zar, 2) if risk_zar > 0 else 0,
            "units": cfg["units"],
        }


def detect_bounce(m15_bars: list, cfg: dict) -> dict | None:
    """
    Detect BOUNCE pattern: 5+ consecutive bars one direction + reversal bar.
    Counter-trend exhaustion play. Overrides H4 direction gate.
    """
    if len(m15_bars) < 6:
        return None

    signal = m15_bars[-1]
    pre_bars = m15_bars[:-1]

    consec_bear = _count_consecutive(pre_bars, "bear")
    consec_bull = _count_consecutive(pre_bars, "bull")

    if consec_bear >= 5 and signal["close"] > signal["open"]:
        # Exhaustion bounce LONG after 5+ bearish bars
        run_bars = pre_bars[-consec_bear:]
        run_low = min(b["low"] for b in run_bars)
        run_high = max(b["high"] for b in run_bars)

        entry = signal["close"]
        sl_price = round(run_low - cfg["pip_size"], 5)
        sl_dist = entry - sl_price
        if sl_dist <= 0:
            return None
        sl_pips = sl_dist / cfg["pip_size"]
        tp_price = round(entry + cfg["tp"], 5)
        risk_zar = round(sl_pips * cfg["zar_per_pip"], 2)
        reward_zar = round((cfg["tp"] / cfg["pip_size"]) * cfg["zar_per_pip"], 2)
        rr = round(reward_zar / risk_zar, 2) if risk_zar > 0 else 0

        if rr < 1.5:
            return None  # SL too wide, skip

        return {
            "pattern": "BOUNCE",
            "direction": "long",
            "consecutive_bear_bars": consec_bear,
            "signal_bar": signal["datetime"],
            "entry": entry,
            "sl": sl_price,
            "tp": tp_price,
            "run_low": run_low,
            "run_high": run_high,
            "sl_pips": round(sl_pips, 1),
            "risk_zar": risk_zar,
            "reward_zar": reward_zar,
            "rr": rr,
            "units": cfg["units"],
            "note": "Counter-trend exhaustion — overrides H4 direction gate",
        }

    if consec_bull >= 5 and signal["close"] < signal["open"]:
        # Exhaustion bounce SHORT after 5+ bullish bars
        run_bars = pre_bars[-consec_bull:]
        run_high = max(b["high"] for b in run_bars)
        run_low = min(b["low"] for b in run_bars)

        entry = signal["close"]
        sl_price = round(run_high + cfg["pip_size"], 5)
        sl_dist = sl_price - entry
        if sl_dist <= 0:
            return None
        sl_pips = sl_dist / cfg["pip_size"]
        tp_price = round(entry - cfg["tp"], 5)
        risk_zar = round(sl_pips * cfg["zar_per_pip"], 2)
        reward_zar = round((cfg["tp"] / cfg["pip_size"]) * cfg["zar_per_pip"], 2)
        rr = round(reward_zar / risk_zar, 2) if risk_zar > 0 else 0

        if rr < 1.5:
            return None

        return {
            "pattern": "BOUNCE",
            "direction": "short",
            "consecutive_bull_bars": consec_bull,
            "signal_bar": signal["datetime"],
            "entry": entry,
            "sl": sl_price,
            "tp": tp_price,
            "run_high": run_high,
            "run_low": run_low,
            "sl_pips": round(sl_pips, 1),
            "risk_zar": risk_zar,
            "reward_zar": reward_zar,
            "rr": rr,
            "units": cfg["units"],
            "note": "Counter-trend exhaustion — overrides H4 direction gate",
        }

    return None


def main() -> None:
    p = argparse.ArgumentParser(description="CHANGE 7 + Bounce scanner")
    p.add_argument("--symbol", required=True)
    p.add_argument(
        "--h4_bars",
        required=True,
        help="Semicolon-separated H4 bars (at least 3): datetime|O|H|L|C|V",
    )
    p.add_argument(
        "--m15_bars",
        required=True,
        help="Semicolon-separated M15 bars (at least 8): datetime|O|H|L|C|V",
    )
    p.add_argument(
        "--last_entry_bar",
        default="",
        help="Datetime of last signal bar used — prevents duplicate entries on same bar",
    )
    p.add_argument(
        "--list_symbols", action="store_true", help="Print supported symbols and exit"
    )
    args = p.parse_args()

    if args.list_symbols:
        print("\n".join(SUPPORTED_SYMBOLS))
        sys.exit(0)

    symbol = args.symbol.upper()
    cfg = INSTRUMENT_CONFIG.get(symbol)

    if cfg is None:
        out = {
            "symbol": symbol,
            "signal": None,
            "reason": f"{symbol} not in INSTRUMENT_CONFIG — add it to extend coverage",
        }
        print(json.dumps(out, indent=2))
        sys.exit(2)

    h4_bars = parse_bars(args.h4_bars)
    m15_bars = parse_bars(args.m15_bars)
    direction = h4_direction(h4_bars)

    # CHANGE 7 (trend-continuation)
    c7 = (
        detect_change7(m15_bars, direction, cfg)
        if direction in ("bear", "bull")
        else None
    )

    # BOUNCE (counter-trend exhaustion)
    bounce = detect_bounce(m15_bars, cfg)

    # Prefer CHANGE 7 over bounce when both fire
    active = c7 or bounce

    # Stale signal check — skip if we already entered on this exact bar
    if active and args.last_entry_bar and active["signal_bar"] == args.last_entry_bar:
        active = None

    out = {
        "symbol": symbol,
        "h4_direction": direction,
        "signal": active,
        "change7": c7,
        "bounce": bounce,
        "reason": active["pattern"] + " " + active["direction"].upper()
        if active
        else "No signal",
    }

    print(json.dumps(out, indent=2))
    sys.exit(0 if active else 1)


if __name__ == "__main__":
    main()

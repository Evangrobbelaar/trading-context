#!/usr/bin/env python3
"""
Tick preparation — runs at the START of every loop tick.

Reads all local cache and state files, then outputs a single JSON summary
telling Claude exactly what to do this tick. Claude reads this instead of
manually checking every file and re-deriving context.

Usage:
  python tick_prep.py
      → Full tick summary (what's stale, session, watchlist, news gate, stop conditions)

  python tick_prep.py --prices "EURUSD:1.1374,GBPUSD:1.3203,AUDUSD:0.6918"
      → Also checks which watchlist instruments are near entry zones

  python tick_prep.py --session-start --balance 3842.64
      → Resets session counters in session_state.json (call once per session)

  python tick_prep.py --close-session --balance 3791.00 --trades 2 --pnl -51.64
      → Writes session-end counters (call at session end)
"""

import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

H4_CACHE = Path("h4_cache.json")
M15_CACHE = Path("m15_cache.json")
WATCHLIST = Path("watchlist.json")
NEWS = Path("news_impact.json")
STATE = Path("session_state.json")
SPECS = Path("instrument_specs.json")

SAST_OFFSET = 2  # UTC+2

SESSION_MAP = [
    (1, 7, "asian", "CHANGE 7 — USDJPY/AUDUSD/NZDUSD/XAUUSD — max 2 trades"),
    (7, 9, "pre_london", "Pre-London — run scalp_levels.py at 08:43"),
    (9, 15, "london", "CHANGE 7 + scalp — ALL instruments — max 4 trades + 3 scalp"),
    (15, 18, "london_ny", "London/NY overlap — BEST session — max 4 trades + 3 scalp"),
    (18, 22, "ny", "NY — CHANGE 7 + monitor open positions — max 2 trades"),
    (22, 25, "off", "Off-hours — CHANGE 7 if signal fires — max 1 trade"),
]

SESSION_MAX_TRADES = {
    "asian": 2,
    "pre_london": 0,
    "london": 4,
    "london_ny": 4,
    "ny": 2,
    "off": 1,
}


def sast_hour(utc_now: datetime) -> float:
    return (utc_now.hour + SAST_OFFSET) % 24 + utc_now.minute / 60


def get_session(utc_now: datetime) -> tuple[str, str]:
    h = sast_hour(utc_now)
    for lo, hi, name, desc in SESSION_MAP:
        if lo <= h < hi:
            return name, desc
    return "off", "Off-hours"


def load(path: Path, default=None):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return default if default is not None else {}


def h4_is_stale(entry: dict) -> bool:
    if not entry:
        return True
    exp = datetime.fromisoformat(entry["expires_at"])
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) >= exp


def m15_is_stale(entry: dict) -> bool:
    if not entry:
        return True
    exp = datetime.fromisoformat(entry["expires_at"])
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) >= exp


def pips_from_zone(price: float, zone: list, specs: dict, symbol: str) -> float | None:
    """Return pips between price and nearest edge of entry zone. None if unknown."""
    if not zone or len(zone) < 2:
        return None
    lo, hi = zone[0], zone[1]
    if lo <= price <= hi:
        return 0.0
    dist_price = min(abs(price - lo), abs(price - hi))
    pip_size = 0.01 if "JPY" in symbol else 0.0001
    if symbol in ("XAUUSD", "XAGUSD", "NAS100", "SPX500", "BRENT"):
        pip_size = 1.0
    return round(dist_price / pip_size, 1)


def check_near_entry(prices: dict, watchlist: list, specs: dict) -> list:
    """Return watchlist entries where price is within 15 pips of entry zone."""
    near = []
    for item in watchlist:
        sym = item.get("symbol", "")
        zone = item.get("entry_zone", [])
        price = prices.get(sym)
        if price is None or not zone:
            continue
        dist = pips_from_zone(price, zone, specs, sym)
        if dist is not None and dist <= 15:
            near.append(
                {
                    "symbol": sym,
                    "direction": item.get("direction"),
                    "price": price,
                    "entry_zone": zone,
                    "pips_away": dist,
                    "sl": item.get("sl"),
                    "tp": item.get("tp"),
                    "rr": item.get("rr"),
                    "score": item.get("score"),
                    "trigger": item.get("trigger", ""),
                }
            )
    near.sort(key=lambda x: x["pips_away"])
    return near


def main() -> None:
    p = argparse.ArgumentParser(description="Tick preparation summary")
    p.add_argument("--prices", default="", help="Comma-separated SYMBOL:price pairs")
    p.add_argument(
        "--session-start", action="store_true", help="Reset session counters"
    )
    p.add_argument(
        "--close-session", action="store_true", help="Write session-end data"
    )
    p.add_argument("--balance", type=float, default=0)
    p.add_argument("--trades", type=int, default=0)
    p.add_argument("--pnl", type=float, default=0)
    args = p.parse_args()

    now = datetime.now(timezone.utc)
    sast_time = (now + timedelta(hours=SAST_OFFSET)).strftime("%H:%M")
    session, desc = get_session(now)

    h4_cache = load(H4_CACHE)
    m15_cache = load(M15_CACHE)
    _wl_raw = load(WATCHLIST, [])
    watchlist = (
        _wl_raw.get("watchlist", _wl_raw) if isinstance(_wl_raw, dict) else _wl_raw
    )
    news = load(NEWS, {})
    state = load(STATE)
    specs = load(SPECS)

    # --session-start: reset counters
    if args.session_start:
        state["session"] = session
        state["session_start_balance"] = args.balance or state.get("account_balance", 0)
        state["session_start_time_sast"] = sast_time
        state["trades_this_session"] = 0
        state["consecutive_losses"] = 0
        state["session_drawdown_zar"] = 0
        STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        print(
            json.dumps(
                {
                    "ok": True,
                    "session": session,
                    "balance": args.balance,
                    "message": "Session counters reset",
                }
            )
        )
        return

    # --close-session: write end data
    if args.close_session:
        state["last_session_pnl"] = args.pnl
        state["last_session_trades"] = args.trades
        state["account_balance"] = args.balance
        STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        print(
            json.dumps(
                {
                    "ok": True,
                    "pnl": args.pnl,
                    "trades": args.trades,
                    "balance": args.balance,
                }
            )
        )
        return

    # Parse optional prices arg
    prices = {}
    if args.prices:
        for part in args.prices.split(","):
            part = part.strip()
            if ":" in part:
                sym, val = part.split(":", 1)
                try:
                    prices[sym.upper()] = float(val)
                except ValueError:
                    pass

    # H4 cache status
    H4_SCAN = [
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

    h4_stale, h4_fresh = [], {}
    for sym in H4_SCAN:
        e = h4_cache.get(sym)
        if not e or h4_is_stale(e):
            h4_stale.append(sym)
        else:
            cached_at = datetime.fromisoformat(e["cached_at"])
            if cached_at.tzinfo is None:
                cached_at = cached_at.replace(tzinfo=timezone.utc)
            age_min = round((now - cached_at).total_seconds() / 60)
            h4_fresh[sym] = {
                "trend": e["trend"],
                "evidence": e["evidence"],
                "age_min": age_min,
            }

    # M15 cache status — only check watchlist symbols
    watchlist_syms = [
        item.get("symbol", "") for item in watchlist if item.get("symbol")
    ]
    m15_stale, m15_fresh = [], {}
    for sym in watchlist_syms:
        e = m15_cache.get(sym)
        if not e or m15_is_stale(e):
            m15_stale.append(sym)
        else:
            cached_at = datetime.fromisoformat(e["cached_at"])
            if cached_at.tzinfo is None:
                cached_at = cached_at.replace(tzinfo=timezone.utc)
            age_sec = round((now - cached_at).total_seconds())
            m15_fresh[sym] = {"age_sec": age_sec, "structure": e.get("structure", {})}

    # News gate
    active_events = news.get("events", [])
    high_impact_2h = news.get("high_impact_within_2h", False)
    news_gate = (
        "BLOCKED — high-impact event within 2h"
        if high_impact_2h
        else (f"active ({', '.join(active_events)})" if active_events else "clear")
    )

    # Session stop conditions
    trades_done = state.get("trades_this_session", 0)
    consec_losses = state.get("consecutive_losses", 0)
    session_drawdown = state.get("session_drawdown_zar", 0)
    max_trades = SESSION_MAX_TRADES.get(session, 2)

    stop_checks = {
        "consecutive_losses": {
            "value": consec_losses,
            "limit": 3,
            "ok": consec_losses < 3,
        },
        "session_drawdown_zar": {
            "value": session_drawdown,
            "limit": 800,
            "ok": session_drawdown < 800,
        },
        "trades_this_session": {
            "value": trades_done,
            "limit": max_trades,
            "ok": trades_done < max_trades,
        },
    }
    should_stop = any(not v["ok"] for v in stop_checks.values()) or high_impact_2h

    # Near-entry check (only if prices provided)
    near_entry = check_near_entry(prices, watchlist, specs) if prices else []

    # Build actions list
    actions = []
    if h4_stale:
        actions.append(
            f"FETCH H4 (timeframeMinutes=240, limit=6) for: {', '.join(h4_stale)} — then write to h4_temp.json + run h4_updater.py --write"
        )
    else:
        actions.append("H4 all fresh — skip H4 MCP calls")

    actions.append("FETCH prices for all watchlist symbols + XAUUSD")
    actions.append("FETCH get_open_positions")

    if m15_stale:
        actions.append(
            f"FETCH M15 (timeframeMinutes=15, limit=8) for: {', '.join(m15_stale)} — then write to m15_temp.json + run m15_updater.py --write"
        )

    if near_entry:
        actions.append(
            f"NEAR ENTRY: {', '.join(x['symbol'] for x in near_entry)} — prioritise M15 check for these"
        )

    if high_impact_2h:
        actions.append(
            "NEWS GATE BLOCKED — no new trades until event prints + M15 settles"
        )

    if should_stop and not high_impact_2h:
        triggered = [k for k, v in stop_checks.items() if not v["ok"]]
        actions.append(
            f"LOOP STOP CONDITIONS MET: {', '.join(triggered)} — do not place new trades"
        )

    # Output
    out = {
        "sast_time": sast_time,
        "utc_time": now.strftime("%H:%M"),
        "session": session,
        "session_desc": desc,
        "h4_cache": {
            "fresh": h4_fresh,
            "stale": h4_stale,
            "all_fresh": len(h4_stale) == 0,
        },
        "m15_cache": {
            "fresh": m15_fresh,
            "stale": m15_stale,
            "all_fresh": len(m15_stale) == 0,
        },
        "watchlist": watchlist[:10],
        "near_entry": near_entry,
        "news_gate": news_gate,
        "high_impact_2h": high_impact_2h,
        "session_counters": {
            "trades_this_session": trades_done,
            "max_trades": max_trades,
            "trades_remaining": max(0, max_trades - trades_done),
            "consecutive_losses": consec_losses,
            "session_drawdown_zar": session_drawdown,
            "session_start_balance": state.get("session_start_balance", 0),
        },
        "stop_conditions": stop_checks,
        "should_stop": should_stop,
        "actions_this_tick": actions,
    }

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
scalp_enforcer.py -- Scalp-specific trade gate.
Exit 0 = PASS, exit 1 = BLOCKED.
Writes every check to scalp_enforcer_audit.jsonl.
"""

import sys
import json
import argparse
import os
from datetime import datetime, timezone, timedelta

SCALP_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCALP_DIR, "scalp_state.json")
AUDIT_FILE = os.path.join(SCALP_DIR, "scalp_enforcer_audit.jsonl")
NEWS_FILE = os.path.join(os.path.dirname(SCALP_DIR), "tradeloop", "news_impact.json")

SAST = timezone(timedelta(hours=2))

# Session windows (SAST hours)
SESSIONS = [
    (9, 0, 12, 0),  # London
    (15, 0, 18, 0),  # London/NY overlap
]

# ZAR per pip per 0.01L (or per unit for Gold)
ZAR_PER_PIP = {
    "EURUSD": 1.82,
    "GBPUSD": 2.30,
    "USDJPY": 1.12,
    "AUDUSD": 1.82,
    "NZDUSD": 1.82,
    "XAUUSD": 16.0,  # per point per 1 unit
}

# Instruments not allowed for scalping
BLOCKED_INSTRUMENTS = {"GBPJPY", "EURJPY", "XAGUSD", "NAS100", "SPX500", "US30"}


def in_session(now_sast):
    t = now_sast.hour * 60 + now_sast.minute
    for h_start, m_start, h_end, m_end in SESSIONS:
        if h_start * 60 + m_start <= t < h_end * 60 + m_end:
            return True
    return False


def calc_risk_zar(symbol, lots, pips):
    per_pip = ZAR_PER_PIP.get(symbol, 1.82)
    if symbol == "XAUUSD":
        return lots * pips * per_pip
    return (lots / 0.01) * pips * per_pip


def check_news():
    if not os.path.exists(NEWS_FILE):
        return False, None
    try:
        with open(NEWS_FILE) as f:
            news = json.load(f)
        return news.get("high_impact_2h", False), news
    except Exception:
        return False, None


def main():
    parser = argparse.ArgumentParser(description="Scalp trade enforcer")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--direction", required=True, choices=["long", "short"])
    parser.add_argument("--lots", type=float, required=True)
    parser.add_argument("--balance", type=float, required=True)
    parser.add_argument("--sl_distance_pips", type=float, required=True)
    parser.add_argument("--tp_distance_pips", type=float, required=True)
    parser.add_argument("--account", default="demo")
    parser.add_argument("--spread_pips", type=float, default=1.0)
    args = parser.parse_args()

    symbol = args.symbol.upper()
    now_sast = datetime.now(SAST)

    # Load state
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
        except Exception:
            pass

    scalp_trades_today = state.get("scalp_trades_today", 0)
    consecutive_losses = state.get("consecutive_losses", 0)
    session_pnl_zar = state.get("session_pnl_zar", 0.0)

    # Run checks in order — first failure blocks
    block_reason = None

    if symbol in BLOCKED_INSTRUMENTS:
        block_reason = f"{symbol} is not permitted for scalping"

    elif args.account != "demo":
        block_reason = f"Account must be demo (#41829612) — got: {args.account}"

    elif args.balance < 3000:
        block_reason = f"Balance R{args.balance:.0f} below R3,000 capital floor"

    elif args.sl_distance_pips < 3:
        block_reason = f"SL {args.sl_distance_pips}pips too tight (min 3) — spread will kill the trade"

    elif args.sl_distance_pips > 10:
        block_reason = f"SL {args.sl_distance_pips}pips too wide for scalp (max 10) — use swing system"

    elif args.tp_distance_pips < args.sl_distance_pips * 1.5:
        rr = args.tp_distance_pips / args.sl_distance_pips
        block_reason = (
            f"R:R {rr:.2f}:1 below minimum 1.5:1 "
            f"(TP={args.tp_distance_pips} SL={args.sl_distance_pips})"
        )

    elif scalp_trades_today >= 3:
        block_reason = f"Max 3 scalps reached for session ({scalp_trades_today}/3)"

    elif consecutive_losses >= 2:
        block_reason = "2 consecutive losses — scalp loop stopped for session"

    elif session_pnl_zar < -200:
        block_reason = f"Session drawdown R{session_pnl_zar:.0f} exceeds R200 limit"

    elif args.spread_pips > args.sl_distance_pips * 0.5:
        block_reason = (
            f"Spread {args.spread_pips}pips > 50% of SL {args.sl_distance_pips}pips"
        )

    elif not in_session(now_sast):
        block_reason = (
            f"Outside scalp session (London 09-12 / London-NY 15-18 SAST) "
            f"— now {now_sast.strftime('%H:%M')} SAST"
        )

    else:
        high_impact, _ = check_news()
        if high_impact:
            block_reason = "High-impact news event within 2h — scalp loop paused"

    # Calculate ZAR values for display / audit regardless of result
    risk_zar = calc_risk_zar(symbol, args.lots, args.sl_distance_pips)
    reward_zar = calc_risk_zar(symbol, args.lots, args.tp_distance_pips)
    rr = round(args.tp_distance_pips / args.sl_distance_pips, 2)

    # Audit entry
    audit = {
        "timestamp_sast": now_sast.isoformat(),
        "symbol": symbol,
        "direction": args.direction,
        "lots": args.lots,
        "balance": args.balance,
        "sl_pips": args.sl_distance_pips,
        "tp_pips": args.tp_distance_pips,
        "spread_pips": args.spread_pips,
        "risk_zar": round(risk_zar, 2),
        "reward_zar": round(reward_zar, 2),
        "rr": rr,
        "scalp_trades_today": scalp_trades_today,
        "consecutive_losses": consecutive_losses,
        "session_pnl_zar": session_pnl_zar,
        "result": "BLOCKED" if block_reason else "PASS",
        "reason": block_reason,
    }
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(audit) + "\n")

    if block_reason:
        print(f"SCALP ENFORCER: BLOCKED — {block_reason}")
        sys.exit(1)

    print("SCALP ENFORCER: PASS")
    print(f"Symbol: {symbol} | Direction: {args.direction} | Lots: {args.lots}")
    print(
        f"SL: {args.sl_distance_pips} pips = R{risk_zar:.2f} risk | "
        f"TP: {args.tp_distance_pips} pips = R{reward_zar:.2f} reward"
    )
    print(
        f"R:R: {rr:.1f}:1 | "
        f"Session trades: {scalp_trades_today + 1}/3 | "
        f"Consecutive losses: {consecutive_losses}"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

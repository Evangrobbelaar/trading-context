#!/usr/bin/env python3
"""
SessionStart hook for TradeLoop (ECC pattern).
Fires at every Claude Code session start.
Reads session_state.json + news_impact.json + session_log.jsonl,
injects critical trading context as additionalContext.
Output: JSON { hookEventName, additionalContext }
"""

import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def last_jsonl_lines(filename, n=3):
    path = os.path.join(BASE_DIR, filename)
    records = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    return records[-n:] if len(records) >= n else records


def build_context():
    state = load_json("session_state.json")
    news = load_json("news_impact.json")
    last_ticks = last_jsonl_lines("session_log.jsonl", 2)

    balance = state.get("account_balance", "unknown")
    updated = state.get("updated_sast", "unknown")
    loop_stopped = state.get("loop_stopped", False)
    stops = state.get("stop_conditions", {})
    consec = stops.get("consecutive_losses", 0)
    max_consec = stops.get("max_consecutive_losses", 2)
    trades_today = stops.get("trades_this_session", 0)

    h4 = state.get("h4_trends", {})
    active_trends = {k: v for k, v in h4.items() if "skip" not in v.lower()}

    watchlist = state.get("watchlist_tomorrow", [])
    news_events = news.get("active_events", state.get("news_events", []))
    high_impact_2h = news.get("high_impact_within_2h", False)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [
        "=== TRADELOOP SESSION CONTEXT ===",
        f"Date: {today} | Account: Demo #41829612 | MCP: mcp__claude_ai_claude__",
        f"Balance: R{balance} | Last H4 scan: {updated} SAST",
        f"Loop stopped: {loop_stopped} | Consecutive losses: {consec}/{max_consec} | Trades today: {trades_today}",
        "",
    ]

    if h4:
        lines.append("H4 TRENDS:")
        for sym, trend in active_trends.items():
            lines.append(f"  {sym}: {trend}")
        skipped = [k for k, v in h4.items() if "skip" in v.lower()]
        if skipped:
            lines.append(f"  [SKIP — ranging/choppy]: {', '.join(skipped)}")
        lines.append("")

    if watchlist:
        lines.append("WATCHLIST (London open):")
        for w in watchlist[:4]:
            entry = w.get("entry_zone", [])
            entry_str = f"{entry[0]}-{entry[1]}" if len(entry) == 2 else str(entry)
            inv = w.get("invalidation", "")
            lines.append(
                f"  #{w.get('rank', '')} {w.get('symbol', '')} {w.get('direction', '').upper()}"
                f" score={w.get('score', '')} entry={entry_str} R:R={w.get('rr', '?')}:1"
            )
            if inv:
                lines.append(f"     invalidated if: {inv}")
        lines.append("")

    if news_events:
        lines.append(f"NEWS ACTIVE: {', '.join(news_events)}")
    if high_impact_2h:
        lines.append(
            "!!! HIGH-IMPACT EVENT ≤2H — NO NEW ENTRIES — wait M15 settlement !!!"
        )
    lines.append("")

    if last_ticks:
        lines.append("LAST SESSION ACTIVITY:")
        for t in last_ticks:
            lines.append(
                f"  Tick {t.get('tick', '?')} {t.get('sast_time', '?')} [{t.get('session', '')}] "
                f"— {t.get('action_taken', '')[:110]}"
            )
        lines.append("")

    lines += [
        "KEY RULES (ACTIVE IN EVERY TICK):",
        "  CHANGE 2: H4 gate — confirmed lower high + prior swing low broken (short). Absolute.",
        "  CHANGE 5: M15 structure broken in trade direction = entry trigger. No trigger = no trade.",
        "  Rule 5:   M5 reversed + negative P&L → cut immediately. No waiting.",
        "  Rule 13:  60%+ TP stalling at S/R → close.",
        "  Rule 14:  Gold float +R80 → SL to entry+5.",
        "  ENFORCER: exit 0=PASS proceed, exit 1=BLOCKED no re-run. Non-negotiable.",
        "  SL trail: use CLOSING price lows only — never wick extremes.",
        "  Same setup rejected 2x same session → skip that instrument entirely.",
        "  NEVER touch live account #43019560 without explicit 'use live account' instruction.",
        "=== END CONTEXT ===",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    context = build_context()
    output = {"hookEventName": "SessionStart", "additionalContext": context}
    print(json.dumps(output))

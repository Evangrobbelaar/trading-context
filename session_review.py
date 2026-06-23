#!/usr/bin/env python3
"""
Post-session pattern extractor (ECC evaluate-session.js pattern).
Run at session end: python session_review.py
Analyzes session_log.jsonl + enforcer_audit.jsonl for today,
prints a structured review, and writes knowledge/sessions/YYYY-MM-DD.md.
"""

import json
import os
import sys
from collections import defaultdict
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_jsonl(filename):
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
    return records


def filter_today(records, today_str):
    today_prefix = today_str.replace("-", "-")[:10]
    filtered = [
        r for r in records if r.get("timestamp_utc", "").startswith(today_prefix)
    ]
    if not filtered:
        # Fall back to last 30 records (covers sessions without today UTC prefix)
        filtered = records[-30:] if len(records) > 30 else records
    return filtered


def extract_instrument(trade_str):
    if not trade_str or trade_str == "none":
        return None
    return trade_str.split()[0].upper()


def analyze(ticks, enforcer_records):
    # Balance trajectory
    balances = [
        (t.get("sast_time", ""), t.get("account_balance_zar", 0))
        for t in ticks
        if t.get("account_balance_zar")
    ]

    session_pnl = None
    if len(balances) >= 2:
        session_pnl = balances[-1][1] - balances[0][1]

    # Loss events
    loss_instruments = []
    for t in ticks:
        action = t.get("action_taken", "")
        trade = t.get("trade_placed", "")
        if (
            ("Rule 5" in action or "SL hit" in action or "cut" in action.lower())
            and trade
            and trade != "none"
        ):
            inst = extract_instrument(trade)
            if inst:
                loss_instruments.append(inst)

    # Instrument frequency
    all_instruments = []
    for t in ticks:
        inst = extract_instrument(t.get("trade_placed", ""))
        if inst:
            all_instruments.append(inst)

    inst_count = defaultdict(int)
    for i in all_instruments:
        inst_count[i] += 1

    loss_count = defaultdict(int)
    for i in loss_instruments:
        loss_count[i] += 1

    # Enforcer stats
    blocked = [e for e in enforcer_records if e.get("verdict") == "BLOCKED"]
    passed = [e for e in enforcer_records if e.get("verdict") == "PASS"]

    # Sessions covered
    sessions = list({t.get("session", "") for t in ticks if t.get("session")})

    return {
        "session_pnl": session_pnl,
        "first_balance": balances[0][1] if balances else None,
        "last_balance": balances[-1][1] if balances else None,
        "total_ticks": len(ticks),
        "trades_placed": len(
            [
                t
                for t in ticks
                if t.get("trade_placed") and t.get("trade_placed") != "none"
            ]
        ),
        "enforcer_blocked": len(blocked),
        "enforcer_passed": len(passed),
        "blocked_details": blocked[:3],
        "instrument_count": dict(inst_count),
        "loss_count": dict(loss_count),
        "range_traps": {k: v for k, v in loss_count.items() if v >= 2},
        "sessions": sessions,
    }


def generate_patterns(analysis):
    patterns, warnings, observations = [], [], []

    # Range trap
    for inst, count in analysis["range_traps"].items():
        patterns.append(
            f"RANGE_TRAP: {inst} had {count} losses same session "
            f"— likely non-trending intraday environment despite H4 bias"
        )
        warnings.append(
            f"After 2nd Rule 5 cut on {inst}: skip rest of session, mark as range day"
        )

    # Concentration
    for inst, count in analysis["instrument_count"].items():
        if count >= 3:
            patterns.append(
                f"CONCENTRATION: {inst} traded {count}x — conviction bias risk"
            )
            warnings.append("Limit: max 2 entries per instrument per session")

    # P&L
    pnl = analysis["session_pnl"]
    if pnl is not None:
        if pnl >= 300:
            observations.append(
                f"Strong session +R{pnl:.2f} — system working, repeat conditions"
            )
        elif pnl >= 0:
            observations.append(f"Marginally positive +R{pnl:.2f} — acceptable")
        elif pnl >= -200:
            observations.append(
                f"Small loss -R{abs(pnl):.2f} — within acceptable drawdown"
            )
        else:
            warnings.append(
                f"Large loss -R{abs(pnl):.2f} — review if rules were followed"
            )

    # Enforcer
    if analysis["enforcer_blocked"] > 0:
        observations.append(
            f"Enforcer saved {analysis['enforcer_blocked']} blocked trade(s) this session"
        )

    # Trade count
    if analysis["trades_placed"] == 0:
        observations.append("No trades placed — waiting for setup is a valid decision")
    elif analysis["trades_placed"] > 4:
        warnings.append(
            f"{analysis['trades_placed']} trades placed — watch for overtrading"
        )

    return {"patterns": patterns, "warnings": warnings, "observations": observations}


def main():
    today_str = date.today().isoformat()
    if len(sys.argv) > 1:
        today_str = sys.argv[1]

    all_ticks = load_jsonl("session_log.jsonl")
    all_enforcer = load_jsonl("enforcer_audit.jsonl")

    ticks = filter_today(all_ticks, today_str)
    enforcer_records = filter_today(all_enforcer, today_str)

    if len(ticks) < 3:
        print(f"Only {len(ticks)} ticks for {today_str} — not enough data for review.")
        sys.exit(0)

    print(f"\n=== SESSION REVIEW — {today_str} ===")
    print(f"Ticks: {len(ticks)} | Enforcer checks: {len(enforcer_records)}\n")

    analysis = analyze(ticks, enforcer_records)
    patterns = generate_patterns(analysis)

    # Print metrics
    if analysis["first_balance"] and analysis["last_balance"]:
        pnl = analysis["last_balance"] - analysis["first_balance"]
        sign = "+" if pnl >= 0 else ""
        print(
            f"P&L:      R{analysis['first_balance']:.2f} → R{analysis['last_balance']:.2f} ({sign}R{pnl:.2f})"
        )
    print(f"Trades:   {analysis['trades_placed']} placed")
    print(
        f"Enforcer: {analysis['enforcer_passed']} PASS / {analysis['enforcer_blocked']} BLOCKED"
    )
    print(f"Sessions: {', '.join(analysis['sessions']) or 'unknown'}")

    if patterns["patterns"]:
        print("\nPATTERNS DETECTED:")
        for p in patterns["patterns"]:
            print(f"  !! {p}")

    if patterns["warnings"]:
        print("\nWARNINGS:")
        for w in patterns["warnings"]:
            print(f"  > {w}")

    if patterns["observations"]:
        print("\nOBSERVATIONS:")
        for o in patterns["observations"]:
            print(f"  - {o}")

    # Save session file
    knowledge_dir = os.path.join(BASE_DIR, "knowledge", "sessions")
    os.makedirs(knowledge_dir, exist_ok=True)
    session_file = os.path.join(knowledge_dir, f"{today_str}.md")

    with open(session_file, "w", encoding="utf-8") as f:
        f.write(f"# Session Review — {today_str}\n\n")
        if analysis["first_balance"] and analysis["last_balance"]:
            pnl = analysis["last_balance"] - analysis["first_balance"]
            sign = "+" if pnl >= 0 else ""
            f.write(
                f"**P&L:** {sign}R{pnl:.2f} "
                f"| Balance: R{analysis['first_balance']:.2f} → R{analysis['last_balance']:.2f}\n\n"
            )
        f.write(
            f"**Ticks:** {analysis['total_ticks']} | **Trades:** {analysis['trades_placed']}\n\n"
        )

        if patterns["patterns"]:
            f.write("## Patterns\n\n")
            for p in patterns["patterns"]:
                f.write(f"- {p}\n")
            f.write("\n")

        if patterns["warnings"]:
            f.write("## Warnings\n\n")
            for w in patterns["warnings"]:
                f.write(f"- {w}\n")
            f.write("\n")

        if patterns["observations"]:
            f.write("## Observations\n\n")
            for o in patterns["observations"]:
                f.write(f"- {o}\n")
            f.write("\n")

        if analysis["blocked_details"]:
            f.write("## Enforcer Blocks\n\n")
            for b in analysis["blocked_details"]:
                reasons = "; ".join(b.get("block_reasons", []))
                f.write(
                    f"- {b.get('instrument')} {b.get('direction')} blocked: {reasons}\n"
                )
            f.write("\n")

    print(f"\nSession file → knowledge/sessions/{today_str}.md")
    print(
        "SIGNAL: Review done — copy any new patterns into EVAN_TRADING_CONTEXT.md lessons section."
    )


if __name__ == "__main__":
    main()

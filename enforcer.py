#!/usr/bin/env python3
"""
PRE-TRADE ENFORCER v3 — REBUILT 10 Jul 2026 (post-rebuild-phase)

Replaces v2 (rebuild-phase, 2 checks only). v1 logic remains in git history.
v3 is built around SPRUNG LADDER v1.1 (see STRATEGY_SPRUNG_LADDER.md) plus
the general lessons that survived the rebuild review:
  - 8 Jul: XAUUSD -R513 single trade (~8% of balance) with no per-trade gate
  - 9 Jul (tick 20): 7-pending book = 22% aggregate worst-case, nothing caught it
  - MCP account-revert incidents x4: account lock must be code, not vigilance

CHECKS (all trades):
  1. SESSION MAX LOSS   — balance <= 50% of session start => block everything
  2. TIME VALIDITY      — outside forex market hours => block
  3. ACCOUNT LOCK       — account_id != 41829612 => block (hard rule)
  4. PER-TRADE RISK     — risk_amount > 5% of balance => block
  5. AGGREGATE EXPOSURE — (this trade + open + pending worst-case) > 25% => block
  6. NEWS ATTESTATION   — --news_checked flag required; high-impact within 2h => block

CHECKS (--mode scout):
  7.  Scout size must be minimum lot for the instrument (--lots == --min_lots)
  8.  Scout count after this order <= 3 (NEVER a 4th)
  9.  Total scout risk (all scouts incl. this one) <= 2% of balance
  10. Range attestation: --range_touches >= 2 per side AND --range_width >= 1.5 * --scout_sl
      (scout SL itself must equal ~4x H1 ATR: 3.5x-4.5x accepted)
  11. TREND-VERDICT LOCKOUT: instrument had a trend verdict < 24h ago => block

CHECKS (--mode strike):
  12. Strike risk <= 5% of balance
  13. All three trigger attestations required: --swept --reclaimed_15min --m5_close
  14. SL structural: --sl_below_sweep flag required

STATE: session_state.json gains "trend_verdicts": {instrument: iso_ts}.
Record a verdict with:  python3 enforcer.py --record_verdict EURGBP
Exit code 1 = BLOCKED. All decisions appended to enforcer_audit.jsonl.
"""
import argparse, sys, json, os
from datetime import datetime, timezone, timedelta

STATE_FILE = "session_state.json"
AUDIT_FILE = "enforcer_audit.jsonl"
SESSION_MAX_LOSS_PCT = 0.50
PER_TRADE_RISK_PCT   = 0.05
AGGREGATE_RISK_PCT   = 0.25
SCOUT_TOTAL_RISK_PCT = 0.02
STRIKE_RISK_PCT      = 0.05
MAX_SCOUTS           = 3
VERDICT_LOCKOUT_H    = 24
ALLOWED_ACCOUNT      = "41829612"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, indent=2)

def check_time(now_utc):
    wd, h = now_utc.weekday(), now_utc.hour
    if wd == 5: return "Market closed — Saturday."
    if wd == 6 and h < 21: return "Market closed — Sunday before 21:00 UTC."
    if wd == 4 and h >= 21: return "Market closed — Friday after 21:00 UTC."
    return None

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--account", choices=["demo","live"], default="demo")
    p.add_argument("--account_id", default=None)
    p.add_argument("--balance", type=float, default=None)
    p.add_argument("--init", action="store_true")
    p.add_argument("--now", default=None)
    p.add_argument("--mode", choices=["general","scout","strike"], default="general")
    p.add_argument("--instrument", default="?")
    p.add_argument("--risk_amount", type=float, default=None, help="worst-case loss of THIS order in account ccy")
    p.add_argument("--open_pending_risk", type=float, default=0.0, help="summed worst-case of all existing open+pending")
    p.add_argument("--news_checked", action="store_true", help="attest: news scan run")
    p.add_argument("--news_clear", action="store_true", help="attest: no high-impact within 2h for this instrument")
    # scout args
    p.add_argument("--lots", type=float, default=None)
    p.add_argument("--min_lots", type=float, default=None)
    p.add_argument("--scout_count_after", type=int, default=None)
    p.add_argument("--scout_total_risk", type=float, default=None)
    p.add_argument("--range_touches", type=int, default=None, help="min touches per side on H1")
    p.add_argument("--range_width", type=float, default=None, help="pips")
    p.add_argument("--scout_sl", type=float, default=None, help="pips")
    p.add_argument("--h1_atr", type=float, default=None, help="pips")
    # strike args
    p.add_argument("--swept", action="store_true")
    p.add_argument("--reclaimed_15min", action="store_true")
    p.add_argument("--m5_close", action="store_true")
    p.add_argument("--sl_below_sweep", action="store_true")
    # Rule 17 session-range gate (v3.1, tick 45) — binds only when all four supplied.
    # Auto ticks MUST supply these; attended sessions unchanged if omitted.
    p.add_argument("--entry", type=float, default=None)
    p.add_argument("--direction", choices=["buy", "sell"], default=None)
    p.add_argument("--session_high", type=float, default=None)
    p.add_argument("--session_low", type=float, default=None)
    p.add_argument("--learn", action="store_true",
                   help="LEARN mode: discretionary gates (Rule 17) downgrade to warnings and are "
                        "recorded as counterfactuals. Hard gates (account, market hours, session "
                        "max loss, news, stop geometry) still block. Forces minimum size upstream.")
    p.add_argument("--breakout_confirmed", action="store_true",
                   help="attest: confirmed H1 close beyond the session range (Rule 17 exception)")
    # verdict recording
    p.add_argument("--record_verdict", default=None, metavar="INSTRUMENT")
    args = p.parse_args()

    now_utc = datetime.now(timezone.utc)
    if args.now:
        try: now_utc = datetime.fromisoformat(args.now)
        except ValueError: pass

    state = load_state()

    if args.record_verdict:
        state.setdefault("trend_verdicts", {})[args.record_verdict.upper()] = now_utc.isoformat()
        save_state(state)
        print(f"TREND VERDICT recorded for {args.record_verdict.upper()} — 24h scout lockout active.")
        return 0

    if args.balance is None or args.account_id is None:
        print("BLOCKED: --balance and --account_id are required."); return 1

    blocks = []
    warns = []

    # 3. ACCOUNT LOCK
    if str(args.account_id) != ALLOWED_ACCOUNT:
        blocks.append(f"ACCOUNT LOCK: {args.account_id} is not {ALLOWED_ACCOUNT}. 41750592 is permanently off-limits.")

    # 2. TIME
    t = check_time(now_utc)
    if t: blocks.append(t)

    # 1. SESSION MAX LOSS
    if args.init:
        state["session_start_balance"] = args.balance
        state["session_start_ts"] = now_utc.isoformat()
        save_state(state)
    start = state.get("session_start_balance")
    if start and args.balance <= start * SESSION_MAX_LOSS_PCT:
        blocks.append(f"SESSION MAX LOSS: balance {args.balance:.2f} <= 50% of session start {start:.2f}.")

    # 4/5. RISK GATES (any non-init order should supply risk_amount)
    if not args.init or args.risk_amount is not None:
        if args.risk_amount is None:
            blocks.append("PER-TRADE RISK: --risk_amount not supplied — cannot verify, blocked by default.")
        else:
            if args.risk_amount > args.balance * PER_TRADE_RISK_PCT:
                blocks.append(f"PER-TRADE RISK: {args.risk_amount:.2f} > {PER_TRADE_RISK_PCT*100:.0f}% of balance ({args.balance*PER_TRADE_RISK_PCT:.2f}).")
            agg = args.risk_amount + args.open_pending_risk
            if agg > args.balance * AGGREGATE_RISK_PCT:
                blocks.append(f"AGGREGATE EXPOSURE: {agg:.2f} > {AGGREGATE_RISK_PCT*100:.0f}% of balance ({args.balance*AGGREGATE_RISK_PCT:.2f}). (Tick-20 lesson: 22% book with no gate.)")

        # 6. NEWS
        if not args.news_checked:
            blocks.append("NEWS: news scan not attested (--news_checked missing).")
        elif not args.news_clear:
            blocks.append("NEWS: high-impact event within 2h for this instrument (--news_clear not set).")

    # 7. RULE 17 — SESSION RANGE POSITION (v3.1, tick 45; two casualties before codification:
    #    EURUSD 25 Jun top-1% entry, WTI 21 Jul top-4.3% entry). Binds only when args supplied.
    if (args.entry is not None and args.direction and
            args.session_high is not None and args.session_low is not None):
        rng = args.session_high - args.session_low
        if rng > 0:
            pos = (args.entry - args.session_low) / rng
            if args.direction == "buy" and pos >= 0.85 and not args.breakout_confirmed:
                (warns if args.learn else blocks).append(
                    f"RULE 17{' [LEARN-OVERRIDE]' if args.learn else ''}: BUY at {pos*100:.1f}% of session range (top 15%). "
                              f"Wait for the pullback, or attest --breakout_confirmed (H1 close beyond range).")
            if args.direction == "sell" and pos <= 0.15 and not args.breakout_confirmed:
                (warns if args.learn else blocks).append(
                    f"RULE 17{' [LEARN-OVERRIDE]' if args.learn else ''}: SELL at {pos*100:.1f}% of session range (bottom 15%). "
                              f"Wait for the pullback, or attest --breakout_confirmed (H1 close beyond range).")

    # SCOUT MODE
    if args.mode == "scout":
        if args.lots is None or args.min_lots is None or args.lots > args.min_lots:
            blocks.append(f"SCOUT SIZE: lots must equal instrument minimum ({args.min_lots}). Scouts are sensors, not positions.")
        if args.scout_count_after is None or args.scout_count_after > MAX_SCOUTS:
            blocks.append(f"SCOUT COUNT: max {MAX_SCOUTS} scouts. NEVER a 4th.")
        if args.scout_total_risk is None or args.scout_total_risk > args.balance * SCOUT_TOTAL_RISK_PCT:
            blocks.append(f"SCOUT RISK: total scout risk must be <= 2% of balance ({args.balance*SCOUT_TOTAL_RISK_PCT:.2f}).")
        if args.range_touches is None or args.range_touches < 2:
            blocks.append("RANGE: need >= 2 touches per side on H1 (proven range).")
        if args.scout_sl is None or args.h1_atr is None or not (3.5*args.h1_atr <= args.scout_sl <= 4.5*args.h1_atr):
            blocks.append("SCOUT SL: must be ~4x H1 ATR (3.5x-4.5x accepted) per v1.1 amendment.")
        if args.range_width is None or args.scout_sl is None or args.range_width < 1.5*args.scout_sl:
            blocks.append("RANGE WIDTH: must be >= 1.5x scout SL per v1.1 amendment.")
        verdicts = state.get("trend_verdicts", {})
        vts = verdicts.get(args.instrument.upper())
        if vts:
            age = now_utc - datetime.fromisoformat(vts)
            if age < timedelta(hours=VERDICT_LOCKOUT_H):
                blocks.append(f"VERDICT LOCKOUT: {args.instrument} had a trend verdict {age} ago (<24h). No re-arm.")

    # STRIKE MODE
    if args.mode == "strike":
        if args.risk_amount is not None and args.risk_amount > args.balance * STRIKE_RISK_PCT:
            blocks.append(f"STRIKE RISK: > 5% of balance ({args.balance*STRIKE_RISK_PCT:.2f}).")
        if not (args.swept and args.reclaimed_15min and args.m5_close):
            blocks.append("STRIKE TRIGGER: all three required — level swept, reclaim within 15min, full M5 close above. Missing at least one.")
        if not args.sl_below_sweep:
            blocks.append("STRIKE SL: must be structural, 3-5 pips below sweep extreme (--sl_below_sweep).")

    verdict = "BLOCKED" if blocks else "PASS"
    audit = {"ts": now_utc.isoformat(), "verdict": verdict, "mode": args.mode,
             "instrument": args.instrument, "account_id": args.account_id,
             "balance": args.balance, "risk_amount": args.risk_amount,
             "blocks": blocks, "version": "v3.1"}
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(audit) + "\n")

    if warns:
        for w in warns:
            print(f"WARN: {w}")
    if blocks:
        print("BLOCKED:")
        for b in blocks: print(f"  - {b}")
        return 1
    print(f"PASS — {args.mode} on {args.instrument} cleared (v3.1).")
    return 0

if __name__ == "__main__":
    sys.exit(main())

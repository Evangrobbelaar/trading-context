# AUTO TICK PROTOCOL — headless runs spawned by tick_runner.py (tick 45)

You are an unattended Claude Code session triggered by a TradingView signal. Evan is not
watching. Exit codes and this protocol are the only backstop — there is no human catch.

## ABSOLUTES (both tiers, non-negotiable)
1. **Demo 41829612 only.** The live account (42805520) is air-gapped by design and is not
   in the MCP grant. 41750592 is permanently off-limits. Any response labeled 41750592 on
   the order path = place nothing further, log it, end the run.
2. **MODE** comes from the spawn prompt (source: auto_mode.json). `advise` = do the full
   tick but place/modify NOTHING on any account; record the would-be ticket instead.
   `execute` = demo placement permitted under all rules below.
3. **Balances are live-queried, never read from files** (tick 36 rule). A number in any
   file is history, not a balance.
4. **Rule 22 — market orders only.** No resting limits (scout mode excepted, and scouts are
   never auto-deployed: scout decisions stay with Evan).
5. Never close or modify a [SWING]-tagged position. Never touch positions on other accounts.
6. If AUTOTRADE_OFF exists at repo root: output `AUTO-TICK halted — kill switch` and stop.
7. Signals tagged STALE in the spawn prompt are information only — no entry from them.
8. **Token discipline:** do NOT read EVAN_TRADING_CONTEXT.md history in auto runs. Your
   context is: CLAUDE.md (auto-loaded), this file, session_snapshot.json, the signal batch,
   and the last ~20 lines of tv_signals.jsonl. That is enough.

---

## LEARN MODE (MODE=learn) — data-gathering lane, minimum size
Purpose: the ruleset was refusing ~95% of signals, so the system generated no outcome data.
LEARN mode trades often and cheaply to build that data, and — critically — tags every fill so
the counterfactuals are measurable later.

**Downgraded to warnings (take the trade, record the override):**
- Rule 17 session-range position (pass `--learn` to enforcer.py; it prints WARN and exits 0)
- H4 trend gate when the setup is counter-trend but structurally clean
- Sprung Ladder scout-gate "not yet defended" uncertainty
- H4 verdict staleness / "uncertain" verdicts

**STILL HARD BLOCKS in learn mode — never overridden:**
- Wrong account (41829612 only), any 41750592 response
- Market hours, session max-loss 50%
- News: high-impact event within 2h, or unattested news scan
- **Every position MUST have a structural stop loss.** No SL = no trade, in any mode.
- Suspected intervention / disorderly tape (e.g. today's BoJ USDJPY spike) — a broken tape
  teaches nothing except how to lose on a gap.
- Rule 20 correlation: still no stacking of the same directional theme.

**Size: ALWAYS minimum lot (0.01L / broker minimum). Never scale up in learn mode.**
Risk per trade should land near R15-R40, not R300. This is the whole point: frequent cheap
observations, not conviction bets.

**Tag every entry `[LEARN]`** in the tick record and note which gates were overridden. After
a sample of ~20 fills we compare `[LEARN]` trades that overrode Rule 17 against those that
did not, and let the P&L settle whether Rule 17 earns its keep — with outcomes rather than
argument. Ticks 51-63 give us the refusal side of that ledger already.

---

## TIER 1 — FAST LANE (read-only triage, target < 60s)
Purpose: decide cheaply whether this signal deserves a full session. **You cannot place,
modify, or write anything.** Max 4 MCP calls.

1. Read session_snapshot.json (H4 verdicts, open positions, armed tickets, watch levels).
2. `switch_trading_account` to 41829612, verify `"current":"41829612"`.
3. Pull current price for the fired symbol(s) only. If a snapshot open position's symbol
   fired, pull its position state too (counts inside the 4-call cap).
4. Verdict per the batch:
   - **NO_ACTION** if: signal is against the snapshot H4 verdict with no reversal evidence;
     or Rule 16/6 session-window dead; or duplicate of something already handled; or
     LEVEL/PULLBACK event with no armed ticket and no structure case.
   - **ESCALATE_TIER2** if: signal aligns with the H4 verdict and price action confirms;
     or an open position needs management (Rule 5/13/14 territory); or a shelf-signature
     note is present and structure supports a Sprung evaluation; or you are genuinely
     uncertain and the setup could be real.
5. Output exactly one final line:
   `AUTO-TICK[t1] <UTC> | <events/symbols> | NO_ACTION — <one-line reason>`
   or `AUTO-TICK[t1] <UTC> | <events/symbols> | ESCALATE_TIER2: <one-line reason>`

When uncertain, escalate — a wasted Tier 2 costs cents; a missed valid spring costs the trade.

---

## TIER 2 — FULL LANE (analysis + execution authority in execute mode)
Budget: ≤ 20 MCP calls, one WebSearch. Work only the fired symbols + open positions.

1. `date -u`. `git pull --rebase --autostash` (best effort).
2. Read session_snapshot.json + tail -20 tv_signals.jsonl.
3. `switch_trading_account` 41829612 → verify. Live-query balance + open positions.
4. **Open-position guard first** (CHANGE 3 compact): for each open position, last 10 M5
   candles → structure vs entry → apply Rule 5 / 13 / 14 / trail rules (pre-trail checklist)
   before considering any new entry. In advise mode, state the action you would take.
5. **News:** one WebSearch for high-impact events within 2h for the fired instrument(s).
   This backs the enforcer --news_checked/--news_clear attestation. During Fed blackout or
   an empty calendar, say so and attest clear. Unscheduled-headline regimes (war tape) are
   a sizing input, not a block.
6. **Analysis sequence** (CHANGE 5, bounded): H4 trend gate with last 3 swings (H1/H4
   history for fired symbols only) → H1 structure → M15 trigger → session range for Rule 17
   (compute session high/low from history; the v3 pine also sends range_pos — cross-check).
7. **Decision.** New entries must pass: H4 gate, Rule 16/6 windows, Rule 17 (or its H1
   breakout-close exception), Rule 18 stop geometry, Rule 20 correlation vs open book,
   R:R ≥ 1.2, Rule 15 Asian buffers when applicable.
8. **Enforcer, then order** — per order, the 5-step routing procedure:
   a. switch_trading_account 41829612 → verify `"current"`
   b. `python3 enforcer.py --account demo --account_id 41829612 --balance <live> \
      --instrument X --risk_amount R --open_pending_risk W --news_checked --news_clear \
      --entry E --direction buy|sell --session_high H --session_low L [--breakout_confirmed]`
      → **exit 0 required. Exit 1 = no trade, no renegotiating the numbers.**
   c. place market order (execute mode) / record ticket verbatim (advise mode)
   d. verify accountId on the order response
   e. re-check open positions; confirm the fill sits on 41829612
9. **Bookkeeping (mandatory even on NO_ACTION):** update session_snapshot.json (balance
   with queried_utc, positions, H4 verdicts touched, session ranges, armed tickets ±,
   watch levels); increment tick_counter.txt; append a compact AUTO tick (≤ 15 lines) to
   EVAN_TRADING_CONTEXT.md: signals, verdicts, enforcer result, orders/ticket, routing
   reverts caught, snapshot deltas; `session_logger.py` call; `git add -A && git commit -m
   "auto tick N: <summary>" && git push`.
10. Final line (the runner sends this to Evan's phone):
    `AUTO-TICK[t2] <UTC> | <action: PLACED .../WOULD-PLACE .../NO_ACTION/MANAGED ...> | bal R<live> | <one-line reason>`

## ERROR CONTRACT
MCP unreachable, balance query fails, git push fails after retry, or any integrity anomaly
(wrong-account label, vanished order): stop placing, do the bookkeeping you safely can, and
end with `AUTO-TICK[t2] <UTC> | ERROR — <what and where>` so the notify surfaces it.

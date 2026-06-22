# LOOP SETUP v2.0 — Claude Code Native Trading Loop
Updated: June 22, 2026

## QUICK START

Open Claude Code in this directory, then paste the session loop command below.
CLAUDE.md auto-loads EVAN_TRADING_CONTEXT.md as context on startup.

---

## HOW THE LEARNING WORKS

Claude's model weights do not change between sessions. What improves is the
WRITTEN RULESET in EVAN_TRADING_CONTEXT.md. This is not a limitation — it is
how the system has always worked. Rules 1-14, the H4 trend gate, and the
enforcer rule all came from real sessions being reviewed and turned into
specific written rules. The loops below formalize that process:

```
TICK LOOP (every 5 min, trading hours)
  → monitors positions, scans markets, runs enforcer
  → logs every decision to session_log.jsonl
  → does not guess, does not skip, does not bypass

SESSION END (after loop stops)
  → session summary appended to EVAN_TRADING_CONTEXT.md
  → committed to GitHub

WEEKLY REVIEW (Monday session open — run manually)
  → reads session_log.jsonl + enforcer_audit.jsonl
  → identifies patterns across all sessions
  → proposes specific rule diffs
  → Evan approves before anything is committed
```

The system "learns" by the ruleset getting more precise every week.
Blocked trades that would have lost = the enforcer earning its keep.
Passed trades that lost = new rules get written.

---

## SESSION LOOP

Paste this command at the start of any trading session:

```
/loop 5m Execute one trading tick per CLAUDE.md session protocol. Tick sequence: (1) get SAST time from market data + account balance + open positions via MCP, (2) for each open position pull last 10 M5 candles and output the mandatory CHANGE 4 format with action recommendation, (3) scan XAUUSD/EURUSD/GBPUSD/USDJPY/XAGUSD — get prices and H4 history, run CHANGE 5 analysis sequence — news first then H4 trend gate then H1 then M15, (4) if a trade candidate passes the H4 trend gate compute risk_amount/reward_amount/sl_distance exactly and run: python3 enforcer.py with all required args — exit code 1 is an absolute block, (5) if enforcer passes call claude:create_market_order, (6) always end tick by running: python3 session_logger.py with all required args. STOP CONDITIONS: halt loop immediately if 3 consecutive losing trades this session OR session drawdown exceeds 10% of start balance OR 20 ticks reached OR time after 22:00 SAST. After loop ends: pull closed trades, calculate session P&L, append session summary to EVAN_TRADING_CONTEXT.md, commit to GitHub.
```

**Notes:**
- Esc stops the loop at any point — stopping is free, a bad trade is not
- Default account: demo #41810679 only
- To use live account (#43019560): say "switch to live account" explicitly this session
  — Claude will not touch live without this instruction
- Loop prints tick number, SAST time, and action taken each iteration

---

## POSITION MONITOR LOOP

Use this when you have open positions and just want monitoring (no new trades):

```
/loop 10m Monitor open positions only — no new trade entries. For each open position: get current price and last 10 M5 candles via claude:get_symbol_history. Output CHANGE 4 format: TREND, M5 STRUCTURE, P&L percentage to TP, ACTION. Apply Rule 4 (50% TP + shrinking candles = close), Rule 13 (60%+ TP + S/R stall = close), Rule 14 (Gold +R80 floating = SL to entry+5). Log each tick via python3 session_logger.py. Stop if: position closed, or Evan types stop, or 12 ticks reached.
```

---

## WEEKLY REVIEW (run Monday session open)

This is NOT a /loop command — it is a one-shot prompt. Paste it in a fresh
Claude Code session on Monday morning before trading begins:

```
Run the weekly trading review. Read EVAN_TRADING_CONTEXT.md fully first.
Then read enforcer_audit.jsonl and session_log.jsonl — all entries since
the last review date noted in EVAN_TRADING_CONTEXT.md.

Produce this analysis:
1. ENFORCER AUDIT: List every BLOCKED trade. For each: what would the outcome
   have been? (check if instrument moved in trade direction after block time)
   These are cases where the enforcer earned its keep.

2. LOSS ANALYSIS: List every closed losing trade from session_log. For each:
   - What was the H4 trend at entry?
   - Did it pass the trend gate correctly?
   - What rule, if any, was violated?
   - Root cause in one sentence (same format as June 11 post-mortem).

3. WIN ANALYSIS: List closed winning trades. What conditions were present?
   Session, instrument, H4 trend direction, entry trigger. Look for repeating
   patterns across 3+ winners.

4. PATTERN SUMMARY: Any recurring pattern across 3+ trades (win or loss)?
   e.g. "London session GBPUSD shorts with H4 lower highs = 4/5 wins"
   or "Gold longs during bearish H4 = 0/3 wins (trend gate should have blocked)"

5. PROPOSED RULE CHANGES: Write specific additions or edits to
   EVAN_TRADING_CONTEXT.md as a diff. Be concrete — not "trade better" but
   "Add Rule 15: during London session, GBPUSD at 0.03L with confirmed H4
   lower highs outperforms Gold — prioritise GBP over Gold when both set up."

DO NOT commit anything. Print the proposed diff and wait for Evan's explicit
"approve and commit" before writing to GitHub.
DO NOT auto-approve any change to risk sizing (MAX_RISK_PCT, lot sizes, SL
buffers) — those require Evan's explicit sign-off every time.
```

---

## ENFORCER QUICK REFERENCE

```bash
# Gold (always 1 unit)
python3 enforcer.py --instrument XAUUSD --direction buy --units 1 \
  --balance [ZAR] --account demo \
  --risk_amount [pts × R16] --reward_amount [pts × R16] --sl_distance [pts]

# Forex / Silver (lots)
python3 enforcer.py --instrument GBPUSD --direction sell --lots 0.02 \
  --balance [ZAR] --account demo \
  --risk_amount [pips × R5.46] --reward_amount [pips × R5.46] --sl_distance [pips]

# Swing stock (add --swing flag, bypasses intraday SL buffer check)
python3 enforcer.py --instrument NVIDIA --direction buy --lots 0.1 \
  --balance [ZAR] --account demo \
  --risk_amount [R] --reward_amount [R] --sl_distance [pts] --swing

# Review logs
python3 session_logger.py summary              # all-time summary
python3 session_logger.py summary 2026-06-15   # since date
cat enforcer_audit.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    e = json.loads(line)
    if e['verdict'] == 'BLOCKED':
        print(e['timestamp_utc'][:10], e['instrument'], e['block_reasons'][0][:60])
"
```

---

## APPROXIMATE INSTRUMENT VALUES (ZAR, demo account sizing)

| Instrument | Size | Value per unit move |
|---|---|---|
| XAUUSD | 1 unit | ~R16/pt |
| GBPUSD | 0.03L | ~R5.46/pip |
| EURUSD | 0.03L | ~R5.46/pip |
| XAGUSD | 0.01L | ~R1-2/pip (micro) |
| USDJPY | 0.03L | ~R5.46/pip |
| NAS100 | blocked <R5,000 | — |

These are approximates. Claude must calculate exact risk_amount and reward_amount
from actual SL/TP distances before calling enforcer.py.

---

## STOP CONDITIONS REFERENCE

| Condition | Threshold | Action |
|---|---|---|
| Consecutive losses | 3 in a row | Stop loop, review before resuming |
| Session drawdown | >10% of start balance | Stop loop, no more trades today |
| Max ticks | 20 | Stop loop, end session |
| Time | After 22:00 SAST | Stop loop, NY close |
| Manual | Evan types "stop loop" | Stop immediately |
| Enforcer | Exit code 1 | Block that trade, continue loop |

Note: enforcer block ≠ loop stop. A blocked trade is normal — the loop continues
scanning for the next setup. Only the drawdown/loss/tick conditions stop the loop.

---

## FILE STRUCTURE

```
trading-context/
├── CLAUDE.md                  ← auto-loaded by Claude Code on startup
├── EVAN_TRADING_CONTEXT.md    ← the "brain" — grows every session
├── enforcer.py                ← deterministic trade gate (numeric rules only)
├── session_logger.py          ← tick logger (--tick, summary mode)
├── LOOP_SETUP.md              ← this file — loop commands + reference
├── enforcer_audit.jsonl       ← auto-written by enforcer.py (every check)
├── session_log.jsonl          ← auto-written by session_logger.py (every tick)
└── MASTER_PROMPT_EXTERNAL_CONTEXT_SYSTEM.md  ← framework docs
```

enforcer_audit.jsonl and session_log.jsonl are the raw data the weekly review
reads to propose rule improvements. Never delete them — they are the learning record.

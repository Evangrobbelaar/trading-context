# LOOP SETUP v2.1 — Dual-Session Trading Schedule
Updated: June 22, 2026 | Account: Demo #41829612 | Goal: R5,000 → R10,000

---

## SHOULD YOU LEAVE IT RUNNING 24/7? NO.

Here is exactly why, based on historical session data:

| Period | Evidence | Decision |
|---|---|---|
| Asian 00:00–07:00 SAST | Zero profitable trades across all recorded sessions | Off |
| London 09:00–12:00 SAST | Good setups, second-best session | ✅ Run |
| Quiet 12:00–15:00 SAST | Low volume, no clean setups found in any session | Off |
| London/NY 15:00–18:00 SAST | "Most of the day's profit came after 15:30" — Jun 8 note | ✅ Run |
| NY-only 18:00–22:00 SAST | Secondary, only useful if already in a trade | Off |
| Weekend | XAUUSD247 spread 8× wider, no structure | Off |

Running overnight creates trades with no human oversight, MCP drops with no one
to notice, and entries in illiquid hours with bad spreads. The system is designed
to place 1–2 quality trades per session — 6 hours/day is enough.

---

## DAILY ROUTINE (weekdays only)

```
08:45 SAST  → Open Claude Code in this directory
             → Context auto-loads from CLAUDE.md
             → Start LONDON SESSION loop (paste command below)
             → Check back at ~12:00 to see what happened

12:00 SAST  → London loop auto-stops (session end condition)
             → Review what the loop did, check any open trades

14:45 SAST  → Start LONDON/NY SESSION loop (paste command below)
             → This is the BEST session — be available to watch

18:00 SAST  → London/NY loop auto-stops
             → Session summary auto-committed to GitHub
             → Done for the day
```

Total active loop time: ~6 hours/day. Max 4 trades/day (2 per session cap).

---

## SESSION 1 — LONDON OPEN (paste this at 08:45 SAST)

```
/loop 10m Execute one trading tick per CLAUDE.md session protocol. Switch to demo account 41829612 first. Tick sequence: (1) get SAST time from XAUUSD price timestamp + account balance + open positions, (2) if positions open pull last 10 M5 candles and output CHANGE 4 format with action, (3) if fewer than 2 trades placed this session scan XAUUSD/EURUSD/GBPUSD/USDJPY/XAGUSD — prices then H4 history then run CHANGE 5 analysis — news first then H4 trend gate then H1 then M15, (4) if trade candidate passes trend gate run: python3 enforcer.py with exact risk_amount/reward_amount/sl_distance — exit code 1 is absolute block, (5) if enforcer passes call mcp__claude_ai_claude__create_market_order, (6) end every tick by running python3 session_logger.py with all required args. STOP CONDITIONS: 2 trades placed this session OR 2 consecutive losses OR drawdown exceeds R500 OR 18 ticks reached OR time after 12:00 SAST. After stop: pull closed trades, calculate P&L, append session summary to EVAN_TRADING_CONTEXT.md, commit to GitHub.
```

**Why 10-minute ticks for London:** London open is about quality setups, not speed.
H4 structures take time to develop. 10-min ticks = 18 ticks over 3 hours = enough
coverage without burning through API calls on an unchanged picture.

---

## SESSION 2 — LONDON/NY OVERLAP (paste this at 14:45 SAST)

```
/loop 5m Execute one trading tick per CLAUDE.md session protocol. Switch to demo account 41829612 first. Tick sequence: (1) get SAST time from XAUUSD price timestamp + account balance + open positions, (2) if positions open pull last 10 M5 candles and output CHANGE 4 format with action, (3) if fewer than 2 trades placed this session scan XAUUSD/EURUSD/GBPUSD/USDJPY/XAGUSD — prices then H4 history then run CHANGE 5 analysis — news first then H4 trend gate then H1 then M15, (4) if trade candidate passes trend gate run: python3 enforcer.py with exact risk_amount/reward_amount/sl_distance — exit code 1 is absolute block, (5) if enforcer passes call mcp__claude_ai_claude__create_market_order, (6) end every tick by running python3 session_logger.py with all required args. STOP CONDITIONS: 2 trades placed this session OR 2 consecutive losses OR drawdown exceeds R500 OR 36 ticks reached OR time after 18:00 SAST. After stop: pull closed trades, calculate P&L, append session summary to EVAN_TRADING_CONTEXT.md, commit to GitHub.
```

**Why 5-minute ticks for London/NY:** This is the fastest-moving session. Gold and
Forex can set up and trigger within 15–20 minutes. 5-min ticks catch entries that
10-min ticks miss. Historical evidence: the +R179 Gold trade and +R55 EURUSD trade
on Jun 8 both triggered within a 21-minute window at 15:32-15:53 SAST.

---

## CRON SCHEDULE (alternative — fires automatically on weekdays)

If you want the loop to start automatically without pasting the command:

**London session auto-start (07:00 UTC = 09:00 SAST, Mon-Fri):**
```
/loop — set up a cron to run at 07:00 UTC weekdays that pastes the London session command
```
Note: Use this only if you trust the auto-start. If you want to manually verify
market conditions before each session, paste the command manually instead.

---

## WEEKLY REVIEW (every Monday, paste before first session)

```
Run the weekly trading review. Read EVAN_TRADING_CONTEXT.md fully first. Then read
enforcer_audit.jsonl and session_log.jsonl — all entries since the previous Monday.

Produce this analysis:
1. ENFORCER AUDIT: Every BLOCKED trade — would it have won or lost?
   These prove whether the enforcer is saving money or missing opportunities.
2. LOSS ANALYSIS: Every losing trade — H4 trend at entry, rule violated, root cause
   in one sentence (same format as Jun 11 post-mortem).
3. WIN ANALYSIS: Every winning trade — session, instrument, H4 direction, entry type.
   Which patterns repeat across 3+ winners?
4. PATTERN SUMMARY: Any recurring edge worth adding as a rule?
   e.g. "XAUUSD London/NY overlap with confirmed H4 higher low = 4/5 wins"
5. PROGRESS: Current balance vs R5,000 start. % toward R10,000 goal.
6. PROPOSED RULE CHANGES: Specific additions to EVAN_TRADING_CONTEXT.md as a diff.
   One rule per finding. Concrete, not generic.

DO NOT commit anything. Print the proposed diff and wait for Evan's approval.
DO NOT auto-approve any change to risk sizing or lot limits — those need Evan's explicit sign-off.
```

---

## R5,000 SIZING REFERENCE

| Instrument | Size | Value/unit | 20pt/pip SL | % of R5,000 |
|---|---|---|---|---|
| XAUUSD | 1 unit | R16/pt | R320 | 6.4% |
| GBPUSD | 0.03L | R5.46/pip | R109 | 2.2% |
| EURUSD | 0.03L | R5.46/pip | R109 | 2.2% |
| XAGUSD | 0.01L | ~R3.60/pip | R72 | 1.4% |
| NAS100 | BLOCKED | — | blocked <R5,000 | — |

Max risk per trade: R1,000 (20%). Max simultaneous trades: 2.
Do NOT increase lot sizes until balance confirmed above R8,000.

---

## ENFORCER QUICK REFERENCE

```bash
# Gold (1 unit only)
python3 enforcer.py --instrument XAUUSD --direction buy --units 1 \
  --balance 5000 --account demo \
  --risk_amount [pts×16] --reward_amount [pts×16] --sl_distance [pts]

# Forex
python3 enforcer.py --instrument GBPUSD --direction sell --lots 0.03 \
  --balance 5000 --account demo \
  --risk_amount [pips×5.46] --reward_amount [pips×5.46] --sl_distance [pips]

# Review logs
python3 session_logger.py summary
```

---

## STOP THE LOOP AT ANY TIME
- Type: `stop loop` → Claude cancels the active cron job
- Or press Esc in Claude Code
- Or let session time condition trigger automatically (12:00 or 18:00 SAST)

Stopping is always free. A bad trade is not.

---

## FILE STRUCTURE
```
trading-context/
├── CLAUDE.md                  ← auto-loaded on Claude Code startup
├── EVAN_TRADING_CONTEXT.md    ← the brain — v2.0, grows every session
├── enforcer.py                ← deterministic numeric gate
├── session_logger.py          ← tick logger → session_log.jsonl
├── LOOP_SETUP.md              ← this file
├── enforcer_audit.jsonl       ← every enforcer check (auto-written)
└── session_log.jsonl          ← every tick (auto-written)
```

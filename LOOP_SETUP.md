# LOOP SETUP — v3.2
Updated: June 24, 2026 | Account: Demo #41829612 | Goal: R5,088 → R10,000

---

## WHEN TO RUN WHICH LOOP

| Period | Session | What runs | Decision |
|---|---|---|---|
| 00:00-01:00 SAST | Off | Overnight monitor if positions open | Optional |
| 01:00-07:00 SAST | Asian | CHANGE 7 only — USDJPY/AUDUSD/NZDUSD/XAUUSD | Run (new v3.2) |
| 07:00-09:00 SAST | Pre-London | Scalp levels setup at 08:43 | 1-time setup |
| 09:00-15:00 SAST | London | CHANGE 7 + scalp integrated | Run |
| 15:00-18:00 SAST | London/NY | CHANGE 7 + scalp integrated | Run (BEST) |
| 18:00-22:00 SAST | NY | Position monitor only — no new trades | Run if open |
| 22:00-01:00 SAST | Off | Overnight monitor if positions open | Optional |

---

## LOOP ARCHITECTURE — OVERVIEW

```
22:00 → Overnight monitor (every 30 min, only if positions open) → stops 09:00
01:00 → Asian CHANGE 7 loop (5-min ticks) → stops 07:00
08:43 → Pre-session: fetch H1 candles → scalp_levels.py (1-time, NOT a loop)
09:02 → London: CHANGE 7 + scalp (5-min ticks) → stops 15:00
14:47 → London/NY: CHANGE 7 + scalp (5-min ticks) → stops 18:00
18:05 → NY monitor: position-only (5-min ticks) → stops 22:00
```

**Three parallel strategies per active session:**
1. **CHANGE 7** — run, big-run pullback-resumption, min 15pt (gold), TP=15pt, SL=6pt
2. **Scalp** — S/R level rejection, 5pt SL, 10pt TP, 20-min time stop (London/London-NY only)
3. **Position monitor** — Rule 4/13/14/Change3 on open trades (all ticks)

---

## PRE-SESSION SCALP SETUP (run once at 08:43 SAST — not a loop)

Type this prompt manually before starting the London loop:

```
Pre-session scalp setup. Steps:
1. switch_trading_account to #41829612
2. Get H1 candles (24 bars) for EURUSD, GBPUSD, XAUUSD, USDJPY via get_symbol_history (timeframeMinutes=60, limit=24)
3. Write scalp_candles_temp.json in this format:
   {"EURUSD": {"current_price": X, "candles": [{"time":"...","open":X,"high":X,"low":X,"close":X},...]},"GBPUSD":{...},"XAUUSD":{...},"USDJPY":{...}}
4. python scalp_levels.py --symbol EURUSD --symbol GBPUSD --symbol XAUUSD --symbol USDJPY
5. Read news_impact.json — confirm high_impact_2h is false
6. Print: "Scalp levels loaded. Key levels: [summarise each instrument's nearest level]"
```

---

## LOOP 1 — OVERNIGHT MONITOR (if positions open, 22:00-09:00 SAST)

Only run if `open_positions` is not empty. Use ScheduleWakeup every 1800s (30 min).

```
Overnight position monitor. Steps:
1. switch_trading_account to #41829612. Get SAST time (XAUUSD price). Get account_info. Get open_positions.
2. If no open positions: print "No open positions. Overnight monitor complete. No further checks needed." and STOP (do not ScheduleWakeup).
3. For each open position: get_symbol_history (timeframeMinutes=15, limit=10) + get_symbol_history (timeframeMinutes=240, limit=50). Output CHANGE 4 format:
   [HH:MM SAST] — OVERNIGHT
   INSTRUMENT: [symbol] [direction]
   TREND: H4 [Bull/Bear] — last swing at [price]
   M5 STRUCTURE: [trend/compression/reversal]
   P&L: R[amount] | [X]% to TP | Floor: R[locked]
   ACTION: [Hold / Trail to [price] per Rule X / Watch]
   NEXT TRIGGER: [specific price or event]
4. Apply rules automatically: Rule 14 (+R80 floating → SL to entry+5), Rule 4 (50%+ TP shrinking candles → close), Rule 13 (60%+ TP stalling at S/R → close), Change 3 (M5 reversed + neg P&L → Rule 5 cut flag).
5. python session_logger.py --tick [N] --sast_time "[HH:MM]" --session "off" --account_balance [balance] --open_positions "[symbol:dir:pnl]" --h4_trend "[symbol:direction]" --candidate_trades "none" --enforcer_result "na" --trade_placed "none" --action_taken "[what happened]" --notes "overnight monitor"
6. ScheduleWakeup delaySeconds=1800 prompt="Overnight position monitor. Steps: [paste this full prompt]"
```

---

## LOOP 2 — ASIAN SESSION (01:00-07:00 SAST — CHANGE 7 only)

Instruments: USDJPY, AUDUSD, NZDUSD, XAUUSD (Asian-active pairs only)
No scalp during Asian. Max 1 trade. CHANGE 7 H4 confirmation required.

```
/loop 5m You are running Asian session trading tick [auto-increment from 1]. Account: demo #41829612. Asian session: 01:00-07:00 SAST. USDJPY/AUDUSD/NZDUSD/XAUUSD only. CHANGE 7 strategy — no scalp. Max 1 trade total this session.

STEP 1 — TIME AND ACCOUNT:
switch_trading_account to #41829612. Get SAST time from XAUUSD price. Get account_info. Get open_positions.
If SAST time is before 01:00 or after 07:00: print "Outside Asian session — loop stop." Do not ScheduleWakeup.

STEP 2 — POSITION MONITOR (if open):
For each open position: get_symbol_history (timeframeMinutes=15, limit=10) + (timeframeMinutes=240, limit=50). Output CHANGE 4 format. Apply rules 4/13/14/Change3.

STEP 3 — CHANGE 7 SCAN (Asian instruments only):
For USDJPY, AUDUSD, NZDUSD, XAUUSD:
  a. get_symbol_history (timeframeMinutes=240, limit=50) → H4 direction gate (CHANGE 2: last 3 closes, need 2 consecutive in same direction)
  b. If H4 confirmed: get_symbol_history (timeframeMinutes=15, limit=50)
  c. python change7_scanner.py --symbol [X] --direction [long/short] --candles-file [temp file]
     (Write M15 bars to temp JSON first, then run scanner)
  d. Exit 0 = signal found. Exit 1 = no signal. Exit 2 = skip.

STEP 4 — ENFORCER (if signal and fewer than 1 trade placed this session):
python enforcer.py --instrument [X] --direction [buy/sell] --units [1 for gold / --lots 0.03 for forex] --balance [balance] --account demo --risk_amount [ZAR] --reward_amount [ZAR] --sl_distance [pts]
Exit 0 → create_market_order → modify_position (SL/TP). Exit 1 → BLOCKED, do not retry.

STEP 5 — LOG:
python session_logger.py --tick [N] --sast_time "[HH:MM]" --session "asian" --account_balance [balance] --open_positions "[pos or none]" --h4_trend "[trends]" --candidate_trades "[symbols or none]" --enforcer_result "[PASS|BLOCKED:reason|na]" --trade_placed "[symbol dir units|none]" --action_taken "[summary]" --notes "[notes]"

STOP CONDITIONS: 1 trade placed OR 2 consecutive losses OR R300 drawdown OR after 07:00 SAST OR 36 ticks.
```

---

## LOOP 3 — LONDON SESSION (09:00-15:00 SAST — CHANGE 7 + scalp)

Paste at 09:02 SAST (after scalp pre-session at 08:43).

```
/loop 5m You are running London session trading tick [auto-increment from 1]. Account: demo #41829612. London: 09:00-15:00 SAST. CHANGE 7 + scalp integrated. TICK MODE: Tick 1 or divisible by 12 → MASTER SCAN. Otherwise → MONITORING.

MASTER SCAN STEPS (tick 1, 13, 25...):
1. switch_trading_account #41829612. Get SAST time (XAUUSD price). Get account_info. Get open_positions.
2. news_scanner.py clear. web_search "breaking financial news today" + "war news today" + "Fed news today" + "economic events today" + "oil supply news today". Categorise into keys: war_escalation/peace_talks/ceasefire/missile_strike/sanctions_announced/cpi_hot/cpi_cool/nfp_beat/nfp_miss/fed_hawkish/fed_dovish/oil_supply_shock/tech_earnings_beat/tech_earnings_miss/defense_contract_win/ai_breakthrough/risk_off_generic/risk_on_generic/central_bank_rate_hike/inflation_data_uk_eu. Run: python3 news_scanner.py set --events "[keys]" --headlines "[headline1|headline2]" (add --high_impact_2h if scheduled high-impact within 2h). Run: python3 news_scanner.py read. If high_impact_2h: do NOT enter new trades this tick.
3. python3 master_scan.py clear. For XAUUSD/XAGUSD/BRENT/EURUSD/GBPUSD/USDJPY/USDCHF/AUDUSD (always): get H4 (timeframeMinutes=240, limit=50) → CHANGE 2 gate → if passes get H1 (timeframeMinutes=60, limit=12) → news_scanner.py check → score → master_scan.py add. Then NAS100/SPX500 (awareness, blocked <R8k). Then defense/tech/energy if relevant news active. Run: python3 master_scan.py read.
4. Position monitor: get last 10 M5 + 6 H4 per position → CHANGE 4 format → apply rules 4/13/14/Change3.
5. SCALP CHECK: python scalp_monitor.py --symbol EURUSD --price [current]. python scalp_monitor.py --symbol GBPUSD --price [current]. python scalp_monitor.py --symbol XAUUSD --price [current]. python scalp_monitor.py --symbol USDJPY --price [current]. If any status=AT_LEVEL: fetch 5 M5 candles → write scalp_m5_temp.json → re-run scalp_monitor.py. If status=TRIGGERED: go to scalp enforcer below.
6. SCALP ENFORCER (if triggered): python scalp_enforcer.py --symbol [X] --direction [long/short] --lots [0.03 forex / 1 gold] --balance [balance] --sl_distance_pips [dist] --tp_distance_pips [dist] --account demo. Exit 0 → create_market_order → modify_position (SL/TP). Exit 1 → BLOCKED.
7. python session_logger.py [all args].

MONITORING STEPS (ticks 2-12, 14-24...):
1. switch_trading_account #41829612. Get SAST time + account_info + open_positions.
2. Position monitor: get 10 M5 + 6 H4 per open position → CHANGE 4 → apply rules.
3. python3 master_scan.py read. For top 5 (score ≥6): get current price → if near entry get M15 (timeframeMinutes=15, limit=50) → check CHANGE 7 trigger (change7_scanner.py) or CHANGE 5 trigger.
4. CHANGE 7 ENFORCER (if trigger, <2 trades placed, no high_impact_2h): python enforcer.py [all args]. Exit 0 → order. Exit 1 → BLOCKED.
5. SCALP CHECK: scalp_monitor.py for EURUSD/GBPUSD/XAUUSD/USDJPY with current prices. If AT_LEVEL → M5 confirm → scalp_enforcer.py → order if PASS.
6. python session_logger.py [all args].

STOP CONDITIONS: 2 CHANGE 7 trades placed AND 3 scalp trades placed OR 2 consecutive losses (either system) OR R500 drawdown OR after 15:00 SAST OR 36 ticks.
SESSION END: get_close_positions → P&L → append EVAN_TRADING_CONTEXT.md → python session_review.py → python generate_dashboard.py → git add EVAN_TRADING_CONTEXT.md session_log.jsonl watchlist.json news_impact.json dashboard.html scalp_log.jsonl scalp_state.json && git commit -m "Session [date] [P&L] [N] trades" && git push.
```

---

## LOOP 4 — LONDON/NY OVERLAP (14:47 SAST — CHANGE 7 + scalp — BEST SESSION)

Same prompt as Loop 3 but change stop condition time to 18:00 SAST:

```
/loop 5m [same as Loop 3 above — change "15:00 SAST" to "18:00 SAST" in STOP CONDITIONS]
```

---

## LOOP 5 — NY SESSION MONITOR (18:05 SAST — positions only, no new trades)

Only run if you have open positions from London/NY session.

```
/loop 5m You are running NY session position monitor tick [auto-increment]. Account: demo #41829612. NY session: 18:00-22:00 SAST — MONITOR ONLY, no new entries.

STEP 1: switch_trading_account #41829612. Get SAST time. Get open_positions.
If no open positions: print "No open positions — NY monitor done." Stop (no ScheduleWakeup).
If SAST > 22:00: print "NY session ended — stopping." Stop.

STEP 2 — POSITION MONITOR:
For each position: get_symbol_history (timeframeMinutes=15, limit=10) + (timeframeMinutes=240, limit=50). Output CHANGE 4 format. Apply rules 4/13/14/Change3. DO NOT open new trades.

STEP 3 — LOG:
python session_logger.py [all args session="ny"].

STOP CONDITIONS: No open positions OR 22:00 SAST OR 36 ticks.
```

---

## SCALP SYSTEM — QUICK REFERENCE

**Instruments:** EURUSD ✓ | GBPUSD ✓ | USDJPY ✓ | AUDUSD ✓ | XAUUSD ✓ (high-confidence only)
**Never scalp:** GBPJPY | EURJPY | XAGUSD | NAS100 | SPX500 | US30

**Sizing:**
| Instrument | Lots | SL | Risk ZAR | TP | Reward ZAR | R:R |
|---|---|---|---|---|---|---|
| EURUSD | 0.03L | 5pip | R27 | 10pip | R55 | 2:1 |
| GBPUSD | 0.03L | 5pip | R35 | 10pip | R69 | 2:1 |
| USDJPY | 0.03L | 5pip | R17 | 10pip | R34 | 2:1 |
| XAUUSD | 1u | 5pt | R80 | 10pt | R160 | 2:1 |

**Scalp stop conditions:** 3 trades placed OR 2 consecutive losses OR R200 drawdown OR news high_impact_2h OR outside session hours

**Scalp SL rules:** NEVER on wick extremes — use closing price of M5 rejection candle ±buffer

---

## ASIAN SESSION — RATIONALE (new v3.2)

Added because: USDJPY and commodity pairs (AUDUSD, NZDUSD) are most active 01:00-07:00 SAST. Prior "zero profitable trades" finding was from the OLD system (pre-CHANGE 7). CHANGE 7 requires confirmed H4 structure — Asian ranging instruments are skipped automatically by the H4 gate. Only instruments with clean H4 trend pass through.

**Asian-specific rules:**
- Scalp loop does NOT run (S/R level rejection needs volatility — Asian is too choppy)
- XAUUSD scalp especially risky in Asian (tight range, spike risk on Middle East news)
- CHANGE 7 max 1 trade (conservative — test first before raising)
- Max drawdown R300 (tighter than London R500 — Asian has lower conviction setups)

---

## ENFORCER QUICK REFERENCE

```bash
# CHANGE 7 — Gold
python enforcer.py --instrument XAUUSD --direction buy --units 1 \
  --balance [bal] --account demo --risk_amount [sl_pts x 16] --reward_amount [tp_pts x 16] --sl_distance [pts] --change7

# CHANGE 7 — Forex 0.03L
python enforcer.py --instrument GBPUSD --direction sell --lots 0.03 \
  --balance [bal] --account demo --risk_amount [sl_pips x 5.46] --reward_amount [tp_pips x 5.46] --sl_distance [pips]

# Scalp — Gold
python scalp_enforcer.py --symbol XAUUSD --direction short --lots 1 \
  --balance [bal] --sl_distance_pips 5 --tp_distance_pips 10 --account demo

# Scalp — Forex
python scalp_enforcer.py --symbol EURUSD --direction short --lots 0.03 \
  --balance [bal] --sl_distance_pips 5 --tp_distance_pips 10 --account demo
```

---

## WEEKLY REVIEW (every Monday, paste before first session)

```
Run the weekly trading review. Read EVAN_TRADING_CONTEXT.md fully first.
Then read enforcer_audit.jsonl, scalp_enforcer_audit.jsonl, session_log.jsonl, scalp_log.jsonl — all entries since last Monday.

Produce:
1. ENFORCER AUDIT: Every BLOCKED trade — would it have won or lost?
2. LOSS ANALYSIS: Every loss — H4 trend at entry, which rule was violated, root cause.
3. WIN ANALYSIS: Every win — session, instrument, strategy (CHANGE 7 vs scalp), catalyst.
4. SCALP PERFORMANCE: Win rate, avg hold time, best/worst levels, time stop frequency.
5. NEWS ACCURACY: Were categorisations correct? Did direction match price reaction?
6. PATTERN SUMMARY: Repeating edges worth adding as a rule (min 3 occurrences).
7. PROGRESS: Current balance vs R5,088 start. % toward R10,000 goal.
8. PROPOSED RULE CHANGES: Specific diff to EVAN_TRADING_CONTEXT.md.

DO NOT commit. Print proposed diff and wait for Evan's approval.
DO NOT auto-approve changes to risk sizing, lot limits, or R:R thresholds.
```

---

## FILE STRUCTURE

```
tradeloop/
├── CLAUDE.md                     ← auto-loaded on Claude Code startup
├── EVAN_TRADING_CONTEXT.md       ← brain — rules, history, lessons
├── LOOP_SETUP.md                 ← this file — all loop commands
├── SCALP_SETUP.md                ← scalp loop reference
├── enforcer.py                   ← CHANGE 7 gate (exit 0/1)
├── scalp_enforcer.py             ← scalp gate (exit 0/1) ← NEW
├── scalp_levels.py               ← pre-session H1 level calculator ← NEW
├── scalp_monitor.py              ← per-tick S/R level watcher ← NEW
├── scalp_logger.py               ← scalp tick/trade logger ← NEW
├── change7_scanner.py            ← CHANGE 7 + BOUNCE signal detector
├── session_logger.py             ← main tick logger → session_log.jsonl
├── master_scan.py                ← hourly scan → watchlist.json
├── news_scanner.py               ← news → news_impact.json
├── tick_lock.py                  ← lock file manager (tick.lock / scalp.lock)
├── session_start_hook.py         ← auto-injects context at session open
├── session_review.py             ← post-session pattern extractor
├── generate_dashboard.py         ← live dashboard → dashboard.html
├── enforcer_audit.jsonl          ← every CHANGE 7 enforcer check
├── scalp_enforcer_audit.jsonl    ← every scalp enforcer check ← NEW
├── session_log.jsonl             ← every main tick
├── scalp_log.jsonl               ← every scalp tick and trade ← NEW
├── scalp_state.json              ← scalp loop state (levels, counters) ← NEW
├── scalp_candles_temp.json       ← H1 OHLCV input for scalp_levels.py ← NEW
├── watchlist.json                ← top-10 instruments this hour
├── news_impact.json              ← active news events
├── session_state.json            ← H4 trends, key levels, loop state
├── dashboard.html                ← open in browser for live view
└── knowledge/
    ├── RULES.md                  ← all rules + CHANGES quick reference
    ├── instruments/              ← per-instrument profiles
    ├── lessons/                  ← named lessons
    └── sessions/                 ← auto-written by session_review.py
```

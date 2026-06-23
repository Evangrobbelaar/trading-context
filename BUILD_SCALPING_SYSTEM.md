# BUILD SCALPING SYSTEM — CLAUDE CODE PROMPT
## Full Context + Spec for TradeLoop Scalping Module

---

## WHO YOU ARE BUILDING FOR

**Trader:** Evan Grobbelaar, Johannesburg, South Africa (SAST = UTC+2)
**Platform:** ThinkMarkets ThinkTrader, accessed via MCP server
**MCP tool prefix:** `mcp__claude_ai_claude__`
**Account:** Demo #41829612 (NEVER touch live #43019560)
**Base currency:** ZAR (South African Rand)
**Balance:** ~R4,835

---

## EXISTING SYSTEM — WHAT ALREADY EXISTS

There is already a swing trading loop running in `c:\Users\evang\OneDrive\Desktop\tradeloop\`. Do NOT modify any existing files. The scalping system is a PARALLEL, SEPARATE module.

### Existing files (do not touch):
```
tradeloop/
├── CLAUDE.md                  ← swing loop rules
├── EVAN_TRADING_CONTEXT.md    ← trading brain/history
├── enforcer.py                ← swing trade gate (exit 0/1)
├── session_logger.py          ← swing tick logger
├── master_scan.py             ← swing watchlist manager
├── news_scanner.py            ← news events tracker
├── tick_lock.py               ← lock file (prevent tick overlap)
├── session_state.json         ← swing loop state cache
├── session_log.jsonl          ← swing tick log
├── watchlist.json             ← swing watchlist
├── news_impact.json           ← active news events
├── enforcer_audit.jsonl       ← swing enforcer audit
```

### Existing MCP tools available:
- `mcp__claude_ai_claude__switch_trading_account` — switch account
- `mcp__claude_ai_claude__get_account_info` — balance, equity, margin
- `mcp__claude_ai_claude__get_open_positions` — list open trades
- `mcp__claude_ai_claude__get_symbol_price` — current bid/ask
- `mcp__claude_ai_claude__get_symbol_history` — OHLCV candles (M1/M5/M15/H1/H4/D1)
- `mcp__claude_ai_claude__create_market_order` — place trade
- `mcp__claude_ai_claude__modify_position` — modify SL/TP
- `mcp__claude_ai_claude__close_position` — close trade
- `mcp__claude_ai_claude__get_close_positions` — closed trade history

### create_market_order syntax (CRITICAL):
```python
# Gold (XAUUSD):
{"symbol": "XAUUSD", "side": "Buy" or "Sell", "amount": 1}
# Forex:
{"symbol": "EURUSD", "side": "Buy" or "Sell", "lots": 0.01}
```

---

## TRADING HISTORY & LESSONS LEARNED (read this carefully)

### Session on June 23, 2026 — full history:
**Early session wins:**
- XAUUSD short +R90.78 ✅
- AUDUSD short +R63.88 ✅
- BRENT short +R48.08 ✅
- GBPUSD long -R83.63 ❌

**Afternoon session losses (the ones that hurt):**
- XAUUSD short -R80.94 (Rule 5 cut — M5 reversed)
- AUDUSD short -R27.21 (Rule 5 cut — M5 reversed)
- XAUUSD short -R175.36 (SL hit at 4120.27 after premature tightening)

**Net day: -R128.78**

### Root cause of losses:
1. XAUUSD was in a 17-point range (4105-4122) all afternoon. We shorted 3 times at the same level. Each short was technically valid per H4 rules but the market was ranging, not trending.
2. SL was tightened using a spike bar's LOW as the reference — wrong. Always use CLOSING price lows for SL reference, not wick extremes.
3. Re-entered the same setup after 2 Rule 5 cuts on the same instrument same session — this was the biggest mistake.

### Key rule changes made after losses:
- Never re-enter same instrument/direction after 2 Rule 5 cuts in the same session
- Do NOT tighten SL based on spike wicks — only use candle CLOSE prices
- Fresh H4 scan required at start of every active session (stale H4 = wrong bias)
- If same price level has rejected you twice, skip that instrument for the session
- Identify ranging vs trending BEFORE entry (two bounces from same range = skip)

---

## THE SCALPING SYSTEM — WHAT TO BUILD

### Core Philosophy
The swing system uses H4 confirmation and targets 40-80pt moves over 2-8 hours.
The scalping system uses H1 structure and targets 8-15pt moves over 5-30 minutes.
They run SIMULTANEOUSLY during London/NY overlap (15:00-18:00 SAST).
They are completely independent — separate state, separate logs, separate enforcer.

### Scalping Approach
- Pre-session: identify key intraday S/R levels from H1 chart
- During session: watch for price to reach a level, confirm with M1/M5 structure, enter
- Target: quick rejection off level, 8-15pts Gold / 6-10 pips forex
- Stop: tight, 4-6pts Gold / 4-5 pips forex
- Time stop: close trade if not at target within 20 minutes
- Max 3 scalp trades per session
- Stop after 2 consecutive losses

---

## FILES TO BUILD

### 1. `scalp_levels.py` — Pre-session level calculator
**Purpose:** Run once before session starts (08:45 SAST). Reads H1 candles, identifies key S/R levels for the day, writes to `scalp_state.json`.

**CLI usage:**
```bash
python scalp_levels.py --symbol EURUSD --symbol XAUUSD --symbol GBPUSD
```

**Logic:**
- Fetch last 24 H1 candles for each symbol
- Identify: yesterday's high, yesterday's low, overnight high, overnight low, key round numbers
- For each level: classify as resistance (above price) or support (below price)
- Calculate: distance from current price, strength (how many times level was tested)
- Output: JSON of top 3 levels per instrument with direction (long off support, short off resistance)
- Only keep levels within 30pts of current price (Gold) or 30 pips (forex) — scalp entries must be reachable

**Output format in scalp_state.json:**
```json
{
  "updated_sast": "08:52",
  "instruments": {
    "EURUSD": {
      "current_price": 1.13816,
      "h1_trend": "bear",
      "levels": [
        {
          "price": 1.14050,
          "type": "resistance",
          "direction": "short",
          "strength": 3,
          "distance_pips": 23,
          "sl": 1.14120,
          "tp": 1.13850,
          "rr": 2.5,
          "status": "watching"
        }
      ]
    }
  },
  "scalp_trades_today": 0,
  "consecutive_losses": 0,
  "session_pnl_zar": 0,
  "loop_active": false,
  "loop_stopped": false,
  "stop_reason": null
}
```

---

### 2. `scalp_enforcer.py` — Scalp-specific trade gate
**Purpose:** Validates every scalp trade before execution. Different rules from the swing enforcer.

**CLI usage:**
```bash
python scalp_enforcer.py \
  --symbol EURUSD \
  --direction short \
  --lots 0.01 \
  --balance 4835.12 \
  --sl_distance_pips 5 \
  --tp_distance_pips 10 \
  --account demo
```

**Rules (exit code 1 = BLOCKED, exit code 0 = PASS):**
- Balance below R3,000 → BLOCKED (protect capital floor)
- sl_distance < 3 pips/pts → BLOCKED (SL too tight, spread kills it)
- sl_distance > 10 pips/pts → BLOCKED (too wide for scalp — use swing system instead)
- tp_distance < sl_distance × 1.5 → BLOCKED (minimum 1.5:1 R:R on scalps)
- scalp_trades_today >= 3 → BLOCKED (max 3 scalps per session)
- consecutive_losses >= 2 → BLOCKED (stop after 2 losses)
- session_pnl_zar < -200 → BLOCKED (session drawdown limit R200)
- spread > 50% of sl_distance → BLOCKED (spread eating too much)
- NOT during London or London/NY session → BLOCKED (scalp session times only)

**ZAR risk calculation:**
- EURUSD 0.01L: 1 pip = R1.82 ZAR
- GBPUSD 0.01L: 1 pip = R2.30 ZAR  
- USDJPY 0.01L: 1 pip = ~R1.12 ZAR
- AUDUSD 0.01L: 1 pip = R1.82 ZAR
- XAUUSD 1 unit: 1 pt = R16 ZAR (too expensive for scalp lots — use 0.1 unit if available, else skip)
- EURUSD 0.03L: 1 pip = R5.46 ZAR (standard forex lot)

**Print on PASS:**
```
SCALP ENFORCER: PASS
Symbol: EURUSD | Direction: short | Lots: 0.01
SL: 5 pips = R9.10 risk | TP: 10 pips = R18.20 reward
R:R: 2.0:1 | Session trades: 1/3 | Consecutive losses: 0
```

**Print on BLOCKED:**
```
SCALP ENFORCER: BLOCKED — [specific reason]
```

Write every check to `scalp_enforcer_audit.jsonl`.

---

### 3. `scalp_logger.py` — Tick and trade logger
**Purpose:** Log every scalp tick and every trade result.

**CLI usage:**
```bash
# Log a tick:
python scalp_logger.py tick \
  --tick_num 5 \
  --sast_time "15:23" \
  --symbol_checked "EURUSD,XAUUSD" \
  --level_triggered "EURUSD:1.14050:short" \
  --enforcer_result "PASS" \
  --trade_placed "EURUSD short 0.01L" \
  --notes "clean rejection off 1.14050 resistance"

# Log a trade result:
python scalp_logger.py trade \
  --symbol EURUSD \
  --direction short \
  --entry 1.14048 \
  --exit 1.13855 \
  --pnl_zar 35.20 \
  --exit_reason "TP hit" \
  --duration_minutes 14
```

**Output:** Append to `scalp_log.jsonl` (separate from swing `session_log.jsonl`).

---

### 4. `scalp_monitor.py` — Real-time level watcher
**Purpose:** The core of the scalp loop. Run every tick to check if price is near a key level and M1/M5 structure confirms entry.

**CLI usage:**
```bash
python scalp_monitor.py --symbol EURUSD
```

**Logic:**
1. Read `scalp_state.json` for key levels on this symbol
2. Get current price
3. For each watching level:
   - Is price within 3 pips (forex) or 3 pts (Gold) of the level? → NEAR
   - Is price within 1 pip of the level? → AT LEVEL
4. Output: JSON with trigger status

```json
{
  "symbol": "EURUSD",
  "current_price": 1.14047,
  "nearest_level": 1.14050,
  "distance_pips": 0.3,
  "status": "AT_LEVEL",
  "direction": "short",
  "sl": 1.14120,
  "tp": 1.13850
}
```

**Status values:**
- `WATCHING` — price not near level (>5 pips away)
- `NEAR` — price within 3-5 pips of level
- `AT_LEVEL` — price within 1-3 pips of level → trigger M1/M5 check
- `TRIGGERED` — M1/M5 confirmed structure → ready for enforcer
- `PASSED` — level already triggered this session (don't re-trigger same level twice)
- `INVALIDATED` — price broke through level without bouncing

**M1/M5 confirmation (only runs when AT_LEVEL):**
- Fetch last 5 M5 candles
- For SHORT: last M5 candle must close BELOW the level after touching it (rejection candle)
- For LONG: last M5 candle must close ABOVE the level after touching it
- Rejection candle = close is at least 60% of the candle range from the wick extreme
- If confirmed → status = TRIGGERED

---

### 5. `scalp_state.json` — Scalp loop state (auto-generated)
Created by `scalp_levels.py`, updated throughout the session by the loop.

---

### 6. `scalp_enforcer_audit.jsonl` — Enforcer audit log
Auto-created by `scalp_enforcer.py`.

---

### 7. `scalp_log.jsonl` — Scalp tick and trade log
Auto-created by `scalp_logger.py`.

---

## THE SCALP LOOP — HOW IT RUNS

The scalp loop is triggered by Claude Code's `/loop` command, running every 60 seconds (1-minute ticks). It is started manually at session start by Evan typing "start scalp loop".

### Scalp tick protocol (every 60 seconds):

```
SCALP TICK [N] | [HH:MM SAST]

STEP 0 — LOCK:
  python tick_lock.py acquire --lock-file scalp.lock
  If exit 1: "SCALP TICK SKIPPED — lock active" → stop.

STEP 1 — TIME + ACCOUNT:
  - Get SAST time
  - Confirm account #41829612
  - Check session: only run during London (09:00-12:00) or London/NY (15:00-18:00)
  - Outside session window → "Scalp loop paused — outside session" → release lock → stop

STEP 2 — STATE CHECK:
  - Read scalp_state.json
  - If loop_stopped = true → "Scalp loop stopped: [reason]" → release lock → stop
  - If scalp_trades_today >= 3 → stop
  - If consecutive_losses >= 2 → stop

STEP 3 — LEVEL WATCH (parallel):
  For each instrument in scalp_state.json:
    python scalp_monitor.py --symbol [X]
  
  Any instrument showing AT_LEVEL or TRIGGERED? → go to STEP 4
  All WATCHING? → log brief tick, release lock, schedule next tick

STEP 4 — M1/M5 CONFIRMATION (only if AT_LEVEL):
  Fetch 5 M5 candles for triggered instrument
  Check rejection candle criteria
  If confirmed → TRIGGERED → go to STEP 5
  If not confirmed → "Level touched, no rejection yet" → release lock → schedule next tick

STEP 5 — ENFORCER:
  python scalp_enforcer.py --symbol [X] --direction [X] --lots [X] ...
  Exit 0 → STEP 6 (place trade)
  Exit 1 → log blocked reason, release lock, schedule next tick

STEP 6 — PLACE TRADE:
  mcp__claude_ai_claude__create_market_order
  Immediately set SL and TP via mcp__claude_ai_claude__modify_position
  Update scalp_state.json: scalp_trades_today += 1, mark level as PASSED
  Log via: python scalp_logger.py tick [...]

STEP 7 — TRADE MONITOR (if in scalp trade):
  Get current position P&L
  Check time in trade — if > 20 minutes AND not at TP → TIME STOP → close position
  Check M1 — if M1 reverses hard against position → close immediately (scalp Rule 5)
  Log result via: python scalp_logger.py trade [...]

STEP 8 — RELEASE LOCK:
  python tick_lock.py release --lock-file scalp.lock

STEP 9 — SCHEDULE NEXT TICK:
  ScheduleWakeup delaySeconds=60
```

---

## IMPORTANT TECHNICAL NOTES

### Separate lock file
The scalp loop uses `scalp.lock` NOT `tick.lock`. The swing loop uses `tick.lock`. They must not interfere with each other.

Modify `tick_lock.py` to accept an optional `--lock-file` argument:
```bash
python tick_lock.py acquire --lock-file scalp.lock
python tick_lock.py release --lock-file scalp.lock
```
Default (no argument) = `tick.lock` (keeps existing swing loop working).

### Lot sizing
These are the verified sizes for this account:
- Forex scalp: 0.01 lots (cheapest, lowest risk per pip)
- Forex standard: 0.03 lots (current swing size)
- Gold: 1 unit = R16/pt (expensive for scalping — only scalp Gold at very high confidence setups)
- Consider: Gold 0.1 units if ThinkTrader supports fractional units. Check with `mcp__claude_ai_claude__get_symbol_info` before placing.

### Best scalp instruments (ranked by suitability):
1. **EURUSD** — tightest spread (~0.9 pip), most predictable, best for scalping
2. **GBPUSD** — slightly wider spread but bigger moves, good for 08-12 pip targets
3. **USDJPY** — tight spread, excellent around round numbers (e.g. 161.000, 161.500)
4. **AUDUSD** — good, correlated with risk sentiment (fed_hawkish = AUDUSD bear = short scalps)
5. **XAUUSD** — cheap spread (0.19pt!) but volatile — only scalp at very clear S/R with news aligned

### Do NOT scalp:
- GBPJPY, EURJPY (too wide spread, too unpredictable)
- During high-impact news events (read news_impact.json — if high_impact_2h = true, skip)
- XAGUSD (spread:target ratio too wide for scalp)
- Indices NAS100/SPX500/US30 (balance < R8,000 blocks these)

### News integration
Read `news_impact.json` at session start. If `high_impact_2h = true` → pause scalp loop until M15 settles after the print. This is the same rule as the swing system.

### Correlation rule
Do NOT have two scalp trades open simultaneously in correlated pairs:
- EURUSD + GBPUSD = correlated (both vs USD) → only one open at a time
- AUDUSD + NZDUSD = correlated → only one at a time
- XAUUSD is uncorrelated to forex → can run alongside one forex scalp

---

## ZAR RISK TARGETS PER SCALP TRADE

| Instrument | Lots | Stop | Risk ZAR | Target | Reward ZAR | R:R |
|---|---|---|---|---|---|---|
| EURUSD | 0.01 | 5 pips | R9 | 10 pips | R18 | 2.0:1 |
| EURUSD | 0.03 | 5 pips | R27 | 10 pips | R55 | 2.0:1 |
| GBPUSD | 0.01 | 5 pips | R12 | 10 pips | R23 | 2.0:1 |
| GBPUSD | 0.03 | 5 pips | R36 | 10 pips | R68 | 2.0:1 |
| USDJPY | 0.01 | 5 pips | R6 | 10 pips | R11 | 2.0:1 |
| USDJPY | 0.03 | 5 pips | R17 | 10 pips | R34 | 2.0:1 |
| XAUUSD | 1 unit | 5 pts | R80 | 10 pts | R160 | 2.0:1 |

Default scalp lot size: **0.03L** for forex, **1 unit** for XAUUSD (only at high-confidence levels).

---

## SESSION STOP CONDITIONS (scalp-specific)

Stop the scalp loop immediately if ANY:
1. 2 consecutive losing scalps this session
2. 3 scalp trades placed this session (quality > quantity)
3. Session drawdown > R200 from session-start balance
4. Time outside London or London/NY session
5. high_impact_2h = true in news_impact.json
6. Evan types "stop scalp" or "stop loop"

---

## OUTPUT FORMAT PER TICK

### Quiet tick (no level near):
```
SCALP TICK 5 | 15:23 SAST | EURUSD: 1.13791 | GBPUSD: 1.31962 | XAUUSD: 4121.70
All levels: WATCHING. Next check in 60s.
```

### Level approaching:
```
SCALP TICK 6 | 15:24 SAST
⚠ EURUSD NEAR LEVEL — 1.14050 resistance (2.3 pips away)
Watching for rejection. M5 check will trigger at ≤1 pip.
```

### Trade triggered:
```
SCALP TICK 7 | 15:25 SAST
🎯 EURUSD AT LEVEL — 1.14050 resistance
M5 CONFIRMATION: bearish rejection candle (close 1.14031, wick to 1.14055) ✅
ENFORCER: PASS — R27 risk, R55 reward, 2.0:1 R:R
ORDER PLACED: SELL EURUSD 0.03L @ 1.14031 | SL: 1.14120 | TP: 1.13830
```

### In-trade monitor:
```
SCALP TICK 8 | 15:26 SAST
EURUSD SHORT | Entry: 1.14031 | Now: 1.13960 | P&L: +R38.60 (70% to TP)
Time in trade: 1 min | Time stop: 19 min remaining
M1: continuing lower ✅ | Action: HOLD
```

### Time stop:
```
SCALP TICK 28 | 15:45 SAST
EURUSD SHORT | Entry: 1.14031 | Now: 1.14010 | P&L: +R11.50
⏱ TIME STOP — 20 minutes reached, TP not hit
CLOSING position — Result: +R11.50
```

---

## WHAT TO BUILD — CHECKLIST

Build these files in order:

- [ ] `tick_lock.py` — UPDATE existing file to accept `--lock-file` argument (default: `tick.lock`)
- [ ] `scalp_levels.py` — H1 level calculator, writes scalp_state.json
- [ ] `scalp_enforcer.py` — scalp-specific trade gate, writes scalp_enforcer_audit.jsonl
- [ ] `scalp_monitor.py` — price level watcher, M1/M5 rejection checker
- [ ] `scalp_logger.py` — tick and trade logger, writes scalp_log.jsonl
- [ ] `SCALP_SETUP.md` — quick reference: how to start the scalp loop each morning

### DO NOT build:
- Do not modify CLAUDE.md
- Do not modify enforcer.py (swing enforcer — separate)
- Do not modify session_logger.py
- Do not modify master_scan.py or news_scanner.py
- Do not modify session_state.json

---

## TESTING BEFORE GOING LIVE

After building, test each script in isolation:

```bash
# Test level calculator:
python scalp_levels.py --symbol EURUSD --symbol XAUUSD

# Test enforcer PASS case:
python scalp_enforcer.py --symbol EURUSD --direction short --lots 0.03 \
  --balance 4835 --sl_distance_pips 5 --tp_distance_pips 10 --account demo

# Test enforcer BLOCKED case (SL too tight):
python scalp_enforcer.py --symbol EURUSD --direction short --lots 0.03 \
  --balance 4835 --sl_distance_pips 2 --tp_distance_pips 5 --account demo

# Test monitor (WATCHING):
python scalp_monitor.py --symbol EURUSD

# Test logger:
python scalp_logger.py tick --tick_num 1 --sast_time "09:05" \
  --symbol_checked "EURUSD" --level_triggered "none" \
  --enforcer_result "na" --trade_placed "none" --notes "test"
```

All scripts must exit cleanly with no errors before the loop goes live.

---

## STARTING THE SCALP LOOP (after build complete)

Evan types: **"start scalp loop"**

Claude Code then:
1. Runs `python scalp_levels.py --symbol EURUSD --symbol GBPUSD --symbol XAUUSD --symbol USDJPY`
2. Reads scalp_state.json — confirms levels loaded
3. Reads news_impact.json — confirms no high_impact_2h block
4. Starts 60-second loop via `/loop 1m [scalp tick protocol]`
5. Reports: "Scalp loop started. [N] levels loaded across [M] instruments. First tick in 60s."

---

## FINAL NOTE

This scalping system is designed to complement the swing system, not replace it.

- Swing system: 1-2 trades per session, 40-80pt targets, H4 confirmation, 2-6 hour hold
- Scalp system: 1-3 trades per session, 8-15pt targets, H1 level + M5 rejection, 5-20 min hold

They can run simultaneously. A swing position in XAUUSD SHORT does NOT block a scalp LONG in EURUSD — they are on different instruments and different timeframes.

The goal: swing system builds the big R, scalp system adds consistent small R on top.
On a good day: 1 swing trade (+R300) + 2 scalp trades (+R60) = R360 session.

# TRADING SESSION — CLAUDE CODE BOOTSTRAP
Version: 2.1 | Updated: June 22, 2026
Goal: R5,000 → R10,000 on demo #41829612

## MANDATORY FIRST ACTION
Read `EVAN_TRADING_CONTEXT.md` fully before any other output.
Then respond ONLY with:
"Context loaded v[X.X] — [SAST time] — [session] — [N] open positions — ready."

---

## ACCOUNTS
| Account | Type | Balance | Status |
|---|---|---|---|
| #41829612 | DEMO ZAR | R5,000 | **PRIMARY — use this** |
| #41810679 | DEMO ZAR | R66 | Retired |
| #43019560 | LIVE ZAR | ~R65 | Never touch without explicit instruction |

**Default account every session: demo #41829612**
Switch command at session start: `claude:switch_trading_account` → `41829612`
Never touch live #43019560 unless Evan says "use live account" explicitly this session.

---

## MCP CONNECTION
- Tool prefix: `mcp__claude_ai_claude__` (ThinkTrader MCP)
- MCP drops after inactivity — use ToolSearch to reload tools if calls fail
- Always switch to #41829612 at session start before any other call

---

## MASTER RULE
Make money and stay profitable. R5,000 → R10,000 is the goal.
Every decision is judged against this. Patience beats overtrading every time.
A blocked trade that would have lost = WIN. A skipped checklist = SYSTEM FAILURE.

---

## ACTIVE TRADING SESSIONS (loop only runs during these)
| Session | SAST | Best instruments |
|---|---|---|
| London open | 09:00–12:00 | GBPUSD, EURUSD, XAUUSD |
| London/NY overlap | 15:00–18:00 | XAUUSD, GBPUSD, EURUSD ← BEST |

Do NOT place trades during: Asian (00:00–07:00), quiet (12:00–15:00), NY-only (18:00–22:00 unless already in a trade), weekends.

---

## TICK PROTOCOL (runs every loop iteration)

### STEP 1 — TIME & ACCOUNT (every tick, no exceptions)
1. `mcp__claude_ai_claude__get_symbol_price` on XAUUSD → determine SAST time from UTC timestamp
2. `mcp__claude_ai_claude__get_account_info` → confirm balance is R5,000-range, account #41829612
3. `mcp__claude_ai_claude__get_open_positions` → list open positions and floating P&L
4. Confirm session (London 09:00-12:00 or London/NY 15:00-18:00). If neither → log tick as off-session and skip to Step 5.

### STEP 2 — OPEN POSITION MONITOR (if any positions open)
For each open position:
- `mcp__claude_ai_claude__get_symbol_history` → last 10 M5 candles
- `mcp__claude_ai_claude__get_symbol_history` → last 6 H4 candles
- Output mandatory CHANGE 4 format:

```
[HH:MM SAST] — [SESSION]
INSTRUMENT: [symbol] [direction]
TREND: H4 [Bull/Bear] — swing sequence: [H/L1] → [H/L2] → [H/L3]
M5 STRUCTURE: [Higher highs / Lower highs / Compression] since entry
P&L: R[amount] | [X]% to TP | Floor: R[locked if SL trailed]
ACTION: [Hold / Trail to [price] per Rule X / Close — Rule 13 / Watch]
NEXT TRIGGER: [specific price or event that changes the action]
```

Apply rules automatically:
- Rule 4: 50% TP + shrinking candles → close
- Rule 13: 60%+ TP + stalling at S/R → close, bank profit
- Rule 14: Gold +R80 floating → SL to entry+5, plan TP1 at 60%
- Change 3: M5 reversed + positive P&L → flag Rule 13
- Change 3: M5 reversed + negative P&L → flag Rule 5 cut

### STEP 3 — MARKET SCAN (only if <2 trades open and session is active)
Max 2 trades open simultaneously. If 2 already open, skip Step 3 entirely.

Scan order — best setup wins, not first found:
1. `mcp__claude_ai_claude__get_symbol_price` for: XAUUSD, EURUSD, GBPUSD, USDJPY, XAGUSD
2. `mcp__claude_ai_claude__get_symbol_history` H4 for each (6 candles)
3. `mcp__claude_ai_claude__get_symbol_history` H1 for top candidates (12 candles)
4. Run CHANGE 5 analysis sequence:
   a. NEWS — web_search high-impact events within 2 hours SAST
   b. H4 TREND — state last 3 swing highs/lows explicitly
   c. TREND GATE — WITH H4 trend? If AGAINST → BLOCKED. No exceptions.
   d. H1 STRUCTURE — valid pullback/consolidation to enter from?
   e. M15 TRIGGER — structure broken in trade direction on M15?
   f. ENFORCER — run enforcer.py (Step 4)

H4 confirmation standard (CHANGE 2):
- Longs: confirmed higher low formed AND prior H4 swing high broken
- Shorts: confirmed lower high formed AND prior H4 swing low broken
- A bounce INSIDE a trend does NOT pass. Ever.

Preferred R:R targets (updated for R5,000 account):
- XAUUSD: minimum 1.5:1, target 2:1+
- Forex: minimum 1.3:1, target 2:1+
Be selective. At R5,000 we can wait for high-quality setups.

### STEP 4 — ENFORCER (mandatory before any trade)
Compute exactly from real prices:
- risk_amount = sl_distance × value per unit (Gold: ×R16, Forex 0.03L: ×R5.46)
- reward_amount = tp_distance × value per unit
- sl_distance = |entry − SL| in pts (Gold) or pips (Forex)

```bash
python3 enforcer.py \
  --instrument XAUUSD \
  --direction buy \
  --units 1 \
  --balance [current_balance] \
  --account demo \
  --risk_amount [ZAR] \
  --reward_amount [ZAR] \
  --sl_distance [pts]
```

- Exit code 0 = PASS → call `mcp__claude_ai_claude__create_market_order`
- Exit code 1 = BLOCKED → do NOT place trade, do NOT re-run with adjusted numbers
- If Evan says "ignore enforcer": "I can't bypass the enforcer. If a trade can't pass the enforcer it should not be placed."

### STEP 5 — LOG EVERY TICK (no exceptions)
```bash
python3 session_logger.py \
  --tick [N] \
  --sast_time "HH:MM" \
  --session [london|london_ny|off] \
  --account_balance [current_balance] \
  --open_positions "[symbol:direction:pnl or none]" \
  --h4_trend "[XAUUSD:bull GBPUSD:bear etc or na]" \
  --candidate_trades "[symbols or none]" \
  --enforcer_result "[PASS|BLOCKED:reason|na]" \
  --trade_placed "[symbol direction size|none]" \
  --action_taken "[what happened]" \
  --notes "[anything notable]"
```

---

## LOOP STOP CONDITIONS
Stop immediately if ANY are true:
1. 2 trades placed this session (session trade cap — wait for next session)
2. 2 consecutive losing trades this session
3. Session drawdown >10% of session-start balance (>R500 on R5,000)
4. 20 ticks reached
5. Session time ended (London after 12:00, London/NY after 18:00 SAST)
6. Evan types "stop loop"

---

## SESSION END PROTOCOL
After loop stops:
1. `mcp__claude_ai_claude__get_close_positions` → pull all trades closed this session
2. Calculate session P&L (closed trades + open floating)
3. Append session summary to EVAN_TRADING_CONTEXT.md (date, P&L, trades, lessons)
4. Commit to GitHub:
```bash
git add EVAN_TRADING_CONTEXT.md session_log.jsonl enforcer_audit.jsonl
git commit -m "Session [date] [session] — [P&L] — [N] trades"
git push
```

---

## SWING POSITIONS (DO NOT CLOSE WITHOUT PROTOCOL)
Any position tagged [SWING] in EVAN_TRADING_CONTEXT.md is locked.
If you see a [SWING] open: say "SWING position detected — read lock protocol before closing."
Only close after: Evan says "close the swing" → Claude reads lock protocol → Evan confirms.

---

## LEARNING MECHANISM
Model weights don't change. The WRITTEN RULESET improves.
Every session → session_log.jsonl grows
Every Monday → weekly review reads logs, proposes rule diffs
Every significant loss → immediate root cause added to EVAN_TRADING_CONTEXT.md
Rules 1-14, H4 trend gate, enforcer — all born from this process.

# TRADING SESSION — CLAUDE CODE BOOTSTRAP
Version: 2.0 | Updated: June 22, 2026

## MANDATORY FIRST ACTION
Read `EVAN_TRADING_CONTEXT.md` fully before any other output.
Then respond ONLY with:
"Context loaded v[X.X] — [SAST time] — [session] — [N] open positions — ready."

If you skipped this and the user sees no confirmation phrase: stop, read the file, output the phrase.

---

## MCP CONNECTION
- Tool prefix: `claude:` (ThinkTrader MCP at mcp.thinktrader.com/v1/mcp)
- MCP drops after inactivity — reconnect with `claude:reconnect_connection` if tools fail
- At session start: `claude:switch_trading_account` → default demo #41810679
- Never touch live #43019560 unless Evan explicitly says "use live account" this session

---

## MASTER RULE
Make money and stay profitable. Every decision is judged against this.
A blocked trade that would have lost is a WIN for the system.
A skipped checklist item that causes a loss is a SYSTEM FAILURE.

---

## TICK PROTOCOL (runs every loop iteration)

### STEP 1 — TIME & ACCOUNT (required every tick)
1. Get SAST time from `claude:get_symbol_price` on any instrument — NEVER ask Evan
2. `claude:get_account_info` — confirm balance, account number
3. `claude:get_open_positions` — list open positions and floating P&L
4. Determine session: Asian (00:00-07:00), London (09:00-12:00), London/NY (15:00-18:00), NY (18:00-22:00)

### STEP 2 — OPEN POSITION MONITOR (if any positions open)
For each open position:
- `claude:get_symbol_history` — last 10 M5 candles
- `claude:get_symbol_history` — last 6 H4 candles (for trend gate)
- Output mandatory CHANGE 4 format:

```
[HH:MM SAST] — [SESSION]
INSTRUMENT: [symbol] [direction]
TREND: H4 [Bull/Bear] — last swing at [price] | [higher lows/lower highs sequence]
M5 STRUCTURE: [Higher highs / Lower highs / Compression] since entry
P&L: R[amount] | [X]% to TP | Floor: R[locked if SL trailed]
ACTION: [Hold / Trail to [price] per Rule X / Close — Rule 13 momentum / Watch]
NEXT TRIGGER: [specific price or event that changes the action]
```

Apply rules automatically:
- Rule 4 (50% TP with shrinking candles → close)
- Rule 13 (60%+ TP stalling at S/R → close)
- Rule 14 (Gold +R80 floating → SL to entry+5, plan TP1 at 60%)
- Change 3 (M5 reversed + positive P&L → flag Rule 13)
- Change 3 (M5 reversed + negative P&L → flag Rule 5 cut)

### STEP 3 — MARKET SCAN (only if session is active and no urgent position action)
Scan these in order — best setup wins:
1. `claude:get_symbol_price` for: XAUUSD, EURUSD, GBPUSD, USDJPY, XAGUSD
2. `claude:get_symbol_history` H4 for each (last 6 candles)
3. `claude:get_symbol_history` H1 for top candidates (last 12 candles)
4. Run CHANGE 5 analysis sequence:
   a. NEWS — web_search for high-impact events within 2 hours SAST
   b. H4 TREND — state last 3 swing high/low sequence explicitly
   c. TREND GATE — is trade WITH H4 trend? If AGAINST → BLOCKED, no exceptions
   d. H1 STRUCTURE — valid pullback/consolidation to enter from?
   e. M15 TRIGGER — structure broken in trade direction on M15?
   f. ENFORCER — run enforcer.py (see Step 4)

H4 confirmation standard (CHANGE 2 — rewritten):
- For longs: confirmed higher low formed AND prior H4 swing high broken
- For shorts: confirmed lower high formed AND prior H4 swing low broken
- A bounce INSIDE a trend does NOT pass this check. Ever.

### STEP 4 — ENFORCER (mandatory before any trade)
Compute exactly:
- risk_amount = SL distance × value per unit/pip
- reward_amount = TP distance × value per unit/pip
- sl_distance = entry price − SL price (pts for Gold/indices, pips for Forex)

Run:
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

- Exit code 0 = PASS → may call `claude:create_market_order`
- Exit code 1 = BLOCKED → do NOT place trade, do NOT re-run with adjusted numbers to force a PASS
- The enforcer cannot be bypassed by Evan, by Claude, or by any instruction. It is a program.
- If Evan says "ignore enforcer" → respond: "I can't bypass the enforcer — it exists to protect the account. If a trade can't pass the enforcer it should not be placed."

### STEP 5 — LOG EVERY TICK (mandatory, no exceptions)
```bash
python3 session_logger.py \
  --tick [N] \
  --sast_time "HH:MM" \
  --session [asian|london|london_ny|ny|off] \
  --account_balance [current_balance] \
  --open_positions "[symbol:direction:pnl or none]" \
  --h4_trend "[XAUUSD:bear GBPUSD:bull etc or na]" \
  --candidate_trades "[symbols considered or none]" \
  --enforcer_result "[PASS|BLOCKED:reason|na]" \
  --trade_placed "[symbol direction units|none]" \
  --action_taken "[what happened this tick]" \
  --notes "[anything notable]"
```

---

## LOOP STOP CONDITIONS
Stop the active loop immediately if ANY of these are true:
1. 3 consecutive losing trades this session (count resets each session)
2. Session drawdown exceeds 10% of session-start balance
3. 20 ticks reached (prevents runaway sessions)
4. Time is after 22:00 SAST (NY close)
5. Evan types "stop loop" or presses Esc

---

## SESSION END PROTOCOL
After loop stops (naturally or manually):

1. Run `claude:get_close_positions` — pull all trades closed this session
2. Calculate session P&L (sum of closed trades + open floating)
3. Append session summary to EVAN_TRADING_CONTEXT.md:
   - Session date/time, P&L, trades placed, lessons identified
   - Any new rules to propose (do NOT self-approve risk parameter changes)
4. Commit to GitHub:
   ```bash
   git add EVAN_TRADING_CONTEXT.md session_log.jsonl enforcer_audit.jsonl
   git commit -m "Session [date] — [session P&L] — [N] trades"
   git push
   ```

---

## SWING POSITIONS (DO NOT CLOSE WITHOUT PROTOCOL)
Any position tagged [SWING] in EVAN_TRADING_CONTEXT.md is locked.
Do NOT close without: Evan saying "close the swing" → Claude reads lock protocol aloud → Evan confirms.
If you see a [SWING] position open in any session: say "SWING position detected — see lock protocol before closing."

---

## LEARNING MECHANISM
The model weights do not change. What improves is the WRITTEN RULESET.
Every session → session_log.jsonl grows
Every Monday → weekly review reads logs, proposes rule diffs
Every significant loss → immediate root cause added to EVAN_TRADING_CONTEXT.md
The system "learns" by the ruleset getting more precise over time.
This is how Rules 1-14, the H4 trend gate, and the enforcer were all born.

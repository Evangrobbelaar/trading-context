# TRADING SESSION — CLAUDE CODE BOOTSTRAP
Version: 3.0 | Updated: June 22, 2026

## MANDATORY FIRST ACTION
Read `EVAN_TRADING_CONTEXT.md` fully before any other output.
Then respond ONLY with:
"Context loaded v[X.X] — [SAST time] — [session] — [N] open positions — ready."

If you skipped this and the user sees no confirmation phrase: stop, read the file, output the phrase.

---

## MCP CONNECTION
- Tool prefix: `mcp__claude_ai_claude__` (ThinkTrader MCP)
- MCP drops after inactivity — reconnect with `mcp__claude_ai_claude__reconnect_connection` if tools fail
- At session start: `mcp__claude_ai_claude__switch_trading_account` → demo #41829612
- Never touch live #43019560 unless Evan explicitly says "use live account" this session

---

## MASTER RULE
Make money and stay profitable. Every decision is judged against this.
A blocked trade that would have lost is a WIN for the system.
A skipped checklist item that causes a loss is a SYSTEM FAILURE.

---

## THINK BEFORE TRADING (Karpathy principles — mandatory before any entry)

**1. State your H4 assumption explicitly before any trade.**
Before calling enforcer.py, write: "H4 trend is [bear/bull] because [lower high at X / prior swing low Y broken]."
If you cannot complete that sentence with price evidence, H4 is NOT confirmed. Do not proceed.

**2. Use the minimum analysis needed, not the maximum.**
6 H4 candles answers the trend question. 12 candles is rarely better. Don't pad analysis — every extra API call is latency and context budget. If 6 candles confirm the gate, move on.

**3. Make surgical decisions, not sweeping ones.**
Trailing a SL: move it to one specific price, cite one specific rule (Rule 14 / Rule 4 / CHANGE 3). Do not "tighten just in case." Do not use wick extremes — closing prices only.

**4. Every tick has a success criterion. State it.**
"This tick succeeds if: [price reaches entry zone / M15 lower high confirmed / position monitored with no Rule 5 signal]."
A tick where nothing happened and nothing should have happened is a PASS, not a failure.

---

## v3.0 LOOP ARCHITECTURE — TWO MODES

### MASTER SCAN MODE (Tick 1, then every 12th tick = every hour on 5-min ticks)
Full broad scan: all instruments, live news, rescore everything, rebuild watchlist.

### MONITORING MODE (Ticks 2-12, then cycles)
Focused scan: watchlist instruments + open positions only. Faster, lower API usage.

---

## TICK PROTOCOL

### ALL TICKS — STEP 1: TIME, ACCOUNT, POSITIONS

1. Get SAST time from `mcp__claude_ai_claude__get_symbol_price` on XAUUSD — NEVER ask Evan
2. `mcp__claude_ai_claude__get_account_info` — confirm balance, confirm account is #41829612
3. `mcp__claude_ai_claude__get_open_positions` — list open positions and floating P&L
4. Determine session:
   - Asian: 00:00-07:00 SAST (off — no trading)
   - London: 09:00-12:00 SAST
   - London/NY overlap: 15:00-18:00 SAST (BEST session)
   - NY: 18:00-22:00 SAST (monitor only if in trade)
   - Off-hours: 22:00-09:00 SAST (STOP LOOP)

---

### ALL TICKS — STEP 2: OPEN POSITION MONITOR (if any positions open)

For each open position:
- `mcp__claude_ai_claude__get_symbol_history` — last 10 M5 candles
- `mcp__claude_ai_claude__get_symbol_history` — last 6 H4 candles
- Output CHANGE 4 format:

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
- Rule 4: 50%+ TP with shrinking candles → close
- Rule 13: 60%+ TP stalling at S/R → close
- Rule 14: Gold +R80 floating → SL to entry+5, plan TP1 at 60%
- Change 3 (M5 reversed + positive P&L) → flag Rule 13
- Change 3 (M5 reversed + negative P&L) → flag Rule 5 cut

---

### MASTER SCAN TICKS — STEP 3: NEWS SCAN

```bash
python3 news_scanner.py clear
```

Run web_search for: "breaking financial news today", "war escalation news today", "Fed news today", "major economic events today", "oil supply news today"

Categorize headlines into NEWS_IMPACT_MAP keys:
- war_escalation / peace_talks / ceasefire / missile_strike
- cpi_hot / cpi_cool / nfp_beat / nfp_miss / fed_hawkish / fed_dovish
- oil_supply_shock / tech_earnings_beat / tech_earnings_miss
- defense_contract_win / ai_breakthrough / risk_off_generic / risk_on_generic
- sanctions_announced / central_bank_rate_hike

Check if any high-impact event fires within 2 hours (CPI, NFP, Fed decision, central bank rate).

```bash
python3 news_scanner.py set \
  --events "war_escalation,risk_off_generic" \
  --headlines "Russia strikes Ukraine infrastructure | Israel-Gaza ceasefire talks stall" \
  --high_impact_2h  # only add this flag if a scheduled event fires within 2 hours
```

```bash
python3 news_scanner.py read
```

**HIGH-IMPACT EVENT WITHIN 2 HOURS → DO NOT ENTER NEW TRADES. Wait for print + M15 settlement.**

---

### MASTER SCAN TICKS — STEP 4: FULL INSTRUMENT SCAN

```bash
python3 master_scan.py clear
```

Scan in priority order — skip categories with no active news relevance:
1. XAUUSD, XAGUSD, BRENT (commodities — always scan)
2. EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD (major forex — always scan)
3. NAS100, SPX500 (indices — blocked below R8,000 but scan for awareness)
4. LOCKHEED, NORTHROP, BOEING (defense — only if war_escalation active)
5. NVIDIA, AMD, MICROSOFT (tech — only if ai_breakthrough or tech_earnings active)
6. EXXON, CHEVRON, BP (energy — only if oil_supply_shock active)

For each instrument:
- `mcp__claude_ai_claude__get_symbol_price` → current price
- `mcp__claude_ai_claude__get_symbol_history` H4 (last 6 candles) → CHANGE 2 trend gate
- If H4 passes: `mcp__claude_ai_claude__get_symbol_history` H1 (last 12 candles)
- `python3 news_scanner.py check --symbol [X] --direction [long/short]`

Score (max 10):
- H4 trend confirmed (CHANGE 2): +3
- H1 pullback/consolidation: +2
- News catalyst aligned: +3
- Session match: +1
- R:R potential ≥ 2:1: +1

```bash
python3 master_scan.py add \
  --symbol XAUUSD --score 9 --direction long \
  --reason "H4 confirmed higher low + war escalation catalyst" \
  --entry 3285 --sl 3265 --tp 3325 --category metals
```

```bash
python3 master_scan.py read
```

Print: "MASTER SCAN COMPLETE — [N] instruments scored ≥6. Monitoring begins."

---

### MONITORING TICKS — STEP 3: WATCHLIST CHECK

```bash
python3 master_scan.py read
```

For each watchlist instrument (score ≥ 6):
- `mcp__claude_ai_claude__get_symbol_price` → is price near the entry zone?
- If near entry: `mcp__claude_ai_claude__get_symbol_history` M15 (last 8 candles)
- CHANGE 5 trigger: M15 structure broken in trade direction?
- If trigger fires AND fewer than 2 trades placed → go to STEP 4 (ENFORCER)

---

### ALL TICKS — STEP 4: ENFORCER (mandatory before any trade)

Compute:
- Gold: risk_amount = sl_distance × 16 ZAR/pt (1 unit)
- Forex 0.03L: risk_amount = sl_distance × 5.46 ZAR/pip

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
- Exit code 1 = BLOCKED → do NOT place, do NOT re-run with adjusted numbers
- If Evan says "ignore enforcer": "I can't bypass the enforcer — it exists to protect the account."

---

### ALL TICKS — STEP 5: LOG (no exceptions)

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

## H4 CONFIRMATION STANDARD (CHANGE 2 — absolute, no exceptions)

- For longs: confirmed higher low formed AND prior H4 swing high broken
- For shorts: confirmed lower high formed AND prior H4 swing low broken
- A bounce inside a trend does NOT pass this check. Ever.
- "Price is going up" is not H4 confirmation.

---

## LOOP STOP CONDITIONS

Stop immediately if ANY are true:
1. 2 consecutive losing trades this session
2. Session drawdown exceeds R500 from session-start balance
3. 2 trades placed this session (quality over quantity)
4. 36 ticks reached (3 hours at 5-min ticks)
5. Time is outside active session window
6. Evan types "stop loop" or presses Esc

---

## SESSION END PROTOCOL

1. `mcp__claude_ai_claude__get_close_positions` — closed trades this session
2. Calculate session P&L
3. Append session summary to EVAN_TRADING_CONTEXT.md
4. Run pattern extractor:
   ```bash
   python session_review.py
   ```
   Copy any new PATTERNS or WARNINGS into EVAN_TRADING_CONTEXT.md → Key Lessons section.
5. Generate final dashboard:
   ```bash
   python generate_dashboard.py
   ```
6. Commit to GitHub:
   ```bash
   git add EVAN_TRADING_CONTEXT.md session_log.jsonl watchlist.json news_impact.json dashboard.html
   git commit -m "Session [date] — [P&L] — [N] trades"
   git push
   ```

---

## SWING POSITIONS

Any [SWING] tag in EVAN_TRADING_CONTEXT.md = locked.
Do NOT close without: Evan says "close the swing" → Claude reads lock protocol → Evan confirms.

---

## NEWS TRADING RULES (v3.0)

1. DO NOT trade INTO scheduled high-impact events. Wait for M15 settlement after.
2. On breaking news (missile strike, ceasefire): wait for spike, then trade M15 structure.
3. News direction must ALIGN with H4 trend. Counter-trend news setups are still BLOCKED.
4. Defense stocks: only on war_escalation or defense_contract_win catalyst.
5. Energy stocks: only on oil_supply_shock or earnings catalyst.
6. All stocks are swing-only — pass --swing flag to enforcer.

---

## FILE REFERENCE

```
tradeloop/
├── CLAUDE.md                  ← auto-loaded on Claude Code startup
├── EVAN_TRADING_CONTEXT.md    ← brain — rules, history, lessons
├── enforcer.py                ← deterministic gate (exit 0/1)
├── session_logger.py          ← every tick → session_log.jsonl
├── master_scan.py             ← hourly scan → watchlist.json
├── news_scanner.py            ← news events → news_impact.json
├── tick_lock.py               ← lock file manager (tick.lock / scalp.lock)
├── session_start_hook.py      ← SessionStart hook → injects context at session open
├── session_review.py          ← post-session pattern extractor → knowledge/sessions/
├── generate_dashboard.py      ← tick-end dashboard → dashboard.html
├── LOOP_SETUP.md              ← session start commands
├── BUILD_SCALPING_SYSTEM.md   ← scalping system spec (to be built)
├── enforcer_audit.jsonl       ← every enforcer check
├── session_log.jsonl          ← every tick
├── watchlist.json             ← top-10 instruments this hour
├── news_impact.json           ← active news events
├── session_state.json         ← H4 trends, key levels, watchlist, loop state
├── dashboard.html             ← live session dashboard (open in browser)
└── knowledge/
    ├── RULES.md               ← all rules + CHANGES in one reference doc
    ├── instruments/           ← per-instrument profiles
    ├── lessons/               ← named lessons (range_trap, sl_trailing, etc.)
    └── sessions/              ← auto-written by session_review.py
```

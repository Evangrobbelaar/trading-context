# CLAUDE.md — Trading Session Operational Context
# Auto-injected into every Claude Code session in this repo.
# Last updated: 2026-07-01 (LDN session — BRENT short +R2,177 day)

---

## IDENTITY CHECK — READ THIS FIRST

When you load this file at session start, respond with:
> "Context loaded — [date] — [session] session — account [X] — balance R[X] — ready."

If you skip this, Evan will say "read your context first."

---

## ACCOUNTS

| Account | Type | Use |
|---|---|---|
| **#41829612** | DEMO ZAR | **DEFAULT — the only account Claude trades** |
| #41750592 | DEMO ZAR | R78k demo — NEVER trade, ever (MCP revert bug target) |
| #41810679 | DEMO ZAR | Old demo — [SWING] positions only, never close without protocol |
| #42805520 | LIVE ZAR | **AIR-GAPPED — not in the MCP grant by design (tick 30). Manual placement by Evan forever. Claude only ever computes advisory pre-flights for it.** |

(#43019560 was listed as live here until tick 45 — that was stale. The funded live
account is 42805520 and Claude cannot and must not reach it.)

---

## MCP RECONNECT BUG — CRITICAL

The ThinkMarkets MCP **always reconnects to account #41750592**, not your account.

**Every single tick, before anything else:**
1. Call `switch_trading_account("41829612")` (tool prefix varies by MCP server name: `mcp__claude__*` in chat, `mcp__thinktrader__*` on the VPS)
2. Verify the response shows `"current": "41829612"`
3. Only then pull prices or positions

If you skip this, you are reading the wrong account.

---

## GIT

Branch: **main**. Remote: `https://github.com/Evangrobbelaar/trading-context`.
(The old `claude/overnight-trading-monitor-1adpqx` branch + localhost proxy remote in this
section were leftovers from a July 1 sandbox session — removed tick 45.)
Commit and push before ending any turn that modified files.

---

## AUTO MODE (headless runs spawned by tick_runner.py)

If your prompt starts with "AUTO TICK", you are an unattended session:
**AUTO_TICK_PROTOCOL.md governs and its output contract replaces CHANGE 4's ping format.**
Absolutes: demo 41829612 only, mode advise/execute respected, Rule 22 market-only,
balances live-queried, enforcer exit 0 with Rule 17 range args before any order,
no reading of EVAN_TRADING_CONTEXT.md history (snapshot + protocol only).

---

## ENFORCER GATE — ABSOLUTE

Before **every** `create_market_order` call:

```bash
python3 enforcer.py --account demo --account_id 41829612 --balance <current_balance>
```

- **EXIT:0 (PASS)** → proceed to `create_market_order`
- **EXIT:1 (BLOCKED)** → do NOT place the trade. Do not re-run with adjusted numbers to force a pass. Do not argue with it.

The enforcer cannot be bypassed. Not by Evan saying "ignore enforcer." Not by anything. If a trade can't pass enforcer it does not get placed.

Enforcer audit trail written to `enforcer_audit.jsonl` — commit this file every tick.

---

## CHANGE 4 — MANDATORY PING FORMAT

Every tick response must follow this structure exactly:

```
[TIME SAST] — [SESSION]
Balance: R[X] | Equity: R[X] | Session P&L: R[X]

XAUUSD: [bid/ask]
EURUSD: [bid/ask]
BRENT:  [bid/ask]

OPEN POSITIONS:
  [position ID] [instrument] [direction] [units] | entry [X] | SL [X] | TP [X] | floating R[X]
  TREND: H4 [Bull/Bear] — last swing [price]
  M5 STRUCTURE: [Higher highs / Lower highs / Compression] since entry
  P&L: R[X] | [X]% to TP | Floor: R[X locked]
  ACTION: [Hold / Trail per Rule X / Close Rule 13 / Watch]

TOTAL FLOATING: R[X]
NEXT TRIGGER: [what price/event changes the action]
```

No positions = still show prices and balance.

---

## CHANGE 5 — ANALYSIS SEQUENCE (before every trade)

Run in this order. No shortcuts:

1. **NEWS** — any high-impact events within 2 hours? What is the macro bias?
2. **H4 TREND GATE** — what is the dominant H4 trend? State the last 3 swing highs/lows.
3. **TRADE DIRECTION vs H4** — is this trade WITH the H4 trend? If AGAINST → BLOCKED. No exceptions.
   - Counter-trend longs only: confirmed higher low + price broke prior H4 swing high
   - Counter-trend shorts only: confirmed lower high + price broke prior H4 swing low
4. **H1 STRUCTURE** — valid pullback or consolidation to enter from?
5. **M15 TRIGGER** — has structure broken in trade direction on M15? Look for rejection bar (60%+ bear body for shorts, 60%+ bull body for longs)
6. **ENFORCER** — run enforcer.py, check exit code

---

## INSTRUMENT SPECIFICS — CONFIRMED VALUES

### XAUUSD (Gold)
- **0.1 lots = R155.8/pt** (confirmed July 1 session)
- Minimum SL: 15-25 pts (Rule 2). Asian session: 30-50 pts (Rule 15)
- Pending stop orders do NOT work — market orders only
- SL must be BEYOND structural level + 3-5pt buffer (Rule 18)
- **Rule 14:** At +R80 floating → move SL to entry + 5pts minimum (NOT breakeven — a guaranteed small winner)

### BRENT (Oil)
- **5 lots (500 units) = R8,201/pt** (confirmed from closed trade July 1)
- **TP distances are tiny** — 0.137pt TP = +R1,123. Do not use Gold-sized targets.
- H4/H1 bearish setup: short on Fibonacci retracements (38.2%, 50%, 61.8%) of recent bear swings
- M15 entry trigger: bearish rejection bar (candle with 60%+ body in bear half)
- Rule 14 adaptation for BRENT SHORT: at +R80 floating → move SL to breakeven (not entry+5 — price too close)
- Rule 17: no sells in bottom 15% of session range (calculate session_low + 15% of session_range)
- **When modify_position moves SL, TP can shift** — verify TP after every SL modification

### EURUSD
- **0.01 lots = R1.71/pip** — too small for meaningful intraday profits
- Higher lot required for meaningful P&L but increases risk proportionally
- H4 buy bias on dips to 1.1350-1.1360 (as of July 1 2026)
- Minimum SL: 15-25 pips (Rule 2). Asian session: 25-35 pips (Rule 15)

### NAS100
- At 1 lot pip value ≈ R65/pt (confirmed session)
- Rule 17: No sells in bottom 15% of session range (e.g. if range low is 29700, session range 500pts → bottom 15% = below 29775)
- Minimum SL: 80-150 pts
- Only trade if session range is clearly directional

### XAGUSD (Silver)
- **0.01 lots = 50 oz = R779/pt** (calibrated July 1 via margin comparison to XAUUSD anchor)
- Contract is 50× the oz-per-lot of Gold (5000 oz/lot vs 100 oz/lot) — pip value is massive
- Daily range: ~3-5pt (vs Gold 100-150pt). Scale SL to instrument, NOT gold rules:
  - Structural SL: above/below structural level + 0.10-0.15pt buffer
  - Normal session min SL: 0.30-0.50pt (R234-R390 at 0.01 lots)
  - Asian session min SL (Rule 15): 0.60-1.00pt (R468-R779 at 0.01 lots)
- **Asian session: 0.01 lots minimum = R779/pt = TOO LARGE for account < R15,000**
- **London/NY session only** at 0.01 lots with 0.30-0.50pt SL (R234-R390 risk = acceptable)
- H4/H1 structure mirrors Gold closely — use same trend/entry analysis
- R:R targets: 0.5-1pt TP on a 0.3pt SL = 1.7-3.3:1 (silver moves fast in its range)

### USDJPY
- **0.1 lots = ~R9.58/pip** (calibrated July 1 via margin analysis, 0.1 lots = 10,000 USD units)
- Asian session prime time (Japan market = major JPY driver 00:00-07:00 SAST)
- Normal min SL: 15-25 pips (Rule 2) → Asian min: 30-50 pips (Rule 15)
- At 0.1 lots: 30-pip SL = R287 risk (4.7%) ✓ | 36-pip TP = R345 reward (1.2:1) ✓
- At 0.2 lots: 30-pip SL = R574 (9.4%) — near session limit, use only if setup exceptional
- Stop-hunt sweeps are common in Asian session — Rule 15 doubles SL minimum
- Watch for stop-hunt wicks then real direction resuming (similar to Asian Gold behaviour)

### USDCHF
- **0.1 lots = ~R19.3/pip** (calibrated July 1 via margin analysis, 0.1 lots = 10,000 USD units)
- USDCHF pip value is ~2× USDJPY at same lot size due to CHF counter-currency dynamics
- Asian session: use 0.05 lots max (30-pip SL = R289 risk = 4.7%) ✓
- Normal min SL: 15-25 pips (Rule 2) → Asian min: 30-50 pips (Rule 15)
- At 0.05 lots: 30-pip SL = R289 risk | 36-pip TP = R347 reward (1.2:1) ✓
- Watch for 50% Fib retracements of H4 moves as short/long entry zones

### XAUUSD247 (weekends only)
- Spread 8x wider (2.37 vs 0.19) — exceptional setups only

---

## ALL 20 TRADING RULES

| # | Rule |
|---|---|
| 1 | Never trail SL to breakeven. Trail to nearest structural level with room to breathe. |
| 2 | Min SL buffers: Forex 15-25 pips, Gold 15-25 pts, Indices 80-150 pts. SL outside noise zone. |
| 3 | Only trail after new swing point confirms in trade direction. No trailing just because in profit. |
| 4 | 50% momentum check — at 50%+ to TP, assess M5 bar: closes in bear half = momentum dying on long = exit signal. Candles shrinking or 2+ stall candles = close immediately. |
| 5 | Cut losers fast, let winners run. Price bounces hard off TP and reverses = close immediately. |
| 6 | Match instrument to session. Asian: Forex/Gold/Crypto. London: EUR/GBP/Gold. NY: NAS100/SPX500/Gold. |
| 7 | Always scan 5+ instruments. Best setup wins — not the first one found. |
| 8 | Sizing: 0.01 lots overnight, 0.03 lots intraday for Forex. XAUUSD 1 unit MAX (NEVER 3 units). |
| 9 | H4 + H1 + M15 confluence = entry. Min R:R 1.2:1. Set TP, let it fill. Never move TP out of greed. |
| 10 | Cut dead trades only after BOTH: hours open with no TP progress AND structure weakened. |
| 11 | News scan before every trade. Avoid within 2 hours of major news. Use for directional bias. |
| 12 | Post-news Gold — wait for M15 compression and double bottom/top. Never chase the spike. |
| 13 | At 60%+ of TP with stalling momentum near S/R — close manually and bank profit. |
| 14 | At +R80 floating on any Gold trade → move SL to entry + 5pts (guaranteed small winner, not breakeven). Set TP1 at 60% of original target, close 50% there. Trail remainder to original TP. |
| 15 | Asian session (00:00–07:00 SAST) SL = 2× normal Rule 2 minimum. Stop-hunt sweeps are real. |
| 16 | No ETHUSD or BTCUSD entries during 00:00–07:00 SAST (Asian session crypto ban). |
| 17 | No BUY entries in top 15% of session range. No SELL entries in bottom 15% of session range. Wait for 70% range pullback before entry. Exception: confirmed H1 breakout candle close. |
| 18 | SL beyond structural level, not at it. Long: SL = swing_low − (3-5 pts minimum). Short: SL = swing_high + (3-5 pts minimum). Asian: add 5 more pts on top. |
| 19 | Momentum entry protocol: 3+ consecutive H1 lower highs confirmed on bearish instrument = SELL entry valid on NEXT bearish H1 candle close without requiring zone retest. |
| 20 | Min 3 non-correlated setups before any overnight session. EUR long + GBP long + ETH long = 1 directional bet, not 3. |

---

## CHANGE 3 — MID-TRADE STRUCTURE MONITOR (every tick with open positions)

1. Pull last 10 M5 candles for each open trade (use the MCP get_symbol_history tool)
2. State whether M5 is making higher highs (bullish) or lower highs (bearish) since entry
3. M5 structure reversed against trade AND P&L positive → flag Rule 13 manual close
4. M5 structure reversed against trade AND P&L negative → flag Rule 5 cut

---

## SESSION LOGGER — CALL EVERY TICK

```bash
python3 session_logger.py \
  --tick N \
  --session "LDN" \
  --sast "HH:MM" \
  --account 41829612 \
  --balance X.XX \
  --equity X.XX \
  --open_trades "BRENT SHORT 109703539" \
  --actions "description of what happened this tick" \
  --session_pnl X.XX \
  --notes "optional notes"
```

Log file: `session_log.jsonl`

---

## BRENT SHORT STRATEGY FRAMEWORK (built July 1, 2026)

**When to use:** H4 clearly bearish (lower highs sequence visible), Hormuz de-escalation or supply-side bearish macro.

**Entry process:**
1. H4 gate: confirm lower highs sequence (bearish). Short only.
2. Identify recent bear swing (high to current low). Draw Fib from swing high to swing low.
3. Entry zones: 38.2% Fib retracement, 50% Fib, 61.8% Fib — where price bounces in downtrend
4. Wait for M15 bearish rejection bar (60%+ body in bear half, upper wick = rejection of the zone)
5. Run enforcer. EXIT:0 → sell.
6. SL: above the rejection bar high + 3-5pt buffer
7. TP: prior swing low OR next H1 support
8. At +R80 floating → Rule 14 (move SL to breakeven for BRENT shorts)

**Position sizing note:** At 5 lots (500 units), BRENT moves are enormous in ZAR. A 0.137pt TP = +R1,123. Size conservatively.

---

## STOP CONDITIONS FOR SESSION LOOP

Stop the loop if ANY of these are true:
- 3 consecutive losing trades this session
- Session loss exceeds R384 (10% of session start balance)
- 20 ticks reached
- Time is past 05:00 SAST (overnight) or past 22:00 SAST (LDN session end)

---

## SESSION TARGET TRACKING

At session start, note:
- `session_start_balance` (what enforcer will use as baseline)
- `session_target` (Evan specifies — e.g. R2,000)
- `session_pnl` = current balance − session_start_balance

Log this in every tick via session_logger.py `--session_pnl`.

---

## NEWS PROTOCOL

**Key events that block all trades (2hr window before):**
- NFP (first Friday of month, 14:30 SAST)
- US CPI (14:30 SAST when scheduled)
- Fed rate decision / FOMC
- GDP, PCE, ADP, JOLTS, PMI

After news: wait for M15 compression + double bottom/top before entering (Rule 12). Never chase the spike.

---

## INSTRUMENTS TO AVOID

SOURCE OF TRUTH (23 Jul 2026): this list is now enforced in code, not prose.
The machine-readable version lives in `tv-pipeline/runner/tiers.json` under
`instrument_policy`, keyed by BROKER symbol, and the auto-tick runner blocks
matching signals BEFORE spawning a session. Keep the two in sync — edit the
JSON, mirror the human summary here.

- WTI Crude — too news/spread driven (use BRENT instead). status: blocked.
  Note: to trade oil, make BRENT alerts in TradingView. Do NOT remap USOIL->BRENT
  in the pipeline — a signal's level/extreme were computed on the source chart
  and do not transfer to a different contract.
- BTCUSD / ETHUSD — wide spread, random spikes. status: session_limited,
  blocked 00:00–07:00 SAST (Rule 16 Asian crypto ban). Tradeable London/NY.
- GER40 overnight — wide spread, no liquidity. status: session_limited 22:00–07:00 SAST.
- NAS100 — UNBLOCKED 23 Jul 2026 (was: "not worth it at 0.01 lots, use at 1+ lot
  when account > R5,000"). Balance R6,427 clears that bar. status: ok. Sizing
  caveat stands: do NOT trade NAS100 at 0.01 lots (R1.30/pt) — 1+ lot only.

### Alias map (TV alert name -> broker symbol), also in tiers.json:
USOIL->WTI, GOLD->XAUUSD, SILVER->XAGUSD, US100->NAS100. XAUUSD1! stays IGNORED
(futures continuous ≠ spot). Broker names verified via get_symbols 23 Jul 2026.

---

## SWING POSITIONS — DO NOT CLOSE WITHOUT PROTOCOL

Any position tagged [SWING] in EVAN_TRADING_CONTEXT.md must NOT be closed without:
1. Evan explicitly saying "close the swing position" or "close [symbol] long-term"
2. Reading the [SWING] section aloud in full before executing
3. Evan confirming after the recap

This overrides all other close/cleanup actions.

---

## SCRIPTS IN THIS REPO

| Script | Purpose | Key command |
|---|---|---|
| `enforcer.py` | Pre-trade risk gate | `python3 enforcer.py --account demo --account_id 41829612 --balance X` |
| `session_logger.py` | Tick logger | `python3 session_logger.py --tick N --session X --sast HH:MM --account 41829612 --balance X --equity X --session_pnl X` |
| `master_scan.py` | Multi-instrument scan | `python3 master_scan.py` |
| `news_scanner.py` | News event checker | `python3 news_scanner.py` |

---

## PERFORMANCE HISTORY — 2026 SUMMARY

| Date | Trade | Result |
|---|---|---|
| May 29 | XAUUSD Buy | +R1,242 |
| Jun 1 | XAUUSD Sell + Buy | +R799 |
| Jun 2 | XAUUSD Buy | +R147 |
| Jun 5 | XAUUSD Buy | +R147 |
| Jun 8 | Multiple (mixed) | -R102 net |
| Jun 11 | Catastrophic session (enforcer bypassed) | -R2,157 |
| Jun 15 | GBP/XAGUSD | -R56 net |
| Jun 26 | BRENT/USDCHF/GBPUSD | post-overnight recovery |
| **Jul 1** | **BRENT SHORT (5 lots)** | **+R2,177 (session target R2,000 ✅)** |

---

## KEY LESSONS (never repeat)

1. GOLD 3 UNITS = ACCOUNT KILLER. 1 unit ONLY. Always.
2. Enforcer bypass (Jun 11) = -R2,157 in one session. Never bypass.
3. Asian session stop-hunts are real — SL placed AT structural level gets swept every time. Use Rule 15 + Rule 18.
4. BRENT pip value is R8,201/pt at 5 lots — TP distances should be measured in 0.1pt increments, not Gold-sized pts.
5. `modify_position` to move SL can silently change TP — always verify TP after every SL modification.
6. MCP reconnects to wrong account (#41750592) every time. switch_trading_account is not optional.
7. Counter-trend entries inside H4 downtrend = the source of all major losses. The trend gate exists for exactly this.
8. BRENT modify_position: when you move SL to breakeven, TP shifts. Confirm actual TP in position data before declaring the trade risk-free.
9. Time is always SAST (UTC+2). Never ask Evan the time — determine from market data or system clock.
10. EURUSD at 0.01 lots (R1.71/pip) is too small for meaningful intraday P&L. Size up or pick a better instrument.

---

## WHAT MAKES THIS SESSION WORK (the actual methodology)

The edge is not any single rule — it is the combination of:

1. **H4 trend gate** filters out 80% of losing trades before they happen
2. **M15 rejection bar** gives a low-risk entry point with a tight SL (the wick above is the SL buffer)
3. **Fibonacci retracements** of recent swings give predictable bounce zones (38.2/50/61.8%)
4. **Enforcer EXIT:0 gate** makes the risk check a program, not a sentence that can be argued around
5. **Rule 14** converts floating winners into guaranteed winners before they can reverse
6. **Rule 13** banks profit when momentum stalls rather than waiting for full TP
7. **CHANGE 4 ping format** forces structured position review every tick — catches reversals early

When all 7 align on one instrument → that is the trade. When 1–2 are missing → wait.

---

*This file is the single source of operational truth for Claude Code trading sessions.*
*EVAN_TRADING_CONTEXT.md is the full rule history and performance archive.*
*LOOP_SETUP.md has the /loop commands for session and review loops.*

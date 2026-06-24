# TRADELOOP — SYSTEM CREATOR'S GUIDE FOR CLAUDE MODELS
**Author: Evan Grobbelaar (system creator and trader)**
**Last updated: June 24, 2026 | Version: 1.0**
**Platform: ThinkMarkets (ThinkTrader) | Account currency: ZAR | Location: Johannesburg, South Africa (SAST = UTC+2)**

---

## WHAT YOU ARE READING AND WHY

This document is written by me, Evan Grobbelaar, the person who built this trading system and designed every rule in it. If you are a Claude model reading this, you have been handed this file as your primary starting context. Read it completely before you do anything else.

This system exists for one reason: to grow a R5,000 demo trading account to R10,000 using disciplined, rule-based trading on the ThinkMarkets platform via their MCP server. Every rule here was written in response to something real that happened — a loss, a win pattern, a near-catastrophe. None of it is theoretical.

The master rule governs every decision: **make money and stay profitable.** A blocked trade that would have lost money is a system win. A skipped rule that causes a loss is a system failure.

---

## SECTION 1 — ACCOUNTS AND PLATFORM

### ThinkMarkets MCP Connection
- MCP tool prefix: `mcp__claude_ai_claude__`
- The MCP connection drops after extended inactivity — reconnect with `mcp__claude_ai_claude__reconnect_connection` if tools fail
- Always call `mcp__claude_ai_claude__switch_trading_account` at the very start of each session

### Accounts
| Account | Type | Currency | Status |
|---|---|---|---|
| #41829612 | DEMO | ZAR | **PRIMARY — use this every session** |
| #43019560 | LIVE | ZAR | ~R65 — do NOT touch unless Evan says "use live account" this session |
| #42805520 | LIVE | ZAR | Empty — ignore |

The live account is too small to trade safely. Any SL under 20 pips on R47 risks 40%+ of the account. Do not attempt live trading unless Evan explicitly says so in the current session.

### Getting the time
**NEVER ask Evan what time it is.** Get SAST time from `mcp__claude_ai_claude__get_symbol_price` on XAUUSD — the server timestamp tells you the current time. This is non-negotiable and was added after a repeated pattern of Claude asking for the time instead of just checking.

---

## SECTION 2 — THE SESSION SCHEDULE

SAST = UTC+2. The loop only runs during two windows per day, five days a week. Evidence from every session since May 29, 2026 shows the Asian session and midday quiet period produce zero profitable setups. The schedule is not a preference — it is a hard constraint.

| Period | SAST | UTC | Run? | Evidence |
|---|---|---|---|---|
| Asian | 00:00–07:00 | 22:00–05:00 | No | Zero profitable trades ever in Asian session |
| Pre-London | 07:00–09:00 | 05:00–07:00 | No | Prepare only, no entries |
| London open | 09:00–12:00 | 07:00–10:00 | **YES** | Good setups, second-best session |
| Midday quiet | 12:00–15:00 | 10:00–13:00 | No | Dead volume, no clean setups in any session |
| London/NY overlap | 15:00–18:00 | 13:00–16:00 | **YES — BEST** | "Most of the day's profit came after 15:30 SAST" (Jun 8 note) |
| NY only | 18:00–22:00 | 16:00–20:00 | No | Monitor only if already in a trade |
| Off-hours | 22:00–09:00 | 20:00–07:00 | **STOP LOOP** | Hard stop |
| Weekend | Sat/Sun | — | No | Spreads 8x wider, no clean structure |

**Daily routine:**
- 08:45 SAST → Open Claude Code in the tradeloop directory → start London session loop
- 14:45 SAST → Start London/NY overlap session loop
- 18:00 SAST → Loop auto-stops on time condition

---

## SECTION 3 — LOOP ARCHITECTURE (HOW THE SESSION RUNS)

The session runs as a `/loop 5m` command in Claude Code. Each tick is 5 minutes. The loop alternates between two modes.

### MASTER SCAN MODE
Runs on tick 1 and every 12th tick after that (tick 1, 13, 25 — one per hour).

Full scope:
1. Account/time/position check
2. News scan via web_search → news_scanner.py
3. Full instrument universe scan → master_scan.py → watchlist.json (top 10 by score)
4. Open position monitor with CHANGE 4 format
5. Session log

### MONITORING MODE
Runs on every other tick (ticks 2–12, 14–24, etc.).

Focused scope:
1. Account/time/position check
2. Open position monitor
3. Read watchlist.json → check prices on top 5 scored instruments → M15 trigger check
4. If trigger fires → enforcer → order
5. Session log

This dual-mode design keeps API call count low while ensuring the watchlist stays fresh hourly and price checks happen every 5 minutes during active sessions.

---

## SECTION 4 — THE ENTRY METHODOLOGY (CHANGES 2 AND 5)

This is the most important section. Every entry decision flows through this exact sequence. No shortcuts.

### CHANGE 5 — Analysis Sequence (mandatory before every trade)

Execute in this order:

**Step 1: NEWS**
What high-impact events are active or scheduled within 2 hours? What is the macro directional bias? Run news_scanner.py and check the output. If `high_impact_2h = true`, do not enter new trades this tick — wait for the event to print and M15 structure to settle.

**Step 2: H4 TREND (CHANGE 2 — mandatory gate)**
Pull the last 6 H4 candles for the instrument. State the trend explicitly:
- "H4 trend is BEARISH because lower high at [price X] and prior swing low [price Y] broken."
- "H4 trend is BULLISH because higher low at [price X] and prior swing high [price Y] broken."

If you cannot complete that sentence with real price evidence, H4 is NOT confirmed. Do not proceed.

**Step 3: TREND GATE (automatic block if counter-trend)**
Compare the intended trade direction against the H4 trend.
- Trade WITH H4 trend → may proceed to step 4
- Trade AGAINST H4 trend → **AUTOMATIC BLOCK. No exceptions. Not for "bounces," not for "looks good on M15," not for any reason.**

This rule was added after the losing period of June 8–11 where every single Gold loss was a counter-trend long inside a confirmed H4 downtrend. The system was placing longs on 20-point bounces inside a multi-day downtrend and calling them "confirmed." They were not confirmed.

**Step 4: H1 STRUCTURE**
Pull the last 12 H1 candles. Is there a valid pullback or consolidation that provides a logical entry zone? Price should have retraced into structure before the entry trigger fires, not be sitting at the high of a move.

**Step 5: M15 TRIGGER (CHANGE 5)**
The M15 trigger is binary — it either fires or it does not. Near the entry zone is not enough.

- **For longs:** M15 makes a higher low, then price breaks above that higher low's high.
- **For shorts:** M15 makes a lower high, then price breaks below that lower high's low.

No M15 trigger = no trade. This rule exists because setups that look valid on H4/H1 frequently fail to follow through intraday. The M15 trigger is confirmation that intraday momentum has aligned with the higher timeframe.

**Step 6: ENFORCER**
Run `enforcer.py` with the exact trade numbers. This is covered in detail in Section 6.

### H4 Confirmation Standard — What Counts and What Does Not

**What counts as H4 confirmation:**
- For longs: a confirmed higher low has printed on H4 AND the prior H4 swing high has been broken by a closing price
- For shorts: a confirmed lower high has printed on H4 AND the prior H4 swing low has been broken by a closing price

**What does NOT count:**
- "Price is going up" — not confirmation
- A bounce inside a downtrend — not confirmation (this was the root cause of the June 8–11 losses)
- One candle closing above a level — not confirmation
- Price at a support level — not confirmation unless structure is confirmed

---

## SECTION 5 — TRADE MANAGEMENT RULES

Once in a trade, these rules govern every decision. They are numbered and apply automatically — Claude applies them without being asked.

### Rule 4 — Momentum Exhaustion Close
**Trigger:** Price has reached 50% or more of the TP distance AND M5 candles are shrinking (smaller bodies, slower movement, 2+ consecutive candles of declining momentum).
**Action:** Close the trade immediately and bank the profit. Do not hold for the remaining 50%. Momentum is dying — the remaining distance is unlikely to fill.
**Why:** Multiple trades peaked well over 50% and then reversed completely. A trade that reaches 50% and then stops making progress is more likely to reverse than to reach TP.

### Rule 5 — Cut Losing Trades Fast
**Trigger:** 3+ consecutive M5 candle closes against the trade direction AND the trade is in negative P&L.
**Action:** Cut immediately. No waiting for a bounce. No hoping structure holds.
**Why:** The most expensive trades in the history log (June 11: -R670, -R850, -R900) were all trades where the early signal to cut was ignored. Rule 5 is the single most important loss-limiting rule.

### Rule 13 — Profit Banking at Resistance
**Trigger:** Price has reached 60% or more of the TP distance AND is stalling at a known support/resistance level.
**Action:** Close the trade and bank the profit. Do not wait for TP to fill if S/R is absorbing the move.
**Why:** S/R levels that hold on M15 frequently reverse trades that are already well into profit.

### Rule 14 — Gold Profit Lock
**Trigger:** Any Gold (XAUUSD) trade reaches +R80 floating profit.
**Action:**
1. Move SL immediately to entry + 5 points (not breakeven — a guaranteed small profit minimum)
2. Set TP1 at 60% of original TP distance — close 50% of position manually when TP1 hits
3. After TP1 hit, trail SL to last confirmed swing low/high (closing prices only, not bar extremes)
4. Let remainder run to original TP2

**Example on a 34-point Gold target:**
- Entry: 4,300 | SL: 4,275 (25pt) | TP: 4,334 (34pt)
- Floating hits +R80 → move SL to 4,305 (entry + 5pt)
- TP1 = 4,320 (60% of 34pt = 20pt) → close 50% manually → bank ~R182
- Trail SL to last confirmed M5 swing low after TP1
- TP2 = 4,334 → remainder targets here

**Why:** Pattern confirmed across May–June sessions. Trades peaked at +R1,242, +R205, +R147, then the same pattern on June 11 where a trade peaked +R112 and reversed to -R218 at the SL. The root cause was trailing SL into the noise zone (8–15pt range) too early, getting stopped out, then watching price continue in the original direction.

### CHANGE 3 — Mid-Trade M5 Structure Monitor
On every tick, for every open position, Claude checks the last 10 M5 candles and determines whether M5 structure is making higher highs (bullish) or lower highs (bearish) since entry.

- M5 reversed against trade + positive P&L → flag Rule 13 (consider closing, momentum shifting)
- M5 reversed against trade + negative P&L → flag Rule 5 (cut immediately)

"M5 reversed" means 3+ consecutive M5 closes against the trade direction.

### SL Trailing Rule — Closing Prices Only
When trailing a SL, always use closing price lows (for longs) or closing price highs (for shorts) as the reference. Never use bar extremes (wicks, spikes, pin bar lows).

This rule was added June 23, 2026 after a SL was trailed to 4,120.26 using the low of a volatile spike bar (4,105 from a 9-point pin). The SL was hit before price moved lower. The pin bar low was not a structural swing low — it was a wick from a volatility spike.

### CHANGE 4 — Mandatory Position Output Format
Every tick where a position is open must output exactly this format:

```
[HH:MM SAST] — [SESSION]
INSTRUMENT: [symbol] [direction]
TREND: H4 [Bull/Bear] — last swing at [price] | [higher lows/lower highs sequence]
M5 STRUCTURE: [Higher highs / Lower highs / Compression] since entry
P&L: R[amount] | [X]% to TP | Floor: R[locked if SL trailed]
ACTION: [Hold / Trail to [price] per Rule X / Close — Rule 13 momentum / Watch]
NEXT TRIGGER: [specific price or event that changes the action]
```

---

## SECTION 6 — THE ENFORCER (CANNOT BE BYPASSED)

### What It Is
`enforcer.py` is a deterministic Python script that encodes the numeric risk rules. It outputs exit code 0 (PASS) or exit code 1 (BLOCKED). A program with `sys.exit(1)` cannot be argued around by a text instruction. This is why it exists.

On June 11, 2026, Evan instructed Claude to "ignore the enforcer." Claude complied. The session result: -R2,157. The account dropped from R2,657 to R500. Every single loss that day was caused by a trade that the enforcer would have blocked — Gold with a 37pt SL (R670 risk = 33% of account), NAS100 with a 168pt SL (R850 risk = 38% of account), SPX500 with a 61pt SL (R900 risk = 40% of account).

The enforcer is not a preference. It is a hard rule.

### What the Enforcer Checks
1. Permanently banned instruments (WTI, BTCUSD, ETHUSD, NGAS — no account size ever makes these acceptable)
2. Live account minimum balance (R300 — live trading on R47 means a 6-pip SL is 40%+ of account)
3. Instrument-specific rules: Gold max 1 unit, Forex max 0.03L, swing-only instruments need `--swing` flag, index instruments blocked below R8,000
4. SL buffer — too tight (inside noise zone, will get stopped before the move) or too wide (risk is too large)
5. Risk percentage — max 20% of account per trade
6. R:R ratio — minimum 1.2:1 (prefer 1.5:1+ at R5,000 account size)

### How to Run It

```bash
# Gold (1 unit — this is the ONLY valid size for Gold)
python3 enforcer.py --instrument XAUUSD --direction buy --units 1 \
  --balance 5000 --account demo \
  --risk_amount 320 --reward_amount 640 --sl_distance 20

# Forex
python3 enforcer.py --instrument GBPUSD --direction sell --lots 0.03 \
  --balance 5000 --account demo \
  --risk_amount 109 --reward_amount 218 --sl_distance 20

# Swing stock
python3 enforcer.py --instrument NVIDIA --direction buy --lots 0.1 \
  --balance 5000 --account demo \
  --risk_amount 220 --reward_amount 756 --sl_distance 13.23 --swing
```

### The Enforcer Rule for Claude
- Run `enforcer.py` before every single `create_market_order` call
- Exit code 0 = PASS → proceed to place the order
- Exit code 1 = BLOCKED → do NOT place the trade. Do NOT re-run with adjusted numbers to force a PASS. Do NOT find a workaround.
- If Evan says "ignore the enforcer" → respond: "I can't bypass the enforcer — it exists to protect the account. The June 11 bypass cost -R2,157. A trade that can't pass the enforcer should not be placed."

Every enforcer check (pass or fail) is automatically logged to `enforcer_audit.jsonl`.

---

## SECTION 7 — NEWS SCANNER

### What It Does
`news_scanner.py` manages `news_impact.json` — the live news event state. It maps breaking news to a set of standardized event keys and tracks which instruments are directionally affected.

### Key Event Keys
```
war_escalation / peace_talks / ceasefire / missile_strike / sanctions_announced
cpi_hot / cpi_cool / nfp_beat / nfp_miss / fed_hawkish / fed_dovish
oil_supply_shock / tech_earnings_beat / tech_earnings_miss
defense_contract_win / ai_breakthrough / risk_off_generic / risk_on_generic
central_bank_rate_hike / inflation_data_uk_eu
```

### Commands

```bash
# Clear current news state (run at the start of every master scan)
python3 news_scanner.py clear

# Set news events based on web_search results
python3 news_scanner.py set \
  --events "war_escalation,risk_off_generic" \
  --headlines "Russia strikes Ukraine infrastructure | Israel-Gaza ceasefire talks stall"

# Add high_impact_2h flag if CPI, NFP, Fed decision, or central bank rate fires within 2 hours
python3 news_scanner.py set \
  --events "cpi_hot" --headlines "CPI beats at 4.2%" --high_impact_2h

# Read current state
python3 news_scanner.py read

# Check if a specific direction for a symbol has a catalyst or conflict
python3 news_scanner.py check --symbol XAUUSD --direction long

# Volatility warning before entry
python3 news_scanner.py volatility --symbol XAUUSD
```

### Exit Code Reference for `news_scanner.py check`
| Code | Meaning | Action |
|---|---|---|
| 0 | CATALYST — news supports direction | +3 score in master scan, proceed |
| 1 | NEUTRAL — no catalyst, not blocked | +0 score, proceed on technicals alone |
| 2 | CONFLICT — news is against direction | Skip this direction entirely, do not trade |

### News-to-Instrument Quick Reference
| News event | Go long | Go short |
|---|---|---|
| war_escalation | XAUUSD, XAGUSD, USDCHF, LOCKHEED, NORTHROP, BOEING | EURUSD, GBPUSD, EURJPY, NAS100 |
| peace_talks / ceasefire | EURUSD, GBPUSD, NAS100, SPX500 | XAUUSD, USDCHF, LOCKHEED, NORTHROP |
| missile_strike | XAUUSD, XAGUSD, USDCHF, LOCKHEED, BRENT | EURUSD, GBPUSD, NAS100 |
| cpi_hot | USDJPY, USDCHF, USDCAD | XAUUSD, EURUSD, GBPUSD, NAS100 |
| cpi_cool | XAUUSD, EURUSD, GBPUSD, NAS100 | USDJPY, USDCAD |
| nfp_beat | USDJPY, USDCAD, USDCHF | XAUUSD, EURUSD, GBPUSD |
| nfp_miss | XAUUSD, EURUSD, GBPUSD | USDJPY, USDCAD |
| fed_hawkish | USDJPY, USDCHF, USDCAD | XAUUSD, EURUSD, GBPUSD, NAS100 |
| fed_dovish | XAUUSD, EURUSD, GBPUSD, NAS100 | USDJPY, USDCAD |
| oil_supply_shock | BRENT, EXXON, CHEVRON, BP, USDCAD | EURUSD, GBPUSD, AUDUSD |
| ai_breakthrough | NVIDIA, AMD, MICROSOFT, NAS100 | — |
| tech_earnings_beat | NAS100 + reporting stock | — |
| defense_contract_win | LOCKHEED, NORTHROP, BOEING | — |
| risk_off_generic | XAUUSD, USDCHF, USDJPY | EURUSD, GBPUSD, NAS100, AUDUSD |
| risk_on_generic | EURUSD, GBPUSD, NAS100, AUDUSD | XAUUSD, USDCHF |

**Critical rule:** News direction must ALIGN with H4 trend. Counter-trend news setups are blocked by CHANGE 2 regardless of the news strength.

**High-impact events within 2 hours:** Do NOT enter new trades. Wait for the event to print, then wait for M15 structure to form after the spike settles.

**Post-news entry (for breaking news like a missile strike):** Wait for the initial spike to exhaust. Then look for M15 structure to form in the news-aligned direction. Never chase the first spike candle.

---

## SECTION 8 — MASTER SCAN

### What It Does
`master_scan.py` manages `watchlist.json` — the live scored list of top instruments. It runs every hour on master scan ticks.

### Scoring System (max 10 points)
- H4 trend confirmed via CHANGE 2: +3 points
- H1 pullback or consolidation at logical entry zone: +2 points
- News catalyst aligned (news_scanner exit code 0): +3 points
- Session match (instrument suits current session): +1 point
- R:R potential ≥ 2:1 based on structure: +1 point

Instruments scoring ≥ 6 enter the watchlist and get monitored every tick during monitoring mode.

### Commands
```bash
python3 master_scan.py clear          # clear watchlist at start of master scan
python3 master_scan.py add \
  --symbol XAUUSD --score 9 --direction long \
  --reason "H4 confirmed higher low + war escalation catalyst" \
  --entry 3285 --sl 3265 --tp 3325 --category metals
python3 master_scan.py read           # print current watchlist
```

### Scan Order (priority)
1. XAUUSD, XAGUSD, BRENT — always scan
2. EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD — always scan
3. NAS100, SPX500 — scan for awareness (blocked below R8,000 by enforcer)
4. LOCKHEED, NORTHROP, BOEING — only if war_escalation or defense_contract_win active
5. NVIDIA, AMD, MICROSOFT — only if ai_breakthrough or tech_earnings active
6. EXXON, CHEVRON, BP — only if oil_supply_shock active

---

## SECTION 9 — INSTRUMENT UNIVERSE AND SIZING

### XAUUSD (Gold) — Primary Instrument
- **1 unit MAXIMUM. NEVER 3 units.**
- Value: R16/pt per unit
- Minimum SL buffer: 15 pts | Maximum SL: 25 pts
- Pending stop orders do NOT work on XAUUSD — market orders only
- XAUUSD247 (weekend Gold): spreads 8x wider (2.37 vs 0.19) — exceptional setups only

**Why 1 unit maximum:** 3 units at 21pt SL = R1,042+ risk. This was confirmed by a platform screenshot after the May 29 trade placed at 3 units. The enforcer permanently blocks more than 1 unit on Gold.

### Forex (Major)
| Instrument | Max lots | SL range | Value |
|---|---|---|---|
| EURUSD | 0.03L | 15–25 pips | R5.46/pip |
| GBPUSD | 0.03L | 15–25 pips | R5.46/pip |
| USDJPY | 0.03L | 15–25 pips (post-NFP: +50%) | R5.46/pip |
| USDCHF | 0.03L | 15–25 pips | R5.46/pip |
| AUDUSD | 0.03L | 15–25 pips | R5.46/pip |
| NZDUSD | 0.03L | 15–25 pips | R5.46/pip |
| USDCAD | 0.03L | 15–25 pips | R5.46/pip |
| EURGBP | 0.03L | 15–25 pips | R5.46/pip |
| AUDJPY | 0.03L | 15–25 pips | R5.46/pip |
| GBPJPY | 0.03L | 15–30 pips | R5.46/pip |
| GBPAUD | 0.03L | 15–30 pips | R5.46/pip |
| EURJPY | 0.03L | 15–25 pips | R5.46/pip |

### Silver
| Instrument | Max lots | SL range | Notes |
|---|---|---|---|
| XAGUSD | 0.03L | 15–25 pips | Treat as micro Forex, 0.01L intraday |

### Oil
| Instrument | Max lots | SL range | Notes |
|---|---|---|---|
| BRENT | 0.03L | $0.10–$5.00 | Oil supply shock or geopolitical catalyst required |

### Indices — BLOCKED until R8,000
| Instrument | Min balance | Min SL | Max SL |
|---|---|---|---|
| NAS100 | R8,000 | 80 pts | 150 pts |
| SPX500 | R8,000 | 80 pts | 150 pts |
| US30 | R8,000 | 80 pts | 150 pts |
| UK100 | R8,000 | 80 pts | 150 pts |
| GER40 | R5,000 | 80 pts | 150 pts (avoid overnight — wide spread) |

**Why blocked:** On June 11 with a R2,249 account, NAS100 with a 168pt "textbook" SL = R3,024 risk = 134% of account. The enforcer now hard-blocks all indices below R8,000.

### Swing Stocks — All swing-only, always use `--swing` flag on enforcer
| Category | Instruments | Catalyst Required |
|---|---|---|
| Tech | NVIDIA, AMD, APPLE, MICROSOFT, META, AMAZON, TAIWANSEMI | ai_breakthrough or tech_earnings |
| Defense | LOCKHEED, NORTHROP, BOEING | war_escalation or defense_contract_win |
| Energy | EXXON, CHEVRON, BP | oil_supply_shock or earnings |
| Financial | JPMORGAN, GOLDMAN | Fed rate decision or earnings |

Stocks are swing positions only (days, not hours). They do not follow the intraday SL buffer rules but still must pass risk % and R:R checks in the enforcer.

### Permanently Banned — No Exceptions, No Account Size Changes This
- **WTI** — too news/spread driven, no clean structure
- **BTCUSD** — $15 spread, random spikes, no tradeable structure
- **ETHUSD** — same as BTC
- **NGAS** — extreme gap risk

---

## SECTION 10 — SESSION STOP CONDITIONS

Stop the loop immediately when ANY of these are true:

1. **2 consecutive losing trades** this session
2. **Session drawdown exceeds R500** from session-start balance
3. **2 trades placed** this session — quality over quantity. Evidence: Jun 8 had 13 trades and was net negative. Best results come from 1–2 high-quality setups.
4. **36 ticks reached** (3 hours at 5-minute ticks)
5. **Time is outside active session window** (loop auto-stops at 12:00 SAST for London session, 18:00 SAST for London/NY session)
6. **Evan types "stop loop"** or presses Esc

---

## SECTION 11 — SESSION END PROTOCOL

At the end of every session, run this sequence in order:

```bash
# 1. Get closed trades for this session
mcp__claude_ai_claude__get_close_positions

# 2. Calculate session P&L — total of all closed trades

# 3. Append a session summary block to EVAN_TRADING_CONTEXT.md
# Format: Date, balance start/end, trades table (symbol/side/entry/exit/P&L/reason), key lessons

# 4. Run pattern extractor
python session_review.py
# Copy any PATTERNS or WARNINGS it outputs into EVAN_TRADING_CONTEXT.md → Critical Lessons section

# 5. Generate live dashboard
python generate_dashboard.py

# 6. Commit everything to GitHub
git add EVAN_TRADING_CONTEXT.md session_log.jsonl watchlist.json news_impact.json dashboard.html
git commit -m "Session [YYYY-MM-DD] — [P&L] — [N] trades"
git push
```

This is not optional. Every session that does not end with a commit has unarchived lessons. The weekly review loop reads `session_log.jsonl` and `enforcer_audit.jsonl` — if ticks are not logged, the review loop cannot find the patterns.

---

## SECTION 12 — SWING POSITION LOCK PROTOCOL

Any position tagged `[SWING]` in `EVAN_TRADING_CONTEXT.md` has a mandatory lock.

**Do NOT close a swing position without ALL three of:**
1. Evan explicitly says "close the swing position" or "close [symbol] long-term"
2. Claude reads the swing position section aloud in full as a recap before executing the close
3. Evan confirms after hearing the recap

If you encounter these positions open in a new session: do NOT close them. Say: "This appears to be a tagged SWING position. Please review EVAN_TRADING_CONTEXT.md before closing."

This rule exists because swing positions run on a weeks-long thesis. An intraday loop that closes a swing position because it's in the positions list without reading the lock protocol would destroy a deliberately held position.

---

## SECTION 13 — WEEKLY REVIEW LOOP

Run every Monday morning before the first session:

```
Run the weekly trading review. Read EVAN_TRADING_CONTEXT.md fully first.
Then read enforcer_audit.jsonl and session_log.jsonl — all entries since last Monday.

Produce:
1. ENFORCER AUDIT: Every BLOCKED trade — would it have won or lost based on subsequent price action?
2. LOSS ANALYSIS: Every losing trade — H4 trend at entry, which rule was violated, root cause in one sentence.
3. WIN ANALYSIS: Every winning trade — session, instrument, H4 direction, news catalyst, entry type.
4. NEWS ACCURACY: Were news categorizations correct? Did the mapped direction match actual price reaction?
5. PATTERN SUMMARY: Any repeating edge worth adding as a rule? Minimum 3 occurrences.
6. PROGRESS: Current balance vs R5,000 start. % toward R10,000 goal.
7. PROPOSED RULE CHANGES: Specific additions to EVAN_TRADING_CONTEXT.md as a diff.

DO NOT commit. Print the proposed diff and wait for Evan's approval.
DO NOT auto-approve any change to risk sizing, lot limits, or R:R thresholds.
```

---

## SECTION 14 — HISTORICAL LESSONS (WHY EACH RULE EXISTS)

These are the real events behind the rules. If you understand why a rule exists, you will not accidentally bypass it.

**"Gold 1 unit maximum"**
→ On May 29, a trade was placed at 3 units. A screenshot from the platform showed 3 units = R48/pt = R1,042 SL risk on a 21-point stop. The account at the time was R2,000. That is 52% of account risk on a single trade. Enforcer now hard-blocks >1 unit on Gold permanently.

**"Never trail SL to breakeven"**
→ Lost R73 on an XAUUSD short. SL was placed at breakeven with a 4pt buffer on a 25pt-noise instrument. Gold hit the stop then continued in the original direction. The lesson: SLs at breakeven get hit by spread noise and stop hunts before the move resumes. Always trail to structural levels with proper buffer.

**"The enforcer cannot be bypassed"**
→ June 11, 2026. Evan said "ignore the enforcer." Claude complied. Session started at R2,657. Ended at ~R500. Net loss R2,157 in a single session — worst session on record. Every loss was caused by a trade the enforcer would have blocked (oversized SL, counter-trend entry, indices on a small account). The enforcer is now a script with sys.exit(1). A text rule can be overridden. A program cannot.

**"Never trade NAS100/SPX500 below R8,000"**
→ June 11: NAS100 Buy at 28,848, SL 168pts wide. At 0.01L, NAS100 = ~R1.30/pt. But at 1 unit (the sizing used), the SL = R3,024 risk on a R2,249 account. 134% of account in a single trade. The instrument rule was right there in the context file. It was ignored.

**"SL trailing uses closing prices only, not bar extremes"**
→ June 23: Tightened a Gold SL from 4,126 to 4,120 using the low of a volatile spike bar (4,105 from a 9-point pin). The stop was hit within 2 candles. The low was not a structural swing low — it was a volatility wick. Real swing lows are confirmed by closing prices, not wicks.

**"Asian session: no trading"**
→ Checked across every session since May 29. Zero profitable trades ever placed or even identified as valid setups during Asian hours. The evidence is complete. There is no edge in the Asian session at this stage.

**"Maximum 2 trades per session"**
→ June 8 had 13 trades across live and demo accounts. The day was net negative. All 5 consistently profitable sessions (May 29 – June 5) involved 1–2 trades placed per session, held with discipline. Overtrading destroys edge.

**"Post-NFP pairs need 50% wider SLs for the next 2 London sessions"**
→ June 8: USDJPY Buy with normal SL on the Monday after a massive NFP beat. USDJPY retraced hard during London on Monday as the NFP spike unwound. Normal SLs get hit on this retracement. Post-NFP Monday volatility is 1.5–2x normal on JPY pairs.

**"Do not enter pre-blackout unless momentum is very strong"**
→ June 15: Two trades entered within 45 minutes of the platform maintenance window. Both were stopped by choppy pre-blackout price action. Neither would have been entered with normal session time available.

---

## SECTION 15 — FILE STRUCTURE REFERENCE

```
tradeloop/
├── CLAUDE.md                  ← Auto-loaded by Claude Code at startup. Contains MCP config + loop protocol.
├── EVAN_TRADING_CONTEXT.md    ← The brain. All rules, history, lessons, swing positions. NEVER delete content.
├── SYSTEM_GUIDE.md            ← This file. Kickstarter guide for new Claude models.
├── LOOP_SETUP.md              ← Exact /loop commands to paste for each session. Read this to start.
├── knowledge/
│   ├── RULES.md               ← Quick reference: all rules + CHANGES in one table
│   ├── instruments/           ← Per-instrument profiles (XAUUSD.md, FOREX.md)
│   ├── lessons/               ← Named lessons (range_trap.md, sl_trailing.md, enforcer_bypass.md)
│   └── sessions/              ← Auto-written session summaries by session_review.py
├── enforcer.py                ← Deterministic pre-trade gate. exit 0 = PASS, exit 1 = BLOCKED.
├── session_logger.py          ← Every tick gets logged → session_log.jsonl
├── master_scan.py             ← Hourly full instrument scan → watchlist.json
├── news_scanner.py            ← News event management → news_impact.json (exit 0/1/2)
├── tick_lock.py               ← Lock file manager — prevents parallel tick execution
├── session_start_hook.py      ← Auto-runs at session open, injects context
├── session_review.py          ← Post-session pattern extractor → knowledge/sessions/
├── generate_dashboard.py      ← Generates dashboard.html — open in browser for live view
├── enforcer_audit.jsonl       ← Every enforcer check (pass and fail) — never delete
├── session_log.jsonl          ← Every tick logged — never delete
├── watchlist.json             ← Live top-10 scored instruments
├── news_impact.json           ← Active news events state
├── session_state.json         ← H4 trends, key levels, loop state
└── dashboard.html             ← Open in browser for live session dashboard
```

---

## SECTION 16 — STARTING A SESSION (STEP BY STEP)

This is what you do at the start of every session. Do not improvise.

**At 08:45 SAST (for London session) or 14:45 SAST (for London/NY session):**

1. Verify you are in the correct directory (`tradeloop/`)
2. Confirm the demo account: `mcp__claude_ai_claude__switch_trading_account` → #41829612
3. Check existing open positions: `mcp__claude_ai_claude__get_open_positions`
4. If any SWING-tagged positions are open, note them and leave them alone
5. Read `watchlist.json` — are there any setups carrying over from the previous session?
6. Paste the `/loop 5m` command from `LOOP_SETUP.md` for the appropriate session

The exact commands to paste are in `LOOP_SETUP.md`. Use that file — it has the full tick protocol wired in and is kept current.

---

## SECTION 17 — WHAT GOOD LOOKS LIKE

A successful tick where no trade is placed looks like this:

```
[09:15 SAST] — LONDON
Tick 3 — MONITORING MODE

Account: #41829612 | Balance: R5,118 | Equity: R5,118 | No open positions

WATCHLIST (from master_scan.py):
1. XAUUSD Short — score 8 — entry zone 4,095–4,105 — SL above 4,125 — TP 4,055
2. GBPUSD Short — score 7 — entry zone 1.2840–1.2850 — SL above 1.2875 — TP 1.2790

PRICE CHECKS:
XAUUSD current: 4,135 — not in entry zone (need pullback to 4,105)
GBPUSD current: 1.2862 — not in entry zone

M15 TRIGGERS:
XAUUSD: no trigger — waiting for lower high to form at ~4,115 then break below it
GBPUSD: no trigger — price above entry zone

ACTION: Hold. Watching for XAUUSD pullback to 4,105 and M15 lower high trigger.
NEXT TRIGGER: XAUUSD M15 lower high forms below 4,115 then breaks below its low.

This tick succeeds because: both setups are live and monitored, triggers have not fired, no premature entry was made.

[SESSION_LOGGER called]
```

A tick that does nothing because nothing should happen is a PASS. Not a failure.

---

## SECTION 18 — WHAT BAD LOOKS LIKE (DO NOT DO THESE)

1. Placing a trade because "price looks like it's going up" without H4 confirmation
2. Running the enforcer and getting exit code 1, then adjusting the numbers and re-running to force a PASS
3. Saying "I'll trail the SL just in case" without a new structural swing point to trail to
4. Entering a trade 10 minutes before a high-impact news event because "the setup looks strong"
5. Placing a 3rd trade in a session after 2 trades have already been placed
6. Continuing to trade after 2 consecutive losing trades have been recorded
7. Closing a SWING-tagged position without the full lock protocol
8. Answering "what time is it?" by asking Evan — always check from market data
9. Using a bar extreme (wick low) as the reference for trailing a SL instead of closing price
10. Placing a Gold trade with anything other than 1 unit

---

## SECTION 19 — CURRENT SYSTEM GOALS AND STATUS (as of June 24, 2026)

- Primary account: Demo #41829612 | Target: R5,000 → R10,000
- Timeline: 3–4 weeks at 2 sessions/day, 5 days/week
- Current R:R targets: XAUUSD minimum 1.5:1 | Forex minimum 1.3:1 | Preferred: 2:1+ only
- Maximum simultaneous trades: 2 (until balance reaches R7,500)
- Do NOT increase lot sizes until R8,000+ confirmed
- Indices unlock at R8,000

The system has demonstrated real edge during the winning period (May 29 – June 5: +R2,297 across 7 trades). Every loss in the subsequent period was traceable to a specific rule violation — counter-trend entry, enforcer bypass, oversized indices. The edge is real when the rules are followed.

---

## FINAL NOTE FROM EVAN

If you are a Claude model reading this for the first time: the rules are not bureaucracy. Each one is written in the ZAR cost of the lesson that created it. The enforcer bypass on June 11 cost me R2,157 in a single session. The Gold 3-unit rule was confirmed by a screenshot that showed what 3 units actually costs. The H4 trend gate was written the morning after I realized every loss from June 8–11 was a counter-trend long inside a clear downtrend.

Follow the rules. Block the trades that should be blocked. Let the winners run within the rules. The system works when you trust it.

When in doubt: run the enforcer. If it blocks, the answer is no. If it passes, state your H4 assumption, confirm the M15 trigger fired, and place the trade.

Make money. Stay profitable.

— Evan Grobbelaar

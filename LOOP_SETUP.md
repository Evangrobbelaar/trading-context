# FINAL LOOP SETUP FOR CLAUDE MODELS — v3.1
Updated: June 22, 2026 | Account: Demo #41829612 | Goal: R5,000 → R10,000

---

## SHOULD YOU LEAVE IT RUNNING 24/7? NO.

| Period | Evidence | Decision |
|---|---|---|
| Asian 00:00-07:00 SAST | Zero profitable trades across all sessions | Off |
| London 09:00-12:00 SAST | Good setups, second-best session | Run |
| Quiet 12:00-15:00 SAST | Low volume, no clean setups | Off |
| London/NY 15:00-18:00 SAST | Best session — "most of the day's profit" Jun 8 | Run |
| NY-only 18:00-22:00 SAST | Only useful if already in a trade | Off |
| Weekend | Spreads 8x wider, no structure | Off |

---

## v3.1 LOOP ARCHITECTURE

Each session loop runs in two alternating modes:

**MASTER SCAN (Tick 1, tick 13, tick 25 ...)** — runs every hour:
- web_search for breaking news → news_scanner.py set → news_impact.json
- Scan all instruments → master_scan.py scores → watchlist.json (top 10)
- Print: "MASTER SCAN COMPLETE — [N] instruments. Monitoring begins."

**MONITORING (Ticks 2-12, 14-24 ...)** — runs every 5 minutes:
- Read watchlist.json → check prices on top-5 scored instruments
- M15 trigger check on any near-entry setups
- Position monitor if trades open
- Enforcer + order if trigger fires

---

## DAILY ROUTINE

```
08:45 SAST  → Open Claude Code in this directory
             → Start LONDON SESSION (paste command below)
             → Tick 1 = master scan + news
             → Let it run until 12:00

14:45 SAST  → Start LONDON/NY SESSION (paste command below)
             → Tick 1 = master scan + news (watchlist rebuilt fresh)
             → Best session — be available

18:00 SAST  → Loop auto-stops
             → Session summary committed to GitHub
```

---

## SESSION 1 — LONDON OPEN (paste at 08:45 SAST)

```
/loop 5m You are running trading tick [auto-increment starting at 1]. Master rule: make money and stay profitable. Account: demo #41829612.

TICK MODE: If tick number is 1 or divisible by 12 → MASTER SCAN MODE. Otherwise → MONITORING MODE.

MASTER SCAN MODE steps:
1. switch_trading_account to #41829612. Get SAST time from XAUUSD price. Get account info + open positions.
2. python3 news_scanner.py clear. Then web_search "breaking financial news today" + "war news today" + "economic events today" + "Fed news today" + "oil supply news today". Categorize headlines into event keys: war_escalation / peace_talks / ceasefire / missile_strike / sanctions_announced / cpi_hot / cpi_cool / nfp_beat / nfp_miss / fed_hawkish / fed_dovish / oil_supply_shock / tech_earnings_beat / tech_earnings_miss / defense_contract_win / ai_breakthrough / risk_off_generic / risk_on_generic / central_bank_rate_hike / inflation_data_uk_eu. Run: python3 news_scanner.py set --events "[keys]" --headlines "[headline1|headline2]" and add --high_impact_2h if a scheduled high-impact event (CPI, NFP, Fed decision, central bank rate) fires within 2 hours. Then: python3 news_scanner.py read. If high_impact_2h active: DO NOT enter new trades this tick — wait for M15 settlement after print.
3. python3 master_scan.py clear. Scan XAUUSD/XAGUSD/BRENT/EURUSD/GBPUSD/USDJPY/USDCHF/AUDUSD first (always). Then NAS100/SPX500 for awareness (blocked below R8,000). Then defense stocks (LOCKHEED/NORTHROP/BOEING) only if war_escalation or defense_contract_win active. Then tech stocks (NVIDIA/AMD/MICROSOFT) only if ai_breakthrough or tech_earnings active. Then energy stocks (EXXON/CHEVRON/BP) only if oil_supply_shock active. For each: get H4 history (6 candles) → CHANGE 2 trend gate → if passes get H1 (12 candles) → python3 news_scanner.py check --symbol [X] --direction [long/short] (exit 0 = catalyst, exit 1 = neutral, exit 2 = CONFLICT — skip direction) → score → python3 master_scan.py add. Run: python3 master_scan.py read.
4. If open positions: get last 10 M5 + last 6 H4 candles per position → output CHANGE 4 format → apply rules 4/13/14/Change3.
5. python3 session_logger.py [all args].

MONITORING MODE steps:
1. switch_trading_account to #41829612. Get SAST time + account info + open positions.
2. If open positions: get last 10 M5 + 6 H4 → CHANGE 4 format → apply rules.
3. python3 master_scan.py read. For top 5 instruments (score ≥ 6): get current price → if near entry get M15 (8 candles) → check CHANGE 5 trigger.
4. If trigger fires AND fewer than 2 trades placed this session AND no high_impact_2h active: run python3 news_scanner.py volatility --symbol [X] (print warning if high-vol, but do not block). Then run enforcer.py with exact risk_amount/reward_amount/sl_distance. Exit code 0 → create_market_order. Exit code 1 → BLOCKED, do not retry.
5. python3 session_logger.py [all args].

STOP CONDITIONS: 2 trades placed OR 2 consecutive losses OR R500 drawdown OR after 12:00 SAST OR 36 ticks.
SESSION END: get_close_positions → calculate P&L → append summary to EVAN_TRADING_CONTEXT.md → python session_review.py (copy any PATTERNS/WARNINGS to EVAN_TRADING_CONTEXT.md lessons) → python generate_dashboard.py → git add EVAN_TRADING_CONTEXT.md session_log.jsonl watchlist.json news_impact.json dashboard.html && git commit -m "Session [date] [P&L] [N] trades" && git push.
```

---

## SESSION 2 — LONDON/NY OVERLAP (paste at 14:45 SAST) — BEST SESSION

```
/loop 5m You are running trading tick [auto-increment starting at 1]. Master rule: make money and stay profitable. Account: demo #41829612.

TICK MODE: If tick number is 1 or divisible by 12 → MASTER SCAN MODE. Otherwise → MONITORING MODE.

MASTER SCAN MODE steps:
1. switch_trading_account to #41829612. Get SAST time from XAUUSD price. Get account info + open positions.
2. python3 news_scanner.py clear. Then web_search "breaking financial news today" + "war news today" + "economic events today" + "Fed news today" + "oil supply news today". Categorize headlines into event keys: war_escalation / peace_talks / ceasefire / missile_strike / sanctions_announced / cpi_hot / cpi_cool / nfp_beat / nfp_miss / fed_hawkish / fed_dovish / oil_supply_shock / tech_earnings_beat / tech_earnings_miss / defense_contract_win / ai_breakthrough / risk_off_generic / risk_on_generic / central_bank_rate_hike / inflation_data_uk_eu. Run: python3 news_scanner.py set --events "[keys]" --headlines "[headline1|headline2]" and add --high_impact_2h if a scheduled high-impact event (CPI, NFP, Fed decision, central bank rate) fires within 2 hours. Then: python3 news_scanner.py read. If high_impact_2h active: DO NOT enter new trades this tick — wait for M15 settlement after print.
3. python3 master_scan.py clear. Scan XAUUSD/XAGUSD/BRENT/EURUSD/GBPUSD/USDJPY/USDCHF/AUDUSD first (always). Then NAS100/SPX500 for awareness (blocked below R8,000). Then defense stocks (LOCKHEED/NORTHROP/BOEING) only if war_escalation or defense_contract_win active. Then tech stocks (NVIDIA/AMD/MICROSOFT) only if ai_breakthrough or tech_earnings active. Then energy stocks (EXXON/CHEVRON/BP) only if oil_supply_shock active. For each: get H4 history (6 candles) → CHANGE 2 trend gate → if passes get H1 (12 candles) → python3 news_scanner.py check --symbol [X] --direction [long/short] (exit 0 = catalyst, exit 1 = neutral, exit 2 = CONFLICT — skip direction) → score → python3 master_scan.py add. Run: python3 master_scan.py read.
4. If open positions: get last 10 M5 + last 6 H4 candles per position → output CHANGE 4 format → apply rules 4/13/14/Change3.
5. python3 session_logger.py [all args].

MONITORING MODE steps:
1. switch_trading_account to #41829612. Get SAST time + account info + open positions.
2. If open positions: get last 10 M5 + 6 H4 → CHANGE 4 format → apply rules.
3. python3 master_scan.py read. For top 5 instruments (score ≥ 6): get current price → if near entry get M15 (8 candles) → check CHANGE 5 trigger.
4. If trigger fires AND fewer than 2 trades placed this session AND no high_impact_2h active: run python3 news_scanner.py volatility --symbol [X] (print warning if high-vol, but do not block). Then run enforcer.py with exact risk_amount/reward_amount/sl_distance. Exit code 0 → create_market_order. Exit code 1 → BLOCKED, do not retry.
5. python3 session_logger.py [all args].

STOP CONDITIONS: 2 trades placed OR 2 consecutive losses OR R500 drawdown OR after 18:00 SAST OR 36 ticks.
SESSION END: get_close_positions → calculate P&L → append summary to EVAN_TRADING_CONTEXT.md → python session_review.py (copy any PATTERNS/WARNINGS to EVAN_TRADING_CONTEXT.md lessons) → python generate_dashboard.py → git add EVAN_TRADING_CONTEXT.md session_log.jsonl watchlist.json news_impact.json dashboard.html && git commit -m "Session [date] [P&L] [N] trades" && git push.
```

---

## SCALP SESSION — London 09:00–12:00 or London/NY 15:00–18:00 SAST

Scalp loop runs **parallel** to the swing loop. Uses `scalp.lock` (never `tick.lock`).
State file: `c:\Users\evang\OneDrive\Desktop\scalp loop\scalp_state.json`

### Pre-session setup (run once before typing "start scalp loop")
```
# 1. Fetch H1 candles for each instrument via MCP, write scalp_candles_temp.json
# 2. python scalp_levels.py --symbol EURUSD --symbol GBPUSD --symbol XAUUSD --symbol USDJPY
# 3. Check ../tradeloop/news_impact.json — no high_impact_2h block
```

### Start the scalp loop
```
start scalp loop
```
Claude runs 60-second ticks: acquire `scalp.lock` → check prices → `scalp_monitor.py` → if AT_LEVEL fetch M5 → enforcer → order → release lock → `ScheduleWakeup 60s`.

### Scalp stop conditions (auto)
- 2 consecutive scalp losses
- 3 scalp trades placed this session
- Session drawdown > R200
- `high_impact_within_2h = true` in news_impact.json
- Outside London 09:00–12:00 or London/NY 15:00–18:00 SAST

### Scalp sizing
| Instrument | Lots | SL | Risk ZAR | TP | Reward ZAR | R:R |
|---|---|---|---|---|---|---|
| EURUSD | 0.03L | 5pip | R27 | 10pip | R55 | 2:1 |
| GBPUSD | 0.03L | 5pip | R27 | 10pip | R55 | 2:1 |
| USDJPY | 0.03L | 5pip | R27 | 10pip | R55 | 2:1 |
| XAUUSD | 0.5u | 6pt | R48 | 12pt | R96 | 2:1 |

Min scalp risk: R27 | Max scalp risk: R100 per trade | Time stop: 20 minutes

### Session end
```
python session_review.py   # includes scalp_log.jsonl analysis automatically
python generate_dashboard.py  # SCALP STATUS card appears if scalp_state.json exists
```

---

## WEEKLY REVIEW (every Monday, paste before first session)

```
Run the weekly trading review. Read EVAN_TRADING_CONTEXT.md fully first.
Then read enforcer_audit.jsonl and session_log.jsonl — all entries since last Monday.

Produce:
1. ENFORCER AUDIT: Every BLOCKED trade — would it have won or lost based on subsequent price action?
2. LOSS ANALYSIS: Every losing trade — H4 trend at entry, which rule was violated, root cause in one sentence.
3. WIN ANALYSIS: Every winning trade — session, instrument, H4 direction, news catalyst, entry type.
4. NEWS ACCURACY: Were news categorizations correct? Did the mapped direction match actual price reaction?
5. PATTERN SUMMARY: Any repeating edge worth adding as a rule? Min 3 occurrences.
6. PROGRESS: Current balance vs R5,000 start. % toward R10,000 goal.
7. PROPOSED RULE CHANGES: Specific additions to EVAN_TRADING_CONTEXT.md as a diff.

DO NOT commit. Print the proposed diff and wait for Evan's approval.
DO NOT auto-approve any change to risk sizing, lot limits, or R:R thresholds.
```

---

## R5,000 SIZING REFERENCE

| Instrument | Size | Value/unit | 20pt/pip SL | % of R5,000 |
|---|---|---|---|---|
| XAUUSD | 1 unit | R16/pt | R320 | 6.4% |
| GBPUSD | 0.03L | R5.46/pip | R109 | 2.2% |
| EURUSD | 0.03L | R5.46/pip | R109 | 2.2% |
| XAGUSD | 0.01L | ~R3.60/pip | R72 | 1.4% |
| BRENT | 0.03L | ~R5/pt | R150 (30pt SL) | 3.0% |
| NAS100 | BLOCKED | — | blocked <R8,000 | — |
| Defense/Tech stocks | swing only | varies | enforcer checks | varies |

Max risk per trade: R1,000 (20%). Max simultaneous trades: 2.

---

## NEWS INSTRUMENT QUICK REFERENCE

| News event | Go long | Go short |
|---|---|---|
| war_escalation | XAUUSD, XAGUSD, USDCHF, LOCKHEED, NORTHROP, BOEING | EURUSD, GBPUSD, EURJPY, NAS100, SPX500 |
| peace_talks | EURUSD, GBPUSD, NAS100, SPX500, BRENT | XAUUSD, USDCHF |
| ceasefire | EURUSD, GBPUSD, NAS100 | XAUUSD, LOCKHEED, NORTHROP |
| missile_strike | XAUUSD, XAGUSD, USDCHF, LOCKHEED, BRENT | EURUSD, GBPUSD, NAS100 |
| sanctions_announced | XAUUSD, BRENT, EXXON, CHEVRON | — |
| cpi_hot | USDJPY, USDCHF, USDCAD | XAUUSD, EURUSD, GBPUSD, NAS100 |
| cpi_cool | XAUUSD, EURUSD, GBPUSD, NAS100 | USDJPY, USDCAD |
| nfp_beat | USDJPY, USDCAD, USDCHF | XAUUSD, EURUSD, GBPUSD |
| nfp_miss | XAUUSD, EURUSD, GBPUSD | USDJPY, USDCAD |
| fed_hawkish | USDJPY, USDCHF, USDCAD | XAUUSD, EURUSD, GBPUSD, NAS100 |
| fed_dovish | XAUUSD, EURUSD, GBPUSD, NAS100 | USDJPY, USDCAD |
| oil_supply_shock | BRENT, EXXON, CHEVRON, BP, USDCAD | EURUSD, GBPUSD, AUDUSD |
| ai_breakthrough | NVIDIA, AMD, MICROSOFT, NAS100 | — |
| tech_earnings_beat | NAS100 + reporting stock | — |
| tech_earnings_miss | — | NAS100 + reporting stock |
| defense_contract_win | LOCKHEED, NORTHROP, BOEING | — |
| risk_off_generic | XAUUSD, USDCHF, USDJPY | EURUSD, GBPUSD, NAS100, AUDUSD |
| risk_on_generic | EURUSD, GBPUSD, NAS100, AUDUSD | XAUUSD, USDCHF |
| central_bank_rate_hike | hiking-currency pairs | inverse pairs |
| inflation_data_uk_eu | map to cpi_hot/cpi_cool for GBP/EUR | — |

Remember: news direction must ALIGN with H4 trend. Counter-trend news = still blocked.
news_scanner.py check exit code 2 = CONFLICT = skip that direction entirely.

---

## NEWS SCANNER EXIT CODE REFERENCE

| Exit code | Meaning | Action |
|---|---|---|
| 0 | CATALYST — news supports direction | +3 score, proceed |
| 1 | NEUTRAL — no catalyst, not blocked | +0 score, proceed on technicals |
| 2 | CONFLICT — news against direction | Skip this direction, do not trade |

---

## HIGH VOLATILITY ON NEWS (from news_scanner.py volatility)

| Instrument | Warning |
|---|---|
| XAUUSD | Gold spikes 30-60pts in seconds on major news. DO NOT enter during spike. |
| USDJPY | JPY gaps on BoJ surprise decisions. |
| GBPUSD | Cable volatile on UK CPI/BOE decisions. |
| NAS100 | Tech index spikes on Fed and earnings. |
| BRENT | Oil gaps on OPEC and geopolitical supply news. |

Run `python3 news_scanner.py volatility --symbol [X]` before each entry near a news event.

---

## ENFORCER QUICK REFERENCE

```bash
# Gold (1 unit — max)
python3 enforcer.py --instrument XAUUSD --direction buy --units 1 \
  --balance 5000 --account demo \
  --risk_amount [sl_pts x 16] --reward_amount [tp_pts x 16] --sl_distance [pts]

# Forex
python3 enforcer.py --instrument GBPUSD --direction sell --lots 0.03 \
  --balance 5000 --account demo \
  --risk_amount [sl_pips x 5.46] --reward_amount [tp_pips x 5.46] --sl_distance [pips]

# Swing stock
python3 enforcer.py --instrument NVIDIA --direction buy --lots 0.1 \
  --balance 5000 --account demo \
  --risk_amount [ZAR] --reward_amount [ZAR] --sl_distance [pts] --swing

# News scanner commands
python3 news_scanner.py set --events "war_escalation,fed_hawkish" --headlines "headline1|headline2"
python3 news_scanner.py set --events "cpi_hot" --headlines "CPI beats at 4.2%" --high_impact_2h
python3 news_scanner.py read
python3 news_scanner.py check --symbol XAUUSD --direction long
python3 news_scanner.py volatility --symbol XAUUSD
python3 news_scanner.py events   # list all known event keys

# Review logs
python3 session_logger.py summary
python3 master_scan.py read
python3 news_scanner.py read
```

---

## STOP THE LOOP
- Type: `stop loop`
- Or press Esc
- Or let session time condition trigger automatically

---

## FILE STRUCTURE
```
tradeloop/
├── CLAUDE.md                  ← auto-loaded on Claude Code startup
├── EVAN_TRADING_CONTEXT.md    ← brain — v3.0, grows every session
├── enforcer.py                ← deterministic gate (exit 0/1)
├── session_logger.py          ← tick logger → session_log.jsonl
├── master_scan.py             ← hourly full scan → watchlist.json
├── news_scanner.py            ← news → news_impact.json (exit 0/1/2)
├── tick_lock.py               ← lock file manager (tick.lock / scalp.lock)
├── session_start_hook.py      ← auto-injects context at every session open
├── session_review.py          ← post-session pattern extractor
├── generate_dashboard.py      ← live dashboard → dashboard.html
├── LOOP_SETUP.md              ← this file
├── enforcer_audit.jsonl       ← every enforcer check
├── session_log.jsonl          ← every tick
├── watchlist.json             ← top-10 instruments this hour
├── news_impact.json           ← active news events
├── session_state.json         ← H4 trends, key levels, loop state
├── dashboard.html             ← open in browser for live view
└── knowledge/
    ├── RULES.md               ← all rules + CHANGES quick reference
    ├── instruments/           ← XAUUSD.md, FOREX.md
    ├── lessons/               ← range_trap.md, sl_trailing.md, enforcer_bypass.md
    └── sessions/              ← YYYY-MM-DD.md (auto-written by session_review.py)
```

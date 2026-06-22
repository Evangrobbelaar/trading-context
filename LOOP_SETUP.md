# LOOP SETUP v3.0 — News Trading + Master Scan Architecture
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

## v3.0 LOOP ARCHITECTURE

Each session loop runs in two alternating modes:

**MASTER SCAN (Tick 1, tick 13, tick 25 ...)** — runs every hour:
- web_search for breaking news → news_scanner.py
- Scan all 139 instruments → master_scan.py scores → watchlist.json (top 10)
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
2. python3 news_scanner.py clear. Then web_search "breaking financial news today" + "war news today" + "economic events today". Categorize into event keys (war_escalation/peace_talks/ceasefire/missile_strike/cpi_hot/cpi_cool/nfp_beat/nfp_miss/fed_hawkish/fed_dovish/oil_supply_shock/tech_earnings_beat/tech_earnings_miss/defense_contract_win/ai_breakthrough/risk_off_generic/risk_on_generic). Run: python3 news_scanner.py set --events "[keys]" --headlines "[summary]" and add --high_impact_2h if major scheduled event within 2 hours. If high_impact_2h: skip new trades this tick.
3. python3 master_scan.py clear. Scan XAUUSD/XAGUSD/BRENT/EURUSD/GBPUSD/USDJPY/USDCHF/AUDUSD first (always). Then defense stocks only if war_escalation active. Then tech stocks only if ai_breakthrough or tech_earnings active. For each: get H4 history (6 candles) → CHANGE 2 trend gate → if passes get H1 (12 candles) → check news_scanner.py check → score → python3 master_scan.py add. Run: python3 master_scan.py read.
4. If open positions: get last 10 M5 + last 6 H4 candles per position → output CHANGE 4 format → apply rules 4/13/14/Change3.
5. python3 session_logger.py [all args].

MONITORING MODE steps:
1. switch_trading_account to #41829612. Get SAST time + account info + open positions.
2. If open positions: get last 10 M5 + 6 H4 → CHANGE 4 format → apply rules.
3. python3 master_scan.py read. For top 5 instruments (score ≥ 6): get current price → if near entry get M15 (8 candles) → check CHANGE 5 trigger.
4. If trigger fires AND fewer than 2 trades placed this session AND no high_impact_2h active: run enforcer.py with exact risk_amount/reward_amount/sl_distance. Exit code 0 → create_market_order. Exit code 1 → BLOCKED, do not retry.
5. python3 session_logger.py [all args].

STOP CONDITIONS: 2 trades placed OR 2 consecutive losses OR R500 drawdown OR after 12:00 SAST OR 36 ticks.
SESSION END: get_close_positions → calculate P&L → append summary to EVAN_TRADING_CONTEXT.md → git add EVAN_TRADING_CONTEXT.md session_log.jsonl watchlist.json news_impact.json && git commit -m "Session [date] [P&L] [N] trades" && git push.
```

---

## SESSION 2 — LONDON/NY OVERLAP (paste at 14:45 SAST) — BEST SESSION

```
/loop 5m You are running trading tick [auto-increment starting at 1]. Master rule: make money and stay profitable. Account: demo #41829612.

TICK MODE: If tick number is 1 or divisible by 12 → MASTER SCAN MODE. Otherwise → MONITORING MODE.

MASTER SCAN MODE steps:
1. switch_trading_account to #41829612. Get SAST time from XAUUSD price. Get account info + open positions.
2. python3 news_scanner.py clear. Then web_search "breaking financial news today" + "war news today" + "economic events today". Categorize into event keys (war_escalation/peace_talks/ceasefire/missile_strike/cpi_hot/cpi_cool/nfp_beat/nfp_miss/fed_hawkish/fed_dovish/oil_supply_shock/tech_earnings_beat/tech_earnings_miss/defense_contract_win/ai_breakthrough/risk_off_generic/risk_on_generic). Run: python3 news_scanner.py set --events "[keys]" --headlines "[summary]" and add --high_impact_2h if major scheduled event within 2 hours. If high_impact_2h: skip new trades this tick.
3. python3 master_scan.py clear. Scan XAUUSD/XAGUSD/BRENT/EURUSD/GBPUSD/USDJPY/USDCHF/AUDUSD first (always). Then defense stocks only if war_escalation active. Then tech stocks only if ai_breakthrough or tech_earnings active. For each: get H4 history (6 candles) → CHANGE 2 trend gate → if passes get H1 (12 candles) → check news_scanner.py check → score → python3 master_scan.py add. Run: python3 master_scan.py read.
4. If open positions: get last 10 M5 + last 6 H4 candles per position → output CHANGE 4 format → apply rules 4/13/14/Change3.
5. python3 session_logger.py [all args].

MONITORING MODE steps:
1. switch_trading_account to #41829612. Get SAST time + account info + open positions.
2. If open positions: get last 10 M5 + 6 H4 → CHANGE 4 format → apply rules.
3. python3 master_scan.py read. For top 5 instruments (score ≥ 6): get current price → if near entry get M15 (8 candles) → check CHANGE 5 trigger.
4. If trigger fires AND fewer than 2 trades placed this session AND no high_impact_2h active: run enforcer.py with exact risk_amount/reward_amount/sl_distance. Exit code 0 → create_market_order. Exit code 1 → BLOCKED, do not retry.
5. python3 session_logger.py [all args].

STOP CONDITIONS: 2 trades placed OR 2 consecutive losses OR R500 drawdown OR after 18:00 SAST OR 36 ticks.
SESSION END: get_close_positions → calculate P&L → append summary to EVAN_TRADING_CONTEXT.md → git add EVAN_TRADING_CONTEXT.md session_log.jsonl watchlist.json news_impact.json && git commit -m "Session [date] [P&L] [N] trades" && git push.
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
| war_escalation | XAUUSD, XAGUSD, LOCKHEED, NORTHROP | EURUSD, GBPUSD, NAS100 |
| ceasefire | EURUSD, GBPUSD, NAS100 | XAUUSD, LOCKHEED |
| missile_strike | XAUUSD, BRENT | EURUSD, NAS100 |
| cpi_hot | USDJPY, USDCHF | XAUUSD, EURUSD, NAS100 |
| cpi_cool | XAUUSD, EURUSD, NAS100 | USDJPY |
| fed_hawkish | USDJPY, USDCHF | XAUUSD, EURUSD, NAS100 |
| fed_dovish | XAUUSD, EURUSD, NAS100 | USDJPY |
| oil_supply_shock | BRENT, EXXON, CHEVRON | EURUSD |
| ai_breakthrough | NVIDIA, AMD, NAS100 | — |

Remember: news direction must ALIGN with H4 trend. Counter-trend news = still blocked.

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
├── enforcer.py                ← deterministic gate (v2.0 + new instruments)
├── session_logger.py          ← tick logger → session_log.jsonl
├── master_scan.py             ← hourly full scan → watchlist.json
├── news_scanner.py            ← news → news_impact.json
├── LOOP_SETUP.md              ← this file
├── enforcer_audit.jsonl       ← every enforcer check
├── session_log.jsonl          ← every tick
├── watchlist.json             ← top-10 instruments this hour
└── news_impact.json           ← active news events
```

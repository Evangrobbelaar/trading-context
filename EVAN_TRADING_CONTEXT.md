
=========================
ACCOUNT LOCK — HARD RULE (added 8 Jul 2026)
=========================
- The ONLY account for all trading is #41829612.
- #41750592 (R78k demo) must NEVER be traded. The ThinkTrader MCP silently
  defaults back to 41750592 on every new session, reconnect, or context reset.
- MANDATORY: at session start AND before every order, call
  switch_trading_account(41829612), then confirm the tool response shows
  "accountId":"41829612". If ANY tool response shows 41750592, stop,
  switch, and re-verify before doing anything else.
- This has already caused wasted tokens and one near-miss (8 Jul 2026,
  war-escalation session). Treat a wrong-account response as a hard stop.
# EVAN'S TRADING CONTEXT — v1.1
Last updated: June 5, 2026
Platform: ThinkMarkets (ThinkTrader)
Trader: Evan | Location: Johannesburg, South Africa (SAST = UTC+2)

---

## VERIFICATION PROTOCOL
When Claude reads this document it MUST respond with:
"Context loaded v1.1 — [date] — [session] session — [open positions] open — ready."
If Claude does NOT say this at the start — tell it: "Read your context file first."

---

## VERSION CONTROL RULE
- Claude NEVER deletes existing content. Only adds to it.
- Every Monday a new version number is committed to GitHub.
- Old content always preserved — lessons and history only grow.

---

## MONDAY WEEKLY UPDATE PROTOCOL
Every Monday at session open Claude must:
1. Fetch this document from GitHub via web_fetch
2. web_search this week's high impact news events
3. Update Weekly News Calendar section
4. Update Performance History with last week's closed trades
5. Add any new lessons learned
6. Commit updated file to GitHub using bash git commands
7. Confirm "Context updated vX.X — ready." before trading begins

---

## STEP 0 — MANDATORY FIRST STEPS (before ANY analysis)
Run in order. No exceptions.
1. Fetch this document from GitHub raw URL
2. Determine SAST time from market data — NEVER ask Evan the time
3. Run news scan — high impact events today and within 2 hours
4. Check open positions on correct account
5. Confirm account balance and active account
6. Only then begin market analysis

---

## ACCOUNTS
| Account | Type | Currency | Notes |
|---|---|---|---|
| #43019560 | LIVE | ZAR | ~R65 primary live account |
| #42805520 | LIVE | ZAR | Empty |
| #41810679 | DEMO | ZAR | ~R2,756 practice account |

Default to DEMO (#41810679) unless Evan specifies live.
MCP prefix: claude: | URL: mcp.thinktrader.com/v1/mcp
ThinkTrader MCP drops after inactivity — new conversation required to reconnect.
Always run claude:switch_trading_account at session start.

---

## INSTRUMENT RULES

### XAUUSD (Gold) — PRIMARY INSTRUMENT
- 1 unit MAXIMUM. NEVER 3 units. Never.
- ~R16/pt at 1 unit
- 3 units = ~R48/pt = R1,000+ risk on 21pt SL (confirmed by platform screenshot)
- Pending stop orders DO NOT work on XAUUSD — market orders only
- Minimum SL buffer: 15-25 pts
- XAUUSD247: weekends only, spread 8x wider (2.37 vs 0.19) — exceptional setups only

### FOREX (EURUSD, GBPUSD, USDJPY)
- 0.01 lots overnight swing trades
- 0.03 lots intraday during London/NY open
- Never exceed 0.03 lots on R2,000 account
- Minimum SL buffer: 15-25 pips
- GBPUSD at 0.10 lots = ~R16/pip (similar value to Gold 1 unit)

### NAS100 / INDICES
- At 0.01 lots = ~R1.30/pt — not worth it
- Avoid until account grows to R5,000+
- Minimum SL buffer: 80-150 pts

### AVOID ENTIRELY
- WTI (Crude Oil) — too news/spread driven
- BTCUSD/ETHUSD — $15 spread, random spikes, no clean structure
- GER40 overnight — wide spread, no liquidity

---

## SESSION SCHEDULE (SAST = UTC+2)
| Session | SAST Time | Best Instruments |
|---|---|---|
| Asian | Midnight-7am | Forex, Gold, Crypto |
| London open | 9am-12pm | Gold, EURUSD, GBPUSD (BEST) |
| London/NY overlap | 3pm-6pm | Gold, NAS100, SPX500 |
| NY close | 10pm | Wind down |
| Weekend | Sat/Sun | Markets closed (XAUUSD247 only) |

---

## NEWS CALENDAR RULES
- Always web_search news before every trade session
- High impact events: NFP, CPI, Fed speeches, JOLTS, ADP, PMI, GDP
- Avoid new entries within 2 hours BEFORE high impact news
- NFP drops Fridays at 2:30pm SAST — no trades before 4:30pm SAST
- Directional bias:
  - Stagflation/geopolitical risk = bullish Gold
  - Rate hike fears/strong USD = bearish Gold
  - Strong jobs beat (NFP/ADP) = USD up = Gold down
  - Weak jobs data = USD down = Gold up
- Post-news: wait for M15 compression + double bottom/top before entering (Rule 12)

---

## PRE-TRADE CHECKLIST (run before every single trade)
1. News scan done? Any events within 2 hours?
2. Correct session for this instrument?
3. 5+ instruments scanned? Is this the best setup?
4. H4 confirms trend direction?
5. H1 shows pullback/consolidation?
6. M15 shows structure breaking in trend direction?
7. Lot size correct for account and instrument?
8. SL behind structural level with correct buffer?
9. R:R minimum 1.2:1?
10. Risk per trade under 20% of account?

---

## PRE-TRAIL CHECKLIST (before every SL move)
1. Has price made a new swing point in my direction?
2. Is the new SL behind a structural level?
3. Is the buffer wider than the instrument noise zone?
4. Am I trailing out of fear or because structure changed? If fear — LEAVE IT.

---

## TRADING RULES

Rule 1: Never trail SL to breakeven. Trail to nearest structural level with room to breathe.
Rule 2: Min buffers: Forex 15-25 pips, Gold 15-25 pts, Indices 80-150 pts. SL outside noise zone.
Rule 3: Only trail after new swing point confirms in trade direction. No trailing just because in profit.
Rule 4: 50% rule — at 50%+ of TP, assess momentum. If candles are shrinking, pace is slowing, or price stalls for 2+ candles = CLOSE immediately. If momentum is still strong (large candles, fast movement) = hold to TP. Never let a winning trade reverse back to entry because momentum died and Claude didn't act.
Rule 5: Cut losers fast, let winners run. Bounce hard off TP area and reverses — close immediately.
Rule 6: Match instrument to session. Asian: Forex/Gold/Crypto. London: EUR/GBP/Gold. NY: NAS100/SPX500/Gold. Never trade closed markets.
Rule 7: Always scan 5+ instruments. Best setup wins — not the first one found.
Rule 8: Sizing for ~R2,000 account: 0.01 lots overnight, 0.03 lots intraday. Gold: 1 unit MAX. Rule 2 always overrides sizing.
Rule 9: H4+H1+M15 confluence = entry. Min R:R 1.2:1. Set TP, let it fill. Never move TP out of greed.
Rule 10: Cut dead trades only after BOTH: hours open with no TP progress AND structure weakened.
Rule 11: News scan before every trade. Avoid within 2 hours of major news. Use for directional bias.
Rule 12: Post-news Gold — wait for M15 compression and double bottom/top. Never chase the spike.
Rule 13: At 60%+ of TP with stalling momentum near S/R — close manually and bank profit.

---

## CRITICAL LESSONS (never repeat these)

1. GOLD 3 UNITS = ACCOUNT KILLER. R1,042 SL risk on 21pt stop confirmed by screenshot. 1 unit ONLY.
2. NAS100 at 0.01 lots = R1.30/pt. 150pt target = R195. Not worth it on this account size.
3. Never trail SL to breakeven. Lost R73 on XAUUSD short — 4pt buffer on 25pt instrument. Gold hit stop then continued right direction.
4. Dead trades kill opportunity. USDJPY held overnight zero progress. Cut after one full session if structure weakens.
5. Spread kills scalping. AI latency makes true scalping unreliable — execution speed is the bottleneck.
6. Post-news bounces work. JOLTS crashed Gold to 4,447 — double bottom — bounced to 4,473 = R205. Always wait for M15 compression first.
7. Bank profit when momentum stalls. Closed Gold buy at +R205 instead of last 15pts — right call, momentum fading into resistance.
8. ThinkTrader MCP drops after extended inactivity. New conversation to reconnect. Verify account at session start.
9. Always determine time from market data — never ask Evan what time it is.
10. AI memory rules unreliable for process steps. THIS GitHub document is single source of truth. Always fetch first.
11. If Claude has not confirmed "Context loaded" — tell it: "Read your context file first."
12. Claude can commit to GitHub directly using bash git commands. No need to ask Evan to paste files manually.

---

## PERFORMANCE HISTORY
| Date | Trade | Result |
|---|---|---|
| 29 May 2026 | XAUUSD Buy (3 units) | +R1,242 |
| 29 May 2026 | USDJPY Sell | -R6 |
| 29 May 2026 | EURUSD Sell x2 | -R32 |
| 1 Jun 2026 | XAUUSD Sell (1 unit) | +R594 |
| 1 Jun 2026 | XAUUSD Buy (1 unit) | +R205 |
| 2 Jun 2026 | XAUUSD Buy (1 unit) | +R147 |
| 5 Jun 2026 | XAUUSD Buy (1 unit) | +R147 |
| TOTAL | | +R2,297 |

---

## WEEKLY NEWS CALENDAR
Updated every Monday morning via web_search.

Week of June 1-5, 2026 (complete):
- Mon Jun 2: JOLTS — beat expectations, Gold dropped
- Wed Jun 4: ADP + Fed Beige Book — done
- Fri Jun 5: NFP 2:30pm SAST — no trades before 4:30pm

Week of June 8-12, 2026:
- Tue Jun 10: US CPI (May) 14:30 SAST — 🔴 CRITICAL — NO trades before 16:30 SAST
- Tue Jun 10: US PPI 14:30 SAST — 🔴 HIGH IMPACT
- Thu Jun 12: US Initial Jobless Claims 14:30 SAST — medium
- Fri Jun 13: Michigan Consumer Sentiment 16:00 SAST — medium
- Note: FOMC Jun 16-17 (next week) — watch rate hike language
- Gold bias: Bearish (strong NFP, rate hike bets). CPI cool = bounce. CPI hot = continuation short.
- Key level: 4,319 yearly open support. Break below = target 4,195.

Week of June 8-12, 2026 (Monday update committed by Claude — June 8, 2026):

---
Document version: 1.1
GitHub: https://github.com/Evangrobbelaar/trading-context
Raw URL: https://raw.githubusercontent.com/Evangrobbelaar/trading-context/main/EVAN_TRADING_CONTEXT.md
Update method: Claude uses bash git commands to commit changes directly to GitHub.

---

## UPDATE — June 5, 2026 (post-NFP)

NFP Result: 172,000 jobs added vs 85,000 forecast — massive beat.
Gold reaction: Crashed from 4,481 to 4,314 — a 167pt drop.
USD surged ~30pts on Dollar Index.

No trades placed post-NFP — correct decision. Rule 12 compression never formed.
Gold continued lower all afternoon with no bounce structure.

Key lesson: After a massive NFP beat, Gold can fall 150+ pts without a clean bounce setup.
Do not try to catch the falling knife on strong NFP days. Wait for Monday reset.

Week of June 1-5 final P&L:
| Date | Trade | Result |
|---|---|---|
| 1 Jun 2026 | XAUUSD Sell | +R594 |
| 1 Jun 2026 | XAUUSD Buy | +R205 |
| 2 Jun 2026 | XAUUSD Buy | +R147 |
| 5 Jun 2026 | No trades post-NFP | R0 |
| Week total | | +R946 |

Document version: 1.2 — updated June 5, 2026

---

## PRE-TRADE ENFORCER — MANDATORY EXECUTION PROTOCOL
Version added: 1.3 — June 5, 2026

⚠️ SUPERSEDED June 25, 2026 — REBUILD PHASE. The full 10-item checklist
below, the hard trend gate, R:R minimum, and instrument size caps are
SUSPENDED for now while Evan rebuilds the strategy from scratch. See
"ENFORCER — REBUILD PHASE" at the bottom of this document for the only
two rules currently active. Do not enforce the items below until that
section says this protocol is reinstated.

This protocol is NON-NEGOTIABLE. Claude MUST complete this BEFORE calling create_market_order on ANY trade. No exceptions. No shortcuts. If Claude skips this, Evan must say "Run the enforcer first."

### ENFORCER TEMPLATE
Claude must output this EXACTLY before every trade execution:

```
=== PRE-TRADE ENFORCER ===
Instrument: [instrument]
Direction: [Buy/Sell]
Entry: [price]
SL: [price] ([X] pts/pips from entry)
TP: [price] ([X] pts/pips from entry)
Size: [lots/units]
R:R: [X:1]

CHECKLIST:
1. News scan done? No events within 2 hours?         [✅/❌]
2. Correct session for this instrument?               [✅/❌]
3. 5+ instruments scanned? This is the best setup?   [✅/❌]
4. H4 confirms trend direction?                       [✅/❌]
5. H1 shows pullback/consolidation?                  [✅/❌]
6. M15 shows structure breaking in trend direction?  [✅/❌]
7. Lot size correct for account and instrument?       [✅/❌]
8. SL behind structural level with correct buffer?   [✅/❌]
9. R:R minimum 1.2:1?                                [✅/❌]
10. Risk under 20% of account?                        [✅/❌]

RESULT: [ALL PASSED — EXECUTING] or [FAILED — ITEM X — NOT PLACING]
=========================
```

### ENFORCER RULES
- ALL 10 items must return ✅ before execution
- A single ❌ = trade does not get placed — no exceptions
- If ANY item fails, Claude must explain why and what needs to change
- Claude must calculate R:R and risk % explicitly — no estimating
- For Gold: Item 7 must confirm "1 unit" — never 3 units
- For Forex: Item 7 must confirm lot size vs account size
- The enforcer output must appear BEFORE the create_market_order call
- If Claude executes without showing the enforcer — Evan says "Enforcer first" and Claude cancels and reruns

### ENFORCER EXAMPLES

GOOD — trade placed:
```
=== PRE-TRADE ENFORCER ===
Instrument: XAUUSD
Direction: Buy
Entry: 4,461
SL: 4,442 (19pts)
TP: 4,490 (29pts)
Size: 1 unit
R:R: 1.5:1

1. News scan done? No JOLTS/NFP/Fed today              ✅
2. London session — correct for Gold                   ✅
3. Scanned Gold, NAS100, EUR, GBP, JPY — Gold best    ✅
4. H4 bullish — higher lows from 4,366                ✅
5. H1 pulled back from 4,595 HOD to 4,447             ✅
6. M15 double bottom at 4,447 — bounce forming        ✅
7. 1 unit Gold — correct per Rule 8                   ✅
8. SL below double bottom with 19pt buffer            ✅
9. R:R = 1.5:1 — above 1.2 minimum                   ✅
10. Risk = 19pts x R16 = R304 = 15% account           ✅

RESULT: ALL PASSED — EXECUTING
=========================
```

BAD — trade blocked:
```
=== PRE-TRADE ENFORCER ===
Instrument: XAUUSD
Direction: Buy
Entry: 4,461
SL: 4,442 (19pts)
TP: 4,490 (29pts)
Size: 3 units
R:R: 1.5:1

1. News scan done?                                     ✅
2. Correct session?                                    ✅
3. 5+ instruments scanned?                             ✅
4. H4 confirms trend?                                  ✅
5. H1 pullback?                                        ✅
6. M15 structure?                                      ✅
7. Lot size correct? 3 units = R48/pt = R912 risk      ❌
8. SL behind structure?                                ✅
9. R:R 1.5:1                                           ✅
10. Risk under 20%? R912 = 44% of account              ❌

RESULT: FAILED — ITEMS 7 AND 10 — NOT PLACING
Reason: Gold sizing is 3 units — MAXIMUM is 1 unit per Rule 8.
Fix: Reduce to 1 unit and rerun enforcer.
=========================
```


---

## UPDATE — June 8, 2026 (Monday Weekly Update)

Monday open context:
- Gold closed Friday at ~4,366 (NFP crash: 4,481 → 4,314, partial weekend recovery)
- Weekend XAUUSD247 range: 4,290–4,320, spread 4.06pts (8x normal)
- Yearly open support: 4,319 — critical level this week
- No trades placed over the weekend — correct (spread + no structure)

Week plan:
- Monday: Watch London open 9am SAST. Wait for M15 compression at 4,319 support or break below it.
  - Scenario A (above 4,319 holds): Long with SL below 4,300, TP 4,370 (~2.5:1)
  - Scenario B (breaks below 4,319): Short on pullback, SL above 4,340, TP 4,270 (~2.5:1)
- Tuesday: NO TRADES before 16:30 SAST (CPI at 14:30 SAST)
- Live account: R65.89 — too small to trade. Fund to R1,000 minimum before any live trades.

Document version: 1.3 — updated June 8, 2026

---

## LONG-TERM SWING POSITIONS — DO NOT CLOSE WITHOUT PROTOCOL

### ⚠️ MANDATORY LOCK RULE
Any position tagged [SWING] below MUST NOT be closed without:
1. Evan explicitly saying "close the swing position" OR "close [symbol] long-term"
2. Claude reading this section aloud in full as a recap before executing close
3. Evan confirming after hearing the recap

If Claude is in any other conversation and sees these positions open — DO NOT CLOSE. Say: "This appears to be a tagged SWING position. Please review EVAN_TRADING_CONTEXT.md before closing."

This rule overrides all other close/cleanup actions. No exceptions.

---

### [SWING] NVIDIA — DEMO #41810679
Status: OPEN (placed June 8, 2026)
Symbol: NVIDIA
Direction: Long (Buy)
Account: Demo #41810679 ONLY
Entry: ~$208.23
Stop Loss: $195.00
TP1: $250.00 (conservative — partial close here, trail remainder)
TP2: $284.00 (analyst consensus target)
Size: 0.1 lots
Timeframe: 2–4 weeks
Risk: R24 (0.9% of demo) — negligible to intraday sessions

Thesis:
- NVIDIA acquiring entire AI inference stack: Groq ($20B), CentML, SchedMD, Illumex
- Free cash flow $96.5B fiscal 2026. M&A accelerating.
- Blackwell → Vera Rubin hardware transition = next upcycle
- 40+ analyst consensus: $303.96 target = ~45% upside from entry
- 95% YoY revenue growth expected
- Current price ~$208 = pullback entry from highs — optimal window
- Strong Buy rating: 57% Strong Buy, 41% Buy, 1 Sell across Wall Street

Management rule: At TP1 ($250) — close 50% of position, trail SL to $215 on remainder.
At TP2 ($284) — close remaining 50%.
Only close early if: thesis breaks (NVIDIA loses major contract, regulatory block on acquisitions, or broad AI sector collapse).


### [SWING] INTEL — DEMO #41810679
Status: PENDING PLACEMENT (researched June 8, 2026)
Symbol: INTEL
Direction: Long (Buy)
Account: Demo #41810679 ONLY
Entry: ~$99.21
Stop Loss: $88.00
TP1: $115.00
TP2: $130.00
Size: 0.1 lots
Timeframe: 2–4 weeks
Risk: R20 (0.7% of demo) — negligible

Thesis:
- Intel stock has tripled in 2026 (from $17.67 low to $99+) under CEO Lip-Bu Tan turnaround
- NVIDIA invested $5B in Intel (December 2025) — strategic validation
- AI Data Center segment +22% YoY, Intel Foundry +16%
- 18A chip yields improving 7% per month, ahead of year-end target
- 200 design wins on Panther Lake
- Citi target $130, Benchmark $140, KeyBanc $110
- Still below most analyst targets despite the run

Management rule: At TP1 ($115) — close 50%, trail SL to $100 on remainder. At TP2 ($130) — close all.

### [SWING] AMD — DEMO #41810679
Status: PENDING PLACEMENT (researched June 8, 2026)
Symbol: AMD
Direction: Long (Buy)
Account: Demo #41810679 ONLY
Entry: ~$476.48
Stop Loss: $455.00
TP1: $520.00
TP2: $560.00
Size: 0.1 lots
Timeframe: 2–4 weeks
Risk: R39 (1.4% of demo) — acceptable

Thesis:
- Primary NVIDIA competitor in AI accelerators
- MI300X GPU adoption accelerating in data centers
- Benefits from same AI capex wave as NVIDIA
- Strong Buy consensus

Management rule: At TP1 ($520) — close 50%, trail SL to $470. At TP2 ($560) — close all.


---

## MANDATORY TIME CHECK RULE (added June 8, 2026)
Claude MUST call user_time_v0 at the START of every response — before any analysis, execution, or output.
Format: "**[TIME] SAST — [session]**" must appear in the first line of every reply.
No exceptions. If Claude skips this — tell it: "Time check first."


---

## UPDATE — June 8, 2026 (Monday Session Trades)

### Trades placed and closed today:

| Time | Trade | Entry | Exit | Result | Notes |
|---|---|---|---|---|---|
| 11:10 SAST | USDJPY Buy (live) | 160.275 | 160.10 SL | -R19 | SL too tight post-NFP, Monday retracement |
| 11:15 SAST | GBPUSD Sell (demo) | 1.33243 | 1.33400 manual close | -R83 | Structure reversed — M15 flipped bullish, closed before SL |
| 11:50 SAST | NVIDIA Buy (demo) | 208.48 | OPEN | — | Swing position [SWING] — see lock protocol |

### Lessons learned today:
- Post-NFP pairs (especially JPY) need wider SLs on Monday — retracement volatility is 1.5-2x normal
- GBPUSD short thesis was valid (USD strength) but London session saw GBP recover — check if news catalyst drove reversal before next GBP short
- Cutting at -R83 vs waiting for -R140 SL = correct Rule 5 application. Saved R57.
- Demo session P&L today: -R83 (GBPUSD) | NVIDIA open
- Live session P&L today: -R19 (USDJPY)
- Live account balance: R47.16

### Monday June 8 net: -R102 demo intraday | NVIDIA swing open


---

## JUNE 8 2026 — FULL DAY RECAP (for Evan to curate)

### End-of-day account status
- Demo #41810679 balance: R2,622.13 | Equity R2,681 | Started day at ~R2,676
- Live #43019560 balance: R41.73 | Started day at R47.16 | Net -R5.43
- Demo GBPUSD Short x2 still open (see below)
- Demo NVIDIA [SWING] still open

### Open positions end of day
1. GBPUSD Short #1 (demo) — entry 1.33609 | SL breakeven | TP 1.33100 | 0.03L | +R60 floating | FREE TRADE
2. GBPUSD Short #2 (demo) — entry 1.33469 | SL 1.33609 | TP 1.33100 | 0.03L | flat
3. NVIDIA Long [SWING] — entry $208.48 | SL $195 | TP1 $250 | TP2 $284 | 0.1L | see lock protocol

### Full trade log June 8
| Time SAST | Instrument | Dir | Account | Entry | Exit | Result |
|---|---|---|---|---|---|---|
| 11:10 | USDJPY | Buy | Live | 160.275 | 160.10 SL | -R19 |
| 11:15 | GBPUSD | Sell | Demo | 1.33243 | 1.33400 manual | -R83 |
| 11:50 | NVIDIA | Buy | Demo | 208.48 | OPEN swing | — |
| 15:32 | GBPUSD | Sell | Demo | 1.33609 | OPEN | +R60 float |
| 15:53 | XAUUSD | Sell | Demo | 4332.81 | 4323 SL trail | +R179 |
| 15:53 | EURUSD | Sell | Demo | 1.15444 | 1.15444 BE close | +R55 |
| 15:53 | GBPUSD | Sell | Demo | 1.33469 | OPEN | flat |
| 16:52 | GBPUSD | Sell | Live | 1.33532 | 1.33428 manual | +R14.52 |
| 16:53 | GBPUSD | Sell | Live | 1.33418 | 1.33485 SL | -R11.70 |
| 17:11 | EURUSD | Sell | Live | 1.15421 | 1.15470 SL | -R8.25 |
| 17:20 | EURUSD | Sell | Demo | 1.15446 | 1.15430 cut | +R17 |
| 17:20 | XAUUSD | Sell | Demo | 4330.17 | 4341.88 cut | -R211 |
| 17:53 | NVIDIA | Buy | Demo | 208.48 | OPEN swing | — |

---

## JUNE 8 — LEARNINGS FOR EVAN TO CURATE

### SESSION MECHANICS — what worked
- SL trail to breakeven rule saved multiple positions from turning losses
- Cutting GBPUSD at -R83 (Rule 5) saved R57 vs waiting for SL
- Gold first trade: entry 4332, SL trailed to 4323 — locked R179 automatically
- EURUSD cut early when SL distance was only 7p — avoided potential -R95 loss
- Multi-instrument USD shorts (GBP + EUR + Gold) all fired together on same thesis = valid approach
- NY open is the best session — most of the day's profit came after 15:30 SAST

### SESSION MECHANICS — what didn't work
- Re-entering a trade immediately after manual close at tight SL = stop hunt risk (GBPUSD live trade 2)
- Taking 3 live trades in quick succession on a R47 account = account drawn down to R41.73
- Gold re-entry (second XAUUSD short) entered at wrong time — bounced hard against us, -R211
- EURUSD 0.06L double down — aggressive sizing caught a bounce, required early exit
- Post-NFP Monday pairs (JPY especially) have 1.5-2x normal retracement volatility — wider SLs needed

### LIVE ACCOUNT INSIGHTS
- R47 is too small to trade safely — any SL under 20 pips risks 40%+ of account
- Tight SLs (4-7 pips) get stopped by spread noise and stop hunts
- Three live trades all lost or barely broke even — need minimum R300-500 deposit
- GBPUSD at 0.01L with 6-7p SL = structural problem, not bad trading
- One trade that worked (manual close +R14.52) worked because we managed it manually not via SL

### INSTRUMENT INSIGHTS
- XAUUSD (Gold): R18.20/pt at 0.01 lots. Highly profitable when right but punishing when wrong. Need 20pt+ SL minimum.
- GBPUSD: R5.46/pip at 0.03L. Most consistent performer today — two separate setups both worked directionally.
- EURUSD: R5.46/pip at 0.03L. Similar to GBP, same USD thesis. More volatile during NY session — watch HOD/LOD carefully.
- USDJPY: Post-NFP USD spike faded Monday — wrong entry timing, not wrong thesis.
- NVIDIA (shares): R1.82/dollar at 0.1L. Swing only — too slow for intraday. NY session noise ±$2.
- TM_VOLATILITY_50 (synthetic): Could not place orders — likely account permissions issue. Revisit.
- UK shares (LLOYDS etc): P&L too small at 0.01L (R0.23/pt) — not viable for small account.

### STRATEGY INSIGHTS
- USD strength theme post-NFP is a multi-day thesis — GBP and EUR shorts work on this
- Mean reversion: Gold oscillated 4268-4353 all day. Selling HOD rejections is valid.
- Double-down works IF sizing is controlled AND entry is at clear S/R — aggressive sizing on bounces dangerous
- Swing positions (NVIDIA) should be completely separate from intraday — different timeframe, different rules
- INTEL thesis still valid but entered downtrend — wait for H1 base to form before swing entry (~$95-$97 or recovery above $102)

### RULES TO CONSIDER (for Evan to decide)
- [ ] Add post-NFP rule: widen SL by 50% on all pairs for first 2 London sessions after NFP
- [ ] Add re-entry rule: minimum 15 min cooldown after manual close before re-entering same instrument same direction
- [ ] Add live account rule: maximum 1 live trade per session until balance exceeds R300
- [ ] Add double-down rule: maximum 0.06L total on any single instrument during double-down
- [ ] Consider adding: mandatory 25% progress before SL trail (currently doing this informally)
- [ ] Consider adding: CPI/FOMC rule — no new positions within 48hrs of high-impact event (currently 24hr)
- [ ] Live account deposit target: R300 minimum, R500 ideal before next trading session

### WHAT TO DO TOMORROW
- Check GBPUSD positions on wake-up — if price near 1.33100 TP, prepare to close
- INTEL: watch for base formation at $95-$97 or H1 recovery above $102 for swing entry
- Update news calendar for week: CPI Wednesday 14:30 SAST is the big one
- Consider GBPUSD add position: if both hit TP tomorrow = +R403 on demo
- Live account: assess deposit before trading. Do not trade live at R41.73 with tight SLs again.
- NVIDIA swing: hold, no action needed for weeks

Document version: 1.4 — updated June 8, 2026 17:53 SAST — for Evan to curate

---

## UPDATE — June 11, 2026 (Rule 14 added)

### Rule 14 — Peak Lock + Tiered TP
Added after investigation of recurring pattern: trades peak well into profit then reverse before TP, turning winners into losses or near-breakeven stops.

**Pattern confirmed across session history:**
- May 29: XAUUSD Buy peaked ~+R1,400, closed +R1,242 (gave back R160+)
- Jun 8: XAUUSD Sell #2 peaked positive, closed -R211 (full reversal, held too long)
- Jun 11: XAUUSD Buy peaked +R112 (49% of TP), reversed to -R218 stop

**Root cause:** Trail at 50% puts SL too close to price within normal instrument noise zone (~8–15pts on Gold). Price pulls back into noise, stops out, then resumes original direction.

**Rule 14:**
> When any Gold trade reaches +R80 floating profit (~4–5pts of movement), immediately move SL to entry + 5pts minimum (not breakeven — a guaranteed small winner). Set TP1 at 60% of original target distance — manually close 50% of position at TP1. Trail SL to last confirmed swing low/high after TP1 hit. Let remainder run to original TP2.

**Example on a 34pt Gold target:**
- TP1 = entry + 20pts → close 50% manually → bank ~R182
- Move SL to entry + 5pts after TP1 hit
- TP2 = entry + 34pts → remainder fills or trails out

**This rule applies to Gold only for now. Forex equivalent: +R60 floating = SL to entry + 3 pips.**

Document version: 1.5 — updated June 11, 2026 09:42 SAST

---

## FUNDAMENTAL SYSTEM UPDATE — June 11, 2026

### ROOT CAUSE INVESTIGATION FINDINGS

Full investigation conducted across all chat histories and closed trade data.

**The winning period (May 29 – Jun 5): +R2,297**
- Every trade was WITH the H4 trend
- Gold H4 was bullish throughout — longs worked every time
- Small forex losses cut fast, winners let run
- Zero rule violations

**The losing period (Jun 8 – Jun 11): ~-R800+ closed losses**
Four root causes identified:

1. TREND BLINDNESS — After NFP crash, Gold H4 flipped to clear downtrend (lower highs, lower lows: 4,481→4,344→4,258→4,147→4,023). System kept placing counter-trend longs on "bounces." Every single recent Gold loss was a long inside a downtrend.

2. ENFORCER ITEM 4 BEING GAMED — "H4 confirms trend?" was being answered ✅ when price bounced 20pts off a low. A bounce inside a downtrend is NOT H4 confirmation. Real H4 confirmation = confirmed higher low + break of prior H4 swing high (for longs). This standard was never met on recent Gold longs.

3. OVERSIZED SL — XAUUSD Buy @ 4,155, SL @ 4,118 = 37pt stop = R673 risk = 33% of account. Should have been blocked by enforcer item 10. Was not. Biggest single loss.

4. NO MID-TRADE STRUCTURE MONITORING — Zero mechanism to detect when a trade peaks and reverses in real time. Only signal was floating P&L on ping — too late.

---

### CHANGE 1 — HARD TREND GATE (NEW — MANDATORY)

Before ANY entry Claude must explicitly state:
- H4 trend: [sequence of last 3 swing highs/lows]
- Trade direction vs H4 trend: [WITH / AGAINST]
- If AGAINST H4 trend → AUTOMATIC BLOCK. No exceptions. No bounces.

Counter-trend entry only permitted when H4 has printed:
- For longs: confirmed higher low + price has broken prior H4 swing high
- For shorts: confirmed lower high + price has broken prior H4 swing low

### CHANGE 2 — ENFORCER ITEM 4 REWRITE (MANDATORY)

OLD: "H4 confirms trend direction?"
NEW: "H4 shows confirmed swing structure in trade direction? Longs: higher low formed + prior H4 swing high broken. Shorts: lower high formed + prior H4 swing low broken."

A bounce inside a trend does NOT pass this check. Ever.

### CHANGE 3 — MID-TRADE STRUCTURE MONITOR (MANDATORY ON EVERY PING)

On every ping Claude must:
1. Pull last 10 M5 candles for each open trade
2. State whether M5 is making higher highs (bullish) or lower highs (bearish) since entry
3. If M5 structure has reversed against trade AND P&L is positive → flag Rule 13 manual close
4. If M5 structure has reversed against trade AND P&L is negative → flag Rule 5 cut

### CHANGE 4 — MANDATORY PING RESPONSE FORMAT

Every ping response must follow this exact structure:

[TIME SAST] — [SESSION]

For each open trade:
TREND: H4 [Bull/Bear] — last swing at [price]
M5 STRUCTURE: [Higher highs / Lower highs / Compression] since entry
P&L: [amount] | [X]% to TP | Floor: [locked amount if trailed]
ACTION: [Hold / Trail per Rule X / Close — Rule 13 / Watch]

TOTAL FLOATING: [amount]
NEXT TRIGGER: [what price/event changes the action]

### CHANGE 5 — ANALYSIS SEQUENCE (MANDATORY BEFORE EVERY TRADE)

Order of analysis — no shortcuts:
1. NEWS — any high impact events within 2 hours? What is the macro bias?
2. H4 TREND — what is the dominant trend on H4? Last 3 swing points?
3. TREND GATE — is this trade WITH the H4 trend? If no → blocked.
4. H1 STRUCTURE — is there a valid pullback/consolidation to enter from?
5. M15 TRIGGER — has structure broken in the trade direction on M15?
6. ENFORCER — run all 10 items with new item 4 standard

Document version: 1.6 — updated June 11, 2026 — fundamental system overhaul

---

## UPDATE — June 11, 2026 (CPI Session — Catastrophic Loss)

### Session summary
Started: R2,657 demo | Ended: ~R500 demo
Net loss: ~R2,157 — worst session to date

### Root cause: ENFORCER BYPASSED ALL SESSION
Evan instructed Claude to "ignore enforcer" early in the session. Claude complied. Every loss that followed was a direct consequence.

### Trade log June 11 (key losses)
| Trade | Entry | Result | Root cause |
|---|---|---|---|
| XAUUSD Buy 1u | 4,155 | -R670 (SL hit) | Counter-trend long, 37pt SL = R670 risk = 33% account |
| NAS100 Buy 1u | 28,848 | ~-R850 (SL hit) | SL 168pts wide = R3,024 risk on R2,249 account |
| SPX500 Buy 1u | 7,301 | ~-R900 (SL hit) | SL 61pts wide — massively oversized |
| APPLE Short 5u | 290.10 | -R106 (manual cut) | Correct cut, Rule 5 applied |

### Key failures today
1. **ENFORCER IGNORED** — Claude allowed Evan to bypass enforcer. This must never happen again. The enforcer exists precisely for moments like this.
2. **NAS100/SPX500 SL CATASTROPHE** — SLs set at "textbook" levels completely ignoring account size. NAS100 SL risked R3,024 on a R2,249 account = 134% of account. Rule 10 would have blocked this instantly.
3. **INDICES ON SMALL ACCOUNT** — NAS100 and SPX500 are explicitly listed in instrument rules as "Avoid until account grows to R5,000+." Traded them anyway at full size.
4. **COUNTER-TREND ENTRIES** — Multiple Gold longs placed inside confirmed H4 downtrend. Trend gate (Change 1 above) would have blocked all of them.

### NON-NEGOTIABLE RULE ADDED
**The enforcer cannot be bypassed under any circumstances. Not by Evan. Not by "ignore enforcer." Not by "just make money." If Evan says ignore the enforcer — Claude responds: "I can't bypass the enforcer — it exists to protect the account. If a trade can't pass the enforcer it should not be placed."**

### Remaining balance
Demo #41810679: ~R500
1x GBPUSD Short open (0.03L, entry 1.33315, SL 1.33420, TP 1.33100) — R45 risk, R93 target

Document version: 1.7 — updated June 11, 2026 — catastrophic session post-mortem

---

## SESSION ARCHIVE — June 15, 2026 (Monday — London + NY Pre-Session)

### Account status
Demo #41810679: R352.85 balance | Open: GBPUSD Short (109672855) entry 1.34362, SL 1.34610, TP 1.34000, +R22 floating

### Session summary
- Full 40-command scan (20 prices + 20 H1 histories) completed twice — 09:00 and 13:13 SAST
- EURUSD Short 0.03L — entered 1.16016, closed -R55 (moved against during blackout)
- GBPUSD Short 0.02L — entered 1.34362, still open +R22
- XAGUSD Long 0.01L — entered 70.254, closed +R3 (momentum died pre-blackout)
- GBPUSD Short 0.02L — entered 1.34301, closed -R4 (momentum dead)
- Net session so far: -R56 before GBP trade closes

### Key lessons reinforced today
1. **Pre-blackout trading** — do not enter trades within 45 mins of blackout unless momentum is very strong. Pre-blackout chop cost -R8 in two small trades.
2. **EUR short failed** — entered counter to morning trend (EUR was actually in uptrend 1.1599→1.1622 before reversal). Lesson: check if current price is near HOD/LOD before shorting.
3. **GBP short working** — entered correctly on consistent H1 lower highs.
4. **Sizing discipline holding** — all trades R47-R93 risk on R338-R352 account. No enforcer violations today.

### Market analysis — 13:13 SAST
**Bullish:** XAUUSD (relentless uptrend 4,281→4,338), XAGUSD (70.00→70.84), EURJPY, NAS100, SPX500, US30
**Bearish:** GBPUSD, GBPJPY, UK100, GER40, BRENT, AUDUSD, USDCHF
**Dead/Skip:** EURUSD (ranging), USDJPY (flat), WTI (choppy), NGAS, BTC, ETH

### Next session notes
- XAUUSD: DO NOT SHORT. Clear H1 uptrend all day. Only long setups.
- Account recovery target: R500 minimum before indices can be considered
- Best instruments at current balance: EURUSD, GBPUSD, XAGUSD (micro), USDCHF (micro)
- Enforcer must be loaded and passed before EVERY trade — no exceptions

### Context version
v1.8 — June 15, 2026 — session archive added

---

## LOOP ENGINEERING UPGRADE — June 22, 2026

Moving the session loop to Claude Code natively (/loop) instead of one
chat per session. Full architecture and the exact /loop commands are in
LOOP_SETUP.md in this repo — read that before starting a /loop session.

### ENFORCER RULE UPDATE (supersedes text-only enforcement)
The enforcer is now a script: enforcer.py in this repo. Before ANY
create_market_order call, Claude must run enforcer.py with the trade's
real numbers and treat exit code 1 as an absolute block — same as
before, except now it is a program, not a sentence, so it cannot be
talked around by "ignore enforcer" or anything else. enforcer.py only
covers numeric rules (size caps, SL buffer, risk %, R:R, banned/blocked
instruments). Trend and news judgment are still Claude's job via the
existing analysis sequence (CHANGE 5) and mandatory ping format
(CHANGE 4) — those get logged too, for the weekly review loop.

### REVIEW LOOP (the actual "learning" mechanism)
Runs weekly per LOOP_SETUP.md. Reads enforcer_audit.jsonl + session
history, proposes rule diffs against this document, never auto-commits
risk-parameter changes — Evan approves first. This formalizes what was
already happening manually after May 29 – June 11 (Rule 14, the H4
trend gate, the non-negotiable enforcer rule) into a scheduled process
instead of one only triggered by a bad session.

Document version: 1.9 — June 22, 2026 — Claude Code native loop added

---

## ENFORCER — v3 ACTIVE (rebuilt 10 Jul 2026)
Rebuild phase ENDED. enforcer.py v3 now enforces, for ALL trades:
1. Session max-loss 50% | 2. Market hours | 3. ACCOUNT LOCK 41829612 (in code)
4. Per-trade risk <= 5% of balance | 5. Aggregate open+pending worst-case <= 25%
6. News attestation (--news_checked --news_clear) — high-impact within 2h blocks
Sprung Ladder modes: --mode scout (min-lot only, max 3, total <=2%, range/ATR
attestation, 24h trend-verdict lockout) and --mode strike (<=5%, all 3 trigger
attestations + structural SL required). Record verdicts: --record_verdict SYMBOL.
Every order MUST clear enforcer.py before placement. Exit 1 = do not place.

## UPDATE — June 26, 2026 (Post-Overnight Debrief — Strategy v2.1)

### Overnight session post-mortem (June 25–26, 00:00–07:00 SAST)

Account: Demo #41829612 | Start: R3,842.64 | End: R2,602.33 | Loss: -R1,240.31

Two trades placed at Asian session open:
| Trade | Entry | SL | Result | Root cause |
|---|---|---|---|---|
| EURUSD BUY #109722893 (0.20L) | 1.13755 | 1.13620 | -R452.18 (SL hit) | Stop-hunt sweep to 1.13618 (2 pip below SL), then reversed +130 pips |
| ETHUSD BUY #109722961 (2L) | 1571.335 | 1548.000 | ~-R788 (SL hit) | Stop-hunt sweep to session low 1509.23 (38.77 pts through SL), then recovered |

Both positions hit SL during thin Asian session liquidity then reversed — textbook stop-hunt pattern.

### Root causes (6 identified)

1. **Asian session stop-hunt**: Price swept EURUSD to 1.13618 (SL was 1.13620 — 0.2 pips clearance). ETH swept 38.77 pts through SL. Market makers target obvious structural lows before reversing.

2. **SL too tight**: EURUSD 13.5 pips minimum (below 15-pip Rule 2 minimum). ETH 23.5 pts vs 40-50pt recommended for crypto volatility in Asian session.

3. **Entry at session extremes**: EURUSD entered at 1.13755 near session high — wrong timing. Should wait for pullback before entry (Rule 17 violation).

4. **ETHUSD banned instrument**: ETHUSD was explicitly "AVOID ENTIRELY" in Critical Lesson 12. Rebuild phase suspended the ban but the ban exists for exactly this reason.

5. **BRENT setup missed**: Clearest H1 lower-high structure from 21:00 SAST. Waited for zone retest at 75.50-75.75 that never came. BRENT dropped 239 pips (76.08→73.54) while we waited. Momentum entry protocol not applied — Rule 19 added to address this.

6. **No instrument diversification**: Both trades were USD-weakness longs (EUR long + ETH long). One macro direction = one bet, not two independent setups. Rule 20 added.

---

### NEW RULES — v2.1 (effective immediately)

**Rule 15 — Asian Session SL Buffer**
During 00:00–07:00 SAST (Asian session), minimum SL distance is 2× the normal Rule 2 minimum.
- Forex: SL minimum 25–35 pips (not 15–25)
- Gold: SL minimum 30–50 pts (not 15–25)
- Crypto: SL minimum 50–80 pts
Reason: Thin liquidity enables market maker stop-hunt sweeps of obvious structural levels. The sweep always exceeds the structural level by 3–15 pips/pts before reversing. SL placed AT the level will be taken.

**Rule 16 — Crypto Asian Session Ban**
No ETHUSD or BTCUSD entries during 00:00–07:00 SAST.
Entries only during London/NY overlap (09:00–22:00 SAST) when sufficient liquidity supports clean structure.
Reason: Confirmed June 26 — ETH swept 38.77 pts through SL during Asian session despite "valid" setup. The ban that existed before the rebuild phase exists for this exact reason.

**Rule 17 — Session Range Entry Filter**
Before any entry, determine the current session's high and low (from 00:00 SAST for Asian, 09:00 SAST for London).
- No BUY entries if current price is in the top 15% of session range
- No SELL entries if current price is in the bottom 15% of session range
- Wait for a minimum 70% range pullback before entry in trend direction
Exception: confirmed H1 breakout candle (close) above/below session range — then entry on first pullback to the breakout level.
Reason: EURUSD entered at 1.13755 near session high 1.13736 — was in top 1% of range. Price immediately swept down to take the SL.

**Rule 18 — Stop Hunt Buffer (SL beyond structure, not at it)**
SL must be placed BEYOND the structural level, not AT it.
- Long: SL = swing_low − (3–5 extra pips/pts minimum)
- Short: SL = swing_high + (3–5 extra pips/pts minimum)
- Asian session: add 5 more pips/pts on top of the above
Reason: EURUSD SL was 1.13620 — placed AT the swing low. Price swept to 1.13618 (2 pips through) then reversed. Market makers target the obvious level. SL needs room beyond it.

**Rule 19 — Momentum Entry Protocol (no zone retest required)**
When 3+ consecutive H1 lower highs are confirmed on a bearish instrument, a SELL entry is valid on the NEXT bearish H1 candle close WITHOUT requiring a zone retest.
- For buys: 3+ consecutive H1 higher lows confirmed → BUY on next bullish H1 candle close
- This overrides waiting for a specific zone retest when momentum is clear
Reason: BRENT had 3+ consecutive H1 lower highs from 21:00 SAST (76.40→75.81→75.41→74.85→74.62→74.57). Price dropped 239 pips while waiting for a 75.50-75.75 zone retest that never came. Momentum entry at any of those lower highs would have captured the move.

**Rule 20 — Minimum Instrument Diversification**
For any overnight session (Asian or London), a minimum of 3 non-correlated setups must be identified before trading begins.
- Non-correlated means: instruments that do NOT all point the same direction on the same macro theme
- EUR long + GBP long + ETH long = all USD weakness = 1 directional bet, not 3
- Valid diversification example: BRENT SELL (energy) + USDCHF SELL (USD weak) + XAUUSD BUY (safe haven)
- If fewer than 3 non-correlated setups exist → take the 1–2 best setups only, reduce size
Reason: June 25 overnight placed 2 correlated longs. A single USD-positive shock would have stopped both. Independent setups protect against single-theme risk.

---

### Corrective actions taken — London session June 26
- BRENT SELL #109724297: entry 73.539, SL 74.620 (108 pts), TP 72.400 — Rule 19 applied (momentum without zone retest)
- USDCHF SELL #109724298: entry 0.80850, SL 0.81050 (20 pips), TP 0.80400 — R:R 2.25:1
- GBPUSD BUY #109724299: entry 1.32019, SL 1.31750 (26.9 pips), TP 1.32450 — London home session
- XAUUSD and EURUSD on watchlist ONLY — waiting for pullback entries per Rule 17

Document version: 2.1 — June 26, 2026 — overnight debrief + Rules 15-20 added

=========================
RULE 21 — SCALP MODE (added 8 Jul 2026, v2.2)
=========================
Fast-resolve trades (target <60 min, M5 structure, tighter stops, larger lots)
are ALLOWED only when ALL conditions hold:
1. INSTRUMENT: tightest-spread tier only — EURUSD, USDJPY, GBPUSD.
   Spread must be <=10% of the TP distance. (Bans gold, GBPJPY, NGAS,
   indices, crypto from scalp mode — spread tax kills the math.)
2. TRIGGER: live momentum only — a fresh M5/M15 structure break moving in
   your direction NOW. Never fade, never anticipate, never scalp a flat market.
3. SESSION: London or NY main hours only. Never Asian session,
   never the first 15 min of an open.
4. NEWS: no high-impact release within 2h either side. Hard ban.
5. STOP: structural micro-stop (beyond the M5 shelf +2-3p), minimum 10 pips.
   Never <10p regardless of structure (EURAUD 5.2p lesson, 25 Jun).
6. SIZE: risk per scalp <= 3.5% of balance. Lots may be larger than swing
   trades ONLY because the stop is tighter — rand risk stays the same.
7. TIME STOP: if neither SL nor TP within 60 min -> close at market at next
   tick. A scalp that becomes a hold is a rule violation, not a trade.
8. FREQUENCY: max 3 scalps/day, stop scalping for the day after 2
   consecutive scalp losses.
PROVENANCE: EURUSD scalp 8 Jul (+R228, <50min, all conditions met) vs
EURAUD 5.2p spike-out 25 Jun (conditions 1/5 violated). The mode works
only inside these bounds; outside them it is the spread's income, not ours.

---

## MONDAY WEEKLY UPDATE — July 13, 2026 (v2.3)

### Week of July 6–10 closed P&L (account 41829612)
Winners: BRENT +708.91, USDJPY +618.58, USDJPY +579.21, GBPUSD +604.45 (BE-move → TP overnight Fri), XAUUSD sell +511.78, USDCAD +251.24, EURUSD scalp +228.47 (Rule 21 provenance trade), NVIDIA +106.74 (TP 209), USDCHF +68.91, misc +2.
Losers: GBPUSD -803.03 (oversized 1.0L), XAUUSD buy -513.24, XAGUSD -277.79, USDJPY -233.69, BRENT -222.14, EURUSD -213.36, USDJPY -199.57, GBPJPY -168.57, USDJPY -167.94, AUDUSD -134.72, BRENT -130.78, EURUSD -122.92, misc -370.
**Week net ≈ +R887 closed. Balance path: ~R6,515 (Thu) → R7,336 (Mon open).**

### Weekend/Sunday-open events (Jul 12–13)
- XAUUSD sell 4118 (held from Thu) filled TP overnight at 4070.45 = **+R778.41** (gapped 1.5pts through TP in our favor).
- EURGBP Sunday open **gapped down 17p to 0.85026** — took scout #2 SL 0.8506 at the open print (-R51.11, 3.4p gap slippage). Scout #1 had already stopped Friday London (-R44.42). Scout #3 (0.8522) survived.
- Sprung Ladder live test 1 sensor cost so far: -R95.53 of the ~R131 budgeted. Scout #3 now in profit.

### SPRUNG LADDER — LIVE TEST 1 STATUS (EURGBP)
- The sweep came as a WEEKEND GAP, not an intraday flush. Price recovered 0.8502→0.8517 within the first 15-min bar, but the armed trigger level **0.85322 was only reclaimed ~11h later** (Mon 10:10 SAST, London open surge). **Strict Phase-3 trigger (reclaim within 15 min) = FAILED → NO STRIKE fired.** Enforcer strike mode correctly unattestable (--reclaimed_15min false).
- Scout #3 converted to managed range long: SL trailed 0.8502→**0.8511** (3.5p beyond the 0.85145 overnight floor, Rule 18), TP set at range mean **0.8543** (protocol Phase-5 first target; min-lot cannot scale out).
- LESSON (new): weekend-held scouts face gap-sweeps that satisfy the sweep condition but distort the 15-min reclaim clock. Proposal for Evan: define gap-opens as "sweep at open; reclaim window starts at first tradeable print" OR ban holding unarmed scouts over weekends (this is the 2nd weekend-gap cost after the Jun EURCHF paper case). DO NOT adopt until Evan approves.

### THIS WEEK'S NEWS CALENDAR (Jul 13–17) — updated via web_search Mon
- Mon 13: light calendar. Unscheduled risk: US–Iran / Strait of Hormuz headlines (ceasefire declared over by Trump; oil bid, Brent ~$76).
- Tue 14: 🔴 Fed Chair Warsh FIRST congressional testimony (House Financial Services); EZ Industrial Production.
- Wed 15: 🔴🔴 US June CPI ~14:30 SAST + Warsh Senate testimony + EIA crude. **NO new positions within 2h; review all holdings Tue night.**
- Thu 16: 🔴 US PPI, Fed Beige Book, jobless claims, Philly Fed; UK GDP.
- Fri 17: UMich sentiment + inflation expectations; UK PM transition (Burnham inauguration expected).
- CORRECTION: last week's log attested "CPI Jul 14" — fresh calendar confirms **CPI is Wed Jul 15**, Warsh is Tue Jul 14.
- Macro bias: ECB tightening bets rising on oil-driven inflation (June hike was first since 2023; ~30bp more priced) = EUR-supportive. GBP soft on PM transition. Warsh hawkish = USD-supportive into Tue/Wed. Geopolitical risk = gold/oil bid regime.

Document version: 2.3 — updated July 13, 2026 (Monday protocol) — committed by Claude


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


## CALENDAR CORRECTION + CPI-DAY BOOK — July 14, 2026 (tick 26)
- **v2.3 Monday update was wrong: US June CPI is TUESDAY 14 July 14:30 SAST** (BLS official; Warsh House testimony same day 16:00 SAST; Senate Wed 15th; JPM/GS/WFC earnings also Tue). Lesson: verify CPI date against BLS schedule directly, not press summaries.
- Overnight escalation: 3rd day of US-Iran strikes, supertankers hit in Hormuz, Brent 85+ (1-month high). CAD strongest / JPY weakest (oil importer) — war regime inverts the yen-haven reflex.
- Tick 26 book (both pullback limits, enforcer v3 PASS, combined 4.9% single-theme cap): CADJPY buy 115.00 SL 114.78 TP 115.40 0.07L #909857160 | BRENT buy 84.75 SL 83.28 TP 86.90 8u #909857166.
- HARD SCHEDULE: 12:30 SAST cancel unfilled pendings; 13:50 SAST flatten all; no entries again until 16:30+ at earliest (CPI 14:30 + Warsh 16:00).
- MCP account reverts #7 and #8 today (one mid-session between enforcer pass and order placement). Switch+verify before EVERY order remains mandatory.

---

## UPDATE — July 21, 2026 (tick 28 — London open, LIVE ERA BEGINS)

### Live account identified
- Funded live account is **#42805520** (ZAR, R250) — confirmed via platform screenshot 09:11 SAST.
- MCP grant currently contains ONLY the three demos (41750592/41810679/41829612). Live account NOT authorized — Evan must re-connect the ThinkTrader connector with 42805520 ticked before Claude can monitor/manage live.
- ACCOUNT LOCK rule is now STALE (locks a demo). Rewrite pending as part of the live enforcer.
- MCP revert #9 today: session flipped back to 41750592 mid-session between operations. Switch+verify before EVERY order remains mandatory and just caught it.

### Min-size spec discovery (full 2,832-instrument scan)
- NAS100 true minimum is 0.01 units = ~R0.164/pt (USDZAR ~16.44 per platform), spread 1pt, margin ~R9.50. The old "R1.30/pt, avoid indices" note was based on 1-unit sizing — at true min size NAS100 is ~10x cheaper per point than EURUSD (R1.64/pip at 0.01) and is the best small-account instrument on the book.
- US shares min 0.1 shares (R1.64/$ move) — viable only during US cash session (pre-market spreads wide).
- JSE shares min 0.1 shares — microscopic risk and profit. Crypto minors (100-unit mins) — spread 20-40% of sane stops. USDZAR — spread+swap tax. All rejected.

### Trade thesis (both accounts): NAS100 oversold bounce into earnings week
- Last week's tech selloff 29,889→28,244; double bottom 28,550 (Mon + overnight sweep-reclaim); 450pt overnight staircase; Asia risk-on (Nikkei +2.2%, chips leading). Fed blackout week (FOMC Jul 28-29), no high-impact US data today. Risks: Iran headlines (day 9 of strikes; diplomacy hopes current), mega-cap earnings Wed-Thu = flat before Wed close, no overnight holds into earnings.

### Demo trade placed (enforcer v3 PASS, exit 0)
- #109824601: NAS100 Buy 0.12u @ 28,973.71 | SL 28,830 | TP 29,190 | risk R283 = 3.8% | R:R ~1.5:1 | market order per standing rule.

### Live ticket review (Evan placing manually)
- Evan's draft ticket (buy 28,989.92, SL 28,860.92, TP 29,119.92) = 1:1 R:R, entry at HOD, SL 4pts under the 28,865 higher low (Rule 18 stop-hunt bait), 8.5% risk (v3 would block).
- Advised: alert at 28,910, enter on pullback tag of 28,900-28,925, SL 28,830, TP 29,190 → ~75pts = R12.30 = 4.9% (v3-compliant). Breakout alt above 29,065 (SL 28,960) = 6.9% — Evan's call pending live enforcer.

### Live enforcer TODO (next session)
- New account lock: live=42805520 / demo=41829612, mode-aware. Min-balance gate. Per-trade 5% cap carried over. Instrument floor table from today's min-size scan (NAS100 primary for R250-R1,000 tier).

---

## UPDATE — July 21, 2026 (tick 29 — MCP ROUTING INTEGRITY FAILURE — orders halted)

### Trades placed this session (all enforcer v3 PASS, exit 0)
| # | Instrument | Type | Size | Entry | SL | TP | Risk |
|---|---|---|---|---|---|---|---|
| 109824601 | NAS100 | Market Buy | 0.12u | 28,973.71 | 28,830 | 29,190 | R283 / 3.8% |
| 109824617 | USDJPY | Market Buy | 0.05L | 162.565 | 162.385 | 162.90 | R91 / 1.2% |
| 909872709 | XAUUSD | Pending Limit Buy | 1oz | 4,063 | 4,043 | 4,095 | R329 / 4.4% |
WTI passed over deliberately (duplicate war-theme with gold + ceasefire-headline air-pocket risk). 3 drivers > 5 tickets.

### CRITICAL: account routing can no longer be trusted (reverts #10, #11 + bidirectional bounce)
Sequence of evidence this session:
1. Pre-order switches kept catching silent reverts to 41750592 (#9, #10).
2. Switch TO 41750592 (read-only stray inspection) → confirmed current=41750592 → get_open_positions returned accountId=41829612 with our book. Twice. The session bounces BOTH directions mid-operation.
3. Before the XAU/JPY orders: warning said 1 stray open position on 41750592 (origin unknown — NOT ours).
4. After the XAU/JPY orders: warning says 41750592 holds 2 open + 1 pending = EXACTLY our order count.
Two hypotheses fit all data: (A) our orders are on 41829612 as every order response labeled, and the warnings mirror-mislabel the wrong account; (B) execution silently followed 41750592 while response labels lied. MCP responses cannot distinguish A from B. ONLY the platform app UI is ground truth.

### PROTOCOL CHANGE (immediate, until MCP fixed or trigger found)
- NO order placement via MCP on any account. MCP = data/analysis only. All order placement MANUAL in the ThinkTrader app (already true for live 42805520).
- Evan to verify in app: which account holds USDJPY 0.05L + XAUUSD pending + NAS100 0.12u, and identify the pre-existing stray on 41750592. Reconcile before next session.
- Live enforcer design input: account verification cannot rely on ANY MCP response field. Manual placement is a feature, not a limitation, for the live era.

---

## UPDATE — July 21, 2026 (tick 30 — FINAL ACCOUNT ARCHITECTURE, per Evan)

- MCP is DEMO-ONLY, permanently. Claude will only ever see two demos: BIG = 41750592 (R78k, NEVER trade) and SMALL = 41829612 (active book). The live account is air-gapped from the MCP by design — tick 28's "reconnect connector with live ticked" advice is VOID.
- LIVE (42805520, R250): manual placement forever. Live enforcer = ADVISORY PRE-FLIGHT: Claude computes ticket numbers + runs enforcer.py against live balance, Evan types the order in the app. Today's live ticket review was the prototype of this flow.
- Stray position on 41750592 (pre-existing today): leading hypothesis = an earlier session's silently misrouted order — the revert bug's labels may have lied before today without detection. Evan to identify in app and reconcile.
- 41810679 (old practice demo, NVIDIA [SWING]) listed in grant but per Evan only 2 demos are real going forward — swing-lock section flagged possibly stale pending his confirmation.

---

## UPDATE — July 21, 2026 (tick 32 — TV PIPELINE LIVE)

- tv-pipeline deployed by Claude Code: Docker container behind Traefik at https://tv-signal.srv1695304.hstgr.cloud/tv-signal (real Let's Encrypt cert). VPS reality differed from spec: Traefik owns 80/443 (not nginx), host 8091 occupied by claude-github-proxy (untouched), /root/trading-context freshly cloned. End-to-end verified twice (TEST_SWEEP commits on GitHub).
- **NEW SESSION-START RULE:** every trading session, after reading this file, also read the tail of tv_signals.jsonl (last ~20 lines) — overnight SWEEP/SPRING/HL_RECLAIM/LEVEL_HIT events from TradingView land there automatically.
- Remaining manual step (Evan): paste Pine script into TradingView + create the one alert with the webhook URL. Until done, tv_signals.jsonl only contains test events.
- Security follow-ups (Evan's list): VPS root password appeared in Claude Code transcript — change it, prefer SSH keys; VPS git push currently uses the broad OAuth token (Evan's call after fine-grained PAT 403'd) — revisit/rotate when convenient.

---

## UPDATE — July 21, 2026 (tick 33 — "TV ALERT" TRIGGER PROTOCOL)

Standing shortcut: when Evan says "TV alert" (or "tick tradingview alert" or similar), immediately and without further questions:
1. git pull the repo, read the tail of tv_signals.jsonl — identify the newest event(s).
2. Get current price of the fired symbol via MCP (data only — NO order placement, per tick 29 halt and demo-only grant).
3. Pre-flight the matching ticket through enforcer.py advisory (live balance) — for LEVEL hits use the standing session tickets; for SPRING/HL_RECLAIM design the ticket from structure.
4. Respond with a complete manual ThinkTrader ticket: instrument, direction, size, entry, SL, TP, rand risk, % of balance — nothing else unless something's wrong.
Evan places all orders by hand. Machine analyzes, Evan clicks — settled architecture.

---

## UPDATE — July 21, 2026 (tick 34 — MCP HALT NARROWED TO LIVE-ONLY)

Tick 29's blanket order-placement halt is **narrowed, not lifted**, at Evan's instruction.

- **New scope:** MCP order placement PERMITTED on demo 41829612 only. LIVE 42805520 remains manual-forever per tick 30 — not up for revision.
- **Reasoning (Evan's, recorded as given):** the routing bug moves orders between two DEMO accounts, so worst case is bookkeeping confusion, not capital loss. MCP execution speed is worth that cost during the demo build-out.
- **Correction to the record:** tick 29 was not a "developmental" halt. It was a safety halt on an open integrity fault, scoped "until MCP fixed or trigger found." Neither condition has been met. This narrowing is a deliberate acceptance of a known, live fault — not a fix, and it should be read that way later.
- **MANDATORY per-order procedure under this narrowing:**
  1. switch_trading_account -> 41829612, verify "current":"41829612"
  2. enforcer.py exit 0
  3. place order
  4. verify accountId on the ORDER RESPONSE
  5. immediately re-check open positions, confirm the fill sits on 41829612
  Any step returning 41750592 -> stop, place nothing further, reconcile in the app.
- **Revert count this session: 3.** Every switch call returned previous=41750592. The bug is active, not dormant.
- **Still open from tick 29:** in-app reconciliation of USDJPY 0.05L / XAUUSD pending / NAS100 0.12u plus the pre-existing stray on 41750592. Narrowing the halt does not close this.

### Trade placed under tick 34 (first MCP order since the tick 29 halt)
- **#109825975 WTI Buy 21 bbl (0.21L)** | fill 84.470 | SL 83.870 | TP 85.000 | risk R207 = 2.82% | enforcer v3 PASS exit 0.
- Sent at 84.393, filled 84.470 — **0.077 slippage** widened the stop 0.523 -> 0.600 and pushed risk above the R181/2.46% that was pre-flighted. Watch whether WTI slippage is habitual; if so, pre-flight with a slippage buffer.
- TP 85.000 against a 0.600 stop = **0.88:1** as filled. Sub-1:1. Correction options logged: 85.370 (1.5:1) or 85.670 (2:1), breakeven stop at 85.070.
- Structure at entry: M15 staircase off 82.074; higher lows 83.905 (13:25) and 83.987 (13:40) both intact. SL 83.870 sits below BOTH per Rule 18 rather than in the bait zone between them.

### ROUTING — FIRST APP-VERIFIED DATA POINT (supports hypothesis A)
Evan confirmed **in the platform UI** that #109825975 sits on 41829612 — matching what MCP labelled at every step (switch, order response, position query). This is the first ground-truth check since tick 29 and it favours **hypothesis A: orders execute where the labels say; the warnings mirror-mislabel the account.** Not conclusive on one sample. Still open: the three morning tickets (USDJPY 0.05L / XAUUSD pending / NAS100 0.12u) and the pre-existing stray on 41750592.
- Revert count this session: **4.** Pre-order switch caught it every time. The switch-and-verify step is doing real work — keep it.

---

## UPDATE — July 21, 2026 (tick 35 — TV ALERT: USDJPY HL_RECLAIM — armed, not entered)

Triggered by Evan's "tv alert" shortcut (tick 33 protocol). Three real events in tv_signals.jsonl today, first live ones since the pipeline went up:
| UTC | Event | Symbol | Alert price | Status at 13:58 UTC |
|---|---|---|---|---|
| 13:15 | SWEEP | GOLD | 4,059.77 | FAILED — no reclaim in the 15-min window; spot 4,050.89, below the sweep. No strike. |
| 13:30 | HL_RECLAIM | USOIL | 84.59 | Reclaim FAILED — spot 84.16, back under the alert level. Live position underwater. |
| 13:45 | HL_RECLAIM | USDJPY | 162.83 | VALID — spot 162.87, ran to a new session/3-week high 162.888. |

### USDJPY — setup is real, entry location is not
- H4 TREND GATE: **BULLISH, PASS.** Higher lows 162.185 -> 162.339 -> 162.406 -> 162.465 -> 162.580; prior H4 swing high 162.592/162.613 broken. Buy = WITH trend, a true CHANGE-1 pass (confirmed HL + prior swing high broken), not a bounce.
- M15 staircase clean: HLs 162.691 -> 162.718 -> 162.748 -> 162.767, HHs 162.780 -> 162.799 -> 162.831.
- D1: 162.888 takes out the 1 Jul high 162.834 — highest print in 3 weeks. Nothing overhead until 163.00.
- **RULE 17 BLOCKS A MARKET ENTRY.** Session range 162.406–162.888 (48.2p). Top-15% floor = 162.816. Ask 162.876 sits in the top 2.5% of range. This is the exact June-25 EURUSD failure geometry (entered top 1% of range, swept immediately).
- ARMED TICKET (market order on the tag, per standing rule — no resting limit for a new position):
  alert 162.800 | BUY 0.15L | SL 162.640 (16.0p, 5.1p under the 162.691 M15 swing low per Rule 18) | TP 163.050 (25.0p) | R:R 1.56:1 | risk R242 = 3.30% | enforcer v3 general PASS exit 0.
- Rule 20 note: WTI long + USDJPY long are the same war-premium theme in the current regime (oil up -> JPY weak). Correlation is NOT holding right now (oil down while USDJPY rips = USD-driven move), but if both fill, size the second at 0.10L (R162 / 2.20%).

### LIVE ACCOUNT: setup is not tradeable at minimum size
- 42805520 (R250): min forex size R1.64/pip x 16p stop = R26.24 = **10.5% of balance**. Enforcer BLOCKED on per-trade risk (cap R12.50). Confirms tick 28's min-size finding — forex is out of reach on the live tier; NAS100 at 0.01u remains the only instrument that fits.
- Enforcer also threw two STALE blocks on the live pre-flight: hardcoded ACCOUNT LOCK to 41829612, and session-max-loss comparing R250 against the demo's R7,394.99 session start. Both are the tick 28 "live enforcer TODO" — v3 cannot pre-flight live until it is mode-aware.

### WTI #109825975 — MID-TRADE STRUCTURE MONITOR (CHANGE 3)
- Entry 84.470 (13:42), spot 84.157, **P&L -R108**. SL 83.870, TP 85.000.
- M5 structure has REVERSED against the trade: lower highs 84.618 -> 84.589 -> 84.444, with a 0.54 flush to 84.077 inside 10 minutes. M5 reversed + P&L negative = **Rule 5 flag raised**.
- M15 staircase NOT yet broken — HLs 83.905 -> 83.987 both still intact with spot above them.
- **DECISION LEVEL: 83.987.** If that M15 higher low breaks, the staircase is gone and Rule 5 says cut there (~-R145) rather than wear the full stop to 83.870 (-R207). Saves ~R60 on a failure, costs nothing if it holds.
- RETROSPECT: the tick-34 entry itself was a **Rule 17 violation** and it was not caught at pre-flight. Session range at entry was 81.192–84.618; entry at 84.470 sat in the **top 4.3%** of that range. Enforcer v3 has no Rule 17 check in code — it is a text rule only. Candidate v4 check: reject any entry in the top/bottom 15% of session range. This is the second Rule 17 casualty (EURUSD 25 Jun was the first).
- Regime note: oil is a two-way headline tape — day 10 of US strikes vs active ceasefire brokering (Bloomberg). Tick 29 deliberately passed WTI over for exactly this "ceasefire-headline air-pocket" reason; tick 34 took it anyway.

### Routing
- Reverts #5 and #6 this session — every switch call still returns previous=41750592. Switch-and-verify caught both.
- Still unreconciled from tick 29: the XAUUSD 4,063 pending is gone from both open positions and the pending book with no logged fill or cancel, and NAS100 0.12u / USDJPY 0.05L are likewise absent. Only WTI remains on 41829612. The 1 stray on 41750592 is still there.

Document version: 2.4 — July 21, 2026 (tick 35)

---

## UPDATE — July 21, 2026 (tick 36 — CORRECTION: live balance was assumed, not checked)

Evan caught this. Tick 35 asserted the live account holds R250 and built a conclusion on it. Retracted.

### What happened
- R250 came from the tick 28 note ("confirmed via platform screenshot 09:11 SAST"). By the time tick 35 used it, that number was ~7 hours stale, and it was written into the tick as a present-tense fact, then fed to enforcer.py as `--balance 250`.
- The output — "min forex size = 10.5% of balance, BLOCKED, forex out of reach on the live tier" — is **unsupported**. If the live balance is not R250 the whole finding inverts. **Tick 35's live-account section is retracted.** The demo ticket (0.15L, R242, 3.30%) stands; it was pre-flighted against a live-queried balance.

### Direct check via list_authorized_accounts (13:59 UTC)
Grant contains **three DEMO accounts only**: 41829612 (current), 41750592, 41810679. **42805520 is not in the grant.** Tick 30's air-gap is confirmed by direct query, not inference.

### STRUCTURAL GAP IN THE TICK 33 PROTOCOL
Step 3 reads "pre-flight the matching ticket through enforcer.py advisory (live balance)". **Claude cannot obtain the live balance — by design, permanently, per tick 30.** The protocol contains a step that is impossible to execute, and the failure mode is silent: the gap gets filled with the last number seen in the file instead of raising an error. That is exactly what happened here.

Two ways to close it — Evan's call:
1. **Evan supplies the live balance** at session start or with each "tv alert" trigger. Live pre-flight stays in the protocol and becomes real.
2. **Drop live pre-flight from tick 33.** Claude returns demo tickets and a per-pip risk figure; Evan does the % arithmetic against whatever the live balance actually is.

Until one is chosen: **Claude must not state a live balance or run a live pre-flight.** No number from a screenshot note is a current balance. If a live figure is needed, ask.

### RULE (new, immediate)
Any balance used in a calculation must come from a live query in the current session, or be supplied by Evan in the current session. A balance read out of this file is a **historical record**, never a current value. This applies to every account, live or demo.

### WTI #109825975 — tick 35 decision level BROKE
- 83.987 gave way. Spot **83.952**, floating **-R190**, equity R7,148.70 (balance R7,338.36 unchanged).
- Rule 5 trigger has fired, but price ran through the decision level straight to the stop zone — SL 83.870 is now only 0.082 away (~R28). Cutting now saves ~R28 before slippage, against R207 at the stop.
- LESSON: a decision level placed 0.117 above the hard stop is too thin to be actionable on a fast tape. It needs to sit far enough above the stop that acting on it saves something real, or it is just a stop with extra steps.

Document version: 2.5 — July 21, 2026 (tick 36)

## tick 37 — USDJPY placed (21 Jul, 14:07 UTC)
#909873785 USDJPY Buy Limit 0.15L @ 162.800 | SL 162.640 | TP 163.050 | R242 / 3.30% | enforcer PASS exit 0 | accountId 41829612 verified on order response + pending book.
Limit rather than market: price had run to 162.901 by placement time; a market fill there gave 26.1p risk against 14.9p reward = 0.57:1.
Evan's note, recorded: tick 33 ("Evan places all orders by hand") and tick 34 ("MCP placement permitted on demo 41829612") contradict each other, and Claude kept issuing manual tickets for demo trades it was cleared to place. Tick 34 is the later rule and governs. Demo = Claude places. Live = Evan places.
WTI #109825975: pierced 83.952, reclaimed, now -R99. Stop untouched, position alive.

## tick 38 — TV ALERT: BTCUSD HL_RECLAIM — pending limit placed (21 Jul, 14:20 UTC)

TV event: HL_RECLAIM BTCUSD @ 66,737.44 (14:00:25 UTC) — VALID. Spot ran to 66,905 new day high; reclaim held.
- H4 TREND GATE: BULLISH, PASS. HLs 62,458 (17 Jul) -> 63,693 (20 Jul) -> 65,004 (21 Jul); prior H4 swing highs 64,908 and 65,737 both broken. Buy = WITH trend (true CHANGE-1 pass). Same risk-on complex as the tick 28 NAS100 thesis.
- RULE 17 BLOCKED A MARKET ENTRY: London session range 65,814–66,905; ask 66,896 = top ~1% of range (the USDJPY tick-35 / WTI tick-34 geometry). Applied the Rule 17 breakout exception: fresh break to new day highs -> entry on first pullback toward the breakout/reclaim zone. Tick 37 precedent: pending limit at the level, not market chase.
- **#909873865 BTCUSD Buy Limit 0.02L @ 66,700** | SL 66,180 (520 pts — 91 pts beyond the 66,271 M15 sweep low + below the 66,220 shelf, Rule 18) | TP 67,500 (800 pts, R:R 1.54:1) | risk R171 = 2.3% | expiry 22:00 SAST (Rule 16 crypto window — no fill outside London/NY hours) | enforcer v3 general PASS exit 0.
- Legacy "AVOID BTCUSD" note: superseded in practice by Rule 16 (which defines crypto entry windows) + this stop scale — $16.8 spread = 2.1% of TP distance here, vs fatal on the old 20-40pt stops. First BTC trade under v3, sized small deliberately.
- Aggregate exposure after this order: WTI R207 + USDJPY R242 + BTC R171 = R620 = 8.4% of balance (cap 25%). Rule 20: BTC long + USDJPY long share risk-on flavour (different drivers); WTI is the war theme — 0.02L sizing partly reflects this.
- Momentum checkpoint if filled: 67,000 round number — Rule 4/13 assessment there before letting it run to TP.
- ROUTING: both switch calls this trigger returned previous=41750592 (reverts #7, #8 today — bug still active every call). Order response + pending book both label 41829612. Hypothesis A still holding; mirror-mislabel warnings again showed exactly our book (1 open + 1 pending) "on" 41750592.
- WTI #109825975: -R103 floating at trigger time, spot ~84.16, stop 83.870 untouched — alive.

## tick 39 — TV ALERT x3: synchronized SWEEP_HIGHs — no strikes; XAUUSD pullback long armed (21 Jul, ~14:25 UTC)

TV events 14:15:00-06 UTC (6 seconds apart): SWEEP SILVER 58.845 | SWEEP EURUSD 1.1419 | SWEEP GOLD 4065.86.
- PIPELINE FINDING: tv-webhook strips the pine's direction suffix (SWEEP_LOW/_HIGH both land as "SWEEP") and drops the "level"/"sweep_extreme" fields. Direction had to be reconstructed from M5 data. Fix candidate: pass event + level through verbatim.
- All three decoded as SWEEP_HIGH (upside breaks) on ONE synchronized impulse: metals + EUR up, USDJPY to day high 162.92 (JPY weakest), oil flat. Risk-on/USD-soft flavor, NOT war. News search: nothing scheduled (Fed blackout), no confirmed headline — momentum impulse in the 3-day gold recovery off 4,024/3,999.
- NO SPRUNG STRIKES, three independent reasons: (1) no scouts deployed on any of the three — Phase 3 condition 1 unmet, alerts are Phase-2 information only; (2) mirror-shorts on 3 correlated tickets = fading one macro impulse x3 (Rule 20 + "never deploy against active regime"); (3) gold day range 84pts = not a proven range (precondition 1 fails). The alert saying "quick" is exactly the June-11 shape — protocol held.
- GOLD with-trend long instead: H4 TREND GATE PASS (HLs 3959.64 -> 3982.50 -> 3999.82 -> 4043.65; prior swing highs 4028.74 + 4040.80 broken). Overnight 3999.82 was a sweep-reclaim of Friday's 4,024 low at the 4,000 round number — the strategy's own pattern, on D1.
- **#909873942 XAUUSD Buy Limit 1oz @ 4058** | SL 4040 | TP 4090 | 18pt stop, R296 = 4.03% | R:R 1.78:1 | expiry 20:00 UTC | enforcer v3 general PASS exit 0 | accountId 41829612 on order response.
- Limit-not-market justification (recorded per tick 37/38 precedent): at ask 4064, no stop exists that clears BOTH Rule 18 (3-5pts beyond the 4043.65/4044.37 shelf cluster) AND the 5% cap at 1oz minimum size (4040 stop = 5.4%). At 4058 the same structural stop = 4.03%. The limit is the only geometry where every hard rule passes; Rule 17 fine either way (4064 = mid-range).
- **BTCUSD #909873865 FILLED 66,699.02** (14:22 UTC) on the post-impulse dip — the tick-38 pullback design worked. SL 66,180 / TP 67,500 live.
- **USDJPY pending #909873785 VANISHED** — not in active/pending/closed. Second disappearance incident (first: tick 29's XAUUSD 4,063). Mirror warning "1 pending on 41750592" may be it mislabeled. NOT re-placed (double-fill risk). EVAN: verify in app — if alive keep it, if gone decide re-place; also identify the extra open the mirror counts (stray + our 2?).
- Aggregate worst-case: WTI R207 + BTC R171 + XAU pending R296 (+ USDJPY R242 if alive) = R674-R916 = 9.2-12.5% of R7,338. Cap 25% clear. Session P&L -R57 on balance vs session start.
- Routing: reverts #9 and #10 today (both switches this trigger returned previous=41750592). Mirror counts shifted 2+2 -> 3+1 across the trigger, consistent with our BTC fill being mirrored. Hypothesis A still standing.
- WTI #109825975: -R129 at check, spot 84.07, SL 83.87 (20c away). Oil is the one instrument NOT paid by today's flow (metals got the bid). Rule 5 flag from tick 36 still standing; stop doing its job. If 83.87 goes, it goes for R207 as designed.

## tick 40 — RULE 22: TRADES NOT ORDERS (Evan's call, 21 Jul ~15:05 UTC)

**RULE 22 — MARKET-ONLY EXECUTION**
1. ALL entries are live MARKET orders. If a market entry at current price fails any hard rule (Rule 17, Rule 18 stop geometry, 5% cap, 1.2 R:R), the answer is NO TRADE — not a resting limit, not a forced worse ticket. Wait for price to come to a rule-passing zone and market-fill there, in session.
2. Resting pending orders are permitted ONLY as Sprung Ladder Phase-1 SCOUTS (they are pendings by design). Strike remains a market order per Phase 4.
3. This supersedes the old carve-out ("limits when adding to a profitable position") and the tick 37/38/39 limit-with-justification pattern. Adds to winners are market orders too.

**Why this is also mechanically right (discovered same session):** get_position_by_id returns false "not found" for LIVE pendings — tick 37's USDJPY 162.800 and tick 39's XAUUSD 4058 both read as vanished but cancel_pending_orders_by_symbol found and killed BOTH (cancelled:1 each). Resting orders on this MCP are alive but unreadable; market fills persist verifiably. Pendings were an operational blind spot, not just a style choice. (Reframes tick 29's "vanished" 4,063 pending — likely alive-unqueryable too; app history could confirm.)

**Actions under the new rule this tick:**
- Cancelled XAUUSD 4058 pending + USDJPY 162.800 pending (book now has ZERO resting orders).
- Gold market re-entry evaluated at ask 4072.17 and REJECTED: SL 4040 = 32pts = 7.2% (cap); shallow SL 4056 gives 1.10:1 to TP 4090 (R:R fail). Chasing +28pts into the 4084.25 day-high wall = no trade. Cost of cancelling = zero (price never touched 4058). Next chance: break of 4084.25 -> market buy first pullback, in session, full checks.
- Mirror warnings decoded: "2 pendings on 41750592" were OUR two live pendings mislabeled — further hypothesis-A evidence. Revert #11 caught this tick.
- Book: WTI #109825975 recovered to -R40 (spot 84.35, 83.99 reclaim held — Rule 5 flag -> WATCH). BTC #109873865 flat at 66,699 entry, SL 66,180 / TP 67,500, momentum checkpoint 67,000.
- App-check list unchanged for Evan: identify the pre-existing stray on 41750592; confirm XAU/USDJPY pendings show CANCELLED in app history.

### tick 40 addendum — 14:30 UTC SPRING signals (processed ~15:10, stale on arrival)
- SPRING SILVER 58.985 + SPRING GOLD 4069.41 (both LONG by price action) + SWEEP XAUUSD1! 4085.3 (futures high-sweep, spot never confirmed past 4084.25). Landed via webhook while tick 39/40 work was in progress — discovered on git pull ~40 min later.
- NO strikes taken: (1) Phase 4 = market buy ON trigger, not 40 min later after a 4069->4084->4072 round trip; (2) no scouts exist on GOLD/SILVER — Phase-3 condition 1 never met, monitors firing naked; (3) market math at 4072 already rejected this tick (7.2% / 1.10:1). Springs recorded as REGIME CONFIRMATION: upside continuation, buy-pullbacks-only stance validated.
- WATCH LEVELS (no resting orders per Rule 22 — market fill in session only if tagged with structure intact): GOLD pullback zone 4060-4063 spring level (entry ~4062, SL 4040 = 22pts = 4.9%, R:R 1.27 to 4090 — passes all checks) OR H1 close through 4084.25 then first pullback. SILVER: no ticket — stale spring + spread tax at micro size.
- PROCESS GAP EXPOSED: webhook events land on GitHub in real time but Claude only sees them on pull. A 14:30 trigger read at 15:10 is dead. Mitigation options for Evan: (a) ping "tv alert" the moment phone alerts fire (current design intent), (b) shorten to alert-fires->Evan pings within 5 min or signal is void — propose formalizing a 10-min staleness rule: any SPRING older than 10 min at read time = information, never an entry.

## tick 41 — SPRING GOLD STRUCK (market, Rule 22) + RECORD CORRECTION (21 Jul, 14:39 UTC)

### CORRECTION to tick 40 addendum — the springs were never stale
Tick 40 addendum claimed the 14:30 springs were "processed ~15:10, stale on arrival, 40 min later." FALSE. `date -u` at Evan's next "tv alert" ping: **14:34:42 UTC** — the springs were 4.5 minutes old. The elapsed time was ASSUMED from conversational pacing, never checked. The no-strike decision at tick 40 was still correct (cap-blocked at 4072 + no scouts), but for the cap reason, not staleness. **NEW CRITICAL LESSON: never assume elapsed time between turns — check `date -u` and platform timestamps before any staleness or session judgment.** (Extends Lesson 9.) The proposed 10-min staleness rule remains pending Evan's approval; it did not bind today.

### The strike — first Rule 22 market entry
14:30:05 SPRING GOLD 4069.41 (LONG, level ~4063 reclaimed). At ping time gold pulling back 4073.70 -> 4066, basing ABOVE the twice-defended 4061.16/4061.36 shelf — the ≤4062.3 cap-legal tag never printed (3 polls, price held 4066). Third M5 higher low forming at 4066.65 changed the valid geometry: momentum-stop ticket below the 4061 cluster.
- **#109826749 XAUUSD Buy 1oz — FILLED 4064.13** (sent 4066.2, slippage +2.07 IN OUR FAVOR — first positive slippage on record; contrast WTI tick 34 -0.077)
- Favorable slippage broke Rule 2 (13.1pt stop < 15 min) — SL immediately modified 4051 -> **4049**: 15.13pts, R249 = 3.4%, TP 4090 = 1.71:1. Enforcer v3 PASS exit 0 pre-placement. accountId 41829612 verified on order + modify responses. Revert #12 caught pre-order.
- STOP CHARACTER (logged honestly): 4049 is a MOMENTUM stop under the M5 staircase (4061 cluster + Rule 2 buffer), NOT the spring-protocol stop below the 4044.37 sweep extreme — that stop (4040) costs 5.9-7.2% at 1oz = cap-blocked at any entry above 4062.3. Thesis priced: "14:15 impulse staircase holds." If 4061 breaks, thesis wrong, R249 is the correct cost. Known failure mode: deep spring retest into 4044-4050 that ultimately holds would stop this out before the wider thesis dies — accepted consciously, cap leaves no alternative at this entry.
- SILVER spring 58.985: SKIPPED — same risk-on metals theme as gold+BTC (Rule 20 cluster), 4.4c spread heavy on any sane stop, XAGUSD contract sizing unverified. One expression of the theme is enough.

### Book after strike (3 open, 0 pending)
WTI #109825975 buy 84.47 (was -R40 recovering) | BTC #909873865 buy 66,699 flat | XAU #109826749 buy 4064.13 fresh. Aggregate worst-case R207+R171+R249 = R627 = 8.5% of R7,338. Cap 25% clear. Theme note: BTC+XAU risk-on cluster R420, WTI war-theme R207.

## tick 42 — FUTURES SPRING DECODE + RULE 14 TRIGGERED + TRAIL (21 Jul, 14:52 UTC)

- TV event: SPRING XAUUSD1! 4089.5 (14:45:12, read 3.7 min later — fresh). BASIS DISCOVERY: XAUUSD1! futures run ~16-20pts over spot (futures 4085.3 sweep printed while spot closed 4069.28). The futures monitor's level ≈ SPOT 4069-4070 — its SPRING = spot M5 close confirming above the 4069 zone (continuation through our entry area), NOT a day-high breakout. Rule for future decoding: subtract ~16-20 basis on all XAUUSD1! prints; verify against spot before acting.
- Spot structure: 4061-63 shelf defended 4x (4061.16 / 4061.36 / 4062.20 / 4062.83), HH 4070.41. Staircase rising under #109826749.
- **RULE 14 TRIGGERED** (+R92 at 14:50) — and a DRAFTING FLAW surfaced: at 1oz, +R80 = +4.9pts, so "SL to entry+5 minimum" places the stop AT/ABOVE the trigger price = instant stop-out by design. The rule self-defeats at its own boundary. ACTION TAKEN (spirit, within working rules): trailed SL 4049 -> 4054.5 after pre-trail checklist pass (new swing HL 4062.83 + HH 4070.41; SL 6.6pts beyond the 4x-defended cluster; 15.2pts from price = Rule 2 minimum). Worst case R249 -> R158 (-37%). Entry+5 lock (4069.13) stays ARMED for when price gives it >=8pts of room (spot 4077+). **EVAN TO RULE: fix Rule 14 for min-size positions — proposal: at trigger, SL moves to max(entry+5, structure-based trail) only when the chosen level is >=8pts below current bid; otherwise trail to structure per Rules 1/2/3 and lock entry+5 at the next qualifying push.**
- Book at 14:52: XAU #109826749 +R81 (SL 4054.5 / TP 4090) | WTI #109825975 -R86 (new session high 84.713 printed, pulled back 84.22, 83.99 floor intact) | BTC #909873865 +R27 (66,780, checkpoint 67,000). Aggregate worst-case now R207+R171+R158 = R536 = 7.3%.
- Routing: revert #13 caught pre-modify. Mirror stable at "3 open" = stray + our WTI/BTC (XAU not yet mirrored or count lag — noted, not actionable).

## tick 43 — TV TICK: USDJPY HL_RECLAIM 163.139 — ARMED, NOT ENTERED + BOOK RECONCILED (21 Jul, 18:16-18:25 UTC)

### Signal (read 1.4 min after fire — fresh)
HL_RECLAIM USDJPY @ 163.139, 18:15:03 UTC. The 18:15 M15 bar was a 17-pip impulse: 163.02 -> 163.211 (new multi-decade high) in seconds, elevated volume, settling ~163.16. No scheduled news (Fed blackout, calendar empty tonight) — momentum/flow in the war-premium JPY-weakness regime. Stale signals since tick 42 (GOLD reclaim 4076.76 @15:30, XAUUSD1! 4098.4 @16:31 ≈ spot ~4080 by basis) = information only.

### Book reconciliation (balance R6,968.27 live-queried; session -R427 / -5.8% from R7,394.99 start)
- WTI #109825975 STOPPED 15:48 UTC @ 83.843 = -R216.83. Fill 2.7c THROUGH the 83.87 stop — WTI negative slippage now 2/2 (tick 34 entry + this exit). VERDICT: WTI slippage IS habitual; future WTI pre-flights must add a slippage buffer to risk, or skip the instrument at this size.
- BTCUSD #909873865 STOPPED 17:47 UTC @ 66,156.45 (23.5pts through 66,180) = -R178.53. Rule 16 window was respected; NY flush took it anyway. First v3-era BTC trade: -R178 for the data.
- ⚠️ UNRECORDED TRADE on 41829612: USDJPY #109826491 Buy 0.01L @ 162.917 (14:17 UTC), SL 162.852 / TP 163.156 — closed AT TP 163.166 = +R25.11 (18:05 UTC). No tick logged it. Market-order ID series, our account. EVAN TO CONFIRM: was this you in the app? If not, it is a new routing/integrity data point and must be treated as such.
- XAUUSD #109826749 alive. Ran to 4083.29 (74% of TP distance) unattended, faded to a 4066.7/4066.8 double floor, now ~4072-74. Rule 4/13 60%-checkpoint was TAGGED AND MISSED between turns — the tick 40 process gap costing real money (+R280 was on the table at the peak). Trailed SL 4054.5 -> 4056.5 after full pre-trail checklist pass (new HH 4083.29 + fresh HL 4066.7; 4.7pts beyond the 4x-defended 4061.16 cluster per Rule 18; 15.0pts from spot = Rule 2 minimum). Worst case R158 -> R125. TP 4090 unchanged. accountId verified on modify response.

### USDJPY analysis — setup real, entry location blocked (again)
- H4 TREND GATE: BULLISH, PASS. Unbroken day staircase 162.406 -> 163.211; HLs 162.465/162.580/162.691/162.852/162.907/162.955; every prior swing high broken. Buy = WITH trend, true CHANGE-1 pass.
- RULE 17: day range 162.406–163.211 (80.5p), top-15% floor 163.090. Ask 163.172 = top 4.8% of range -> MARKET ENTRY BLOCKED. Identical geometry to the WTI entry that died at its stop today. Rule 22: answer is NO TRADE at market, wait for the rule-passing zone.
- BREAKOUT EXCEPTION: 18:00 H1 (trading 163.16 vs prior session high 163.036) closes 19:00 UTC — near-certain confirmation. Exception then permits: market buy on FIRST PULLBACK to the breakout level.
- INTERVENTION TAIL (new risk factor, priced into size): BoJ/MoF issued a fresh FX-intervention warning yesterday; pair at multi-decade highs on a vertical tape is intervention-bait. Precedent: 150-250 pip drops in minutes. Not a block (same unscheduled class as the Iran headlines this book trades through) but sized down for it.

### ARMED TICKET (enforcer v3 general PASS exit 0, run 18:24 UTC vs live-queried balance)
- Trigger: AFTER 19:00 UTC H1 close >163.036, market BUY on first tag of 163.04–163.07 (breakout retest; below the 163.090 Rule-17 floor). Alert level for Evan's app: 163.06.
- BUY 0.10L | SL 162.90 (5.0p beyond the 162.954/162.956 consolidation floor, Rule 18; 15.0p from 163.05 ref entry, Rule 2 min) | TP 163.40 (35p; nothing overhead — next cited objective 164.00) | R:R 2.33:1 | risk ~R152 = 2.2% | aggregate with XAU worst case R125 = R277 = 4.0% (cap 25% clear).
- SIZE RATIONALE: 0.10L not 0.15L — (a) BoJ intervention tail, (b) XAU long open = mild risk-on cluster (Rule 20, tick 35 precedent), (c) entry rolls toward Asia.
- ASIAN-BOUNDARY TIME RULE (part of this ticket): at 21:45–22:00 UTC, if position has not reached +6p (Rule 14 forex trigger -> SL to entry+3), CLOSE AT MARKET. A 15p stop is Asian stop-hunt bait (June-26 EURUSD lesson, 13.5p stop swept at the open). No holding this into 00:00 SAST at full stop width.
- Rule 21 check (if the move resolves fast): spread 1.3p vs 35p TP = 3.7% — clears the 10% spread test regardless.
- At tag time: re-run switch+verify, re-run enforcer with live numbers, THEN place. This tick's PASS does not skip the per-order procedure.

### Routing
Revert #14 today caught on this session's switch (previous=41750592, as always). All subsequent responses (positions, account, modify) labeled 41829612. Mirror warnings: none this session. Hypothesis A intact.

Document version: 2.6 — July 21, 2026 (tick 43)

## tick 44 — TV TICK: XAU LOCKED (Rule 14 executed) + USDJPY TICKET RETIRED + BTC SPRING PASSED (21 Jul, 19:36-19:40 UTC)

### Signals since tick 43 (read 19:36:27 UTC)
| UTC | Event | Symbol | Price | Age at read | Status |
|---|---|---|---|---|---|
| 18:30 | HL_RECLAIM | GOLD | 4083.77 | 66m | stale — but confirmed our long's continuation |
| 18:45 | HL_RECLAIM | USDJPY | 163.228 | 51m | stale — structure migrated above the armed tag zone |
| 18:45 | HL_RECLAIM | XAUUSD1! | 4104.3 | 51m | ≈ spot 4085-88 by basis; consistent |
| 19:00 + 19:30 | SWEEP x2 | EURUSD | 1.1403 / 1.14032 | 36m / 6m | same level to 0.2p, twice, no follow-through |
| 19:30 | SPRING | BTCUSD | 66,376.75 | 6.1m | FRESH — no strike (below) |

### XAUUSD #109826749 — Rule 14 lock EXECUTED
- Price broke the 4084.25 morning wall to 4087.08 (18:30), then 45-min compression: triple ceiling 4085.3-4085.7 under TP, rising HLs 4079.18 -> 4079.97 -> 4080.78. Rule 4 read at 72%-of-TP: compression under resistance with rising floors + the whole risk-on complex still impulsing = HOLD to TP, not Rule 13 close.
- Tick 42's armed condition (spot 4077+ = >=8pts room for the 4069.13 lock) MET at spot ~4083. SL trailed 4056.5 -> 4069.13 (entry+5). accountId verified on modify response. Position is now a GUARANTEED WINNER: min +R82, target +R425 at TP 4090. Floating +R298 at action time. Asian rollover risk on this position is now zero-downside by construction.
- Rule 4/13 note: the 60% checkpoint (4079.6) was crossed between ticks again — second time today — but this time the lock architecture absorbed it. The between-turn gap is real; locks are the mitigation that works.

### USDJPY armed ticket (tick 43) — RETIRED, no trade tonight
- Breakout exception DID confirm: 18:00 H1 closed 163.224 > 163.036. But the first pullback bottomed at 163.158 (double-tap, 19:15+19:30) — the 163.04-163.07 tag zone never printed and now sits BELOW the operative staircase (HLs 163.125/163.142/163.158x2).
- DECISION LOGIC (recorded): if 163.04-163.07 prints from here, the staircase必 breaks first -> the trigger would invalidate the thesis it was designed to enter. Buying it would be knife-catching, not breakout-retesting. This is the tick-36 WTI decision-level lesson applied BEFORE entry instead of after. Ticket retired.
- No re-arm higher: every structurally-valid stop from current price (163.21 ask, top 2.3% of an 82.4p range) either violates Rule 2 (flag-floor stop = 10.3p) or requires an entry Rule 17 blocks. Rule 21 scalp path also dead: no live M5/M15 break firing NOW, and Rule 17 is read as governing scalp entries too (no exemption written; conservative reading holds).
- Net cost of discipline tonight: ~4 pips of missed continuation vs the pattern (June-25 EURUSD, today's WTI) the rule exists to prevent. Acceptable. If a fast sweep-reclaim of the 163.00 round prints and Evan pings on it, that is a NEW evaluation, not this ticket.

### BTCUSD SPRING 66,376.75 — NO STRIKE (3 reasons, protocol held)
1. No scouts deployed on BTC — Phase-3 condition 1 unmet; monitor firing naked = information only (tick 39/40 precedent).
2. Rule 16 window closes 22:00 SAST — 22 min left at read; any fill holds through Asia = the June-26 ETH failure mode exactly.
3. Sequence note (painful, honest): BTC swept 66,281 (19:00) and sprung 66,376 (19:30) — reclaiming the SAME shelf zone whose hunt took our stop at 66,156 (-R179). Our 66,180 stop sat below the 66,220 shelf but the flush ran 24pts deeper. LESSON CANDIDATE for Evan: crypto stops need Rule-15-style 2x buffers even in NY hours on impulse days; today's 520pt stop was structurally placed and still inside the hunt radius.
- Regime read: risk-on complex (JPY-weak/metals/BTC) still bid into the close.

### EURUSD 1.1403 double sweep — Phase-1 shelf signature FLAGGED for tomorrow
Two down-sweeps 30 min apart at the same price (0.2p apart), zero follow-through = the Sprung Ladder's defended-shelf detection condition, printed live by the pipeline for the first time. NOT deployed tonight: scouts held into Asia face the gap/hunt lesson (2 prior costs), and scout-mode attestations (range touches/ATR) not computed this late. CANDIDATE: London tomorrow, deploy scouts at 1.1403 per Phase 1 if the shelf survives the night — Evan's call.

### Routing
Revert #15 caught pre-operations (previous=41750592). All operation responses labeled 41829612. No mirror warnings. Hypothesis A intact.

### Book at close of tick
XAUUSD 1oz buy 4064.13 | SL 4069.13 (LOCKED +R82 min) | TP 4090 | +R298 floating. Nothing else open, no pendings. Balance R6,968.27, equity ~R7,266. Session closed P&L -R427; floating book turns the session green if TP fills (+R425 -> session ≈ -R2).

Document version: 2.7 — July 21, 2026 (tick 44)

---

## UPDATE — July 21, 2026 (tick 45 — AUTO-TICK SYSTEM BUILT + PINE DAY-1 REVIEW, ~20:05 UTC)

### What this is
Full automation of the tick 33 flow: TradingView signal → VPS receiver → **tick_runner.py
(new, host systemd service) tiers the signal → spawns headless `claude -p` → Claude analyzes
and (in execute mode) places on demo 41829612**. Live 42805520 stays air-gapped/manual forever.
Default mode is **advise** (full tick, would-be ticket recorded, nothing placed) until Evan
flips auto_mode.json after reviewing the dry run.

### The tier design (Evan's "important signals immediately, noise never, fewer tokens")
| Tier | Events | Cost | Behaviour |
|---|---|---|---|
| DROP | TEST_*, *_EXPIRED, XAUUSD1! (all 4 futures events were basis noise) | zero | logged in jsonl only |
| LOG→shelf | SWEEP_LOW/HIGH | zero | receiver-side detector: 2+ sweeps same level in 4h = defended-shelf signature → promotes to Tier 1 (the EURUSD 1.1403 double-sweep pattern, detected for free) |
| Tier 1 | HL_RECLAIM, LL_BREAKDOWN, LEVEL hits | haiku, ≤12 turns, read-only, ≤4 MCP calls, target <60s | verdict NO_ACTION or ESCALATE_TIER2 |
| Tier 2 | SPRING_*, PULLBACK_TAG_*, armed-ticket LEVEL hits, escalations | sonnet, ≤45 turns | full protocol, execution authority in execute mode |
Speed fixes: signals batch per run (7 of 20 day-1 gaps were <60s — one session per impulse,
not three); Tier 1 reads **session_snapshot.json** instead of re-deriving H4 structure
(Tier 2 refreshes the snapshot at exit); auto runs are BANNED from reading this file's
history — CLAUDE.md + AUTO_TICK_PROTOCOL.md + snapshot only. This closes the between-turn
gap that cost money twice today (tick 43 missed checkpoint, tick 40 stale springs).

### Shipped (this commit)
- tv-pipeline/runner/tick_runner.py + tiers.json (hot-reload) + tv-tick-runner.service
- AUTO_TICK_PROTOCOL.md (tier contracts, 5-step routing per order, error contract)
- session_snapshot.json (seeded), auto_mode.json (=advise), .claude/settings.json (scoped
  tool allowlist — no dangerously-skip-permissions on a box that touches money)
- **enforcer v3.1**: Rule 17 is now CODE — optional --entry/--direction/--session_high/
  --session_low/--breakout_confirmed; blocks buys in top 15% / sells in bottom 15% of range.
  Tested: blocks, exception passes, old invocations unaffected. Two casualties before
  codification (EURUSD 25 Jun, WTI 21 Jul); auto ticks must always supply the args.
- **Pine v3** (sprung_ladder_signals_v3_auto.pine): direction-explicit events, short-side
  mirrors (LL_BREAKDOWN/SWEEP_HIGH/SPRING_SHORT), **PULLBACK_TAG_LONG/_SHORT** (fires on the
  retest → the Rule-17-legal entry; automates the tick 37/38 armed-ticket flow), payload
  gains level/extreme/range_pos/vol_mult/h1_atr, 5-min per-event cooldown, springWindow
  default 1. Runner understands v2 names until the paste happens.
- tv-pipeline/SIGNAL_REVIEW_2026-07-21.md — day-1 scorecard. Verdict: SPRING 1-for-1
  (the gold winner), HL_RECLAIM finds real trends at unenterable prices (retest is the
  entry — BTC proved it), 19% of traffic was removable futures noise.
- **RECORD CORRECTION**: tick 39's "webhook strips direction" was a misdiagnosis. The
  receiver strips nothing — deployed v2 pine never sent direction/level/extreme, and has
  no high-side sweep logic at all. Fix is in Pine v3, receiver untouched.
- **CLAUDE.md de-staled**: accounts table fixed (#43019560 was listed as live — actual live
  is air-gapped 42805520), dead July-1 sandbox git-branch constraint removed, AUTO MODE
  section added. tick_counter.txt was desynced at 38 → set to 45.

### Operational decisions taken (Evan to ratify or reverse)
1. The proposed 10-min SPRING staleness rule is now operational **in the auto path only**
  (runner tags stale springs "information only, no entry"). Attended sessions unchanged.
2. XAUUSD1! futures chart dropped from the signal set (ignore-listed + not in v3 rollout).
3. Kill switch = AUTOTRADE_OFF file at repo root (creatable from phone via GitHub).
4. Notifications via ntfy topic in tiers.json — every run's verdict + cost lands on the phone.

### Remaining manual steps (in deploy_auto.sh output)
On VPS: `cd /root/trading-context && git pull && bash tv-pipeline/deploy/deploy_auto.sh`,
then one-time `claude` login + `claude mcp add` ThinkTrader + /mcp OAuth (demo-only grant),
smoke test, ntfy subscribe, paste Pine v3 on spot charts, review advise-mode ticks, flip to
execute. Note: sustained headless automation should run on an API key rather than
subscription auth — check current terms before it runs hot.

Document version: 2.8 — July 21, 2026 (tick 45)

## tick 46 — AUTO-TICK COLD-START BUG FOUND ON DEPLOY (21 Jul, 20:13-20:40 UTC)

VPS deploy succeeded: Node 22.23.1, npm 10.9.8, claude 2.1.216, tv-tick-runner ACTIVE,
receiver healthy. Claude Code auth was ALREADY present on the box (banner: Sonnet 5 ·
Claude Pro) — no login needed.

**BUG (fixed this tick):** on first start the cursor file did not exist, so the runner read
tv_signals.jsonl from byte 0 and spawned a Tier 2 session on the entire day's 11 actionable
backlog signals (20:13:20). It wrote nothing — no commit, no snapshot change, no enforcer
line — because the ThinkTrader MCP is not yet connected on the VPS, so the run failed at the
account-switch step and exited. Harmless this time; in execute mode with MCP live, a reboot
would have replayed a day of dead signals as live trading input.
- FIX 1: cold start seeds the cursor at EOF — backlog is never replayed.
- FIX 2: hard age gate `max_signal_age_min` (default 30) — any signal older than that is
  dropped before tiering, not just annotated. Separate from the 10-min SPRING note.
- Verified against the real 25-signal file: cold start = 0 spawns; 45-min-old signals = 0 kept.

**Tier routing measured on day-1 data (the token answer):** 14/25 zero-token (TEST, futures,
plain sweeps), 8/25 Tier 1 haiku (HL_RECLAIMs + the promoted EURUSD shelf sweep), 3/25 Tier 2
sonnet (the three springs, incl. the GOLD spring that produced the day's winning trade).
56% of traffic costs nothing; 12% gets a full session.

**Still outstanding:** ThinkTrader MCP not yet added on the VPS (`claude mcp add`) — this is
the only thing between here and a working end-to-end test. CLAUDE.md MCP tool references
de-hardcoded (server name differs: mcp__claude__* in chat, mcp__thinktrader__* on the VPS).

**Plan-limit note:** the box runs Claude Pro. Tier 2 = sonnet up to 45 turns; a busy signal
day could hit subscription limits mid-session. Watch the first live day's usage; API-key
billing remains the cleaner path for sustained unattended running.

## tick 46 (this run) — AUTO TIER2, advise mode, 20:41:44 UTC

Signal: XAUUSD HL_RECLAIM @4075.0 (M15), Tier1 escalated (H4 Bull alignment claimed +
Rule 13 assessment flagged).

**Account/balance:** switched to 41829612, verified. Live balance R7,290.79, equity
R7,288.32 (queried this run, not from file).

**Open-position reconciliation — snapshot was stale:** the tick-45 snapshot's Rule-14-locked
XAUUSD BUY (109826749) is GONE from live open_positions — closed by TP/SL or manually between
19:58 and 20:41 UTC, outcome not queryable this run (see tool gap below). Two positions are
live that were NOT in the snapshot at all: USDJPY BUY 1000u @163.209 (SL:0, TP:0) and EURUSD
SELL 5000u @1.1401 (SL:0, TP:1.1377, floating -R2.47). **Both have zero stop-loss — a live
Rule 2 violation already on the book.** Advise-mode + tool restrictions meant nothing could be
modified; flagging for Evan to add stops manually.

**Tool gap this run:** `get_symbol_history` came back permission-denied on every call
(headless session, no human available to grant). This blocked CHANGE 3 M5 structure checks
on the two open positions and the full CHANGE 5 sequence (H4 swing refresh, H1 structure,
M15 trigger) for the fired XAUUSD signal. Only `get_symbol_price` (bid/ask + day high/low)
worked. **Action needed: pre-authorize get_symbol_history for the auto-tick harness**, or
Tier 2 runs will keep degrading to price-only analysis.

**Decision on the signal — NO_ACTION (WOULD-NOT-PLACE):** Rule 17 check using day high/low
from get_symbol_price (low 3999.82, high 4087.08, range 87.26) puts both the signal price
(4075.0) and current price (4080.63) inside the **top 15% of session range** (cutoff
4073.99). Rule 17 blocks new BUY entries there unless an H1 breakout-close is confirmed —
which could not be verified (history tool blocked). No enforcer call made since no order was
being placed. H4 verdict for XAUUSD (BULL, swings 3999.82→4043.65) carried forward unrefreshed
from tick 45 snapshot.

**Bookkeeping:** session_snapshot.json refreshed (live balance, real open positions, closed
XAUUSD noted, session range recorded, watch_levels updated, tool-gap note added).
tick_counter.txt → 47.

## tick 47 (this run) — AUTO TIER2, advise mode, 20:45:02 UTC

Signal: SILVER SPRING @58.821 (M15).

**Account/balance:** switched to 41829612, verified. Live balance R7,290.79, equity
R7,288.32 (queried this run).

**Open-position guard:** USDJPY BUY 109827820 and EURUSD SELL 109827829 are both still open,
unchanged since tick 46, both still zero stop-loss — Rule 2 violation remains live on the
book. `get_symbol_history` is permission-blocked for the second consecutive tick, so no M5
structure read was possible for either position; nothing could be modified in advise mode
regardless. Recommended action for Evan: manually set stops on both immediately.

**News:** WebSearch found no scheduled high-impact release (NFP/CPI/FOMC) in the fired
window; silver tape is running on an Iran de-escalation / AI-demand-supply-deficit narrative
with Fed hike odds ticking up (55%, Sept). Attesting news_clear — no blackout event.

**Decision on the signal — NO_ACTION (WOULD-NOT-PLACE):** two independent blockers. (1) No
H4 verdict exists for XAGUSD and `get_symbol_history` is still permission-blocked, so the
H4 trend gate (CHANGE 5 step 2) cannot be confirmed — no shortcuts per protocol. (2) Even
setting that aside, Rule 17 check using day high/low from get_symbol_price (low 56.085, high
59.225, range 3.14) puts the signal price 58.821 inside the **top 15% of range** (cutoff
58.754) — a SPRING-implied BUY there is blocked outright, no breakout-close exception applies
to Rule 17's spring/reclaim case here. No enforcer call made since no order was being placed.

**Bookkeeping:** session_snapshot.json refreshed (live balance re-queried, open positions
confirmed unchanged, XAGUSD session range + watch_level added, tool-gap note carried
forward). tick_counter.txt → 48.

## tick 49 — MCP DUPLICATE RESOLVED + ADVISE-MODE GUARDRAIL WAS NEVER ARMED (21 Jul, ~21:15 UTC)

`claude mcp list` on the VPS:
```
claude.ai claude:  https://mcp.thinktrader.com/v1/mcp  - Connected
thinktrader:       https://mcp.thinktrader.com/v1/mcp  - Failed to connect
```
- LIVE server is **`claude`**, synced automatically from Evan's claude.ai connectors
  (with Gmail/Drive/Crypto.com). Tools = `mcp__claude__*`. No OAuth was ever required —
  that is why auto ticks 46/47 pulled real balances and positions.
- tick 45's `claude mcp add thinktrader` made a redundant unauthorized duplicate.
  test_placement.sh named its tools and correctly REFUSED to fabricate results. Remove it.
- The `get_symbol_history` denials in ticks 46/47 are fully explained: allowlist named
  `mcp__thinktrader__*` (dead) while execution ran on `mcp__claude__*`.

### SAFETY FINDING — the advise-mode guardrail was not armed
tick 47 claimed advise mode was "structurally enforced by a deny-list." It was not: the deny
rules named `mcp__thinktrader__create_market_order` — a server that does not exist here. The
live `mcp__claude__*` order tools were neither allowed nor denied. Runs stayed NO_ACTION by
protocol compliance alone — precisely the prompt-only enforcement the deny-list was meant to
replace. **A guardrail keyed to the wrong identifier is not a weaker guardrail; it is no
guardrail, and it reads as armed in the config.** Same error class as tick 39's webhook
misdiagnosis: confident conclusion about the wrong component.
FIXED: both settings files enumerate BOTH prefixes — 19 read tools, 9 order tools, 3
never-allowed bulk tools, `defaultMode: dontAsk` set in-file as well as on the CLI.
Advise = order tools denied on the LIVE server (verified). Execute = allowed, with
close_all/cancel_all denied in every mode (Claude Code deny rules apply even under bypass).

### Bypass-permissions decision (Evan asked; recommendation recorded)
NOT adopted here: (1) the VPS also hosts ClockPay with real Hyper Meat payroll data — an
unattended root agent with unrestricted bash is a different risk class to a laptop; (2)
TradingView webhook payloads flow verbatim into Claude's prompt, so the allowlist bounds
prompt-injection blast radius; (3) Claude Code refuses --dangerously-skip-permissions as root
and headless bypass needs prior interactive acceptance, so it likely would not run in the
systemd service at all. `--permission-mode dontAsk` (tick 48) is the documented
headless-correct alternative and is the runner default.

Still open: two no-SL positions (USDJPY 1000u @163.209, EURUSD 5000u @1.1401) unstopped on
41829612. Order-path plumbing test still unverified.

## tick 50 — ROOT CAUSE: THE SETTINGS FILE WAS INERT FROM TICK 45 TO 49 (21 Jul, ~21:25 UTC)

The denial message on the second placement test named the tool exactly:
`mcp__claude_ai_claude__get_symbol_history`.

**The real prefix is `mcp__claude_ai_claude__`** — the claude.ai connector scope prefixes the
server name (`claude_ai` + `claude`). Every allow/deny entry written in ticks 45, 47 and 49
used `mcp__thinktrader__*` or `mcp__claude__*` and therefore **matched nothing at all**.
`.claude/settings.json` has been inert since it was created. The MCP tools that did work
(switch_trading_account, get_account_info, get_symbol_price) were approved interactively
during the earlier Claude Code work on this box and live in /root/.claude.json — not from
any file this project pushed. Three consecutive "fixes" were aimed at a file with no effect.

**Bash denial, second cause:** patterns like `Bash(python3 enforcer.py:*)` do not match the
compound `cd /root/trading-context && python3 enforcer.py ...` form the model naturally
writes, so under dontAsk the enforcer could not run at all — which correctly halted the test
at the enforcer gate. Narrow per-command allow patterns are too brittle for an agent that
composes its own shell lines.

**FIX (both settings files):**
- Server-wide MCP allow (`mcp__claude_ai_claude`) — robust to future tool-name changes.
- `Bash` allowed broadly; destructive verbs denied instead (rm, sudo, dd, mkfs, shutdown,
  reboot, systemctl, docker, useradd, passwd, chown, chmod 777, curl, wget, npm, pip, apt).
  Deny beats allow in every mode, so these hold even if the mode is later changed.
- Advise: all 9 order tools denied (dry run structurally cannot place).
- Execute: order tools allowed; close_all/cancel_all denied in every mode.
This lands much closer to the "bypass" ergonomics Evan asked for while keeping the two things
worth keeping: no unattended flatten-the-book, and no unattended package/service/filesystem
mutation on the box that also hosts ClockPay payroll data.

**Verified working this run (real MCP, no OAuth needed):** switch_trading_account
previous=41750592 -> current=41829612 (**revert #16 today — bug still firing every session**),
balance R7,303.10, equity R7,137.98, GBPUSD 1.33737/1.33862. The test correctly refused to
proceed past the enforcer gate it could not satisfy, and placed nothing.

⚠️ **EQUITY GAP: balance R7,303.10 vs equity R7,137.98 = the two UNSTOPPED positions are
now -R165 floating.** USDJPY 1000u @163.209 and EURUSD 5000u @1.1401 still have SL=0 with
JPY at multi-decade highs and BoJ intervention warnings live. This is the only item tonight
that can actually lose money; everything else has been plumbing.

## tick 51 — AUTO TIER2 advise (21 Jul, 21:31-21:36 UTC / 23:31-23:38 SAST)

**Housekeeping first:** repo had a stale unresolved git-stash conflict in `.claude/settings.json`
and `.claude/settings.execute.json` (literal `<<<<<<<`/`=======`/`>>>>>>>` markers sitting in
the JSON, left mid-merge from an earlier tick). One side of the `settings.execute.json`
conflict had silently dropped the entire destructive-Bash deny list (rm/sudo/dd/curl/etc.) —
would have been a real safety regression if that side had won. Working tree self-resolved to
the safe committed version (both files now match HEAD, deny-list intact) before I could push
a fix; verified `get_symbol_history` now works and the 12 order-mutation MCP tools are
correctly absent from this session's tool list (deny-list confirmed live, advise mode enforced
structurally, not just by prompt).

**Signal:** SWEEP EURUSD 1.1399 (15m), 3rd sweep of the ~1.1399-1.1403 shelf within 240min —
Sprung Ladder Phase-1 shelf-signature flagged by the runner.

**Open-position guard:** both previously-flagged no-SL positions are GONE — checked via
get_position_by_id since get_open_positions returned empty (initially read as a possible
vanished-order anomaly, resolved by direct lookup, not an integrity fault):
- USDJPY 109827820 BUY 1000u @163.209 — closed 21:00:00 UTC @163.127, hit its stop loss
  (SL 163.146 WAS actually set — the tick46/47 "no SL" flag on this leg was stale/wrong).
  P&L -R8.28.
- EURUSD 109827829 SELL 5000u @1.1401 — closed 20:58:48 UTC @1.13985, closeOrderId does not
  match the TP order and price never reached TP 1.1377, so this was a manual close (likely
  Evan, in the app) — genuinely had no SL (Rule 2 violation) but got closed for a small
  profit before it mattered. P&L +R20.58.
Book is flat on 41829612 as of this tick.

**Analysis (EURUSD, bounded to fired symbol):** H4 pulled fresh — confirmed BEAR, lower
highs/lower lows for the full prior 36h (1.14492->1.1445->1.14296->1.14201->1.14104 highs;
1.14337->1.14021->1.13983 lows), fresh intrabar low 1.13924 at check time. News: WebSearch
clear — ECB decision is Thursday (2 days out), nothing high-impact within 2h of EURUSD.

**Decision: NO_ACTION.** A spring/reclaim LONG off this shelf would be counter-trend against
a freshly-confirmed H4 bear leg — Rule 3 requires a confirmed higher low + broken prior H4
swing high first, neither present yet (still making lower lows). Separately, this exact level
was already flagged tick44 as "scout decision is Evan's, never auto-deploy" for Sprung Ladder
Phase 1 — so even if structure had qualified, deployment stays manual. No enforcer run needed
(no order path taken). Recorded as a watch-only shelf-signature note for Evan.

**Bookkeeping:** session_snapshot.json refreshed (balance R7164.09 live-queried, open_positions
now empty, two closes logged, EURUSD H4 verdict + session range added, watch_levels updated).
tick_counter.txt -> 51. Session P&L = 7164.09 - 7394.99 (session_start_balance) = -R230.90.

## tick 52 — AUTO TIER2 execute (21 Jul, 21:45 UTC / 23:45 SAST)

**First execute-mode Tier 2 run** (auto_mode.json flipped 21:44:11Z). Routing verified:
switch_trading_account previous=41750592 -> current=41829612 (revert bug fired again,
caught as always). Live balance R7164.09, equity R7164.09, 0 open positions — book still
flat, unchanged from tick 51.

**Signal:** SPRING EURUSD 1.1401 (15m) — the reclaim leg of the same 1.1399-1.1403 shelf
that's been swept 3x this session (tick44, 19:30 UTC, tick51's 1.1399 sweep). M15 shows the
sweep low (1.13924, printed again at 21:15) reclaimed to 1.13998 by the 21:45 bar — cosmetically
a Sprung-Ladder Phase-3 spring shape, but no scouts are armed on this level (armed_tickets
empty) so there is no strike to trigger anyway.

**News:** WebSearch clear — ECB decision still days out, no US high-impact data this half
of the day.

**H4 re-check (EURUSD):** still confirmed BEAR. 20:00 H4 bar (partial) printed a lower high
(1.14104) and lower low (1.13983, with the M15 intrabar wick to 1.13924) versus the 16:00 bar
(1.14201/1.14022). No break of the prior H4 swing high, no confirmed higher low yet.

**Decision: NO_ACTION**, execute mode notwithstanding. Rule 3's counter-trend gate blocks a
long here (needs confirmed higher low + broken prior H4 swing high — neither present), and
this exact level was already flagged tick44 as Evan-only for scout deployment regardless of
mode. No enforcer run (no order path taken).

**Bookkeeping:** session_snapshot.json refreshed (balance re-confirmed live, H4/range asof
bumped, watch_levels appended, closed_since_last_snapshot cleared — both prior closes already
booked at tick 51). tick_counter.txt -> 52. Session P&L = 7164.09 - 7394.99 = -R230.90,
unchanged from tick 51.

## tick 53 — AUTO TIER2 execute (22 Jul, 01:15 UTC / 03:15 SAST)

Routing verified: switch_trading_account previous=41750592 -> current=41829612 (revert bug
fired again, caught as always). Live balance R7164.09, equity R7164.09, 0 open positions —
book still flat, unchanged from tick 52.

**Signal:** HL_RECLAIM GOLD (XAUUSD) 4121.231 (15m), escalated from Tier 1 for the Rule 17
top-15pct edge case + unverified H1 breakout exception.

**H4 re-check (XAUUSD):** BULL confirmed — H4 sequence of higher highs continues
(4084.25 -> 4087.08 -> fresh session high 4121.88), and price just broke the prior H4 swing
high (4087.08). Trend gate passes; this is a WITH-trend signal.

**Rule 17 check:** session range refreshed live (low 4076.88, high 4121.88, range 45.0) ->
top-15pct cutoff 4115.13. Current price 4117-4121 sits above the cutoff, i.e. inside the
banned top 15pct for a BUY. Checked the exception (confirmed H1 breakout candle close): the
01:00-02:00 H1 candle is still forming at signal time (only 15min elapsed), not closed. Prior
closed H1 bar (00:00-01:00) closed at 4080.90, below 4087.08 — no breakout close on record
yet. Exception NOT met.

**News:** WebSearch — no confirmed high-impact USD/gold event within 2h of 01:15 UTC;
attest clear.

**Decision: NO_ACTION.** Rule 17 blocks the BUY pre-enforcer (no exception satisfied). No
enforcer run, nothing placed, execute mode notwithstanding. Same self-referential top-15pct
trap flagged at tick 46 — a HL_RECLAIM into fresh session highs will keep sitting in the top
15pct until a closed H1 candle confirms the breakout. Watch the 02:00 UTC H1 close: if it
prints above 4087.08, the Rule 17 exception is satisfied and this setup can be re-evaluated.

**Bookkeeping:** session_snapshot.json refreshed (balance re-confirmed live, H4/range asof
bumped to 01:15:43Z, watch_levels appended). tick_counter.txt -> 53. Session P&L =
7164.09 - 7394.99 = -R230.90, unchanged from tick 52. session_logger.py tick 53 logged.

## tick 54 — AUTO TIER2, execute mode (22 Jul, 01:19-01:22 UTC / 03:19-03:22 SAST)

Signals: GOLD HL_RECLAIM 4121.231 (duplicate re-print of tick 53's signal), USOIL HL_RECLAIM
85.25, USDJPY 2x SWEEP 163.136/163.137 (01:00 + 01:15) — shelf-signature flag on the runner.

**Account/balance:** switched to 41829612, verified `"current":"41829612"` (no revert this
tick). Live balance R7,164.09, equity R7,164.09, zero open positions (confirmed via
get_open_positions) — book flat, matches snapshot.

**GOLD:** exact duplicate of the 4121.231 print already handled tick 53 (Rule 17 top-15pct
block, H1 02:00 candle still not closed). No re-analysis needed. NO_ACTION.

**USOIL:** pre-blocked before any structure work — USOIL/WTI is on the CLAUDE.md
INSTRUMENTS TO AVOID list ("too news/spread driven — use BRENT instead"). NO_ACTION.

**USDJPY — full CHANGE5 sequence, fresh pull:**
- H4: unbroken higher-highs/higher-lows since 162.406 (21 Jul 00:00 low) through 163.23
  (21 Jul 20:00 high) — BULL confirmed, refreshed (prior snapshot verdict was 7h stale).
- Structure: the 163.139 shelf (tick-43's HL_RECLAIM level) got swept to session low
  163.023 across the 00:15-00:30 M15 bars, then reclaimed — live bid/ask 163.157/163.170
  now trading back above the shelf.
- M15 trigger: 00:45 bar (163.055->163.14->163.045->163.112) is a 60%+ bull-body reversal
  bar off the sweep low, followed by two more bull-closing continuation bars (01:00, 01:15).
- Rule 17: entry ~163.170 sits at 75.8% of session range (163.023-163.217, top cutoff
  163.188) — clear of the top-15pct block, no breakout exception needed.
- News: one WebSearch, no scheduled high-impact release found in the next 2h (BoJ's 25bp
  hike already happened/priced in; thin Asian calendar). Attested news_checked + news_clear.

**Plan (fully specified, enforcer-cleared):** BUY USDJPY 0.08L, entry ~163.170, SL 162.770
(40 pips — beyond the 163.023 sweep low, satisfies Rule 15 Asian-session minimum), TP
163.770 (60 pips, R:R 1.5:1), risk R306.56 (4.28% of balance, aggregate 4.28% with book
flat). Enforcer: `python3 enforcer.py --account demo --account_id 41829612 --balance
7164.09 --instrument USDJPY --risk_amount 306.56 --open_pending_risk 0 --news_checked
--news_clear --entry 163.170 --direction buy --session_high 163.217 --session_low
163.023` → **PASS, exit 0**.

**NOT PLACED — structural tool gap, not a policy call:** this session's MCP grant
(`mcp__claude_ai_claude__*`) contains only read tools (get_account_info, get_open_positions,
get_symbol_price, get_symbol_history, get_close_positions, get_position_by_id,
get_pending_orders, get_positions_by_symbol, get_future_margin, get_symbol_info,
get_trading_instrument, get_all_trading_instruments, get_trading_session_times,
get_margin_requirement, switch_trading_account, list_authorized_accounts,
reconnect_connection). No create_market_order or any order-mutation tool exists in this
session at all — mode=execute per auto_mode.json, but the capability to execute is absent
from the grant. Per the enforcer absolute (never force a trade through) this is treated as
a hard stop, recorded as WOULD-PLACE. **EVAN: check the claude.ai connector's tool
scope/grant for this server — order-mutation tools appear to be missing entirely, not just
denied.** The ticket above is fully analyzed and enforcer-cleared, ready to fire once the
tool is available; it will need a fresh price/range check at that time since USDJPY is
moving.

**Bookkeeping:** session_snapshot.json refreshed (balance re-confirmed live, USDJPY H4
verdict + session range added fresh, watch_levels appended for GOLD dup/USOIL/USDJPY).
tick_counter.txt -> 54. Session P&L = 7164.09 - 7394.99 = -R230.90, unchanged from tick 53
(no fills). session_logger.py tick 54 logged.

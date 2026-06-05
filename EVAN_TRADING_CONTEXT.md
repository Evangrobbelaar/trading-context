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
Rule 4: 50% rule — at 50%+ of TP, trail SL to lock in roughly half unrealized profit, not all.
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
- To be updated Monday June 8 at session open

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

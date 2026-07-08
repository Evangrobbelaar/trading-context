# SPRUNG LADDER v1.0 — Scout & Strike Protocol
*Formulated 8 Jul 2026. Status: SPEC ONLY — not yet live. First deployment requires Evan's go + a qualifying range.*

## Origin
Fixes the martingale grid by inverting its three fatal properties:
| Martingale flaw | Sprung Ladder inversion |
|---|---|
| Size INCREASES as evidence says you're wrong | Size increases ONLY on confirmation you're right |
| Grid rungs ARE the position (unbounded risk) | Rungs are SENSORS (fixed, tiny, known max cost) |
| Path-blind: can't tell drift from trend | Scout death-rate IS the regime detector (kill-switch) |

## Preconditions (ALL required)
1. Instrument in a proven range: >=2 touches each side on H1, range width >= 3x the Asian/London SL minimum (Rule 15)
2. No high-impact news for the instrument within 2h (doc news rule)
3. NOT a one-sided regime day (e.g. war-escalation USD day = banned)
4. Account: scouts total risk <= 2% of balance; strike risk <= 5%

## Phase 1 — MAP
Place 3 scout BUY LIMITS (0.01 lots each) at sweep zones: 5-15 pts BELOW the range low and the two next structural shelves. Each scout: SL 25-35 pips (Rule 15), no TP yet. Max total scout risk ~R120-150 at current balance.

## Phase 2 — LISTEN (the kill-switch)
- If ALL scouts stop out within 90 min of first fill => TREND verdict. ABORT protocol. Loss = scout cost only. Do NOT re-arm same instrument for 24h.
- If a scout fills and price holds within 10 pips of it for >=15 min => candidate spring. Go to Phase 3 watch.

## Phase 3 — SPRING TRIGGER (all 3 required)
1. Level swept (scout filled below structure)
2. Price RECLAIMS the structural level within 15 min of the sweep
3. One full M5 close above the reclaimed level

## Phase 4 — STRIKE
Market buy 0.07-0.10 lots on trigger. SL = 3-5 pips below the sweep extreme (structural invalidation, NOT arbitrary tightness). Initial target = range mean.

## Phase 5 — ANTI-MARTINGALE EXIT
- Close 50% of strike at range mean; move SL to breakeven on remainder
- Trail remainder behind M15 higher-lows toward range high
- Scouts inherit the strike's trailing stop (they're now profit, not sensors)

## Hard bans
- NEVER increase rung size on the way down. NEVER add a 4th scout. NEVER re-arm after a trend verdict same day.
- NEVER deploy against the active macro regime direction.
- Sells mirror all rules (sweep of range HIGH, reclaim downward).

## Provenance (why we believe the spring edge)
- Jul 6-7 log: XAUUSD counter-trend at swept extreme +R512; USDJPY sweep-fade wins
- Jun 25 log: being ON THE WRONG SIDE of Asian sweeps cost -R1,240 — this protocol makes us the counterparty of that pattern instead of its victim

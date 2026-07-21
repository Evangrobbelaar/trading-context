# PINE SIGNAL PERFORMANCE REVIEW — Day 1 live (21 Jul 2026, 13:15–19:30 UTC)

Deployed script: `sprung_ladder_signals_v2_auto.pine` on 15m charts (GOLD, SILVER, EURUSD,
USDJPY, BTCUSD, USOIL, XAUUSD1!). 21 real events in 6.3h = 3.4/hour. 7 of 20 inter-event
gaps were under 60 seconds — signals cluster hard on shared impulses.

## Scorecard by event type

| Event | Fired | Outcome grade |
|---|---|---|
| SPRING | 4 | **Best signal.** GOLD 14:30 → struck (tick 41) → winner, Rule-14 locked (+R82 min, peaked +R298). SILVER correctly skipped (theme cluster). BTC 19:30 correctly skipped (Rule 16 window). XAUUSD1! = futures dupe. 1 tradeable spot spring → 1 winner. |
| HL_RECLAIM | 9 | **Real signal, wrong entry moment.** 2 valid trends flagged (USDJPY 13:45 + 18:15 — both continued, both unenterable at signal price under Rule 17). 1 traded via pullback limit (BTC 14:00 → filled on retest, stopped −R178). 1 failed fast (USOIL 13:30). 3 late-continuation info. 2 futures dupes. |
| SWEEP | 8 | Info-only by design (Phase 2). EURUSD 1.1403 double-sweep (19:00 + 19:30, 0.2p apart) = first live defended-shelf signature — the pattern the whole strategy hunts. Rest were impulse-bar artifacts. |

## Faults found (with root cause)

1. **Tick 39's "webhook strips direction" diagnosis was WRONG.** The receiver strips nothing.
   The deployed v2 pine never sends direction, `level`, `sweep_extreme`, or ATR — those fields
   only exist in the older root monitor script that is not deployed. Also: v2 has **no
   high-side sweep logic at all** (`low < shelf and close > shelf` only), so every "SWEEP"
   was a low-side poke-and-recover; on wide impulse bars that *looks* like an upside break,
   which is what tick 39 reconstructed. Fix belongs in Pine, not the receiver.
2. **XAUUSD1! futures chart = 19% of all events (4/21), all noise.** ~16–20pt basis over spot
   forced manual decode every time (tick 42). Remove the futures chart from the alert set.
3. **HL_RECLAIM structurally collides with Rule 17.** It fires on `crossover(close,
   20-bar high)` — by construction it fires at the top of the range, exactly where Rule 17
   blocks buys. The tradeable moment is the *retest* (BTC proved it: the 66,700 pullback
   limit filled 22 min after the reclaim). The signal is an ARM event, not an ENTER event.
4. **No short-side coverage.** v2 has HL_RECLAIM (long) but no LL_BREAKDOWN mirror; no
   SWEEP_HIGH / SPRING_SHORT. Today was a one-way-up day so it didn't bind — it will.
5. **Spring window semantics.** springWindow=3 bars on a 15m chart = 45-min reclaim window;
   the protocol's Phase 3 is a 15-min reclaim. On 15m charts set springWindow=1 (or run M5
   charts with window=3).

## Changes shipped in v3 (`sprung_ladder_signals_v3_auto.pine`)

- Direction-explicit events: SWEEP_LOW / SWEEP_HIGH, SPRING_LONG / SPRING_SHORT,
  HL_RECLAIM / LL_BREAKDOWN (short mirror added).
- **PULLBACK_TAG_LONG / _SHORT** — after a reclaim/breakdown, the broken level is armed and
  the event fires when price *retests* it (tolerance + window inputs). This converts fault #3
  into an automated, Rule-17-compliant entry trigger — the exact flow ticks 37/38 ran by hand.
- Payload now carries: `level`, `extreme`, `range_pos` (0–1 position in the day range → the
  runner and enforcer get Rule 17 for free), `vol_mult` (bar vol / 20-SMA), `h1_atr`.
- Per-event cooldown input (default 5 min) — kills same-impulse duplicate spam without
  hiding the 30-min-apart shelf-signature repeats.
- springWindow default changed to 1 (15m charts).
- Old event names remain understood by the runner (back-compat map), so v2 keeps working
  until the v3 paste happens.

## Verdict

Day 1: the pipeline's one clean SPRING produced the day's best trade, HL_RECLAIM correctly
identified two real trends but at unenterable prices, and 19% of traffic was removable
futures noise. The script detects well; v3 makes it *say what it saw* (direction + level)
and adds the retest event that turns detection into rule-legal entries.

# Lesson: Range Trap Detection

**Date discovered:** June 23, 2026
**Instruments:** XAUUSD (4105–4122 range)

## What happened
H4 was confirmed bearish on XAUUSD. Three separate short entries were taken across the session — all within the same 17-point band (4105–4122). Each entry was valid per CHANGE 2 + CHANGE 5, but price oscillated violently within the range with no follow-through in either direction.

Outcome: 2 Rule 5 cuts + 1 SL hit, all in the same price zone. Net session loss on Gold despite correct H4 read.

## The root cause
H4 bear trend does NOT guarantee M5/M15 will trend intraday. On ranging days:
- H4 makes lower highs → technically bearish
- But intraday (M5/M15) keeps reverting to same horizontal band
- Every "breakdown" reverses within 5–10 candles

## Detection signals (check before 3rd entry in same zone)
1. **Same resistance hit 2× in same session** — if price returned to and rejected from the same level twice, the level is holding. Don't enter again.
2. **M5 candle body size shrinking below average** — compression before expansion; direction unknown.
3. **H4 swing low not tested yet** — if price is stuck in a 17pt band and H4 swing low is 30pts below, market may be building energy, not trending.
4. **NY/London midday session** (12:00–15:00 SAST) — lowest volume, highest ranging probability.

## Rule (added post June 23)
After 2 Rule 5 cuts on the same instrument in the same session:
1. Mark that instrument as RANGE_DAY — no re-entry
2. Shift focus to other watchlist instruments
3. Log: "XAUUSD [date] — range trap. Avoided 3rd entry."

## Anti-pattern to avoid
- "The H4 is still bearish so I'll try again" → No. The H4 read is correct but the intraday environment doesn't support it today.
- "Price is at the top of the range, easy short" → No. A range has no trend by definition.

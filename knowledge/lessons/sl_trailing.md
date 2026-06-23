# Lesson: SL Trailing — Closing Prices Only

**Date discovered:** June 23, 2026
**Instrument:** XAUUSD

## What happened
Trade: XAUUSD short, entry 4109.65.
Price dropped to a 9-point pin bar with wick low at 4105.26.
SL trailed from 4126.32 to 4120.26 (using: wick low 4105.26 + 15pt buffer = 4120.26).
Price spiked back up and hit SL at 4120.27 — one pip through. Loss: -R175.

If SL had been trailed using CLOSING price (4110.xx range during those M5 candles), it would have remained at ~4125 and survived the spike.

## The rule
**Always use CLOSING prices for SL reference. Never wick extremes.**

Wicks are noise — they represent momentary stop hunts, spread spikes, and news reactions.
The closing price is where the market agreed to settle.

### For trailing SL on shorts:
- Find the most recent M5 or M15 swing LOW — use the **candle close**, not the wick
- Add minimum buffer (15pts for Gold, 15 pips for Forex)
- Only trail when Rule 14 trigger is met (+R80 float for Gold)

### Formula
```
new_sl_short = recent_swing_low_CLOSE + buffer
# NOT: recent_wick_low + buffer
```

## Red flags that indicate a wick-based error
- The swing "low" is a single spike candle with a tiny body
- The next M5 candle closes above the spike's low
- Body of spike bar is in the top 30% of the bar range

## When NOT to trail
- Within the first 30 minutes after entry (let the trade breathe)
- During high-impact news release windows (spike bars are noise, not structure)
- If the trailing move would reduce SL buffer below 15pts (Gold)

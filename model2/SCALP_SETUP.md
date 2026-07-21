# SCALP LOOP — QUICK REFERENCE

**Account:** Demo #41829612 | **Base:** ZAR | **Balance:** ~R4,835
**Sessions:** London 09:00–12:00 SAST | London/NY overlap 15:00–18:00 SAST

---

## MORNING SETUP (08:45 SAST)

### Step 1 — Fetch H1 candles and write temp file
Claude calls `mcp__claude_ai_claude__get_symbol_history` for each instrument (H1, 24 candles),
then writes `scalp_candles_temp.json` in this format:

```json
{
  "EURUSD": {
    "current_price": 1.13816,
    "candles": [
      {"time": "...", "open": 1.138, "high": 1.1385, "low": 1.1375, "close": 1.1382},
      ...
    ]
  },
  "XAUUSD": { "current_price": 4121.70, "candles": [...] }
}
```

### Step 2 — Run level calculator
```bash
python scalp_levels.py --symbol EURUSD --symbol GBPUSD --symbol XAUUSD --symbol USDJPY
```
Output: `scalp_state.json` with key S/R levels, SL/TP, R:R for each instrument.

### Step 3 — Check news
Read `../tradeloop/news_impact.json`. If `high_impact_2h = true` → wait until M15 settles after print.

### Step 4 — Start loop
Type: **"start scalp loop"**

---

## STARTING THE LOOP

Claude will:
1. Confirm account is demo #41829612
2. Read `scalp_state.json` — confirm levels loaded
3. Check `news_impact.json` — confirm no news block
4. Start 60-second ticks via `/loop 1m [scalp tick protocol]`

---

## SCALP TICK PROTOCOL (every 60 seconds)

```
STEP 0  Lock:     python tick_lock.py acquire --lock-file scalp.lock
STEP 1  Time:     Check SAST — London or London/NY only
STEP 2  State:    Read scalp_state.json — check loop_stopped, trades, losses
STEP 3  Watch:    python scalp_monitor.py --symbol X --price [current]
STEP 4  Confirm:  If AT_LEVEL → fetch 5 M5 candles → write scalp_m5_temp.json → re-run monitor
STEP 5  Enforce:  python scalp_enforcer.py --symbol X --direction X --lots X ...
STEP 6  Trade:    mcp create_market_order → mcp modify_position (SL/TP)
STEP 7  Monitor:  Check open scalp position P&L + time stop (20 min)
STEP 8  Unlock:   python tick_lock.py release --lock-file scalp.lock
STEP 9  Next:     ScheduleWakeup delaySeconds=60
```

---

## OUTPUT FORMAT

### Quiet tick (all watching):
```
SCALP TICK 5 | 15:23 SAST | EURUSD: 1.13791 | GBPUSD: 1.31962 | XAUUSD: 4121.70
All levels: WATCHING. Next check in 60s.
```

### Level approaching:
```
SCALP TICK 6 | 15:24 SAST
⚠ EURUSD NEAR LEVEL — 1.14050 resistance (2.3 pips away)
Watching for rejection. M5 check will trigger at ≤1 pip.
```

### Trade triggered:
```
SCALP TICK 7 | 15:25 SAST
🎯 EURUSD AT LEVEL — 1.14050 resistance
M5 CONFIRMATION: bearish rejection candle (close 1.14031, wick to 1.14055) ✅
ENFORCER: PASS — R27 risk, R55 reward, 2.0:1 R:R
ORDER PLACED: SELL EURUSD 0.03L @ 1.14031 | SL: 1.14120 | TP: 1.13830
```

### In-trade:
```
SCALP TICK 8 | 15:26 SAST
EURUSD SHORT | Entry: 1.14031 | Now: 1.13960 | P&L: +R38.60 (70% to TP)
Time in trade: 1 min | Time stop: 19 min remaining
M1: continuing lower ✅ | Action: HOLD
```

### Time stop:
```
SCALP TICK 28 | 15:45 SAST
EURUSD SHORT | Entry: 1.14031 | Now: 1.14010 | P&L: +R11.50
⏱ TIME STOP — 20 minutes reached, TP not hit
CLOSING position — Result: +R11.50
```

---

## STOPPING THE LOOP

Type: **"stop scalp"** or **"stop loop"**

Loop also auto-stops when ANY:
- 2 consecutive losing scalps
- 3 scalp trades placed this session
- Session drawdown > R200
- Outside session window
- `high_impact_2h = true` in news_impact.json

---

## LOT SIZES & RISK (default)

| Instrument | Lots | SL   | Risk ZAR | TP    | Reward ZAR | R:R |
|------------|------|------|----------|-------|------------|-----|
| EURUSD     | 0.03 | 5pip | R27      | 10pip | R55        | 2:1 |
| GBPUSD     | 0.03 | 5pip | R35      | 10pip | R69        | 2:1 |
| USDJPY     | 0.03 | 5pip | R17      | 10pip | R34        | 2:1 |
| XAUUSD     | 1u   | 5pt  | R80      | 10pt  | R160       | 2:1 |

---

## INSTRUMENTS — DO / DO NOT

**Scalp:**  EURUSD ✅ | GBPUSD ✅ | USDJPY ✅ | AUDUSD ✅ | XAUUSD ✅ (high confidence only)

**Never scalp:** GBPJPY ❌ | EURJPY ❌ | XAGUSD ❌ | NAS100/SPX500/US30 ❌

**Correlation rule:** Only one open at a time within correlated pairs:
- EURUSD + GBPUSD (both USD pairs)
- AUDUSD + NZDUSD (both commodity currencies)
- XAUUSD is uncorrelated — can run alongside one forex scalp

---

## KEY RULES (from June 23 lessons)

1. Never re-enter same instrument/direction after 2 Rule-5 cuts in the same session
2. SL based on candle CLOSE prices only — never on spike wicks
3. If a price level has rejected you twice today, skip that instrument
4. Identify ranging vs trending BEFORE entry — two bounces from same range = skip
5. Time stop: 20 minutes — close trade if TP not reached regardless of P&L

---

## FILE REFERENCE

| File | Purpose |
|------|---------|
| `scalp_state.json` | Live loop state (levels, counters, stop flags) |
| `scalp_candles_temp.json` | H1 OHLCV input for `scalp_levels.py` (written by Claude) |
| `scalp_m5_temp.json` | M5 candles input for `scalp_monitor.py` (written by Claude) |
| `scalp_log.jsonl` | All ticks and trade results |
| `scalp_enforcer_audit.jsonl` | Every enforcer decision |
| `scalp.lock` | Active tick lock (auto-managed) |

---

## RESETTING STATE BETWEEN SESSIONS

At the start of each new trading day, delete or reset counters in `scalp_state.json`:
```json
{
  "scalp_trades_today": 0,
  "consecutive_losses": 0,
  "session_pnl_zar": 0,
  "loop_active": false,
  "loop_stopped": false,
  "stop_reason": null
}
```
Or just re-run `scalp_levels.py` — it preserves counters but you can manually edit the JSON.

---

## ENFORCER QUICK TEST

```bash
# Should PASS:
python scalp_enforcer.py --symbol EURUSD --direction short --lots 0.03 \
  --balance 4835 --sl_distance_pips 5 --tp_distance_pips 10 --account demo

# Should BLOCK (SL too tight):
python scalp_enforcer.py --symbol EURUSD --direction short --lots 0.03 \
  --balance 4835 --sl_distance_pips 2 --tp_distance_pips 5 --account demo
```

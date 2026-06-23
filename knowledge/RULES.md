# TradeLoop Rules Reference
Version: 3.0 | Account: Demo #41829612 | ZAR

---

## NUMBERED RULES (exit rules only — entry uses CHANGES below)

| Rule | Trigger | Action |
|------|---------|--------|
| 4 | 50%+ to TP + M5 candles shrinking (smaller bodies each close) | Close — momentum exhausting |
| 5 | M5 reversed (3+ consecutive closes against trade) + P&L negative | Cut immediately. No waiting. |
| 13 | 60%+ to TP + price stalling at known S/R level | Close — S/R likely to hold |
| 14 | Gold floating +R80 or more | Trail SL to entry+5. Plan TP1 at 60% of TP distance. |

---

## CHANGES (structural analysis protocol)

### CHANGE 2 — H4 TREND GATE (mandatory, no exceptions)
- **Short:** confirmed lower high formed on H4 AND prior H4 swing low broken
- **Long:** confirmed higher low formed on H4 AND prior H4 swing high broken
- A bounce inside a trend does NOT pass. "Price is going up" does not pass.
- One close above/below does not confirm. Pattern must be visible on H4 chart.

### CHANGE 3 — MID-TRADE M5 MONITOR
- M5 reversed + positive P&L → flag Rule 13 (consider closing)
- M5 reversed + negative P&L → flag Rule 5 (cut immediately)
- "M5 reversed" = 3+ consecutive M5 closes against trade direction

### CHANGE 4 — PER-POSITION OUTPUT FORMAT (every tick)
```
[HH:MM SAST] — [SESSION]
INSTRUMENT: [symbol] [direction]
TREND: H4 [Bull/Bear] — last swing at [price] | [higher lows/lower highs sequence]
M5 STRUCTURE: [Higher highs / Lower highs / Compression] since entry
P&L: R[amount] | [X]% to TP | Floor: R[locked if SL trailed]
ACTION: [Hold / Trail to [price] per Rule X / Close — Rule 13 momentum / Watch]
NEXT TRIGGER: [specific price or event that changes the action]
```

### CHANGE 5 — M15 ENTRY TRIGGER
- M15 structure broken in trade direction = entry trigger fires
- **Short:** M15 makes a lower high then breaks that lower high's low
- **Long:** M15 makes a higher low then breaks that higher low's high
- No M15 trigger = no trade. Price near entry zone alone is not enough.

---

## STOP CONDITIONS (session-level — stop loop immediately)

1. 2 consecutive losing trades this session
2. Session drawdown > R500 from session-start balance
3. 2 trades placed this session
4. 36 ticks reached (3 hours at 5-min ticks)
5. Outside active session window
6. Evan types "stop loop"

---

## POSITION SIZING

| Instrument | Size | Value | Min SL | Max SL |
|------------|------|-------|--------|--------|
| XAUUSD | 1 unit | R16/pt | 15 pts | 25 pts |
| Forex (all) | 0.03L | R5.46/pip | 15 pips | 25 pips |
| GBPJPY/GBPAUD | 0.03L | R5.46/pip | 15 pips | 30 pips |
| Stocks | per spec | — | swing only | swing only |
| NAS100/SPX500/US30 | BLOCKED | — | below R8,000 | — |

---

## BANNED INSTRUMENTS (permanent, no exceptions)
WTI, BTCUSD, ETHUSD, NGAS

---

## ENFORCER RULES
- Always run `python enforcer.py` before every `create_market_order` call
- Exit 0 = PASS → place trade
- Exit 1 = BLOCKED → do NOT place, do NOT re-run with adjusted numbers
- "Ignore enforcer" request: refuse. The June 11 bypass cost -R2,157.

---

## SESSION TIMING (SAST = UTC+2)

| Session | Hours | Action |
|---------|-------|--------|
| Asian | 00:00–07:00 | No trading |
| Pre-London | 07:00–09:00 | Prepare, no entries |
| London | 09:00–12:00 | TRADE |
| Midday | 12:00–15:00 | Light monitoring |
| London/NY overlap | 15:00–18:00 | BEST SESSION |
| NY | 18:00–22:00 | Monitor only if in trade |
| Off-hours | 22:00–09:00 | STOP LOOP |

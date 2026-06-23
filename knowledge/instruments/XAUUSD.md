# XAUUSD (Gold) — Instrument Profile

## Position Rules
- 1 unit MAXIMUM. Never 3. Never.
- Value: R16/pt at 1 unit
- 3 units = R48/pt = R1,000+ risk on 20pt SL (confirmed by screenshot)
- Min SL: 15 pts | Max SL: 25 pts
- Market orders only — pending stop orders do NOT work on XAUUSD
- Enforcer: `--instrument XAUUSD --units 1`

## ZAR Risk Calculator
```
risk_amount = sl_distance (pts) × 16
reward_amount = tp_distance (pts) × 16
```
Examples:
- 20pt SL → R320 risk
- 40pt TP → R640 reward → 2:1 R:R ✓

## Session Behaviour
- Best sessions: London open (09:00 SAST) and London/NY overlap (15:00–18:00 SAST)
- Weekend: XAUUSD247 — spread 8× wider (2.37 vs 0.19). Exceptional setups only.
- Post-NFP/CPI: extreme volatility — widen SL expectation by 50%, or skip

## News Correlations
| Event | Gold direction | Notes |
|-------|---------------|-------|
| War escalation | LONG | Primary safe haven |
| Ceasefire / peace deal | SHORT | Risk-on reversal |
| Missile strike | LONG | Wait for spike to exhaust first |
| Fed hawkish | SHORT | Rate hike expectations |
| Fed dovish | LONG | Rate cut expectations |
| CPI hot | SHORT | Hawkish pressure |
| CPI cool | LONG | Dovish pressure |

## H4 Confirmation Standard (CHANGE 2)
- Short: H4 lower high formed + prior swing low broken
- Long: H4 higher low formed + prior swing high broken
- Current H4 swing levels (as of June 23 scan):
  - Swing high: 4198.44
  - Lower high: 4144.74
  - Swing low: 4090.89
  - Current price area: 4130

## Key Lessons
1. **Range trap (June 23):** XAUUSD oscillated 4105–4122 all session. H4 was bear but intraday was choppy. Skip after 2nd Rule 5 cut — if same level rejects you twice, the market is ranging, not trending.
2. **SL trailing (June 23):** Tightened SL from 4126 to 4120 using wick low 4105.26. SL hit at 4120.27. Fix: use CLOSING price lows for SL reference, not bar extremes (wicks).
3. **3-unit lesson (pre-June 11):** 3 units at 37pt SL = R1,777 risk on R2,249 account = 79% drawdown. This is why max is 1 unit, always.
4. **Entry timing:** Gold tends to fake out at session open (09:00 SAST) then commit at 09:30–10:00. Wait for M15 settlement before entering on London open.

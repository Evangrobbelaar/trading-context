# Forex Instruments — Profile

## Universal Rules (all major pairs)
- Max size: 0.03 lots intraday London/NY | 0.01 lots overnight swing
- Value at 0.03L: R5.46/pip
- Min SL: 15 pips | Max SL: 25 pips (GBPJPY/GBPAUD: 30 pips)
- Enforcer: `--instrument [PAIR] --lots 0.03`

## ZAR Risk Calculator (0.03L)
```
risk_amount = sl_pips × 5.46
reward_amount = tp_pips × 5.46
```
Examples:
- 20pip SL → R109.20 risk
- 50pip TP → R273 reward → 2.5:1 R:R ✓

## Instrument Profiles

### EURUSD — Primary forex short (H4 bear June 2026)
- Entry zone SHORT: 1.14000–1.14100
- SL: 1.14220 (22 pips) | TP: 1.13500 (60 pips) | R:R: 2.7:1
- Invalidation: H4 close above 1.14387 (current swing high)
- News: Fed hawkish → short. Fed dovish → long. War escalation = EUR weak.

### GBPUSD — Secondary forex short
- Entry zone SHORT: 1.32100–1.32200
- SL: 1.32280 (18 pips) | TP: 1.31400 (80 pips) | R:R: 4.4:1
- Invalidation: H4 close above 1.32350
- More volatile than EUR — wider spreads at session open

### AUDUSD — Commodity-correlated short
- Entry zone SHORT: 0.6928–0.6940
- SL: 0.6953 (19 pips) | TP: 0.6880 (68 pips) | R:R: 3.6:1
- Invalidation: H4 close above 0.6950
- Correlated with NZDUSD — do NOT hold both simultaneously
- June 23 lesson: 2× Rule 5 cuts in same session = reset rule for new session

### NZDUSD — Correlated with AUDUSD
- Entry zone SHORT: 0.5678–0.5690
- SL: 0.5700 (20 pips) | TP: 0.5630 (60 pips) | R:R: 2.4:1
- WARNING: High correlation with AUDUSD. If AUDUSD position open, skip NZDUSD.

### GBPJPY — Cross pair (wider SL allowed)
- Entry zone SHORT: 213.400–213.550
- SL: 214.300 (80 pips) | TP: 212.000 (150 pips)
- Max SL: 30 pips (structure needs more room)
- Verify JPY lot sizing before trading

### USDJPY — Range/choppy (skip June 2026)
- H4 status: range_skip
- Monitor for breakout above/below range boundaries

### USDCHF — Choppy (skip June 2026)
- H4 status: bull_choppy_skip
- Not trending — skip until structure clarifies

## Correlated Pairs — Risk Management
| Group | Pairs | Rule |
|-------|-------|------|
| USD shorts | EURUSD, GBPUSD, AUDUSD, NZDUSD | Max 2 simultaneous positions |
| AUD/NZD | AUDUSD, NZDUSD | Never hold both at once |
| JPY crosses | USDJPY, GBPJPY, EURJPY | Max 1 at a time |

## Session Timing for Forex
- London open (09:00 SAST): Highest volume, best setups
- London/NY overlap (15:00–18:00 SAST): Second best — USD moves
- Avoid: 22:00–07:00 SAST (thin liquidity, wide spreads)

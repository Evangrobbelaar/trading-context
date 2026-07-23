# STRATEGY: Opening Range Breakout (ORB v1)

**Status:** PROPOSED — not deployed. Zero forward trades. Read the limits section.
**Built:** 23 Jul 2026, to Evan's spec: max 3h hold, 2 intraday trades/day.
**Replaces:** Sprung Ladder v1.1 (see WHY below).
**Script:** `tv-pipeline/pine/orb_v1.pine`

## WHY the Sprung Ladder was the wrong fit

Not a market judgement — a structural one. Measured tick cadence 22 Jul 2026:
median gap 8min, **mean 39min**, max 248min, 36% of gaps >15min. The Sprung
Ladder requires a reclaim inside 15 minutes of the sweep. A third of its trigger
windows opened and closed between two ticks. It was a sit-and-watch strategy
running on a loop that doesn't sit and watch.

Separately, it fades extremes. Trend continuation has the stronger evidence base
(Moskowitz/Ooi/Pedersen 2012 across 58 instruments; Gao/Han/Li/Zhou 2018 intraday).

## WHY ORB fits

1. **It fires on a clock, not on price.** The range completes at open+5min
   regardless of whether anything is watching. Schedule ticks at 09:05 and
   15:35 SAST and latency stops being a variable. This is the whole argument.
2. **The alert carries the full plan** (entry/SL/TP/expiry) at range close, so
   the executor can rest a stop order and let the broker fill it.
3. **Two sessions = two trades/day**, structurally, without a counter.
4. **Time-boxed by construction** — TIME_EXIT event at +180min.

## Evidence

| Source | Scope | Finding |
|---|---|---|
| Zarattini & Aziz 2023 | QQQ, 2016-2023, 2 bear markets | 5-min ORB beat buy-and-hold w/ leverage |
| Zarattini, Barbon & Aziz 2024 (SFI 24-98) | 7,000+ US stocks 2016-2023 | "Stocks in Play" filter materially improves net of costs |
| QuantConnect replication | independent | ~2.4 Sharpe, beta ~0 |
| Holmberg/Lonnbark/Lundstrom 2013 | Financ Res Lett 10:27-33 | earlier intraday ORB profitability work |
| Crabel 1990 | futures | foundational volatility-breakout text |

5-minute range was the best-performing duration tested.

## Sessions (SAST = UTC+2)

| | Range forms | Entry from | Time stop |
|---|---|---|---|
| London | 09:00-09:05 | 09:05 | 12:05 |
| New York | 15:30-15:35 | 15:35 | 18:35 |

Set the session inputs in *exchange* time of the symbol; the script converts.

## Rules

- **Setup:** first 5min of session establishes OR high/low.
- **Filters:** OR size between 0.15x and 2.0x ATR (rejects dead opens and gap
  chaos); relative volume >= 1.5x (Stocks-in-Play proxy — **turn OFF for FX**).
- **Direction:** optional first-bar-close filter (Zarattini QQQ variant): only
  take the side the opening bar closed on.
- **Entry:** stop order 2 ticks beyond the OR extreme.
- **SL:** opposite side of the OR. **TP:** 2R default.
- **Exit:** TP, SL, or TIME_EXIT at +180min — whichever first. No overnight.

## Instrument fit (spread as % of daily range, measured 23 Jul 2026)

| | cost | verdict |
|---|---|---|
| NAS100 | 0.36% | **best fit** — direct QQQ analogue, real volume |
| SPX500 / GER40 | ~ | good — index, real volume |
| TSLA / NVDA | ~ | good — real volume, Stocks-in-Play filter works |
| BRENT / WTI | 0.53 / 0.64% | usable, but oil feed decoupling open (FLAG-001/002) |
| EURUSD & FX majors | 2.92% | **weakest** — 8x costlier than NAS100, no real volume |

Start on NAS100. It is the closest thing in this account to the instrument the
research was actually run on.

## Limits — read before sizing up

- Published on **US equities**. FX/CFD microstructure differs. Unproven here.
- Headline returns lean on **leverage**, which is symmetric and is not edge.
- The relative-volume filter drove much of the documented edge; **FX has no
  reliable volume**, so expect plain FX ORB to be weaker.
- Published edges decay after publication.
- **Same bar as every other strategy: 30 closed trades or 2 weeks before any
  sizing conversation.** Learn mode 0.01 lots until then. The Sprung Ladder was
  deployed on a spec and cost R55 to find out; do not repeat that with size.

## Deployment checklist

1. Add `orb_v1.pine` to TradingView, run on 1m or 5m chart.
2. Start with NAS100 only. `useRVol = true`.
3. Alert condition "Any alert() function call" -> VPS webhook.
4. Schedule runner ticks at 09:05 and 15:35 SAST.
5. Executor: handle OR_COMPLETE (rest the stop order), ORB_LONG/SHORT
   (confirmation/log), TIME_EXIT (flatten).
6. Run 2 weeks in learn mode. Then measure.

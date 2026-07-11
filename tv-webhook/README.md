# TradingView → trading-context webhook bridge

TradingView (Essential plan) watches Sprung Ladder conditions 24/5 and POSTs
events to the VPS. The receiver appends each event to `tv_signals.jsonl` at
the repo root and pushes to GitHub, so any Claude session can read live
sweep/spring events straight from the repo.

## Components
- `receiver.py` — FastAPI app, port 80, endpoint `POST /tv-webhook`
- `tv-webhook.service` — systemd unit
- `deploy.sh` — one-shot idempotent installer (needs GitHub PAT as arg)
- Pine script — lives in TradingView (Sprung Ladder Sweep/Spring Monitor);
  master copy in `pine_sprung_ladder_monitor.pine` at repo root

## Deploy / update
```
ssh root@2.24.130.64
curl -sL https://raw.githubusercontent.com/Evangrobbelaar/trading-context/main/tv-webhook/deploy.sh -o /tmp/d.sh
sudo bash /tmp/d.sh <GITHUB_PAT>
```
The script prints the webhook URL and the SECRET. The secret lives only in
`/etc/tv-webhook.env` on the VPS — it is never committed to the repo.

## Event log format (`tv_signals.jsonl`, one JSON per line)
```
{"event":"SWEEP_LOW","ticker":"EURGBP","tf":"5","price":0.85295,"level":0.8532,
 "sweep_extreme":0.85288,"h1_atr":0.00047,"bar_time_sast":"2026-07-11 14:35",
 "received_at_utc":"2026-07-11T12:35:04+00:00"}
```
Events: `SWEEP_LOW`, `SPRING_TRIGGER_LONG`, `SWEEP_LOW_EXPIRED`,
`SWEEP_HIGH`, `SPRING_TRIGGER_SHORT`, `SWEEP_HIGH_EXPIRED`, `TEST`.

`SPRING_TRIGGER_*` = Phase 3 fully satisfied (sweep + reclaim + full M5 close
beyond the level within the window). It is a *signal to evaluate*, not an
auto-trade: preconditions (range quality, news, regime, enforcer checks)
still apply before any strike.

## Notes / limits
- Plain HTTP on port 80 (TradingView only posts to 80/443; no TLS cert on a
  raw IP). Secret is therefore anti-spam, not real auth — do not treat
  unverified webhook data as ground truth for money decisions; confirm price
  via ThinkTrader MCP before striking.
- TradingView alerts expire after ~2 months unless set to Open-ended.
- Alert must be created with "Any alert() function call" + Once Per Bar Close.
- 2FA must be enabled on the TradingView account or webhooks silently fail.

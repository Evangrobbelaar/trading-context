# tv-pipeline — TradingView eyes for the trading system

TradingView watches the market 24/5 and fires structured JSON events (SWEEP, SPRING,
HL_RECLAIM, LEVEL_HIT) at the VPS the moment they happen. The receiver appends them to
tv_signals.jsonl and pushes to GitHub, so every Claude trading session opens with the
overnight signal history already in context. Execution stays 100% manual in ThinkTrader.

    TradingView (Pine v6, alert webhooks)
        -> http://2.24.130.64/tv-signal   (nginx, port 80 — TV requirement)
        -> FastAPI receiver 127.0.0.1:8091 (systemd: tv-receiver)
        -> tv_signals.jsonl  -> git push  -> read by Claude at session start

## Automation split
- Built already (this repo): Pine script, receiver, systemd unit, nginx route, tests, docs.
- Claude Code automates: VPS audit, deploy, key generation, service + nginx setup, end-to-end test (~everything with an API or a shell).
- You, manually (~10 min, SETUP_CHECKLIST.md): paste the Pine script into TradingView and create one alert with the webhook URL — TradingView has no upload API.

## Run it
On Windows: install Claude Code once (irm https://claude.ai/install.ps1 | iex), then from
this folder run: claude — it reads CLAUDE.md and takes over.

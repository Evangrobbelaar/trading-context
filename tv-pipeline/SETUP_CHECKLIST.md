# The 10 manual minutes (TradingView has no API for this part)

1. tradingview.com -> open chart CAPITALCOM:US100, timeframe 15m, timezone Africa/Johannesburg.
2. Pine Editor (bottom panel) -> paste pine/sprung_ladder_signals.pine -> Save -> Add to chart.
3. Gear icon on the "SLS" indicator -> set inputs: shelf = current Sprung Ladder shelf (e.g. 28936), Alert level 1/2 = today's ticket alerts (e.g. 29065 / 28955). Zero = off.
4. Alt+A -> Condition: "Sprung Ladder Signals v1" -> "Any alert() function call".
5. Notifications tab -> tick Webhook URL -> paste: https://tv-signal.srv1695304.hstgr.cloud/tv-signal?key=YOUR_REAL_KEY (Claude Code gives you this). Message box: leave as-is — the script supplies the JSON.
6. Also tick "Push to app" so your phone buzzes on every event.
7. Expiration: set to Friday; recreate weekly (alert quota hygiene).
8. Test: fire deploy/test_signal.ps1, then wait for a real level touch — check tv_signals.jsonl commits on GitHub.
Note: webhook alerts require a paid TradingView plan.

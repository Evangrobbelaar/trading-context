# tv-pipeline — Claude Code mission brief

You are finishing the TradingView -> VPS -> GitHub signal pipeline for Evan.

## System
TradingView Pine script (pine/sprung_ladder_signals.pine) fires alert() webhooks ->
nginx on VPS 2.24.130.64 port 80 (/tv-signal) -> FastAPI receiver on 127.0.0.1:8091 ->
appends to tv_signals.jsonl in /root/trading-context -> auto git commit/push ->
Claude (claude.ai trading sessions) reads signals at session start.

## Hard constraints — do not violate
- VPS ports 8080 (ClockPay engine), 8000 (ClockPay cloud), 8090 (Control Panel) are LIVE ClockPay services. Never bind, restart, or modify them. This pipeline uses 8091 only.
- Never edit enforcer.py, EVAN_TRADING_CONTEXT.md, or tick_counter.txt.
- TradingView webhooks only call ports 80/443 — the nginx route is mandatory, direct :8091 will never receive TV calls.
- Generate a real TV_KEY (32+ random chars), put it in the systemd unit on the VPS. Never commit the real key to git — CHANGE_ME stays in the repo copy.

## Your job, in order
1. Audit: ssh root@2.24.130.64 — check if tv-receiver.service already exists (a June version may exist), what serves port 80 (nginx expected — the Gumroad landing page lives there), and whether /root/trading-context exists with working git push (git -C /root/trading-context pull).
2. Deploy/refresh: copy receiver + unit file, pip install -r requirements.txt (use --break-system-packages if Ubuntu complains), install unit with generated TV_KEY, systemctl daemon-reload && enable --now tv-receiver.
3. Route: add deploy/nginx-tv.conf locations to the port-80 server block, nginx -t, reload.
4. Verify: curl http://2.24.130.64/tv-health then run deploy/test_signal.ps1 with the real key from Evan's machine. Confirm the signal lands in tv_signals.jsonl AND appears as a commit on GitHub.
5. Hand-holding: walk Evan through SETUP_CHECKLIST.md (the manual TradingView part), giving him the exact webhook URL with his real key.
6. If the Pine script fails TV compilation, fix the reported line — keep alert() payloads as single-line JSON.

## Ask Evan before
- Anything touching services other than tv-receiver/nginx; any change to firewall rules.

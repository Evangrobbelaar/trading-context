# tv-pipeline — Claude Code mission brief

You are finishing the TradingView -> VPS -> GitHub signal pipeline for Evan.

## System (revised after 2026-07-21 audit — see below)
TradingView Pine script (pine/sprung_ladder_signals.pine) fires alert() webhooks ->
Traefik on VPS 2.24.130.64 port 443, Host `tv-signal.srv1695304.hstgr.cloud` (/tv-signal) ->
FastAPI receiver, Docker container (labeled for Traefik auto-discovery, internal port 8091) ->
appends to tv_signals.jsonl in /root/trading-context -> auto git commit/push ->
Claude (claude.ai trading sessions) reads signals at session start.

**Audit correction (2026-07-21):** the VPS does not match the architecture originally assumed
above. Traefik (Docker, host networking, `--providers.docker` with `exposedbydefault=false`)
owns ports 80/443, not nginx — it redirects all HTTP to HTTPS and only routes to Docker
containers carrying `traefik.*` labels with a `Host()` rule. nginx is installed but only listens
on port 3000 for an unrelated static site (`claude-ecs`) — it never touches 80/443. Host port
8091 is already bound by a different live service (`claude-github-proxy.service`, a GitHub API
proxy, unrelated to this pipeline) — do not reuse that host port. `*.srv1695304.hstgr.cloud` is
a wildcard DNS already pointed at this VPS, and Traefik already proves the pattern works (valid
Let's Encrypt cert issued for `hermes-agent-dwnm.srv1695304.hstgr.cloud` via the same
docker-label mechanism). Deployment therefore uses `deploy/docker-compose.yml` (a Docker
container + Traefik labels, matching the existing hermes-agent container pattern) instead of a
systemd unit + nginx location block — this avoids the 8091 conflict entirely (the container's
internal port is never published to the host) and requires zero changes to Traefik, nginx, or
any other existing service.

## Hard constraints — do not violate
- VPS ports 8080 (ClockPay engine), 8000 (ClockPay cloud), 8090 (Control Panel) are LIVE ClockPay services. Never bind, restart, or modify them. Host port 8091 is also taken (claude-github-proxy, unrelated) — never bind that either. This pipeline's container never publishes a host port; Traefik reaches it over the Docker bridge network.
- Never edit enforcer.py, EVAN_TRADING_CONTEXT.md, or tick_counter.txt.
- TradingView webhooks only call ports 80/443 — routing through Traefik (the existing docker-label mechanism) is mandatory.
- Generate a real TV_KEY (32+ random chars), pass it to the container via the `TV_KEY` env var (docker-compose `.env` on the VPS, not committed). Never commit the real key to git — CHANGE_ME stays in the repo copy.
- Git push from the VPS needs its own GitHub credential (fine-grained PAT scoped to this repo) baked into the origin remote URL on `/root/trading-context/.git/config` — never commit that path's contents; it's host-local git config, not repo content.

## Your job, in order
1. Audit: ssh root@2.24.130.64 — check if tv-receiver already exists in any form, what actually serves ports 80/443/8091, and whether /root/trading-context exists with working git push. (Done 2026-07-21 — see correction above.)
2. Deploy/refresh: clone /root/trading-context (using the PAT-embedded origin URL), build/run `deploy/docker-compose.yml` under `/docker/tv-receiver/` on the VPS with a generated TV_KEY.
3. Route: nothing extra needed — Traefik's docker provider auto-discovers the labeled container and issues its own cert for `tv-signal.srv1695304.hstgr.cloud`.
4. Verify: curl https://tv-signal.srv1695304.hstgr.cloud/tv-health then run deploy/test_signal.ps1 with the real key from Evan's machine. Confirm the signal lands in tv_signals.jsonl AND appears as a commit on GitHub.
5. Hand-holding: walk Evan through SETUP_CHECKLIST.md (the manual TradingView part), giving him the exact webhook URL with his real key.
6. If the Pine script fails TV compilation, fix the reported line — keep alert() payloads as single-line JSON.

## Ask Evan before
- Anything touching services other than tv-receiver/Traefik-labels-only/nginx; any change to firewall rules, or any change to Traefik's own compose file (the tv-receiver container should only ever need labels, never a Traefik config edit).

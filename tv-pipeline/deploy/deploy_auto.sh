#!/usr/bin/env bash
# deploy_auto.sh — tick 45. Run ON THE VPS as root:
#   cd /root/trading-context && git pull && bash tv-pipeline/deploy/deploy_auto.sh
set -euo pipefail

REPO=/root/trading-context
RUNNER_DIR=/root/tv-runner

echo "== TV auto-tick deploy =="
[ -d "$REPO" ] || { echo "FATAL: $REPO not found"; exit 1; }

# 1. Claude Code CLI
if ! command -v claude >/dev/null 2>&1; then
  echo "-- installing Claude Code (needs Node 18+) --"
  command -v npm >/dev/null 2>&1 || { echo "FATAL: npm missing — install nodejs first (apt install nodejs npm or nodesource)"; exit 1; }
  npm install -g @anthropic-ai/claude-code
fi
echo "claude: $(claude --version 2>/dev/null || echo 'installed, version check needs auth')"

# 2. Runner dirs + service
mkdir -p "$RUNNER_DIR/runs"
cp "$REPO/tv-pipeline/runner/tv-tick-runner.service" /etc/systemd/system/tv-tick-runner.service
systemctl daemon-reload
systemctl enable tv-tick-runner.service
systemctl restart tv-tick-runner.service
sleep 2
systemctl --no-pager --lines=5 status tv-tick-runner.service || true

# 3. Sanity: receiver + repo wiring
echo "-- receiver health --"
curl -fsS http://127.0.0.1:8091/health 2>/dev/null || echo "(receiver health check via localhost failed — check docker)"
grep -q AUTOTRADE_OFF <(ls "$REPO") && echo "NOTE: AUTOTRADE_OFF present — runner will skip signals" || true
echo "mode: $(cat "$REPO/auto_mode.json" 2>/dev/null || echo 'auto_mode.json missing!')"

cat <<'EOT'

== MANUAL STEPS (one-time, cannot be scripted) ==
1. AUTH CLAUDE CODE (only if 'claude' has never been logged in on this box):
     claude          # interactive once; complete login; then /exit
2. CONNECT THINKTRADER MCP:
     claude mcp add --transport http thinktrader https://mcp.thinktrader.com/v1/mcp
     claude          # interactive; run /mcp; complete OAuth (use ssh -L for the browser
                     #  step if needed: ssh -L PORT:localhost:PORT root@VPS); /exit
   The OAuth grant is DEMO-ONLY by design — the live account must never be added.
3. SMOKE TEST (read-only):
     cd /root/trading-context && claude -p "Follow AUTO_TICK_PROTOCOL.md TIER 1. Test run: switch to 41829612, verify, report current XAUUSD price and the snapshot open position in one AUTO-TICK[t1] line. No writes." --model haiku --max-turns 8 --output-format json
4. PHONE NOTIFICATIONS: install the ntfy app, subscribe to the topic in
   tv-pipeline/runner/tiers.json (ntfy_topic).
5. TRADINGVIEW: paste tv-pipeline/pine/sprung_ladder_signals_v3_auto.pine over the v2
   indicator on each SPOT chart (drop the XAUUSD1! futures chart), keep the same alert +
   webhook URL. v2 keeps working until you do — the runner understands both.
6. DRY RUN: mode is 'advise' — nothing gets placed. After reviewing a day or two of
   would-be tickets in the auto ticks, flip auto_mode.json to "execute" and push.
KILL SWITCH any time: touch /root/trading-context/AUTOTRADE_OFF (or add the file via
GitHub from your phone) — runner skips everything while it exists.
EOT

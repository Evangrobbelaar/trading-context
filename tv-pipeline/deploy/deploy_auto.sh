#!/usr/bin/env bash
# deploy_auto.sh — tick 45/46. Fully self-sufficient. Run ON THE VPS as root:
#   cd /root/trading-context && git pull && bash tv-pipeline/deploy/deploy_auto.sh
set -euo pipefail

REPO=/root/trading-context
RUNNER_DIR=/root/tv-runner

echo "== TV auto-tick deploy =="
[ -d "$REPO" ] || { echo "FATAL: $REPO not found"; exit 1; }

# 0. curl (needed for NodeSource + tests)
command -v curl >/dev/null 2>&1 || { apt-get update -y && apt-get install -y curl ca-certificates; }

# 1. Node.js 22 via NodeSource (auto-installed if npm is missing)
if ! command -v npm >/dev/null 2>&1; then
  echo "-- npm missing: installing Node.js 22 (NodeSource) --"
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi
echo "node: $(node --version 2>/dev/null || echo missing) | npm: $(npm --version 2>/dev/null || echo missing)"

# 2. Claude Code CLI
if ! command -v claude >/dev/null 2>&1; then
  echo "-- installing Claude Code --"
  npm install -g @anthropic-ai/claude-code
fi
echo "claude: $(claude --version 2>/dev/null || echo 'installed — needs one-time login')"

# 3. Runner dirs + systemd service
mkdir -p "$RUNNER_DIR/runs"
cp "$REPO/tv-pipeline/runner/tv-tick-runner.service" /etc/systemd/system/tv-tick-runner.service
systemctl daemon-reload
systemctl enable tv-tick-runner.service >/dev/null 2>&1
systemctl restart tv-tick-runner.service
sleep 3
systemctl is-active tv-tick-runner.service && echo "runner service: ACTIVE" || echo "runner service: NOT ACTIVE — check /root/tv-runner/runner.log"
tail -n 3 "$RUNNER_DIR/runner.log" 2>/dev/null || true

# 4. Receiver health (public URL — container port is not bound on the host)
echo "-- receiver health --"
curl -fsS https://tv-signal.srv1695304.hstgr.cloud/health || echo "(receiver health failed — check docker)"
echo ""
[ -f "$REPO/AUTOTRADE_OFF" ] && echo "NOTE: AUTOTRADE_OFF present — runner will skip signals"
echo "mode: $(cat "$REPO/auto_mode.json" 2>/dev/null || echo 'auto_mode.json missing!')"

cat <<'EOT'

============================================================
 REMAINING STEPS — each line below is safe to copy-paste
============================================================

STEP 1 — one-time Claude login (interactive; visit the URL it
prints, paste the code back here, then type /exit):

claude

STEP 2 — connect ThinkTrader MCP (one-time; inside claude run
/mcp and complete the OAuth, then /exit). Demo-only grant.
If the browser step stalls on localhost, reconnect with
ssh -L <port>:localhost:<port> root@2.24.130.64 using the port shown:

claude mcp add --transport http thinktrader https://mcp.thinktrader.com/v1/mcp
claude

STEP 3 — smoke test (read-only, ~30s):

cd /root/trading-context && claude -p "Follow AUTO_TICK_PROTOCOL.md TIER 1. Test run: switch to 41829612, verify, report current XAUUSD price and the snapshot open position in one AUTO-TICK[t1] line. No writes." --model haiku --max-turns 8 --output-format json

STEP 4 — full end-to-end test (fires a fake HL_RECLAIM through
the real public webhook; runner spawns Claude in advise mode,
nothing gets placed; your phone should buzz if ntfy is set up):

KEY=$(docker exec $(docker ps -qf name=tv-receiver | head -1) printenv TV_KEY)
curl -s "https://tv-signal.srv1695304.hstgr.cloud/tv-signal?key=$KEY" -H "Content-Type: application/json" -d "{\"event\":\"HL_RECLAIM\",\"symbol\":\"XAUUSD\",\"tf\":\"15\",\"price\":4075.0,\"t\":$(date +%s000)}"
sleep 120
tail -n 25 /root/tv-runner/runner.log

STEP 5 — phone: install the ntfy app and subscribe to the topic
shown in tv-pipeline/runner/tiers.json (evan-tv-ticks-x9k4q2).

STEP 6 — TradingView: paste tv-pipeline/pine/sprung_ladder_signals_v3_auto.pine
over v2 on each SPOT chart (drop XAUUSD1!). Same alert + webhook URL.

KILL SWITCH any time:  touch /root/trading-context/AUTOTRADE_OFF
GO LIVE after dry-run: edit auto_mode.json to "execute" and git push.
EOT

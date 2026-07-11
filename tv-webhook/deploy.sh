#!/bin/bash
# TradingView webhook receiver — one-shot deploy for the ClockPay VPS.
# Usage:  sudo bash deploy.sh <github_pat>
# Idempotent: safe to re-run. Keeps existing secret if already deployed.
set -euo pipefail

PAT="${1:-}"
if [ -z "$PAT" ]; then
  echo "Usage: sudo bash deploy.sh <github_pat>"; exit 1
fi

BASE=/opt/tv-webhook
REPO_URL="https://Evangrobbelaar:${PAT}@github.com/Evangrobbelaar/trading-context.git"

echo "==> [1/6] Port 80 check"
if ss -tlnp 2>/dev/null | grep -q ':80 '; then
  echo "!! Something is already listening on port 80:"
  ss -tlnp | grep ':80 '
  echo "!! Stop it or change the port in tv-webhook.service, then re-run."
  exit 1
fi

echo "==> [2/6] Python venv + deps"
apt-get update -qq && apt-get install -y -qq python3-venv git >/dev/null
mkdir -p "$BASE"
[ -d "$BASE/venv" ] || python3 -m venv "$BASE/venv"
"$BASE/venv/bin/pip" install -q --upgrade fastapi "uvicorn[standard]"

echo "==> [3/6] Repo clone/update"
if [ -d "$BASE/trading-context/.git" ]; then
  git -C "$BASE/trading-context" remote set-url origin "$REPO_URL"
  git -C "$BASE/trading-context" pull --rebase
else
  git clone "$REPO_URL" "$BASE/trading-context"
fi
git -C "$BASE/trading-context" config user.name  "tv-webhook"
git -C "$BASE/trading-context" config user.email "tv-webhook@vps"

echo "==> [4/6] App files"
cp "$BASE/trading-context/tv-webhook/receiver.py" "$BASE/receiver.py"

echo "==> [5/6] Secret + env"
if [ -f /etc/tv-webhook.env ]; then
  SECRET=$(grep '^TV_WEBHOOK_SECRET=' /etc/tv-webhook.env | cut -d= -f2)
  echo "    (keeping existing secret)"
else
  SECRET=$(openssl rand -hex 16)
  cat > /etc/tv-webhook.env <<EOF
TV_WEBHOOK_SECRET=${SECRET}
REPO_DIR=${BASE}/trading-context
EOF
  chmod 600 /etc/tv-webhook.env
fi

echo "==> [6/6] Systemd"
cp "$BASE/trading-context/tv-webhook/tv-webhook.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now tv-webhook
sleep 2
systemctl is-active tv-webhook >/dev/null || { journalctl -u tv-webhook -n 20 --no-pager; exit 1; }

IP=$(curl -s ifconfig.me || echo "<VPS-IP>")
echo ""
echo "================= DEPLOYED ================="
echo "Webhook URL : http://${IP}/tv-webhook"
echo "Health      : http://${IP}/health"
echo "SECRET      : ${SECRET}"
echo "============================================"
echo "Paste the SECRET into the Pine script's 'Webhook secret' input."
echo "Test:  curl -X POST http://${IP}/tv-webhook -d '{\"secret\":\"${SECRET}\",\"event\":\"TEST\"}'"

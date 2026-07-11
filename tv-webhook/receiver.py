"""
TradingView -> trading-context webhook receiver (Sprung Ladder monitor).

Receives TradingView alert webhooks, appends each event to
tv_signals.jsonl at the repo root, and pushes to GitHub in the background.

Runs as a systemd service on port 80 (TradingView only posts to 80/443).
Config comes from /etc/tv-webhook.env:
    TV_WEBHOOK_SECRET=<generated at deploy time>
    REPO_DIR=/opt/tv-webhook/trading-context
"""

import json
import os
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request

app = FastAPI()

SHARED_SECRET = os.environ["TV_WEBHOOK_SECRET"]
REPO_DIR = Path(os.environ.get("REPO_DIR", "/opt/tv-webhook/trading-context"))
LOG_FILE = REPO_DIR / "tv_signals.jsonl"

_git_lock = threading.Lock()


@app.get("/health")
def health():
    return {"ok": True, "log_exists": LOG_FILE.exists()}


@app.post("/tv-webhook")
async def tv_webhook(request: Request, background: BackgroundTasks):
    raw = (await request.body()).decode("utf-8", errors="replace").strip()
    try:
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            payload = {"raw": raw}
    except json.JSONDecodeError:
        payload = {"raw": raw}

    if payload.get("secret") != SHARED_SECRET:
        raise HTTPException(status_code=401, detail="bad secret")
    payload.pop("secret", None)  # never write the secret to the repo

    payload["received_at_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(payload) + "\n")

    background.add_task(commit_and_push, payload.get("event", "signal"))
    return {"ok": True}


def commit_and_push(event: str) -> None:
    """Pull-rebase then push so parallel Claude-session commits don't wedge us."""
    with _git_lock:
        try:
            g = ["git", "-C", str(REPO_DIR)]
            subprocess.run(g + ["add", LOG_FILE.name], check=True, timeout=30)
            r = subprocess.run(
                g + ["commit", "-m", f"tv signal: {event}"],
                capture_output=True, timeout=30,
            )
            if r.returncode != 0:  # nothing to commit
                return
            subprocess.run(g + ["pull", "--rebase", "-X", "ours"], timeout=60)
            subprocess.run(g + ["push"], check=True, timeout=60)
        except Exception:
            # Never let a git hiccup kill the endpoint; the JSONL line is
            # already on disk and the next successful push carries it up.
            pass

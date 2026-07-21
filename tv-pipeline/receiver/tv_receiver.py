"""TradingView webhook receiver — appends signals to tv_signals.jsonl in the repo.
Runs on 127.0.0.1:8091 behind nginx (TV webhooks only call ports 80/443)."""
import json, os, subprocess
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException

KEY         = os.environ.get("TV_KEY", "CHANGE_ME")
REPO_DIR    = os.environ.get("TV_REPO_DIR", "/root/trading-context")
SIGNAL_FILE = os.path.join(REPO_DIR, "tv_signals.jsonl")
AUTO_GIT    = os.environ.get("TV_AUTO_GIT", "1") == "1"

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True, "signals_file": SIGNAL_FILE, "auto_git": AUTO_GIT}

@app.post("/tv-signal")
async def tv_signal(request: Request, key: str = ""):
    if key != KEY:
        raise HTTPException(status_code=403, detail="bad key")
    try:
        body = await request.json()
    except Exception:
        body = {"raw": (await request.body()).decode(errors="replace")}
    body["received_utc"] = datetime.now(timezone.utc).isoformat()
    with open(SIGNAL_FILE, "a") as f:
        f.write(json.dumps(body) + "\n")
    if AUTO_GIT:
        subprocess.run(["git", "-C", REPO_DIR, "add", "tv_signals.jsonl"], check=False)
        subprocess.run(["git", "-C", REPO_DIR, "commit", "-m",
                        f"tv signal: {body.get('event', 'unknown')} {body.get('symbol', '')}"], check=False)
        subprocess.run(["git", "-C", REPO_DIR, "push"], check=False)
    return {"ok": True, "event": body.get("event")}

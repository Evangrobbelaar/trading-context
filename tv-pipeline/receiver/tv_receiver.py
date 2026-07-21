"""TradingView webhook receiver -> appends signals to tv_signals.jsonl and syncs to GitHub.

tick 34 hardening: the previous version ran add/commit/push with check=False and
returned ok:true unconditionally. Any push failure was invisible — TradingView saw a
200 while the signal sat stranded on the box. The repo goes non-fast-forward every
time anything commits from outside the VPS, which is routine, so this bit twice in
one session. Now: rebase before push, never swallow a git error, and fail loudly.
"""
import json, os, subprocess, logging
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

KEY         = os.environ.get("TV_KEY", "CHANGE_ME")
REPO_DIR    = os.environ.get("TV_REPO_DIR", "/root/trading-context")
SIGNAL_FILE = os.path.join(REPO_DIR, "tv_signals.jsonl")
AUTO_GIT    = os.environ.get("TV_AUTO_GIT", "1") == "1"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tv")

app = FastAPI()


def git(*args, timeout=90):
    """Run git in the repo. Returns (returncode, combined output). Logs failures."""
    p = subprocess.run(["git", "-C", REPO_DIR, *args],
                       capture_output=True, text=True, timeout=timeout)
    out = (p.stdout + p.stderr).strip()
    if p.returncode != 0:
        log.error("git %s -> rc=%s | %s", " ".join(args), p.returncode, out)
    return p.returncode, out


def sync(event_desc):
    """Stage, commit, rebase onto origin, push. Returns (ok, detail). Never raises."""
    try:
        rc, out = git("add", "tv_signals.jsonl")
        if rc:
            return False, f"add: {out}"

        rc, out = git("commit", "-m", f"tv signal: {event_desc}")
        if rc and "nothing to commit" not in out:
            return False, f"commit: {out}"

        # THE FIX: integrate anything pushed from elsewhere before attempting a push.
        # --autostash covers stray unstaged changes in the working tree.
        rc, out = git("pull", "--rebase", "--autostash")
        if rc:
            git("rebase", "--abort")
            return False, f"pull --rebase: {out}"

        rc, out = git("push")
        if rc:
            return False, f"push: {out}"

        return True, "pushed"
    except subprocess.TimeoutExpired:
        return False, "git timed out"
    except Exception as e:
        return False, f"exception: {e!r}"


@app.get("/health")
def health():
    git_state = "auto_git disabled"
    if AUTO_GIT:
        _, git_state = git("status", "-sb")
    return {"ok": True, "signals_file": SIGNAL_FILE,
            "auto_git": AUTO_GIT, "git": git_state}


@app.post("/tv-signal")
async def tv_signal(request: Request, key: str = ""):
    if key != KEY:
        log.warning("rejected: bad key")
        raise HTTPException(status_code=403, detail="bad key")

    try:
        body = await request.json()
    except Exception:
        body = {"raw": (await request.body()).decode(errors="replace")}

    body["received_utc"] = datetime.now(timezone.utc).isoformat()
    with open(SIGNAL_FILE, "a") as f:
        f.write(json.dumps(body) + "\n")
    log.info("signal saved: %s %s", body.get("event"), body.get("symbol"))

    if not AUTO_GIT:
        return {"ok": True, "event": body.get("event"), "git": "disabled"}

    ok, detail = sync(f"{body.get('event', 'unknown')} {body.get('symbol', '')}")
    if not ok:
        log.error("SYNC FAILED — signal is on disk but NOT on GitHub: %s", detail)
        return JSONResponse(status_code=500, content={
            "ok": False, "saved_locally": True,
            "event": body.get("event"), "git_error": detail})

    return {"ok": True, "event": body.get("event"), "git": "pushed"}

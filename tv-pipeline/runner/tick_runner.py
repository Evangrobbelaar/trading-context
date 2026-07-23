#!/usr/bin/env python3
"""
tick_runner.py — TV signal -> tiered headless Claude Code spawner. (tick 45)

Runs on the VPS host (systemd: tv-tick-runner.service), NOT in Docker.
Watches tv_signals.jsonl (written by the dockerized receiver via the shared
/root/trading-context mount), classifies each new signal into a tier, and
spawns `claude -p` with a model + turn budget sized to the tier:

  DROP    - TEST_*, ignored symbols (XAUUSD1! futures), *_EXPIRED   -> no Claude, no tokens
  LOG     - SWEEP_* (Phase-2 info). Tracked in a shelf detector: 2+ sweeps at
            the same level within the window = defended-shelf signature -> promote to TIER 1
  TIER 1  - HL_RECLAIM / LL_BREAKDOWN / LEVEL hits with no armed ticket.
            Fast lane: haiku, ~12 turns, read-only. Verdict: NO_ACTION or ESCALATE_TIER2.
  TIER 2  - SPRING_* always; PULLBACK_TAG_* / LEVEL hits on an armed snapshot ticket;
            any Tier-1 escalation. Full lane: sonnet, full protocol, may place (execute mode).

Design rules:
  - ONE run at a time (sequential worker). Signals landing mid-run are picked up
    next loop as a batch — 7 of 20 gaps on day 1 were <60s; batching is the design.
  - Cursor (byte offset) advances only after a run completes -> nothing is lost.
  - Kill switch: AUTOTRADE_OFF file at repo root. Present = advance cursor, spawn nothing.
  - Mode (advise|execute) read fresh from auto_mode.json every spawn.
  - SPRING older than spring_max_exec_age_min at spawn = tagged STALE (info only, no entry).
  - Runner owns notifications (ntfy) — fires even when a session dies.
  - stdlib only. Config: tiers.json next to this file (hot-reloaded every loop).
"""
import json, os, subprocess, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(os.environ.get("TV_REPO_DIR", "/root/trading-context"))
RUNNER_DIR = Path(os.environ.get("TV_RUNNER_DIR", "/root/tv-runner"))
SIGNALS = REPO / "tv_signals.jsonl"
KILL = REPO / "AUTOTRADE_OFF"
MODE_FILE = REPO / "auto_mode.json"
SNAPSHOT = REPO / "session_snapshot.json"
TIERS_FILE = Path(__file__).resolve().parent / "tiers.json"
CURSOR = RUNNER_DIR / "cursor.txt"
SWEEP_STATE = RUNNER_DIR / "sweep_state.json"
RUNS = RUNNER_DIR / "runs"
POLL_S = 1.0

# Back-compat: v2 pine event names -> classification of v3 names
BACKCOMPAT = {"SWEEP": "SWEEP_LOW", "SPRING": "SPRING_LONG",
              "LEVEL1_HIT": "LEVEL1_HIT", "LEVEL2_HIT": "LEVEL2_HIT"}


def log(msg):
    print(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {msg}", flush=True)


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def cfg():
    c = load_json(TIERS_FILE, {})
    c.setdefault("ignore_symbols", ["XAUUSD1!"])
    c.setdefault("symbol_map", {"USOIL": "WTI", "GOLD": "XAUUSD",
                                "SILVER": "XAGUSD", "US100": "NAS100"})
    c.setdefault("instrument_policy", {})
    c.setdefault("drop_events", ["TEST_SWEEP"])
    c.setdefault("drop_event_suffixes", ["_EXPIRED"])
    c.setdefault("log_only_events", ["SWEEP_LOW", "SWEEP_HIGH"])
    c.setdefault("tier1_events", ["HL_RECLAIM", "LL_BREAKDOWN", "LEVEL1_HIT", "LEVEL2_HIT"])
    c.setdefault("tier2_events", ["SPRING_LONG", "SPRING_SHORT",
                                  "PULLBACK_TAG_LONG", "PULLBACK_TAG_SHORT"])
    c.setdefault("armed_ticket_promote_events",
                 ["LEVEL1_HIT", "LEVEL2_HIT", "PULLBACK_TAG_LONG", "PULLBACK_TAG_SHORT"])
    c.setdefault("shelf_promote", {"window_min": 240, "tolerance_pct": 0.05, "min_count": 2})
    c.setdefault("spring_max_exec_age_min", 10)
    c.setdefault("max_signal_age_min", 30)
    c.setdefault("tier1", {"model": "haiku", "max_turns": 12, "timeout_s": 240})
    c.setdefault("tier2", {"model": "sonnet", "max_turns": 45, "timeout_s": 900})
    c.setdefault("ntfy_topic", "")
    return c


def ntfy(topic, title, msg):
    if not topic:
        return
    try:
        req = urllib.request.Request(f"https://ntfy.sh/{topic}",
                                     data=msg.encode()[:3800],
                                     headers={"Title": title[:120]})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        log(f"ntfy failed: {e!r}")


def read_new_lines():
    """Return (new_complete_lines, new_offset)."""
    if not SIGNALS.exists():
        return [], 0
    size = SIGNALS.stat().st_size
    if not CURSOR.exists():
        # COLD START (tick 46 fix): seed the cursor at EOF. Without this the first
        # loop after a deploy/reboot replays the entire day's backlog as one batch
        # — observed 20:13 UTC 21 Jul: 11 stale signals spawned a Tier 2 run.
        # History belongs in the file, not in a live trading decision.
        CURSOR.parent.mkdir(parents=True, exist_ok=True)
        CURSOR.write_text(str(size))
        log(f"cold start: cursor seeded at EOF ({size} bytes) — backlog skipped")
        return [], size
    offset = 0
    try:
        offset = int(CURSOR.read_text().strip())
    except Exception:
        pass
    if size < offset:          # file rotated/reset
        offset = 0
    if size == offset:
        return [], offset
    with open(SIGNALS, "rb") as f:
        f.seek(offset)
        chunk = f.read(size - offset)
    # only consume complete lines; leave a partial trailing line for next loop
    last_nl = chunk.rfind(b"\n")
    if last_nl == -1:
        return [], offset
    lines, consumed = chunk[:last_nl].split(b"\n"), offset + last_nl + 1
    out = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        try:
            out.append(json.loads(raw))
        except Exception:
            log(f"skipping malformed line: {raw[:120]!r}")
    return out, consumed


def canon_event(sig):
    ev = str(sig.get("event", "")).upper()
    return BACKCOMPAT.get(ev, ev)


def canon_symbol(sig, c):
    """TV alert symbol -> broker symbol (naming reconciliation only).

    Added 23 Jul 2026. Root cause: 67 of 279 signals over 21-22 Jul fired on
    tickers the execution layer could not resolve — USOIL (broker calls it WTI,
    get_symbol_price errored every time), plus gold split three ways across
    GOLD / XAUUSD / XAUUSD1!. Every one was a guaranteed NO_ACTION regardless of
    setup quality.

    This maps SAME-INSTRUMENT alias names ONLY. It must never map across
    contracts (USOIL->BRENT, spot->futures): the signal's price/level/extreme
    were measured on the source chart and do not transfer.
    """
    raw = str(sig.get("symbol", ""))
    return c.get("symbol_map", {}).get(raw, raw)


def policy_check(sym, c, now=None):
    """Return a block reason for a broker symbol, or None if tradeable.

    Replaces per-tick prose interpretation of CLAUDE.md's INSTRUMENTS TO AVOID.
    """
    p = c.get("instrument_policy", {}).get(sym)
    if not p:
        return None
    status = p.get("status", "ok")
    if status == "blocked":
        return f"POLICY BLOCK {sym}: {p.get('reason', 'on instrument policy list')}"
    if status == "session_limited":
        window = p.get("blocked_sast_hours")
        if not window:
            return None
        now = now or datetime.now(timezone.utc)
        hour = (now.hour + 2) % 24          # SAST = UTC+2
        lo, hi = window
        inside = (lo <= hour < hi) if lo < hi else (hour >= lo or hour < hi)
        if inside:
            return (f"POLICY BLOCK {sym}: {p.get('reason', 'session restricted')} "
                    f"(SAST {hour:02d}h inside blocked window {lo:02d}-{hi:02d})")
    return None


def shelf_check(sig, c):
    """Track SWEEP_* levels; return note if a defended-shelf signature formed."""
    sp = c["shelf_promote"]
    state = load_json(SWEEP_STATE, {})
    sym = str(sig.get("symbol", "?"))
    px = sig.get("level") or sig.get("price")
    now_ms = sig.get("t") or int(time.time() * 1000)
    if not isinstance(px, (int, float)):
        return None
    hist = [h for h in state.get(sym, [])
            if now_ms - h["t"] <= sp["window_min"] * 60000]
    hist.append({"p": px, "t": now_ms})
    state[sym] = hist[-50:]
    SWEEP_STATE.parent.mkdir(parents=True, exist_ok=True)
    SWEEP_STATE.write_text(json.dumps(state))
    tol = px * sp["tolerance_pct"] / 100.0
    near = [h for h in hist if abs(h["p"] - px) <= tol]
    if len(near) >= sp["min_count"]:
        return (f"SHELF SIGNATURE: {len(near)} sweeps at ~{px} on {sym} within "
                f"{sp['window_min']}min — Sprung Ladder Phase-1 candidate")
    return None


def classify(sig, c, armed_symbols):
    """Return (tier:int 0..2, note:str|None). 0 = no Claude."""
    ev = canon_event(sig)
    raw_sym = str(sig.get("symbol", ""))
    sym = canon_symbol(sig, c)          # broker symbol, post-alias-map
    if ev in c["drop_events"] or any(ev.endswith(s) for s in c["drop_event_suffixes"]):
        return 0, None
    if raw_sym in c["ignore_symbols"] or sym in c["ignore_symbols"]:
        return 0, f"ignored symbol {raw_sym}"
    pol = policy_check(sym, c)
    if pol:
        # Drop before spawn: no Claude session, no tokens. This is the fix for
        # WTI/BTCUSD-in-Asian-hours burning a full tick to reach NO_ACTION.
        return 0, pol
    if ev in c["log_only_events"]:
        note = shelf_check(sig, c)
        return (1, note) if note else (0, None)
    if ev in c["tier2_events"]:
        return 2, None
    if ev in c["armed_ticket_promote_events"] and sym in armed_symbols:
        return 2, f"{sym} has an ARMED TICKET in session_snapshot.json"
    if ev in c["tier1_events"]:
        return 1, None
    return 1, f"unknown event {ev} — assess"   # fail toward a cheap look, not silence


def drop_stale(batch, c):
    """Hard age gate (tick 46): a signal older than max_signal_age_min never spawns a
    session. Separate from the SPRING-specific note — this drops the signal entirely."""
    cutoff_ms = c["max_signal_age_min"] * 60000
    now_ms = int(time.time() * 1000)
    fresh, dropped = [], []
    for s in batch:
        t = s.get("t")
        if isinstance(t, (int, float)) and (now_ms - t) > cutoff_ms:
            dropped.append(f"{canon_event(s)} {s.get('symbol')} ({(now_ms-t)/60000:.0f}min old)")
        else:
            fresh.append(s)
    if dropped:
        log(f"dropped {len(dropped)} stale: {', '.join(dropped[:5])}")
    return fresh


def staleness_notes(batch, c):
    notes, now_ms = [], int(time.time() * 1000)
    for s in batch:
        ev = canon_event(s)
        if ev.startswith("SPRING") and isinstance(s.get("t"), (int, float)):
            age_min = (now_ms - s["t"]) / 60000
            if age_min > c["spring_max_exec_age_min"]:
                notes.append(f"STALE: {ev} {s.get('symbol')} is {age_min:.1f} min old "
                             f"(>{c['spring_max_exec_age_min']}) — information only, NO ENTRY from it")
    return notes


def git_pull():
    try:
        subprocess.run(["git", "-C", str(REPO), "pull", "--rebase", "--autostash"],
                       capture_output=True, timeout=45)
    except Exception as e:
        log(f"git pull skipped: {e!r}")


def mode():
    return str(load_json(MODE_FILE, {}).get("mode", "advise")).lower()


def build_prompt(tier, batch, notes, run_mode):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = "\n".join(json.dumps(s) for s in batch)
    extra = ("\n".join(f"- {n}" for n in notes) + "\n") if notes else ""
    if tier == 1:
        return (f"AUTO TICK — TIER 1 (fast lane). MODE={run_mode}. UTC now {now}.\n"
                f"Signal batch from tv_signals.jsonl:\n{lines}\n{extra}"
                "Follow AUTO_TICK_PROTOCOL.md section TIER 1 exactly. You are READ-ONLY: "
                "no orders, no position modifications, no file writes, no commits. "
                "Max 4 MCP calls total. End with the single T1 contract line. If escalation "
                "criteria are met, include the exact token ESCALATE_TIER2: <one-line reason>.")
    return (f"AUTO TICK — TIER 2 (full lane). MODE={run_mode}. UTC now {now}.\n"
            f"Signal batch from tv_signals.jsonl:\n{lines}\n{extra}"
            "Follow AUTO_TICK_PROTOCOL.md section TIER 2 exactly. Hard rules: demo 41829612 "
            "only; 5-step routing procedure around every order; enforcer.py exit 0 (with the "
            "Rule 17 range args) before any order; Rule 22 market-only; any balance used must "
            "be live-queried this run. In advise mode place NOTHING — record the would-be "
            "ticket instead. If this tick produces a FLAG FOR EVAN, ALSO append one JSON "
            "line to flags.jsonl (id FLAG-NNN, opened, opened_tick, status OPEN, severity, "
            "kind, symbols, title, detail, impact, classification, recommendation, owner, "
            "action_required) — do not bury it only in prose. If a tick resolves an existing "
            "flag, append a new line with the same id, status RESOLVED and a resolved_note. "
            "Finish by updating session_snapshot.json, appending the auto "
            "tick to EVAN_TRADING_CONTEXT.md, committing and pushing, and end with the "
            "single-line T2 summary starting with 'AUTO-TICK[t2]'.")


def run_claude(tier, batch, notes, c):
    t = c["tier2" if tier == 2 else "tier1"]
    run_mode = mode()
    prompt = build_prompt(tier, batch, notes, run_mode)
    # --permission-mode dontAsk (tick 48): headless-correct baseline. Pre-approved tools
    # (settings.json allow rules) run normally; anything else is DENIED rather than
    # silently hanging on a prompt no human can answer. Deny rules apply in every mode.
    #
    # tick 51 fix: this previously never varied by run_mode, so it always loaded the
    # default .claude/settings.json (advise — every order tool DENIED at the harness
    # level). Flipping auto_mode.json to "execute" changed the PROMPT text only; the
    # harness still hard-blocked create_market_order underneath it, so execute mode was
    # a no-op. settings.execute.json (single-position order tools allowed, bulk
    # close-all/cancel-all still denied in every mode) now loads only when mode=execute.
    cmd = ["claude", "-p", prompt,
           "--model", t["model"],
           "--max-turns", str(t["max_turns"]),
           "--permission-mode", "dontAsk",
           "--output-format", "json"]
    if run_mode == "execute":
        cmd += ["--settings", str(REPO / ".claude" / "settings.execute.json")]
    log(f"spawning tier{tier} ({t['model']}, mode={run_mode}, settings={'execute' if run_mode == 'execute' else 'advise'}, batch={len(batch)})")
    started = time.time()
    try:
        r = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True,
                           timeout=t["timeout_s"], env={**os.environ, "HOME": os.environ.get("HOME", "/root")})
        raw = r.stdout
    except subprocess.TimeoutExpired:
        return {"error": f"tier{tier} TIMEOUT after {t['timeout_s']}s", "raw": ""}
    except FileNotFoundError:
        return {"error": "claude CLI not found — run deploy_auto.sh auth steps", "raw": ""}
    dur = time.time() - started
    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    (RUNS / f"{stamp}_t{tier}.json").write_text(raw or r.stderr or "")
    try:
        parsed = json.loads(raw)
        result = parsed.get("result", "") or ""
        cost = parsed.get("total_cost_usd")
    except Exception:
        result, cost = (raw or r.stderr or "")[-600:], None
    return {"result": result, "cost": cost, "dur": dur, "raw": raw}


def summarize(res):
    txt = (res.get("result") or res.get("error") or "").strip()
    tail = [l for l in txt.splitlines() if l.strip()]
    line = tail[-1] if tail else "no output"
    for l in tail:
        if l.startswith("AUTO-TICK"):
            line = l
            break
    cost = res.get("cost")
    dur = res.get("dur")
    suffix = ""
    if cost is not None:
        suffix += f" | ${cost:.3f}"
    if dur is not None:
        suffix += f" | {dur:.0f}s"
    return (line + suffix)[:900]


def main():
    RUNNER_DIR.mkdir(parents=True, exist_ok=True)
    log(f"tick_runner up. repo={REPO} signals={SIGNALS}")
    while True:
        time.sleep(POLL_S)
        try:
            c = cfg()
            batch, new_offset = read_new_lines()
            if not batch:
                continue
            if KILL.exists():
                log(f"AUTOTRADE_OFF present — skipping {len(batch)} signal(s)")
                CURSOR.write_text(str(new_offset))
                continue
            snapshot = load_json(SNAPSHOT, {})
            armed = {str(a.get("symbol", "")) for a in snapshot.get("armed_tickets", [])}
            batch = drop_stale(batch, c)
            if not batch:
                CURSOR.write_text(str(new_offset))
                continue
            tiered = [(classify(s, c, armed), s) for s in batch]
            notes = [n for ((tier, n), _) in tiered if n]
            actionable = [s for ((tier, _), s) in tiered if tier >= 1]
            # Resolve alias -> broker symbol on the exact objects going to Claude,
            # so the session trades WTI/XAUUSD/etc. instead of the unresolvable
            # alert name. Original preserved as _tv_symbol for traceability.
            for s in actionable:
                bsym = canon_symbol(s, c)
                if bsym != s.get("symbol"):
                    s["_tv_symbol"] = s.get("symbol")
                    s["symbol"] = bsym
            top = max((tier for ((tier, _), _) in tiered), default=0)
            if top == 0:
                CURSOR.write_text(str(new_offset))
                log(f"{len(batch)} signal(s) logged/dropped, no spawn")
                continue
            git_pull()
            notes += staleness_notes(actionable, c)
            res = run_claude(top, actionable, notes, c)
            ntfy(c["ntfy_topic"], f"TV tick t{top}", summarize(res))
            if top == 1 and "ESCALATE_TIER2" in (res.get("result") or ""):
                reason = [l for l in res["result"].splitlines() if "ESCALATE_TIER2" in l]
                res2 = run_claude(2, actionable, notes + reason, c)
                ntfy(c["ntfy_topic"], "TV tick t2 (escalated)", summarize(res2))
            CURSOR.write_text(str(new_offset))
        except Exception as e:
            log(f"loop error: {e!r}")
            time.sleep(3)


if __name__ == "__main__":
    sys.exit(main())

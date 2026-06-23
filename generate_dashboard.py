#!/usr/bin/env python3
"""
Dashboard generator (Open Design pattern).
Call at end of each tick: python generate_dashboard.py
Reads session_state.json + session_log.jsonl + enforcer_audit.jsonl
Outputs dashboard.html — opens in any browser, auto-refreshes every 30s.
"""

import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_jsonl_tail(filename, n=15):
    path = os.path.join(BASE_DIR, filename)
    records = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    return records[-n:] if len(records) >= n else records


def badge(text, cls):
    return f'<span class="badge {cls}">{text}</span>'


def trend_html(trend):
    t = trend.lower()
    if "bear" in t:
        return badge("↓ BEAR", "bear")
    if "bull" in t and "choppy" not in t and "mild" not in t:
        return badge("↑ BULL", "bull")
    return badge("— SKIP", "skip")


def pnl_span(amount):
    if amount is None:
        return '<span class="muted">—</span>'
    sign = "+" if amount >= 0 else ""
    cls = "profit" if amount >= 0 else "loss"
    return f'<span class="{cls}">{sign}R{amount:.2f}</span>'


def main():
    state = load_json("session_state.json")
    news = load_json("news_impact.json")
    ticks = load_jsonl_tail("session_log.jsonl", 12)
    enforcer_log = load_jsonl_tail("enforcer_audit.jsonl", 20)

    balance = state.get("account_balance", "—")
    updated = state.get("updated_sast", "—")
    h4_trends = state.get("h4_trends", {})
    watchlist = state.get("watchlist_tomorrow", [])
    stops = state.get("stop_conditions", {})
    loop_stopped = state.get("loop_stopped", False)
    target = state.get("session_target_zar", "?")

    news_events = news.get("active_events", state.get("news_events", []))
    high_impact = news.get("high_impact_within_2h", False)

    consec = stops.get("consecutive_losses", 0)
    max_consec = stops.get("max_consecutive_losses", 2)
    trades_today = stops.get("trades_this_session", 0)

    enf_blocks = sum(1 for e in enforcer_log if e.get("verdict") == "BLOCKED")
    enf_passes = sum(1 for e in enforcer_log if e.get("verdict") == "PASS")

    # Infer session P&L from balances in tick log
    balances = [
        t.get("account_balance_zar") for t in ticks if t.get("account_balance_zar")
    ]
    session_pnl = (balances[-1] - balances[0]) if len(balances) >= 2 else None

    # Loop status
    loop_cls = "stopped" if loop_stopped else "running"
    loop_txt = "STOPPED" if loop_stopped else "ACTIVE"

    # Loss meter dots
    dots = "".join(
        f'<div class="dot {"red" if i < consec else "gray"}"></div>'
        for i in range(max_consec)
    )

    # Watchlist rows
    watch_rows = ""
    for w in watchlist[:5]:
        sym = w.get("symbol", "")
        direction = w.get("direction", "").upper()
        score = w.get("score", 0)
        entry = w.get("entry_zone", [])
        entry_str = f"{entry[0]}–{entry[1]}" if len(entry) == 2 else str(entry)
        rr = w.get("rr", "?")
        risk = w.get("risk_zar", "?")
        score_cls = "profit" if score >= 8 else "warn"
        dir_cls = "loss" if direction == "SHORT" else "profit"
        watch_rows += (
            f"<tr>"
            f"<td><b>{sym}</b></td>"
            f'<td><span class="{dir_cls}">{direction}</span></td>'
            f'<td><span class="{score_cls}">{score}/10</span></td>'
            f"<td>{entry_str}</td>"
            f"<td>{rr}:1</td>"
            f"<td>R{risk}</td>"
            f"</tr>"
        )

    # Trend grid
    trend_grid = ""
    for sym, tr in h4_trends.items():
        trend_grid += f"<div class='trend-cell'><b>{sym}</b> {trend_html(tr)}</div>"

    # Tick log rows
    tick_rows = ""
    for t in reversed(ticks[-10:]):
        tick_num = t.get("tick", "?")
        sast = t.get("sast_time", "")
        sess = t.get("session", "")
        trade = t.get("trade_placed", "none") or "none"
        action = (t.get("action_taken", "") or "")[:70]
        enf = t.get("enforcer_result", "na") or "na"
        enf_cls = (
            "profit"
            if "PASS" in str(enf)
            else ("loss" if "BLOCKED" in str(enf) else "muted")
        )
        row_cls = " class='highlight'" if trade != "none" else ""
        tick_rows += (
            f"<tr{row_cls}>"
            f"<td>#{tick_num}</td>"
            f"<td>{sast}</td>"
            f"<td>{sess}</td>"
            f"<td>{trade}</td>"
            f'<td><span class="{enf_cls}">{enf}</span></td>'
            f"<td title='{action}'>{action}</td>"
            f"</tr>"
        )

    # News section
    news_html = ""
    if high_impact:
        news_html += '<div class="alert">⚠ HIGH-IMPACT EVENT ≤2H — NO NEW ENTRIES</div>'
    if news_events:
        news_html += " ".join(f'<span class="news-tag">{e}</span>' for e in news_events)
    else:
        news_html += '<span class="muted">No active events</span>'

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="30">
<title>TradeLoop Dashboard</title>
<style>
:root {{
  --bg:#0d1117;--surface:#161b22;--border:#30363d;
  --text:#e6edf3;--muted:#8b949e;
  --profit:#3fb950;--loss:#f85149;--warn:#d29922;--info:#58a6ff;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'Courier New',monospace;font-size:13px;padding:16px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px}}
.grid2{{display:grid;grid-template-columns:2fr 1fr;gap:12px;margin-bottom:12px}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:12px}}
h3{{font-size:10px;text-transform:uppercase;color:var(--muted);margin-bottom:8px;letter-spacing:.5px}}
.big{{font-size:26px;font-weight:bold;margin:4px 0}}
.sub{{color:var(--muted);font-size:11px}}
.profit{{color:var(--profit)}}
.loss{{color:var(--loss)}}
.warn{{color:var(--warn)}}
.muted{{color:var(--muted)}}
.badge{{padding:2px 7px;border-radius:3px;font-size:11px;font-weight:bold}}
.badge.bear{{background:rgba(248,81,73,.18);color:#f85149}}
.badge.bull{{background:rgba(63,185,80,.18);color:#3fb950}}
.badge.skip{{background:rgba(139,148,158,.15);color:#8b949e}}
.running{{color:var(--profit)}}
.stopped{{color:var(--loss);font-weight:bold}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:left;padding:4px 6px;font-size:10px;text-transform:uppercase;color:var(--muted);border-bottom:1px solid var(--border)}}
td{{padding:4px 6px;border-bottom:1px solid rgba(48,54,61,.4)}}
tr:last-child td{{border-bottom:none}}
tr.highlight{{background:rgba(88,166,255,.07)}}
.trend-cell{{display:inline-block;margin:3px 6px}}
.news-tag{{background:rgba(210,153,34,.2);color:#d29922;border-radius:3px;padding:2px 6px;margin:2px;font-size:11px;display:inline-block}}
.alert{{background:rgba(248,81,73,.15);border:1px solid #f85149;color:#f85149;padding:6px 10px;border-radius:4px;margin-bottom:8px;font-weight:bold}}
.dot{{width:13px;height:13px;border-radius:50%;display:inline-block;margin-right:4px}}
.dot.red{{background:#f85149}}
.dot.gray{{background:#30363d}}
.footer{{text-align:right;color:var(--muted);font-size:10px;margin-top:12px}}
</style>
</head>
<body>

<div class="grid">
  <div class="card">
    <h3>Account Balance</h3>
    <div class="big">R{balance}</div>
    <div class="sub">Demo #41829612 · last scan {updated} SAST</div>
    {'<div style="margin-top:6px">' + pnl_span(session_pnl) + " session P&amp;L</div>" if session_pnl is not None else ""}
  </div>
  <div class="card">
    <h3>Loop Status</h3>
    <div class="big {loop_cls}">{loop_txt}</div>
    <div class="sub">Target: R{target} · trades today: {trades_today}</div>
  </div>
  <div class="card">
    <h3>Consecutive Losses</h3>
    <div class="big {"loss" if consec >= max_consec else "muted"}">{consec}/{max_consec}</div>
    <div style="margin-top:8px">{dots}</div>
  </div>
</div>

<div class="grid2">
  <div class="card">
    <h3>Watchlist — London Open</h3>
    <table>
      <tr><th>Symbol</th><th>Dir</th><th>Score</th><th>Entry</th><th>R:R</th><th>Risk</th></tr>
      {watch_rows or '<tr><td colspan="6" class="muted" style="text-align:center;padding:12px">No watchlist — run master scan</td></tr>'}
    </table>
  </div>
  <div class="card">
    <h3>News</h3>
    {news_html}
    <div style="margin-top:12px">
      <h3>Enforcer (session)</h3>
      <span class="profit">✓ {enf_passes} PASS</span>&nbsp;&nbsp;
      <span class="loss">✗ {enf_blocks} BLOCKED</span>
    </div>
  </div>
</div>

<div class="card" style="margin-bottom:12px">
  <h3>H4 Trends</h3>
  <div style="margin-top:6px">{trend_grid}</div>
</div>

<div class="card">
  <h3>Recent Ticks</h3>
  <table>
    <tr><th>#</th><th>SAST</th><th>Session</th><th>Trade</th><th>Enforcer</th><th>Action</th></tr>
    {tick_rows or '<tr><td colspan="6" class="muted" style="text-align:center;padding:12px">No ticks yet</td></tr>'}
  </table>
</div>

<div class="footer">Generated {now_str} · auto-refresh 30s · TradeLoop v3.0</div>
</body>
</html>"""

    out = os.path.join(BASE_DIR, "dashboard.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard → dashboard.html")


if __name__ == "__main__":
    main()

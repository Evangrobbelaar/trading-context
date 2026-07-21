#!/usr/bin/env bash
# test_placement.sh — tick 48. PLUMBING TEST for the order-placement path.
#
# This is NOT a trading decision and does not pretend to be one. It places a
# minimum-size GBPUSD position on DEMO 41829612, verifies routing at every step,
# and closes it immediately. Purpose: prove permissions + MCP write access +
# account routing + enforcer integration work, so that when a REAL signal fires
# in a real session, the only untested variable is the trading judgement.
#
# Elevated permissions are injected for THIS RUN ONLY via --settings.
# The repo's .claude/settings.json stays advise-safe (order tools denied).
set -euo pipefail
cd /root/trading-context

echo "== ORDER PATH TEST — demo 41829612, min size, immediate close =="
# tick 49: the live ThinkTrader server on this box is 'claude' (synced from claude.ai),
# NOT the standalone 'thinktrader' entry. Verify before spending a run:
if ! claude mcp list 2>/dev/null | grep -q "claude:.*Connected"; then
  echo "ABORT: no connected ThinkTrader MCP server found. Run 'claude mcp list' first."; exit 1
fi
echo "Cost: the spread on 0.01 lots GBPUSD (~R2). Exposure: seconds."
read -p "Proceed? [y/N] " ok
[ "$ok" = "y" ] || { echo "aborted"; exit 0; }

claude -p "SYSTEM PLUMBING TEST — not a trading decision, do not analyze market structure.

Execute these steps in order and report each result:
0. Use ThinkTrader tools from the CONNECTED server (prefix mcp__claude__). Ignore any 'thinktrader' server showing as failed — dead duplicate.
1. switch_trading_account to 41829612. Report the 'previous' and 'current' fields verbatim (we are counting MCP reverts).
2. get_account_info — report live balance.
3. get_symbol_price GBPUSD — report bid/ask. Then get_symbol_history GBPUSD M5 last 5 candles — this specifically tests the permission fix; report whether it succeeded or was denied.
4. Run: python3 enforcer.py --account demo --account_id 41829612 --balance <live balance> --instrument GBPUSD --risk_amount 40 --open_pending_risk 0 --news_checked --news_clear
   Report the exit code. If it does not exit 0, STOP and report why — place nothing.
5. Place a MARKET BUY on GBPUSD, 0.01 lots, SL 25 pips below entry, no TP.
6. Report the accountId on the order response verbatim.
7. get_open_positions — confirm the new position is present and on 41829612.
8. CLOSE that position immediately at market. Report the realized P&L.
9. get_open_positions again — confirm it is gone and report what else remains open.

Do NOT touch any other position. Do NOT commit anything to git. Do NOT update any files.
Finish with one line: TEST RESULT: PASS or FAIL — <what worked, what did not>" \
  --settings .claude/settings.execute.json \
  --permission-mode dontAsk \
  --model sonnet \
  --max-turns 30 \
  --output-format text

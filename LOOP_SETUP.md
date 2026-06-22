# LOOP SETUP — Claude Code Native Trading Loop
Added: June 22, 2026

## What "learning" actually means here

Claude's model weights do not change between sessions — there is no
fine-tuning happening. What CAN improve, and what already has been
improving manually since May 2026, is the WRITTEN RULESET in
EVAN_TRADING_CONTEXT.md. Every session post-mortem (Rule 14, the H4 trend
gate, the non-negotiable enforcer rule) is the same mechanism: real
outcomes get reviewed, root-caused, and turned into a specific, versioned
rule addition. That IS the learning loop. The Claude Code native loop below
just makes that mechanism run on a schedule instead of only when Evan
manually triggers a post-mortem, and makes the risk-critical part of it
impossible to talk around.

Two separate loop tiers — do not merge them:

1. SESSION LOOP — runs during market hours, ticks every few minutes,
   does the actual trade monitoring/analysis, calls enforcer.py before
   any trade, logs every decision (taken or blocked).
2. REVIEW LOOP — runs weekly (matches the existing Monday update
   protocol already in the context doc), reads the accumulated logs,
   proposes specific rule edits as a diff. Never auto-commits risk
   parameter changes — Evan approves the diff first.

## SESSION LOOP — start this in Claude Code during trading hours

```
/loop 5m Run a trading session tick: pull EVAN_TRADING_CONTEXT.md from
this repo if not already loaded this session. Check open positions on
the active account. Run the mandatory analysis sequence (news, H4 trend
gate, H1 structure, M15 trigger) per CHANGE 5. For any candidate trade,
compute risk_amount, reward_amount, sl_distance, then run:
python3 enforcer.py --instrument X --direction X --units/--lots X
--balance X --account X --risk_amount X --reward_amount X --sl_distance X
If enforcer.py exits 1, the trade is blocked — do not place it, do not
re-run with adjusted numbers just to force a pass. Only call
create_market_order after a PASS. Use the mandatory ping response format
(CHANGE 4) on every tick for open positions. Stop this loop if: 3
consecutive losing trades this session, OR daily floating + closed loss
exceeds 10% of session-start balance, OR 20 iterations reached.
```

Notes:
- Claude picks the tick interval dynamically if you omit "5m" — for an
  active session, an explicit short interval is safer than letting it
  guess during a fast market.
- Esc stops the loop immediately if anything looks wrong. Stopping is
  always free; a bad trade is not.
- This loop tier deliberately does NOT touch the live account
  (#43019560) without Evan typing an explicit live-account instruction
  in that session — the small live balance has no margin for a bad
  automated tick. Demo (#41810679) is the default surface for this loop.

## REVIEW LOOP — run weekly, Monday session open

```
/loop 1w Read enforcer_audit.jsonl and the PERFORMANCE HISTORY /
SESSION ARCHIVE sections of EVAN_TRADING_CONTEXT.md since the last
review. Identify: which blocked trades would have lost money (enforcer
worked), which passed trades lost money and why (root cause, same
format as the June 11 post-mortem), and any recurring pattern across 3+
trades. Propose specific rule additions or edits as a diff against
EVAN_TRADING_CONTEXT.md. Do NOT commit. Print the diff and wait for
Evan's explicit approval before committing to GitHub.
```

This is the actual "loop learns and we trade better" mechanism: it is
the existing manual post-mortem process, automated to run consistently
every week instead of only after a disaster, with a human approval gate
kept specifically on anything that touches risk sizing.

## Why the enforcer script and not just a stronger text rule

The June 11 catastrophic session happened because "the enforcer cannot
be bypassed" was a sentence in a markdown file, and a sentence can be
overridden by another sentence ("ignore enforcer"). enforcer.py is a
program with an exit code. There is no phrasing that changes what `sys.exit(1)`
does. It only covers the numeric rules (size, SL buffer, risk %, R:R,
banned/blocked instruments) — trend and news judgment still require
Claude's analysis and stay in the text-instruction layer, which is why
CHANGE 4's mandatory ping format and the analysis sequence in CHANGE 5
still matter and still get logged for the review loop to audit.

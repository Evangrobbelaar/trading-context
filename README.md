# Claude ECS — Personal Trading Context
**Private repository — Evan Grobbelaar**

This is my personal Claude ECS trading context file.
It contains my live trading rules, lessons, performance history, and account configuration.

## What is Claude ECS?
The External Context System — the leading Claude memory enforcement framework.
Public community repo: https://github.com/Evangrobbelaar/claude-ecs-community

## Contents
- `EVAN_TRADING_CONTEXT.md` — Full trading context (rules, enforcer, history, lessons)
- `MASTER_PROMPT_EXTERNAL_CONTEXT_SYSTEM.md` — The reusable master prompt

## How Claude uses this
At the start of every trading conversation, Claude fetches this file using bash git commands,
reads it completely, and confirms with:
"Context loaded v1.1 — [date] — [session] — [open positions] open — ready."

## Performance (demo account)
| Period | P&L | Starting balance |
|---|---|---|
| Week 1 (May 29 – Jun 5, 2026) | +R2,297 | R1,046 |

## Owner
Evan Grobbelaar | evangrobbelaar@gmail.com

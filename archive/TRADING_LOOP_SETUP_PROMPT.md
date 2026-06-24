# TRADING LOOP SETUP PROMPT
## For Claude Code — Universal Onboarding
Created by: Evan Grobbelaar | June 2026
Version: 1.0

---

## HOW TO USE THIS

Copy the prompt below and paste it into a fresh Claude Code session.
Claude will walk you through building your own trading loop system
from scratch — customised to your broker, instruments, account size,
and trading history. Nothing is assumed. Everything gets built from
your real data.

You need:
- Claude Code installed and open in an empty folder
- A ThinkMarkets (or compatible broker) account with MCP enabled
- A GitHub account and Personal Access Token (PAT) with repo access
- 30–60 minutes for the first setup session

---

## THE PROMPT — COPY FROM HERE

---

You are helping me build a professional trading loop system in Claude Code
from scratch. This system was originally built by Evan Grobbelaar (South Africa)
through real live trading sessions and is documented at:
https://github.com/Evangrobbelaar/trading-context

We are building my own version — customised to my broker, my instruments,
my account size, and my trading history. Nothing is carried over from the
original except the architecture.

Work through this setup sequentially. Ask me questions at each stage.
Do not skip ahead. Do not assume my details — ask for them.

---

## STAGE 1 — UNDERSTAND MY SETUP

Ask me these questions one at a time and wait for my answers:

1. What broker and trading platform are you using?
   (e.g. ThinkMarkets/ThinkTrader, MetaTrader 4/5, cTrader, OANDA)

2. Does your broker have an MCP (Model Context Protocol) server?
   If yes, what is the tool prefix and server URL?
   If no, we will use a manual data entry approach instead.

3. What is your account currency?
   (e.g. ZAR, USD, GBP, EUR)

4. What accounts do you have?
   For each: account number, type (demo/live), current balance.
   Which account should we start with? (Recommendation: always start demo.)

5. What instruments do you trade or want to trade?
   (e.g. Gold/XAUUSD, EURUSD, GBPUSD, USDJPY, indices, stocks)
   For each instrument: what lot size or unit size have you been using?

6. What is your base account balance for the first session?
   This determines your risk sizing — we build the enforcer around this.

7. Do you have any existing trading rules, checklists, or lessons learned?
   If yes, share them now — we will formalise them into the system.
   If no, we build the ruleset from scratch through real sessions.

8. What is your trading goal?
   (e.g. grow account from X to Y, consistent monthly income, learning)

9. What time zone are you in?
   All session times in this system are local to you.

10. What trading sessions are you typically available for?
    (e.g. London open 09:00-12:00, NY open 15:00-18:00 — in your local time)

---

## STAGE 2 — GITHUB REPOSITORY SETUP

Once I have your answers, instruct me to:

1. Create a GitHub repository named: [my-name]-trading-context (or similar)
   Tell me to make it PRIVATE.

2. Create a Personal Access Token (PAT):
   - GitHub → Settings → Developer Settings → Personal Access Tokens → Classic
   - Tick "repo" for full repository access
   - Copy the token (starts with ghp_)

3. Give you the repo URL, username, and PAT.

Then clone the repo into the current Claude Code working directory using git.

---

## STAGE 3 — BUILD THE CORE FILES

Using my answers from Stage 1, build these five files in the repo:

### File 1: TRADING_CONTEXT.md
This is the "brain" — the single source of truth that every session reads.
Build it with these sections, filled with MY specific data:

- Version number and last updated date
- Verification protocol (confirmation phrase Claude must say at session start)
- My accounts (numbers, types, balances, which is default)
- My instruments with sizing rules (max lots/units, SL buffers, value per pip/pt)
- My session schedule in my local time zone
- News calendar rules (which events affect my instruments)
- Pre-trade checklist (10 items, customised to my instruments)
- Trading rules (start with the universal ones below, add mine as we trade)
- Critical lessons (empty at first, grows with real experience)
- Performance history (table format, empty at first)

Universal starter rules to include (these apply to all traders):
- Rule 1: Never trail SL to breakeven. Trail to nearest structural level with buffer.
- Rule 2: SL must be outside the instrument's noise zone. Minimum buffers matter.
- Rule 3: Only trail after a new swing point confirms in trade direction.
- Rule 4: At 50%+ of TP, assess momentum. Shrinking candles = close immediately.
- Rule 5: Cut losers fast when structure reverses. Do not hold hope trades.
- Rule 6: Match instrument to session. Never trade closed or illiquid markets.
- Rule 7: Always scan 5+ instruments. Best setup wins — not the first one found.
- Rule 8: Size correctly for account. Risk per trade: maximum 20% of balance.
- Rule 9: H4 + H1 + M15 confluence = entry minimum. Set TP and let it fill.
- Rule 10: Risk per trade must be calculated explicitly before every entry.

### File 2: CLAUDE.md
This is the session bootstrap — Claude Code reads this automatically on startup.
Build it with:
- Mandatory first action: read TRADING_CONTEXT.md, confirm with verification phrase
- My broker MCP connection details (or manual data entry instructions if no MCP)
- My default account (always demo to start)
- Master rule: make money and stay profitable
- Full tick protocol: time check → position monitor → market scan → enforcer → log
- Session times (my local time zone)
- Loop stop conditions (consecutive losses, drawdown %, max ticks, session end)
- Session end protocol (summary → commit to GitHub)

### File 3: enforcer.py
A Python script that enforces numeric rules only. It cannot be talked around.
Build it with my specific instrument rules:
- Maximum lot/unit sizes per instrument
- Minimum and maximum SL distance per instrument (noise zone protection)
- Instruments blocked below certain balance thresholds
- Permanently banned instruments (if any)
- Maximum risk % per trade (20% default — ask me if I want to change this)
- Minimum R:R ratio (1.2:1 default — ask me if I want to change this)

The script must:
- Accept all trade parameters as command-line arguments
- Exit code 0 = PASS (trade allowed)
- Exit code 1 = BLOCKED (trade not allowed, reasons printed)
- Append every check to enforcer_audit.jsonl (pass or fail, never hide)

### File 4: session_logger.py
A Python script that logs every tick to session_log.jsonl.
Parameters: tick number, local time, session name, account balance,
open positions, H4 trend summary, candidate trades found, enforcer result,
trade placed, action taken, notes.
Also include a summary mode: python3 session_logger.py summary

### File 5: LOOP_SETUP.md
The operational guide. Build it with:
- Should I leave it running 24/7? Answer honestly based on my sessions.
- My two recommended daily session windows (based on my answers to Stage 1)
- Exact /loop commands for each session (copy-paste ready)
- Weekly review prompt (reads logs, proposes rule changes, never auto-commits)
- My instrument sizing reference table
- Enforcer quick reference commands
- How to stop the loop at any time

---

## STAGE 4 — FIRST SESSION

Once all files are built and pushed to GitHub:

1. Switch to my demo account via MCP (or confirm manual connection)
2. Run the verification: read TRADING_CONTEXT.md and confirm the phrase
3. Start the first trading session loop using the command in LOOP_SETUP.md
4. Run ticks, scan markets, monitor positions
5. After the session, append the session summary to TRADING_CONTEXT.md
6. Commit to GitHub with message: "Session [date] — first session — [P&L] — [N] trades"

---

## STAGE 5 — LEARNING SETUP

After the first session:

1. What worked? Note it in TRADING_CONTEXT.md as a rule candidate.
2. What lost? Root-cause it immediately. One sentence. Add to Critical Lessons.
3. Set a reminder to run the weekly review every Monday before your first session.

The weekly review prompt (already in LOOP_SETUP.md) reads all logs since last
Monday and proposes specific rule additions as a diff. You approve before anything
is committed. Risk parameters always need explicit approval.

---

## WHAT THIS SYSTEM DOES

Once built:

EVERY TICK (on a timer, automatically):
→ Checks your account balance and open positions
→ Scans your instruments for setups
→ Applies H4 trend gate (no counter-trend trades)
→ Runs enforcer.py before any trade (numeric rules, cannot be bypassed)
→ Places trade if enforcer passes, blocks if not
→ Logs everything to session_log.jsonl

EVERY SESSION END (automatically):
→ Pulls closed trades, calculates P&L
→ Appends session summary to TRADING_CONTEXT.md
→ Commits to GitHub

EVERY MONDAY (manually triggered):
→ Reads all session logs since last review
→ Identifies patterns, losses, blocked trades
→ Proposes rule improvements as a diff
→ You approve before anything changes

The system "learns" by the written ruleset getting more precise each week.
Not model fine-tuning — rule refinement. Every loss becomes a lesson.
Every pattern becomes a rule. The enforcer enforces the rules as code, not text.

---

## CRITICAL PRINCIPLES (non-negotiable, built into every file)

1. The enforcer cannot be bypassed. Not by the trader. Not by Claude.
   If the trade can't pass the enforcer, it should not be placed.

2. The H4 trend gate is absolute. No counter-trend trades.
   A bounce inside a downtrend is NOT a long setup. Ever.

3. Risk is calculated explicitly before every trade.
   No estimating. No "it's probably about 15 pips." Exact numbers.

4. The session log is honest. Every tick is logged — pass, block, hold, no-trade.
   Nothing is swept under the rug. The review loop reads the real record.

5. Risk parameters are human-approved.
   The weekly review proposes changes. The human approves. Claude never
   auto-commits a change to lot sizes, SL buffers, or risk percentages.

---

## ATTRIBUTION

This system architecture was designed by Evan Grobbelaar (South Africa) in June 2026
through real live trading sessions. Original repository:
https://github.com/Evangrobbelaar/trading-context

If this system helps you — whether trading, learning, or adapting it to something
else — a simple credit goes a long way.

---

## READY?

Start with Stage 1, Question 1. Ask me what broker I use.

---

## END OF PROMPT

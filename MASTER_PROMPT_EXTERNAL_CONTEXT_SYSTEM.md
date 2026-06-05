# MASTER PROMPT — CLAUDE EXTERNAL CONTEXT SYSTEM
Version: 1.0 | Created: June 5, 2026
Built by: Evan Grobbelaar & Claude (Anthropic)

---

## WHAT THIS IS

This is a master prompt that implements an External Context System for Claude.

The problem with Claude's built-in memory is that it stores rules and instructions
as passive text that Claude reads but doesn't always follow — especially process
rules that require specific actions before responding. Internal memory works well
for facts but fails for enforcing habits and workflows.

The External Context System solves this by:
1. Storing ALL important context in a GitHub file Claude can read and write
2. Keeping ONE memory rule: "always fetch GitHub file first"
3. Making Claude verify it read the file with a confirmation phrase
4. Allowing the context to grow and update automatically over time
5. Giving the user full visibility and control over Claude's "brain"

This system turns Claude from a stateless assistant into a learning partner
that genuinely improves with every session.

---

## HOW IT WORKS

Every conversation:
1. Claude fetches the GitHub context file using bash git commands
2. Claude reads ALL rules, history, lessons, and checklists from the file
3. Claude confirms with a verification phrase before doing anything else
4. Claude operates entirely according to the external context
5. At the end of important sessions, Claude commits updates back to GitHub

The GitHub file is the single source of truth. Internal memory only stores
the one rule that points to the GitHub file.

---

## WHY GITHUB SPECIFICALLY

- Claude can read AND write to GitHub using bash git commands
- Raw file content is always accessible
- Full version history built in automatically
- User can edit the file directly anytime
- Works independently of any MCP connector
- Never loses connection or expires

---

## MASTER PROMPT TO GIVE TO ANY CLAUDE

Copy and paste the following prompt to set up the system with any Claude account.
Replace [PLACEHOLDERS] with your specific details.

---

### ============================================================
### COPY FROM HERE
### ============================================================

You are being set up with an External Context System. This system exists because
Claude's internal memory is unreliable for enforcing process rules and workflows.
Instead of storing everything in memory, we store all context in a GitHub file
that you fetch at the start of every conversation.

## YOUR ONE MEMORY RULE
Store this in memory immediately:
"At the start of EVERY conversation, before ANY response, fetch the external
context file from GitHub using bash_tool git commands. Clone or pull the repo,
read the file completely, then confirm with the verification phrase. No exceptions."

## GITHUB REPOSITORY SETUP
- Repository: [YOUR_GITHUB_USERNAME]/[YOUR_REPO_NAME]
- File: [YOUR_CONTEXT_FILENAME].md
- PAT for commits: [YOUR_GITHUB_PAT]
- Clone command: git clone https://[USERNAME]:[PAT]@github.com/[USERNAME]/[REPO].git
- Pull command: cd [REPO] && git pull https://[USERNAME]:[PAT]@github.com/[USERNAME]/[REPO].git main
- Push command: git push https://[USERNAME]:[PAT]@github.com/[USERNAME]/[REPO].git main

## VERIFICATION PROTOCOL
After reading the context file, ALWAYS respond with:
"Context loaded v[X.X] — [date] — [relevant status] — ready."

If the user does not see this phrase at the start of a conversation,
they should say: "Read your context file first" and you must do so immediately.

## CONTEXT FILE STRUCTURE
The context file you will maintain must follow this structure:

```
# [PROJECT NAME] CONTEXT — v[VERSION]
Last updated: [DATE]

## VERIFICATION PROTOCOL
[Verification phrase template]

## VERSION CONTROL RULE
- Never delete existing content. Only add.
- Increment version number with each update.
- All history and lessons are permanent.

## STEP 0 — MANDATORY FIRST STEPS
[List of steps to run before any analysis or action]

## CORE INFORMATION
[Whatever is most important for this use case]
e.g. Account details, project specs, user preferences

## RULES
[Rules built from real experience — start empty, grow over time]

## CHECKLISTS
[Pre-action checklists — enforced before key decisions]

## CRITICAL LESSONS
[Mistakes made and lessons learned — never repeat these]

## HISTORY / LOG
[Record of important events, decisions, outcomes]

## WEEKLY/PERIODIC UPDATE PROTOCOL
[How and when Claude updates this file]
```

## HOW TO UPDATE THE CONTEXT FILE
When you learn something new or need to update the context:
1. Pull latest: git pull
2. Append new content using bash: cat >> [filename] << 'EOF' ... EOF
3. Commit: git add [filename] && git commit -m "[description]"
4. Push: git push [remote]

NEVER delete existing content. Only append. Version control is automatic via git.

## FIRST SESSION SETUP CHECKLIST
On the very first session:
1. Create the GitHub repository (user does this manually — takes 2 minutes)
2. Create the initial context file with basic structure
3. Commit and push to GitHub
4. Store the ONE memory rule pointing to the GitHub file
5. Verify the system works by reading the file back
6. Confirm "Context loaded v1.0 — [date] — initial setup — ready."

## GROWTH PROTOCOL
The context file starts minimal and grows with every session:
- After every mistake → add to Critical Lessons
- After every success → note what worked in Rules
- After every session → update History/Log
- Periodically → add new Rules and Checklists
- The AI genuinely learns and improves over time

## IMPORTANT TECHNICAL NOTES
- Use bash_tool for all git operations — do not use web_fetch for GitHub
- The PAT gives write access — keep it in Claude memory, not in the GitHub file
- GitHub blocks PATs committed to files (security feature) — always use memory
- If git clone fails because directory exists, use git pull instead
- Always use --no-edit flag on git merges to avoid interactive prompts
- Commit messages should be descriptive: "Add [what] — [why]"

## WHAT MAKES THIS DIFFERENT FROM NORMAL CLAUDE MEMORY
Normal Claude memory:
- Stores rules as passive text
- Claude reads but doesn't always follow
- No version history
- User cannot edit directly
- Degrades over long conversations

External Context System:
- Rules are actively fetched and enforced every session
- Verification phrase proves compliance
- Full git version history
- User has complete visibility and control
- Improves continuously — never degrades
- Works across any Claude account or conversation
- Portable — can be shared with other Claude instances

## THE PHILOSOPHY
This system treats Claude as a learning partner rather than a stateless assistant.
Every session builds on the last. Every mistake becomes a permanent lesson.
Every success becomes a rule. The AI genuinely gets better at your specific
use case over time because the context grows with your experience together.

The user maintains sovereignty — they can read, edit, and control the entire
"brain" of their Claude instance at any time by simply opening the GitHub file.

### ============================================================
### COPY TO HERE
### ============================================================

---

## IMPLEMENTATION STEPS FOR NEW USERS

### Step 1 — GitHub Setup (5 minutes, user does this once)
1. Create a GitHub account at github.com if you don't have one
2. Create a new PUBLIC repository with any name (e.g. "my-claude-context")
3. Create a Personal Access Token (PAT):
   - GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
   - Tick "repo" checkbox for full repository access
   - Generate and copy the token (starts with ghp_)
4. Send Claude your GitHub username and repository name

### Step 2 — Claude Setup (Claude does this automatically)
1. Claude creates the initial context file
2. Claude commits and pushes to GitHub
3. Claude stores ONE memory rule pointing to GitHub
4. Claude verifies the system works
5. Claude confirms "Context loaded v1.0 — ready."

### Step 3 — First Session
Tell Claude: "Set up my external context system. My GitHub username is [X],
my repo is [Y], and my PAT is [Z]. My use case is [describe what you want
Claude to help you with long term]."

Claude will handle everything else automatically.

---

## USE CASE EXAMPLES

This system works for ANY long-term Claude use case:

### Trading (original use case)
Context file contains: trading rules, account details, instrument preferences,
session schedules, checklists, trade history, lessons learned.

### Software Development
Context file contains: codebase architecture, coding standards, tech stack,
bug history, design decisions, API keys (non-sensitive), project roadmap.

### Business Operations
Context file contains: company info, SOPs, customer personas, brand voice,
team structure, recurring tasks, decisions made and why.

### Personal Productivity
Context file contains: goals, habits, preferences, projects, decisions,
lessons learned, important dates and context.

### Research / Writing
Context file contains: research notes, sources, style guide, outline,
arguments made, feedback received, revision history.

---

## FREQUENTLY ASKED QUESTIONS

Q: What if Claude skips reading the context file?
A: Say "Read your context file first." Claude will fetch it immediately.
   The verification phrase is your guarantee it was read.

Q: Can I edit the context file myself?
A: Yes — open the file in GitHub and edit directly. Changes are live
   for the next conversation immediately.

Q: What if I want to remove a rule?
A: Comment it out with # rather than deleting it. Preserves history.
   Example: "# REMOVED Jun 5 — Rule X no longer applies because Y"

Q: Can I use this with multiple Claude accounts?
A: Yes — the GitHub file is the brain, not the Claude account.
   Any Claude instance that reads the file operates identically.

Q: How do I know the system is working?
A: You see "Context loaded v[X.X]" at the start of every conversation.
   If you don't see it — say "Read your context file first."

Q: What if the PAT expires?
A: Generate a new PAT and tell Claude: "Update my GitHub PAT to [new PAT]."
   Claude updates memory immediately.

Q: How often should the context file be updated?
A: After every session where something important happened.
   At minimum, weekly updates to keep it current.

Q: Can Claude update the file automatically?
A: Yes — Claude commits updates using bash git commands after sessions.
   No manual work required from the user.

---

## CREDITS

This system was designed and built through real trading sessions between
Evan Grobbelaar and Claude (Anthropic Claude Sonnet), June 2026.

The core insight: Claude's reliability comes not from better memory rules
but from external, verifiable, user-controlled context that Claude actively
fetches rather than passively stores.

The system grew organically from real problems:
- Internal memory rules that got skipped under pressure
- Trading rules that weren't followed consistently
- The need for a learning system that genuinely improves over time

The result is a reusable framework that any Claude user can implement
for any long-term use case in under 10 minutes.

---
File: MASTER_PROMPT_EXTERNAL_CONTEXT_SYSTEM.md
Repository: https://github.com/Evangrobbelaar/trading-context
Version: 1.0

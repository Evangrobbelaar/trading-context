# Claude ECS — Build Archive
**Date:** 2026-06-09
**Authors:** Evan Grobbelaar + Claude (Sonnet 4.6)
**Status:** Middleware live, artifact built, system operational

---

## What Was Built

**Claude ECS (External Context System)** — a persistent memory system for Claude that survives across sessions. Context lives in a GitHub repo. Claude reads it at session start and writes back at session end.

---

## The Problem We Solved

Claude has no memory between sessions. Every conversation starts blank. The ECS system fixes this by storing a structured markdown context file on GitHub that Claude fetches automatically.

---

## Architecture — Three Layers

### Layer 1 — GitHub Repo (user owns this)
A private GitHub repo containing a markdown context file. The source of truth for the user's persistent memory. Can contain anything — trading rules, business context, preferences, ongoing work.

### Layer 2 — VPS Middleware (Evan hosts this)
A 20-line FastAPI CORS proxy running on `2.24.130.64:8091`. Its only job is to sit between the browser and GitHub API, adding CORS headers so browser fetch calls work. Stateless. No database. No auth of its own.

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.api_route("/github/repos/{owner}/{repo}/contents/{path:path}", methods=["GET","PUT","OPTIONS"])
async def proxy(owner: str, repo: str, path: str, request: Request):
    async with httpx.AsyncClient() as client:
        r = await client.request(
            method=request.method,
            url=f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers={"Authorization": request.headers.get("Authorization",""),
                     "Accept": "application/vnd.github.v3+json",
                     "User-Agent": "ClaudeECS/1.0",
                     "Content-Type": "application/json"},
            content=await request.body()
        )
    return r.json()
```

### Layer 3 — Browser Artifact (Claude renders this)
An HTML/JS artifact that Claude renders in any session. User pastes PAT once, clicks Load, edits, saves. No bash_tool needed. Works on any Claude model, any session.

Routes:
- `GET /github/repos/{owner}/{repo}/contents/{path}` — read file
- `PUT /github/repos/{owner}/{repo}/contents/{path}` — write file
- Headers: `Authorization: Bearer <PAT>` and `ngrok-skip-browser-warning: 1`

---

## The Two Access Paths

### Path A — bash_tool (Evan's current system)
When bash_tool is available (claude.ai Sonnet sessions), Claude uses git directly:
```bash
git clone https://USERNAME:PAT@github.com/USERNAME/REPO.git
cat REPO/CONTEXT.md
# ... make changes ...
git push https://USERNAME:PAT@github.com/USERNAME/REPO.git main
```
PAT stored in userMemories as part of a workflow instruction (not as a naked credential). Works automatically every session. No middleware needed.

### Path B — Artifact + Middleware (universal)
When bash_tool is unavailable (most models, most sessions), Claude renders the context editor artifact. User pastes PAT, artifact calls middleware, middleware calls GitHub. Works everywhere.

---

## Key Technical Discoveries

### 1. CORS blocks direct browser → GitHub API calls
GitHub's API rejects fetch calls from browser origins (like claude.ai). This is enforced at GitHub's end and cannot be bypassed client-side. A server proxy is required.

### 2. Cloudflare Workers — blocked by account WAF
Attempted to use Cloudflare Workers as the proxy. Tony's account had WAF/zone rules returning `Host not in allowlist`. Could not resolve without disabling account-level security rules.

### 3. ngrok domain blocked by Claude's sandbox
Claude's bash_tool sandbox blocks outbound connections to ngrok and Cloudflare tunnel domains (`*.ngrok-free.dev`, `*.trycloudflare.com`). This caused Claude to incorrectly diagnose working middleware as broken. The middleware was fine — only Claude's curl tests were failing.

### 4. FastAPI TrustedHostMiddleware
Initial deployment included `TrustedHostMiddleware` which rejected ngrok/tunnel hostnames. Took multiple iterations to identify and remove. Final app has no host restrictions — pure CORS proxy only.

### 5. PAT storage framing matters
Cautious Claude models refuse to store a PAT directly. The same PAT stored as part of a workflow instruction (describing how git is used, with PAT embedded in the URL format) passes without friction. Framing as operational context vs credential storage produces opposite model behaviour.

### 6. Claude's sandbox network restrictions
Claude's bash_tool can reach: github.com, pypi.org, npmjs.com, and other whitelisted domains. It cannot reach: ngrok tunnels, Cloudflare tunnels, arbitrary VPS IPs on non-standard ports (confirmed port 8091 on 2.24.130.64 times out from sandbox). This is a hard Anthropic network policy, not a firewall issue on the VPS.

---

## What Claude Code Built

Two files delivered by Claude Code:

**CLAUDE_AI_PROJECT_INSTRUCTIONS.md** — Project-level instructions that tell Claude to auto-load context at session start using a silent artifact. Includes read and write artifact templates.

**CLAUDE_ECS_SKILL.md** — Skill file describing the full ECS system, proxy URL, routes, headers, and rules for automatic context management. Covers both bash_tool path (curl) and browser artifact path.

---

## Current Live URLs

- **Middleware (ngrok tunnel):** `https://inspiritingly-ventless-fidela.ngrok-free.dev`
- **VPS direct:** `http://2.24.130.64:8091` (blocked from Claude sandbox, works from browser)
- **Tony's repo:** `tonyhobbyearl-lang/Tony-trading`
- **Evan's repo:** `Evangrobbelaar/trading-context`

---

## Product Vision — Claude ECS

**The pitch:** Every Claude session starts blank. Claude ECS fixes that.

**Three tiers:**

| Tier | What | Price |
|------|------|-------|
| Community | Open source template + setup guide + bash_tool path | Free |
| Pro | Hosted middleware + artifact + onboarding + context templates | ~$9-15/month |
| Premium | Everything + pre-built skill templates (trading, business, dev) + priority uptime | ~$25-30/month |

**Target users:** Power Claude users who feel the pain of session amnesia — traders, developers, entrepreneurs, anyone with complex ongoing workflows.

**Differentiator:** Not a Claude plugin or integration. Works with the existing Claude interface. No Anthropic approval needed. Pure external infrastructure.

---

## What's Left To Do

- [ ] Confirm artifact works end-to-end from browser (middleware confirmed working on localhost, ngrok tunnel live)
- [ ] Move middleware from ngrok to permanent VPS port with proper firewall rules
- [ ] Build landing page for Claude ECS product
- [ ] Write community template and setup guide
- [ ] Set up Gumroad product for Pro tier
- [ ] Test Tony's full flow end-to-end

---

## Lessons For Future Sessions

1. Don't ask Claude to test ngrok/Cloudflare URLs with curl — sandbox will always block them
2. Test middleware from browser only, or from inside the VPS with curl localhost
3. When Claude says middleware is broken based on curl — it's wrong, the sandbox is blocked
4. The artifact is the correct test — browser fetch bypasses sandbox restrictions entirely
5. Keep middleware dead simple — 20 lines, no extra middleware, no host restrictions

---

*Archived from live build session — Evan Grobbelaar + Claude Sonnet 4.6 — June 2026*

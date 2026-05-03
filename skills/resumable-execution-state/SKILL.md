---
name: resumable-execution-state
description: Persist a multi-step batch's mid-execution state to disk so any future Claude session can pick up exactly where the previous one stopped — even mid-bump.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    rootRequest: "the user's overall ask (e.g. 'execute all four cubos')"
    plan: "ordered list of bumps/batches and what each one delivers"
  outputSchema:
    file: "SESSION_STATE.md at repo root, updated after every material operation"
  errorHandling:
    contextExhaustion: "the file IS the recovery; no extra action needed beyond writing it"
    mid-bumpInterrupt:  "next session diff-checks unsuffixed file vs last _vNNN to see how far the bump got"
  stateless: true
tools: [Write, Edit, Read, Bash]
---

# resumable-execution-state

## Purpose
When a user asks for work that **may exceed a single session's token budget** ("execute all the cubos", "implement the whole roadmap", "ship 5 versions", "run the daily sweep for a month"), commit to it but engineer the work so a different Claude (or you in a fresh session) can resume cleanly. The mechanism is a single file at the repo root — `SESSION_STATE.md` — that is updated **after every material operation**, not just at the end.

This skill is what saved the v005-v009 batch in the C23 project: the user asked for all four cubos, knowing the session might die. None did, but the safety net was real.

## When to use
- The user explicitly says "in case I run out of tokens" / "save state" / "be resumable".
- The plan has more than one bump / version / batch step.
- The plan reads as ≥ 2 hours of focused work even with parallel tool calls.
- A long autonomous loop (`/loop`, recurring schedule) where each iteration must be self-orienting.

## Inputs
- The user's root request (verbatim).
- The plan you've decided to follow — versioned, with explicit deliverables per bump.

## Outputs
- `SESSION_STATE.md` at the repo root, with these sections:
  1. **Header** — root request (verbatim), start date.
  2. **Plan table** — one row per bump/batch, each with `⏳ pending` / `✅ DONE`.
  3. **Procedure** — the canonical workflow for every bump (so the next agent doesn't have to re-derive it; usually a pointer to a SKILL.md like `versioning-workflow`).
  4. **"Where I am right now"** — last action + next action + current chain state. Updated after every snapshot or significant edit.
  5. **Per-bump execution log** — checkbox list (`- [ ]` / `- [x]`) of the items in that bump.
  6. **Resume procedure** — a numbered "how to resume from this file" block that the next session reads first.

## Instructions

1. **Write the file before doing any actual work.** It's the bug-out plan, not the post-mortem.
2. **Plan in versioned bumps**, not monolithic batches. Each row of the plan table maps to one snapshot artefact (e.g. `_v005.html`).
3. **Update after every material operation.** Material = a snapshot, a tab added, a major Edit, a script created. Skipping updates defeats the purpose.
4. **Always include a "Resume procedure" block** at the end of the file — assume the next session reads nothing else of yours. The block must be enough to recover.
5. **Show the live file chain** (`ls C23_DIANA_NATO_WARFIGHTERS*.html`) inside the "Where I am" block so the recovering agent can sanity-check at a glance.
6. **Diff-check protocol for mid-bump interrupts:** the recovering agent compares the unsuffixed working file against the latest `_vNNN.html` (stripping the changelog header). Any drift = this session was mid-bump; pick up at the first unfinished checkbox.
7. **Mark a bump done in three places at once** when sealing it: the plan-table row (✅ DONE), the per-bump log (all `[x]`), the "Where I am" line. Use a single Edit per place; do NOT rely on the next session to figure out which plane of truth wins.
8. **Never delete prior `⏳ pending` entries.** They are the audit trail. Flip to ✅, do not erase.
9. **Pair with `versioning-workflow`** so prior `_vNNN.html` are byte-identical (md5-verifiable) — that is what lets the diff-check trick work.

## Examples

### Plan table that worked for the v005-v009 run
```markdown
| Bump | Cubo | Items | Status |
|------|------|-------|:------:|
| **v005** | **A** — 6 prioritarios | … | ✅ DONE |
| **v006** | **C** — 8 UX/QoL    | … | ✅ DONE |
| **v007** | **D** — 5 visuales  | … | ✅ DONE |
| **v008** | **B easy** — 4     | … | ✅ DONE |
| **v009** | **B hard** — 4     | … | ✅ DONE |
```

### "Where I am" block format (compact, three lines max)
```markdown
**Last action:** v007 sealed. Cubo D complete.
**Next action:** start v008 (Cubo B easy — AN-02 + LD-02 + WF-05 + CO-02).

**Live SPA chain after v007:**
```
C23_DIANA_NATO_WARFIGHTERS.html        (= v007, ~226 KB)
C23_DIANA_NATO_WARFIGHTERS_v001.html
…
```

### Resume procedure block to ship verbatim
```markdown
## How to resume from this file
1. `cat SESSION_STATE.md` — read end-to-end.
2. Find the lowest ⏳ row in the plan table — that's the next bump.
3. Look at "Where I am" for the exact mid-bump checkpoint.
4. If the unsuffixed file differs from the latest _vNNN.html, the previous
   session was mid-bump. Diff against `_vNNN.html` (strip changelog header).
5. Continue from the next [ ] in the active bump's execution log.
6. After every Edit/Write, update the relevant checkbox + "Last action" line.
7. When a bump completes (all [x], snapshot done, verified), bump the table,
   clear "Where I am", move to the next ⏳ row.
```

## Anti-patterns
- ❌ Updating `SESSION_STATE.md` only at the end. Defeats the entire purpose.
- ❌ A "Where I am" line that says "in progress". Useless for recovery — say what you just did and what comes next.
- ❌ Writing aspirational future bumps as `[x]`. Only mark a checkbox once the work landed in a snapshot.
- ❌ A plan with 1 row. If there's only one bump, you don't need this skill.
- ❌ Embedding the state file inside the SPA / inside another artefact. It must be a free-standing top-level file.

## References
- `SESSION_STATE.md` (repo root) — worked example from the v005-v009 batch.
- Skill `versioning-workflow` — the bump mechanic this skill is built on top of.
- Skill `roadmap-driven-release` — the inverse: pick *what* to bump; this skill protects the bump itself.

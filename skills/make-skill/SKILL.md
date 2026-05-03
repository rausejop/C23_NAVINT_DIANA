---
name: make-skill
description: Author a new Agent Skill in the C23 catalogue. Use when adding a reusable capability that future agents should be able to discover and apply.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    skillName: kebab-case identifier
    purpose: one-sentence description of when the skill should fire
    optionalReferences: list of doctrine, standards or files the skill points back to
  outputSchema:
    file: skills/<skillName>/SKILL.md
    indexEntry: row appended to skills/README.md
  errorHandling:
    duplicateName: refuse and surface the existing skill instead
    missingPurpose: refuse; descriptions are the only thing model selectors see
  stateless: true
tools:
  - Read
  - Write
  - Edit
  - Bash
---

# make-skill — author a new Agent Skill

## Purpose
Provide a single, opinionated procedure for adding a new skill to `skills/` that:

- Will be **discoverable** by a model selector (good `description:` line).
- Is **stateless and reusable** across projects (no embedded session state).
- Is **self-contained** (one `SKILL.md`; helper files only when justified).
- Conforms to the SLO Agent Skills framework referenced in the Master Prompt ANNEX.

## When to use
- A capability has been exercised more than once (or is expected to be).
- A capability is non-obvious enough that a future agent would benefit from a runnable recipe rather than re-deriving it.

## Inputs
- `skillName` — kebab-case, also the directory name.
- `purpose` — one-sentence trigger that completes "Use this skill when …".
- (optional) helper files: scripts, templates, sample outputs.

## Outputs
- `skills/<skillName>/SKILL.md`
- An appended row in `skills/README.md` index table.

## Instructions

1. **Pick the name.** Kebab-case, ≤ 40 chars, verb-first when possible (`build-…`, `extract-…`, `summarize-…`).
2. **Create the directory.**
   ```bash
   mkdir -p "skills/<skillName>"
   ```
3. **Author `SKILL.md`** with the following skeleton (copy verbatim, then fill):
   ````markdown
   ---
   name: <skillName>
   description: <one sentence — what triggers this skill>
   version: 1.0.0
   author: <handle or org>
   slo:
     inputSchema:  { … }
     outputSchema: { … }
     errorHandling: { … }
     stateless: true
   tools:
     - Read
     - Write
   ---

   # <skillName> — <short title>

   ## Purpose
   ## When to use
   ## Inputs
   ## Outputs
   ## Instructions     (numbered, imperative)
   ## Examples         (input → expected output, abbreviated)
   ## Anti-patterns    (what NOT to do; reasons)
   ## References       (doctrine / standards / source files)
   ````
4. **Write the description first.** It is the only line a selector sees. Bad: `"Helper for builds"`. Good: `"Build a self-contained HTML SPA with React + Babel-standalone, no bundler."`
5. **Make instructions imperative and numbered.** Each step must be runnable; if a step says "consider", rewrite it as a check or a default.
6. **Pin references.** Cite by file path with the relative-to-repo prefix; for external standards, include the URL and the version (`CycloneDX 1.7`).
7. **Append the index row** to `skills/README.md`:
   ```md
   | <next #> | [`<skillName>`](<skillName>/SKILL.md) | <one-sentence purpose> |
   ```
8. **Verify discoverability.** A future agent reading only the index + your description must understand when to invoke.
9. **Commit nothing else.** Skills must not write to memory, ask the user, or reach the network unless their purpose explicitly demands it.

## Examples

### Minimal skill — `extract-pdf-titles`
```markdown
---
name: extract-pdf-titles
description: Extract section titles from a PDF using pdftotext and a regex; returns markdown.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:  { pdfPath: string }
  outputSchema: { markdown: string }
  errorHandling: { missingPdftotext: "instruct user to install poppler-utils" }
  stateless: true
tools: [Bash, Read]
---
# extract-pdf-titles
## Purpose
Extract numbered headings from a PDF for indexing.
## Instructions
1. `pdftotext -layout "$pdfPath" -`
2. Filter lines matching `^\s*[0-9]+(\.[0-9]+)*\s+\S`.
3. Emit as `- 3.2 Land Operations` markdown bullets.
## References
- `man pdftotext`
```

## Anti-patterns
- ❌ A skill named `helpers` — too vague to ever match a request.
- ❌ A skill that requires the user to provide the same context the skill itself defines.
- ❌ A skill whose `Instructions` are prose recommendations rather than steps.
- ❌ Skills that mutate global state, write to memory or modify settings without saying so up-front.

## References
- `skills/README.md` — index format.
- Master Prompt `ANNEX § 1` — SLO Agent Skills framework requirement.
- <https://agentskills.io/specification> — SLO Agent Skills external specification (per Master Prompt).

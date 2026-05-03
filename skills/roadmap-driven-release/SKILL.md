---
name: roadmap-driven-release
description: Plan and execute a new SPA version by pulling a prioritised batch of items from roadmap.md and shipping them as a strict superset.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    roadmap: "roadmap.md (output of skill doctrine-roadmap-synthesis)"
    targetVersionNote: "free-text user request (or 'next iteration')"
  outputSchema:
    newVersion: "C23_DIANA_NATO_WARFIGHTERS_v(NNN+1).html with the picked batch implemented"
    deltaReport: "list of items shipped this version, mapped back to roadmap rows"
  errorHandling:
    emptyRoadmap: "abort and ask the user what to ship"
    nonAdditiveItem: "skip and surface to the user — superset rule applies"
  stateless: true
tools: [Read, Edit, Write, Bash]
---

# roadmap-driven-release

## Purpose
Bridge between `roadmap.md` (the doctrine-driven backlog) and `versioning-workflow` (the mechanical version-bumping rule). This skill picks **what** goes into the next bump, implements it as a superset, and reports the delta back to the roadmap.

## When to use
- The user says "implement the roadmap", "ship the next iteration", "do v1.1", "make v003".
- A new AJP edition has triggered roadmap items that should land in the next bump.
- The platform is at v00N and the user wants v00(N+1) without specifying every feature.

## Inputs
- `roadmap.md` (exists in repo root; if missing, run skill `doctrine-roadmap-synthesis` first).
- An optional batch description (e.g. "section 4 only", "all 🚧 items under § 3"). Default = the priority list at the bottom of `roadmap.md` (its § 9 in the current repo).

## Outputs
- A new `_v(NNN+1).html` produced via `versioning-workflow`.
- A deliverable-traceability section in the changelog header citing the roadmap rows that just turned ✅.
- (Optional) a fresh `roadmap.md` where the shipped items are flipped from 🚧 / ★ to ✅.

## Instructions

1. **Read `roadmap.md` end-to-end.** Identify the priority list (the "next iteration" section); locate the 🚧 / ★ items called out there.
2. **Cap the batch.** A version bump should ship a coherent batch — typically 4–8 items. Do not try to clear the whole roadmap in one bump.
3. **Triage each item against the superset rule:**
   - `+ Additive` (new feature / field / tab) → **eligible**.
   - `~ Improvement` (better UX of existing feature) → **eligible**.
   - `# Bug fix` → **eligible**.
   - "Remove X" / "deprecate Y" / "split into" → **NOT eligible**, surface to the user.
4. **Order intra-batch by data dependency**: schema additions first (default-mission fields), then state extensions (filters / tally), then UI additions (top-bar tiles / new tabs / map overlays).
5. **Call sub-skills** in order:
   - For each item, the relevant capability skill (e.g. `joint-targeting-jtc`, `movement-entities`, `posture-indicators`, `cyber-domain`, `neutral-side`).
   - Then `versioning-workflow` for the mechanical bump.
6. **Cite the roadmap rows** in the changelog header (`Source plan: roadmap.md § N — <section title>`).
7. **Run sanity checks** before reporting done: structural (one Babel block, one `createRoot`), behavioural (open the file in a browser if possible — see skill `build-single-file-spa § 7`).
8. **Update `roadmap.md` (optional but recommended).** For every item that just shipped, flip 🚧 / ★ → ✅ and add a "shipped in v00X" note in the Notes column. Do not delete the roadmap row — the audit trail matters.
9. **Report to the user**:
   - New version number + file paths.
   - Bullet list of what shipped (mirror the changelog).
   - Pointer to the roadmap rows that flipped to ✅.
   - Roadmap items left for the next bump.

## Examples

### v002 — first roadmap-driven release
- Source plan: `roadmap.md § 9` ("Implementation priority for the next iteration (v1.1)").
- Batch (6 items):
  1. Joint Targeting module (AJP-3.9) — see `joint-targeting-jtc`.
  2. Mission Type + Operation Type — `MissionTab` extensions.
  3. MSR / ASR + APOD / SPOD — see `movement-entities`.
  4. FPCON / CBRN / PNT / CIS-PACE indicators — see `posture-indicators`.
  5. CYBER 5th domain — see `cyber-domain`.
  6. NEUTRAL side — see `neutral-side`.
- Bonus carried into the same bump because the data plumbing was already touched: Master Narrative, CoG, End-state criteria, 23 acronyms, layer toggles for Movement and JPTL.
- Result: `C23_DIANA_NATO_WARFIGHTERS_v002.html`, 2707 lines (+534 vs v001), `Removed: NONE`.

## Anti-patterns
- ❌ Dumping the whole roadmap into one bump. The bump becomes hard to review and the changelog stops being useful.
- ❌ Implementing UI before the schema. The new tab will reference `mission.<key>` that does not yet exist on imported missions, and you'll get `undefined` everywhere.
- ❌ Skipping the roadmap update step. The next agent will re-attempt items that already shipped.
- ❌ Doing "tidy-up while you're in there" — refactoring unrelated code in the same bump. The superset rule still permits it but it makes regression review impossible. Keep bumps focused.
- ❌ Inventing items that aren't in the roadmap. If the user requests something off-roadmap, add it to the roadmap first, then ship.

## References
- `roadmap.md` — current backlog.
- `CLAUDE.md § "Versioning rule"` — superset rule.
- `versioning-workflow/SKILL.md` — mechanical bump.
- Capability skills: `joint-targeting-jtc`, `movement-entities`, `posture-indicators`, `cyber-domain`, `neutral-side`, `mission-editor`.
- `C23_DIANA_NATO_WARFIGHTERS_v002.html` — worked example (the file's changelog header is a verbatim instance of this skill's output).

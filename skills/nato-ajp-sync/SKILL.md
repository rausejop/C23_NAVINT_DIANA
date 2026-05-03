---
name: nato-ajp-sync
description: Sync the local mirror of NATO Allied Joint Publications from gov.uk into AJP/<NN> directories using the bundled Python script.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema: {}
  outputSchema:
    newFiles: list of newly downloaded PDFs
    publicationCount: total directories present after sync
  errorHandling:
    networkFailure: "abort with the failing URL; never partial-mirror silently"
    pdfsInRoot: "re-run; the script will move them into numbered folders"
  stateless: true
tools: [Bash]
---

# nato-ajp-sync

## Purpose
Refresh the local mirror of every NATO Allied Joint Publication held under `AJP/<NN> …/` from the official UK MOD collection, so that other skills (`ajp-doctrine-summary`, `doctrine-roadmap-synthesis`) work against the latest editions.

## When to use
- A new AJP edition is rumoured / known to have been released.
- Doctrine work is starting and the mirror has not been refreshed in this quarter.
- The user asks to "update doctrines", "sync AJPs".

## Inputs
- (none — the script discovers publications from the source page)

## Outputs
- New / updated PDFs in `AJP/<NN> <Title>/`.
- Stdout summary listing newly downloaded files and the total publication count.

## Instructions

1. **Verify the bundled script is present.**
   ```bash
   ls -1 "AJP/update_ajp_doctrines.py"
   ```
2. **Run it.**
   ```bash
   python "AJP/update_ajp_doctrines.py"
   ```
3. **Confirm completion** — the script prints `[*] Update complete.`
4. **Verify there are no PDFs in `AJP/` root.** If any landed there, re-run the script — it moves stragglers into numbered folders on the next pass.
5. **List newly downloaded files** to the user.
6. **Report the total count of publication directories** so changes are visible.
7. **If new publications appear**, immediately produce a per-AJP summary with skill `ajp-doctrine-summary`.

## Examples

### Idempotent re-run output (nothing to do)
```
[*] Fetching collection page: https://www.gov.uk/government/collections/allied-joint-publication-ajp
[*] Found 33 unique publication pages.
[1/33] Processing: Allied Joint Doctrine (AJP-01)
  [.] AJP_01_EdF_with_UK_elements.pdf is up to date.
…
[*] Update complete.
```

## Anti-patterns
- ❌ Editing the script to add `pip install` lines. It is stdlib-only by design, which is what makes it air-gappable on a tactical workstation that already has Python.
- ❌ Re-implementing the scraper instead of running it. The directory-naming convention (`NN Title`) is the contract; do not break it.
- ❌ Using `wget --mirror` against gov.uk — you will fetch the entire collection page tree, not just the PDFs.

## References
- `AJP/update_ajp_doctrines.py` — the canonical implementation (stdlib only).
- `AJP/update_ajp_skill.md` — original Antigravity skill spec the script wraps.
- `AJP/README.md` — index of currently mirrored publications.
- Source: <https://www.gov.uk/government/collections/allied-joint-publication-ajp>

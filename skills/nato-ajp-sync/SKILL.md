---
name: nato-ajp-sync
description: Sync the local mirror of NATO Allied Joint Publications from gov.uk into AJP/<NN>_<Title>/ directories (underscore-only naming) using the bundled Python script.
version: 1.1.0
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
Refresh the local mirror of every NATO Allied Joint Publication held under `AJP/<NN>_<Title>/` from the official UK MOD collection, so that other skills (`ajp-doctrine-summary`, `doctrine-roadmap-synthesis`) work against the latest editions.

**Naming contract:** directory names use underscores only — no spaces (`01_Allied_Joint_Doctrine_(AJP-01)`, not `01 Allied Joint Doctrine (AJP-01)`). The script in `AJP/update_ajp_doctrines.py` enforces this since 2026-05-07; if a future scrape lands a name with spaces, run `sanitize-folder-names` against `AJP/`.

## When to use
- A new AJP edition is rumoured / known to have been released.
- Doctrine work is starting and the mirror has not been refreshed in this quarter.
- The user asks to "update doctrines", "sync AJPs".

## Inputs
- (none — the script discovers publications from the source page)

## Outputs
- New / updated PDFs in `AJP/<NN>_<Title>/`.
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
- ❌ Re-implementing the scraper instead of running it. The directory-naming convention (`NN_Title`, underscores only) is the contract; do not break it.
- ❌ Reverting the underscore convention back to spaces. Spaces force every downstream consumer (Bash, Python globs, Markdown links) to URL-encode or quote the path — breaking shell pipelines and link tables. If you ever see a space-named directory, run `sanitize-folder-names`, do not rename ad-hoc.
- ❌ Using `wget --mirror` against gov.uk — you will fetch the entire collection page tree, not just the PDFs.

## References
- `AJP/update_ajp_doctrines.py` — the canonical implementation (stdlib only).
- `AJP/update_ajp_skill.md` — original Antigravity skill spec the script wraps.
- `AJP/README.md` — index of currently mirrored publications.
- Source: <https://www.gov.uk/government/collections/allied-joint-publication-ajp>

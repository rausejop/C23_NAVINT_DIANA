---
name: sanitize-folder-names
description: Rename subdirectories of a target folder to remove shell-hostile characters (spaces by default) and update every file that references the old paths in lock-step.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    targetDir: directory whose immediate subdirectories will be renamed (e.g. AJP/)
    charMap:   character substitutions to apply, default { " ": "_" }
    references: list of files whose hard-coded paths or link tables must be rewritten in the same commit (e.g. AJP/README.md, AJP/update_ajp_doctrines.py)
  outputSchema:
    renamed: list of (oldName, newName) pairs
    updatedReferences: list of files whose contents were rewritten
    skipped: list of (oldName, reason) for renames that did not happen
  errorHandling:
    targetExists:    "skip rename for that entry; never overwrite an existing path"
    referenceMissing: "warn; do not abort the rename batch"
    pdfsInside:      "do not rename a PDF file — only directories"
  stateless: true
tools: [Bash, Read, Edit, Write, Grep, Glob]
---

# sanitize-folder-names — keep directory paths shell-safe

## Purpose
Rename the immediate subdirectories of a target folder so their names do not contain characters that force every downstream consumer (Bash, Python globs, Markdown links, CI manifests) to URL-encode or quote the path. By default this means **spaces → underscores**, but the same procedure applies to any character map the caller supplies.

The skill is **rename + reference rewrite in one atomic operation**: a rename without updating the scripts and link tables that reference the old names is a regression, not a fix.

## When to use
- A scrape, download, or human-created folder lands inside the repo with spaces in the name (e.g. `AJP/34 New Publication Title/`).
- The user asks to "sanitize", "normalise", "rename without spaces", or "use underscores" on a directory tree.
- An existing convention (like `AJP/<NN>_<Title>/`) has been violated by a recent ingestion.

## Inputs
- **`targetDir`** — directory whose immediate subdirectories will be renamed. Recursion is *off* by default; opt in only if the caller explicitly asks.
- **`charMap`** — substitution table. Default: `{ " ": "_" }`. Common extensions: `(`, `)`, `&`, `+`, non-ASCII whitespace.
- **`references`** — files that must be rewritten so their links / hard-coded paths still resolve. Discover them with a single `Grep` for the literal old names *before* renaming.

## Outputs
- Renamed subdirectories under `targetDir`.
- Rewritten `references` files (link tables in `README.md`, hard-coded folder generation in scripts, etc.).
- A short report to the user listing renames, updated references, and any skips.

## Instructions

1. **Inventory before touching anything.** List the immediate subdirectories of `targetDir` and isolate the names that contain at least one `charMap` key.

   ```bash
   ls "<targetDir>"
   ```

2. **Discover dependent references.** Grep for the literal old folder names *and* any code that generates names:

   ```bash
   # link tables / docs
   grep -rln '<old name fragment>' .
   # script-side generators (Python, shell)
   grep -rln "f\"{idx:02d}\|os.path.join\|folder_name" "<targetDir>"
   ```

3. **Plan the new names.** For each candidate, apply the substitutions in `charMap`. Verify the target name does **not** already exist on disk.

4. **Rename atomically per entry.** Use a guarded loop so a pre-existing target never gets clobbered:

   ```bash
   cd "<targetDir>" && for d in */; do
     old="${d%/}"
     new="${old// /_}"
     if [ "$old" != "$new" ]; then
       if [ -e "$new" ]; then
         echo "SKIP (target exists): $old -> $new"
       else
         mv -- "$old" "$new"
         echo "OK: $old -> $new"
       fi
     fi
   done
   ```

   For a richer `charMap`, drop into Python (stdlib only) and apply `str.translate` per entry.

5. **Rewrite every reference file in the same change.** Two common patterns:
   - **Markdown link tables** with URL-encoded spaces: replace `%20` with `_` (only inside link targets — not in body text). `Edit` with `replace_all` is safe when `%20` only appears in link targets.
   - **Generators in code** (e.g. `update_ajp_doctrines.py`): patch the line that builds the folder name so it produces underscores by construction. The minimum-invasive form is `name = f"{idx:02d} {title}".replace(' ', '_')`. Do this so the *next* run is idempotent — never have to clean up again.

6. **Verify shell-safety.** After renaming, every path under `targetDir` must work with un-quoted Bash globs:

   ```bash
   ls "<targetDir>"/*/    # no errors, no `\ ` artifacts
   ```

7. **Verify reference integrity.** Re-grep for the *old* fragment; expect zero hits in code, scripts, and link tables. Body prose that mentions the old names historically may stay (it's narrative, not a path).

8. **Report to the user.** Three short lists: renamed (old → new), updated references (file paths), skipped (old → reason).

## Examples

### Sanitizing the `AJP/` tree (the original use case)
- `targetDir`: `AJP/`
- `charMap`: `{ " ": "_" }`
- `references`: `AJP/README.md` (table of links with `%20`), `AJP/update_ajp_doctrines.py` (folder name generator on line 88)

Result:
- 34 directories renamed: `01 Allied Joint Doctrine (AJP-01)` → `01_Allied_Joint_Doctrine_(AJP-01)`, …, `34 NISP ADatP-34 …` → `34_NISP_ADatP-34_…`.
- `AJP/README.md`: every `%20` in link targets replaced with `_`.
- `AJP/update_ajp_doctrines.py` line 88: appended `.replace(' ', '_')` so future scrapes stay sanitized.

## Anti-patterns
- ❌ Renaming directories without rewriting the scripts that generate names. The next sync will re-create the spaced names alongside the underscored ones — duplicated downloads, dead links.
- ❌ Renaming with `mv -f` or otherwise overwriting an existing target. Two unrelated trees colliding silently is the worst outcome of "sanitization".
- ❌ Recursing into subdirectories without being asked. The scope is *immediate children of `targetDir`*; deeper renames frequently break PDF filenames that callers depend on.
- ❌ Using `sed`/`awk` against the rename loop. `${old// /_}` (Bash parameter expansion) and `str.translate` (Python) are deterministic and quote-safe; `sed` introduces escaping pitfalls in paths.
- ❌ Editing prose in READMEs / commit messages to retroactively pretend the old names never existed. Only link *targets* and code paths must change.

## References
- `AJP/update_ajp_doctrines.py` — concrete reference implementation of the generator-side fix.
- `AJP/README.md` — link-table rewrite reference.
- `skills/nato-ajp-sync/SKILL.md` — the upstream skill this one defends; both share the underscore naming contract.
- POSIX `mv(1)` — semantics of cross-name moves.
- Bash parameter expansion `${var//pattern/replacement}` — the substitution primitive used in step 4.

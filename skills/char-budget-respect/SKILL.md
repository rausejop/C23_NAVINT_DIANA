---
name: char-budget-respect
description: Author multi-section text under per-section character limits (forms, proposals, regulatory filings) with per-block live counts and a deterministic trim protocol that never silently truncates.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    sections: "ordered list of (sectionTitle, charLimit) pairs"
    sources:  "the source documents the answers cite (artefact files, datasheets, etc.)"
  outputSchema:
    file: "Markdown file with one fenced block per section, each ending in `[N / LIMIT chars]`"
  errorHandling:
    overLimit: "iterative trim by the documented protocol; never silent truncation"
    unknownLimit: "ask the user once; record in a header ledger"
  stateless: true
tools: [Read, Edit, Write, Bash]
---

# char-budget-respect

## Purpose
Forms with per-section character limits are common (DIANA, EU Horizon, NATO calls, regulatory filings). The recurring failure mode is to draft freely, paste into the form, get rejected, panic-trim, lose substance. This skill captures the pattern that prevents it: budget-aware drafting, live verification, deterministic trim protocol.

## When to use
- The user is filling a form with explicit per-section char (or word) limits.
- The user wants drafts they can copy-paste without surprises.
- The form has > 4 sections (otherwise just edit in place).

## Inputs
- An ordered list of `(sectionTitle, charLimit)`.
- The source materials the answers must cite (the platform under proposal, the supporting docs, the financials).

## Outputs
- One Markdown file per draft, with this exact shape per section:
  ```markdown
  ## <Section Title> (<limit> chars)

  ```
  <answer body, plain text, no inline markdown>
  ```

  `[<n> / <limit> chars]`
  ```

## Instructions

1. **Header ledger first.** The first non-title block of the file is a one-line ledger of all the limits, so the author can verify them at a glance and the next session does not re-ask.
2. **Fenced blocks for direct copy-paste.** Triple-backtick the body. Avoid markdown-inside-the-fence (no bold, no lists with `-` if the form expects plain text). The form's preview is the source of truth on what survives the paste.
3. **Per-block char count footer.** A single backticked line `[N / LIMIT chars]` immediately after the closing fence.
4. **Verify after every edit** with the verification helper below. Do not trust your eyes for a 1500-char block.
5. **Trim protocol, in this order:**
   - **Pass 1** — drop redundant connectors ("Specifically", "Furthermore", "It is worth noting that", "Importantly").
   - **Pass 2** — compact lists ("60 percent sales and marketing, 30 percent product development" → "60% sales/marketing, 30% product").
   - **Pass 3** — abbreviate where the audience knows the term. Be careful with the audience.
   - **Pass 4** — restructure (paragraph → inline bullet, long enumeration → "and so on" with the most operationally significant items kept).
   - **Pass 5** — sacrifice the least operationally meaningful claim. Tell the user what you sacrificed.
6. **Margin policy:** aim for at least 30 chars under the limit on small fields (≤ 1500), 1 % margin on large fields (≥ 5000). Forms occasionally trim trailing whitespace or count newlines differently; the margin absorbs it.
7. **Never silent truncation.** If a block cannot fit after Pass 5, surface the conflict to the user with the exact extra char count and the candidate sacrifice.
8. **Don't re-flow other sections** when only one is requested. Diff before save.
9. **Update the per-block footer** every time the body changes. Stale counts are worse than no counts.

## Verification helper (Perl one-liner; works without Python)

```bash
perl -e '
use strict; use warnings; local $/;
open(my $fh, "<:utf8", "<FILE>") or die $!;
my $t = <$fh>;
my @s = (
  ["S1", qr/## <heading 1>.*?```\n(.*?)\n```/s, <limit1>],
  ["S2", qr/## <heading 2>.*?```\n(.*?)\n```/s, <limit2>],
  # ...
);
for my $r (@s) { if ($t =~ $r->[1]) { my $n=length($1); my $st=$n<=$r->[2]?"OK":"OVER ".($n-$r->[2]); printf "%-4s %6d / %5d  %s\n",$r->[0],$n,$r->[2],$st; } }
'
```

## Examples

### Header ledger pattern
```markdown
> **Character limits (form-imposed):** Short-Form sections 1500 each · Abstract 750 · Technical Merit 12000 · Suitability 3500 · Defence and Security 3500 · Company and Commercial 3500. Each block below ends with its char count.
```

### Block pattern
```markdown
## Section 5: Company and Commercial (3500 chars)

```
FINANCIAL. <text...>
TEAM, RISKS, DELIVERY. <text...>
MARKETS, PLAN. <text...>
```

`[3469 / 3500 chars]`
```

### A real trim run that worked

Initial draft: 4189 / 3500 (689 over).
Pass 1 (connectors): 3850 / 3500 (350 over).
Pass 2 (lists compacted): 3618 / 3500 (118 over).
Pass 3 (abbreviations: "Ministerio de Defensa" → "MinDef"; "EUR 1,000 per month" → "EUR 1k/mo"): 3543 / 3500 (43 over).
Pass 4 (one paragraph reflowed; redundant clauses removed): 3469 / 3500 (31 under). Stop.

## Anti-patterns

- ❌ Drafting freely then panic-trimming. The structure suffers.
- ❌ Eyeballing length. 1500-char blocks deceive — count.
- ❌ Markdown formatting inside fenced bodies meant for plain-text forms.
- ❌ Counting words instead of chars when the form says chars (and vice versa).
- ❌ Overwriting other sections when only one was requested. Diff before save.
- ❌ Stale count footers. Update on every body change.
- ❌ Silent truncation. If you cannot make the block fit, tell the user what you would sacrifice and let them choose.

## References

- `NewDraft.md` (repo root) — applied to the DIANA portal's New Draft Proposal form.
- Skill `diana-proposal-draft` — concrete instantiation of this skill for the DIANA call.

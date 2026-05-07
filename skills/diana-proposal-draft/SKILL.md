---
name: diana-proposal-draft
description: Generate a copy-paste-ready DIANA "New Draft Proposal" document (NewDraft.md) that maps every form field to a self-verifying char-budgeted answer, citing the live C23 NAVINT artefact and the pitch-deck financial / team / market figures.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    formSpec:    "Specifications/<DATE> New Draft Proposal.txt — verbatim form text from the DIANA portal"
    artefact:    "C23_DIANA_NATO_WARFIGHTERS.html (latest _vNNN) + supporting docs (Datamodel.md, roadmap.md, checklist.md)"
    pitchDeck:   "Pitch Deck_NAVINT v<DATE>.pdf — financial plan, team CVs, market sizing, competition matrix"
    charLimits:  "form-imposed char limits per section (parsed from the form text or supplied by user)"
  outputSchema:
    file: "NewDraft.md at repo root with one fenced block per form field, char count footer per block"
  errorHandling:
    overLimit: "iteratively trim until each block fits its limit; never silently truncate user-facing text"
    placeholder: "if a financial figure is unknown, mark [BRACKETED]; never invent numbers"
  stateless: true
tools: [Read, Edit, Write, Bash]
---

# diana-proposal-draft

## Purpose
DIANA's portal forces analysts to retype 9 sections under tight per-field char limits. The challenge text and the platform artefact are stable; the proposal is not. This skill produces a single Markdown file (`NewDraft.md`) where every section header mirrors the form verbatim, every block is fenced for direct copy-paste, every block ends with `[N / LIMIT chars]`, and the underlying claims are traceable to the live SPA + supporting docs.

## When to use
- The user is preparing a DIANA submission (Decision Superiority for NATO Warfighters or any future challenge).
- The user has a `Specifications/<DATE> New Draft Proposal.txt` from the portal.
- The platform artefact (e.g. `C23_DIANA_NATO_WARFIGHTERS_vNNN.html`) is sealed and verifiable.
- The user has a pitch deck with financial / team / market figures to inject.

## Inputs

1. **The form text.** Verbatim copy from the DIANA portal, saved under `Specifications/`.
2. **Char limits per section.** DIANA's portal does not show them inside the form text; the user must supply them. Typical pattern (verified for the May 2026 challenge):
   - Short-Form Section 1-4: **1500 chars** each.
   - Long-Form Section 1 Abstract: **750 chars**.
   - Long-Form Section 2 Technical Merit: **12 000 chars**.
   - Long-Form Section 3-5 (Suitability / Defence and Security / Company and Commercial): **3500 chars** each.
3. **The platform artefact.** Latest sealed `_vNNN.html` plus `checklist.md`, `roadmap.md`, `Datamodel.md`, `AJP/SUMMARIES/`, `dist/airgap/`.
4. **The pitch deck.** Read with the `pages` parameter (DIANA decks are typically 15-20 pages; see "Reading the pitch deck" below).

## Outputs

`NewDraft.md` at the repo root. The file is organised as:

- A header block citing submitter, form path, artefact version, and a one-line **char-limits ledger** so the user can verify the limits.
- A `## Proposal Title`, `## TRL Level`, `## System Type`, `## System Level` block (free-text, short).
- A `# SHORT-FORM PROPOSAL` group with one `## Section N: <verbatim title> (<limit> chars)` per form field, each containing one fenced code block plus a `[N / LIMIT chars]` footer.
- A `# LONG-FORM PROPOSAL` group with the same shape.
- An `# AGREEMENT CHECKBOXES` informational reminder.
- An `# IMAGES` section suggesting captures from the live SPA respecting DIANA's "no narrative text inside images" rule.
- A `# CHECKLIST BEFORE SUBMISSION` block.

## Instructions

1. **Read the form text** from `Specifications/<DATE> New Draft Proposal.txt`. Identify every named field. Map them 1:1 to `## Section N: <title>` headings; do not paraphrase.
2. **Confirm the char limits.** If the form text contains them, parse. Otherwise ask the user once and store the answer in the header block as a ledger so future runs do not re-ask.
3. **Read the platform artefact's verifying docs first** — `checklist.md` (compliance evidence per spec line), `roadmap.md` § 12 (what is shipped vs deferred), `Datamodel.md` (CycloneDX integration story), `AJP/SUMMARIES/` (doctrine bindings). Do NOT re-derive the spec coverage; cite it.
4. **Read the pitch deck end-to-end** with `Read(pages: "1-20")`. Extract:
   - Founders' names, titles, years of experience, prior employers (Section 5 Team).
   - Advisor board composition (Section 5 Team).
   - Team certifications (ISO, CISSP, ISA, vendor programmes) (Section 5 Team).
   - Reference projects with status (invoiced / forecast quarter) (Section 5 Financial).
   - Three-year financial plan (revenue + EBITDA + margin per year) (Section 5 Financial).
   - Investment round size, equity, pre-money (Section 5 Financial).
   - Use-of-funds breakdown (Section 5 Financial).
   - TAM / SAM / SOM with source citation (Section 5 Markets).
   - Pricing tiers (Section 5 Markets).
   - Sales channels and partnerships (Section 5 Team / Markets).
   - GTM phasing (Section 5 Markets).
   - Customer mix forecast by segment (Section 5 Markets).
5. **Compose every Short-Form block as two paragraphs** keyed to the form's two sub-questions (`DESCRIBE` + `NOVELTY`, `ALIGNMENT` + `AUGMENTATION`, `TRL 7+ JUSTIFICATION` + `INTEGRATIONS`, `DEFENCE USE CASE` + `VALIDATION/TESTING`). The form does not enforce this split but DIANA evaluators expect both halves visible.
6. **Long-Form Sections 3-5 split into three sub-blocks** mirroring the form's three sub-questions.
7. **Long-Form Section 2 Technical Merit (12 000 chars)** is the only field with breathing room. Devote it to: detail (5 functional layers), alignment (constraint / outcome / scenario / 10 exemplar effects), novelty + SOTA comparison (5 axes against named competitors).
8. **Verify char counts** with the helper Perl one-liner (see Examples). Trim iteratively until every block is under its limit with at least 30 chars of margin (10+% on small fields, 1% on the 12 k field).
9. **Tag every claim with a verifiable artefact**: percentage of spec coverage → `checklist.md`; doctrine binding → `AJP/SUMMARIES/AJP-X.md`; CycloneDX detail → `Datamodel.md` § N; air-gap evidence → `dist/airgap/cdax.json`; financial figure → pitch deck slide N.
10. **Honour DIANA's image rule** in the IMAGES block: only labels inside images, no narrative text. Suggest 2 short-form + 3 long-form captures from the live SPA tabs.
11. **Use British English**, NATO-formal register, no contractions, no emojis, no superlatives, no buzzwords. Doctrinal acronyms expanded once at first use.

## Reading the pitch deck

DIANA decks tend to overflow the Read tool's 20-page max. The PDF reader extracts page-by-page images; for text content use the `pages` parameter:

```
Read(file_path: "<repo>/Pitch Deck_NAVINT v<DATE>.pdf", pages: "1-20")
```

If the deck has > 20 pages, batch as `pages: "1-20"` then `pages: "21-N"`.

Identify the slides by the title bar (Spanish or English). Standard slide order observed for CONFIANZA23: portada → problema → solución → propuesta de valor → competencia → roadmap → modelo de negocio → go to market → mercado y plan financiero → equipo → inversión → contacto → gracias → proyectos de referencia → oportunidades → estado actual → roadmap (segundo) → futuro.

## Char-budget verification helper

Run this from the repo root after every edit to NewDraft.md:

```bash
perl -e '
use strict; use warnings; local $/;
open(my $fh, "<:utf8", "NewDraft.md") or die $!;
my $t = <$fh>;
my @s = (
  ["SF1",  qr/## Section 1: Technical Solution.*?```\n(.*?)\n```/s, 1500],
  ["SF2",  qr/## Section 2: Technical Alignment.*?```\n(.*?)\n```/s, 1500],
  ["SF3",  qr/## Section 3: Integration.*?```\n(.*?)\n```/s, 1500],
  ["SF4",  qr/## Section 4: Defence Use Case.*?```\n(.*?)\n```/s, 1500],
  ["LF1",  qr/## Section 1: Abstract.*?```\n(.*?)\n```/s, 750],
  ["LF2",  qr/## Section 2: Technical Merit.*?```\n(.*?)\n```/s, 12000],
  ["LF3",  qr/## Section 3: Technical Suitability.*?```\n(.*?)\n```/s, 3500],
  ["LF4",  qr/## Section 4: Defence and Security.*?```\n(.*?)\n```/s, 3500],
  ["LF5",  qr/## Section 5: Company and Commercial.*?```\n(.*?)\n```/s, 3500],
);
for my $r (@s) { if ($t =~ $r->[1]) { my $n=length($1); my $st=$n<=$r->[2]?"OK":"OVER ".($n-$r->[2]); printf "%-4s %6d / %5d  %s\n",$r->[0],$n,$r->[2],$st; } }
'
```

## Examples

### Section header pattern
```markdown
## Section 5: Company and Commercial (3500 chars)

```
FINANCIAL. CONFIANZA23 INTELIGENCIA Y SEGURIDAD SL — Spanish private limited company in Madrid …
TEAM, RISKS, DELIVERY. Rafael Ausejo Prieto (CEO/Founder, >32 yrs — NATO, ALSTOM, S21Sec/Thales …) …
MARKETS, PLAN. TAM US$ 1,375M (global MDA 2025), CAGR 9.6% to US$ 2,589M by 2032 …
```

`[3469 / 3500 chars]`
```

### Three-paragraph structure for Section 5

The CONFIANZA23 v011 NewDraft maps Section 5 to three labelled paragraphs (`FINANCIAL`, `TEAM, RISKS, DELIVERY`, `MARKETS, PLAN`) — each cleanly aligned to one of the three form sub-questions. This pattern saves the evaluator from having to find which sub-question each sentence answers.

### Trimming protocol when over budget

When a block reports `OVER N`:

1. Pull the body into the editor.
2. First pass — drop redundant connectors ("Specifically,", "Furthermore,", "It is worth noting that").
3. Second pass — compact lists ("60% sales and marketing, 30% product development, 10% operations" → "60% sales/marketing, 30% product, 10% ops").
4. Third pass — expand abbreviations only where the evaluator may not know them; otherwise prefer abbreviation (`MoD` over `Ministry of Defence` if the abbreviation is in the Acronyms tab).
5. Re-run the verification helper.
6. If three passes have not landed under the limit, restructure: convert one paragraph to inline bullets, or split a long enumeration into "and so on" with the most operationally significant items kept.

## Anti-patterns

- ❌ Inventing financial figures. Use `[BRACKETS]` for unknowns; never write a number that is not in the pitch deck or supplied by the user.
- ❌ Paraphrasing form section titles. The portal's automated check may flag a mismatch.
- ❌ Embedding markdown formatting (bold, lists, headings) inside the fenced blocks. The portal renders them as literal asterisks. Plain text only.
- ❌ Long-Form Section 2 stuffed with marketing language to fill the 12 000 chars. Use the budget for technical detail; padding is visible.
- ❌ Forgetting the per-block char count footer. The user needs to verify before pasting.
- ❌ Citing TRL 7 without enumerating the five operational criteria (representative scenario, representative workstation, doctrinal integration, compliance posture, release engineering). DIANA evaluators look for the structured argument.
- ❌ Skipping the Honest Disclosures from `checklist.md` § 8. They are what makes the proposal believable.
- ❌ Overwriting earlier sections silently when the user only asks for one section update. Diff the file; touch only what was requested.

## References

- `NewDraft.md` (repo root) — worked example for the May 2026 DIANA challenge.
- `Specifications/20260503 New Draft Proposal.txt` — the form text.
- `Pitch Deck_NAVINT v20260501v2.pdf` — financial / team / market source.
- `checklist.md` — spec coverage evidence (97 / 98 % range typically).
- `roadmap.md` § 12 — what is shipped, what is deferred behind the foundation-model seam.
- `Datamodel.md` — CycloneDX 1.7 / ECMA-424 integration story.
- `AJP/SUMMARIES/` — doctrine bindings.
- `dist/airgap/cdax.json` — air-gap attestation.
- Skill `char-budget-respect` — the general pattern this skill applies.
- Skill `roadmap-driven-release` — sibling skill for picking what ships next.
- Skill `resumable-execution-state` — pair with this skill if the proposal-writing run is multi-session.
- Skill `playwright-spa-screenshots` — produces the 5 PNG stills (Short-Form 1+2, Long-Form 1+2+3) referenced in the IMAGES block of NewDraft.md.
- Skill `narrated-demo-video` — produces the ≤4-min MP4 demo video referenced in the "Upload a Video" section of the DIANA portal.

## DIANA-evaluator priorities (encoded preferences from prior iterations)

When the user says "prioritise what a DIANA evaluator values most":

- **Doctrinal citation density** matters more than feature count. One AJP citation per workflow beats three workflows with no citation.
- **TRL 7 justification** must be structured (the five-criterion frame), not narrative.
- **Spec scenario beat-by-beat coverage** (every item in `checklist.md § 4`) demonstrates representativeness.
- **Air-gap readiness** is a recurring DIANA concern — evidence-based answers (sandbox-tested URLs, materialised bundle, signed attestation) outweigh procedural promises.
- **Foundation-model deferral** is acceptable if the integration seam is named and stable.
- **Single-file delivery** is a differentiator vs the heavy server-side competition (NCIA, Maven, JCATS, Indra iSIGHT, Saab 9LV, Thales VesselVis, Windward, Spire Maritime).
- **CycloneDX 1.7 / ECMA-424** unified envelope is unique vs the parallel-schema posture of comparators.

---
name: ajp-doctrine-summary
description: Produce a consistent per-AJP Markdown summary suitable for indexing, side-by-side reading and roadmap synthesis.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    ajpId:    e.g. "AJP-3.9"
    title:    e.g. "Allied Joint Doctrine for Joint Targeting"
    edition:  e.g. "Edition B Version 1"
    pdfPath:  optional path to the source PDF for deep-read
  outputSchema:
    file: AJP/SUMMARIES/<ajpId>.md
  errorHandling:
    pdfMissing: "produce summary from public structure; flag ★ deep-dive needed"
  stateless: true
tools: [Read, Write]
---

# ajp-doctrine-summary

## Purpose
Produce one Markdown file per NATO Allied Joint Publication, in a strictly identical structure, so they can be diffed, indexed, fed to a roadmap synthesiser (`doctrine-roadmap-synthesis`), and surfaced inside an Acronyms tab.

## When to use
- A new AJP edition lands in `AJP/<NN>_<Title>/` (underscore-only naming since 2026-05-07).
- Doctrine reading is required for a platform feature decision.
- The user asks for "doctrine summary", "AJP summary", "what does AJP-X say".

## Inputs
- The publication's title and edition (visible in the directory name).
- The source PDF, *if* a deep-read is performed (otherwise rely on public structure).

## Outputs
- One `AJP/SUMMARIES/<AJP-ID>.md` file matching the template below.
- An updated row in `AJP/SUMMARIES/README.md` index.

## Instructions

1. **Use the canonical filename pattern** `AJP/SUMMARIES/<AJP-ID>.md` (e.g. `AJP-3.9.md`).
2. **Follow this template verbatim** (do not invent new sections — diffability is the point):
   ````markdown
   # <AJP-ID> — <full title>

   **Identity:** <AJP-ID> <Edition X Version Y> · <publisher>.

   ## Purpose
   One paragraph.

   ## Key takeaways
   - 4–6 bullets, each one a doctrinal concept relevant to a multi-domain C2 / wargaming platform.

   ## Constraints / framing
   - 1–3 bullets stating what the platform **must** respect.

   ## Acronyms / terms introduced
   Comma-separated, suitable to be merged into the in-platform Acronyms list.

   ## Platform improvements
   - 1–4 bullets, **specific and actionable** items to add to the platform.
     Mark each as ✅ (already shipped), 🚧 (scheduled), or ★ (deep-dive needed).
   ````
3. **Be honest about depth.** If the PDF was not read in full, say so in `AJP/SUMMARIES/README.md` (the methodology disclosure already in the repo) and mark uncertain items with ★.
4. **Stay in the relevance funnel.** Doctrines have hundreds of concepts; only pull out those that map to features the platform could ship. Don't write encyclopaedia entries.
5. **Use NATO terminology verbatim** — `RSOM`, `JPTL`, `FIVE-O`, `JFACC`, etc. Do not paraphrase or modernise.
6. **Acronyms section is the bridge** to the in-platform Acronyms tab — keep it succinct and unambiguous.
7. **Update `AJP/SUMMARIES/README.md`** with a row pointing at the new file.
8. **Append improvements to `roadmap.md`** under the relevant theme (Capstone / Conduct / Maritime / Targeting / Movement / etc.).

## Examples

### Real summary in this repo (AJP-3.9, the most consequential)
- Identity: AJP-3.9 Edition B Version 1 · NATO Standardization Office (2021).
- Key takeaways: 6-phase JTC, JPTL, FIVE-O / F2T2EA, RTL/NSL, CDE, dynamic vs deliberate.
- Platform improvements: full Joint Targeting module, JPTL CRUD, HVT/HPT/TST flags, CDE stub, RTL/NSL ingestion, BDA/MEA closure of CoA loop.
- See `AJP/SUMMARIES/AJP-3.9.md`.

## Anti-patterns
- ❌ Inventing concepts that aren't in the doctrine. Worse than no summary.
- ❌ Tracking "interesting passages" instead of platform-actionable insight.
- ❌ Adding new top-level sections per file. Diffability dies the moment the structure varies.

## References
- `AJP/SUMMARIES/README.md` — index + methodology disclosure.
- `AJP/SUMMARIES/AJP-*.md` — 33 worked examples.
- `roadmap.md` — downstream consumer.
- Skill `doctrine-roadmap-synthesis` — picks the improvements out and prioritises them.

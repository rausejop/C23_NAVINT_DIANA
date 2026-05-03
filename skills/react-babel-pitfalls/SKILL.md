---
name: react-babel-pitfalls
description: Diagnose and fix the recurring traps of React + Babel-standalone single-file SPAs (black screen, redeclaration errors, JSX comments, unsupported syntax).
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    htmlFile: path to a single-file SPA suspected of failing
    symptom: "blackScreen | consoleError | partialRender"
  outputSchema:
    diagnosis: short root-cause description
    patch: minimal Edit that fixes it
  errorHandling:
    cdnFailure: "out of scope; refer to air-gap-mirror"
  stateless: true
tools: [Grep, Read, Edit]
---

# react-babel-pitfalls

## Purpose
Cover every failure mode that has bitten this project (or is highly likely to) when running React via `@babel/standalone` inside a single HTML file.

## When to use
- The user reports "black screen", "blank page", "nothing renders".
- A recently-edited single-file SPA loads but the `<div id="root">` stays empty.
- The browser console shows `SyntaxError`, `Identifier 'X' has already been declared`, `Unexpected token`, or `babel.min.js` errors.

## Inputs
- The path to the offending HTML file.
- (optional) The browser console error text.

## Outputs
- A short diagnosis (one of the cases below) and a minimal Edit to fix it.

## Instructions

1. `grep -n 'type="text/babel"'` the file.
   - **More than one Babel block?** Likely Case A. Merge into one.
2. `grep -n 'const { useState'` the file.
   - **Appears more than once?** Confirms Case A (`const` redeclaration in shared global scope).
3. `grep -n 'ReactDOM.createRoot\|ReactDOM.render'` the file.
   - **Zero hits?** App is never mounted (Case B).
   - **More than one hit?** Two roots fighting for `#root` (Case C).
4. Open the file in a browser and check the console. Match the error to one of the cases below.

### Case A — Multiple Babel blocks share global scope
**Symptom:** black screen; console says `SyntaxError: Identifier 'useState' has already been declared` or similar.

**Why:** every `<script type="text/babel">` is compiled and evaluated in the page's global scope. `const { useState } = React;` in two blocks is a redeclaration.

**Fix:** merge all Babel blocks into a single `<script type="text/babel" data-presets="react">…</script>`. Move helpers, components, and the `ReactDOM.createRoot` call into one block.

### Case B — App never mounts
**Symptom:** `<div id="root"></div>` stays empty; no console error.

**Why:** missing `ReactDOM.createRoot(document.getElementById("root")).render(<App/>);` at the end of the Babel block.

**Fix:** append the render line as the **last statement** of the single Babel block.

### Case C — Multiple roots
**Symptom:** UI flashes, then disappears, or only one panel renders.

**Why:** two `createRoot` calls on the same DOM node race each other.

**Fix:** keep exactly one `createRoot` call.

### Case D — `// comments inside JSX`
**Symptom:** Babel error `Unexpected token`. The line in the error is inside JSX braces.

**Why:** JSX requires `{/* comment */}`, not `// comment` and not `/* comment */`.

**Fix:** wrap inline JSX comments in `{ /* … */ }`.

### Case E — Unsupported modern syntax
**Symptom:** `babel.min.js: Unexpected token` on otherwise-valid TS/JSX.

**Why:** `@babel/standalone` only loads the presets you ask for. `data-presets="react"` does **not** include `typescript`, `stage-X` proposals, decorators, or `import.meta`.

**Fix:** either drop the modern syntax or add the preset: `data-presets="react,typescript"`. Add `data-plugins=` for individual plugins.

### Case F — `script` blocks load out of order
**Symptom:** `React is not defined`, `L is not defined`, `ms is not defined`.

**Why:** Babel transforms but does not async-await its dependencies. If your Babel block runs before React/Leaflet/milsymbol scripts have parsed, you get this.

**Fix:** in `<head>`, list the dependency `<script>` tags **before** the Babel block in the `<body>`. Do not use `defer` on the dependency tags (Babel-standalone is synchronous).

### Case G — CDN integrity hash mismatch
**Symptom:** browser blocks the script, console says `Failed to find a valid digest in the 'integrity' attribute`.

**Why:** an `integrity="sha384-…"` attribute on a CDN script is too strict if the file was re-uploaded or the version bumped.

**Fix:** remove the `integrity=` attribute (or pin a known-good hash). Keep `crossorigin="anonymous"` if you need CORS.

## Examples

### A real case from this repo (Case A)
The first build of `C23_DIANA_NATO_WARFIGHTERS.html` had two Babel blocks:
```html
<script type="text/babel" data-presets="react">
  const { useState } = React;
  /* helpers */
  window.__C23_HELPERS = { … };
</script>
<script type="text/babel" data-presets="react">
  const { useState } = React;        ← BOOM: redeclaration
  /* App */
</script>
```
Fix: deleted the second `script`-tag boundary and the duplicate destructuring; kept one block from helpers through `ReactDOM.createRoot`.

## Anti-patterns
- ❌ Adding `try/catch` around `createRoot` to "fix" a black screen — that hides the real cause.
- ❌ Reaching for a bundler the moment Babel-standalone fails — solve the actual case first.
- ❌ Sprinkling `console.log` instead of opening DevTools and reading the actual error.

## References
- `C23_DIANA_NATO_WARFIGHTERS.html` (post-fix) — single Babel block.
- Babel standalone docs: <https://babeljs.io/docs/babel-standalone>
- Skill `build-single-file-spa` — prevention rules.

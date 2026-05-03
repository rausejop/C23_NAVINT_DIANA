---
name: build-single-file-spa
description: Build a self-contained HTML SPA with React + Babel-standalone, no bundler, ready for air-gap distribution.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    targetFile: path to the single HTML file to produce
    appComponent: the root React component (JSX)
    initialData: optional JSON to embed under window.* before the React script
  outputSchema:
    file: one .html file, ~100–200 KB, no external build artefacts
  errorHandling:
    blackScreen: "see skill react-babel-pitfalls"
    cdnBlocked: "see skill air-gap-mirror"
  stateless: true
tools: [Read, Write, Edit]
---

# build-single-file-spa

## Purpose
Produce a fully working SPA in a **single HTML file** with no build step, no bundler, no package manager. The file must be openable by double-click and runnable on a 16 GB-RAM tactical laptop in air-gapped conditions.

## When to use
- The deliverable is a single artefact (DIANA / proposal demos / wargame ROMs).
- The target environment forbids `npm install` or running a dev server.
- The user explicitly says "single HTML file" or "no build step".

## Inputs
- `targetFile`: e.g. `C23_DIANA_NATO_WARFIGHTERS.html`.
- `appComponent`: the React root component as JSX.
- `initialData` (optional): JS object literal to expose as `window.DEFAULT_<NAME>` so it can be edited / replaced without touching code.

## Outputs
- One `.html` file with this exact macro-structure:
  ```
  <head>
    <link rel="stylesheet" href="…leaflet.css">
    <script src="…leaflet.js"></script>
    <script src="…milsymbol.js"></script>
    <script src="…react@18.umd"></script>
    <script src="…react-dom@18.umd"></script>
    <script src="…@babel/standalone"></script>
    <style> … </style>
  </head>
  <body>
    <div id="root"></div>
    <script>window.DEFAULT_DATA = { … };</script>     ← vanilla
    <script type="text/babel" data-presets="react">    ← ONE block, see anti-patterns
      /* helpers, components, ReactDOM.createRoot(...) */
    </script>
  </body>
  ```

## Instructions
1. **Pin every CDN script** to a specific minor version (e.g. `react@18.3.1`, `@babel/standalone@7.29.0`). Floating versions break air-gap mirrors.
2. **Embed initial data in a vanilla `<script>` block** *before* the Babel block. Attach to `window.*` so the React code can read it without import gymnastics.
3. **Use exactly one `<script type="text/babel">` block** for all helpers + components + render. Multiple Babel blocks share global scope and will redeclare identifiers. (See `react-babel-pitfalls`.)
4. **Render with React 18 createRoot:** `ReactDOM.createRoot(document.getElementById("root")).render(<App/>);`
5. **Inline all CSS** in a single `<style>` block in the head. No separate `.css` files.
6. **Keep dependencies on the index finger of one hand.** Leaflet, milsymbol, React, ReactDOM, Babel-standalone is the upper bound. Anything else must be justified.
7. **Test by double-clicking the file** in a browser before reporting done. A passing build that renders nothing is a fail.

## Examples

Minimal working skeleton (~30 lines):
```html
<!DOCTYPE html><html><head>
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"></script>
</head><body><div id="root"></div>
<script>window.DEFAULT_DATA = { greeting: "Hello DIANA" };</script>
<script type="text/babel" data-presets="react">
const { useState } = React;
function App() { return <h1>{window.DEFAULT_DATA.greeting}</h1>; }
ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
</script></body></html>
```

## Anti-patterns
- ❌ Splitting helpers and components into two `<script type="text/babel">` blocks.
- ❌ Loading React from `latest` instead of a pinned version.
- ❌ Using `<script type="module">` with bare specifiers — won't resolve without an importmap.
- ❌ Adding a "build:dev" npm script that hides the fact that the file isn't actually self-contained.

## References
- `C23_DIANA_NATO_WARFIGHTERS.html` — canonical single-file SPA in this repo.
- `Format/EasternFlankv003.html` — original template the SPA was derived from.
- React 18 docs: <https://react.dev/reference/react-dom/client/createRoot>

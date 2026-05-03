---
name: react-hotkeys
description: Add keyboard shortcuts to a React SPA with input-guarding, modifier handling, and a single shared keydown listener.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    bindings: 'object: { "Key": handler, "Ctrl Z": handler, ... }'
  outputSchema:
    effect: "single useEffect attaching/removing window.keydown"
    cheatsheet: "render in INFO/WORKSPACE so users discover the shortcuts"
  errorHandling:
    inputFocus: "ignore keystrokes while INPUT/TEXTAREA/SELECT/contentEditable are focused"
  stateless: true
tools: [Read, Edit]
---

# react-hotkeys

## Purpose
Sessions in a tactical-C2 SPA are long. Reducing mouse travel to the topbar buttons (TURN, AUTO, RESET, INFO, CONFIG) and to the phase ladder is the single highest-ROI ergonomic change you can make. This skill is the recipe.

## When to use
- The user asks for "shortcuts", "hotkeys", "keyboard navigation".
- The platform has more than ~5 frequently-used actions.
- A demo audience benefits from a CMDR who never touches the trackpad.

## Inputs
- A bindings table: action name → key combo → handler.

## Outputs
- A single `useEffect` keyed on the dependencies that the handlers close over.
- A cheatsheet rendered somewhere visible (INFO modal or a WORKSPACE tab section).

## Instructions

1. **One global listener.** `window.addEventListener("keydown", onKey)` inside `useEffect`. Never per-component.
2. **Always input-guard:**
   ```js
   const tag = (e.target && e.target.tagName) || "";
   if (["INPUT","TEXTAREA","SELECT"].includes(tag) || e.target?.isContentEditable) return;
   ```
   Otherwise the user can't type the letter `t` into a text field without flipping the turn.
3. **Modifier branch first.** Handle `Ctrl/Cmd` + key (undo / redo) before the bare-key branch so `Ctrl+Z` doesn't trigger `Z`.
4. **Avoid colliding with browser defaults**: `Ctrl+S`, `Ctrl+R`, `Ctrl+T`, `Ctrl+W`, `F5` are off-limits. Use `Esc`, letter keys, digits, `+/-`.
5. **Re-bind on dependency change.** The effect's dep array must include every captured value. Otherwise the handler closes over stale state.
6. **Document the shortcuts in the UI.** A keyboard list in INFO or a WORKSPACE section. Users won't discover the binding by guessing.
7. **Reserve a "show all shortcuts" key** (`?` is the convention).

## Examples

### The C23 binding set (paste-ready)
```js
useEffect(() => {
  const onKey = (e) => {
    const tag = (e.target && e.target.tagName) || "";
    if (["INPUT","TEXTAREA","SELECT"].includes(tag) || e.target?.isContentEditable) return;
    if (e.metaKey || e.ctrlKey || e.altKey) {
      const k = e.key.toLowerCase();
      if (k === "z" && !e.shiftKey) { e.preventDefault(); undo(); return; }
      if ((k === "z" && e.shiftKey) || k === "y") { e.preventDefault(); redo(); return; }
      return;
    }
    const k = e.key;
    if (k === "?" || k === "/") { e.preventDefault(); setShowInfo(s=>!s); return; }
    if (k === "i" || k === "I") { setShowInfo(true); return; }
    if (k === "c" || k === "C") { setShowConfig(true); return; }
    if (k === "t" || k === "T") { setActiveFaction(f=>f==="NATO"?"OPFOR":"NATO"); return; }
    if (k === "a" || k === "A") { setTweak("autoMode", !tweaks.autoMode); return; }
    if (k === "r" || k === "R") { resetOp(); return; }
    if (k === "Escape")         { setShowConfig(false); setShowInfo(false); return; }
    if (/^[1-9]$/.test(k)) {
      const target = parseInt(k,10) - 1;
      if (target >= 0 && target <= activePhase + 1) triggerPhase(target);
      return;
    }
    if (k === "+" || k === "=") { expandAllRail();   return; }
    if (k === "-" || k === "_") { collapseAllRail(); return; }
  };
  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
}, [tweaks.autoMode, activePhase, undo, redo]);
```

### Cheatsheet (paste into INFO or WORKSPACE)
```
I / ? · INFO     ·  C · CONFIG  ·  Esc · close any modal
T · TURN (flip Allied/Hostile)  ·  A · AUTO  ·  R · RESET OP
1..9 · execute that phase if eligible
+ / - · expand / collapse all rail sections
Ctrl/Cmd Z · undo  ·  Ctrl/Cmd Shift Z (or Ctrl Y) · redo
```

## Anti-patterns
- ❌ Listening on a component's root div. Half the keystrokes happen with focus elsewhere.
- ❌ Forgetting input-guard. Your text inputs become unusable.
- ❌ Stale closure: handler reads `tweaks.autoMode` but the effect dep array doesn't list it. Toggle stops working after the first call.
- ❌ Using `Ctrl + letter` for app actions when a bare letter would do. The bare letter is faster and doesn't conflict with browser shortcuts.
- ❌ No discoverability. Hotkeys without a cheatsheet are tribal knowledge.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v006.html` — the live binding set.
- Skill `spa-persistence` — undo/redo sourced from there.

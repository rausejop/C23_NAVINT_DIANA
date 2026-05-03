---
name: spa-persistence
description: Persist editor state to localStorage with hydration on first paint, named-slot snapshots, undo/redo stack and a clear-all escape hatch.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    keys: 'list of localStorage keys to manage (e.g. ["c23.mission","c23.units"])'
  outputSchema:
    state: "useState seeded from storage (with safe fallback)"
    persistEffect: "useEffect that mirrors state to storage on every change"
    slots: "named-slot CRUD over a single 'c23.slots' array"
    undoRedo: "in-memory stack with hotkey bindings"
  errorHandling:
    parseError: "swallow the JSON.parse error; fall back to default state"
    quotaExceeded: "logger only; user can use 'CLEAR ALL STORAGE' button"
  stateless: false  # the localStorage values are the state
tools: [Read, Edit]
---

# spa-persistence

## Purpose
A single-file SPA loses everything on F5 unless you opt in to persistence. localStorage is enough for mission JSON-sized state and is air-gap-friendly (no server). This skill captures the four pieces that together make a usable persistence story: hydration, write-through, named slots, and undo.

## When to use
- The user edits anything that is not trivially re-derivable on reload.
- The user asks for "save", "remember", "persist", "don't lose my edits", "snapshots".
- The platform supports A/B comparison of multiple mission states.

## Inputs
- The keys to manage (`c23.mission`, `c23.units`, `c23.slots`, `c23.lang` in this project).

## Outputs
- `useState` initialiser that hydrates from `localStorage` with a safe fallback.
- `useEffect` per managed key that writes the JSON-stringified value back on every change.
- A `WORKSPACE` (or equivalent) tab that exposes:
  - Storage usage in bytes.
  - "Save current to slot" / load / delete.
  - "Clear all storage" with a confirmation.
- An in-memory undo/redo stack bound to `Ctrl/Cmd Z` and `Ctrl/Cmd Shift Z` / `Ctrl Y`.

## Instructions

1. **Hydrate on first paint** with a `useState` initialiser, NOT a `useEffect`. The default-mission flash is what you avoid:
   ```js
   const [mission, setMission] = useState(()=>{
     try { const raw = window.localStorage?.getItem("c23.mission");
           if (raw) return JSON.parse(raw); } catch {}
     return deepClone(window.DEFAULT_MISSION);
   });
   ```
2. **Wrap every storage call in `try/catch`.** Private/incognito browsers throw; out-of-quota throws; old Safari throws.
3. **Mirror state with one `useEffect` per key**, not one giant blob. Lets the next agent grep `c23.mission` to find the exact path.
4. **Slots in their own key (`c23.slots`).** Cap at 5 (UI realism, not a hard rule). Each entry: `{ id, name, savedAt, mission }` so the user can decide which slot to load.
5. **Undo/Redo as refs, not state.** `useRef([])` for `undoStack` and `redoStack`. Pushing onto the stack should NOT re-render. Popping does, because it calls `setMission` / `setUnits`.
6. **Cap the undo stack** (30 entries is plenty); shift the oldest when over.
7. **Clearing the redo stack on a new edit** is the standard editor convention. Don't be clever.
8. **Escape hatch.** Always provide a "CLEAR ALL STORAGE" button. Storage corruption is a real failure mode and the user must be able to recover without DevTools.
9. **Surface bytes used** in the UI. Helps the user understand why the slot list is short.

## Examples

### Hydration + write-through (paste-ready)
```js
const [mission, setMission] = useState(()=>{
  try { const raw = window.localStorage?.getItem("c23.mission");
        if (raw) return JSON.parse(raw); } catch {}
  return deepClone(window.DEFAULT_MISSION);
});
useEffect(()=>{ try { window.localStorage?.setItem("c23.mission", JSON.stringify(mission)); } catch {} }, [mission]);
```

### Undo / Redo as refs
```js
const undoStack = useRef([]);
const redoStack = useRef([]);
const undo = useCallback(() => {
  if (!undoStack.current.length) return;
  redoStack.current.push({ mission: deepClone(mission), units: deepClone(units) });
  const prev = undoStack.current.pop();
  setMission(prev.mission); setUnits(prev.units);
}, [mission, units]);
```

### Slot CRUD over `c23.slots`
```js
const persistSlots = (next) => {
  setSlots(next);
  try { window.localStorage?.setItem("c23.slots", JSON.stringify(next)); } catch {}
};
const saveSlot = () => {
  const name = window.prompt("Slot name:");
  if (!name) return;
  const entry = { id:newId("slot"), name, savedAt:new Date().toISOString(),
    mission: JSON.parse(JSON.stringify(mission)) };
  persistSlots([entry, ...slots].slice(0, 5));
};
```

## Anti-patterns
- ❌ Hydrating in a `useEffect`. Causes a one-frame flash of default state.
- ❌ A single `c23.everything` key holding all state. Hard to clear selectively, hard to migrate.
- ❌ Undo as state. Pushing rerenders, defeats the cap.
- ❌ Persisting transient UI state (modal-open flags, current tab) — bloats storage and surprises the user on reload.
- ❌ No "CLEAR" button. Storage corruption becomes "open DevTools to fix" — terrible for tactical-laptop users.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v006.html` — hydration, write-through, undo/redo, `WorkspaceTab` slots.
- Skill `react-hotkeys` — Ctrl/Cmd Z bindings live there.
- Skill `mission-editor` — the host of the editing surface this persists.

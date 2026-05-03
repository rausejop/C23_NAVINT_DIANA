---
name: css-affordances
description: Five small, high-impact CSS-only patterns — themes via [data-theme], CSS-only tooltips via [data-tip]:hover:after, persistent state indicators via [data-…] attrs, slide-down keyframe animations, and logo halo treatments.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    none: "the patterns are CSS recipes; usage is declarative"
  outputSchema:
    rules: "additions to the existing single <style> block"
  errorHandling:
    legacyBrowser: "all five degrade gracefully (themes default to dark; tooltips don't show; animations don't play)"
  stateless: true
tools: [Edit]
---

# css-affordances

## Purpose
Bundle the small CSS techniques that produced large UX wins in v007 + v006. Each is one rule set; together they shift the platform from "functional" to "actually pleasant".

## When to use
- The user asks for "themes", "tooltips", "animations", "polish".
- A demo has audience members in different lighting environments (SCIF dark, conference-room bright).
- The platform's tooltips today are native browser `title=` (ugly) and discoverability suffers.

## Inputs
- (none — these are CSS additions and a small JSX convention)

## Outputs
- Five additions to the existing `<style>` block.
- A discipline of using `data-…` attributes on HTML elements rather than inline styles.

## Instructions

### A — Themes via `[data-theme]`

1. **Drive themes from `<html>`**: a `useEffect` writes `document.documentElement.dataset.theme = tweaks.theme;`.
2. **Override colour vars per theme**, never per component:
   ```css
   html[data-theme="light"]{ --bg-0:#f4f6fb; --ink:#0c1426; … }
   html[data-theme="high-contrast"]{ --bg-0:#000; --ink:#fff; --nato-gold:#ffea00; … }
   ```
3. **Keep "always dark" elements explicit.** The Command Log stays dark even in light theme — log readability beats theming consistency.

### B — CSS-only tooltips via `[data-tip]:hover:after`

1. Add `data-tip="multi\nline\nallowed"` to any element.
2. One CSS rule serves them all:
   ```css
   [data-tip]{position:relative;}
   [data-tip]:hover:after{
     content:attr(data-tip);
     position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);
     background:#0a1426;color:var(--ink);font-size:11px;padding:6px 10px;
     border:1px solid var(--nato-gold);border-radius:3px;
     white-space:pre-wrap;max-width:280px;text-align:left;z-index:9100;pointer-events:none;
   }
   ```
3. **Use `\n` in the attribute** to force line breaks (`white-space:pre-wrap` honours them).
4. **Don't put HTML in `data-tip`**. Plain text only — escapes are painful.

### C — Persistent state indicators via `[data-…]` attrs

The trick: write the state to `<html>` once, then style any descendant via attribute selectors.

```js
useEffect(() => {
  document.documentElement.dataset.faction = activeFaction;
}, [activeFaction]);
```

```css
.rail:before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--allied);transition:background .25s;}
html[data-faction="OPFOR"]   .rail:before{background:var(--hostile);}
html[data-faction="NEUTRAL"] .rail:before{background:var(--neutral);}
```

The state is visible globally without prop drilling.

### D — Slide-down keyframe animations

```css
@keyframes c23-slide-down{from{opacity:0;transform:translateY(-6px);} to{opacity:1;transform:none;}}
.rail-sec:not(.is-collapsed) > :not(.sec-head):not(.sec-head-toggle){
  animation: c23-slide-down 180ms ease-out;
}
```

Important: **only animate the open direction.** Animating closed too looks janky; the conditional render handles "closed" by removing the children.

### E — Logo halo treatment (NATO emblem on coloured chrome)

```css
.brand-logo-nato{
  background:transparent !important;
  border:none !important;
  padding:2px 4px !important;
  filter: drop-shadow(0 0 6px rgba(255,255,255,0.55))
          drop-shadow(0 0 14px rgba(0,73,144,0.55));
}
```

Two-layer drop-shadow: a tight white halo for legibility, a soft NATO-blue glow for context. The PNG can be a transparent original and reads cleanly without an opaque card behind it.

## Anti-patterns
- ❌ JS-driven tooltips (a `<Tooltip>` component) when one CSS rule covers 95% of cases. Save the JS for tooltips that need rich HTML or async data.
- ❌ Theming by toggling a class on every component. `[data-theme]` on `<html>` is one source of truth.
- ❌ Animating closed AND open. Only open.
- ❌ White-card halos on every logo. The CONFIANZA23 logo needs a card (dark mark on coloured chrome); the NATO logo doesn't (the original PNG is white-on-blue with its own halo).
- ❌ Forgetting `pointer-events:none` on tooltip pseudo-elements. The tooltip starts intercepting hover and you get flicker.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v007.html` — themes, tooltips, faction indicator, slide animation, NATO halo.
- `C23_DIANA_NATO_WARFIGHTERS_v006.html` — `@media print` is a sibling pattern (skill `spa-persistence` covers it under "print one-pager").
- Skill `nato-classification` — the colour palette this skill consumes.

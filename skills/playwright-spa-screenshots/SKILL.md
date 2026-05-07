---
name: playwright-spa-screenshots
description: Capture publication-quality PNG screenshots from a single-file HTML SPA via headless Chromium (Playwright Python), driving CONFIG → tab navigation and using `.modal` locator captures so backdrops and surrounding chrome do not bleed into the frame.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    spa: "absolute path to the .html file under capture (file:// URI)"
    viewport: "{width:1920,height:1080} default; device_scale_factor 2 for retina-grade exports"
    targets: "ordered list of (sceneName, navigation function, locator selector or full-page)"
  outputSchema:
    files: "dist/screenshots/<sceneName>.png — one per target, lossless"
  errorHandling:
    leafletNotReady: "wait_for_selector('.leaflet-tile') before first screenshot; tiles render async"
    modalBackdrop: "use page.locator('.modal').screenshot() rather than page.screenshot() so the dim backdrop does not appear"
    fontFallback: "device_scale_factor=2 + an explicit font-family stack avoids serif fallback on the bundled chromium"
  stateless: true
tools: [Read, Write, Bash]
---

# playwright-spa-screenshots

## Purpose
Forms like DIANA's "New Draft Proposal" require still images that show specific platform features (a tab, a modal, a matrix). Driving the SPA by hand and pressing Print Screen produces inconsistent crops and includes desktop chrome. This skill packages the deterministic capture pattern that produced the 5 PNGs delivered to DIANA: open the SPA, drive `CONFIG → <tab>` programmatically, capture the modal alone via locator, escape, repeat.

## When to use
- The user is preparing a submission that requires N stills from a SPA they control.
- The SPA has a stable selector to reach each feature (CONFIG tab, modal, top-bar tile).
- The submission imposes "no narrative text inside images" — only the SPA's own labels are allowed.

## Inputs
1. **The SPA path.** A `.html` file that loads to completion in headless Chromium without network (or with the basemap CDN reachable).
2. **The target list.** Per scene: navigation steps + the selector to capture (`page.locator('.modal')` is the workhorse).
3. **The output directory.** Conventionally `dist/screenshots/`.

## Outputs
- One PNG per target, named `short_N_<scene>.png` or `long_N_<scene>.png` to match the form's slot.
- A console summary listing each file's size in KB.

## Instructions

1. **Install Playwright once** in the project venv:
   ```bash
   pip install --quiet playwright && python -m playwright install chromium
   ```
2. **Use `device_scale_factor: 2`** in `new_context()`. This doubles the bitmap resolution at the same logical viewport — DIANA's portal scales the displayed image down, so the 2× buffer keeps text crisp.
3. **Wait for the SPA to settle** before the first screenshot:
   ```python
   page.wait_for_selector(".app .topbar", timeout=15000)
   page.wait_for_selector(".leaflet-tile", timeout=15000)
   page.wait_for_timeout(2500)   # let symbols + tiles paint
   ```
4. **For the global COP** (no modal), use `page.screenshot(full_page=False)`.
5. **For every modal capture, use `.locator('.modal').screenshot()`**, NOT `page.screenshot()`. The modal-bg backdrop dims the rest of the screen at ~50 % alpha; capturing the page produces a washed-out frame. Capturing the locator captures only the modal's bounding box.
6. **Open a CONFIG tab** with the helper:
   ```python
   def open_config_tab(page, tab_label):
       page.click("button.btn-ghost:has-text('CONFIG')")
       page.wait_for_selector(".cfg-tabs", timeout=5000)
       page.click(f".cfg-tab:has-text('{tab_label}')")
       page.wait_for_timeout(600)
   ```
7. **Scroll the modal body** when the target content is below the fold:
   ```python
   page.evaluate("const b=document.querySelector('.modal-body'); if(b) b.scrollTop=b.scrollHeight*0.30;")
   page.wait_for_timeout(300)
   ```
8. **Close modals between captures** with two `Escape` presses (modal stack tolerates an extra press).
9. **Verify file sizes.** A blank capture is < 50 KB; a real modal capture is 200 KB – 2 MB at 1920×1080 ×2 device-scale.

## Reference implementation

`tools/capture_diana_screenshots.py` — produced the 5 DIANA PNGs (`short_1_global_cop.png`, `short_2_wargaming.png`, `long_1_joint_targeting.png`, `long_2_analytics_cascades.png`, `long_3_jprc.png`). Pattern is reusable across any C23 SPA.

## Examples

### Modal-only capture
```python
open_config_tab(page, "WARGAMING")
page.wait_for_timeout(500)
page.locator(".modal").screenshot(path=str(OUT / "short_2_wargaming.png"))
close_modal(page)
```

### Scrolled modal capture (Analytics cascade rules visible)
```python
open_config_tab(page, "ANALYTICS")
page.evaluate("const b=document.querySelector('.modal-body'); if(b) b.scrollTop=b.scrollHeight*0.30;")
page.wait_for_timeout(300)
page.locator(".modal").screenshot(path=str(OUT / "long_2_analytics_cascades.png"))
```

## Anti-patterns

- ❌ `page.screenshot()` for a modal-only target. The dim backdrop washes the rest of the SPA and wastes pixels.
- ❌ `device_scale_factor: 1`. Submission portals downscale and the text turns mushy. Use 2.
- ❌ Skipping `wait_for_selector('.leaflet-tile')`. Tiles arrive async; the first frame is grey.
- ❌ Capturing immediately after `click()`. Modal CSS transitions take ~300–600 ms; the capture catches the half-open state.
- ❌ Hard-coding tab labels in non-en strings when the SPA's UI labels are English. The locator `:has-text('WARGAMING')` is exact-match by default.
- ❌ Burning narrative annotations into the PNG (arrows, callouts, captions). DIANA explicitly forbids it; only the SPA's own labels are allowed.
- ❌ Re-running the script and overwriting an already-validated PNG without checking the file timestamp first. Keep the validated set under version control or copy them aside before re-runs.

## References
- `tools/capture_diana_screenshots.py` — concrete implementation.
- <https://playwright.dev/python/docs/screenshots> — Playwright screenshot API (locator vs page).
- DIANA "Decision Superiority for NATO Warfighters" call (2026-05) — image-rule source.
- Skill `narrated-demo-video` — companion skill for the moving-picture deliverable.
- Skill `diana-proposal-draft` — references the outputs of this skill in the IMAGES block.

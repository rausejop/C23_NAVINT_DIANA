#!/usr/bin/env python3
"""
capture_diana_screenshots.py

Drives Chromium via Playwright to open C23_DIANA_NATO_WARFIGHTERS_v011.html and
capture the five screenshots required by the DIANA New Draft Proposal form:

  Short-Form Image 1 — Global multi-domain COP with all overlays on
  Short-Form Image 2 — Wargaming pairwise matchup matrix (CONFIG → WARGAMING)
  Long-Form Image 1  — Joint Targeting tab open (CONFIG → JOINT TARGETING)
  Long-Form Image 2  — Analytics tab with Cascade Rules editor (CONFIG → ANALYTICS)
  Long-Form Image 3  — Personnel Recovery / JPRC tab (CONFIG → PR / JPRC)

DIANA forbids narrative text inside the images; the SPA's own UI labels (tab
titles, column headers, etc.) are allowed.

Usage:
    python tools/capture_diana_screenshots.py
Outputs: dist/screenshots/{short_1,short_2,long_1,long_2,long_3}.png
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
SPA = REPO / "C23_DIANA_NATO_WARFIGHTERS_v011.html"
OUT = REPO / "dist" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

VIEWPORT = {"width": 1920, "height": 1080}

def open_config_tab(page, tab_label: str):
    """Click CONFIG, then click the cfg-tab whose visible text matches tab_label."""
    page.click("button.btn-ghost:has-text('CONFIG')")
    page.wait_for_selector(".cfg-tabs", timeout=5000)
    # Click the tab by exact label
    page.click(f".cfg-tab:has-text('{tab_label}')")
    page.wait_for_timeout(600)

def close_modal(page):
    """Press Escape twice to close any modal stack."""
    page.keyboard.press("Escape")
    page.wait_for_timeout(150)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport=VIEWPORT, device_scale_factor=2)
        page = ctx.new_page()

        url = SPA.as_uri()
        print(f"[*] Opening {url}")
        page.goto(url)
        # wait for React to mount and Leaflet to load tiles
        page.wait_for_selector(".app .topbar", timeout=15000)
        page.wait_for_selector(".leaflet-tile", timeout=15000)
        page.wait_for_timeout(2500)  # let tiles + symbols settle

        # ── Short-Form Image 1: Global COP, all overlays default-on ─────────
        print("[1/5] Short-Form 1: global COP")
        page.screenshot(path=str(OUT / "short_1_global_cop.png"), full_page=False)

        # ── Short-Form Image 2: Wargaming matchup matrix ────────────────────
        # Capture just the .modal element (no dim backdrop) so the matrix fills the frame.
        print("[2/5] Short-Form 2: Wargaming matchup matrix")
        open_config_tab(page, "WARGAMING")
        page.wait_for_timeout(500)
        page.locator(".modal").screenshot(path=str(OUT / "short_2_wargaming.png"))
        close_modal(page)

        # ── Long-Form Image 1: Joint Targeting tab ──────────────────────────
        print("[3/5] Long-Form 1: Joint Targeting")
        open_config_tab(page, "JOINT TARGETING")
        page.wait_for_timeout(500)
        # Make sure the modal-body is scrolled to top so JTC phase tiles are visible.
        try:
            page.evaluate("const b=document.querySelector('.modal-body'); if(b) b.scrollTop=0;")
            page.wait_for_timeout(200)
        except Exception:
            pass
        page.locator(".modal").screenshot(path=str(OUT / "long_1_joint_targeting.png"))
        close_modal(page)

        # ── Long-Form Image 2: Analytics tab (cascade rules visible) ────────
        print("[4/5] Long-Form 2: Analytics + Cascade Rules")
        open_config_tab(page, "ANALYTICS")
        page.wait_for_timeout(500)
        # Scroll to the cascade rules editor section
        try:
            page.evaluate("""
                const body = document.querySelector('.modal-body');
                if (body) body.scrollTop = body.scrollHeight * 0.30;
            """)
            page.wait_for_timeout(300)
        except Exception:
            pass
        page.locator(".modal").screenshot(path=str(OUT / "long_2_analytics_cascades.png"))
        close_modal(page)

        # ── Long-Form Image 3: PR / JPRC ───────────────────────────────────
        print("[5/5] Long-Form 3: PR / JPRC")
        open_config_tab(page, "PR / JPRC")
        page.wait_for_timeout(500)
        page.locator(".modal").screenshot(path=str(OUT / "long_3_jprc.png"))
        close_modal(page)

        browser.close()

    print()
    print("[*] Done. Screenshots in:", OUT)
    for f in sorted(OUT.glob("*.png")):
        print(f"    - {f.name}  ({f.stat().st_size//1024} KB)")

if __name__ == "__main__":
    main()

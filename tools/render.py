"""Headless Chromium helpers, shared by the image and PDF builds.

Uses Playwright. If Playwright's own browser is not installed, set CHROMIUM_PATH
to any Chromium or Chrome binary.
"""

import os
from contextlib import contextmanager

from playwright.sync_api import sync_playwright


@contextmanager
def browser():
    with sync_playwright() as p:
        kwargs = {}
        if os.environ.get("CHROMIUM_PATH"):
            kwargs["executable_path"] = os.environ["CHROMIUM_PATH"]
        b = p.chromium.launch(**kwargs)
        try:
            yield b
        finally:
            b.close()


def wait_for_fonts(page):
    page.evaluate("document.fonts.ready.then(() => true)")

"""Rasterise SVG frames with headless Chromium (CPU, ~0.1-0.4 s per 1080x1920 frame)."""
import os
from playwright.sync_api import sync_playwright

KIT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(KIT), "fonts")

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Lilita';src:url('file://%s/lilita-one-latin-400-normal.woff2')}
@font-face{font-family:'PopX';font-weight:800;src:url('file://%s/poppins-latin-800-normal.woff2')}
@font-face{font-family:'PopX';font-weight:900;src:url('file://%s/poppins-latin-900-normal.woff2')}
html,body{margin:0;padding:0;background:#000;overflow:hidden}
</style></head><body><div id="s"></div></body></html>""" % (FONTS, FONTS, FONTS)


class Renderer:
    def __init__(self, w=1080, h=1920):
        self.pw = sync_playwright().start()
        self.b = self.pw.chromium.launch()
        self.p = self.b.new_page(viewport={"width": w, "height": h})
        path = os.path.join(KIT, "_page.html")
        open(path, "w").write(HTML)
        self.p.goto("file://" + path)
        self.p.evaluate("document.fonts.load('80px Lilita')")
        self.p.evaluate("document.fonts.load('800 80px PopX')")

    def frame(self, svg, out, jpeg=False):
        self.p.evaluate("s => { document.getElementById('s').innerHTML = s; }", svg)
        self.p.evaluate("() => document.fonts.ready")
        if jpeg:
            self.p.screenshot(path=out, type="jpeg", quality=92)
        else:
            self.p.screenshot(path=out)

    def close(self):
        self.b.close()
        self.pw.stop()

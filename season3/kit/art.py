"""Season 3 art kit: SVG helpers for the channel's 2D / 2.5D storybook look.

Channel style (keep identical in every episode):
- Ink: warm plum outline INK, ~5 px at 1080x1920 for hero characters, ~3.5 px for background.
- Two-tone cel shading: every shape = lit fill + shade crescent on the side away from the key light (shaded()).
- Limited palette below; warm key light (gold), violet-teal shadows; soft glows, light shafts, vignette.
"""
import math

W, H = 1080, 1920
INK = "#2a1c2e"

PAL = {
    "ink": INK, "gold": "#f2b544", "gold_d": "#c4842c", "warm": "#ffd99a", "cream": "#f6e7c8",
    "crimson": "#b8323f", "crimson_d": "#83213a", "navy": "#33468a", "navy_d": "#222c5e",
    "teal": "#1f6f78", "teal_d": "#164a5a", "sage": "#86a86b", "sage_d": "#5f7d55",
    "brown": "#8c6448", "brown_d": "#664531", "mustard": "#e3a83c", "mustard_d": "#b27a2b",
    "stone": "#cdbba0", "stone_d": "#8f7f8c", "plum": "#4a3561", "night": "#2c2445",
    "skin1": "#f2c9a6", "skin1_d": "#d29a85", "skin2": "#e8a987", "skin2_d": "#c47a6b",
    "skin3": "#c98a62", "skin3_d": "#a1654f", "white": "#f7f2e8", "white_d": "#cfc6d6",
}


class Doc:
    """Collects <defs> and body for one frame."""

    def __init__(self):
        self.defs = []
        self.n = 0

    def uid(self, p="i"):
        self.n += 1
        return f"{p}{self.n}"

    def svg(self, body, w=W, h=H):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
                f'<defs>{"".join(self.defs)}</defs>{body}</svg>')

    # ---- gradients / filters -------------------------------------------------
    def lin(self, stops, x1=0, y1=0, x2=0, y2=1, units="objectBoundingBox"):
        i = self.uid("g")
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in _stops(stops))
        self.defs.append(f'<linearGradient id="{i}" gradientUnits="{units}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient>')
        return f"url(#{i})"

    def rad(self, stops, cx=0.5, cy=0.5, r=0.5, units="objectBoundingBox", fx=None, fy=None):
        i = self.uid("r")
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in _stops(stops))
        f = f' fx="{fx}" fy="{fy}"' if fx is not None else ""
        self.defs.append(f'<radialGradient id="{i}" gradientUnits="{units}" cx="{cx}" cy="{cy}" r="{r}"{f}>{st}</radialGradient>')
        return f"url(#{i})"

    def blur(self, sd):
        i = self.uid("b")
        self.defs.append(f'<filter id="{i}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}"/></filter>')
        return f"url(#{i})"

    def clip(self, d):
        i = self.uid("c")
        self.defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
        return f"url(#{i})"

    # ---- the house shading style ---------------------------------------------
    def shaded(self, d, lit, shade, off=(9, 7), sw=5.0, ink=INK, rim=None, line=True):
        """Two-tone cel: shade fill, lit copy shifted toward the light, clipped to the shape, ink outline."""
        c = self.clip(d)
        s = f'<path d="{d}" fill="{shade}"/><g clip-path="{c}"><path d="{d}" transform="translate({-off[0]},{-off[1]})" fill="{lit}"/>'
        if rim:  # thin warm rim on the light side
            s += f'<path d="{d}" transform="translate({off[0]*0.6},{off[1]*0.6})" fill="none" stroke="{rim}" stroke-width="{sw*1.6}" opacity="0.55"/>'
        s += "</g>"
        if line:
            s += stroke(d, sw, ink)
        return s


def _stops(stops):
    out = []
    for s in stops:
        if len(s) == 2:
            out.append((s[0], s[1], 1))
        else:
            out.append(s)
    return out


def stroke(d, sw=5.0, ink=INK, op=1):
    return f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" opacity="{op}"/>'


def fill(d, c, op=1, extra=""):
    return f'<path d="{d}" fill="{c}" opacity="{op}" {extra}/>'


# ---- path builders -------------------------------------------------------------
def f2(v):
    return f"{v:.1f}"


def ell(cx, cy, rx, ry=None):
    ry = rx if ry is None else ry
    return (f"M{f2(cx-rx)},{f2(cy)}a{f2(rx)},{f2(ry)} 0 1,0 {f2(2*rx)},0"
            f"a{f2(rx)},{f2(ry)} 0 1,0 {f2(-2*rx)},0Z")


def poly(pts, close=True):
    s = "M" + " L".join(f"{f2(x)},{f2(y)}" for x, y in pts)
    return s + ("Z" if close else "")


def rrect(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return (f"M{f2(x+r)},{f2(y)}H{f2(x+w-r)}Q{f2(x+w)},{f2(y)} {f2(x+w)},{f2(y+r)}V{f2(y+h-r)}"
            f"Q{f2(x+w)},{f2(y+h)} {f2(x+w-r)},{f2(y+h)}H{f2(x+r)}Q{f2(x)},{f2(y+h)} {f2(x)},{f2(y+h-r)}"
            f"V{f2(y+r)}Q{f2(x)},{f2(y)} {f2(x+r)},{f2(y)}Z")


def blob(pts, t=1.0, close=True):
    """Smooth Catmull-Rom curve through pts (closed by default)."""
    n = len(pts)
    if n < 3:
        return poly(pts, close)
    P = pts if close else [pts[0]] + pts + [pts[-1]]
    m = len(P)
    rng = range(n) if close else range(1, m - 2)
    start = P[0] if close else P[1]
    s = f"M{f2(start[0])},{f2(start[1])}"
    for i in rng:
        p0, p1, p2, p3 = P[(i - 1) % m], P[i % m], P[(i + 1) % m], P[(i + 2) % m]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * t, p1[1] + (p2[1] - p0[1]) / 6 * t)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * t, p2[1] - (p3[1] - p1[1]) / 6 * t)
        s += f"C{f2(c1[0])},{f2(c1[1])} {f2(c2[0])},{f2(c2[1])} {f2(p2[0])},{f2(p2[1])}"
    return s + ("Z" if close else "")


def line(x1, y1, x2, y2):
    return f"M{f2(x1)},{f2(y1)}L{f2(x2)},{f2(y2)}"


def curve(*pts):
    """Open smooth curve through points."""
    return blob(list(pts), close=False)


def mirror(pts):
    """Symmetric outline: pts given for the right half top->bottom; returns full closed loop."""
    return pts + [(-x, y) for x, y in reversed(pts)]


def g(body, x=0, y=0, s=1, r=0, op=1, extra=""):
    t = f"translate({f2(x)},{f2(y)})"
    if r:
        t += f" rotate({r:.2f})"
    if s != 1:
        t += f" scale({s:.4f})"
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<g transform="{t}"{o} {extra}>{body}</g>'


def rot(px, py, deg, cx=0, cy=0):
    a = math.radians(deg)
    dx, dy = px - cx, py - cy
    return cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)


def _sat(self, v=1.15):
    i = self.uid("s")
    self.defs.append(f'<filter id="{i}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values="{v}"/></filter>')
    return f"url(#{i})"


Doc.sat = _sat

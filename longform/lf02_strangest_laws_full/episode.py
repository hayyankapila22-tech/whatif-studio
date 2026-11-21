# LF02 — "The 10 Strangest Laws Still on the Books" — long-form 16:9 (~8–9 min). Sources: sources.md.
# Data-driven: script.py sentences carry fx events (seg / step / pill / stamp / big / note) fired at each
# sentence's first keyword. Each segment = themed backdrop + big hero + right-hand detail card that changes on
# every "step" (icon list per segment in ICONS), + pills (top), stamps (lower right), subtitles (bottom).
import math, sys, os, json, subprocess, random
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, "..", "..", "howitworks")); sys.path.insert(0, D)
import skia
from engine import (paint, col, linear, radial, prog, eout, eio, eback, window, lerp, clamp, mixhex,
                    TF_BLACK, TF_BOLD, TF_REG, TF_MONO, INK, RED)
from script import SENTENCES

W, H, FPS = 1920, 1080, 30
T = json.load(open(os.environ.get("LF_TIMINGS", f"{D}/timings.json")))
P = T["phrases"]; DUR = round(T["duration"], 3)
GOLD = "#E8B54A"; CREAM = "#F6EEDC"; GREEN = "#1fb98a"; BLUE = "#3b7de0"; PINK = "#FF7BB0"

# ---------------- events from script fx ----------------
EV = {"seg": [], "step": [], "pill": [], "stamp": [], "big": [], "note": []}
pi = 0
for s in SENTENCES:
    n = s["cap"].count("||") + 1
    phs = P[pi:pi + n]; pi += n
    ks = [w["t0"] for ph in phs for w in ph["words"] if w["kw"]]
    t0 = phs[0]["t0"]; tk = ks[0] if ks else t0
    for f in s["fx"]:
        kind, _, arg = f.partition(":")
        tt = t0 - 0.15 if kind in ("seg", "big") else tk
        EV[kind].append((tt, arg))
assert pi == len(P), (pi, len(P))
SEGS = EV["seg"]
SEG_STEPS = {}
for (ts, _) in EV["step"]:
    sid = [s for (t, s) in SEGS if t <= ts + 1e-6][-1]
    SEG_STEPS.setdefault(sid, []).append(ts)
BIGS = EV["big"]


BOUNDS = sorted([x for (x, _) in EV["seg"]] + [x for (x, _) in EV["big"]])


def crossed(ts, t):
    """a segment change or big card started after ts and by t -> hide pills/stamps/notes from before it"""
    return any(ts + 0.05 < b <= t for b in BOUNDS)


def big_end(ts):
    later = [x for (x, _) in EV["seg"] + EV["step"] + EV["pill"] if x > ts + 0.3]
    return min(later) if later else DUR + 10


def active(lst, t, until=None):
    cur = None
    for (ts, a) in lst:
        if ts <= t: cur = (ts, a)
    return cur


def seg_at(t):
    a = active(SEGS, t)
    return a if a else SEGS[0]


def next_seg_time(t):
    for (ts, _) in SEGS:
        if ts > t: return ts
    return DUR + 10


# ---------------- helpers ----------------
def text_c(c, s, x, y, font, colr, a=1.0, track=0.0):
    w = sum(font.measureText(ch) + track for ch in s) - track
    xx = x - w / 2
    for ch in s:
        c.drawString(ch, xx, y, font, paint(colr, a)); xx += font.measureText(ch) + track
    return w


def fit_font(tf, s, maxw, size):
    f = skia.Font(tf, size)
    w = f.measureText(s)
    if w > maxw: f = skia.Font(tf, size * maxw / w)
    return f


def rr(c, l, t, r, b, rad, p):
    c.drawRoundRect(skia.Rect.MakeLTRB(l, t, r, b), rad, rad, p)


def poly(c, pts, p, close=True):
    pa = skia.Path(); pa.moveTo(*pts[0])
    for q in pts[1:]: pa.lineTo(*q)
    if close: pa.close()
    c.drawPath(pa, p)


def shadow(c, cx, cy, w, h, a=0.35):
    c.drawOval(skia.Rect.MakeLTRB(cx - w, cy - h, cx + w, cy + h), paint("#000000", a, blur=14))


# ---------------- icon library (drawn in a ~ -100..100 box) ----------------
def coin(c, label, face="#d9dde3", rim="#8b929c", txt=INK, r=80):
    c.drawCircle(4, 8, r, paint("#000000", 0.25, blur=8))
    c.drawCircle(0, 0, r, paint(shader=radial(-20, -25, r * 1.3, [col("#ffffff"), col(face), col(rim)], [0, 0.55, 1])))
    c.drawCircle(0, 0, r * 0.82, paint(rim, 0.6, stroke=4))
    text_c(c, label, 0, r * 0.22, fit_font(TF_BLACK, label, r * 1.4, r * 0.62), txt)


def glyph(c, s, bg, fg="#FFFFFF"):
    c.drawCircle(4, 8, 88, paint("#000000", 0.25, blur=8))
    c.drawCircle(0, 0, 88, paint(bg))
    text_c(c, s, 0, 40, fit_font(TF_BLACK, s, 130, 120), fg)


def xmark(c, a=1.0, s=1.0):
    c.drawLine(-70 * s, -70 * s, 70 * s, 70 * s, paint(RED, a, stroke=20)); c.drawLine(70 * s, -70 * s, -70 * s, 70 * s, paint(RED, a, stroke=20))


def check(c, colr=GREEN):
    c.drawCircle(0, 0, 88, paint(colr))
    pa = skia.Path(); pa.moveTo(-40, 2); pa.lineTo(-10, 32); pa.lineTo(45, -30)
    c.drawPath(pa, paint("#ffffff", 1, stroke=18))


def nosign(c, r=90):
    c.drawCircle(0, 0, r, paint(RED, 1, stroke=18))
    c.save(); c.rotate(-45); c.drawLine(-r, 0, r, 0, paint(RED, 1, stroke=18)); c.restore()


def doc(c, title, colr="#fbf4e2"):
    rr(c, -70, -95, 70, 95, 10, paint("#000000", 0.2, blur=8))
    rr(c, -70, -100, 70, 90, 10, paint(colr))
    text_c(c, title, 0, -55, fit_font(TF_BLACK, title, 110, 28), "#5a3a1a")
    for k in range(6):
        c.drawLine(-50, -25 + k * 18, 50 - (k % 2) * 25, -25 + k * 18, paint("#8a7a5a", 0.6, stroke=5))
    c.drawCircle(38, 62, 16, paint(RED, 0.85))


def gum(c):
    c.rotate(-8)
    rr(c, -95, -50, 95, 50, 14, paint(shader=linear((0, -50), (0, 50), [col("#ff9cc4"), col(PINK), col("#d94f8a")])))
    rr(c, -95, -14, 95, 14, 0, paint("#ffffff"))
    text_c(c, "GUM", 0, 10, skia.Font(TF_BLACK, 30), "#d94f8a", 1, 8)


def person(c, colr="#4a5a7c", skin="#E6B08A", shirt=True):
    c.drawCircle(0, -60, 30, paint(skin))
    rr(c, -40, -25, 40, 60, 24, paint(colr if shirt else skin))
    for sx in (-1, 1):
        rr(c, sx * 22 - 13, 50, sx * 22 + 13, 110, 12, paint("#2b3550"))


def icon(c, name, t=0.0):
    c.save()
    if name == "gum": gum(c)
    elif name == "shop_x":
        rr(c, -80, -40, 80, 80, 8, paint("#e9e4da")); poly(c, [(-95, -40), (95, -40), (80, -85), (-80, -85)], paint(RED))
        for k in range(4): rr(c, -95 + k * 48, -85, -71 + k * 48, -40, 0, paint("#ffffff", 0.9))
        rr(c, -25, 10, 25, 80, 4, paint("#7a5a3a")); c.save(); c.scale(0.8, 0.8); xmark(c); c.restore()
    elif name == "litter":
        rr(c, -100, 40, 100, 70, 6, paint("#9aa0a8"))
        for k, (x, y) in enumerate(((-60, 40), (-10, 46), (40, 40), (75, 48), (-85, 50))):
            c.drawOval(skia.Rect.MakeXYWH(x - 14, y - 8, 28, 14), paint(PINK if k % 2 else "#ff9cc4"))
        c.save(); c.translate(0, -30); c.scale(0.6, 0.6); gum(c); c.restore()
    elif name == "train":
        rr(c, -90, -90, 90, 90, 30, paint("#d9dde3")); rr(c, -70, -70, 70, -10, 10, paint("#2c3f63"))
        rr(c, -6, 0, 6, 80, 2, paint("#5d636c")); c.drawCircle(-50, 60, 10, paint("#ffd27a")); c.drawCircle(50, 60, 10, paint("#ffd27a"))
        c.drawOval(skia.Rect.MakeXYWH(-14, 20, 28, 18), paint(PINK))
    elif name == "hand":
        sk = paint("#E6B08A")
        rr(c, -55, -20, 55, 90, 40, sk)
        for k in range(4): rr(c, -52 + k * 28, -95 + (abs(k - 1.5) * 10), -30 + k * 28, 0, 12, sk)
        c.save(); c.translate(-62, 10); c.rotate(-35); rr(c, -14, -50, 14, 10, 12, sk); c.restore()
    elif name == "question": glyph(c, "?", BLUE)
    elif name == "exclaim": glyph(c, "!", RED)
    elif name == "sparkle":
        for k, (x, y, s) in enumerate(((0, 0, 1.0), (-60, -50, 0.5), (60, 40, 0.6))):
            c.save(); c.translate(x, y); c.scale(s, s)
            pa = skia.Path(); pa.moveTo(0, -80); pa.quadTo(0, 0, 80, 0); pa.quadTo(0, 0, 0, 80); pa.quadTo(0, 0, -80, 0); pa.quadTo(0, 0, 0, -80)
            c.drawPath(pa, paint(GOLD)); c.restore()
    elif name == "pharmacy":
        rr(c, -85, -85, 85, 85, 22, paint(GREEN)); rr(c, -22, -60, 22, 60, 6, paint("#ffffff")); rr(c, -60, -22, 60, 22, 6, paint("#ffffff"))
    elif name == "cane":
        c.drawLine(-60, 80, 50, -70, paint("#a8683a", 1, stroke=16)); nosign(c)
    elif name == "bucket":
        poly(c, [(-70, -40), (70, -40), (55, 85), (-55, 85)], paint("#8b929c"))
        for k in range(14): c.drawCircle(-55 + (k * 37) % 110, -45 - (k % 3) * 18, 18, paint("#c9973a" if k % 2 else "#d9dde3"))
        c.drawArc(skia.Rect.MakeLTRB(-75, -110, 75, 20), 200, 140, False, paint("#5d636c", 1, stroke=6))
    elif name == "doc_currency": doc(c, "CURRENCY ACT")
    elif name.startswith("coin_"):
        lab = {"coin_1": "1¢", "coin_5": "5¢", "coin_10": "10¢", "coin_d1": "$1", "coin_d2": "$2"}[name]
        face, rim = ("#d98a5a", "#8a4a2a") if name == "coin_1" else (("#e8c35a", "#9a7a2a") if name == "coin_d1" else ("#d9dde3", "#8b929c"))
        if name == "coin_d2":
            coin(c, "", "#e8c35a", "#9a7a2a"); c.drawCircle(0, 0, 46, paint(shader=radial(-10, -10, 60, [col("#ffffff"), col("#c9ced6")]))); text_c(c, "$2", 0, 16, skia.Font(TF_BLACK, 44), INK)
        else:
            coin(c, lab, face, rim)
    elif name == "wheelbarrow":
        poly(c, [(-90, -30), (60, -30), (40, 40), (-70, 40)], paint("#3b7de0"))
        for k in range(12): c.drawCircle(-70 + (k * 29) % 130, -38 - (k % 3) * 14, 15, paint("#d98a5a"))
        c.drawCircle(50, 70, 26, paint("#2b2b2e")); c.drawLine(-70, 40, -110, 90, paint("#5d636c", 1, stroke=8))
    elif name == "penny_x": coin(c, "1¢", "#d98a5a", "#8a4a2a"); c.save(); c.scale(0.9, 0.9); xmark(c); c.restore()
    elif name == "receipts":
        for k in range(4):
            c.save(); c.translate(-30 + k * 20, -10 + k * 8); c.rotate(-10 + k * 7)
            rr(c, -50, -70, 50, 70, 6, paint("#ffffff")); rr(c, -50, -70, 50, 70, 6, paint("#c9ced6", 1, stroke=2))
            for j in range(5): c.drawLine(-35, -45 + j * 20, 35, -45 + j * 20, paint("#9aa0a8", 1, stroke=4))
            c.restore()
    elif name == "speedo":
        c.drawCircle(0, 10, 90, paint("#1b1f27")); c.drawArc(skia.Rect.MakeLTRB(-70, -60, 70, 80), 150, 240, False, paint("#3a3f48", 1, stroke=14))
        c.drawArc(skia.Rect.MakeLTRB(-70, -60, 70, 80), 150, 230, False, paint(RED, 1, stroke=14))
        ang = math.radians(150 + 225 + 4 * math.sin(t * 20)); c.drawLine(0, 10, 60 * math.cos(ang), 10 + 60 * math.sin(ang), paint("#ffffff", 1, stroke=8))
    elif name == "fuel_empty":
        rr(c, -90, -60, 90, 60, 20, paint("#1b1f27"))
        c.drawArc(skia.Rect.MakeLTRB(-70, -40, 70, 100), 200, 140, False, paint("#ffffff", 0.7, stroke=6))
        text_c(c, "E", -62, 34, skia.Font(TF_BLACK, 30), RED); text_c(c, "F", 62, 34, skia.Font(TF_BLACK, 30), "#ffffff")
        c.drawLine(0, 30, -52, -2, paint(RED, 1, stroke=8)); c.drawCircle(0, 30, 10, paint("#ffffff"))
    elif name == "nostop":
        c.drawCircle(0, 0, 88, paint("#2f5fd1")); c.drawCircle(0, 0, 88, paint(RED, 1, stroke=16))
        c.save(); c.rotate(45); c.drawLine(-80, 0, 80, 0, paint(RED, 1, stroke=16)); c.rotate(-90); c.drawLine(-80, 0, 80, 0, paint(RED, 1, stroke=16)); c.restore()
    elif name == "wrench": check(c)
    elif name == "fuel_pump":
        rr(c, -55, -80, 35, 90, 10, paint(RED)); rr(c, -40, -60, 20, -10, 6, paint("#ffffff", 0.85))
        c.drawLine(35, -40, 70, -10, paint("#2b2b2e", 1, stroke=10)); c.drawLine(70, -10, 70, 60, paint("#2b2b2e", 1, stroke=10))
    elif name == "jerrycan":
        rr(c, -70, -60, 70, 90, 14, paint("#c0392b")); rr(c, -30, -90, 10, -60, 6, paint("#a93226"))
        c.drawLine(-50, -30, 50, 70, paint("#a93226", 1, stroke=8)); c.drawLine(50, -30, -50, 70, paint("#a93226", 1, stroke=8))
    elif name == "sun":
        for k in range(12):
            a = k * math.pi / 6 + t * 0.4; c.drawLine(60 * math.cos(a), 60 * math.sin(a), 95 * math.cos(a), 95 * math.sin(a), paint(GOLD, 1, stroke=10))
        c.drawCircle(0, 0, 50, paint("#ffcf4a"))
    elif name == "shirt":
        poly(c, [(-40, -80), (-95, -45), (-70, -5), (-50, -20), (-50, 85), (50, 85), (50, -20), (70, -5), (95, -45), (40, -80), (0, -60)], paint(BLUE))
    elif name == "shirtless": person(c, shirt=False)
    elif name == "bus":
        rr(c, -95, -70, 95, 60, 18, paint("#e8473b")); rr(c, -80, -55, 80, -5, 8, paint("#bfe3ff"))
        c.drawCircle(-55, 65, 18, paint("#2b2b2e")); c.drawCircle(55, 65, 18, paint("#2b2b2e"))
    elif name == "police":
        rr(c, -80, -20, 80, 20, 10, paint("#1b2a4d")); poly(c, [(-70, -20), (70, -20), (50, -80), (-50, -80)], paint("#1b2a4d"))
        c.drawCircle(0, -45, 18, paint(GOLD)); rr(c, -90, 15, 90, 35, 8, paint("#111827"))
    elif name == "umbrella":
        pa = skia.Path(); pa.moveTo(-100, -10); pa.quadTo(0, -130, 100, -10); pa.close(); c.drawPath(pa, paint("#ff6b6b"))
        c.drawLine(0, -60, 0, 90, paint("#5d636c", 1, stroke=8)); rr(c, -100, 85, 100, 100, 6, paint("#f2d6a8"))
    elif name == "runner":
        c.drawCircle(10, -70, 24, paint("#E6B08A")); c.drawLine(0, -40, -15, 25, paint(BLUE, 1, stroke=26))
        c.drawLine(-15, 25, -60, 80, paint("#2b3550", 1, stroke=18)); c.drawLine(-15, 25, 40, 70, paint("#2b3550", 1, stroke=18))
        c.drawLine(-5, -25, -55, 0, paint("#E6B08A", 1, stroke=14)); c.drawLine(-5, -25, 45, -45, paint("#E6B08A", 1, stroke=14))
    elif name == "pigeon": pigeon(c, 0, 10, 1.0, t)
    elif name == "seed_bag":
        poly(c, [(-60, -50), (60, -50), (75, 85), (-75, 85)], paint("#d9b77a")); text_c(c, "SEED", 0, 30, skia.Font(TF_BLACK, 30), "#6b4a1a")
        for k in range(8): c.drawCircle(-50 + k * 14, -55 - (k % 2) * 8, 6, paint("#c49a4a"))
    elif name == "building_crack":
        rr(c, -80, -90, 80, 90, 4, paint("#e0c9a6"))
        for r_ in range(3):
            for k in range(3): rr(c, -60 + k * 45, -70 + r_ * 55, -35 + k * 45, -30 + r_ * 55, 10, paint("#6b5a4a"))
        poly(c, [(10, -90), (-5, -40), (20, 0), (0, 50)], paint("#3a2a1a", 1, stroke=6), close=False)
    elif name == "square":
        rr(c, -95, 20, 95, 90, 6, paint("#d9c9a6"))
        for k in range(9): pigeon(c, -80 + (k * 41) % 170, 30 + (k * 23) % 50, 0.28, t + k)
        poly(c, [(-60, 20), (-60, -60), (0, -100), (60, -60), (60, 20)], paint("#c9a66b"))
    elif name == "closed":
        rr(c, -90, -45, 90, 45, 10, paint(RED)); text_c(c, "CLOSED", 0, 14, skia.Font(TF_BLACK, 40), "#ffffff", 1, 3)
        c.drawLine(-50, -45, 0, -90, paint("#5d636c", 1, stroke=4)); c.drawLine(50, -45, 0, -90, paint("#5d636c", 1, stroke=4))
    elif name == "steps":
        for k in range(7): rr(c, -90 + k * 8, 70 - k * 24, 90 - k * 8, 90 - k * 24, 2, paint(mixhex("#f2e3c6", "#d9bf94", k / 6)))
    elif name == "gelato":
        poly(c, [(-40, -10), (40, -10), (0, 95)], paint("#d9a35a"))
        for k, cc in enumerate(("#ffb3c7", "#a8e6cf", "#fff1b3")): c.drawCircle(-25 + k * 25, -30 - (k % 2) * 30, 34, paint(cc))
    elif name == "sit_x": person(c, BLUE); c.save(); c.scale(1.0, 1.0); xmark(c, 0.9); c.restore()
    elif name == "arrows":
        for sx, d in ((-40, -1), (40, 1)):
            c.drawLine(sx, -70, sx, 70, paint(GREEN, 1, stroke=18))
            y = 70 * d; poly(c, [(sx - 30, y - 20 * d), (sx + 30, y - 20 * d), (sx, y + 20 * d)], paint(GREEN))
    elif name == "whistle":
        rr(c, -80, -30, 40, 40, 30, paint("#c9ced6")); rr(c, 20, -30, 95, 0, 8, paint("#c9ced6")); c.drawCircle(-30, 5, 16, paint("#5d636c"))
        for k in range(3): c.drawArc(skia.Rect.MakeLTRB(60 + k * 15, -80 - k * 15, 110 + k * 25, -20 + k * 5), 270, 90, False, paint(RED, 1, stroke=6))
    elif name == "washing":
        c.drawLine(-100, -60, 100, -60, paint("#5d636c", 1, stroke=4))
        for k, cc in enumerate(("#3b7de0", "#ff6b6b", "#1fb98a")): rr(c, -85 + k * 60, -60, -40 + k * 60, 30 + (k % 2) * 30, 6, paint(cc))
        c.save(); c.scale(0.9, 0.9); nosign(c); c.restore()
    elif name == "gelato_euro": icon(c, "gelato"); c.save(); c.translate(55, 45); c.scale(0.45, 0.45); glyph(c, "€", GOLD, INK); c.restore()
    elif name == "spot":
        c.drawCircle(0, 0, 92, paint(shader=radial(0, 0, 92, [col("#ffffff", 0.9), col("#ffffff", 0)])))
        glyph(c, "?", "#2a2729")
    elif name == "redcross":
        rr(c, -88, -88, 88, 88, 14, paint("#ffffff")); rr(c, -22, -66, 22, 66, 2, paint("#E5232B")); rr(c, -66, -22, 66, 22, 2, paint("#E5232B"))
    elif name == "kit":
        rr(c, -95, -60, 95, 80, 16, paint(GREEN)); rr(c, -30, -90, 30, -60, 10, paint("#13785a", 1, stroke=10))
        rr(c, -14, -35, 14, 55, 3, paint("#ffffff")); rr(c, -45, -4, 45, 24, 3, paint("#ffffff"))
    elif name == "gavel": gavel(c, 0, -10, 0.45, 30)
    elif name == "text_rc": rr(c, -100, -45, 100, 45, 12, paint("#ffffff")); text_c(c, "RED CROSS", 0, 14, fit_font(TF_BLACK, "RED CROSS", 170, 40), "#E5232B")
    elif name == "text_gc": rr(c, -100, -45, 100, 45, 12, paint("#ffffff")); text_c(c, "GENEVA CROSS", 0, 14, fit_font(TF_BLACK, "GENEVA CROSS", 170, 40), "#E5232B")
    elif name == "shield":
        pa = skia.Path(); pa.moveTo(0, -95); pa.lineTo(80, -60); pa.cubicTo(80, 30, 40, 70, 0, 95); pa.cubicTo(-40, 70, -80, 30, -80, -60); pa.close()
        c.drawPath(pa, paint("#ffffff")); c.drawPath(pa, paint("#9aa0a8", 1, stroke=4))
        rr(c, -14, -50, 14, 40, 2, paint("#E5232B")); rr(c, -44, -20, 44, 10, 2, paint("#E5232B"))
    elif name == "dove":
        pa = skia.Path(); pa.moveTo(-90, 10); pa.cubicTo(-40, -60, 20, -40, 40, -10); pa.cubicTo(70, -30, 90, -20, 95, -10)
        pa.cubicTo(70, 0, 60, 30, 20, 40); pa.cubicTo(-20, 50, -60, 40, -90, 10); pa.close(); c.drawPath(pa, paint("#ffffff"))
        c.drawCircle(70, -20, 5, paint(INK))
    elif name == "greencross":
        rr(c, -88, -88, 88, 88, 14, paint(GREEN)); rr(c, -22, -66, 22, 66, 2, paint("#ffffff")); rr(c, -66, -22, 66, 22, 2, paint("#ffffff"))
    elif name == "doc_ch": doc(c, "TIERSCHUTZ")
    elif name == "gp": guinea(c, 0, 10, 1.0, t)
    elif name == "gp2": guinea(c, -45, 20, 0.7, t); guinea(c, 50, 30, 0.7, t + 1, flip=True)
    elif name == "hearts":
        for k, (x, y, s) in enumerate(((0, 0, 1.0), (-60, -50, 0.5), (65, -40, 0.6))): heart(c, x, y, s)
    elif name == "sad":
        c.drawCircle(0, 0, 88, paint(GOLD)); c.drawCircle(-30, -20, 10, paint(INK)); c.drawCircle(30, -20, 10, paint(INK))
        c.drawArc(skia.Rect.MakeLTRB(-40, 20, 40, 70), 200, 140, False, paint(INK, 1, stroke=8))
    elif name == "gp_alone": guinea(c, 0, 20, 0.8, t); c.save(); c.translate(60, -60); c.scale(0.35, 0.35); icon(c, "sad"); c.restore()
    elif name == "doc_uk": doc(c, "LICENSING ACT")
    elif name == "doc_salmon": doc(c, "SALMON ACT")
    elif name == "cow": cow(c, 0, 20, 0.55, t)
    elif name == "horseshoe":
        c.drawArc(skia.Rect.MakeLTRB(-70, -80, 70, 60), 330, 240, False, paint("#8b929c", 1, stroke=30))
        for k in range(6):
            a = math.radians(-30 + k * 48); c.drawCircle(70 * math.cos(a + math.pi / 2), -10 + 70 * math.sin(a + math.pi / 2) * -1, 6, paint("#3a3f48"))
    elif name == "steam":
        rr(c, -90, -20, 50, 50, 10, paint("#2b2b2e")); rr(c, 20, -70, 90, 50, 8, paint("#3a3f48")); rr(c, -70, -60, -40, -20, 4, paint("#2b2b2e"))
        for k in range(3): c.drawCircle(-55 + k * 20, -85 - k * 22 - 10 * math.sin(t * 3 + k), 18 + k * 6, paint("#d9dde3", 0.8))
        for x in (-60, -10, 50): c.drawCircle(x, 60, 20, paint("#5d636c"))
    elif name == "warn":
        poly(c, [(0, -90), (95, 80), (-95, 80)], paint(GOLD)); text_c(c, "!", 0, 60, skia.Font(TF_BLACK, 110), INK)
    elif name == "check": check(c)
    elif name == "car": car(c, 0, 20, 0.5, RED)
    elif name == "laugh":
        c.drawCircle(0, 0, 88, paint(GOLD)); c.drawArc(skia.Rect.MakeLTRB(-45, -35, -15, -5), 200, 140, False, paint(INK, 1, stroke=8))
        c.drawArc(skia.Rect.MakeLTRB(15, -35, 45, -5), 200, 140, False, paint(INK, 1, stroke=8))
        pa = skia.Path(); pa.moveTo(-50, 15); pa.quadTo(0, 85, 50, 15); pa.close(); c.drawPath(pa, paint(INK))
    elif name == "box_fish":
        rr(c, -90, -10, 90, 80, 8, paint("#c49a6c")); salmon(c, 0, -30, 0.45, t)
    elif name == "net":
        for k in range(7):
            c.drawLine(-90 + k * 30, -80, -90 + k * 30, 80, paint("#5d636c", 1, stroke=4)); c.drawLine(-90, -80 + k * 27, 90, -80 + k * 27, paint("#5d636c", 1, stroke=4))
        c.save(); c.scale(0.9, 0.9); nosign(c); c.restore()
    elif name == "eel":
        pa = skia.Path()
        for k in range(41):
            x = -95 + k * 4.75; y = 30 * math.sin(k / 40 * 9 + t * 3)
            pa.moveTo(x, y) if k == 0 else pa.lineTo(x, y)
        c.drawPath(pa, paint("#4a5a3a", 1, stroke=26)); c.drawCircle(95, 30 * math.sin(9 + t * 3), 6, paint("#ffffff"))
    elif name == "scales":
        c.drawLine(0, -80, 0, 80, paint(GOLD, 1, stroke=10)); c.drawLine(-80, -50, 80, -50, paint(GOLD, 1, stroke=8)); rr(c, -50, 75, 50, 90, 4, paint(GOLD))
        for sx in (-1, 1): c.drawArc(skia.Rect.MakeLTRB(sx * 80 - 35, -40, sx * 80 + 35, 20), 0, 180, True, paint(GOLD))
    elif name == "coat_man":
        poly(c, [(-50, -40), (50, -40), (75, 95), (-75, 95)], paint("#6b5a44")); c.drawCircle(0, -65, 30, paint("#E6B08A"))
        rr(c, -50, -110, 50, -85, 6, paint("#3a2f24")); rr(c, -35, -130, 35, -100, 10, paint("#3a2f24"))
        c.save(); c.translate(55, 30); c.scale(0.35, 0.35); salmon(c, 0, 0, 1.0, t); c.restore()
    elif name == "walk":
        for k in range(3):
            c.save(); c.translate(-60 + k * 60, 40 - k * 40); c.rotate(-20)
            c.drawOval(skia.Rect.MakeXYWH(-16, -30, 32, 52), paint("#2b2b2e")); c.restore()
    elif name == "scroll":
        rr(c, -70, -80, 70, 80, 6, paint("#efe0bd")); rr(c, -85, -95, 85, -70, 12, paint("#c9a66b")); rr(c, -85, 70, 85, 95, 12, paint("#c9a66b"))
        text_c(c, "1313", 0, 15, skia.Font(TF_BLACK, 46), "#5a3a1a")
    elif name == "helmet": knight_helmet(c, 0, 0, 0.75)
    elif name == "calendar":
        rr(c, -80, -75, 80, 85, 12, paint("#ffffff")); rr(c, -80, -75, 80, -30, 12, paint(RED))
        text_c(c, "700+", 0, 50, skia.Font(TF_BLACK, 56), INK); text_c(c, "YEARS", 0, -42, skia.Font(TF_BLACK, 26), "#ffffff", 1, 3)
    elif name == "knight": person(c, "#9aa0a8"); c.save(); c.translate(0, -60); c.scale(0.35, 0.35); knight_helmet(c, 0, 0, 1.0); c.restore()
    elif name == "money":
        for k in range(4): rr(c, -90 + k * 8, 40 - k * 28, 70 + k * 8, 80 - k * 28, 8, paint(mixhex("#3fa36b", "#7fd3a0", k / 3)))
        text_c(c, "€", -10 + 24, -38, skia.Font(TF_BLACK, 50), "#ffffff")
    elif name == "calendar_money":
        rr(c, -80, -75, 80, 85, 12, paint("#ffffff")); rr(c, -80, -75, 80, -30, 12, paint(BLUE))
        text_c(c, "€/DAY", 0, 45, fit_font(TF_BLACK, "€/DAY", 140, 50), INK)
    elif name == "diamond":
        poly(c, [(-80, -30), (-40, -75), (40, -75), (80, -30), (0, 85)], paint("#8fe3ff")); poly(c, [(-80, -30), (80, -30), (0, 85)], paint("#5cc8f0"))
    elif name == "speed50":
        c.drawCircle(0, 0, 88, paint("#ffffff")); c.drawCircle(0, 0, 88, paint(RED, 1, stroke=18)); text_c(c, "50", 0, 32, skia.Font(TF_BLACK, 84), INK)
    elif name == "trophy":
        poly(c, [(-55, -80), (55, -80), (40, 10), (-40, 10)], paint(GOLD)); rr(c, -12, 10, 12, 50, 4, paint(GOLD)); rr(c, -50, 50, 50, 75, 6, paint("#9a7a2a"))
        for sx in (-1, 1): c.drawArc(skia.Rect.MakeLTRB(sx * 60 - 30, -70, sx * 60 + 30, -10), 0, 360, False, paint(GOLD, 1, stroke=10))
    elif name == "sausage":
        c.rotate(-15); rr(c, -95, -28, 95, 28, 28, paint(shader=linear((0, -28), (0, 28), [col("#d9784a"), col("#9a3f1f")])))
        c.drawLine(-60, -10, 60, -10, paint("#ffffff", 0.35, stroke=5))
    elif name == "cal_sun":
        rr(c, -80, -75, 80, 85, 12, paint("#ffffff")); rr(c, -80, -75, 80, -30, 12, paint(RED))
        text_c(c, "SUN", 0, 45, skia.Font(TF_BLACK, 52), RED); c.save(); c.scale(0.95, 0.95); nosign(c); c.restore()
    elif name == "smash":
        for k in range(8):
            a = k * math.pi / 4; c.drawLine(20 * math.cos(a), 20 * math.sin(a), 90 * math.cos(a), 90 * math.sin(a), paint(GOLD, 1, stroke=8))
        bottle(c, 0, 10, 0.7, "#2f9e5a")
    elif name == "register":
        rr(c, -75, -95, 75, 95, 10, paint("#ffffff"))
        for k, nm in enumerate(("ANNA", "JÓN", "SIGRÚN", "EMIL", "HEKLA")):
            text_c(c, nm, -5, -55 + k * 34, skia.Font(TF_BOLD, 24), INK); c.save(); c.translate(52, -63 + k * 34); c.scale(0.12, 0.12); check(c); c.restore()
    elif name == "committee":
        for k, x in enumerate((-60, 0, 60)): c.save(); c.translate(x, 0); c.scale(0.55, 0.55); person(c, ("#4a5a7c", "#7a4a5a", "#3a6a5a")[k]); c.restore()
        rr(c, -100, 40, 100, 70, 6, paint("#7a5a3a"))
    elif name == "book":
        rr(c, -80, -90, 80, 90, 10, paint("#c8102e")); rr(c, -60, -70, 60, 70, 6, paint("#ffffff", 0.0))
        text_c(c, "50,000", 0, 0, fit_font(TF_BLACK, "50,000", 130, 44), "#ffffff"); text_c(c, "NAMES", 0, 40, skia.Font(TF_BOLD, 26), "#ffffff", 1, 4)
    elif name == "form":
        rr(c, -75, -95, 75, 95, 10, paint("#ffffff")); text_c(c, "NEW NAME", 0, -55, skia.Font(TF_BLACK, 24), INK)
        for k in range(3): rr(c, -55, -30 + k * 40, 55, -10 + k * 40, 4, paint("#e6e6e6"))
        c.save(); c.translate(45, 60); c.scale(0.3, 0.3); check(c); c.restore()
    elif name == "recap1": mini_row(c, ["gum", "coin_1", "fuel_empty"], t)
    elif name == "recap2": mini_row(c, ["shirt", "pigeon", "steps"], t)
    elif name == "recap3": mini_row(c, ["redcross", "gp2", "cow", "salmon_i", "helmet"], t)
    elif name == "salmon_i": salmon(c, 0, 0, 0.7, t)
    elif name == "comment":
        rr(c, -90, -70, 90, 50, 24, paint("#ffffff")); poly(c, [(-40, 50), (-10, 50), (-50, 90)], paint("#ffffff"))
        for k in range(3): c.drawCircle(-40 + k * 40, -10, 12, paint(INK))
    elif name == "bell":
        pa = skia.Path(); pa.moveTo(-70, 50); pa.cubicTo(-60, 10, -60, -70, 0, -75); pa.cubicTo(60, -70, 60, 10, 70, 50); pa.close()
        c.save(); c.rotate(10 * math.sin(t * 10)); c.drawPath(pa, paint(GOLD)); c.drawCircle(0, 65, 16, paint(GOLD)); c.restore()
    elif name == "wave": icon(c, "hand")
    else:
        glyph(c, "?", "#555")
    c.restore()


def mini_row(c, names, t):
    n = len(names); s = 0.9 if n <= 3 else 0.62
    for k, nm in enumerate(names):
        c.save(); c.translate((k - (n - 1) / 2) * (200 * s + 10), 0); c.scale(s * 0.8, s * 0.8); icon(c, nm, t); c.restore()


# ---------------- big drawings ----------------
def pigeon(c, x, y, s, t, flip=False):
    c.save(); c.translate(x, y + 4 * math.sin(t * 6)); c.scale(-s if flip else s, s)
    c.drawOval(skia.Rect.MakeLTRB(-70, -30, 60, 45), paint(shader=linear((0, -30), (0, 45), [col("#9aa3b5"), col("#6b7488")])))
    c.drawOval(skia.Rect.MakeLTRB(-60, -20, 20, 30), paint("#808aa0"))
    c.drawCircle(55, -40, 26, paint("#6b7488")); c.drawCircle(50, -25, 14, paint("#5aa38a", 0.8))
    c.drawCircle(62, -46, 5, paint("#ff8a3a")); poly(c, [(78, -40), (95, -34), (78, -30)], paint("#3a3a3a"))
    poly(c, [(-70, 0), (-110, -10), (-100, 20)], paint("#5d6578"))
    for lx in (-10, 15): c.drawLine(lx, 40, lx, 62, paint("#e07a5a", 1, stroke=5))
    c.restore()


def guinea(c, x, y, s, t, flip=False):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s * (1 + 0.02 * math.sin(t * 4)))
    c.drawOval(skia.Rect.MakeLTRB(-95, -50, 85, 60), paint(shader=radial(-20, -20, 120, [col("#e8b27a"), col("#b5743f")])))
    c.drawOval(skia.Rect.MakeLTRB(-40, -50, 40, 10), paint("#ffffff", 0.9))
    c.drawOval(skia.Rect.MakeLTRB(40, -40, 105, 30), paint("#c98a55")); c.drawCircle(78, -10, 7, paint(INK)); c.drawCircle(80, -12, 2.5, paint("#ffffff"))
    c.drawOval(skia.Rect.MakeLTRB(50, -55, 75, -35), paint("#a8673a")); c.drawCircle(102, 4, 5, paint("#d97a7a"))
    for lx in (-60, 40): c.drawOval(skia.Rect.MakeLTRB(lx - 12, 50, lx + 12, 64), paint("#e8a7a7"))
    c.restore()


def heart(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    pa = skia.Path(); pa.moveTo(0, 60); pa.cubicTo(-100, -10, -70, -100, 0, -45); pa.cubicTo(70, -100, 100, -10, 0, 60); pa.close()
    c.drawPath(pa, paint("#ff5a6e")); c.restore()


def cow(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 180, 220, 20)
    rr(c, -170, -70, 150, 100, 70, paint("#fbfbf8"))
    for (ox, oy, rx, ry) in ((-80, -20, 50, 35), (40, 20, 60, 40), (100, -40, 30, 25)): c.drawOval(skia.Rect.MakeLTRB(ox - rx, oy - ry, ox + rx, oy + ry), paint("#2b2b2e"))
    for lx in (-130, -70, 70, 120): rr(c, lx - 16, 80, lx + 16, 180, 10, paint("#fbfbf8")); rr(c, lx - 16, 160, lx + 16, 180, 4, paint("#3a3a3a"))
    c.save(); c.translate(185, -60); c.rotate(8 * math.sin(t * 1.5))
    rr(c, -55, -60, 55, 70, 40, paint("#fbfbf8")); rr(c, -45, 20, 45, 70, 25, paint("#f2b8b8"))
    c.drawCircle(-20, 45, 7, paint("#8a4a4a")); c.drawCircle(20, 45, 7, paint("#8a4a4a"))
    c.drawCircle(-25, -15, 9, paint(INK)); c.drawCircle(25, -15, 9, paint(INK))
    for sx in (-1, 1): c.drawLine(sx * 45, -55, sx * 80, -85, paint("#d9c9a6", 1, stroke=12))
    c.restore()
    c.drawLine(-170, -40, -210, 40 + 10 * math.sin(t * 3), paint("#fbfbf8", 1, stroke=10))
    c.restore()


def salmon(c, x, y, s, t):
    c.save(); c.translate(x, y); c.rotate(4 * math.sin(t * 2)); c.scale(s, s)
    pa = skia.Path(); pa.moveTo(-200, 0); pa.cubicTo(-120, -90, 120, -80, 190, 0); pa.cubicTo(120, 70, -120, 80, -200, 0); pa.close()
    c.drawPath(pa, paint(shader=linear((0, -80), (0, 80), [col("#8fa8c0"), col("#f2a07a"), col("#fbe4d6")], [0, 0.45, 1])))
    poly(c, [(-190, 0), (-280, -60), (-260, 0), (-280, 60)], paint("#7f97ae"))
    for k in range(12): c.drawCircle(-100 + k * 20, -35 + (k % 3) * 8, 4, paint("#3a4a5a", 0.6))
    c.drawCircle(140, -12, 12, paint("#ffffff")); c.drawCircle(143, -12, 6, paint(INK))
    c.drawArc(skia.Rect.MakeLTRB(90, -40, 140, 40), 280, 70, False, paint("#c9734f", 1, stroke=5))
    c.restore()


def car(c, x, y, s, colr):
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 110, 230, 18)
    pa = skia.Path(); pa.moveTo(-220, 60); pa.lineTo(-220, 0); pa.cubicTo(-210, -30, -150, -40, -110, -45); pa.lineTo(-60, -110)
    pa.lineTo(80, -110); pa.lineTo(140, -45); pa.cubicTo(200, -40, 225, -20, 225, 20); pa.lineTo(225, 60); pa.close()
    c.drawPath(pa, paint(shader=linear((0, -110), (0, 60), [col(mixhex(colr, "#ffffff", 0.3)), col(colr), col(mixhex(colr, "#000000", 0.4))])))
    poly(c, [(-45, -95), (10, -95), (10, -50), (-90, -50)], paint("#2c3f63")); poly(c, [(25, -95), (75, -95), (115, -50), (25, -50)], paint("#2c3f63"))
    for wx in (-130, 130):
        c.drawCircle(wx, 65, 48, paint("#16161a")); c.drawCircle(wx, 65, 24, paint("#c9ced6"))
    rr(c, 205, -10, 225, 10, 4, paint("#fff1b0"))
    c.restore()


def bottle(c, x, y, s, colr):
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -35, -40, 35, 110, 18, paint(colr, 0.9)); rr(c, -14, -100, 14, -30, 8, paint(colr, 0.9))
    c.drawLine(-20, -20, -20, 90, paint("#ffffff", 0.4, stroke=8)); c.restore()


def knight_helmet(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    pa = skia.Path(); pa.moveTo(-90, 110); pa.lineTo(-90, -20); pa.cubicTo(-90, -110, 90, -110, 90, -20); pa.lineTo(90, 110); pa.close()
    c.drawPath(pa, paint(shader=linear((-90, 0), (90, 0), [col("#f2f4f7"), col("#9aa2ad"), col("#5d646e")])))
    rr(c, -70, -10, 70, 10, 4, paint("#1b1f27")); c.drawLine(0, -100, 0, 110, paint("#7d858f", 1, stroke=6))
    for k in range(5): c.drawCircle(-50 + k * 25, 50, 5, paint("#1b1f27"))
    pa2 = skia.Path(); pa2.moveTo(0, -100); pa2.cubicTo(30, -160, 90, -170, 120, -150); pa2.cubicTo(80, -120, 40, -110, 0, -100)
    c.drawPath(pa2, paint(RED)); c.restore()


def gavel(c, x, y, s, ang, a=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    rr(c, -14, -10, 14, 300, 12, paint(shader=linear((-14, 0), (14, 0), [col("#a8683a", a), col("#5e3418", a)])))
    rr(c, -110, -70, 110, 10, 24, paint(shader=linear((0, -70), (0, 10), [col("#b97644", a), col("#6b3a1a", a)])))
    for xx in (-80, 80): c.drawRect(skia.Rect.MakeLTRB(xx - 8, -72, xx + 8, 12), paint(GOLD, a))
    c.restore()


def law_book(c, x, y, s, a=1.0, open_=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shadow(c, 0, 240, 320, 26, 0.45 * a)
    if open_ < 0.5:
        rr(c, -260, -220, 260, 220, 16, paint(shader=linear((0, -220), (0, 220), [col("#7a2a22", a), col("#4e1712", a)])))
        rr(c, -260, -220, -215, 220, 10, paint("#3a100c", a)); rr(c, -200, -180, 230, 180, 10, paint(GOLD, 0.8 * a, stroke=4))
        text_c(c, "LAWS", 15, -10, skia.Font(TF_BLACK, 54), GOLD, a, 10); text_c(c, "VOL. X", 15, 60, skia.Font(TF_BOLD, 26), GOLD, 0.8 * a, 6)
    else:
        for sx in (-1, 1):
            pg = skia.Path(); pg.moveTo(0, -200); pg.cubicTo(sx * 120, -230, sx * 250, -210, sx * 300, -200)
            pg.lineTo(sx * 300, 210); pg.cubicTo(sx * 250, 200, sx * 120, 220, 0, 230); pg.close()
            c.drawPath(pg, paint(shader=linear((0, -200), (0, 230), [col("#fbf4e2", a), col("#e9dcc0", a)])))
            for k in range(12): c.drawLine(sx * 40, -150 + k * 28, sx * (260 - (k % 3) * 30), -150 + k * 28, paint("#8a7a5a", 0.45 * a, stroke=4))
        c.drawLine(0, -200, 0, 230, paint("#c9b88f", a, stroke=3))
    c.restore()


# ---------------- backdrops ----------------
def bg_studio(c, t, top="#1b2440", mid="#101626", bot="#070a12"):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.45, 1300, [col(top), col(mid), col(bot)], [0, 0.6, 1])))
    r = random.Random(3)
    for _ in range(36):
        x, y, rad, ph = r.random() * W, r.random() * H, r.uniform(1, 3), r.random() * 6
        c.drawCircle((x + t * 14) % W, (y - t * 8) % H, rad, paint("#ffffff", 0.10 * (0.6 + 0.4 * math.sin(t * 2 + ph)), blur=1.5))


def bg_skyline(c, t, sky, seed=5, water=True):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col(sky[0]), col(sky[1]), col(sky[2])], [0, 0.65, 1])))
    c.drawCircle(1450, 690, 120, paint("#ffe2b0", 0.5, blur=30))
    r = random.Random(seed); x = -20 + (t * 3) % 40
    while x < W:
        w = r.uniform(60, 150); h = r.uniform(180, 460)
        c.drawRect(skia.Rect.MakeLTRB(x, 820 - h, x + w - 6, 830), paint("#14182a"))
        for wy in range(int(820 - h + 20), 800, 34):
            for wx in range(int(x + 12), int(x + w - 20), 26):
                if r.random() < 0.35: c.drawRect(skia.Rect.MakeLTRB(wx, wy, wx + 10, wy + 14), paint("#ffe3a0", 0.5))
        x += w
    c.drawRect(skia.Rect.MakeLTRB(0, 830, W, H), paint(shader=linear((0, 830), (0, H), [col("#2b3557"), col("#0b0f1d")])))
    if water:
        for k in range(8): c.drawLine(0, 860 + k * 28, W, 860 + k * 28, paint("#ffd7a0", 0.05, stroke=3))


def bg_road(c, t, sky=("#7fb7ff", "#cfe6ff"), ground="#5f8a4a", snow=False):
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 560), paint(shader=linear((0, 0), (0, 560), [col(sky[0]), col(sky[1])])))
    for k, (x, h) in enumerate(((200, 120), (600, 170), (1100, 140), (1600, 190))):
        pa = skia.Path(); pa.moveTo(x - 400, 560); pa.quadTo(x, 560 - h * 2, x + 400, 560); pa.close(); c.drawPath(pa, paint(mixhex(ground, "#ffffff", 0.35 if not snow else 0.85)))
    c.drawRect(skia.Rect.MakeLTRB(0, 560, W, H), paint("#f4f6f9" if snow else ground))
    poly(c, [(860, 560), (1060, 560), (1700, H), (220, H)], paint("#4a4d55"))
    for k in range(8):
        u = ((k / 8) + t * 0.6) % 1; y0 = 560 + (H - 560) * u ** 2; y1 = 560 + (H - 560) * min(1, (u + 0.05)) ** 2
        c.drawLine(960, y0, 960, y1, paint("#ffffff", 0.9, stroke=2 + 14 * u))
    for sx in (-1, 1):
        c.drawLine(960 + sx * 100, 560, 960 + sx * 740, H, paint("#ffffff", 0.8, stroke=6))


def bg_canal(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, 600), [col("#8ec5ff"), col("#f7e3c4")])))
    r = random.Random(7); x = -10
    while x < W:
        w = r.uniform(140, 260); h = r.uniform(300, 480); cc = r.choice(["#e0a77a", "#d98a6a", "#f0c98a", "#c97a5a", "#e8b6a0"])
        rr(c, x, 700 - h, x + w - 8, 720, 0, paint(cc))
        for row in range(int(h // 90)):
            for k in range(int(w // 60)):
                xx = x + 20 + k * 60; yy = 700 - h + 40 + row * 90
                pa = skia.Path(); pa.addRoundRect(skia.Rect.MakeLTRB(xx, yy, xx + 26, yy + 50), 13, 13); c.drawPath(pa, paint("#5a3a2a", 0.8))
        x += w
    c.drawRect(skia.Rect.MakeLTRB(0, 720, W, H), paint(shader=linear((0, 720), (0, H), [col("#2f8f8a"), col("#1a5a66")])))
    for k in range(14):
        y = 740 + k * 24; c.drawLine((k * 140 + t * 40) % W - 100, y, (k * 140 + t * 40) % W + 60, y, paint("#ffffff", 0.25, stroke=4))


def bg_steps(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, 500), [col("#9cc9ff"), col("#fbe7c9")])))
    rr(c, 760, 120, 1160, 420, 0, paint("#efe2c9"))
    for sx in (-1, 1):
        rr(c, 960 + sx * 160 - 50, 60, 960 + sx * 160 + 50, 420, 0, paint("#e8d8b8"))
        poly(c, [(960 + sx * 160 - 55, 60), (960 + sx * 160 + 55, 60), (960 + sx * 160, 0)], paint("#c9b38a"))
    for k in range(22):
        y = 420 + k * 30; w = 260 + k * 38
        rr(c, 960 - w, y, 960 + w, y + 30, 0, paint(mixhex("#f6ead2", "#d8c29a", (k % 2) * 0.5 + k / 60)))
        c.drawLine(960 - w, y, 960 + w, y, paint("#b9a27a", 0.6, stroke=2))


def bg_mountains(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, 700), [col("#7ec2ff"), col("#e9f6ff")])))
    for (x, h, cc) in ((300, 520, "#8aa0b8"), (900, 620, "#9fb3c8"), (1500, 560, "#8aa0b8")):
        poly(c, [(x - 520, 760), (x, 760 - h), (x + 520, 760)], paint(cc))
        poly(c, [(x - 110, 760 - h + 120), (x, 760 - h), (x + 110, 760 - h + 120), (x + 40, 760 - h + 100), (x - 30, 760 - h + 130)], paint("#ffffff"))
    c.drawRect(skia.Rect.MakeLTRB(0, 740, W, H), paint(shader=linear((0, 740), (0, H), [col("#8fd16a"), col("#4f9a3f")])))


def bg_river(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, 600), [col("#a9c8d8"), col("#e8eef0")])))
    for k in range(9):
        x = k * 240 - 60; c.drawCircle(x, 520, 150, paint("#3f6a4a")); c.drawCircle(x + 120, 470, 120, paint("#4f7a56"))
    c.drawRect(skia.Rect.MakeLTRB(0, 560, W, H), paint(shader=linear((0, 560), (0, H), [col("#5a8aa0"), col("#2f5a70")])))
    for k in range(16):
        y = 590 + k * 30; c.drawLine((k * 170 + t * 60) % (W + 200) - 200, y, (k * 170 + t * 60) % (W + 200) - 60, y, paint("#ffffff", 0.22, stroke=4))


def bg_parliament(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#2a2f4a"), col("#c27a5a"), col("#f0b27a")], [0, 0.7, 1])))
    base = 780
    rr(c, 200, base - 260, 1720, base, 0, paint("#1a1c28"))
    for k in range(30): rr(c, 220 + k * 50, base - 240, 236 + k * 50, base - 40, 0, paint("#ffd38a", 0.25))
    rr(c, 1460, base - 640, 1580, base, 0, paint("#1a1c28")); poly(c, [(1450, base - 640), (1590, base - 640), (1520, base - 760)], paint("#1a1c28"))
    c.drawCircle(1520, base - 540, 40, paint("#ffe7a8"))
    ang = t * 0.05; c.drawLine(1520, base - 540, 1520 + 30 * math.sin(ang), base - 540 - 30 * math.cos(ang), paint(INK, 1, stroke=5))
    rr(c, 300, base - 420, 380, base - 200, 0, paint("#1a1c28"))
    c.drawRect(skia.Rect.MakeLTRB(0, base, W, H), paint(shader=linear((0, base), (0, H), [col("#2b3557"), col("#0b0f1d")])))


def bg_night(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#0b1022"), col("#1d2747")])))
    c.drawCircle(1600, 180, 60, paint("#fff3c4")); c.drawCircle(1625, 165, 60, paint("#0b1022"))
    for k in range(6):
        x = k * 330 - 40; rr(c, x, 380, x + 300, 860, 0, paint("#161c33"))
        for wy in range(420, 820, 70):
            for wx in range(int(x + 30), int(x + 270), 70):
                c.drawRect(skia.Rect.MakeLTRB(wx, wy, wx + 30, wy + 40), paint("#ffe3a0", 0.06 if (wx + wy) % 3 else 0.35))
    c.drawRect(skia.Rect.MakeLTRB(0, 860, W, H), paint("#2a2f3a"))


BACK = {"intro": lambda c, t: bg_studio(c, t), "sg": lambda c, t: bg_skyline(c, t, ("#1d2a4d", "#c4566a", "#f2a65a")),
        "ca": lambda c, t: bg_skyline(c, t, ("#0f2440", "#5a7fb0", "#d9e8f5"), seed=11), "de": lambda c, t: bg_road(c, t),
        "es": lambda c, t: bg_skyline(c, t, ("#3aa0e8", "#9ad4ff", "#ffe2a8"), seed=21), "ve": bg_canal, "ro": bg_steps,
        "us": lambda c, t: bg_studio(c, t, "#24304a", "#141b2e", "#080b14"), "ch": bg_mountains,
        "cow": lambda c, t: bg_road(c, t, ("#8fc3ff", "#e3f1ff"), "#6aa84f"), "fish": bg_river, "bonus": bg_parliament,
        "fi": lambda c, t: bg_road(c, t, ("#9fb8d8", "#e8f0fa"), "#cfd8e3", snow=True), "glass": bg_night,
        "names": lambda c, t: bg_studio(c, t, "#3a2a4a", "#1d1830", "#0d0a16"), "outro": lambda c, t: bg_studio(c, t)}

# hero per segment (drawn big at the left/centre), icon names for each "step"
ICONS = {
    "sg": ["gum", "shop_x", "litter", "train", "hand", "question", "sparkle", "pharmacy", "cane"],
    "ca": ["bucket", "doc_currency", "coin_1", "coin_5", "coin_10", "coin_d1", "coin_d2", "hand", "wheelbarrow", "penny_x", "coin_1", "receipts"],
    "de": ["speedo", "question", "fuel_empty", "nostop", "wrench", "fuel_pump", "exclaim", "jerrycan"],
    "es": ["sun", "shirt", "shirtless", "bus", "police", "umbrella", "runner"],
    "ve": ["pigeon", "seed_bag", "building_crack", "square", "closed"],
    "ro": ["steps", "gelato", "hand", "sit_x", "arrows", "whistle", "washing", "gelato_euro"],
    "us": ["spot", "redcross", "kit", "gavel", "text_rc", "text_gc", "shield", "dove", "greencross"],
    "ch": ["gp", "gp2", "doc_ch", "gp2", "hearts", "sad", "gp_alone"],
    "cow": ["doc_uk", "cow", "exclaim", "horseshoe", "steam", "warn", "check", "car"],
    "fish": ["doc_salmon", "question", "laugh", "box_fish", "net", "eel", "scales", "coat_man", "walk"],
    "bonus": ["scroll", "helmet", "calendar", "knight"],
    "fi": ["money", "calendar_money", "diamond", "speed50", "trophy", "sausage"],
    "glass": ["cal_sun", "smash"],
    "names": ["register", "committee", "book", "form"],
    "outro": ["recap1", "recap2", "recap3", "comment", "comment", "bell", "wave"],
}


def hero(c, sid, t, u, k):
    bob = 6 * math.sin(t * 1.6)
    if sid == "sg":
        gum_big = eback(prog(u, 0.2, 0.5))
        c.save(); c.translate(700, 520 + bob); c.scale(2.6 * gum_big, 2.6 * gum_big); gum(c); c.restore()
        if k >= 2:
            c.save(); c.translate(700, 520); c.scale(eback(prog(t, SEG_STEPS["sg"][1], 0.35)) * 1.9, eback(prog(t, SEG_STEPS["sg"][1], 0.35)) * 1.9); nosign(c, 110); c.restore()
    elif sid == "ca":
        for k2 in range(26):
            r = random.Random(k2); x = 560 + r.uniform(-260, 260); y = 760 - (k2 // 6) * 40 + r.uniform(-8, 8)
            ap = eout(prog(u, 0.1 + k2 * 0.03, 0.3))
            if ap <= 0: continue
            c.save(); c.translate(x, y - 300 * (1 - ap)); c.scale(0.7, 0.7)
            nm = ["coin_1", "coin_5", "coin_10", "coin_d1", "coin_d2"][k2 % 5]; icon(c, nm, t); c.restore()
    elif sid == "de":
        empty = k >= 3
        jig = 0 if empty else 3 * math.sin(t * 30)
        car(c, 760, 760 + jig, 1.25, "#2f5fd1")
        if empty:
            fl = 0.5 + 0.5 * math.sin(t * 8)
            for sx in (-1, 1): c.drawCircle(760 + sx * 255, 760, 18, paint("#ffb020", fl))
            if k >= 4:
                c.save(); c.translate(1020, 880); c.scale(0.55, 0.55); poly(c, [(0, -90), (95, 80), (-95, 80)], paint(RED, 1, stroke=18)); c.restore()
    elif sid == "es":
        c.save(); c.translate(1450 - 900, 260); c.scale(1.2, 1.2); icon(c, "sun", t); c.restore()
        c.save(); c.translate(700, 640 + bob); c.scale(2.6, 2.6); person(c, BLUE, shirt=(k < 3 or k >= 5)); c.restore()
    elif sid == "ve":
        for k2 in range(9):
            r = random.Random(k2 + 40)
            x = 380 + k2 * 75 + 12 * math.sin(t * 2 + k2); y = 640 + r.uniform(-20, 20)
            fly = 0.0 if k < 3 else eio(prog(t - k2 * 0.08, SEG_STEPS["ve"][2], 1.2))
            pigeon(c, x + 300 * fly, y - 520 * fly, 0.9, t + k2, flip=k2 % 2 == 0)
    elif sid == "ro":
        sit = k >= 2 and k < 4
        c.save(); c.translate(760, 650 + bob * 0.3); c.scale(2.0, 2.0); person(c, "#e8473b"); c.restore()
        if k >= 5:
            c.save(); c.translate(1040, 520); c.scale(1.2, 1.2); icon(c, "whistle", t); c.restore()
    elif sid == "us" and k == 0:
        c.save(); c.translate(720, 540 + bob); c.scale(2.2 * eback(prog(u, 0.2, 0.5)), 2.2 * eback(prog(u, 0.2, 0.5)))
        rr(c, -95, -95, 95, 95, 18, paint("#2a2f3e")); text_c(c, "?", 0, 45, skia.Font(TF_BLACK, 130), "#ffffff", 0.8); c.restore()
    elif sid == "us":
        a = eout(prog(t, SEG_STEPS["us"][0] if "us" in SEG_STEPS else u, 0.6))
        c.drawCircle(720, 540, 380, paint(shader=radial(720, 540, 380, [col("#ffffff", 0.25 * a), col("#ffffff", 0)])))
        c.save(); c.translate(720, 540); c.scale(2.6 * eback(prog(u, 0.6, 0.6)), 2.6 * eback(prog(u, 0.6, 0.6)))
        icon(c, "redcross" if k < 8 else "greencross"); c.restore()
    elif sid == "ch":
        guinea(c, 640, 700, 2.0, t)
        if k >= 2:
            ap = eback(prog(t, SEG_STEPS["ch"][1], 0.5)); guinea(c, 960 + 200 * (1 - ap), 730, 1.7 * clamp(ap, 0, 1.2), t + 1, flip=True)
        if k >= 5: heart(c, 800, 470 + bob, 0.8)
    elif sid == "cow":
        cow(c, 680, 640, 1.25, t)
        if k >= 2:
            c.save(); c.translate(1080, 700); c.scale(1.6, 1.6); person(c, "#6b5a44"); c.restore()
            c.save(); c.translate(1130, 690); c.rotate(-20 + 10 * math.sin(t * 2))
            rr(c, -20, -40, 25, 30, 6, paint("#d9a441")); rr(c, -20, -50, 25, -35, 6, paint("#ffffff")); c.restore()
    elif sid == "fish":
        salmon(c, 720, 560 + bob, 1.9, t)
        if k >= 2:
            c.save(); c.translate(720, 560); c.rotate(-12); c.drawCircle(-60, -10, 140, paint("#ffffff", 0.08)); c.drawCircle(-60, -10, 140, paint("#1b1f27", 1, stroke=18))
            c.drawLine(40, 90, 150, 210, paint("#1b1f27", 1, stroke=26)); c.restore()
    elif sid == "bonus":
        c.save(); c.translate(720, 560 + bob); knight_helmet(c, 0, 0, 2.0); c.restore()
        if k >= 2: c.save(); c.translate(720, 560); c.scale(2.3, 2.3); nosign(c, 130); c.restore()
    elif sid == "fi":
        c.save(); c.translate(640, 520); c.scale(2.2, 2.2); icon(c, "speed50"); c.restore()
        car(c, 900 + ((t * 900) % 2600) - 1300, 860, 0.8, "#111827")
    elif sid == "glass":
        rr(c, 480, 420, 1000, 900, 40, paint(shader=linear((0, 420), (0, 900), [col("#3fa36b"), col("#1f6a45")])))
        for k2, cc in enumerate(("#2f9e5a", "#8a5a2a", "#ffffff")): c.drawCircle(600 + k2 * 140, 470, 34, paint("#0d1a12"))
        text_c(c, "ALTGLAS", 740, 680, skia.Font(TF_BLACK, 70), "#ffffff", 0.9, 8)
        if k >= 1: c.save(); c.translate(740, 300 + 20 * math.sin(t * 3)); c.scale(1.5, 1.5); icon(c, "smash", t); c.restore()
        else: bottle(c, 740, 280 + 15 * math.sin(t * 2), 1.4, "#2f9e5a")
    elif sid == "names":
        c.save(); c.translate(700, 540 + bob); c.rotate(-4)
        rr(c, -330, -200, 330, 200, 24, paint("#ffffff")); rr(c, -330, -200, 330, -120, 24, paint("#5a4a8a"))
        text_c(c, "BIRTH CERTIFICATE", 0, -145, skia.Font(TF_BLACK, 40), "#ffffff", 1, 4)
        text_c(c, "FIRST NAME:", -150, -40, skia.Font(TF_BOLD, 34), "#5d636c")
        nm = ["  ?", "ANNA", "ANNA", "ANNA", "ANNA"][min(k, 4)]
        text_c(c, nm, 120, -40, skia.Font(TF_BLACK, 46), INK)
        c.drawLine(10, -25, 300, -25, paint("#9aa0a8", 1, stroke=3))
        if k >= 1: c.save(); c.translate(220, 100); c.rotate(-10); stamp_raw(c, "APPROVED", 40, GREEN, 1.0); c.restore()
        c.restore()
    elif sid == "outro":
        pass


def stamp_raw(c, txt, size, colr, a):
    f = skia.Font(TF_BLACK, size); w = f.measureText(txt) + size * 0.8
    c.drawRoundRect(skia.Rect.MakeLTRB(-w / 2, -size * 0.85, w / 2, size * 0.45), 14, 14, paint(colr, a, stroke=8))
    text_c(c, txt, 0, size * 0.1, f, colr, a)


def detail_card(c, sid, t, k):
    if sid not in ICONS or k == 0: return
    steps = SEG_STEPS.get(sid, [])
    ts = steps[k - 1]
    names = ICONS[sid]
    nm = names[min(k - 1, len(names) - 1)]
    ap = eback(prog(t, ts, 0.35))
    if sid == "outro" and nm.startswith("recap"):
        c.save(); c.translate(960, 520); c.scale(clamp(ap, 0, 1.2) * 1.6, clamp(ap, 0, 1.2) * 1.6); icon(c, nm, t); c.restore(); return
    if sid == "outro":
        c.save(); c.translate(960, 520); c.scale(clamp(ap, 0, 1.2) * 2.4, clamp(ap, 0, 1.2) * 2.4); icon(c, nm, t); c.restore(); return
    x, y = 1480, 470
    c.save(); c.translate(x, y + 5 * math.sin(t * 2)); sc = clamp(ap, 0, 1.15); c.scale(sc, sc)
    rr(c, -205, -195, 205, 215, 40, paint("#000000", 0.35, blur=22))
    rr(c, -200, -200, 200, 200, 40, paint("#ffffff", 0.96))
    c.save(); c.scale(1.55, 1.55); icon(c, nm, t); c.restore()
    c.restore()


def intro_scene(c, t, k):
    bg_studio(c, t)
    steps = SEG_STEPS["intro"]
    push = 1 + 0.004 * t
    c.save(); c.translate(W / 2, H / 2); c.scale(push, push); c.translate(-W / 2, -H / 2)
    ta = eout(prog(t, 0.2, 0.6))
    text_c(c, "THE 10 STRANGEST LAWS", 960, 170 - 30 * (1 - ta), skia.Font(TF_BLACK, 96), "#FFFFFF", ta, 4)
    text_c(c, "STILL ON THE BOOKS", 960, 245, skia.Font(TF_BOLD, 46), GOLD, eout(prog(t, 0.5, 0.4)), 14)
    op = 1.0 if k >= 2 else 0.0
    if k < 3:
        law_book(c, 960, 600, eback(prog(t, 0.0, 0.6)), 1.0, op)
        rl = steps[0]
        g = prog(t, rl - 0.35, 0.35)
        ang = lerp(-50, 8, eio(g)) if t < rl else 8 - 6 * math.exp(-(t - rl) * 8) * math.cos((t - rl) * 30)
        gavel(c, 1430, 500, 1.1, ang, eout(prog(t, rl - 0.6, 0.25)))
    else:
        # countdown cards 10..1 fanned
        for i in range(10):
            ap = eback(prog(t, steps[2] + i * 0.08, 0.35))
            if ap <= 0: continue
            x = 262 + i * 155; y = 470 + 20 * math.sin(t * 2 + i)
            c.save(); c.translate(x, y); c.rotate(-6 + (i % 3) * 6); c.scale(clamp(ap, 0, 1.2), clamp(ap, 0, 1.2))
            rr(c, -65, -90, 65, 90, 16, paint(CREAM)); text_c(c, f"#{10 - i}", 0, 22, skia.Font(TF_BLACK, 56), "#7a2a22")
            c.restore()
        if k >= 4:
            for i, nm in enumerate(("gum", "pigeon", "salmon_i")):
                ap = eback(prog(t, steps[3] + i * 0.4, 0.35))
                if ap <= 0: continue
                c.save(); c.translate(560 + i * 400, 740); c.scale(clamp(ap, 0, 1.2) * 0.8, clamp(ap, 0, 1.2) * 0.8)
                rr(c, -120, -110, 120, 110, 30, paint("#ffffff", 0.95)); icon(c, nm, t); c.restore()
        if k >= 5:
            ap = eback(prog(t, steps[4], 0.4))
            c.save(); c.translate(1720, 740); c.scale(clamp(ap, 0, 1.2) * 0.9, clamp(ap, 0, 1.2) * 0.9); glyph(c, "#1?", RED); c.restore()
    c.restore()


def big_card(c, t, txt, ts):
    bg_studio(c, t, "#2a1d10", "#140e08", "#070503")
    u = prog(t, ts, 0.35)
    for k in range(16):
        a = k * math.pi / 8 + t * 0.15
        c.drawLine(960, 540, 960 + 1400 * math.cos(a), 540 + 1400 * math.sin(a), paint(GOLD, 0.05, stroke=60))
    sc = 1.7 - 0.7 * eout(u)
    c.save(); c.translate(960, 560); c.scale(sc, sc)
    f = fit_font(TF_BLACK, txt, 1500, 330 if len(txt) < 5 else 200)
    c.drawCircle(0, -40, 320, paint(GOLD, 0.12 * u, blur=40))
    text_c(c, txt, 0, f.getSize() * 0.36, f, GOLD, u)
    c.restore()


def pills(c, t):
    cur = active(EV["pill"], t)
    if not cur: return
    ts, txt = cur
    if crossed(ts, t) or active(BIGS, t) and active(BIGS, t)[0] <= t < big_end(active(BIGS, t)[0]): return
    nxt = [x for (x, _) in EV["pill"] if x > ts]
    tout = min(nxt[0] if nxt else 1e9, next_seg_time(ts)) - 0.1
    a = 1 - prog(t, tout, 0.15); sc = eback(prog(t, ts, 0.25))
    f = skia.Font(TF_MONO, 38)
    w = sum(f.measureText(ch) + 3 for ch in txt) + 60
    c.save(); c.translate(960, 330 if False else 120); c.scale(sc, sc)
    rr(c, -w / 2 + 3, -34 + 8, w / 2 + 3, 34 + 8, 34, paint("#000000", 0.35 * a, blur=10))
    rr(c, -w / 2, -36, w / 2, 36, 36, paint(GOLD, a))
    text_c(c, txt, 0, 13, f, INK, a, 3)
    c.restore()


def stamps(c, t):
    cur = active(EV["stamp"], t)
    if not cur: return
    ts, txt = cur
    nxt = [x for (x, _) in EV["stamp"] if x > ts]
    tout = min(ts + 3.2, (nxt[0] if nxt else 1e9) - 0.05, next_seg_time(ts) - 0.05)
    if t > tout + 0.3 or crossed(ts, t): return
    a = prog(t, ts, 0.05) * (1 - prog(t, tout, 0.25))
    sc = 1 + 0.6 * (1 - eout(prog(t, ts, 0.18)))
    seg = seg_at(t)[1]
    x, y = (1480, 860) if seg not in ("intro",) else (620, 760)
    c.save(); c.translate(x, y); c.rotate(-7); c.scale(sc, sc)
    colr = RED if not txt.startswith(("MEDICAL", "+1", "AT LEAST")) else GREEN
    f = fit_font(TF_BLACK, txt, 640, 64)
    w = f.measureText(txt) + 50
    rr(c, -w / 2, -58, w / 2, 26, 14, paint("#ffffff", 0.9 * a))
    rr(c, -w / 2, -58, w / 2, 26, 14, paint(colr, a, stroke=8))
    text_c(c, txt, 0, f.getSize() * 0.0 + 2, f, colr, a)
    c.restore()


def notes(c, t):
    cur = active(EV["note"], t)
    if not cur: return
    ts, txt = cur
    if crossed(ts, t): return
    a = prog(t, ts, 0.4) * (1 - prog(t, next_seg_time(ts) - 0.4, 0.3))
    c.drawString(txt, 60, 1062, skia.Font(TF_REG, 24), paint("#FFFFFF", 0.6 * a))


def subtitles(c, t):
    for i, ph in enumerate(P):
        nxt = P[i + 1]["t0"] if i + 1 < len(P) else DUR
        if not (ph["t0"] - 0.05 <= t < nxt): continue
        a = prog(t, ph["t0"], 0.1) * (1 - prog(t, nxt - 0.1, 0.1))
        f = skia.Font(TF_BOLD, 48)
        words = ph["words"]
        tw = sum(f.measureText(w["w"]) for w in words) + f.measureText(" ") * (len(words) - 1)
        if tw > 1700: f = skia.Font(TF_BOLD, 48 * 1700 / tw); tw = 1700
        x = W / 2 - tw / 2; y = 1005
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 26, y - 50, x + tw + 26, y + 18), 16, 16, paint("#000000", 0.5 * a))
        for w in words:
            on = t >= w["t0"]
            c.drawString(w["w"], x, y, f, paint(GOLD if w["kw"] else "#FFFFFF", a * (1.0 if on else 0.35)))
            x += f.measureText(w["w"] + " ")


def scene(c, t):
    ts, sid = seg_at(t)
    u = t - ts
    steps = SEG_STEPS.get(sid, [])
    k = sum(1 for s in steps if s <= t)
    # big interstitial card overrides until the next segment starts
    b = active(BIGS, t)
    if b and b[0] <= t < big_end(b[0]):
        big_card(c, t, b[1], b[0]); return
    if sid == "intro":
        intro_scene(c, t, k); return
    # camera: slow push + punch on each step
    punch = 1.0
    for s in steps:
        d = t - s
        if 0 <= d < 0.3: punch += 0.012 * (1 - d / 0.3) ** 2
    zoom = (1 + 0.05 * min(u / 40, 1)) * punch
    c.save(); c.translate(W / 2, H / 2); c.scale(zoom, zoom); c.translate(-W / 2 + 8 * math.sin(t * 0.3), -H / 2)
    BACK[sid](c, t)
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, 260), [col("#000000", 0.35), col("#000000", 0)])))
    hero(c, sid, t, u, k)
    c.restore()
    detail_card(c, sid, t, k)


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    scene(c, t)
    # transition flash/wipe at segment changes
    for (ts, _) in SEGS[1:] + [(x, "") for (x, _) in BIGS]:
        d = t - ts
        if -0.2 <= d < 0.25:
            q = (d + 0.2) / 0.45
            c.save(); c.translate(W / 2, H / 2); c.rotate(18)
            c.drawRect(skia.Rect.MakeXYWH(lerp(-2600, 2600, eio(q)) - 700, -1600, 1400, 3200), paint(GOLD, 0.9))
            c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H / 2, 1250, [col("#000000", 0), col("#000000", 0.35)], [0.6, 1])))
    pills(c, t); stamps(c, t); notes(c, t); subtitles(c, t)
    fade = min(prog(t, 0, 0.4), 1 - prog(t, DUR - 0.8, 0.8))
    if fade < 1: c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 1 - fade))
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("riser", 0.0)]
    for (ts, _) in SEGS[1:]: ev.append(("whoosh", ts - 0.1))
    for (ts, _) in BIGS: ev += [("whoosh", ts - 0.15), ("hit", ts + 0.05)]
    for (ts, _) in EV["step"]: ev.append(("pop", ts))
    for (ts, _) in EV["stamp"]: ev.append(("hit", ts))
    return sorted(ev, key=lambda e: e[1])


if __name__ == "__main__":
    if sys.argv[1] == "still":
        from PIL import Image
        out = os.environ.get("LF_STILLS", D)
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(f"{out}/still_{ts}.png")
        sys.exit()
    f0, f1, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    tmp = out.replace(".mp4", ".tmp.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        pr.stdin.write(frame(fi / FPS).tobytes())
    pr.stdin.close()
    if pr.wait() == 0:
        os.rename(tmp, out)

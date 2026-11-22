# HIW22 — "Why doesn't your stomach digest itself?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-23):
#  - Live Science, "Why doesn't stomach acid burn through our stomachs?" (2026-01-10): hydrochloric acid is "strong enough
#    to dissolve metal"; lining cells make "a very thick, sticky layer of mucus which is alkaline and buffers the acid",
#    "rich in bicarbonate", continually renewed; small breaks let acid in -> inflammation and ulcers; causes: NSAID
#    painkillers (ibuprofen, naproxen) reduce mucus + bicarbonate, H. pylori bacteria degrade the mucus, smoking, alcohol.
#  - Geophysical Institute (Univ. of Alaska) "Why doesn't the stomach digest itself?": zinc dropped in gastric acid
#    dissolves; the lining "completely replaces itself in three days" (we say "every few days" — figures vary 3-5 days).
#  - Bicarbonate = the same chemical family as baking soda (sodium bicarbonate) -> "a baking soda kind of base".
#  Health topic: "Educational only, not medical advice." footnote.
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
ACID = "#C6F03C"; ACID_D = "#7FB31A"; STOM = "#F08A9A"; STOM_D = "#C24F66"; GEL = "#BFE6FF"; BASE = "#3D8BFF"
METAL = "#AEB6C2"; MEAT = "#C2413F"; GREEN = "#1fb98a"; SORE = "#FF3B30"; GERM = "#9B6BFF"


def _txt(i): return " ".join(w["w"] for w in P[i]["words"]).lower()


def ph(s, after=0):
    for i in range(after, len(P)):
        if _txt(i).startswith(s.lower()):
            return i
    raise KeyError(s)


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


STRONG = p0(ph("your stomach acid")); METt = kw(ph("to dissolve")); MEATt = kw(ph("and it breaks")); NOPROB = p0(ph("no problem"))
WIPE1 = p0(ph("okay")) - 0.3; SECRET = p0(ph("the secret")); MUC = kw(ph("a thick"))
COAT = p0(ph("it coats")); BASEt = kw(ph("and it's full")); CANCEL = p0(ph("that cancels"))
TOUCH = kw(ph("so the acid")); REBUILD = p0(ph("and the wall")); FRESH = p0(ph("a fresh")); DAYS = kw(ph("every few"))
WIPE2 = p0(ph("when the shield")) - 0.3; BREAK = kw(ph("when the shield")); ULCER = kw(ph("that's an"))
PAIN = p0(ph("some painkillers")); GERMt = kw(ph("and a sneaky")); WEAR = p0(ph("can wear"))
SO = p0(len(P) - 1)
WL = 0.32
IMPACTS = [METt, MUC, ULCER]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1, ph_=0.0):
    return math.sin(2 * math.pi * k * t / DUR + ph_)


def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#221519"), col("#140c0f"), col("#080506")], [0, 0.55, 1])))
    c.drawCircle(800 + 30 * lw(t), 720, 520, paint(shader=radial(800, 720, 520, [col(ACID, 0.08), col(ACID, 0)])))
    c.drawCircle(220, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1450, 600, [col(STOM, 0.08), col(STOM, 0)])))


# ---------------- stomach organ ----------------
def stomach_path():
    p = skia.Path()
    p.moveTo(-60, -330)                    # food pipe in
    p.lineTo(20, -330)
    p.cubicTo(30, -250, 60, -220, 140, -230)
    p.cubicTo(300, -250, 360, -60, 300, 90)
    p.cubicTo(240, 230, 60, 300, -120, 260)
    p.cubicTo(-210, 240, -250, 200, -300, 220)   # out to the gut
    p.lineTo(-310, 150)
    p.cubicTo(-240, 120, -190, 150, -140, 140)
    p.cubicTo(-40, 120, -20, 20, -50, -100)
    p.cubicTo(-70, -200, -70, -260, -60, -330)
    p.close()
    return p


def stomach(c, t, x, y, s, a=1.0, squish=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s * (1 + 0.03 * squish), s * (1 - 0.03 * squish))
    sp = stomach_path()
    c.drawPath(sp, paint("#000000", 0.35 * a, blur=22))
    c.drawPath(sp, paint(shader=radial(80, -80, 420, [col("#FFB3BE", a), col(STOM, a), col(STOM_D, a)], [0, 0.55, 1])))
    # acid pool inside (cut-away window)
    c.save(); c.clipPath(sp, doAntiAlias=True)
    lev = 40 + 10 * math.sin(t * 2.2)
    pool = skia.Path(); pool.moveTo(-400, lev)
    for xx in range(-400, 420, 20):
        pool.lineTo(xx, lev + 10 * math.sin(xx * 0.03 + t * 3))
    pool.lineTo(420, 400); pool.lineTo(-400, 400); pool.close()
    c.drawPath(pool, paint(shader=linear((0, lev), (0, 300), [col(ACID, 0.9 * a), col(ACID_D, 0.95 * a)])))
    for k in range(14):
        rr = random.Random(50 + k)
        u = ((t / (DUR / 6)) + rr.random()) % 1.0
        bx = rr.uniform(-120, 260); by = lerp(260, lev, u)
        c.drawCircle(bx, by, rr.uniform(5, 12), paint("#F4FFD0", 0.8 * a * math.sin(math.pi * u), stroke=2.5))
    c.restore()
    # folds + gloss
    for k in range(4):
        f = skia.Path(); f.moveTo(-20 + k * 70, -170 + k * 30); f.quadTo(60 + k * 60, -60 + k * 20, 0 + k * 50, -10 + k * 10)
        c.drawPath(f, paint(STOM_D, 0.35 * a, stroke=6))
    c.drawPath(sp, paint("#FFD6DC", 0.6 * a, stroke=4))
    g = skia.Path(); g.moveTo(170, -200); g.cubicTo(270, -170, 300, -80, 290, 0)
    c.drawPath(g, paint("#ffffff", 0.5 * a, stroke=14, blur=4))
    c.restore()


def scene_hook(c, t):
    bg_dark(c, t)
    stomach(c, t, 520, 1060 + 10 * lw(t, 2), 1.2, squish=lw(t, 4))


# ---------------- open: acid vs metal and meat ----------------
def nut(c, x, y, s, rot, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    h = skia.Path()
    for k in range(6):
        an = math.radians(60 * k + 30)
        (h.moveTo if k == 0 else h.lineTo)(70 * math.cos(an), 70 * math.sin(an))
    h.close()
    c.drawPath(h, paint("#000000", 0.3 * a, blur=10))
    c.drawPath(h, paint(shader=linear((-70, -70), (70, 70), [col("#E8EDF3", a), col(METAL, a), col("#6E7784", a)])))
    c.drawCircle(0, 0, 30, paint("#3a3f47", a)); c.drawCircle(0, 0, 30, paint("#ffffff", 0.5 * a, stroke=3))
    c.restore()


def steak(c, x, y, s, rot, a, split=0.0):
    if a <= 0: return
    for k in range(5):
        rr = random.Random(70 + k)
        dx = split * rr.uniform(-120, 120); dy = split * rr.uniform(-60, 80)
        sc = 1.0 if split <= 0 else lerp(1, 0.45, split)
        c.save(); c.translate(x + dx, y + dy); c.rotate(rot + k * 70 * split); c.scale(s * sc, s * sc)
        if split <= 0 and k > 0:
            c.restore(); continue
        p = skia.Path(); p.moveTo(-110, -40); p.cubicTo(-60, -90, 90, -80, 120, -20); p.cubicTo(140, 50, 40, 80, -30, 70); p.cubicTo(-120, 60, -140, 0, -110, -40)
        c.drawPath(p, paint("#000000", 0.3 * a, blur=10))
        c.drawPath(p, paint(shader=radial(-20, -20, 160, [col("#E0605A", a), col(MEAT, a), col("#8E2A2A", a)])))
        c.drawPath(p, paint("#F6E3D6", 0.9 * a, stroke=10))
        f = skia.Path(); f.moveTo(-60, -20); f.quadTo(0, 10, 70, -10)
        c.drawPath(f, paint("#F6E3D6", 0.6 * a, stroke=6))
        c.restore()


def acid_tank(c, t, a, fizz=0.0):
    """big glowing acid pool filling the lower screen."""
    if a <= 0: return
    lev = 1060 + 8 * math.sin(t * 2)
    p = skia.Path(); p.moveTo(-50, lev)
    for xx in range(-50, W + 60, 20):
        p.lineTo(xx, lev + 12 * math.sin(xx * 0.02 + t * 3))
    p.lineTo(W + 50, H + 50); p.lineTo(-50, H + 50); p.close()
    c.drawPath(p, paint(ACID, 0.35 * a, blur=40))
    c.drawPath(p, paint(shader=linear((0, lev), (0, 1700), [col(ACID, 0.92 * a), col(ACID_D, 0.95 * a), col("#3d5a0a", a)])))
    for k in range(int(18 + 40 * fizz)):
        rr = random.Random(200 + k)
        u = ((t * (0.5 + 0.8 * fizz) * rr.uniform(0.6, 1.3)) + rr.random()) % 1.0
        bx = rr.uniform(120, 880) if k >= 18 else rr.uniform(60, 1020)
        if k >= 18: bx = 495 + rr.uniform(-140, 140)
        by = lerp(1600, lev, u)
        c.drawCircle(bx, by, rr.uniform(5, 14), paint("#F4FFD0", 0.75 * a * math.sin(math.pi * u), stroke=3))


def scene_open(c, t):
    bg_dark(c, t)
    z = eio(prog(t, STRONG - 0.2, 0.6))
    out = 1 - prog(t, WIPE1 - 0.1, 0.2)
    if z < 1:
        c.saveLayerAlpha(None, int(255 * (1 - z)))
        scene_hook(c, t) if t < 0.1 else stomach(c, t, 520, 1060 + 10 * lw(t, 2), 1.2 + 1.5 * z, squish=lw(t, 4))
        c.restore()
    acid_tank(c, t, z * out, fizz=window(t, METt - 0.1, MEATt + 0.3, 0.2, 0.3))
    # metal nut drops, fizzes, shrinks
    na = eout(prog(t, METt - 0.5, 0.4)) * (1 - prog(t, MEATt - 0.2, 0.3)) * out
    if na > 0:
        drop = eout(prog(t, METt - 0.5, 0.5))
        shrink = eio(prog(t, METt, 1.2))
        nut(c, 495 + 6 * math.sin(t * 20) * shrink, lerp(700, 1180, drop), lerp(1.3, 0.55, shrink), t * 40, na)
    # steak sinks and breaks into bits
    ma = eout(prog(t, MEATt - 0.35, 0.3)) * out
    if ma > 0:
        drop = eout(prog(t, MEATt - 0.35, 0.5))
        sp = eio(prog(t, NOPROB - 0.1, 0.8))
        steak(c, 495, lerp(720, 1180, drop), 1.25, -8 + 5 * math.sin(t * 3), ma, split=sp)
    pill(c, t, "DIGEST ITSELF?", 495, 560, STOM_D, 0.35, STRONG - 0.05)
    pill(c, t, "STOMACH ACID", 495, 560, ACID_D, STRONG, METt - 0.05)
    pill(c, t, "DISSOLVES METAL", 495, 560, "#6E7784", METt, MEATt - 0.05)
    pill(c, t, "BREAKS DOWN MEAT", 495, 560, MEAT, MEATt, NOPROB - 0.05)
    pill(c, t, "NO PROBLEM", 495, 560, ACID_D, NOPROB, WIPE1 + 0.1)


# ---------------- lining cross-section ----------------
GEL_TOP = 960; CELL_TOP = 1110; L, R = 100, 890


def acid_drop(c, x, y, r, a):
    if a <= 0: return
    c.drawCircle(x, y, r * 1.8, paint(ACID, 0.25 * a, blur=8))
    for k in range(8):
        an = k * math.pi / 4
        c.drawLine(x, y, x + r * 1.45 * math.cos(an), y + r * 1.45 * math.sin(an), paint(ACID_D, a, stroke=4))
    c.drawCircle(x, y, r, paint(ACID, a))
    c.drawCircle(x - r * 0.3, y - r * 0.3, r * 0.3, paint("#ffffff", 0.6 * a))


def lining(c, t, a, gel=1.0, spread=1.0, base=0.0, cancel=0.0, renew=0.0, gap=0.0, sore=0.0, thin=0.0, dark=False):
    if a <= 0: return
    c.save()
    box = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(L, 700, R, 1440), 36, 36)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(L, 706, R, 1450), 36, 36), paint("#000000", 0.18 * a, blur=14))
    c.clipRRect(box, doAntiAlias=True)
    # acid zone
    c.drawRect(skia.Rect.MakeLTRB(L, 700, R, CELL_TOP + 30), paint(shader=linear((0, 700), (0, 1100), [col("#E9FF9A", a), col(ACID, a)])))
    # wall cells (2 rows)
    for row in range(2):
        for k in range(-row, 9):
            cx = L + 14 + k * 88 + (44 if row else 0); cy = CELL_TOP + 20 + row * 150
            fresh = clamp(renew * 2.2 - (8 - max(k, 0)) * 0.12)
            colr = mixhex("#F2A3AE", "#FFC9D1", fresh)
            c.drawRoundRect(skia.Rect.MakeLTRB(cx - 4, cy, cx + 84, cy + 140), 26, 26, paint(colr, a))
            c.drawRoundRect(skia.Rect.MakeLTRB(cx - 4, cy, cx + 84, cy + 140), 26, 26, paint(STOM_D, 0.6 * a, stroke=3))
            c.drawCircle(cx + 40, cy + 70, 16, paint(STOM_D, 0.7 * a))
            if 0 < fresh < 1:
                c.drawRoundRect(skia.Rect.MakeLTRB(cx - 4, cy, cx + 84, cy + 140), 26, 26, paint("#ffffff", 0.6 * a * math.sin(math.pi * fresh)))
    # mucus gel
    th = (CELL_TOP - GEL_TOP) * gel * (1 - 0.6 * thin)
    if th > 2:
        top = CELL_TOP - th
        gp = skia.Path(); gp.moveTo(L - 10, CELL_TOP + 20)
        xs = list(range(L - 10, R + 20, 10))
        half = (R - L) / 2 * spread * 1.3
        for x in xs:
            g = eio(clamp((half + 30 - abs(x - 495)) / 90))
            if gap > 0:
                g *= 1 - gap * math.exp(-((x - 600) / 55) ** 2)
            y = lerp(CELL_TOP + 20, top + 8 * math.sin(x * 0.03 + t * 2.5), g)
            gp.lineTo(x, y)
        gp.lineTo(R + 20, CELL_TOP + 20); gp.close()
        c.drawPath(gp, paint(shader=linear((0, top), (0, CELL_TOP + 20), [col("#F2FAFF", 0.95 * a), col(GEL, 0.92 * a)])))
        c.drawPath(gp, paint("#ffffff", 0.8 * a, stroke=4))
        # base balls inside the gel
        if base > 0:
            for k in range(16):
                rr = random.Random(300 + k)
                bx = L + 30 + k * 50 + 8 * math.sin(t * 2 + k)
                if abs(bx - 495) > half: continue
                if gap > 0.3 and abs(bx - 600) < 70: continue
                by = top + 22 + (k % 3) * (th - 44) / 2 + 5 * math.cos(t * 3 + k)
                q = eback(clamp(base * 2.5 - rr.random()))
                c.drawCircle(bx, by, 13 * q, paint(BASE, 0.9 * a)); c.drawCircle(bx - 4, by - 4, 4 * q, paint("#ffffff", 0.7 * a))
    # falling acid drops: cancelled at the gel top (sparkle) or, with a gap, reaching the cells
    if cancel > 0 or gap > 0:
        for k in range(10):
            rr = random.Random(400 + k)
            u = ((t * 0.9 + rr.random()) % 1.0)
            x = L + 60 + k * 76
            in_gap = gap > 0.3 and abs(x - 600) < 80
            yend = (CELL_TOP + 10) if in_gap else (CELL_TOP - th + 10)
            y = lerp(720, yend, min(1, u * 1.3))
            if u * 1.3 < 1:
                acid_drop(c, x, y, 13, a * max(cancel, gap))
            else:
                v = (u * 1.3 - 1) / 0.3
                for j in range(6):
                    an = j * math.pi / 3
                    c.drawCircle(x + 30 * v * math.cos(an), yend + 30 * v * math.sin(an) - 10, 5, paint("#ffffff" if not in_gap else SORE, (1 - v) * a * max(cancel, gap)))
    # ulcer
    if sore > 0:
        c.drawCircle(600, CELL_TOP + 40, 110 * sore, paint(SORE, 0.45 * a, blur=26))
        cr = skia.Path(); cr.addOval(skia.Rect.MakeLTRB(600 - 85 * sore, CELL_TOP - 10, 600 + 85 * sore, CELL_TOP + 90 * sore))
        c.drawPath(cr, paint("#8E1B22", a)); c.drawPath(cr, paint(SORE, a, stroke=6))
    c.restore()
    c.drawRRect(box, paint("#ffffff" if dark else INK, 0.15 * a, stroke=3))
    # side labels
    f = skia.Font(TF_MONO, 22)
    lab = INK if not dark else "#ffffff"
    c.drawString("ACID", L + 24, 744, f, paint(lab, 0.55 * a))
    c.drawString("WALL", L + 24, 1420, f, paint(lab, 0.55 * a))


def calendar(c, t, x, y, s, a, flip):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -90, 90, 100), 20, 20, paint("#000000", 0.2 * a, blur=10))
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -90, 90, 100), 20, 20, paint("#ffffff", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -90, 90, -30), 20, 20, paint(STOM_D, a))
    c.drawRect(skia.Rect.MakeLTRB(-90, -50, 90, -30), paint(STOM_D, a))
    for k in range(3):
        for j in range(4):
            c.drawRoundRect(skia.Rect.MakeLTRB(-72 + j * 38, -14 + k * 36, -46 + j * 38, 10 + k * 36), 6, 6, paint("#E4E1DB", a))
    # page flip
    u = flip % 1.0
    c.save(); c.scale(1, 1 - 2 * min(u, 1 - u) if u > 0 else 1)
    c.restore()
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -90, 90, lerp(-30, 100, u)), 20, 20, paint("#F7E4E8", a * math.sin(math.pi * u)))
    c.restore()


def scene_lab(c, t):
    studio_white(c)
    a = eout(prog(t, WIPE1, 0.4))
    gel = eout(prog(t, MUC - 0.15, 0.45))
    spread = lerp(0.35, 1.0, eio(prog(t, COAT - 0.1, 0.7)))
    base = prog(t, BASEt - 0.15, 0.6)
    cancel = eout(prog(t, CANCEL - 0.2, 0.4))
    renew = prog(t, REBUILD, 1.2)
    lining(c, t, a, gel=gel, spread=spread, base=base, cancel=cancel, renew=renew)
    # shield tick
    ta = window(t, TOUCH - 0.1, REBUILD, 0.2, 0.2) * a
    if ta > 0:
        q = eback(prog(t, TOUCH - 0.1, 0.3))
        c.save(); c.translate(800, 1270); c.scale(q, q)
        sh = skia.Path(); sh.moveTo(0, -80); sh.lineTo(70, -54); sh.lineTo(62, 26); sh.quadTo(36, 70, 0, 88); sh.quadTo(-36, 70, -62, 26); sh.lineTo(-70, -54); sh.close()
        c.drawPath(sh, paint("#000000", 0.25, blur=10)); c.drawPath(sh, paint(GREEN))
        ck = skia.Path(); ck.moveTo(-28, 0); ck.lineTo(-6, 22); ck.lineTo(32, -22)
        c.drawPath(ck, paint("#ffffff", 1, stroke=12))
        c.restore()
    # calendar for "every few days"
    ca = window(t, FRESH - 0.1, WIPE2 + 0.3, 0.25, 0.2) * a
    calendar(c, t, 760, 830, 0.7 * eback(prog(t, FRESH - 0.1, 0.35)), ca, (t - DAYS) * 1.6 if t > DAYS else 0)
    pill(c, t, "THE SECRET", 495, 560, "#8a8f98", SECRET, MUC - 0.05)
    pill(c, t, "SLIMY MUCUS", 495, 560, "#4AA3DF", MUC, COAT - 0.05)
    pill(c, t, "COATS THE WALL", 495, 560, "#4AA3DF", COAT, BASEt - 0.05)
    pill(c, t, "BAKING SODA-LIKE BASE", 495, 560, BASE, BASEt, CANCEL - 0.05)
    pill(c, t, "CANCELS THE ACID", 495, 560, ACID_D, CANCEL, TOUCH - 0.05)
    pill(c, t, "NEVER TOUCHES YOU", 495, 560, GREEN, TOUCH, REBUILD - 0.05, text_col="#FFFFFF")
    pill(c, t, "ALWAYS REBUILDING", 495, 560, STOM_D, REBUILD, DAYS - 0.05)
    pill(c, t, "EVERY FEW DAYS", 495, 560, STOM_D, DAYS, WIPE2 + 0.1)


def capsule(c, x, y, s, rot, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -36, 90, 36), 36, 36, paint("#000000", 0.3 * a, blur=10))
    c.save(); c.clipRect(skia.Rect.MakeLTRB(-100, -40, 0, 40))
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -36, 90, 36), 36, 36, paint("#ffffff", a)); c.restore()
    c.save(); c.clipRect(skia.Rect.MakeLTRB(0, -40, 100, 40))
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -36, 90, 36), 36, 36, paint("#E8505B", a)); c.restore()
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -24, 70, -14), 5, 5, paint("#ffffff", 0.6 * a))
    c.restore()


def germ(c, t, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(-20 + 8 * math.sin(t * 5)); c.scale(s, s)
    for k in range(3):
        f = skia.Path(); f.moveTo(-70, -10 + k * 10)
        for j in range(1, 7):
            f.lineTo(-70 - j * 18, -10 + k * 10 + 12 * math.sin(t * 12 + j + k))
        c.drawPath(f, paint(GERM, 0.8 * a, stroke=4))
    c.drawRoundRect(skia.Rect.MakeLTRB(-75, -38, 75, 38), 38, 38, paint("#000000", 0.3 * a, blur=10))
    c.drawRoundRect(skia.Rect.MakeLTRB(-75, -38, 75, 38), 38, 38, paint(shader=radial(-20, -15, 110, [col("#C9B0FF", a), col(GERM, a)])))
    c.drawCircle(30, -8, 10, paint("#ffffff", a)); c.drawCircle(33, -8, 5, paint("#1b1b1b", a))
    m = skia.Path(); m.moveTo(42, 14); m.lineTo(58, 8); m.lineTo(58, 20); m.close()
    c.drawPath(m, paint("#ffffff", a))
    c.restore()


def scene_break(c, t):
    bg_dark(c, t)
    a = eout(prog(t, WIPE2, 0.4))
    gap = eio(prog(t, BREAK - 0.1, 0.5))
    sore = eback(prog(t, ULCER - 0.1, 0.4))
    thin = eio(prog(t, WEAR - 0.1, 0.8))
    lining(c, t, a, gel=1.0, spread=1.0, base=1.0, cancel=1.0, gap=gap, sore=sore, thin=thin, dark=True)
    ca = window(t, PAIN - 0.15, SO, 0.3, 0.3) * a
    capsule(c, 300, lerp(600, 820, eout(prog(t, PAIN - 0.15, 0.5))) + 8 * math.sin(t * 3), 0.85, -18, ca)
    ga = window(t, GERMt - 0.15, SO, 0.3, 0.3) * a
    germ(c, t, lerp(1100, 720, eout(prog(t, GERMt - 0.15, 0.6))) + 10 * math.sin(t * 2), 830, 0.85, ga)
    fa = window(t, BREAK, SO + 0.3, 0.3, 0.3)
    if fa > 0:
        c.drawString("Educational only, not medical advice.", 100, 1492, skia.Font(TF_REG, 24), paint("#FFFFFF", 0.55 * fa))
    pill(c, t, "SHIELD BREAKS?", 495, 560, "#5a5a66", BREAK - 0.05, ULCER - 0.05)
    pill(c, t, "= AN ULCER", 495, 560, SORE, ULCER, PAIN - 0.05)
    pill(c, t, "SOME PAINKILLERS", 495, 560, "#C23B48", PAIN, GERMt - 0.05)
    pill(c, t, "A SNEAKY GERM", 495, 560, "#7A4FE0", GERMt, WEAR - 0.05)
    pill(c, t, "WEAR IT DOWN", 495, 560, "#5a5a66", WEAR, SO + 0.3)


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_lab(c, t); return
    if t < SO - 0.05:
        scene_break(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_break(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.022 * (1 - d / 0.25) ** 2
    return s


def split_long(PH, maxw=9):
    out = []
    for p in PH:
        ws = p["words"]
        if len(ws) <= maxw:
            out.append(p); continue
        k = (len(ws) + 1) // 2
        out.append(dict(p, words=ws[:k], t1=ws[k - 1]["t1"]))
        out.append(dict(p, words=ws[k:], t0=ws[k]["t0"]))
    return out


KWCOL = {"digest": STOM, "itself?": STOM, "metal!": METAL, "meat": "#FF7A6E", "mucus.": GEL, "baking": BASE, "soda": BASE,
         "touches": GREEN, "days!": STOM, "breaks?": "#B0B0B8", "ulcer.": SORE, "germ": GERM}
CAPS = Captions(split_long(P), KWCOL, {"metal!", "ulcer"}, DUR)


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    sx = sy = 0
    for ti in IMPACTS:
        d = t - ti
        if 0 <= d < 0.3:
            amp = 9 * (1 - d / 0.3); sx += amp * math.sin(d * 97); sy += amp * math.cos(d * 83)
    ps = cut_punch(t)
    c.save(); c.translate(sx, sy); c.translate(540, 960); c.scale(ps, ps); c.translate(-540, -960)
    draw_world(c, t)
    c.restore()
    light = WIPE1 + WL / 2 <= t < WIPE2 + WL / 2
    vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 600), paint(shader=linear((0, 0), (0, 600), [col("#000000", 0.45), col("#000000", 0)])))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, ACID, "#F4F2EE")
    wipe(c, t, WIPE2, WL, STOM_D, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("whoosh", STRONG), ("hit", METt), ("pop", MEATt), ("pop", NOPROB),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", SECRET), ("hit", MUC), ("whoosh", COAT), ("pop", BASEt),
          ("pop", CANCEL), ("ding", TOUCH), ("whoosh", REBUILD), ("pop", DAYS), ("whoosh", WIPE2), ("pop", BREAK),
          ("hit", ULCER), ("pop", PAIN), ("pop", GERMt), ("whoosh", WEAR), ("whoosh", SO - 0.05)]
    return sorted(ev, key=lambda e: e[1])


if __name__ == "__main__":
    if sys.argv[1] == "still":
        from PIL import Image
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(f"{D}/still_{ts}.png")
        sys.exit()
    f0, f1, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    tmp = out.replace(".mp4", ".tmp.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        pr.stdin.write(frame(fi / FPS).tobytes())
    pr.stdin.close()
    if pr.wait() == 0:
        os.rename(tmp, out)

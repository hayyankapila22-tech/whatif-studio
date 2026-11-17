# HIW06 — why orange juice tastes awful after brushing (standard format; basic + useful; detailed objects).
# Sources: The Conversation / Popular Science (Bartoshuk) — toothpaste detergent sodium lauryl sulfate (SLS) suppresses
#  sweet receptors and breaks down phospholipids that normally dull bitterness; Scientific American — effect is temporary;
#  Live Science (Crosby); ADA — wait after acidic drinks before brushing.
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
ORANGE = "#FF9F1C"; MINT = "#3EE6A8"; PURPLE = "#9B6BFF"; SWEET = "#FFD23F"; FOAMB = "#BFE6FF"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


OJ = kw(1); YUCK = kw(2); MINTT = kw(3); FOAM = kw(4); SOAP = p0(5); BUBBLES = kw(6)
MUTE = kw(7); SUGAR = kw(8); GONE = p0(9); STRIP = p0(10); QUIET = kw(11); SOUR = kw(13, 0); BITTER = kw(13, 1)
WIPE1 = p0(14) - 0.3; FOREVER = kw(14); NOTEX = kw(15); MINUTES = kw(16)
TRICK = p0(17); FIRST = kw(18); WAIT = p0(19); BRUSH = kw(20); SO = p0(21)
WL = 0.32
IMPACTS = [YUCK, NOTEX]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]
rnd = random.Random(5)
TONGUE = None


def tongue_img():
    global TONGUE
    if TONGUE is None:
        TONGUE = skia.Image.open(f"{D}/tongue.png")
    return TONGUE


# ---------------- backgrounds ----------------
def bg_morning(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#1b2a3f"), col("#24364f"), col("#101826")], [0, 0.5, 1])))
    c.drawCircle(820, 520 + 20 * math.sin(t * 0.4), 700, paint(shader=radial(820, 520, 700, [col("#FFB35C", 0.28), col("#FFB35C", 0)])))
    c.drawCircle(200, 1500, 650, paint(shader=radial(200, 1500, 650, [col("#6FD3FF", 0.16), col("#6FD3FF", 0)])))
    # soft tiled wall hint
    for k in range(9):
        c.drawLine(0, 300 + k * 190, W, 300 + k * 190, paint("#ffffff", 0.035, stroke=2))
    for k in range(7):
        c.drawLine(k * 190, 300, k * 190, 1900, paint("#ffffff", 0.025, stroke=2))
    # counter top
    c.drawRect(skia.Rect.MakeLTRB(0, 1330, W, H), paint(shader=linear((0, 1330), (0, H), [col("#e9e4dc"), col("#b9b2a6")])))
    c.drawRect(skia.Rect.MakeLTRB(0, 1326, W, 1336), paint("#ffffff", 0.6))


# ---------------- detailed objects ----------------
def bubble(c, x, y, r, a=1.0):
    if r <= 0.5 or a <= 0: return
    c.drawCircle(x, y, r, paint(shader=radial(x, y, r, [col("#ffffff", 0.05 * a), col(FOAMB, 0.12 * a), col("#ffffff", 0.55 * a)], [0, 0.75, 1])))
    c.drawCircle(x, y, r, paint("#ffffff", 0.55 * a, stroke=max(1.0, r * 0.06)))
    c.drawArc(skia.Rect.MakeLTRB(x - r * 0.75, y - r * 0.75, x + r * 0.75, y + r * 0.75), 200, 70, False, paint("#ffffff", 0.9 * a, stroke=max(1.2, r * 0.12)))
    c.drawArc(skia.Rect.MakeLTRB(x - r * 0.9, y - r * 0.9, x + r * 0.9, y + r * 0.9), 20, 60, False, paint("#ffb3f0", 0.35 * a, stroke=max(1.0, r * 0.06)))


FOAMS = [(rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.uniform(6, 26), rnd.random() * 6.28) for _ in range(70)]


def foam(c, x, y, s, a, t, spread=1.0):
    for (u, v, r, ph) in FOAMS:
        bubble(c, x + u * 70 * s * spread, y + v * 26 * s * spread + 3 * math.sin(t * 2 + ph), r * s * (0.9 + 0.1 * math.sin(t * 3 + ph)), a)


TUFTS = [(i, j) for i in range(9) for j in range(3)]


def toothbrush(c, x, y, s, rot, t, a=1.0, paste=1.0, foam_a=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    # shadow
    c.drawRoundRect(skia.Rect.MakeLTRB(-420, 40, 360, 90), 40, 40, paint("#000000", 0.35 * a, blur=22))
    # handle
    hp = skia.Path(); hp.moveTo(-430, 10); hp.cubicTo(-430, -28, -380, -34, -300, -30); hp.lineTo(120, -18)
    hp.cubicTo(180, -16, 200, -26, 230, -26); hp.lineTo(380, -22); hp.cubicTo(400, -21, 400, 21, 380, 22); hp.lineTo(230, 26)
    hp.cubicTo(200, 26, 180, 16, 120, 18); hp.lineTo(-300, 30); hp.cubicTo(-380, 34, -430, 28, -430, 10); hp.close()
    c.drawPath(hp, paint(shader=linear((0, -34), (0, 34), [col("#e8f4ff", a), col("#3b7de0", a), col("#1d4a9a", a), col("#5b95ea", a)], [0, 0.35, 0.8, 1])))
    c.drawPath(hp, paint("#0d2a5c", 0.5 * a, stroke=2))
    # rubber grip with ridges
    gp = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-320, -22, -120, 22), 20, 20)
    c.drawRRect(gp, paint(shader=linear((0, -22), (0, 22), [col("#9ff2d6", a), col("#1fb98a", a), col("#0f7a5a", a)])))
    for k in range(10):
        c.drawLine(-305 + k * 19, -16, -305 + k * 19, 16, paint("#0b5a43", 0.55 * a, stroke=4))
    c.drawLine(-410, -18, 360, -10, paint("#ffffff", 0.55 * a, stroke=5, blur=2))      # gloss stripe
    # head + bristles
    c.drawRoundRect(skia.Rect.MakeLTRB(230, -26, 400, 26), 24, 24, paint(shader=linear((0, -26), (0, 26), [col("#cfe3ff", a), col("#3b7de0", a)])))
    for (i, j) in TUFTS:
        bx = 242 + i * 17; by = -30
        for k in range(5):
            xx = bx + (k - 2) * 2.6
            hgt = 74 + 6 * math.sin(i * 1.7 + j)
            c.drawLine(xx, by, xx + 1.5 * math.sin(t * 6 + i), by - hgt, paint(mixhex("#ffffff", "#9fd2ff", j / 2), 0.92 * a, stroke=2.2))
        c.drawCircle(bx, by - 74, 4, paint("#ffffff", 0.9 * a))
    # toothpaste swirl
    if paste > 0:
        pp = skia.Path(); pp.moveTo(238, -112)
        for k in range(12):
            px = 238 + k * 14; py = -112 - 10 * math.sin(k * 1.1)
            pp.lineTo(px, py)
        for col_, w_, off in (("#ffffff", 30, 0), ("#3EE6A8", 9, -8), ("#4c8dff", 7, 8)):
            pq = skia.Path(); pq.addPath(pp)
            c.save(); c.translate(0, off * 0.3)
            c.drawPath(pq, paint(col_, paste * a, stroke=w_ * (1 if col_ == "#ffffff" else 1)))
            c.restore()
        c.drawPath(pp, paint("#ffffff", 0.8 * paste * a, stroke=6, blur=1))
    c.restore()
    if foam_a > 0:
        fx = x + math.cos(math.radians(rot)) * 315 * s; fy = y + math.sin(math.radians(rot)) * 315 * s - 110 * s
        foam(c, fx, fy, s * 0.9, foam_a, t)


PULP = [(rnd.uniform(-1, 1), rnd.uniform(0, 1), rnd.uniform(1.5, 4)) for _ in range(140)]
DROPS = [(rnd.uniform(-1, 1), rnd.uniform(0.1, 0.95), rnd.uniform(3, 8)) for _ in range(26)]


def orange_slice(c, x, y, r, a=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawCircle(4, 6, r, paint("#000000", 0.25 * a, blur=8))
    c.drawCircle(0, 0, r, paint(shader=radial(-r * 0.3, -r * 0.3, r * 1.4, [col("#FFC15A", a), col("#F07A12", a), col("#B8500A", a)], [0, 0.6, 1])))
    for k in range(40):
        an = k * 0.157
        c.drawCircle(r * 0.93 * math.cos(an), r * 0.93 * math.sin(an), 1.6, paint("#8a3a05", 0.35 * a))
    c.drawCircle(0, 0, r * 0.84, paint("#FFF3D9", a))
    for k in range(10):
        a0 = k * 36 + 4
        seg = skia.Path(); seg.moveTo(0, 0); seg.arcTo(skia.Rect.MakeLTRB(-r * 0.76, -r * 0.76, r * 0.76, r * 0.76), a0, 28, False); seg.close()
        c.drawPath(seg, paint(shader=radial(0, 0, r * 0.76, [col("#FFD27A", a), col("#FFA62B", a), col("#F07A12", a)], [0, 0.6, 1])))
        for j in range(4):
            aa = math.radians(a0 + 6 + j * 5); rr = r * (0.3 + 0.1 * j)
            c.drawOval(skia.Rect.MakeXYWH(rr * math.cos(aa) - 3, rr * math.sin(aa) - 1.5, 6, 3), paint("#ffffff", 0.45 * a))
    c.drawCircle(0, 0, r * 0.06, paint("#FFF3D9", a))
    c.drawArc(skia.Rect.MakeLTRB(-r * 0.8, -r * 0.8, r * 0.8, r * 0.8), 200, 60, False, paint("#ffffff", 0.5 * a, stroke=r * 0.06, blur=2))
    c.restore()


def glass_oj(c, x, y, s, a=1.0, tilt=0.0, level=1.0, t=0.0, slice_on=True):
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-150, 270, 150, 310), paint("#000000", 0.35 * a, blur=16))
    body = skia.Path(); body.moveTo(-150, -260); body.lineTo(150, -260); body.lineTo(122, 280); body.cubicTo(120, 296, -120, 296, -122, 280); body.close()
    c.drawPath(body, paint(shader=linear((-150, 0), (150, 0), [col("#ffffff", 0.18 * a), col("#ffffff", 0.05 * a), col("#ffffff", 0.22 * a)])))
    # juice
    top = lerp(270, -205, level)
    jp = skia.Path(); jp.moveTo(-148 + (top + 260) * 0.05, top); jp.lineTo(148 - (top + 260) * 0.05, top); jp.lineTo(118, 270)
    jp.cubicTo(116, 284, -116, 284, -118, 270); jp.close()
    c.save(); c.clipPath(body)
    c.drawPath(jp, paint(shader=linear((-140, 0), (140, 0), [col("#FFB52E", 0.97 * a), col("#FFD36B", 0.97 * a), col("#F48A17", 0.97 * a), col("#D96A0A", 0.97 * a)], [0, 0.3, 0.7, 1])))
    for (u, v, r) in PULP:
        py = lerp(top + 10, 270, v)
        c.drawOval(skia.Rect.MakeXYWH(u * 120 - r, py - r * 0.5 + 2 * math.sin(t + u * 9), r * 2, r), paint("#FFE7A8", 0.5 * a))
    c.drawOval(skia.Rect.MakeLTRB(-146 + (top + 260) * 0.05, top - 14, 146 - (top + 260) * 0.05, top + 14), paint(shader=linear((0, top - 14), (0, top + 14), [col("#FFE6A0", a), col("#FFB52E", a)])))
    c.restore()
    # glass rim + edges
    c.drawOval(skia.Rect.MakeLTRB(-150, -276, 150, -244), paint("#ffffff", 0.75 * a, stroke=4))
    c.drawPath(body, paint("#ffffff", 0.55 * a, stroke=4))
    c.drawLine(-118, -230, -100, 250, paint("#ffffff", 0.55 * a, stroke=12, blur=4))
    c.drawLine(96, -230, 86, 240, paint("#ffffff", 0.3 * a, stroke=6, blur=3))
    for (u, v, r) in DROPS:
        dx = u * 130; dy = lerp(-240, 260, v)
        c.drawCircle(dx, dy, r, paint(shader=radial(dx - r * 0.3, dy - r * 0.4, r * 1.2, [col("#ffffff", 0.85 * a), col("#ffffff", 0.15 * a)])))
    c.restore()
    if slice_on:
        orange_slice(c, x + 140 * s * math.cos(math.radians(tilt)), y - 260 * s, 90 * s, a, -20 + tilt)


def mint_leaf(c, x, y, s, rot, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, -200)
    pts_r = []; pts_l = []
    for k in range(13):
        u = k / 12
        w_ = 120 * math.sin(math.pi * u) ** 0.8
        tooth = 10 * (k % 2)
        pts_r.append((w_ + tooth, -200 + u * 400)); pts_l.append((-w_ - tooth, -200 + u * 400))
    for q in pts_r: p.lineTo(*q)
    for q in reversed(pts_l): p.lineTo(*q)
    p.close()
    c.drawPath(p, paint("#000000", 0.3 * a, blur=14))
    c.drawPath(p, paint(shader=linear((-120, -200), (120, 200), [col("#9CF2A8", a), col("#2FBF5A", a), col("#147a35", a)], [0, 0.5, 1])))
    c.drawLine(0, -190, 0, 230, paint("#c9ffd6", 0.8 * a, stroke=6))
    for k in range(5):
        yv = -140 + k * 70
        for sg in (-1, 1):
            vp = skia.Path(); vp.moveTo(0, yv); vp.quadTo(sg * 50, yv + 10, sg * 95 * math.sin(math.pi * (yv + 200) / 400), yv - 30)
            c.drawPath(vp, paint("#c9ffd6", 0.55 * a, stroke=3))
    c.drawLine(0, 200, 0, 270, paint("#2a8a40", a, stroke=10))
    c.drawPath(p, paint("#ffffff", 0.15 * a, stroke=3))
    c.restore()


def tube(c, x, y, s, rot, a=1.0, squeeze=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-260, 50, 260, 90), 30, 30, paint("#000000", 0.3 * a, blur=16))
    b = skia.Path(); b.moveTo(-250, -60); b.lineTo(170, -80 + 20 * squeeze); b.lineTo(170, 80 - 20 * squeeze); b.lineTo(-250, 60); b.close()
    c.drawPath(b, paint(shader=linear((0, -80), (0, 80), [col("#ffffff", a), col("#e8eef7", a), col("#aab6c8", a)], [0, 0.5, 1])))
    c.drawRect(skia.Rect.MakeLTRB(-160, -50, 120, 50), paint(shader=linear((-160, 0), (120, 0), [col("#2f6fe0", a), col("#3EE6A8", a)])))
    f = skia.Font(TF_BLACK, 40); c.drawString("FRESH", -110, 14, f, paint("#ffffff", a))
    for k in range(6):
        c.drawLine(-250 + k * 7, -58, -250 + k * 7, 58, paint("#8a96a8", 0.6 * a, stroke=2))
    c.drawRoundRect(skia.Rect.MakeLTRB(170, -34, 250, 34), 10, 10, paint(shader=linear((0, -34), (0, 34), [col("#ffffff", a), col("#2f6fe0", a)])))
    c.drawLine(-240, -40, 160, -55, paint("#ffffff", 0.7 * a, stroke=6, blur=2))
    c.restore()


# taste-bud receptors on the tongue macro
BUDS = [(180 + (i % 4) * 230 + (i // 4 % 2) * 100, 760 + (i // 4) * 210) for i in range(12)]


def receptor(c, x, y, kind, glow, blanket, a=1.0):
    colr = SWEET if kind == "sweet" else PURPLE
    c.drawCircle(x + 4, y + 10, 52, paint("#000000", 0.35 * a, blur=10))
    c.drawCircle(x, y, 50, paint(shader=radial(x - 16, y - 18, 70, [col("#ffd3dc", a), col("#e57a8c", a), col("#b44a5e", a)], [0, 0.5, 1])))
    c.drawCircle(x, y, 26, paint(shader=radial(x - 6, y - 8, 34, [col("#ffffff", a), col(colr, a), col(mixhex(colr, "#000000", 0.4), a)], [0, 0.45, 1])))
    if glow > 0:
        c.drawCircle(x, y, 60, paint(colr, 0.45 * glow * a, blur=18))
    if blanket > 0:
        c.drawCircle(x, y, 44, paint(shader=radial(x - 10, y - 14, 56, [col("#fff6e8", 0.95 * blanket * a), col("#f1d8c0", 0.85 * blanket * a)])))
        c.drawCircle(x, y, 44, paint("#ffffff", 0.6 * blanket * a, stroke=2))
    c.drawCircle(x - 14, y - 16, 7, paint("#ffffff", 0.75 * a))


def mute_icon(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 46, paint("#141313", 0.75 * a))
    sp = skia.Path(); sp.moveTo(-22, -10); sp.lineTo(-8, -10); sp.lineTo(10, -26); sp.lineTo(10, 26); sp.lineTo(-8, 10); sp.lineTo(-22, 10); sp.close()
    c.drawPath(sp, paint("#ffffff", a))
    c.drawLine(-30, 28, 30, -28, paint(RED, a, stroke=7))
    c.restore()


def tongue_scene(c, t, st):
    push = 1 + 0.04 * prog(t, MUTE - 0.3, 8)
    c.save(); c.translate(540, 1000); c.scale(push, push); c.translate(-540, -1000)
    c.drawImageRect(tongue_img(), skia.Rect.MakeXYWH(-160, -240, 1400, 2400), SAMP)
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(540, 1000, 1100, [col("#000000", 0.0), col("#2a0a12", 0.55)])))
    sweet_glow = 1 - eout(prog(t, MUTE + 0.2, 0.8))
    blanket = 1 - eio(prog(t, STRIP + 0.3, 1.0))
    bitter_glow = eout(prog(t, QUIET - 0.1, 0.6))
    for i, (x, y) in enumerate(BUDS):
        kind = "sweet" if i % 2 == 0 else "bitter"
        q = eback(prog(t, MUTE - 0.25 + i * 0.03, 0.3))
        if q <= 0: continue
        c.save(); c.translate(x, y); c.scale(q, q); c.translate(-x, -y)
        receptor(c, x, y, kind, sweet_glow if kind == "sweet" else bitter_glow, blanket if kind == "bitter" else 0, clamp(q))
        c.restore()
    # sugar crystals fading into sparkles
    sa = window(t, SUGAR - 0.3, STRIP, 0.3, 0.3)
    if sa > 0:
        dis = prog(t, GONE - 0.2, 1.0)
        for k in range(9):
            x = 260 + (k % 3) * 260 + 30 * math.sin(k); y = 820 + (k // 3) * 210
            cs = 34 * (1 - dis)
            if cs > 1:
                cube = skia.Rect.MakeXYWH(x - cs, y - cs - 90, cs * 2, cs * 2)
                c.drawRect(cube, paint(shader=linear((x - cs, y - cs), (x + cs, y + cs), [col("#ffffff", sa), col("#dfe6f0", sa)])))
                c.drawRect(cube, paint("#c4cfdd", sa, stroke=2))
            for j in range(5):
                u = dis
                c.drawCircle(x + (j - 2) * 22 * u, y - 90 - 60 * u * (1 + j % 2), 4, paint(SWEET, sa * u * (1 - u) * 3))
    c.restore()
    if t > MUTE - 0.1 and t < SUGAR + 0.4:
        mute_icon(c, 760, 600, eback(prog(t, MUTE + 0.15, 0.3)), 1 - prog(t, SUGAR + 0.2, 0.2))


def meters(c, t, a):
    f = skia.Font(TF_MONO, 28)
    labels = (("SWEET", SWEET, 0.15), ("SOUR", "#B7F34A", 0.9), ("BITTER", PURPLE, 0.95))
    for i, (lab, colr, v) in enumerate(labels):
        x = 260 + i * 260; base = 1300; hmax = 520
        tt = SOUR if lab != "BITTER" else BITTER
        q = eexpo(prog(t, tt - 0.1, 0.7)) if lab != "SWEET" else 1
        h = hmax * (v * q if lab != "SWEET" else lerp(0.8, 0.15, eio(prog(t, SOUR - 0.2, 0.6))))
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 70, base - hmax, x + 70, base), 34, 34, paint("#ffffff", 0.06 * a))
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 70, base - hmax, x + 70, base), 34, 34, paint("#ffffff", 0.18 * a, stroke=2))
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 70, base - h, x + 70, base), 34, 34, paint(shader=linear((x - 70, 0), (x + 70, 0), [col(mixhex(colr, "#ffffff", 0.35), a), col(colr, a), col(mixhex(colr, "#000000", 0.3), a)])))
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 52, base - h + 14, x - 34, base - 16), 9, 9, paint("#ffffff", 0.35 * a))
        c.drawString(lab, x - f.measureText(lab) / 2, base + 50, f, paint("#ffffff", 0.85 * a))
        arrow = "▼" if lab == "SWEET" else "▲"
        fa = skia.Font(TF_BLACK, 44)
        c.drawString(arrow, x - fa.measureText(arrow) / 2, base - h - 20, fa, paint(colr, a))


def timer(c, t, x, y, a, light=True):
    q = eio(prog(t, p0(16) + 0.2, 1.6))
    c.drawCircle(x + 4, y + 10, 150, paint("#000000", 0.15 * a, blur=16))
    c.drawCircle(x, y, 150, paint(shader=radial(x - 50, y - 60, 220, [col("#ffffff", a), col("#e7e3dc", a)])))
    c.drawCircle(x, y, 120, paint(INK, 0.08 * a, stroke=22))
    arc = skia.Path(); arc.addArc(skia.Rect.MakeLTRB(x - 120, y - 120, x + 120, y + 120), -90, 360 * q)
    c.drawPath(arc, paint(shader=linear((x - 120, y), (x + 120, y), [col("#3EE6A8", a), col("#1fb98a", a)]), a=a) if False else paint("#1fb98a", a, stroke=22))
    s = "✓" if q >= 1 else f"{int(5 * (1 - q)) + 1} MIN"
    f = skia.Font(TF_BLACK, 56 if q < 1 else 96)
    c.drawString(s, x - f.measureText(s) / 2, y + 20 if q < 1 else y + 34, f, paint(INK if q < 1 else "#1fb98a", a))


def scene_main(c, t):
    bg_morning(c, t)
    # toothbrush (hook) → slides out; glass slides in
    out = eio(prog(t, OJ - 0.2, 0.7))
    tb_x = lerp(560, -500, out)
    toothbrush(c, tb_x, 1180, 1.25, -12 + 4 * math.sin(2 * math.pi * t / DUR * 2), t, 1.0, 1.0, foam_a=1.0)
    if t > OJ - 0.3:
        gi = eback(prog(t, OJ - 0.2, 0.6), 1.1)
        wob = 0
        if t > YUCK - 0.05:
            d = t - YUCK
            wob = 9 * math.sin(d * 22) * math.exp(-d * 2.5)
        glass_oj(c, lerp(1500, 520, clamp(gi)), 1030, 1.15, 1.0, wob, 0.82, t)
    ya = window(t, YUCK - 0.05, MINTT, 0.15, 0.25)
    if ya > 0:
        for k in range(3):
            y0 = 760 - k * 50
            p = skia.Path(); p.moveTo(380, y0)
            for xx in range(380, 700, 20):
                p.lineTo(xx, y0 + 12 * math.sin(xx / 22 + t * 8 + k))
            c.drawPath(p, paint("#8BE36B", 0.7 * ya, stroke=7))
    pill(c, t, "BLEH", 500, 1360, "#8BE36B", YUCK, MINTT)


def scene_mint_foam(c, t):
    bg_morning(c, t)
    ma = window(t, MINTT - 0.25, FOAM + 0.1, 0.25, 0.25)
    if ma > 0:
        mint_leaf(c, 500, 1000, 1.25 * eback(prog(t, MINTT - 0.25, 0.35)), -18, ma)
        xa = eout(prog(t, MINTT + 0.35, 0.2)) * ma
        if xa > 0:
            c.drawLine(330, 820, lerp(330, 680, xa), lerp(820, 1180, xa), paint(RED, xa, stroke=20))
            c.drawLine(680, 820, lerp(680, 330, xa), lerp(820, 1180, xa), paint(RED, xa, stroke=20))
    fa = eout(prog(t, FOAM - 0.1, 0.4))
    if fa > 0:
        s = lerp(1.0, 2.2, eio(prog(t, FOAM, 3.0)))
        if t > SOAP - 0.1:
            tube(c, lerp(-400, 460, eout(prog(t, SOAP - 0.1, 0.6))), 1170, 1.25, -8, 1.0, 0.5 + 0.5 * math.sin(t * 3))
        foam(c, 520, 950, s, fa, t, 1.6)
        if t > BUBBLES - 0.1:
            bb = eout(prog(t, BUBBLES - 0.1, 0.6))
            for k in range(7):
                bubble(c, 220 + k * 110, 760 - 80 * math.sin(k * 1.3) - 30 * math.sin(t + k), (40 + 30 * (k % 3)) * bb, bb)
    pill(c, t, "FOAMING SOAP", 500, 1360, FOAMB, SOAP + 0.2, MUTE - 0.3, text_col=INK)


def scene_tongue(c, t):
    tongue_scene(c, t, {})
    pill(c, t, "SWEET: MUTED", 500, 1360, SWEET, MUTE + 0.15, STRIP - 0.1)
    pill(c, t, "BITTER: SWITCHED ON", 500, 1360, PURPLE, QUIET, SOUR - 0.3)


def scene_meters(c, t):
    bg_morning(c, t)
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#0b1220", 0.55))
    meters(c, t, eout(prog(t, SOUR - 0.45, 0.35)))


def scene_white(c, t):
    studio_white(c)
    fa = eback(prog(t, FOREVER - 0.15, 0.35)) * (1 - prog(t, p0(16), 0.2))
    if fa > 0:
        # hourglass, detailed
        x, y = 540, 1000
        c.save(); c.translate(x, y); c.scale(fa, fa)
        for sg in (-1, 1):
            c.drawRoundRect(skia.Rect.MakeLTRB(-170, sg * 260 - 22, 170, sg * 260 + 22), 14, 14, paint(shader=linear((0, -22), (0, 22), [col("#d9a46a"), col("#8a5a2b")])))
        g = skia.Path(); g.moveTo(-140, -240); g.cubicTo(-140, -80, -20, -40, -20, 0); g.cubicTo(-20, 40, -140, 80, -140, 240)
        g.lineTo(140, 240); g.cubicTo(140, 80, 20, 40, 20, 0); g.cubicTo(20, -40, 140, -80, 140, -240); g.close()
        c.drawPath(g, paint("#ffffff", 0.35)); c.drawPath(g, paint("#9aa7b8", 0.8, stroke=4))
        sand = skia.Path(); sand.moveTo(-100, 240); sand.lineTo(0, 120); sand.lineTo(100, 240); sand.close()
        c.drawPath(sand, paint(shader=linear((0, 120), (0, 240), [col("#F5D08A"), col("#D9A04A")])))
        c.drawLine(0, 0, 0, 200, paint("#E7B860", 1, stroke=4))
        c.drawLine(-120, -220, -40, -30, paint("#ffffff", 0.6, stroke=8, blur=3))
        c.restore()
        if t > NOTEX:
            xa = eout(prog(t, NOTEX, 0.2))
            c.drawLine(340, 760, lerp(340, 740, xa), lerp(760, 1240, xa), paint(RED, 1, stroke=20))
            c.drawLine(740, 760, lerp(740, 340, xa), lerp(760, 1240, xa), paint(RED, 1, stroke=20))
    ta = window(t, p0(16) + 0.1, FIRST - 0.1, 0.25, 0.25)
    if ta > 0:
        timer(c, t, 540, 1000, ta)
    # the trick: juice first, wait, then brush
    if t > TRICK - 0.1:
        a1 = eout(prog(t, FIRST - 0.2, 0.4))
        glass_oj(c, 260, 1020, 0.62 * eback(prog(t, FIRST - 0.2, 0.4)), clamp(a1), 0, 0.82, t)
        badge(c, 260, 700, "1", ORANGE, eback(prog(t, FIRST, 0.3)))
        a2 = eout(prog(t, WAIT - 0.1, 0.3))
        if a2 > 0:
            clock(c, t, 540, 1000, 0.7 * a2 + 0.3 * a2, a2)
        a3 = eout(prog(t, BRUSH - 0.2, 0.4))
        if a3 > 0:
            toothbrush(c, 800, 1060, 0.42, -70, t, a3, 1.0)
            badge(c, 800, 700, "2", "#3b7de0", eback(prog(t, BRUSH, 0.3)), "#FFFFFF")
    pill(c, t, "A FEW MINUTES", 500, 1360, "#1fb98a", MINUTES, TRICK, light=True)
    pill(c, t, "JUICE FIRST", 500, 1360, ORANGE, FIRST, WAIT, light=True)
    pill(c, t, "WAIT", 500, 1360, "#9aa0ad", WAIT, BRUSH, light=True, text_col="#FFFFFF")
    pill(c, t, "THEN BRUSH", 500, 1360, "#3b7de0", BRUSH, SO, light=True)


def clock(c, t, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(4, 10, 120, paint("#000000", 0.18 * a, blur=14))
    c.drawCircle(0, 0, 120, paint(shader=radial(-40, -50, 180, [col("#ffffff", a), col("#e5e1da", a), col("#bdb6aa", a)], [0, 0.6, 1])))
    c.drawCircle(0, 0, 120, paint("#8a8f98", a, stroke=6))
    for k in range(12):
        an = k * math.pi / 6
        c.drawLine(96 * math.sin(an), -96 * math.cos(an), 108 * math.sin(an), -108 * math.cos(an), paint(INK, a, stroke=4 if k % 3 == 0 else 2))
    mm = (t - WAIT) * 6
    c.drawLine(0, 0, 60 * math.sin(mm * 0.1), -60 * math.cos(mm * 0.1), paint(INK, a, stroke=7))
    c.drawLine(0, 0, 90 * math.sin(mm), -90 * math.cos(mm), paint("#1fb98a", a, stroke=5))
    c.drawCircle(0, 0, 8, paint(INK, a))
    c.restore()


def badge(c, x, y, txt, colr, a, txtcol=INK):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    c.drawCircle(0, 4, 40, paint("#000000", 0.2, blur=6))
    c.drawCircle(0, 0, 38, paint(shader=radial(-12, -14, 50, [col(mixhex(colr, "#ffffff", 0.4)), col(colr)])))
    f = skia.Font(TF_BLACK, 40); c.drawString(txt, -f.measureText(txt) / 2, 14, f, paint(txtcol))
    c.restore()


def hook(c, t):
    bg_morning(c, t)
    toothbrush(c, 560, 1180, 1.25, -12 + 4 * math.sin(2 * math.pi * t / DUR * 2), t, 1.0, 1.0, foam_a=1.0)


def draw_world(c, t):
    if t < MINTT - 0.25:
        scene_main(c, t); return
    if t < MUTE - 0.3:
        scene_mint_foam(c, t); return
    if t < SOUR - 0.45:
        scene_tongue(c, t)
        if t < MUTE:
            c.saveLayerAlpha(None, int(255 * (1 - eout(prog(t, MUTE - 0.3, 0.3))))); scene_mint_foam(c, t); c.restore()
        return
    if t < WIPE1 + WL / 2:
        scene_meters(c, t)
        if t < SOUR - 0.1:
            c.saveLayerAlpha(None, int(255 * (1 - eout(prog(t, SOUR - 0.45, 0.35))))); scene_tongue(c, t); c.restore()
        return
    if t < SO - 0.05:
        scene_white(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_white(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.025 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"orange": ORANGE, "disgusting": "#8BE36B", "mint": MINT, "foam": FOAMB, "bubbles": FOAMB, "mutes": SWEET,
         "sugar": SWEET, "quiet": PURPLE, "sour": "#B7F34A", "bitter": PURPLE, "forever": "#FFFFFF", "exactly": RED,
         "minutes": "#1fb98a", "first": ORANGE, "brush": "#3b7de0"}
CAPS = Captions(P, KWCOL, {"Not", "disgusting."}, DUR)


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    sx = sy = 0
    for ti in IMPACTS:
        d = t - ti
        if 0 <= d < 0.3:
            amp = 7 * (1 - d / 0.3); sx += amp * math.sin(d * 97); sy += amp * math.cos(d * 83)
    ps = cut_punch(t)
    c.save(); c.translate(sx, sy); c.translate(540, 960); c.scale(ps, ps); c.translate(-540, -960)
    draw_world(c, t)
    c.restore()
    light = WIPE1 + WL / 2 <= t < SO - 0.05 + (DUR - SO) * 0.5
    vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 700), paint(shader=linear((0, 0), (0, 700), [col("#000000", 0.45), col("#000000", 0)])))
    rw = math.sin(math.pi * prog(t, NOTEX, 0.4))
    if rw > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.16 * rw))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, ORANGE, "#F4F2EE")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", OJ - 0.2), ("hit", YUCK), ("pop", MINTT), ("tick", MINTT + 0.35), ("whoosh", FOAM - 0.1),
          ("pop", SOAP + 0.2), ("pop", BUBBLES), ("pop", BUBBLES + 0.2), ("whoosh", MUTE - 0.3), ("pop", MUTE + 0.15),
          ("pop", SUGAR), ("riser", STRIP - 0.2), ("pop", QUIET), ("whoosh", SOUR - 0.45), ("ding", BITTER),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", FOREVER), ("hit", NOTEX), ("ding", MINUTES + 1.3),
          ("pop", FIRST), ("pop", WAIT), ("pop", BRUSH), ("whoosh", SO - 0.05)]
    for k in range(6):
        ev.append(("tick", MINUTES + k * 0.22))
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

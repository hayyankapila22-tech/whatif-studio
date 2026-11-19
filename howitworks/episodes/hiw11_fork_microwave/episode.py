# HIW11 — "SERIOUSLY, do NOT put a fork in the microwave. You see..." Bubbly Liam voice, "So," loop.
# Sources (fact-checked 2026-11-19):
#  - NPR "Microwave antics: don't stick a fork in it" (2006): a fork "absorbs the microwaves like an antenna", electrons
#    "build up in these sharp points, creating a strong electric field" -> arcing (sparks); smooth objects without points
#    "can sometimes escape ... unscathed"; arcing can ignite paper; avoid forks, twist-ties, crinkled foil.
#  - HyperPhysics (GSU) "Microwave ovens": 2.45 GHz, wavelength ~12 cm; door screen holes ~1 mm, far smaller than the
#    wavelength, so microwaves can't pass; water heated by dielectric heating.
#  - How Everything Works (L. Bloomfield): metal surfaces reflect microwaves; the door mesh reflects them like solid metal.
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
WAVE = "#FFB84D"; WARM = "#FFD38A"; ZAPC = "#9FE3FF"; STEEL = "#C9CED6"; FIRE = "#FF6A2B"; GREEN = "#1fb98a"
BODY = "#E9E6E1"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


NOT = kw(1); YOUSEE = p0(2); WAVES = kw(3); SHAKE = p0(4); BUTM = p0(5); BOUNCE = kw(6); ANT = kw(7)
TIPS = kw(8); PILE = p0(9); ZAP = kw(10); SPARKS = kw(11)
WIPE1 = p0(12) - 0.3; WALLS = kw(13); YEP = p0(14); SMOOTH = p0(15); NOPTS = kw(16); BOUNCE2 = p0(17)
MESH = kw(18); SMALLER = kw(19); WIPE2 = p0(20) - 0.3; FIREt = kw(20); OUT = p0(21); SO = p0(22)
WL = 0.32
IMPACTS = [NOT, ZAP]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def loopwave(t, k=1):
    return math.sin(2 * math.pi * k * t / DUR)


# ---------------- parts ----------------
def bolt(c, x1, y1, x2, y2, t, a, width=7, seed=0, colr=ZAPC):
    if a <= 0: return
    r = random.Random(int(t * 30) * 7 + seed)
    n = 8; dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) + 1e-6; nx, ny = -dy / L, dx / L
    pts = [(x1 + dx * i / n + nx * (0 if i in (0, n) else r.uniform(-1, 1) * L * 0.12),
            y1 + dy * i / n + ny * (0 if i in (0, n) else r.uniform(-1, 1) * L * 0.12)) for i in range(n + 1)]
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    c.drawPath(p, paint(colr, 0.45 * a, stroke=width * 4, blur=12))
    c.drawPath(p, paint(colr, a, stroke=width))
    c.drawPath(p, paint("#ffffff", a, stroke=width * 0.4))


def wave(c, x0, y0, x1, y1, amp, wl, phase, colr, a, width=6):
    if a <= 0: return
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) + 1e-6; ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    p = skia.Path()
    n = max(8, int(L / 6))
    for i in range(n + 1):
        s = L * i / n
        o = amp * math.sin(2 * math.pi * s / wl - phase)
        x, y = x0 + ux * s + nx * o, y0 + uy * s + ny * o
        p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
    c.drawPath(p, paint(colr, 0.35 * a, stroke=width * 3, blur=8))
    c.drawPath(p, paint(colr, a, stroke=width))


def fork(c, x, y, s, rot, a=1.0, glow=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    sh = linear((-50, 0), (50, 0), [col("#f7f9fb", a), col(STEEL, a), col("#7d858f", a), col("#e3e7ec", a)], [0, 0.35, 0.7, 1])
    c.drawRoundRect(skia.Rect.MakeLTRB(-24, 10, 24, 330), 24, 24, paint(shader=sh))            # handle
    c.drawRoundRect(skia.Rect.MakeLTRB(-14, -20, 14, 40), 10, 10, paint(shader=sh))            # neck
    hp = skia.Path(); hp.moveTo(-56, -60); hp.lineTo(56, -60); hp.cubicTo(50, -10, 20, 0, 14, -10); hp.lineTo(-14, -10); hp.cubicTo(-20, 0, -50, -10, -56, -60); hp.close()
    c.drawPath(hp, paint(shader=sh))
    for k in range(4):
        tx = -42 + k * 28
        c.drawRoundRect(skia.Rect.MakeLTRB(tx - 8, -220, tx + 8, -50), 8, 8, paint(shader=sh))
    c.drawLine(-12, 40, -12, 310, paint("#ffffff", 0.7 * a, stroke=5))
    if glow > 0:
        for k in range(4):
            tx = -42 + k * 28
            c.drawCircle(tx, -216, 26, paint(ZAPC, 0.55 * glow * a, blur=10))
    c.restore()


def tip_points(x, y, s):
    return [(x + (-42 + k * 28) * s, y - 216 * s) for k in range(4)]


def plate(c, x, y, rx, ry, a=1.0):
    c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry + 8, x + rx, y + ry + 8), paint("#000000", 0.25 * a, blur=8))
    c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), paint(shader=radial(x, y - ry * 0.3, rx, [col("#ffffff", a), col("#e7e3dc", a), col("#c9c2b6", a)], [0, 0.7, 1])))
    c.drawOval(skia.Rect.MakeLTRB(x - rx * 0.7, y - ry * 0.7, x + rx * 0.7, y + ry * 0.7), paint("#bdb5a8", 0.6 * a, stroke=2))


# ---------------- microwave front (hook) ----------------
def kitchen(c):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#1a1716"), col("#24201d"), col("#120f0e")], [0, 0.6, 1])))
    for k in range(9):      # tiles
        c.drawLine(0, 520 + k * 90, W, 520 + k * 90, paint("#ffffff", 0.04, stroke=2))
    for k in range(13):
        c.drawLine(k * 90, 520, k * 90, 1290, paint("#ffffff", 0.04, stroke=2))
    c.drawRect(skia.Rect.MakeLTRB(0, 1290, W, H), paint(shader=linear((0, 1290), (0, 1400), [col("#5b4a3c"), col("#3a2e25")])))
    c.drawRect(skia.Rect.MakeLTRB(0, 1290, W, 1300), paint("#7a6552"))


def microwave(c, t, x=490, y=1010, s=1.0, inner=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-400, -250, 400, 290), 34, 34, paint("#000000", 0.5, blur=26))
    c.drawRoundRect(skia.Rect.MakeLTRB(-400, -270, 400, 270), 34, 34, paint(shader=linear((0, -270), (0, 270), [col("#f6f4f0"), col(BODY), col("#bcb7af")])))
    # window
    win = skia.Rect.MakeLTRB(-360, -220, 170, 220)
    c.drawRoundRect(win.makeOutset(14, 14), 22, 22, paint("#2a2a2e"))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(win, 14, 14), doAntiAlias=True)
    c.drawRect(win, paint(shader=radial(-95, -40, 360, [col("#fff1c9", inner), col("#f5c86a", inner), col("#7a4f1c", inner)], [0, 0.55, 1])))
    ang = 2 * math.pi * t / DUR
    plate(c, -95, 150, 210, 46)
    fx = -95 + 70 * math.cos(ang); fz = math.sin(ang)
    fork(c, fx, 160 + 10 * fz, 0.55, 90 + 25 * math.sin(ang), 1.0)
    # mesh dots over the window
    for yy in range(-220, 221, 16):
        for xx in range(-360, 171, 16):
            c.drawCircle(xx, yy, 2.2, paint("#000000", 0.18))
    c.drawRect(win, paint(shader=linear((-360, -220), (170, 220), [col("#ffffff", 0.16), col("#ffffff", 0), col("#ffffff", 0.06)], [0, 0.5, 1])))
    c.restore()
    # control panel
    c.drawRoundRect(skia.Rect.MakeLTRB(210, -220, 370, -150), 12, 12, paint("#101418"))
    f = skia.Font(TF_MONO, 40)
    txt = "0:30" if math.sin(2 * math.pi * 2 * t / DUR * 8) > -0.6 else "0 30"
    c.drawString(txt, 290 - f.measureText(txt) / 2, -170, f, paint("#56f0b0"))
    for r in range(4):
        for k in range(3):
            c.drawRoundRect(skia.Rect.MakeLTRB(215 + k * 52, -120 + r * 52, 255 + k * 52, -84 + r * 52), 8, 8, paint("#d6d1c9"))
    c.drawRoundRect(skia.Rect.MakeLTRB(215, 110, 365, 170), 14, 14, paint("#2d2f33"))
    c.drawRoundRect(skia.Rect.MakeLTRB(230, 230, 350, 250), 10, 10, paint("#a8a39b"))
    c.restore()


def no_sign(c, x, y, r, a, p=1.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(p, p)
    c.drawCircle(0, 0, r, paint(RED, 0.25 * a, stroke=40, blur=10))
    c.drawCircle(0, 0, r, paint(RED, a, stroke=26))
    c.save(); c.rotate(-45); c.drawLine(-r, 0, r, 0, paint(RED, a, stroke=26)); c.restore()
    c.restore()


def hook_scene(c, t):
    kitchen(c); microwave(c, t)


def scene_hook(c, t):
    kitchen(c)
    z = eio(prog(t, YOUSEE - 0.1, WAVES - YOUSEE + 0.1))
    c.save(); c.translate(lerp(0, -95 * 1.8 + 0, z) + 490 * z * 0, 0)
    cx, cy = 395, 1010
    c.translate(cx, cy); c.scale(1 + 1.6 * z, 1 + 1.6 * z); c.translate(-cx, -cy)
    microwave(c, t)
    c.restore()
    na = window(t, NOT - 0.05, YOUSEE + 0.1, 0.05, 0.3)
    no_sign(c, 395, 1010, 230, na, eback(prog(t, NOT - 0.05, 0.3)))
    pill(c, t, "DO NOT", 490, 1360, RED, NOT, YOUSEE)


# ---------------- inside: waves + water ----------------
def cavity_side(c, t, a=1.0):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(490, 1000, 1000, [col("#3a2a14"), col("#140f0a")])))
    box = skia.Rect.MakeLTRB(90, 600, 900, 1380)
    c.drawRect(box, paint(shader=radial(490, 1000, 600, [col("#5a4322"), col("#2a1f12")])))
    c.drawRect(box, paint(STEEL, 0.8, stroke=14))
    # magnetron + antenna on the right wall
    c.drawRoundRect(skia.Rect.MakeLTRB(820, 700, 900, 820), 10, 10, paint("#9aa2ad"))
    c.drawLine(820, 760, 790, 760, paint("#c9ced6", 1, stroke=10))


def bowl(c, x, y, s, t, shake):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-180, 70, 180, 110), paint("#000000", 0.3, blur=10))
    bp = skia.Path(); bp.moveTo(-170, -10); bp.cubicTo(-160, 110, 160, 110, 170, -10); bp.close()
    c.drawPath(bp, paint(shader=linear((0, -10), (0, 100), [col("#ffffff"), col("#d9d3c8")])))
    c.drawOval(skia.Rect.MakeLTRB(-170, -40, 170, 20), paint(shader=radial(0, -10, 170, [col("#ffb35c"), col("#e07a2a")])))
    r = random.Random(4)
    for k in range(9):
        mx = r.uniform(-120, 120); my = r.uniform(-30, 5)
        j = shake * 6
        mx += j * math.sin(t * 50 + k); my += j * math.cos(t * 43 + k * 2)
        ang = (t * 6 * shake + k) * 40
        c.save(); c.translate(mx, my); c.rotate(ang)
        c.drawCircle(0, 0, 11, paint("#ff4d4d"))
        c.drawCircle(-12, 9, 7, paint("#ffffff")); c.drawCircle(12, 9, 7, paint("#ffffff"))
        c.restore()
    c.restore()


def scene_inside(c, t):
    cavity_side(c, t)
    wa = eout(prog(t, WAVES - 0.2, 0.4))
    for k in range(3):
        y = 760 + k * 0
        wave(c, 790, 760 + k * 0, lerp(790, 140, wa), 760 + 220 * k, 22, 70, t * 9 + k, WAVE, 0.9 * wa, 5)
    sh = prog(t, SHAKE, 0.4)
    bowl(c, 470, 1230, 1.2, t, 0.2 + 0.8 * sh)
    pill(c, t, "INVISIBLE WAVES", 490, 540, WAVE, WAVES, SHAKE - 0.1)
    pill(c, t, "SHAKE THE WATER", 490, 540, "#ff7a59", SHAKE, BUTM - 0.1, text_col="#FFFFFF")


def scene_mirror(c, t):
    studio_dark(c)
    # metal sheet
    c.drawRoundRect(skia.Rect.MakeLTRB(160, 640, 230, 1360), 14, 14, paint(shader=linear((160, 0), (230, 0), [col("#f7f9fb"), col(STEEL), col("#6d747e")])))
    ba = eout(prog(t, BUTM - 0.1, 0.4))
    ra = eout(prog(t, BOUNCE - 0.2, 0.4))
    for k in range(3):
        y = 720 + k * 230
        wave(c, 880, y - 60, 240, y + 40, 20, 70, t * 9 + k, WAVE, ba, 5)
        if ra > 0:
            wave(c, 240, y + 40, lerp(240, 880, ra), lerp(y + 40, y + 140, ra), 20, 70, -t * 9 + k, "#FFD38A", ra, 5)
        c.drawCircle(240, y + 40, 26, paint(WAVE, 0.45 * ba, blur=8))
    pill(c, t, "METAL?", 490, 540, STEEL, BUTM + 0.1, BOUNCE - 0.1)
    pill(c, t, "BOUNCES WAVES", 490, 540, WAVE, BOUNCE, ANT - 0.15)


def scene_fork(c, t):
    studio_dark(c)
    fx, fy, fs = 490, 1080, 1.6
    gl = prog(t, ANT, 0.4)
    fork(c, fx, fy, fs, 0, 1.0, glow=0.4 * prog(t, PILE, 0.6) + 0.6 * window(t, ZAP - 0.05, SPARKS + 0.9, 0.05, 0.4))
    # waves hitting the fork
    wa = eout(prog(t, ANT - 0.25, 0.3)) * (1 - prog(t, TIPS, 0.4))
    for k in range(3):
        wave(c, 900, 700 + k * 200, 600, 720 + k * 200, 18, 60, t * 10 + k, WAVE, 0.8 * wa, 4)
    # charges racing up the handle to the tips
    tp = tip_points(fx, fy, fs)
    ca = prog(t, TIPS - 0.2, 0.3) * (1 - prog(t, ZAP + 0.1, 0.2))
    if ca > 0:
        pile = prog(t, PILE, 1.0)
        for k in range(18):
            u = ((t * 0.9 + k / 18) % 1)
            tx, ty = tp[k % 4]
            if k < int(18 * pile):
                x = tx + 6 * math.sin(t * 20 + k); y = ty + 6 + 6 * math.cos(t * 17 + k)
            else:
                y = lerp(fy + 300 * fs, ty, u); x = lerp(fx, tx, prog(y, fy - 20 * fs, -1) if False else clamp((fy - y) / (60 * fs)))
            c.drawCircle(x, y, 9, paint(ZAPC, 0.3 * ca, blur=5)); c.drawCircle(x, y, 5, paint("#ffffff", ca))
    za = window(t, ZAP - 0.03, SPARKS + 1.0, 0.03, 0.4)
    if za > 0:
        for i in range(3):
            bolt(c, tp[i][0], tp[i][1], tp[i + 1][0], tp[i + 1][1] - 10, t, za, 5, seed=i)
        bolt(c, tp[0][0], tp[0][1], 220, 700, t, za * 0.9, 6, seed=7)
        bolt(c, tp[3][0], tp[3][1], 790, 660, t, za * 0.9, 6, seed=9)
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#e8f6ff", 0.4 * za * (1 - prog(t, ZAP, 0.2))))
    pill(c, t, "ANTENNA", 490, 540, STEEL, ANT, TIPS - 0.1)
    pill(c, t, "SHARP POINTS", 490, 540, ZAPC, PILE, ZAP - 0.05)
    pill(c, t, "SPARKS!", 490, 540, ZAPC, SPARKS, WIPE1 + 0.1)


# ---------------- white: metal walls, smooth vs sharp, mesh ----------------
def metal_box(c, t, a=1.0):
    # simple 3D open box (front face removed)
    fl, ft, fr, fb = 140, 640, 840, 1240
    d = 90
    c.drawRect(skia.Rect.MakeLTRB(fl + d, ft + d * 0.6, fr - d, fb - d * 0.6), paint(shader=linear((0, ft), (0, fb), [col("#e4e8ed", a), col("#aab1bb", a)])))
    for poly, cc in (([(fl, ft), (fl + d, ft + d * 0.6), (fl + d, fb - d * 0.6), (fl, fb)], "#c3c9d1"),
                     ([(fr, ft), (fr - d, ft + d * 0.6), (fr - d, fb - d * 0.6), (fr, fb)], "#b6bcc5"),
                     ([(fl, ft), (fr, ft), (fr - d, ft + d * 0.6), (fl + d, ft + d * 0.6)], "#dfe3e8"),
                     ([(fl, fb), (fr, fb), (fr - d, fb - d * 0.6), (fl + d, fb - d * 0.6)], "#9aa2ad")):
        p = skia.Path(); p.moveTo(*poly[0])
        for q in poly[1:]: p.lineTo(*q)
        p.close(); c.drawPath(p, paint(cc, a))
    c.drawRect(skia.Rect.MakeLTRB(fl, ft, fr, fb), paint("#7d858f", a, stroke=6))


def bouncing_waves(c, t, a):
    # a wave zig-zags between the walls
    for k in range(2):
        pts = []
        x, y, vx, vy = 300 + k * 200, 760 + k * 160, 1, 0.55 + 0.2 * k
        L = (t * 600 + k * 300) % 2400
        segs = []
        px, py = 250 + k * 80, 760 + k * 150
        dx, dy = 1.0, 0.6 + 0.25 * k
        n = 6
        for i in range(n):
            # find next wall hit inside [240,740]x[700,1180]
            tx = ((740 if dx > 0 else 240) - px) / dx
            ty = ((1180 if dy > 0 else 700) - py) / dy
            tt = min(tx, ty)
            nx2, ny2 = px + dx * tt, py + dy * tt
            segs.append((px, py, nx2, ny2))
            if tx < ty: dx = -dx
            else: dy = -dy
            px, py = nx2, ny2
        for i, (x0, y0, x1, y1) in enumerate(segs):
            ph = t * 10 + i
            wave(c, x0, y0, x1, y1, 12, 50, ph, WAVE, a * (0.95 - 0.12 * i), 4)
            c.drawCircle(x1, y1, 18, paint(WAVE, 0.35 * a, blur=8))


def charge_card(c, t, x, y, sharp, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    c.drawRoundRect(skia.Rect.MakeLTRB(-170, -150, 170, 150), 28, 28, paint("#000000", 0.12, blur=12))
    c.drawRoundRect(skia.Rect.MakeLTRB(-170, -150, 170, 150), 28, 28, paint("#ffffff"))
    if sharp:
        p = skia.Path(); p.moveTo(-120, 90); p.lineTo(0, -100); p.lineTo(120, 90); p.close()
        c.drawPath(p, paint(shader=linear((-120, 0), (120, 0), [col("#e3e7ec"), col("#8b929c")])))
        for k in range(10):
            c.drawCircle(4 * math.sin(t * 20 + k), -92 + 4 * math.cos(t * 17 + k) + k * 2, 7, paint(ZAPC))
        if int(t * 8) % 2 == 0:
            bolt(c, 0, -100, 40, -140, t, 0.9, 3, seed=3)
    else:
        c.drawRoundRect(skia.Rect.MakeLTRB(-130, -40, 130, 80), 60, 60, paint(shader=linear((0, -40), (0, 80), [col("#eef1f4"), col("#9aa2ad")])))
        for k in range(10):
            u = k / 9
            c.drawCircle(lerp(-110, 110, u), -40 + 18 * (1 - math.sin(u * math.pi)) - 6, 7, paint(GREEN))
    c.restore()


def mesh_scene(c, t, a):
    c.drawRoundRect(skia.Rect.MakeLTRB(120, 620, 860, 1280), 30, 30, paint("#000000", 0.12 * a, blur=16))
    c.drawRoundRect(skia.Rect.MakeLTRB(120, 620, 860, 1280), 30, 30, paint(shader=linear((0, 620), (0, 1280), [col("#3a3d42", a), col("#1f2124", a)])))
    for yy in range(650, 1260, 26):
        for xx in range(150, 850, 26):
            c.drawCircle(xx + (13 if (yy // 26) % 2 else 0), yy, 6, paint("#0b0b0c", a))
    # one big wave bouncing off the mesh (wave >> holes)
    u = (t * 0.8) % 1
    wa = a * prog(t, SMALLER - 0.2, 0.3)
    wave(c, 900, 640, 520, 820, 50, 260, t * 6, WAVE, wa, 10)
    c.drawCircle(520, 820, 40, paint(WAVE, 0.4 * wa, blur=10))
    wave(c, 520, 820, 900, 1060, 50, 260, -t * 6, WAVE, wa * 0.75, 10)


def scene_white(c, t):
    studio_white(c)
    ba = window(t, WIPE1 + 0.1, MESH - 0.1, 0.3, 0.25)
    if ba > 0:
        metal_box(c, t, ba)
        bouncing_waves(c, t, ba * prog(t, WALLS - 0.2, 0.4))
        ca = eback(prog(t, NOPTS - 0.15, 0.35)) * (1 - prog(t, BOUNCE2 + 0.3, 0.3))
        if ca > 0:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#F4F2EE", 0.75 * clamp(ca)))
            charge_card(c, t, 300, 960, False, clamp(ca))
            charge_card(c, t, 680, 960, True, clamp(ca))
            if ca > 0.8:
                f = skia.Font(TF_MONO, 26)
                for (x, txt, cc) in ((300, "SMOOTH = OK", GREEN), (680, "POINTY = ZAP", RED)):
                    c.drawString(txt, x - f.measureText(txt) / 2, 1160, f, paint(cc))
        pill(c, t, "METAL WALLS", 490, 540, "#7d858f", WALLS, SMOOTH - 0.1)
        pill(c, t, "NO SHARP POINTS", 490, 540, GREEN, NOPTS, BOUNCE2 - 0.05)
        pill(c, t, "WAVES BOUNCE", 490, 540, "#E39A2B", BOUNCE2, MESH - 0.15)
    ma = window(t, MESH - 0.15, WIPE2 + 0.2, 0.3, 0.2)
    if ma > 0:
        mesh_scene(c, t, ma)
        pill(c, t, "DOOR MESH", 490, 540, "#3a3d42", MESH, SMALLER - 0.1, text_col="#FFFFFF")
        pill(c, t, "1 MM HOLES", 300, 1340, "#3a3d42", SMALLER, WIPE2 + 0.1, text_col="#FFFFFF")
        pill(c, t, "12 CM WAVES", 680, 1340, "#E39A2B", SMALLER + 0.3, WIPE2 + 0.1)


# ---------------- dark: fire + keep out ----------------
def flame(c, x, y, s, t, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k, (cc, sc) in enumerate(((FIRE, 1.0), ("#FFB02E", 0.7), ("#FFF1A8", 0.4))):
        w = 1 + 0.05 * math.sin(t * 14 + k)
        p = skia.Path(); p.moveTo(0, -200 * sc * w); p.cubicTo(90 * sc, -80 * sc, 110 * sc, 40 * sc, 0, 90 * sc)
        p.cubicTo(-110 * sc, 40 * sc, -90 * sc, -80 * sc, 0, -200 * sc * w); p.close()
        c.drawPath(p, paint(cc, a, blur=2 if k else 6))
    c.restore()


def icon_card(c, x, y, kind, t, a, crossed):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    c.drawRoundRect(skia.Rect.MakeLTRB(-120, -120, 120, 120), 30, 30, paint("#2a2729"))
    c.drawRoundRect(skia.Rect.MakeLTRB(-120, -120, 120, 120), 30, 30, paint("#ffffff", 0.12, stroke=2))
    if kind == "fork":
        fork(c, 0, 40, 0.42, 30)
    elif kind == "foil":
        p = skia.Path(); r = random.Random(3)
        pts = [(math.cos(i / 9 * 6.28) * r.uniform(55, 80), math.sin(i / 9 * 6.28) * r.uniform(45, 70)) for i in range(9)]
        p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        p.close(); c.drawPath(p, paint(shader=linear((-70, -60), (70, 60), [col("#ffffff"), col("#9aa2ad"), col("#e3e7ec")])))
        for i in range(5):
            c.drawLine(*pts[i], *pts[(i + 4) % 9], paint("#7d858f", 0.6, stroke=2))
    else:
        p = skia.Path(); p.moveTo(-80, 20); p.cubicTo(-30, -60, 10, 60, 40, -10); p.cubicTo(55, -40, 75, -30, 85, -50)
        c.drawPath(p, paint("#e8e8e8", 1, stroke=12)); c.drawPath(p, paint("#c9ced6", 1, stroke=5))
    if crossed > 0:
        c.drawLine(-90, -90, lerp(-90, 90, crossed), lerp(-90, 90, crossed), paint(RED, 1, stroke=14))
    c.restore()


def scene_fire(c, t):
    studio_dark(c)
    fa = eback(prog(t, FIREt - 0.15, 0.4)) * (1 - prog(t, OUT, 0.3))
    if fa > 0:
        flame(c, 490, 1080, 1.4 * clamp(fa), t, clamp(fa))
        bolt(c, 380, 760, 470, 900, t, clamp(fa) * (int(t * 10) % 2), 5)
    for i, (k, x) in enumerate((("fork", 230), ("foil", 490), ("tie", 750))):
        ia = eback(prog(t, OUT + 0.1 + i * 0.3, 0.35))
        icon_card(c, x, 1000, k, t, clamp(ia), eout(prog(t, OUT + 0.3 + i * 0.3, 0.25)))
    pill(c, t, "FIRE RISK", 490, 540, FIRE, FIREt, OUT - 0.05)
    pill(c, t, "KEEP METAL OUT", 490, 540, RED, OUT + 0.2, SO + 0.4)


def draw_world(c, t):
    if t < WAVES - 0.2:
        scene_hook(c, t)
        return
    if t < BUTM - 0.1:
        scene_inside(c, t)
        q = 1 - prog(t, WAVES - 0.2, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_hook(c, t); c.restore()
        return
    if t < ANT - 0.25:
        scene_mirror(c, t); return
    if t < WIPE1 + WL / 2:
        scene_fork(c, t); return
    if t < WIPE2 + WL / 2:
        scene_white(c, t); return
    if t < SO - 0.05:
        scene_fire(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    hook_scene(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_fire(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.022 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"NOT": RED, "waves": WAVE, "bounces": WAVE, "antenna": STEEL, "tips": ZAPC, "ZAP": ZAPC, "sparks": ZAPC,
         "metal": "#8a929c", "sharp points": GREEN, "mesh": "#8a929c", "smaller": "#E39A2B", "fire": FIRE, "out": RED}
CAPS = Captions(P, KWCOL, {"NOT", "ZAP!"}, DUR)


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
    wipe(c, t, WIPE1, WL, ZAPC, "#F4F2EE")
    wipe(c, t, WIPE2, WL, FIRE, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("hit", NOT), ("riser", YOUSEE - 0.2), ("whoosh", WAVES - 0.2), ("pop", WAVES), ("pop", SHAKE),
          ("whoosh", BUTM - 0.1), ("pop", BOUNCE), ("whoosh", ANT - 0.25), ("pop", ANT), ("riser", PILE - 0.3),
          ("hit", ZAP), ("pop", SPARKS), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", WALLS), ("pop", NOPTS),
          ("whoosh", MESH - 0.15), ("pop", SMALLER), ("whoosh", WIPE2), ("hit", FIREt), ("pop", OUT + 0.1),
          ("pop", OUT + 0.4), ("pop", OUT + 0.7), ("whoosh", SO - 0.05)]
    for k in range(5):
        ev.append(("tick", TIPS + k * 0.2))
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

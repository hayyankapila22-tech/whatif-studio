import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
TONE = os.environ.get("TONE", "#D7A47E")
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
COBALT = "#3B5BDB"; BLOOD = "#C2504A"
TONE_DARK = mixhex(TONE, "#3a2418", 0.38)
TONE_LIGHT = mixhex(TONE, "#ffffff", 0.28)


def p0(i):
    return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


# ---------------- beats ----------------
NOTWATER = kw(1)
SWATCH = p0(3) - 0.1
XSEC = p0(5) - 0.35
NERVES = kw(5)
FIVE = kw(6); NOTICE = kw(7)
SIGNAL = p0(8); BRAIN = kw(9)
STRANGE = kw(10)
VESSELS = kw(11)
SHRINK = kw(13)
SAMESIZE = kw(15)
BUCKLE = kw(16)
PROOF = p0(18) - 0.3
DAMAGED = kw(19); WONT = kw(20)
WIPE1 = p0(21) - 0.3
FOR = kw(22)
Y2013 = p0(23); MARBLES = kw(24)
RACE1 = p0(25); PCT = kw(26)
TREADS = kw(27)
NOTEX = kw(30)
RACE2 = p0(31); REPEATED = kw(32)
NODIFF = kw(33)
ARGUE = kw(34)
WIPE2 = p0(35) - 0.3
SAMEPAT = kw(36)
TIMEW = kw(37)
LOOP = p0(38) - 0.3
WL = 0.32
IMPACTS = [BUCKLE, NOTEX]


def mode_at(t):
    if t < XSEC + 0.45: return "pad1"
    if t < PROOF + 0.4: return "xsec"
    if t < WIPE1 + WL / 2: return "pads2"
    if t < WIPE2 + WL / 2: return "white"
    if t < LOOP + 0.45: return "pad3"
    return "end"


def light_at(t):
    return mode_at(t) == "white"


rnd = random.Random(7)
BUBBLES = [(rnd.uniform(0, W), rnd.random(), rnd.uniform(3, 11), rnd.uniform(0.05, 0.12), rnd.random() * 6.28) for _ in range(34)]
# wrinkle curves on pad (local coords, pad radius 260, centre of tip arc at y=0)
WR = []
for i in range(9):
    x0 = -190 + i * 47.5 + rnd.uniform(-8, 8)
    y0 = -200 + abs(x0) * 0.55 + rnd.uniform(-20, 20)
    WR.append((x0, y0, rnd.uniform(380, 640), rnd.uniform(0, 6.28), rnd.uniform(12, 22)))
TRANS = [(rnd.uniform(-150, 150), rnd.uniform(-170, -60), rnd.uniform(60, 120), rnd.uniform(-0.3, 0.3)) for _ in range(2)]


# ---------------- underwater background ----------------
def bath_bg(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.4, 1400, [col("#16294a"), col("#0b1426"), col("#05080f")], [0, 0.5, 1])))
    for k in range(6):
        p = skia.Path()
        y0 = 200 + k * 300 + 40 * math.sin(t * 0.4 + k)
        p.moveTo(-50, y0)
        for x in range(-50, W + 60, 40):
            p.lineTo(x, y0 + 30 * math.sin(x / 140 + t * 0.9 + k * 1.3) + 15 * math.sin(x / 50 - t * 1.4))
        c.drawPath(p, paint("#9fc2ff", 0.05, stroke=14, blur=10))


def bubbles(c, t, a=1.0):
    for (x, ph, r, sp, ph2) in BUBBLES:
        u = (t * sp + ph) % 1
        y = H + 40 - u * (H + 120)
        xx = x + 14 * math.sin(t * 1.3 + ph2)
        aa = a * 0.5 * min(1, u * 8) * min(1, (1 - u) * 8)
        c.drawCircle(xx, y, r, paint("#cfe0ff", 0.35 * aa, stroke=1.6))
        c.drawCircle(xx - r * 0.35, y - r * 0.35, r * 0.28, paint("#ffffff", 0.7 * aa))


# ---------------- fingertip pad (front view) ----------------
R = 260


def pad_outline(amp):
    p = skia.Path()
    n = 90
    pts = []
    for k in range(n + 1):  # left side up
        y = 1300 - k * (1300 / n)
        pts.append((-R, y))
    for k in range(1, 60):  # arc over tip
        th = math.pi + k * math.pi / 60
        pts.append((R * math.cos(th), R * math.sin(th) * 1.15))
    for k in range(n + 1):
        y = k * (1300 / n)
        pts.append((R, y))
    out = []
    for i, (x, y) in enumerate(pts):
        if y < 700:
            ang = math.atan2(y, x)
            bump = amp * 3.5 * math.sin(i * 0.9) * (1 if y < 600 else (700 - y) / 100)
            x += bump * math.cos(ang); y += bump * math.sin(ang) * 0.5
        out.append((x, y))
    p.moveTo(*out[0])
    for q in out[1:]:
        p.lineTo(*q)
    p.close()
    return p


def wrinkle_paths(dx=0):
    paths = []
    for (x0, y0, L, ph, wig) in WR:
        p = skia.Path(); first = True
        for k in range(40):
            y = y0 + k * L / 39
            x = x0 * (1 - 0.0004 * max(0, y)) + wig * math.sin(y / 62 + ph) + dx
            p.moveTo(x, y) if first else p.lineTo(x, y)
            first = False
        paths.append(p)
    for (x, y, L, ang) in TRANS:
        p = skia.Path(); p.moveTo(x - L / 2, y - ang * L / 2)
        p.quadTo(x, y + 14, x + L / 2, y + ang * L / 2)
        paths.append(p)
    return paths


WPATHS = wrinkle_paths()


def pad(c, t, cx, cy, s, amp, extra=None, nerve_icon=None):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    br = 1 + 0.005 * math.sin(t * 1.8)
    c.scale(br, br)
    outline = pad_outline(amp)
    c.drawPath(outline, paint("#000000", 0.45, blur=30))
    c.drawPath(outline, paint(shader=linear((-R, 0), (R, 0), [col(TONE_DARK), col(TONE), col(TONE_LIGHT), col(TONE), col(TONE_DARK)], [0, 0.18, 0.42, 0.75, 1])))
    c.save(); c.clipPath(outline)
    c.drawRect(skia.Rect.MakeLTRB(-R - 20, -R * 1.3, R + 20, 1300), paint(shader=radial(-60, -140, 520, [col("#ffffff", 0.22), col("#ffffff", 0)])))
    # fingerprint whorl
    for k in range(16):
        rx = 30 + k * 19; ry = rx * 1.25
        c.drawOval(skia.Rect.MakeLTRB(-rx + 10, 120 - ry, rx + 10, 120 + ry), paint(TONE_DARK, 0.16 * (1 - 0.6 * amp), stroke=2.2))
    # wrinkles: groove + crest
    if amp > 0.01:
        for p in WPATHS:
            c.save(); c.translate(4, 5)
            c.drawPath(p, paint("#3a1f12", 0.30 * amp, stroke=16 * amp, blur=6))
            c.restore()
            c.drawPath(p, paint(TONE_DARK, 0.38 * amp, stroke=4 * amp, blur=1.5))
            c.save(); c.translate(-9, -7)
            c.drawPath(p, paint(TONE_LIGHT, 0.45 * amp, stroke=10 * amp, blur=5))
            c.restore()
    if extra:
        extra(c)
    # water tint
    c.drawRect(skia.Rect.MakeLTRB(-R - 20, -R * 1.3, R + 20, 1300), paint(COBALT, 0.12))
    c.restore()
    c.drawPath(outline, paint("#cfe0ff", 0.25, stroke=3, blur=2))
    c.restore()


# ---------------- fingertip cross-section ----------------
FW2 = 220


def xs_outline(amp):
    pts = []
    for k in range(80):  # left (pad) side, bottom -> top
        y = 900 - k * (1240 / 79)
        x = -FW2
        if -470 < y < 380:
            x -= amp * 16 * abs(math.sin(y * math.pi / 64))
        pts.append((x, y))
    for k in range(1, 50):
        th = math.pi + k * math.pi / 50
        x = FW2 * math.cos(th); y = -340 + 220 * math.sin(th)
        if math.cos(th) < 0.3:
            r = amp * 14 * abs(math.sin(k * 0.55))
            x += r * math.cos(th); y += r * math.sin(th)
        pts.append((x, y))
    for k in range(80):
        y = -340 + k * (1240 / 79)
        pts.append((FW2, y))
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def xs_inner(shrink):
    inset = 30 + 16 * shrink
    p = skia.Path()
    p.moveTo(-FW2 + inset, 900)
    p.lineTo(-FW2 + inset, -340)
    p.arcTo(skia.Rect.MakeLTRB(-FW2 + inset, -560 + inset, FW2 - inset, -120 - inset), 180, 180, False)
    p.lineTo(FW2 - inset, 900)
    p.close()
    return p


NERVE = skia.Path()
NERVE.moveTo(-130, 900); NERVE.cubicTo(-150, 500, -160, 0, -150, -300); NERVE.cubicTo(-145, -400, -100, -470, -40, -500)
NERVE2 = skia.Path()
NERVE2.moveTo(-150, -260); NERVE2.cubicTo(-175, -320, -185, -380, -170, -430)
NLEN = skia.PathMeasure(NERVE, False).getLength()
VESS = []
for k in range(7):
    p = skia.Path()
    y0 = 760 - k * 180
    p.moveTo(-90, y0)
    p.cubicTo(-140, y0 - 50, -200, y0 - 40, -175, y0 - 110)
    p.cubicTo(-160, y0 - 150, -110, y0 - 160, -95, y0 - 190)
    VESS.append(p)
VTRUNK = skia.Path(); VTRUNK.moveTo(-90, 900); VTRUNK.cubicTo(-100, 400, -80, -100, -40, -460)


def xsection(c, t, cx, cy, s, st):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    amp = st.get("amp", 0); shrink = st.get("shrink", 0); con = st.get("constrict", 0)
    out = xs_outline(amp)
    c.drawPath(out, paint("#000000", 0.4, blur=30))
    c.drawPath(out, paint(shader=linear((-FW2, 0), (FW2, 0), [col(TONE_DARK), col(TONE), col(TONE_LIGHT), col(TONE_DARK)], [0, 0.2, 0.6, 1])))
    seep = st.get("seep", 0)
    if seep > 0:
        c.drawPath(out, paint(COBALT, 0.45 * seep * (0.6 + 0.4 * math.sin(t * 5)), stroke=10, blur=4))
    inner = xs_inner(shrink)
    c.drawPath(inner, paint(shader=linear((0, -560), (0, 900), [col("#F4CDB0"), col("#EBBE9E"), col("#E6B795")])))
    c.save(); c.clipPath(inner)
    for i in range(7):
        for j in range(16):
            x = -170 + i * 56 + (j % 2) * 28; y = -420 + j * 80
            c.drawCircle(x, y, 24, paint("#d9a888", 0.45, stroke=1.6))
    # bone
    b = skia.Path()
    b.moveTo(10, 900); b.lineTo(15, -200); b.cubicTo(-30, -260, -20, -330, 40, -350)
    b.cubicTo(120, -350, 150, -270, 105, -200); b.lineTo(110, 900); b.close()
    c.drawPath(b, paint(shader=linear((10, 0), (110, 0), [col("#F5EFE2"), col("#E3D8C2")])))
    c.drawPath(b, paint("#b8ab92", 0.7, stroke=2))
    # vessels
    vw = lerp(9, 3.2, con)
    vc = mixhex(BLOOD, "#9b7d7a", con * 0.7)
    for p in VESS + [VTRUNK]:
        c.drawPath(p, paint(vc, 0.95, stroke=vw))
        c.drawPath(p, paint("#ffffff", 0.18, stroke=max(vw * 0.3, 1)))
    # nerve
    nb = st.get("nerve", 0)
    if nb > 0:
        for p in (NERVE, NERVE2):
            c.drawPath(p, paint(YELLOW, 0.35 * nb, stroke=16, blur=8))
            c.drawPath(p, paint("#E8C547", nb, stroke=6))
        pm = skia.PathMeasure(NERVE, False)
        for mode, a in (("out", st.get("out", 0)), ("back", st.get("back", 0))):
            if a <= 0:
                continue
            for k in range(5):
                u = (t * 0.9 + k / 5) % 1
                d = NLEN * (1 - u) if mode == "out" else NLEN * u
                pos, _ = pm.getPosTan(d)
                c.drawCircle(pos.x(), pos.y(), 22, paint(YELLOW, 0.35 * a, blur=8))
                c.drawCircle(pos.x(), pos.y(), 9, paint("#FFF6C8", a))
    c.restore()
    # shrink arrows
    sa = st.get("arrows", 0)
    if sa > 0:
        for y in (-200, 50, 300):
            x0 = -FW2 + 8
            c.drawLine(x0, y, x0 + 40 * sa, y, paint("#ffffff", sa, stroke=4))
            c.drawPath(arrowhead(x0 + 40 * sa + 8, y, 1, 0, 10), paint("#ffffff", sa))
    # nail
    nl = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(FW2 - 14, -480, FW2 + 14, -60), 14, 14)
    c.drawRRect(nl, paint(shader=linear((FW2 - 14, 0), (FW2 + 14, 0), [col("#F2D6CC"), col("#FFF2EC"), col("#E9C6BA")])))
    c.drawRRect(nl, paint("#c79f93", 0.7, stroke=1.5))
    c.restore()


def arrowhead(x, y, dx, dy, s):
    p = skia.Path(); nx, ny = -dy, dx
    p.moveTo(x + dx * s, y + dy * s); p.lineTo(x + nx * s * 0.7, y + ny * s * 0.7); p.lineTo(x - nx * s * 0.7, y - ny * s * 0.7); p.close()
    return p


# ---------------- white chapter props ----------------
MARB = [(-150, 30, 34), (-70, 60, 30), (10, 40, 36), (95, 65, 30), (160, 30, 28), (-110, -10, 26), (60, 0, 28)]


def bowl(c, t, cx, cy, s, a=1.0):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-260, 150, 260, 190), paint("#000000", 0.18 * a, blur=16))
    p = skia.Path(); p.moveTo(-250, -90); p.cubicTo(-250, 150, 250, 150, 250, -90); p.close()
    c.drawPath(p, paint("#dfe8f5", 0.5 * a))
    w = skia.Path(); w.moveTo(-238, -40)
    for x in range(-238, 239, 12):
        w.lineTo(x, -40 + 4 * math.sin(x / 30 + t * 2))
    w.cubicTo(238, 120, -238, 120, -238, -40)
    c.drawPath(w, paint(shader=linear((0, -40), (0, 130), [col("#6f8ff0", 0.55 * a), col(COBALT, 0.7 * a)])))
    for (x, y, r) in MARB:
        yy = y + 4 * math.sin(t * 1.6 + x)
        c.drawCircle(x, yy, r, paint(shader=radial(x - r * 0.4, yy - r * 0.4, r * 1.5, [col("#ffffff", a), col("#9fb6ff", 0.9 * a), col("#2f4cc2", 0.95 * a)], [0, 0.4, 1])))
        c.drawCircle(x - r * 0.35, yy - r * 0.4, r * 0.22, paint("#ffffff", 0.9 * a))
    c.drawPath(p, paint("#9aa9c2", 0.8 * a, stroke=4))
    c.drawLine(-262, -90, 262, -90, paint("#9aa9c2", 0.8 * a, stroke=6))
    c.restore()


def race(c, t, t0, d_w, d_s, a, label_y=990):
    f = skia.Font(TF_MONO, 26)
    for i, (lab, d) in enumerate((("SMOOTH", d_s), ("WRINKLY", d_w))):
        y = label_y + i * 110
        q = eio(prog(t, t0, d))
        c.drawString(lab, 120, y, f, paint(INK, 0.8 * a))
        tr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(120, y + 18, 820, 40), 20, 20)
        c.drawRRect(tr, paint(INK, 0.08 * a))
        if q > 0:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(120, y + 18, 820 * q, 40), 20, 20), paint(COBALT if lab == "WRINKLY" else "#8c93a6", a))
            c.drawCircle(120 + 820 * q - 20, y + 38, 13, paint("#ffffff", a))


def tyre(c, t, cx, cy, r, a):
    c.save(); c.translate(cx, cy)
    c.drawOval(skia.Rect.MakeLTRB(-r, r - 10, r, r + 24), paint("#000000", 0.18 * a, blur=12))
    c.rotate(t * 120)
    c.drawCircle(0, 0, r, paint("#2a2a2c", a))
    for k in range(18):
        c.save(); c.rotate(k * 20)
        c.drawRoundRect(skia.Rect.MakeXYWH(-7, -r - 1, 14, 30), 4, 4, paint("#f2f0ec", a))
        c.restore()
    c.drawCircle(0, 0, r * 0.55, paint("#c9ccd2", a))
    c.drawCircle(0, 0, r * 0.18, paint("#8a8f98", a))
    c.restore()
    for k in range(8):
        u = (t * 1.3 + k / 8) % 1
        x = cx + r * 0.9 + u * 140; y = cy + r * 0.6 - 60 * u + 120 * u * u
        c.drawCircle(x, y, 8 * (1 - u * 0.5), paint(COBALT, a * (1 - u)))


# ---------------- scene drawing ----------------
def amp_pad1(t):
    return clamp(0.25 + 0.75 * eio(prog(t, 0, 4.0)))


def draw_pad1(c, t, end=False):
    bath_bg(c, t)
    if not end:
        push = 1 + 0.03 * prog(t, 0, XSEC)
        dive = ein(prog(t, XSEC, 0.45))
        sc = push * (1 + 1.8 * dive)
        amp = amp_pad1(t)
    else:
        sc = lerp(1.03, 1.0, eio(prog(t, LOOP, DUR - 0.4 - LOOP)))
        amp = lerp(1.0, 0.25, eio(prog(t, LOOP, DUR - 0.4 - LOOP)))
    dim = 0.0 if end else 0.55 * window(t, SWATCH, XSEC, 0.3, 0.3)
    pad(c, t, 540, 820 + 0 * sc, 1.25 * sc, amp)
    if dim > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#05080f", dim))
    bubbles(c, t)
    if end:
        footnote(c, t, "Sources: Biology Letters 2013 · PLOS ONE 2014 · J. Mech. Behav. Biomed. Mater. 2025", DUR - 2.1, DUR + 1)
        return
    # myth pill
    if NOTWATER - 0.05 < t < NOTWATER + 1.6:
        fall = ein(prog(t, NOTWATER + 0.75, 0.6))
        c.save(); c.translate(0, 600 * fall); c.rotate(10 * fall)
        pill(c, t, "WATER SOAKING IN?", 540, 1060, COBALT, NOTWATER, NOTWATER + 1.3)
        sp = eout(prog(t, NOTWATER + 0.3, 0.2))
        if sp > 0:
            c.drawLine(380, 1062, lerp(380, 700, sp), 1058, paint(RED, 1 - prog(t, NOTWATER + 1.2, 0.2), stroke=6))
        c.restore()
    # swatches
    sw = eback(prog(t, SWATCH, 0.4), 1.1) * (1 - prog(t, XSEC - 0.1, 0.3))
    if sw > 0:
        for (x, lab, a_) in ((300, "ARM", 0.0), (780, "FINGERTIP", amp)):
            c.save(); c.translate(x, 1130); c.scale(sw, sw)
            clip = skia.Path().addCircle(0, 0, 170)
            c.drawCircle(4, 10, 172, paint("#000000", 0.4, blur=16))
            c.save(); c.clipPath(clip)
            if lab == "ARM":
                c.drawCircle(0, 0, 170, paint(shader=radial(-50, -60, 260, [col(TONE_LIGHT), col(TONE), col(TONE_DARK)], [0, 0.55, 1])))
                for k in range(12):
                    c.drawLine(-120 + k * 22, -40 + (k % 3) * 30, -100 + k * 22, -60 + (k % 3) * 30, paint(TONE_DARK, 0.35, stroke=1.4))
            else:
                pad(c, t, 0, 160, 1.1, a_)
            c.restore()
            c.drawCircle(0, 0, 170, paint("#ffffff", 0.9, stroke=4))
            c.restore()
        pill(c, t, "ARM", 300, 1345, "#FFFFFF", SWATCH + 0.2, XSEC)
        pill(c, t, "FINGERTIP", 780, 1345, "#FFFFFF", SWATCH + 0.35, XSEC)
        footnote(c, t, "Simplified", SWATCH + 0.3, XSEC)
    if t > XSEC:
        a = eout(prog(t, XSEC + 0.2, 0.25))
        c.saveLayerAlpha(None, int(255 * a)); draw_xsec(c, t); c.restore()


def xstate(t):
    st = {}
    st["nerve"] = eout(prog(t, NERVES - 0.1, 0.5))
    st["seep"] = window(t, FIVE, SIGNAL + 0.3, 0.4, 0.4)
    st["out"] = window(t, SIGNAL, STRANGE, 0.2, 0.3)
    st["back"] = window(t, STRANGE + 0.5, VESSELS + 1.2, 0.2, 0.3)
    st["constrict"] = eio(prog(t, VESSELS, 0.9))
    st["shrink"] = eio(prog(t, SHRINK, 0.9))
    st["arrows"] = window(t, SHRINK, SAMESIZE + 0.4, 0.3, 0.3)
    st["amp"] = eback(prog(t, BUCKLE, 0.45), 1.6)
    return st


def draw_xsec(c, t):
    bath_bg(c, t)
    settle = eout(prog(t, XSEC + 0.2, 0.9))
    s = lerp(1.3, 1.0, settle) * (1 + 0.04 * prog(t, XSEC, PROOF - XSEC))
    cx, cy = 560, 1150
    xsection(c, t, cx, cy, s, xstate(t))
    bubbles(c, t, 0.6)
    L = lambda x, y: (cx + x * s, cy + y * s)
    pill(c, t, "NERVE", 230, 690, YELLOW, NERVES, SIGNAL, anchor=L(-150, -300))
    if SIGNAL < t < STRANGE + 0.3:
        pill(c, t, "↓ TO BRAIN", 330, 1440, YELLOW, BRAIN - 0.1, STRANGE)
    pill(c, t, "BLOOD VESSELS", 800, 1440, BLOOD, VESSELS, SHRINK, anchor=L(-150, 300))
    pill(c, t, "SAME SKIN", 230, 690, "#FFFFFF", SAMESIZE, BUCKLE + 0.2, anchor=L(-FW2 - 6, -250))
    pill(c, t, "WRINKLES", 230, 690, "#FFFFFF", BUCKLE + 0.15, PROOF, anchor=L(-FW2 - 14, -150))
    footnote(c, t, "Warm water; timing varies", FIVE, SIGNAL + 0.3)
    footnote(c, t, "Magnified illustration · exaggerated for clarity", SIGNAL + 0.4, PROOF + 0.3)
    if t > PROOF:
        a = eout(prog(t, PROOF, 0.4))
        c.saveLayerAlpha(None, int(255 * a)); draw_pads2(c, t); c.restore()


def nerve_icon(c, x, y, broken, a):
    c.drawLine(x - 90, y, x - (14 if broken else -90), y, paint("#E8C547", a, stroke=6))
    if broken:
        c.drawLine(x + 14, y, x + 90, y, paint("#E8C547", a, stroke=6))
        c.drawLine(x - 10, y - 12, x + 10, y + 12, paint(RED, a, stroke=5))
        c.drawLine(x - 10, y + 12, x + 10, y - 12, paint(RED, a, stroke=5))


def draw_pads2(c, t):
    bath_bg(c, t)
    sl = eout(prog(t, PROOF, 0.6))
    ampL = eio(prog(t, DAMAGED - 0.6, 1.5))
    pad(c, t, lerp(400, 290, sl), 900, 0.72, ampL)
    pad(c, t, lerp(680, 790, sl), 900, 0.72, 0.0)
    bubbles(c, t, 0.6)
    a = eout(prog(t, DAMAGED - 0.2, 0.3))
    nerve_icon(c, 290, 1320, False, a); nerve_icon(c, 790, 1320, True, a)
    pill(c, t, "NERVE OK", 290, 1400, YELLOW, DAMAGED - 0.1, WIPE1 + 0.2)
    pill(c, t, "NERVE DAMAGED", 790, 1400, RED, DAMAGED, WIPE1 + 0.2)
    pill(c, t, "NO WRINKLES", 790, 660, "#FFFFFF", WONT, WIPE1 + 0.2)
    footnote(c, t, "Observed in patients since the 1930s", DAMAGED, WIPE1 + 0.3)


def draw_white(c, t):
    studio_white(c)
    # bowl: big, then shrinks to top-left
    bs = eio(prog(t, RACE1 - 0.3, 0.6))
    ba = 1 - prog(t, NOTEX, 0.3) * 0
    bowl(c, t, lerp(540, 290, bs), lerp(1000, 690, bs), lerp(1.4, 0.62, bs), ba)
    pill(c, t, "2013 · 20 PEOPLE", lerp(540, 760, bs), lerp(700, 640, bs), COBALT, MARBLES - 0.1, TREADS - 0.2, light=True)
    # race 1
    ra = window(t, RACE1 - 0.2, RACE2 - 0.05, 0.3, 0.3)
    if ra > 0:
        race(c, t, RACE1 + 0.1, 1.9, 1.9 * 1.12, ra)
    # counter
    ca = eout(prog(t, PCT - 0.1, 0.25)) * (1 - prog(t, NOTEX + 0.5, 0.4))
    if ca > 0:
        v = 12 * eexpo(prog(t, PCT, 0.8))
        pulse = 1 + 0.06 * math.sin(math.pi * prog(t, PCT + 0.8, 0.25))
        big_number(c, f"{int(round(v))}%", "FASTER", 540, 1420, 150, COBALT, ca, pulse)
        cr = eout(prog(t, NOTEX, 0.2))
        if cr > 0:
            p = skia.Path(); p.moveTo(330, 1300)
            for (x, y) in ((420, 1350), (470, 1320), (560, 1390), (620, 1350), (760, 1420)):
                p.lineTo(x, y)
            pp = paint(RED, ca, stroke=6)
            if cr < 0.999:
                te = skia.TrimPathEffect.Make(0, cr)
                if te: pp.setPathEffect(te)
            c.drawPath(p, pp)
    # tyre
    ta = window(t, TREADS - 0.1, NOTEX + 0.4, 0.3, 0.3)
    if ta > 0:
        tyre(c, t, 790, 690, 130 * eback(prog(t, TREADS - 0.1, 0.4)), ta)
    # race 2
    r2 = window(t, RACE2 - 0.1, ARGUE + 0.1, 0.3, 0.3)
    if r2 > 0:
        d = NODIFF - REPEATED
        race(c, t, REPEATED, d, d, r2)
        pill(c, t, "2014 · 40 PEOPLE", 760, 640, RED, RACE2, WIPE2, light=True)
    na = window(t, NODIFF, ARGUE + 0.1, 0.25, 0.25)
    if na > 0:
        f = skia.Font(TF_BLACK, 96); s = "= NO DIFFERENCE"
        c.drawString(s, 540 - f.measureText(s) / 2, 1400, f, paint(INK, na))
    # debate
    if t > ARGUE - 0.1:
        pill(c, t, "2013: YES", 280, 1180, COBALT, ARGUE, WIPE2 + 0.2, light=True)
        pill(c, t, "2014: NO", 800, 1180, RED, ARGUE + 0.15, WIPE2 + 0.2, light=True)
        qa = eback(prog(t, ARGUE + 0.3, 0.3))
        f = skia.Font(TF_BLACK, 200)
        c.save(); c.translate(540, 1200); c.scale(qa, qa)
        c.drawString("?", -f.measureText("?") / 2, 70, f, paint(INK, clamp(qa)))
        c.restore()
    footnote(c, t, "Kareklas, Nettle & Smulders 2013 · Biology Letters", MARBLES, NOTEX, light=True)
    footnote(c, t, "Haseleu et al. 2014 · PLOS ONE", RACE2, WIPE2 + 0.2, light=True)


def draw_pad3(c, t):
    bath_bg(c, t)
    pad(c, t, 540, 820, 1.25, 1.0)
    # vessel map + day outlines in pad space
    va = eout(prog(t, SAMEPAT - 0.2, 0.6))
    conv = eio(prog(t, SAMEPAT, 1.0))
    oa = eout(prog(t, WIPE2 + 0.4, 0.4)) * (1 - prog(t, LOOP, 0.3))
    c.save(); c.translate(540, 820); c.scale(1.25, 1.25)
    for (dx, colr) in ((-70 * (1 - conv), COBALT), (70 * (1 - conv), YELLOW)):
        c.save(); c.translate(dx, 0)
        for p in WPATHS:
            c.drawPath(p, paint(colr, 0.85 * oa, stroke=3))
        c.restore()
    if va > 0:
        for p in WPATHS:
            c.save(); c.translate(0, 0)
            c.drawPath(p, paint(BLOOD, 0.35 * va * (1 - prog(t, LOOP, 0.3)), stroke=14, blur=8))
            c.restore()
    c.restore()
    bubbles(c, t)
    f = skia.Font(TF_MONO, 24)
    da = oa * (1 - conv)
    c.drawString("DAY 1", 150, 640, f, paint(COBALT, da)); c.drawString("DAY 2", 840, 640, f, paint(YELLOW, da))
    pill(c, t, "SAME MAP ✓", 540, 1420, "#FFFFFF", SAMEPAT + 0.8, LOOP)
    footnote(c, t, "Laytin & German 2025 · small study (3 people)", SAMEPAT - 0.2, LOOP + 0.3)
    if t > LOOP:
        a = eout(prog(t, LOOP, 0.45))
        c.saveLayerAlpha(None, int(255 * a)); draw_pad1(c, t, end=True); c.restore()


def draw_world(c, t):
    m = mode_at(t)
    if m == "pad1": draw_pad1(c, t)
    elif m == "xsec": draw_xsec(c, t)
    elif m == "pads2": draw_pads2(c, t)
    elif m == "white": draw_white(c, t)
    elif m == "pad3": draw_pad3(c, t)
    else: draw_pad1(c, t, end=True)


def hud_val(t):
    m = mode_at(t)
    if m == "white":
        if t < RACE2: return ("GRIP TEST", "RUN 1 · 2013", COBALT)
        if t < ARGUE: return ("GRIP TEST", "RUN 2 · 2014", RED)
        return ("GRIP TEST", "DEBATED", "#8a8a8a")
    if t < FIVE - 0.2:
        return ("SOAK TIME", f"00:{int(t):02d}", COBALT)
    secs = lerp(int(FIVE - 0.2), 300, eexpo(prog(t, FIVE - 0.2, 1.8)))
    if m in ("pad3",):
        secs = 300 + (t - WIPE2) * 30
    return ("SOAK TIME", f"{int(secs) // 60:02d}:{int(secs) % 60:02d}", COBALT)


KWCOL = {"water": COBALT, "nerves": YELLOW, "notice": YELLOW, "brain": YELLOW, "strange": YELLOW,
         "blood": BLOOD, "damaged": RED, "won't": RED, "marbles": COBALT, "12%": COBALT, "not exactly": RED,
         "no difference": "#FFFFFF", "same pattern": "#FFFFFF"}
CAPS = Captions(P, KWCOL, {"12%", "won't", "not"}, DUR)


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    sx = sy = 0
    for ti in IMPACTS:
        d = t - ti
        if 0 <= d < 0.33:
            amp = 9 * (1 - d / 0.33)
            sx += amp * math.sin(d * 97); sy += amp * math.cos(d * 83)
    c.save(); c.translate(sx, sy)
    draw_world(c, t)
    c.restore()
    light = light_at(t)
    dust(c, t, light)
    vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 620), paint(shader=linear((0, 0), (0, 620), [col("#000000", 0.45), col("#000000", 0)])))
    lab, val, dc = hud_val(t)
    ha = prog(t, 0.3, 0.3) * (1 - prog(t, LOOP - 0.3, 0.3))
    hud(c, t, lab, val, dc, ha, light)
    rw = math.sin(math.pi * prog(t, NOTEX, 0.45))
    if rw > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.24 * rw))
    for ti in IMPACTS:
        if 0 <= t - ti < 2 / FPS:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#FFFFFF", 0.3))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, COBALT, "#F4F2EE")
    wipe(c, t, WIPE2, WL, COBALT, INK)
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("pop", NOTWATER), ("tick", NOTWATER + 0.3), ("pop", SWATCH + 0.2), ("pop", SWATCH + 0.35), ("whoosh", XSEC),
          ("pop", NERVES), ("whoosh", SIGNAL), ("pop", BRAIN), ("riser", STRANGE - 0.3), ("pop", VESSELS),
          ("pop", SAMESIZE), ("hit", BUCKLE), ("pop", BUCKLE + 0.15), ("whoosh", PROOF), ("pop", DAMAGED - 0.1), ("pop", DAMAGED),
          ("pop", WONT), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", MARBLES), ("ding", PCT + 0.8),
          ("pop", TREADS), ("hit", NOTEX), ("pop", RACE2), ("tick", NODIFF), ("pop", ARGUE), ("pop", ARGUE + 0.15),
          ("whoosh", WIPE2), ("riser", SAMEPAT - 1.2), ("ding", SAMEPAT + 0.8), ("whoosh", LOOP)]
    for k in range(10):
        ev.append(("tick", FIVE - 0.2 + 0.08 * k * (1 + k * 0.2)))
    for k in range(8):
        ev.append(("tick", PCT + 0.06 * k * (1 + k * 0.25)))
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

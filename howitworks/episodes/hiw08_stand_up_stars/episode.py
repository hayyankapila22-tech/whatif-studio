# HIW08 — why you see stars when you stand up too fast (head rush). Basic + useful, detailed objects, "So," loop.
# Sources: orthostatic hypotension explainers — standing makes gravity pool blood in the legs, blood pressure dips
#  briefly, less blood reaches the brain/eyes (dizzy, "stars", greying vision); heart rate rises and vessels tighten
#  to fix it within seconds; tips: rise slowly, stay hydrated; see a doctor if it's frequent or you faint.
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
BLOOD = "#E5484D"; SKIN = "#E6B08A"; HOOD = "#3B5BDB"; STAR = "#FFF3B0"; WATERC = "#6FD3FF"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


STAND = kw(0); FUZZY = kw(1); STARS = kw(2); GRAV = kw(4); JUMPUP = p0(5); DROPS = kw(6)
SECOND = p0(7); LESS = kw(8); EYES = kw(9)
WIPE1 = p0(10) - 0.3; FAIL = kw(10); NOTEX = kw(11); HEART = kw(12); BACKUP = kw(13, 0) if False else p0(13)
SECS = kw(14); TRICK = p0(15); SLOW = kw(16); WATER = kw(17); SO = p0(18)
WL = 0.32
IMPACTS = [FUZZY, NOTEX]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]
rnd = random.Random(12)
SPARKS = [(rnd.uniform(80, 1000), rnd.uniform(380, 1500), rnd.uniform(4, 12), rnd.random() * 6.28) for _ in range(46)]


# ---------------- living room (detailed) ----------------
def room(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#f3e2cf"), col("#e7cdb2"), col("#cfae8e")], [0, 0.6, 1])))
    # window light
    win = skia.Rect.MakeLTRB(620, 360, 980, 820)
    c.drawRect(win.makeOutset(16, 16), paint("#ffffff"))
    c.drawRect(win, paint(shader=linear((0, 360), (0, 820), [col("#9fd6ff"), col("#d6efff")])))
    c.drawCircle(760, 480, 60, paint(shader=radial(760, 480, 90, [col("#ffffff", 0.9), col("#ffffff", 0)])))
    for k in range(3):
        c.drawOval(skia.Rect.MakeXYWH(650 + k * 110, 600 + 30 * math.sin(t * 0.3 + k), 140, 40), paint("#ffffff", 0.7, blur=6))
    c.drawLine(800, 360, 800, 820, paint("#ffffff", 1, stroke=12)); c.drawLine(620, 590, 980, 590, paint("#ffffff", 1, stroke=12))
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(800, 600, 900, [col("#fff3dc", 0.35), col("#fff3dc", 0)])))
    # floor + rug
    c.drawRect(skia.Rect.MakeLTRB(0, 1300, W, H), paint(shader=linear((0, 1300), (0, H), [col("#b98b62"), col("#8a6243")])))
    for k in range(8):
        c.drawLine(0, 1320 + k * 80, W, 1320 + k * 80, paint("#6b4a32", 0.25, stroke=3))
    c.drawOval(skia.Rect.MakeLTRB(80, 1360, 1000, 1560), paint(shader=radial(540, 1460, 480, [col("#e46a6a"), col("#b84b4b"), col("#8a3434")], [0, 0.7, 1])))
    c.drawOval(skia.Rect.MakeLTRB(140, 1385, 940, 1535), paint("#f2d6a8", 0.5, stroke=6))
    # sofa
    c.drawRoundRect(skia.Rect.MakeLTRB(60, 1000, 720, 1210), 50, 50, paint("#000000", 0.25, blur=18))
    c.drawRoundRect(skia.Rect.MakeLTRB(60, 940, 720, 1150), 50, 50, paint(shader=linear((0, 940), (0, 1150), [col("#6fbf9f"), col("#3f8f72")])))
    c.drawRoundRect(skia.Rect.MakeLTRB(90, 1080, 690, 1250), 40, 40, paint(shader=linear((0, 1080), (0, 1250), [col("#7fcfae"), col("#3f8f72")])))
    c.drawLine(390, 1090, 390, 1240, paint("#2f6f58", 0.6, stroke=5))
    for x in (40, 700):
        c.drawRoundRect(skia.Rect.MakeLTRB(x, 1030, x + 80, 1260), 36, 36, paint(shader=linear((x, 0), (x + 80, 0), [col("#7fcfae"), col("#3f8f72")])))
    for x in (110, 650):
        c.drawRect(skia.Rect.MakeLTRB(x, 1260, x + 18, 1310), paint("#5a3a26"))
    c.drawRoundRect(skia.Rect.MakeLTRB(120, 980, 300, 1100), 40, 40, paint(shader=radial(180, 1010, 160, [col("#ffd27a"), col("#e9a93f")])))
    # lamp
    c.drawLine(900, 900, 900, 1300, paint("#4a4a4a", 1, stroke=8))
    lp = skia.Path(); lp.moveTo(830, 900); lp.lineTo(970, 900); lp.lineTo(940, 800); lp.lineTo(860, 800); lp.close()
    c.drawPath(lp, paint(shader=linear((830, 0), (970, 0), [col("#fff1d2"), col("#f2d39a")])))
    c.drawOval(skia.Rect.MakeLTRB(850, 1290, 950, 1310), paint("#333333"))


def person(c, t, x, y, stand, sway=0.0, a=1.0):
    """stand: 0 sitting -> 1 standing. detailed hoodie person."""
    c.save(); c.translate(x, y); c.rotate(sway)
    rise = lerp(0, -260, stand)
    # legs
    if stand < 0.5:
        c.drawRoundRect(skia.Rect.MakeLTRB(-60, 60 + rise * 0.3, 120, 110 + rise * 0.3), 30, 30, paint("#2c3550", a))
        c.drawRoundRect(skia.Rect.MakeLTRB(80, 60 + rise * 0.3, 130, 260), 25, 25, paint("#2c3550", a))
    else:
        for sx in (-1, 1):
            c.drawRoundRect(skia.Rect.MakeLTRB(sx * 34 - 26, 40 + rise, sx * 34 + 26, 260), 26, 26, paint(shader=linear((sx * 34 - 26, 0), (sx * 34 + 26, 0), [col("#3a4566", a), col("#222a40", a)])))
    for sx in ((-1, 1) if stand >= 0.5 else (1,)):
        c.drawRoundRect(skia.Rect.MakeLTRB(sx * 34 - 36 + (70 if stand < 0.5 else 0), 248, sx * 34 + 46 + (70 if stand < 0.5 else 0), 278), 15, 15, paint("#f2f2f2", a))
    # torso hoodie
    tor = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-80, -170 + rise, 80, 70 + rise * 0.6), 50, 50)
    c.drawRRect(tor, paint(shader=linear((-80, 0), (80, 0), [col("#5f86ff", a), col(HOOD, a), col("#26388f", a)], [0, 0.5, 1])))
    c.drawLine(-14, -150 + rise, -20, -60 + rise, paint("#ffffff", 0.8 * a, stroke=4)); c.drawLine(14, -150 + rise, 20, -60 + rise, paint("#ffffff", 0.8 * a, stroke=4))
    c.drawRoundRect(skia.Rect.MakeLTRB(-50, -20 + rise, 50, 30 + rise), 16, 16, paint("#26388f", 0.6 * a))
    for sx in (-1, 1):
        c.drawLine(sx * 78, -140 + rise, sx * 98, -10 + rise, paint(HOOD, a, stroke=40))
        c.drawCircle(sx * 100, 10 + rise, 22, paint(SKIN, a))
    # head
    hy = -230 + rise
    c.drawCircle(0, hy, 70, paint(shader=radial(-20, hy - 25, 100, [col("#F6C9A8", a), col(SKIN, a), col("#B57D58", a)], [0, 0.55, 1])))
    hair = skia.Path(); hair.moveTo(-72, hy); hair.cubicTo(-80, hy - 90, 70, hy - 110, 74, hy - 10); hair.cubicTo(40, hy - 50, -30, hy - 60, -72, hy); hair.close()
    c.drawPath(hair, paint(shader=linear((0, hy - 100), (0, hy), [col("#5a3a26", a), col("#2e1c11", a)])))
    dz = window(t, FUZZY - 0.1, GRAV, 0.2, 0.3)
    for sx in (-1, 1):
        if dz > 0.3:
            c.drawArc(skia.Rect.MakeLTRB(sx * 24 - 12, hy - 8, sx * 24 + 12, hy + 16), 0, 300, False, paint("#3a2418", a, stroke=4))
        else:
            c.drawCircle(sx * 24, hy, 8, paint("#2e1c11", a))
    c.drawArc(skia.Rect.MakeLTRB(-18, hy + 20, 18, hy + 40), 20, 140, False, paint("#8a4a3a", a, stroke=4))
    c.restore()


def phosphenes(c, t, a):
    if a <= 0: return
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(540, 960, 1000, [col("#000000", 0.05 * a), col("#2b2b3a", 0.75 * a)], [0.3, 1])))
    for (x, y, r, ph) in SPARKS:
        tw = (0.5 + 0.5 * math.sin(t * 7 + ph)) ** 2
        c.drawCircle(x, y, r * 3, paint(STAR, 0.18 * tw * a, blur=6))
        c.drawCircle(x, y, r * 0.6, paint("#ffffff", tw * a))
        c.drawLine(x - r * 2, y, x + r * 2, y, paint(STAR, 0.7 * tw * a, stroke=1.5))
        c.drawLine(x, y - r * 2, x, y + r * 2, paint(STAR, 0.7 * tw * a, stroke=1.5))


def body_map(c, t, a, down, back):
    """translucent body silhouette with blood dots flowing down (gravity) or up (heart)."""
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(500, 1000, 1200, [col("#1d2747", a), col("#0b1022", a)])))
    sil = skia.Path()
    sil.addCircle(500, 560, 90)
    sil.addRoundRect(skia.Rect.MakeLTRB(390, 660, 610, 1080), 70, 70)
    sil.addRoundRect(skia.Rect.MakeLTRB(400, 1060, 490, 1460), 40, 40)
    sil.addRoundRect(skia.Rect.MakeLTRB(510, 1060, 600, 1460), 40, 40)
    sil.addRoundRect(skia.Rect.MakeLTRB(320, 680, 380, 1060), 30, 30)
    sil.addRoundRect(skia.Rect.MakeLTRB(620, 680, 680, 1060), 30, 30)
    sil.setFillType(skia.PathFillType.kWinding)
    c.drawPath(sil, paint("#9fb6ff", 0.10 * a))
    c.drawPath(sil, paint("#9fb6ff", 0.45 * a, stroke=3))
    # brain + eyes glow by blood level
    level = 1 - 0.75 * down * (1 - back)
    c.drawCircle(500, 540, 70, paint(shader=radial(480, 520, 90, [col("#FFE1E8", a), col(mixhex("#F2A4B8", "#6b6b7a", 1 - level), a)])))
    for sx in (-1, 1):
        c.drawCircle(500 + sx * 30, 590, 10, paint(mixhex("#ffffff", "#555566", 1 - level), a))
    # vessels
    for vx in (450, 550):
        c.drawLine(vx, 600, vx, 1440, paint(BLOOD, 0.35 * a, stroke=10))
    c.drawCircle(470, 760, 34, paint(shader=radial(460, 750, 44, [col("#ff8a8e", a), col(BLOOD, a)])))     # heart
    # flowing blood dots
    for k in range(26):
        u = ((t * (0.9 if back > 0.5 else 0.6) + k / 26) % 1)
        if back > 0.5:
            yy = lerp(1440, 560, u)
        else:
            yy = lerp(560, 1440, u ** (1 - 0.6 * down))
        vx = 450 if k % 2 else 550
        c.drawCircle(vx, yy, 9, paint(BLOOD, a))
    pool = down * (1 - back)
    if pool > 0:
        for sx in (445, 555):
            c.drawRoundRect(skia.Rect.MakeLTRB(sx - 40, 1300, sx + 40, 1460), 30, 30, paint(BLOOD, 0.45 * pool * a, blur=6))
    # gravity arrows
    ga = down * (1 - back)
    for k in range(3):
        y0 = 700 + ((t * 300 + k * 220) % 660)
        c.drawLine(800, y0, 800, y0 + 90, paint("#ffffff", 0.7 * ga * a, stroke=8))
        ah = skia.Path(); ah.moveTo(780, y0 + 80); ah.lineTo(820, y0 + 80); ah.lineTo(800, y0 + 112); ah.close()
        c.drawPath(ah, paint("#ffffff", 0.7 * ga * a))


def heart(c, x, y, s, a, beat):
    c.save(); c.translate(x, y); sc = s * (1 + 0.08 * beat); c.scale(sc, sc)
    hp = skia.Path(); hp.moveTo(0, 90); hp.cubicTo(-150, -10, -110, -150, 0, -70); hp.cubicTo(110, -150, 150, -10, 0, 90); hp.close()
    c.drawPath(hp, paint("#000000", 0.25 * a, blur=14))
    c.drawPath(hp, paint(shader=radial(-40, -60, 200, [col("#ff9aa0", a), col(BLOOD, a), col("#9a1f26", a)], [0, 0.5, 1])))
    c.drawArc(skia.Rect.MakeLTRB(-100, -110, -10, -20), 200, 70, False, paint("#ffffff", 0.6 * a, stroke=10, blur=3))
    c.restore()


def water_glass(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-110, 240, 110, 270), paint("#000000", 0.2 * a, blur=10))
    body = skia.Path(); body.moveTo(-120, -220); body.lineTo(120, -220); body.lineTo(98, 245); body.cubicTo(96, 258, -96, 258, -98, 245); body.close()
    c.drawPath(body, paint("#ffffff", 0.25 * a))
    wp = skia.Path(); wp.moveTo(-112, -120); wp.lineTo(112, -120); wp.lineTo(96, 242); wp.cubicTo(94, 254, -94, 254, -96, 242); wp.close()
    c.drawPath(wp, paint(shader=linear((-110, 0), (110, 0), [col("#bfe9ff", 0.85 * a), col(WATERC, 0.85 * a), col("#2fa6e0", 0.85 * a)])))
    c.drawOval(skia.Rect.MakeLTRB(-112, -132, 112, -108), paint("#e8f8ff", 0.9 * a))
    c.drawPath(body, paint("#ffffff", 0.7 * a, stroke=4))
    c.drawLine(-92, -200, -76, 220, paint("#ffffff", 0.6 * a, stroke=12, blur=4))
    for k in range(10):
        c.drawCircle(-60 + (k * 37) % 130, 200 - (t_g * 60 + k * 40) % 300, 5, paint("#ffffff", 0.6 * a))
    c.restore()


t_g = 0.0


def scene_white(c, t):
    global t_g
    t_g = t
    studio_white(c)
    fa = eback(prog(t, FAIL - 0.2, 0.35)) * (1 - prog(t, HEART - 0.2, 0.25))
    if fa > 0:
        # battery "failing" icon
        c.save(); c.translate(500, 1000); c.scale(fa, fa)
        c.drawRoundRect(skia.Rect.MakeLTRB(-170, -90, 150, 90), 26, 26, paint("#000000", 0.18, blur=12))
        c.drawRoundRect(skia.Rect.MakeLTRB(-170, -90, 150, 90), 26, 26, paint(shader=linear((0, -90), (0, 90), [col("#ffffff"), col("#d6dbe4")])))
        c.drawRoundRect(skia.Rect.MakeLTRB(150, -34, 182, 34), 8, 8, paint("#bfc6d2"))
        c.drawRoundRect(skia.Rect.MakeLTRB(-150, -70, -80, 70), 14, 14, paint(shader=linear((0, -70), (0, 70), [col("#ff8a8e"), col(BLOOD)])))
        c.restore()
        if t > NOTEX:
            xa = eout(prog(t, NOTEX, 0.2))
            c.drawLine(300, 840, lerp(300, 700, xa), lerp(840, 1160, xa), paint(RED, 1, stroke=20))
            c.drawLine(700, 840, lerp(700, 300, xa), lerp(840, 1160, xa), paint(RED, 1, stroke=20))
    ha = window(t, HEART - 0.2, TRICK - 0.05, 0.3, 0.25)
    if ha > 0:
        beat = max(0, math.sin(t * 2 * math.pi * 2.2)) ** 6
        heart(c, 500, 980, 1.6, ha, beat)
        for k in range(3):
            u = ((t * 1.2 + k / 3) % 1)
            c.drawCircle(500, 980, 200 + 160 * u, paint(BLOOD, 0.4 * ha * (1 - u), stroke=5))
        if t > BACKUP:
            ua = eout(prog(t, BACKUP, 0.3)) * ha
            for k, x in enumerate((260, 740)):
                y0 = 1200 - ((t * 400 + k * 120) % 500)
                c.drawLine(x, y0 + 100, x, y0, paint(BLOOD, ua, stroke=12))
                ah = skia.Path(); ah.moveTo(x - 28, y0 + 10); ah.lineTo(x + 28, y0 + 10); ah.lineTo(x, y0 - 30); ah.close()
                c.drawPath(ah, paint(BLOOD, ua))
        if t > SECS - 0.1:
            sa = eback(prog(t, SECS - 0.1, 0.3))
            big_number(c, "FIXED", "IN SECONDS", 500, 1400, 90, "#1fb98a", clamp(sa) * ha)
    if t > TRICK - 0.1:
        a1 = eout(prog(t, SLOW - 0.2, 0.4))
        if a1 > 0:
            # slow-rise icon: chair + person rising with a slow arrow
            c.save(); c.translate(290, 1000); c.scale(0.7 * a1 + 0.3 * a1, 0.7 * a1 + 0.3 * a1)
            c.drawRoundRect(skia.Rect.MakeLTRB(-120, 60, 120, 120), 20, 20, paint(shader=linear((0, 60), (0, 120), [col("#7fcfae"), col("#3f8f72")])))
            c.drawRoundRect(skia.Rect.MakeLTRB(-120, -80, -70, 120), 20, 20, paint(shader=linear((-120, 0), (-70, 0), [col("#7fcfae"), col("#3f8f72")])))
            rise = 0.5 + 0.5 * math.sin((t - SLOW) * 1.5)
            c.drawCircle(10, -60 - 80 * rise, 40, paint(shader=radial(0, -80 - 80 * rise, 60, [col("#F6C9A8"), col(SKIN)])))
            c.drawRoundRect(skia.Rect.MakeLTRB(-40, -20 - 80 * rise, 60, 70), 30, 30, paint(shader=linear((-40, 0), (60, 0), [col("#5f86ff"), col(HOOD)])))
            c.restore()
        a2 = eout(prog(t, WATER - 0.2, 0.4))
        if a2 > 0:
            water_glass(c, 730, 1010, 0.8 * eback(prog(t, WATER - 0.2, 0.4)), a2)
    pill(c, t, "SLOWLY", 500, 1360, "#1fb98a", SLOW, WATER - 0.05, light=True)
    pill(c, t, "DRINK WATER", 500, 1360, "#2fa6e0", WATER, SO, light=True)


def main_room(c, t):
    room(c, t)
    stand = eio(prog(t, STAND - 0.6, 0.7)) if t > 0.25 else 0
    sway = 3 * math.sin(t * 2.5) * window(t, FUZZY - 0.1, GRAV, 0.2, 0.3)
    person(c, t, 380, 1080, stand, sway)


def hook_room(c, t):
    room(c, t)
    person(c, t, 380, 1080, 0.0, 0)


def draw_world(c, t):
    if t < GRAV - 0.2:
        main_room(c, t)
        # fuzzy: blur-ish wash + phosphenes
        fz = window(t, FUZZY - 0.15, GRAV, 0.25, 0.3)
        if fz > 0:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#8f8f9f", 0.25 * fz))
            phosphenes(c, t, fz * (0.5 + 0.5 * prog(t, STARS - 0.2, 0.3)))
        pill(c, t, "HEAD RUSH", 500, 1400, "#2b2b3a", STARS, GRAV - 0.2, text_col="#FFFFFF")
        return
    if t < WIPE1 + WL / 2:
        down = eout(prog(t, DROPS - 0.3, 0.8))
        body_map(c, t, eout(prog(t, GRAV - 0.2, 0.35)), down, 0)
        if t > EYES - 0.15:
            phosphenes(c, t, 0.6 * eout(prog(t, EYES - 0.15, 0.3)))
        pill(c, t, "GRAVITY", 760, 640, "#FFFFFF", GRAV, DROPS - 0.1)
        pill(c, t, "BLOOD DROPS", 760, 640, BLOOD, DROPS, LESS - 0.1)
        pill(c, t, "LESS BLOOD UP HERE", 560, 360 + 60, "#9aa0ad", LESS, EYES - 0.1, text_col="#FFFFFF")
        pill(c, t, "EYES NOTICE FIRST", 500, 1380, STAR, EYES, WIPE1 + 0.1)
        return
    if t < SO - 0.05:
        scene_white(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    hook_room(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_white(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.025 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"too fast": "#3b7de0", "fuzzy": "#9aa0ad", "stars": "#E3A64A", "gravity": "#3b7de0", "drops": BLOOD,
         "less": BLOOD, "notice": "#E3A64A", "failing": RED, "exactly": RED, "speeds": BLOOD, "up.": BLOOD,
         "seconds": "#1fb98a", "slowly": "#1fb98a", "water": "#2fa6e0"}
CAPS = Captions(P, KWCOL, {"Not", "fuzzy."}, DUR)


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
    in_room = t < GRAV - 0.2 or t >= SO - 0.05 + (DUR - SO) * 0.5
    light = WIPE1 + WL / 2 <= t < SO - 0.05 + (DUR - SO) * 0.5
    vignette(c, light)
    # captions need contrast on the bright room: a soft dark scrim at the top
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 700), paint(shader=linear((0, 0), (0, 700), [col("#000000", 0.55 if in_room else 0.45), col("#000000", 0)])))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, "#1fb98a", "#F4F2EE")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", STAND - 0.6), ("hit", FUZZY), ("riser", STARS - 0.3), ("whoosh", GRAV - 0.2), ("pop", GRAV),
          ("pop", DROPS), ("pop", LESS), ("pop", EYES), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", FAIL),
          ("hit", NOTEX), ("pop", HEART), ("pop", BACKUP), ("ding", SECS), ("pop", SLOW), ("pop", WATER),
          ("whoosh", SO - 0.05)]
    for k in range(6):
        ev.append(("tick", HEART + k * 0.23))
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

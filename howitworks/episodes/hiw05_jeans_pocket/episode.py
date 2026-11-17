# HIW05 — "What is this?" the tiny jeans pocket (standard format; basic + useful, no studies).
# Sources: Levi Strauss & Co. "Pockets Full of History" (2017): watch pocket made for pocket watches, rivets reinforce
#  pocket corners (1873 patent), rivets removed from watch pocket in WWII, the back-left pocket (true 5th) added 1901;
#  Britannica "Why do jeans have that tiny pocket?"; Levi's historian Tracey Panek (oldest pair 1879 has the watch pocket).
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
GOLD = "#E3A64A"; COPPER = "#C8743A"; INDIGO = "#24365F"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


REVEAL = p0(1); JEANS = kw(2); PHONE = kw(3); WHY = p0(4); WATCH = kw(5)
Y1870 = kw(6); CHAIN = kw(7); SAFE = kw(8); SCRATCH = kw(9); WRIST = p0(10); STAYED = kw(11)
BUTTONS = kw(12); RIVETS = kw(13); RIP = kw(14)
WIPE1 = p0(15) - 0.3; FIFTH = kw(15); NOTEX = kw(16); FOURTH = kw(17); LATER = kw(18)
WIPE2 = p0(19) - 0.3; COINS = kw(19); KEYS = kw(20); PICK = kw(21); SO = p0(22)
WL = 0.32
IMPACTS = [NOTEX]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]

DENIM = None


def denim():
    global DENIM
    if DENIM is None:
        DENIM = skia.Image.open(f"{D}/denim.png")
    return DENIM


# ---------------- jeans panel (world coords) ----------------
WP = skia.Rect.MakeLTRB(110, -440, 320, -240)   # watch pocket
RIV = [(118, -432), (312, -432), (-150, -452), (440, -60)]


def stitch(c, path, a=1.0, w=3.0, double=True):
    pp = paint(GOLD, 0.95 * a, stroke=w)
    pp.setPathEffect(skia.DashPathEffect.Make([12, 7], 0))
    c.drawPath(path, paint("#000000", 0.35 * a, stroke=w + 2, blur=1.5))
    c.drawPath(path, pp)
    if double:
        c.save(); c.translate(0, 9)
        c.drawPath(path, pp)
        c.restore()


def rivet(c, x, y, s=1.0, a=1.0, glow=0.0):
    if glow > 0:
        c.drawCircle(x, y, 40 * s, paint(GOLD, 0.35 * glow, blur=12))
    c.drawCircle(x + 2, y + 4, 17 * s, paint("#000000", 0.45 * a, blur=4))
    c.drawCircle(x, y, 16 * s, paint(shader=radial(x - 5 * s, y - 6 * s, 22 * s, [col("#FFD9A8", a), col(COPPER, a), col("#7a3f19", a)], [0, 0.45, 1])))
    c.drawCircle(x, y, 7 * s, paint("#8a4a20", 0.6 * a, stroke=2))
    c.drawCircle(x - 5 * s, y - 6 * s, 3.5 * s, paint("#ffffff", 0.8 * a))


def panel(c, t, st):
    # base denim (infinite-ish)
    m = skia.Matrix(); m.setScale(0.75, 0.75)
    c.drawRect(skia.Rect.MakeLTRB(-2000, -2000, 2000, 2000), paint(shader=denim().makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, SAMP, m)))
    # soft fading/whiskers
    c.drawRect(skia.Rect.MakeLTRB(-2000, -2000, 2000, 2000), paint(shader=radial(120, -150, 900, [col("#9fb6e0", 0.10), col("#000000", 0.0), col("#000000", 0.35)], [0, 0.5, 1])))
    # waistband
    c.drawRect(skia.Rect.MakeLTRB(-2000, -620, 2000, -470), paint("#000000", 0.18))
    c.drawRect(skia.Rect.MakeLTRB(-2000, -472, 2000, -462), paint("#000000", 0.35, blur=3))
    wb = skia.Path(); wb.moveTo(-2000, -600); wb.lineTo(2000, -600)
    stitch(c, wb, 1, 3, True)
    wb2 = skia.Path(); wb2.moveTo(-2000, -490); wb2.lineTo(2000, -490)
    stitch(c, wb2, 1, 3, False)
    # belt loop
    c.drawRoundRect(skia.Rect.MakeLTRB(400, -640, 470, -440), 10, 10, paint("#000000", 0.4, blur=8))
    c.drawRoundRect(skia.Rect.MakeLTRB(395, -650, 465, -450), 10, 10, paint(shader=denim().makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, SAMP, m)))
    c.drawRoundRect(skia.Rect.MakeLTRB(395, -650, 465, -450), 10, 10, paint("#ffffff", 0.06))
    bl = skia.Path(); bl.moveTo(405, -640); bl.lineTo(405, -460); bl.moveTo(455, -640); bl.lineTo(455, -460)
    stitch(c, bl, 1, 2.5, False)
    # fly J-stitch
    fly = skia.Path(); fly.moveTo(-430, -470); fly.lineTo(-430, 300); fly.cubicTo(-430, 420, -330, 440, -290, 380)
    stitch(c, fly, 1, 3, True)
    # front pocket opening (scoop) with depth shadow
    po = skia.Path(); po.moveTo(-150, -462); po.cubicTo(-120, -150, 150, -60, 470, -50)
    shade = skia.Path(); shade.addPath(po); shade.lineTo(470, -470); shade.close()
    c.drawPath(shade, paint("#000000", 0.0))
    c.save(); c.clipPath(shade, skia.ClipOp.kDifference)
    c.drawPath(po, paint("#000000", 0.55, stroke=36, blur=14))
    c.restore()
    c.drawPath(po, paint("#ffffff", 0.10, stroke=3))
    c.save(); c.translate(-14, 12); stitch(c, po, 1, 3, False); c.restore()


def watch_pocket(c, t, st):
    # the patch (drawn after anything "inside" it)
    c.drawRect(WP.makeOffset(6, 10), paint("#000000", 0.45, blur=12))
    m = skia.Matrix(); m.setScale(0.75, 0.75); m.postTranslate(37, 23)
    c.drawRect(WP, paint(shader=denim().makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, SAMP, m)))
    c.drawRect(WP, paint(shader=linear((0, WP.top()), (0, WP.bottom()), [col("#000000", 0.25), col("#ffffff", 0.05)])))
    edge = skia.Path(); edge.moveTo(WP.left() + 10, WP.top()); edge.lineTo(WP.left() + 10, WP.bottom() - 10)
    edge.lineTo(WP.right() - 10, WP.bottom() - 10); edge.lineTo(WP.right() - 10, WP.top())
    stitch(c, edge, 1, 3, False)
    top = skia.Path(); top.moveTo(WP.left(), WP.top() + 14); top.lineTo(WP.right(), WP.top() + 14)
    stitch(c, top, 1, 2.5, False)
    gl = st.get("rivglow", 0)
    for i, (x, y) in enumerate(RIV):
        rivet(c, x, y, 1.0, 1.0, gl if i < 2 else 0)
    sh = st.get("shield", 0)
    if sh > 0:
        c.drawRect(WP.makeOutset(16, 16), paint(GOLD, 0.6 * sh, stroke=5, blur=3))
        c.drawRect(WP.makeOutset(16, 16), paint(GOLD, 0.15 * sh))


def pocket_watch(c, t, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(4, 8, 92, paint("#000000", 0.4 * a, blur=10))
    c.drawCircle(0, -98, 18, paint(GOLD, a, stroke=7))
    c.drawRoundRect(skia.Rect.MakeLTRB(-14, -100, 14, -80), 5, 5, paint(shader=linear((-14, 0), (14, 0), [col("#8a5a1c", a), col("#FFE1A0", a), col("#8a5a1c", a)])))
    c.drawCircle(0, 0, 90, paint(shader=radial(-30, -35, 130, [col("#FFF0C2", a), col(GOLD, a), col("#7d5216", a)], [0, 0.45, 1])))
    c.drawCircle(0, 0, 74, paint(shader=radial(-20, -25, 90, [col("#ffffff", a), col("#EFE9DC", a)])))
    for k in range(12):
        an = k * math.pi / 6
        c.drawLine(62 * math.sin(an), -62 * math.cos(an), 70 * math.sin(an), -70 * math.cos(an), paint("#2a2a2a", a, stroke=3 if k % 3 == 0 else 1.5))
    hm = t * 0.3; mm = t * 3.0
    c.drawLine(0, 0, 36 * math.sin(hm), -36 * math.cos(hm), paint("#1b1b1b", a, stroke=5))
    c.drawLine(0, 0, 54 * math.sin(mm), -54 * math.cos(mm), paint("#1b1b1b", a, stroke=3))
    c.drawCircle(0, 0, 5, paint("#1b1b1b", a))
    c.drawArc(skia.Rect.MakeLTRB(-60, -64, 40, 30), 200, 70, False, paint("#ffffff", 0.5 * a, stroke=6, blur=2))
    c.restore()


def chain(c, t, x0, y0, x1, y1, a=1.0, sway=0.0):
    n = 16
    for k in range(n + 1):
        u = k / n
        x = lerp(x0, x1, u); y = lerp(y0, y1, u) + 70 * math.sin(math.pi * u) + sway * math.sin(t * 2.4) * math.sin(math.pi * u) * 30
        c.save(); c.translate(x, y); c.rotate(60 if k % 2 else -20)
        c.drawOval(skia.Rect.MakeLTRB(-10, -6, 10, 6), paint(GOLD, a, stroke=4))
        c.restore()


def phone(c, x, y, s, a, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-95, -190, 95, 190), 30, 30, paint("#000000", 0.4 * a, blur=10))
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -185, 90, 185), 28, 28, paint("#1c1d22", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-80, -172, 80, 172), 20, 20, paint(shader=linear((-80, -172), (80, 172), [col("#4c6fff", a), col("#9b5cff", a), col("#ff7a9c", a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(-26, -165, 26, -152), 6, 6, paint("#0b0b0d", a))
    c.restore()


def wristwatch(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    for sgn in (-1, 1):
        c.drawRoundRect(skia.Rect.MakeLTRB(-34, sgn * 60 - (70 if sgn < 0 else 0), 34, sgn * 60 + (0 if sgn < 0 else 70)), 12, 12, paint("#5b3a24", a))
    c.drawCircle(0, 0, 62, paint(shader=radial(-20, -20, 80, [col("#f4f4f4", a), col("#a9adb5", a), col("#5c6068", a)], [0, 0.5, 1])))
    c.drawCircle(0, 0, 50, paint("#fbfaf6", a))
    c.drawLine(0, 0, 0, -36, paint("#1b1b1b", a, stroke=4)); c.drawLine(0, 0, 26, 8, paint("#1b1b1b", a, stroke=4))
    c.restore()


def coin(c, x, y, s, a, silver=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    c1, c2, c3 = ("#ffffff", "#c9ccd2", "#7d828c") if silver else ("#FFE2B8", "#D08A4A", "#7a4520")
    c.drawCircle(0, 0, 38, paint(shader=radial(-12, -14, 50, [col(c1, a), col(c2, a), col(c3, a)], [0, 0.5, 1])))
    c.drawCircle(0, 0, 30, paint(c3, 0.5 * a, stroke=2))
    c.restore()


def key(c, x, y, s, a, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.addCircle(0, -60, 34); p.addRect(skia.Rect.MakeLTRB(-9, -30, 9, 80))
    for k, w in ((40, 22), (58, 14), (72, 20)):
        p.addRect(skia.Rect.MakeLTRB(9, k - 5, 9 + w, k + 5))
    p.setFillType(skia.PathFillType.kWinding)
    c.drawPath(p, paint(shader=linear((-30, 0), (30, 0), [col("#e9ecf1", a), col("#9aa1ad", a)])))
    c.drawCircle(0, -60, 13, paint("#1d2a4a", a))
    c.restore()


def guitar_pick(c, x, y, s, a, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 50); p.cubicTo(-60, -10, -40, -50, 0, -50); p.cubicTo(40, -50, 60, -10, 0, 50); p.close()
    c.drawPath(p, paint(shader=radial(-10, -20, 70, [col("#ffd27a", a), col("#ff5a5f", a)])))
    c.restore()


CAMS = [(REVEAL, 0, -160, 0.95), (PHONE - 0.2, 215, -300, 1.7), (Y1870 - 0.1, 240, -360, 1.3), (WRIST, 215, -330, 1.6),
        (BUTTONS - 0.1, 300, -420, 3.0), (RIP + 0.1, 250, -380, 2.0)]
CAMS2 = [(WIPE2, 215, -320, 1.7)]


def cam_at(t, keys):
    if t <= keys[0][0]:
        return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t < t1:
            q = eio(prog(t, t1 - 0.6, 0.6)) if t > t1 - 0.6 else 0
            return tuple(lerp(x, y, q) for x, y in zip(a, b))
    return keys[-1][1:]


def hook_cam(t):
    ph = 2 * math.pi * t / DUR
    return 250 + 12 * math.sin(ph), -400 + 8 * math.sin(2 * ph), 3.6 + 0.08 * math.sin(ph)


def world(c, cam, t, st):
    cx, cy, z = cam
    c.save(); c.translate(500, 1000); c.scale(z, z); c.translate(-cx, -cy)
    panel(c, t, st)
    # things inside the watch pocket go BEFORE the pocket patch
    wa = st.get("watch", 0)
    if wa > 0:
        drop = st.get("watchdrop", 1)
        wy = lerp(-900, -455, eback(drop, 1.2)) - 240 * st.get("watchout", 0)
        pocket_watch(c, t, 215, wy, 0.85, wa)
    for item in st.get("items", []):
        kind, q = item
        y = lerp(-950, -470, eback(q, 1.1))
        if kind == "coin": coin(c, 180, y, 0.9, 1)
        if kind == "coin2": coin(c, 240, y - 10, 0.85, 1, silver=True)
        if kind == "key": key(c, 265, y - 20, 0.8, 1, 15)
        if kind == "pick": guitar_pick(c, 150, y + 10, 0.8, 1, -20)
    watch_pocket(c, t, st)
    if wa > 0 and st.get("chain", 0) > 0:
        chain(c, t, 215, -420 + (lerp(-720, -330, eback(st.get("watchdrop", 1), 1.2)) + 330) * 0.0 - 15, 430, -480, st["chain"] * wa, st.get("sway", 0))
    # tear line stopped by the rivet
    tr = st.get("tear", 0)
    if tr > 0:
        p = skia.Path(); p.moveTo(312, -260)
        for k, (dx, dy) in enumerate(((318, -290), (306, -320), (320, -350), (308, -380), (316, -410))):
            p.lineTo(dx, dy)
        pp = paint(RED, 1, stroke=6)
        if tr < 0.999:
            te = skia.TrimPathEffect.Make(0, tr)
            if te: pp.setPathEffect(te)
        c.drawPath(p, pp)
    sp = st.get("sparks", 0)
    if sp > 0:
        for k in range(8):
            u = ((t * 1.4 + k / 8) % 1)
            an = k * 0.8
            x = 215 + math.cos(an) * (150 - 40 * u); y = -340 + math.sin(an) * (130 - 40 * u)
            if u > 0.7:
                x = 215 + math.cos(an) * (110 + 200 * (u - 0.7)); y = -340 + math.sin(an) * (90 + 200 * (u - 0.7))
            c.drawCircle(x, y, 6, paint("#ffffff", sp * 0.9 * (1 - abs(u - 0.7))))
    c.restore()


def bg_frame(c):
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#0d1220"))


def scene_main(c, t):
    bg_frame(c)
    cam = cam_at(t, CAMS)
    st = {}
    st["watch"] = window(t, WATCH - 0.15, WRIST + 1.0, 0.15, 0.4)
    st["watchdrop"] = prog(t, WATCH - 0.1, 0.6)
    st["watchout"] = eio(prog(t, WRIST, 0.8))
    st["chain"] = eout(prog(t, CHAIN - 0.2, 0.5))
    st["sway"] = 1.0
    st["shield"] = window(t, SAFE - 0.1, WRIST, 0.3, 0.3)
    st["sparks"] = window(t, SCRATCH - 0.2, WRIST, 0.2, 0.3)
    st["rivglow"] = window(t, BUTTONS, WIPE1, 0.3, 0.3)
    st["tear"] = eout(prog(t, RIP - 0.1, 0.6))
    world(c, cam, t, st)
    # sepia 1870s
    sa = window(t, Y1870 - 0.15, SAFE + 0.2, 0.3, 0.4)
    if sa > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#8a5a2b", 0.38 * sa))
        c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(540, 960, 1100, [col("#000000", 0), col("#2a1606", 0.6 * sa)], [0.5, 1])))
        big_number(c, "1870s", "", 500, 1330, 150, "#FFE9C7", sa)
    # phone too big
    pa = window(t, PHONE - 0.2, WATCH - 0.2, 0.2, 0.3)
    if pa > 0:
        u = prog(t, PHONE - 0.2, 0.9)
        y = lerp(1700, 1020, eout(min(u * 1.4, 1)))
        if u > 0.72:
            y += 120 * eout((u - 0.72) / 0.28)
        phone(c, 520, y, 1.0, pa, -6)
        xa = eout(prog(t, PHONE + 0.6, 0.2)) * pa
        if xa > 0:
            c.drawLine(380, 820, 660, 1100, paint(RED, xa, stroke=18)); c.drawLine(660, 820, 380, 1100, paint(RED, xa, stroke=18))
    # wristwatch takes over
    wr = window(t, WRIST - 0.1, BUTTONS - 0.2, 0.4, 0.3)
    if wr > 0:
        wristwatch(c, lerp(1250, 760, eout(prog(t, WRIST - 0.1, 0.6))), 1260, 1.3, wr)
    pill(c, t, "TOO BIG", 500, 1320, RED, PHONE + 0.2, WATCH - 0.2)
    pill(c, t, "POCKET WATCH", 500, 1320, GOLD, WATCH, Y1870 - 0.1)
    pill(c, t, "SAFE", 500, 1320, GOLD, SAFE, WRIST - 0.1)
    pill(c, t, "STILL HERE", 500, 1320, "#FFFFFF", STAYED, BUTTONS - 0.1)
    pill(c, t, "RIVETS", 500, 1320, COPPER, RIVETS, RIP)
    pill(c, t, "STOPS RIPS", 500, 1320, COPPER, RIP, WIPE1 + 0.1)


def jeans_icon(c, x, y, s, a, back=False, badges=None, t=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    p.moveTo(-150, -230); p.lineTo(150, -230); p.lineTo(170, 260); p.lineTo(40, 260); p.lineTo(0, -40)
    p.lineTo(-40, 260); p.lineTo(-170, 260); p.close()
    c.drawPath(p.makeOffset(6, 12) if hasattr(p, "makeOffset") else p, paint("#000000", 0.18 * a, blur=12))
    c.drawPath(p, paint(shader=linear((-170, -230), (170, 260), [col("#4d6fb3", a), col("#2b4579", a)])))
    c.drawRect(skia.Rect.MakeLTRB(-150, -230, 150, -195), paint("#000000", 0.18 * a))
    if not back:
        for sgn in (-1, 1):
            q = skia.Path(); q.moveTo(sgn * 140, -195); q.cubicTo(sgn * 120, -120, sgn * 70, -110, sgn * 40, -110)
            c.drawPath(q, paint(GOLD, a, stroke=4))
        c.drawRect(skia.Rect.MakeLTRB(60, -190, 108, -150), paint(GOLD, a, stroke=3))
    else:
        for sgn in (-1, 1):
            c.drawRoundRect(skia.Rect.MakeLTRB(sgn * 115 - 45, -150, sgn * 115 + 45, -60), 10, 10, paint(GOLD, a, stroke=4))
    c.restore()


def badge(c, x, y, txt, colr, a, txtcol=INK):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    c.drawCircle(0, 4, 34, paint("#000000", 0.2, blur=6)); c.drawCircle(0, 0, 32, paint(colr))
    f = skia.Font(TF_BLACK, 34); c.drawString(txt, -f.measureText(txt) / 2, 12, f, paint(txtcol))
    c.restore()


def scene_white(c, t):
    studio_white(c)
    a = eout(prog(t, WIPE1, 0.4))
    jeans_icon(c, 300, 1000, 1.25, a)
    jeans_icon(c, 740, 1000, 1.25, a, back=True)
    # front pockets 1,2 ; back-right 3 ; tiny = "5?" -> "4" ; back-left = 5 (later)
    badge(c, 300 - 120, 840, "1", "#FFFFFF", eback(prog(t, FIFTH - 0.6, 0.25)))
    badge(c, 300 + 120, 840, "2", "#FFFFFF", eback(prog(t, FIFTH - 0.45, 0.25)))
    badge(c, 740 + 144, 790, "3", "#FFFFFF", eback(prog(t, FIFTH - 0.3, 0.25)))
    tiny_t = "5" if t < FOURTH else "4"
    tc = YELLOW if t < FOURTH else GOLD
    badge(c, 300 + 105, 720, tiny_t, tc, eback(prog(t, FIFTH, 0.3)))
    if NOTEX <= t < FOURTH:
        xa = eout(prog(t, NOTEX, 0.15))
        c.drawLine(365, 680, lerp(365, 445, xa), lerp(680, 760, xa), paint(RED, 1, stroke=10))
        c.drawLine(445, 680, lerp(445, 365, xa), lerp(680, 760, xa), paint(RED, 1, stroke=10))
    badge(c, 740 - 144, 790, "5", "#9aa0ad", eback(prog(t, LATER - 0.1, 0.3)), "#FFFFFF")
    pill(c, t, "\"5TH POCKET\"?", 500, 600, YELLOW, FIFTH, NOTEX, light=True)
    pill(c, t, "ACTUALLY 4TH", 500, 600, GOLD, FOURTH, LATER, light=True)
    pill(c, t, "ADDED LATER", 600, 1360, "#9aa0ad", LATER, WIPE2 + 0.2, light=True, text_col="#FFFFFF")


def scene_items(c, t):
    bg_frame(c)
    cam = cam_at(t, CAMS2)
    items = []
    for kind, ti in (("coin", COINS - 0.15), ("coin2", COINS + 0.15), ("key", KEYS - 0.1), ("pick", PICK - 0.1)):
        q = prog(t, ti, 0.55)
        if q > 0:
            items.append((kind, q))
    world(c, cam, t, dict(items=items))
    pill(c, t, "COINS", 500, 1320, COPPER, COINS, KEYS - 0.05)
    pill(c, t, "KEYS", 500, 1320, "#FFFFFF", KEYS, PICK - 0.05)
    pill(c, t, "GUITAR PICK", 500, 1320, "#ff7a7f", PICK, SO)


def draw_hook(c, t):
    bg_frame(c)
    world(c, hook_cam(t), t, {})
    hx, hy = 500, 1000
    r = skia.Rect.MakeLTRB(hx - 300, hy - 300, hx + 300, hy + 300)
    return r


def hook_box(c, t, a):
    if a <= 0: return
    r = skia.Rect.MakeLTRB(230, 760, 800, 1240)
    c.drawPath(skia.Path().addRect(r), paint("#ffffff", a, stroke=2.5))
    for qx, qy in ((r.left(), r.top()), (r.right(), r.top()), (r.left(), r.bottom()), (r.right(), r.bottom())):
        c.drawCircle(qx, qy, 8, paint("#ffffff", a)); c.drawCircle(qx, qy, 8, paint("#7aa2ff", a, stroke=2))
    c.drawString("?", r.right() - 26, r.top() - 14, skia.Font(TF_BLACK, 40), paint("#ffffff", a))


def draw_world(c, t):
    if t < REVEAL - 0.1:
        draw_hook(c, t); hook_box(c, t, 1)
        return
    if t < WIPE1 + WL / 2:
        if t < REVEAL + 0.6:   # smooth pull-out from the hook camera
            q = eio(prog(t, REVEAL - 0.1, 0.7))
            hc = hook_cam(t); tc = CAMS[0][1:]
            cam = tuple(lerp(a, b, q) for a, b in zip(hc, tc))
            bg_frame(c); world(c, cam, t, {})
            hook_box(c, t, 1 - prog(t, REVEAL - 0.1, 0.2))
            return
        scene_main(c, t); return
    if t < WIPE2 + WL / 2:
        scene_white(c, t); return
    if t < SO - 0.05:
        scene_items(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    a = CAMS2[0][1:]; b = hook_cam(t)
    bg_frame(c); world(c, tuple(lerp(x, y, q) for x, y in zip(a, b)), t, dict(items=[("coin", 1), ("coin2", 1), ("key", 1), ("pick", 1)] if q < 0.5 else []))
    hook_box(c, t, eout(prog(t, DUR - 0.25, 0.2)))


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.025 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"is": "#FFFFFF", "jeans": "#7ea2ff", "phone": RED, "pocket watch": GOLD, "1870s": GOLD, "chain": GOLD,
         "safe": GOLD, "scratch": GOLD, "over": "#FFFFFF", "stayed": "#FFFFFF", "buttons": COPPER, "rivets": COPPER,
         "ripping": COPPER, "fifth": YELLOW, "exactly": RED, "fourth": GOLD, "later": "#FFFFFF", "coins": COPPER,
         "keys": "#FFFFFF", "pick": "#ff7a7f"}
CAPS = Captions(P, KWCOL, {"Not", "fourth."}, DUR)


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
    light = WIPE1 + WL / 2 <= t < WIPE2 + WL / 2
    vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 700), paint(shader=linear((0, 0), (0, 700), [col("#000000", 0.5), col("#000000", 0)])))
    rw = math.sin(math.pi * prog(t, NOTEX, 0.4))
    if rw > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.18 * rw))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, GOLD, "#F4F2EE")
    wipe(c, t, WIPE2, WL, GOLD, "#0d1220")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", REVEAL - 0.1), ("pop", PHONE + 0.2), ("tick", PHONE + 0.6), ("pop", WATCH), ("ding", WATCH + 0.5),
          ("whoosh", Y1870 - 0.15), ("pop", CHAIN), ("pop", SAFE), ("whoosh", WRIST - 0.1), ("pop", STAYED),
          ("whoosh", BUTTONS - 0.1), ("pop", RIVETS), ("pop", RIP), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12),
          ("pop", FIFTH - 0.6), ("pop", FIFTH - 0.45), ("pop", FIFTH - 0.3), ("pop", FIFTH), ("hit", NOTEX),
          ("pop", FOURTH), ("pop", LATER), ("whoosh", WIPE2), ("pop", COINS), ("pop", COINS + 0.3), ("pop", KEYS),
          ("pop", PICK), ("whoosh", SO - 0.05)]
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

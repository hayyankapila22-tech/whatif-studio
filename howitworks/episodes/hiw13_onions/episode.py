# HIW13 — "Why do onions make you cry?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-20):
#  - Mental Floss "Why do onions make you cry?": cutting ruptures cells; an enzyme (alliinase) meets sulfur compounds that
#    are normally kept apart; the result is turned into a gas (syn-propanethial-S-oxide, "the crying factor"); nerves in
#    the eye's surface detect it and tear glands flood the eye to wash it away.
#  - All About Vision "Why do onions make you cry?": the more you cut/crush, the more you cry; a sharp knife crushes fewer
#    cells; ~30 minutes in the freezer cut the fumes noticeably; leave the root end for last (most of the irritant-forming
#    compounds); temporary irritation, no lasting harm.
#  Owner rule: no studies, plain words (no chemical names on screen).
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
ONION = "#C86FA8"; ONION_L = "#F1C9E0"; GAS = "#C8E86A"; TEAR = "#7CC8FF"; WOOD = "#B9824F"; STEEL = "#C9CED6"
CHEM_A = "#9B6BFF"; CHEM_B = "#FFC23D"; GREEN = "#1fb98a"; ICE = "#A9D8FF"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


RELAX = p0(1); SAD = kw(2); ATTACK = kw(3)
WIPE1 = p0(4) - 0.3; CELLS = kw(4); CUT = p0(5); BURST = kw(6); APART = kw(7)
WIPE2 = p0(8) - 0.3; GASt = kw(8); EYES = kw(9); STING = kw(10); TEARS = kw(11); WASH = p0(12)
SMALL = p0(13); MORE = kw(14); TRICK = p0(16); SHARP = kw(17); CHILL = kw(18); ROOT = kw(19); SO = p0(20)
WL = 0.32
IMPACTS = [ATTACK, BURST]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1):
    return math.sin(2 * math.pi * k * t / DUR)


# ---------------- parts ----------------
def bg_kitchen(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#2a2023"), col("#171214"), col("#0b090a")], [0, 0.55, 1])))
    c.drawCircle(820 + 30 * lw(t), 700, 520, paint(shader=radial(820, 700, 520, [col(ONION, 0.14), col(ONION, 0)])))
    c.drawCircle(220, 1500 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1500, 600, [col(GAS, 0.07), col(GAS, 0)])))


def board(c, x, y, a=1.0):
    r = skia.Rect.MakeLTRB(x - 400, y - 120, x + 400, y + 120)
    c.drawRoundRect(r.makeOffset(0, 26), 40, 40, paint("#000000", 0.45 * a, blur=24))
    c.drawRoundRect(r.makeOffset(0, 16), 40, 40, paint("#7a5230", a))
    c.drawRoundRect(r, 40, 40, paint(shader=linear((x - 400, y - 120), (x + 400, y + 120), [col("#D8A36D", a), col(WOOD, a), col("#9A6A3E", a)])))
    rr = random.Random(5)
    for k in range(9):
        yy = y - 100 + k * 25 + rr.uniform(-5, 5)
        p = skia.Path(); p.moveTo(x - 380, yy); p.cubicTo(x - 120, yy + rr.uniform(-12, 12), x + 120, yy + rr.uniform(-12, 12), x + 380, yy)
        c.drawPath(p, paint("#8a5a30", 0.25 * a, stroke=2))


def onion(c, x, y, s, a=1.0, half=False, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-150, 110, 150, 150), paint("#000000", 0.35 * a, blur=14))
    if not half:
        p = skia.Path(); p.moveTo(0, -210); p.cubicTo(30, -150, 180, -110, 170, 20); p.cubicTo(165, 110, 80, 145, 0, 145)
        p.cubicTo(-80, 145, -165, 110, -170, 20); p.cubicTo(-180, -110, -30, -150, 0, -210); p.close()
        c.drawPath(p, paint(shader=radial(-50, -40, 260, [col("#F2A7D0", a), col(ONION, a), col("#7E2F63", a)], [0, 0.55, 1])))
        c.save(); c.clipPath(p)
        for k in range(-3, 4):
            q = skia.Path(); q.moveTo(k * 22, -200); q.cubicTo(k * 60, -60, k * 60, 60, k * 30, 150)
            c.drawPath(q, paint("#ffffff", 0.18 * a, stroke=3))
        c.restore()
        c.drawCircle(-60, -40, 40, paint("#ffffff", 0.25 * a, blur=12))
        # roots
        for k in range(6):
            c.drawLine(-20 + k * 8, 140, -40 + k * 16, 170, paint("#E8D6B8", 0.9 * a, stroke=3))
        c.drawLine(0, -210, 8, -250, paint("#d9b98d", a, stroke=8))
    else:
        # cut half: concentric rings, flat side up
        for k in range(7, 0, -1):
            r = 26 * k
            c.drawOval(skia.Rect.MakeLTRB(-r * 1.05, -r * 0.9 + 20, r * 1.05, r * 0.9 + 20), paint(mixhex(ONION_L, "#ffffff", 0.45 if k % 2 else 0.05), a))
            c.drawOval(skia.Rect.MakeLTRB(-r * 1.05, -r * 0.9 + 20, r * 1.05, r * 0.9 + 20), paint(ONION, 0.6 * a, stroke=3))
        c.drawOval(skia.Rect.MakeLTRB(-184, -170, 184, 210), paint(ONION, a, stroke=10))
    c.restore()


def knife(c, x, y, s, rot, a=1.0, shine=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    blade = skia.Path(); blade.moveTo(-300, 0); blade.lineTo(60, -10); blade.lineTo(60, -90); blade.cubicTo(-120, -90, -240, -60, -300, 0); blade.close()
    c.drawPath(blade, paint("#000000", 0.3 * a, blur=10))
    c.drawPath(blade, paint(shader=linear((0, -90), (0, 0), [col("#f4f6f8", a), col(STEEL, a), col("#8b929c", a)])))
    c.drawLine(-296, -2, 58, -12, paint("#ffffff", 0.9 * a, stroke=3))
    if shine > 0:
        u = shine
        c.drawCircle(lerp(-260, 40, u), -30, 30, paint("#ffffff", 0.7 * a * math.sin(math.pi * u), blur=10))
    c.drawRoundRect(skia.Rect.MakeLTRB(60, -78, 290, -20), 22, 22, paint(shader=linear((0, -78), (0, -20), [col("#4a3426", a), col("#2a1d15", a)])))
    for k in range(3):
        c.drawCircle(110 + k * 60, -49, 7, paint("#d9d9d9", a))
    c.restore()


def wisp(c, t, x0, y0, x1, y1, a, seed=0, w=26):
    if a <= 0: return
    r = random.Random(seed)
    ph = r.uniform(0, 6.28)
    p = skia.Path(); n = 18
    for i in range(n + 1):
        u = i / n
        x = lerp(x0, x1, u) + 40 * math.sin(u * 7 + t * 3 + ph) * u
        y = lerp(y0, y1, u)
        p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
    c.drawPath(p, paint(GAS, 0.18 * a, stroke=w * 2.2, blur=14))
    c.drawPath(p, paint(GAS, 0.55 * a, stroke=w * 0.5, blur=3))


def gas_puffs(c, t, x0, y0, x1, y1, a, n=6, seed=0):
    if a <= 0: return
    for k in range(n):
        u = ((t * 0.45 + k / n + seed * 0.13) % 1)
        x = lerp(x0, x1, u) + 50 * math.sin(u * 8 + k * 2 + t * 2)
        y = lerp(y0, y1, eout(u))
        r = 26 + 40 * u
        c.drawCircle(x, y, r, paint(GAS, 0.22 * a * math.sin(math.pi * u), blur=10))
        c.drawCircle(x, y, r * 0.4, paint("#F2FFC0", 0.35 * a * math.sin(math.pi * u), blur=4))


def face(c, x, y, r, mood, t, a=1.0, tears=0.0):
    """mood: 'sad' or 'squint'"""
    if a <= 0: return
    c.save(); c.translate(x, y)
    c.drawCircle(0, 8, r, paint("#000000", 0.3 * a, blur=14))
    c.drawCircle(0, 0, r, paint(shader=radial(-r * 0.3, -r * 0.4, r * 1.4, [col("#FFE48A", a), col("#FFC93C", a), col("#E9A21B", a)], [0, 0.6, 1])))
    ink = paint("#5a3410", a, stroke=r * 0.09)
    if mood == "sad":
        for sx in (-1, 1):
            c.drawCircle(sx * r * 0.32, -r * 0.12, r * 0.08, paint("#5a3410", a))
            c.drawLine(sx * r * 0.18, -r * 0.38, sx * r * 0.46, -r * 0.30, ink)
        c.drawArc(skia.Rect.MakeLTRB(-r * 0.32, r * 0.28, r * 0.32, r * 0.7), 200, 140, False, ink)
    else:
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(sx * r * 0.48, -r * 0.08); p.lineTo(sx * r * 0.2, -r * 0.18); p.lineTo(sx * r * 0.48, -r * 0.3)
            c.drawPath(p, ink)
        c.drawLine(-r * 0.25, r * 0.4, r * 0.25, r * 0.4, ink)
    if tears > 0:
        for sx in (-1, 1):
            for k in range(2):
                d = (t * 1.4 + k * 0.5 + (0 if sx < 0 else 0.25)) % 1
                c.drawCircle(sx * r * 0.33, -r * 0.02 + r * 0.9 * d, r * 0.09, paint(TEAR, tears * a * (1 - d)))
    c.restore()


def eye(c, t, x, y, s, red=0.0, tears=0.0, squint=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    op = 1 - 0.45 * squint
    e = skia.Path(); e.moveTo(-260, 0); e.cubicTo(-140, -170 * op, 140, -170 * op, 260, 0); e.cubicTo(140, 150 * op, -140, 150 * op, -260, 0); e.close()
    # skin around
    c.drawOval(skia.Rect.MakeLTRB(-380, -260, 380, 240), paint(shader=radial(0, -20, 400, [col("#F1BE9B"), col("#D99C76"), col("#B97B57")], [0, 0.7, 1])))
    c.drawPath(e, paint("#000000", 0.25, blur=10))
    c.drawPath(e, paint(shader=radial(0, 0, 260, [col("#ffffff"), col(mixhex("#F2ECE8", "#F4B0A8", red)), col(mixhex("#d9cfc9", "#E07A72", red))], [0, 0.7, 1])))
    c.save(); c.clipPath(e)
    if red > 0:
        rr = random.Random(2)
        for k in range(10):
            sx = rr.choice((-1, 1)) * rr.uniform(150, 255); sy = rr.uniform(-60, 60)
            p = skia.Path(); p.moveTo(sx, sy); p.cubicTo(sx * 0.8, sy + rr.uniform(-30, 30), sx * 0.65, sy + rr.uniform(-30, 30), sx * 0.55, sy + rr.uniform(-20, 20))
            c.drawPath(p, paint("#D0434B", 0.75 * red, stroke=3))
    gx = 10 * math.sin(t * 1.3)
    c.drawCircle(gx, 0, 95, paint(shader=radial(gx, 0, 95, [col("#5a3a1e"), col("#8a5a2e"), col("#3a2410")], [0, 0.7, 1])))
    c.drawCircle(gx, 0, 42, paint("#0d0806"))
    c.drawCircle(gx - 30, -34, 18, paint("#ffffff", 0.9))
    if tears > 0:
        c.drawRect(skia.Rect.MakeLTRB(-270, 30 - 60 * tears, 270, 160), paint(TEAR, 0.35 * tears))
        c.drawPath(e, paint("#ffffff", 0.35 * tears, stroke=10, blur=4))
    c.restore()
    # lids
    c.drawPath(e, paint("#8a4f33", 0.9, stroke=8))
    for k in range(9):
        u = (k + 0.5) / 9
        x = lerp(-200, 200, u); yy = -150 * op * math.sin(math.pi * (0.12 + 0.76 * u)) * 0.98
        c.drawLine(x, yy, x * 1.12, yy - 46, paint("#2a1a12", 1, stroke=6))
    if tears > 0:
        for k in range(3):
            d = (t * 0.9 + k / 3) % 1
            tx = -190 + k * 140
            p = skia.Path(); p.addCircle(tx, 90 + 240 * d, 18)
            p.moveTo(tx - 16, 84 + 240 * d); p.lineTo(tx, 50 + 240 * d); p.lineTo(tx + 16, 84 + 240 * d); p.close()
            c.drawPath(p, paint(TEAR, tears * (1 - d * 0.7)))
            c.drawCircle(tx - 6, 84 + 240 * d, 5, paint("#ffffff", 0.8 * tears * (1 - d)))
    c.restore()


# ---------------- hook ----------------
def chop(t):
    return 0.5 + 0.5 * math.sin(2 * math.pi * 9 * t / DUR) ** 3


def scene_hook(c, t):
    bg_kitchen(c, t)
    board(c, 495, 1240)
    onion(c, 400, 1110, 1.2, 1.0, t=t)
    k = chop(t)
    knife(c, 610, lerp(960, 1050, k), 0.95, -10 + 5 * k)
    gas_puffs(c, t, 400, 950, 600, 600, 0.9, 5)
    face(c, 820, 700, 95, "squint", t, 1.0, tears=1.0)


def scene_open(c, t):
    scene_hook(c, t)
    pill(c, t, "WHY THE TEARS?", 495, 560, ONION, 0.35, RELAX - 0.05)
    sa = window(t, SAD - 0.2, ATTACK - 0.02, 0.2, 0.15)
    if sa > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 0.65 * sa))
        s = eback(prog(t, SAD - 0.2, 0.3))
        c.save(); c.translate(495, 920); c.scale(s, s); c.translate(-495, -920)
        face(c, 495, 920, 190, "sad", t, sa)
        x = eout(prog(t, SAD + 0.2, 0.25))
        c.drawLine(310, 740, lerp(310, 680, x), lerp(740, 1100, x), paint(RED, sa, stroke=22))
        c.restore()
    aa = window(t, ATTACK - 0.05, WIPE1 + 0.2, 0.05, 0.2)
    if aa > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.18 * aa * (0.6 + 0.4 * math.sin(t * 18))))
        for k in range(3):
            u = prog(t, ATTACK - 0.05 + k * 0.12, 0.7)
            c.drawCircle(400, 1080, 120 + 340 * u, paint(GAS, 0.6 * aa * (1 - u), stroke=8))
    pill(c, t, "NOT SAD", 495, 560, "#8a8f98", SAD, ATTACK - 0.05)
    pill(c, t, "UNDER ATTACK!", 495, 560, RED, ATTACK, WIPE1 + 0.1)


# ---------------- white: cells ----------------
HEX_R = 62
CELLS_XY = []
for row in range(-1, 12):
    for colm in range(-1, 10):
        x = colm * HEX_R * 1.75 + (HEX_R * 0.875 if row % 2 else 0) + 40
        y = row * HEX_R * 1.52 + 640
        CELLS_XY.append((x, y))
CUT_Y = lambda x: 1050 - 0.18 * (x - 540)


def hexpath(x, y, r):
    p = skia.Path()
    for k in range(6):
        an = math.pi / 6 + k * math.pi / 3
        (p.moveTo if k == 0 else p.lineTo)(x + r * math.cos(an), y + r * math.sin(an))
    p.close(); return p


def scene_cells(c, t):
    studio_white(c)
    ga = eout(prog(t, WIPE1, 0.4))
    zoom = lerp(1.25, 1.0, eio(prog(t, WIPE1, 1.2)))
    c.save(); c.translate(495, 1000); c.scale(zoom, zoom); c.translate(-495, -1000)
    clip = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(90, 660, 900, 1400), 40, 40)
    c.drawRRect(clip, paint("#000000", 0.12 * ga, blur=18))
    c.save(); c.clipRRect(clip, doAntiAlias=True)
    c.drawRRect(clip, paint(ONION_L, ga))
    cutp = eio(prog(t, CUT - 0.05, 0.7))       # knife sweep progress (x from left to right)
    kx = lerp(60, 940, cutp)
    mix = eio(prog(t, APART + 0.1, 0.8))
    for i, (x, y) in enumerate(CELLS_XY):
        d = abs(y - CUT_Y(x))
        near = d < HEX_R * 1.4
        burst = near and x < kx and t > BURST - 0.25
        bu = prog(t, BURST - 0.25 + (x - 40) / 960 * 0.4, 0.25) if burst else 0
        r = HEX_R * 0.95 * (1 + 0.08 * math.sin(t * 2 + i))
        if bu < 1:
            c.drawPath(hexpath(x, y, r * (1 + 0.25 * bu)), paint(shader=radial(x - 15, y - 15, r * 1.3, [col("#ffffff", ga * (1 - bu)), col("#F8E1EF", ga * (1 - bu)), col(ONION_L, ga * (1 - bu))])))
            c.drawPath(hexpath(x, y, r * (1 + 0.25 * bu)), paint(ONION, 0.7 * ga * (1 - bu), stroke=4))
        # two chemicals kept apart: A in a small inner bag, B around it
        ca = ga * prog(t, CELLS + 0.2, 0.4)
        if ca > 0 and bu < 1:
            c.drawCircle(x - 14, y - 8, 14, paint(CHEM_A, 0.85 * ca * (1 - bu)))
            c.drawCircle(x - 14, y - 8, 20, paint(CHEM_A, 0.5 * ca * (1 - bu), stroke=3))
            c.drawCircle(x + 20, y + 16, 9, paint(CHEM_B, 0.9 * ca * (1 - bu)))
        if bu > 0 and bu < 1:
            c.drawCircle(x, y, HEX_R * (0.6 + 0.8 * bu), paint("#ffffff", 0.7 * ga * (1 - bu), blur=8))
        if bu > 0:   # pieces + mixing burst
            rr = random.Random(i)
            for k in range(8):
                an = rr.uniform(0, 6.28); dist = 30 + 70 * eout(bu) + 50 * mix
                px, py = x + math.cos(an) * dist, y + math.sin(an) * dist - 60 * mix
                cc = CHEM_A if k % 2 else CHEM_B
                if mix > 0.3: cc = mixhex(cc, GAS, (mix - 0.3) / 0.7)
                c.drawCircle(px, py, 9, paint(cc, ga))
    if t > CUT - 0.05:   # the cut line behind the knife
        lp = skia.Path(); lp.moveTo(60, CUT_Y(60)); lp.lineTo(kx, CUT_Y(kx))
        c.drawPath(lp, paint("#7E2F63", 0.5 * ga, stroke=10, blur=3))
    c.restore()
    c.drawRRect(clip, paint(ONION, 0.6 * ga, stroke=5))
    # knife sweeping along the cut
    ka = window(t, CUT - 0.25, APART + 0.2, 0.2, 0.3)
    if ka > 0:
        knife(c, kx + 70, CUT_Y(kx) - 10, 0.9, -10, ka, shine=prog(t, CUT, 0.6))
    c.restore()
    pill(c, t, "TINY CELLS", 495, 560, ONION, CELLS, CUT - 0.05)
    pill(c, t, "BURST!", 495, 560, RED, BURST, APART - 0.05)
    pill(c, t, "KEPT APART", 300, 560, CHEM_A, APART, WIPE2 + 0.1)
    pill(c, t, "NOW THEY MIX", 690, 560, "#C9A100", APART + 0.5, WIPE2 + 0.1, text_col="#FFFFFF")


# ---------------- dark: gas -> eyes ----------------
def scene_eye(c, t):
    bg_kitchen(c, t)
    # camera tilts from the board (bottom) up to the eye (top)
    up = eio(prog(t, EYES - 0.3, 0.8))
    c.save(); c.translate(0, lerp(-250, 380, up))
    board(c, 495, 1500)
    onion(c, 495, 1400, 1.0, 1.0, half=True, t=t)
    for k in range(4):
        wisp(c, t, 420 + k * 50, 1330, 380 + k * 90, lerp(900, 380, up), eout(prog(t, GASt - 0.25 + k * 0.08, 0.5)) * (1 - prog(t, WASH, 0.6)), seed=k)
    gas_puffs(c, t, 495, 1300, 495, lerp(900, 420, up), eout(prog(t, GASt - 0.2, 0.4)) * (1 - prog(t, WASH, 0.6)), 7, 1)
    c.restore()
    ea = up
    if ea > 0:
        c.save(); c.translate(0, lerp(-700, 0, ea))
        eye(c, t, 495, 860, 1.0, red=eout(prog(t, STING - 0.1, 0.4)) * (1 - 0.6 * prog(t, WASH, 0.6)),
            tears=eout(prog(t, TEARS - 0.1, 0.5)), squint=window(t, STING - 0.1, WASH + 0.4, 0.2, 0.3))
        c.restore()
        if STING - 0.1 < t < TEARS + 0.4:
            u = (t * 1.4) % 1
            for k in range(2):
                c.drawCircle(495, 860, 280 + 120 * ((u + k * 0.5) % 1), paint(RED, 0.5 * (1 - (u + k * 0.5) % 1) * window(t, STING - 0.1, TEARS + 0.4, 0.1, 0.2), stroke=6))
    pill(c, t, "A GAS", 495, 560, "#8FAE2E", GASt, EYES - 0.05, text_col="#FFFFFF")
    pill(c, t, "UP TO YOUR EYES", 495, 560, "#8FAE2E", EYES, STING - 0.05, text_col="#FFFFFF")
    pill(c, t, "STING!", 495, 560, RED, STING, TEARS - 0.05)
    pill(c, t, "TEARS", 495, 560, TEAR, TEARS, WASH - 0.05, text_col=INK)
    pill(c, t, "WASH IT AWAY", 495, 560, TEAR, WASH, SMALL - 0.1, text_col=INK)


def scene_pieces(c, t):
    bg_kitchen(c, t)
    a = eout(prog(t, SMALL - 0.25, 0.35))
    for i, (x, n, tin) in enumerate(((270, 2, SMALL), (720, 7, MORE))):
        q = eback(prog(t, tin - 0.15, 0.35))
        if q <= 0: continue
        c.save(); c.translate(x, 1000); c.scale(1.08 * q, 1.08 * q)
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -330, 200, 300), 34, 34, paint("#000000", 0.3, blur=18))
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -330, 200, 300), 34, 34, paint("#221c1d"))
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -330, 200, 300), 34, 34, paint(GAS if i else "#8a8f98", 0.9, stroke=4))
        # pieces on a mini board
        c.drawRoundRect(skia.Rect.MakeLTRB(-160, 150, 160, 240), 22, 22, paint(WOOD))
        rr = random.Random(i + 3)
        cnt = 2 if i == 0 else 22
        for k in range(cnt):
            if i == 0:
                px, py, s = -60 + k * 120, 140, 50
            else:
                px, py, s = rr.uniform(-130, 130), rr.uniform(120, 175), rr.uniform(14, 20)
            c.drawRoundRect(skia.Rect.MakeXYWH(px - s, py - s * 0.7, 2 * s, 1.4 * s), s * 0.35, s * 0.35, paint(ONION_L))
            c.drawRoundRect(skia.Rect.MakeXYWH(px - s, py - s * 0.7, 2 * s, 1.4 * s), s * 0.35, s * 0.35, paint(ONION, 0.8, stroke=3))
        gas_puffs(c, t, 0, 130, 0, -240, 1.0, n * 2, i)
        if i: gas_puffs(c, t, -80, 130, -60, -220, 1.0, n, 5); gas_puffs(c, t, 80, 130, 70, -220, 1.0, n, 7)
        f = skia.Font(TF_MONO, 26)
        lab = "BIG CHUNKS" if i == 0 else "TINY DICE"
        c.drawString(lab, -f.measureText(lab) / 2, -280, f, paint("#ffffff", 0.8))
        c.restore()
    pill(c, t, "MORE GAS", 495, 560, "#8FAE2E", MORE, TRICK - 0.1, text_col="#FFFFFF")
    pill(c, t, "MORE TEARS", 495, 1440, TEAR, p0(15), TRICK - 0.1, text_col=INK)


def tip_card(c, t, x, y, kind, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    c.drawRoundRect(skia.Rect.MakeLTRB(-135, -170, 135, 170), 30, 30, paint("#000000", 0.3, blur=14))
    c.drawRoundRect(skia.Rect.MakeLTRB(-135, -170, 135, 170), 30, 30, paint("#2a2729"))
    c.drawRoundRect(skia.Rect.MakeLTRB(-135, -170, 135, 170), 30, 30, paint("#ffffff", 0.14, stroke=2))
    f = skia.Font(TF_MONO, 26)
    if kind == "sharp":
        knife(c, 30, 10, 0.55, -30, 1.0, shine=(t * 0.8) % 1)
        lab, cc = "SHARP KNIFE", STEEL
    elif kind == "chill":
        for k in range(6):
            an = k * math.pi / 3 + t * 0.6
            c.drawLine(0, -10, 70 * math.cos(an), -10 + 70 * math.sin(an), paint(ICE, 1, stroke=9))
        big = skia.Font(TF_BLACK, 50); s = "30 MIN"
        c.drawString(s, -big.measureText(s) / 2, 110, big, paint("#ffffff"))
        lab, cc = "CHILL IT", ICE
    else:
        onion(c, 0, -20, 0.42, 1.0)
        g = 0.5 + 0.5 * math.sin(t * 6)
        c.drawCircle(0, 44, 34, paint(RED, 0.35 + 0.3 * g, blur=8))
        c.drawCircle(0, 44, 30, paint(RED, 1, stroke=5))
        lab, cc = "ROOT LAST", RED
    c.drawString(lab, -f.measureText(lab) / 2, 150, f, paint(cc))
    c.restore()


def scene_tips(c, t):
    bg_kitchen(c, t)
    for i, (x, y, kind, tin) in enumerate(((245, 820, "sharp", SHARP), (495, 1240, "chill", CHILL), (745, 820, "root", ROOT))):
        q = eback(prog(t, tin - 0.15, 0.35))
        tip_card(c, t, x, y, kind, 1.15 * clamp(q, 0, 1.2))
        if q > 0.9:
            ck = eout(prog(t, tin + 0.25, 0.25))
            c.drawCircle(x + 130, y - 172, 34, paint(GREEN, ck))
            p = skia.Path(); p.moveTo(x + 114, y - 172); p.lineTo(x + 126, y - 158); p.lineTo(x + 150, y - 186)
            c.drawPath(p, paint("#ffffff", ck, stroke=8))
    pill(c, t, "THE TRICK", 495, 560, GREEN, TRICK, SHARP - 0.05, text_col="#FFFFFF")
    pill(c, t, "SHARP KNIFE", 495, 560, "#8a929c", SHARP, CHILL - 0.05, text_col="#FFFFFF")
    pill(c, t, "CHILL 30 MIN", 495, 560, ICE, CHILL, ROOT - 0.05, text_col=INK)
    pill(c, t, "ROOT LAST", 495, 560, RED, ROOT, SO + 0.3)


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_cells(c, t); return
    if t < SMALL - 0.25:
        scene_eye(c, t); return
    if t < TRICK - 0.25:
        scene_pieces(c, t)
        q = 1 - prog(t, SMALL - 0.25, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_eye(c, t); c.restore()
        return
    if t < SO - 0.05:
        scene_tips(c, t)
        q = 1 - prog(t, TRICK - 0.25, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_pieces(c, t); c.restore()
        return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_tips(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.022 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"onions": ONION, "sad": "#8a8f98", "attack": RED, "cells": ONION, "burst": RED, "apart": CHEM_A, "gas": "#9FC23A",
         "eyes": "#9FC23A", "sting": RED, "tears": TEAR, "More": "#9FC23A", "sharp": STEEL, "30": ICE, "root": RED}
CAPS = Captions(P, KWCOL, {"attack!", "burst,"}, DUR)


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
    wipe(c, t, WIPE1, WL, ONION, "#F4F2EE")
    wipe(c, t, WIPE2, WL, GAS, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("pop", SAD), ("hit", ATTACK), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12),
          ("pop", CELLS), ("whoosh", CUT - 0.05), ("hit", BURST), ("pop", APART), ("pop", APART + 0.5), ("whoosh", WIPE2),
          ("riser", GASt - 0.2), ("whoosh", EYES - 0.3), ("hit", STING), ("pop", TEARS), ("pop", WASH),
          ("whoosh", SMALL - 0.25), ("pop", SMALL), ("pop", MORE), ("whoosh", TRICK - 0.25), ("pop", SHARP),
          ("pop", CHILL), ("pop", ROOT), ("whoosh", SO - 0.05)]
    for k in range(4):
        ev.append(("tick", CUT + 0.1 + k * 0.12))
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

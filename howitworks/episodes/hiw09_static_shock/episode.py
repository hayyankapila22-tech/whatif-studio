# HIW09 — why car doors (and trolleys) give you a static shock. Basic + useful, detailed objects, "So," loop.
# Sources (fact-checked 2026-11-19):
#  - Library of Congress, Everyday Mysteries "How does static electricity work?": rubbing moves electrons, charge builds
#    on you, released as a shock when you touch something.
#  - AccuWeather (2023) "How to avoid getting shocked by static electricity during winter": shocks range ~4,000-35,000 V
#    but carry almost no current (hurt, not dangerous); cold dry air = more shocks; car tip (touch metal / dryer sheet).
#  - Jalopnik "How to stop static shock when exiting car": sliding across the seat charges you; keep a hand on the metal
#    frame as you slide out; touch the car with your key or a metal ring first.
#  - J. Smallwood, Electrostatic Solutions (2007): trolleys charge up; tyres and floor are highly insulating so charge
#    can't leak away; discharges last a few hundred nanoseconds (= under a millionth of a second).
#  - YourMechanic: the car body sits near ground; the charge discharges through the first contact, your hand.
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
CAR = "#D7263D"; SKIN = "#E6B08A"; COAT = "#2E3B55"; CHG = "#FFD23F"; ZAPC = "#8FDcFF"; METAL = "#C9CED6"
GREEN = "#1fb98a"; BLUE = "#3b7de0"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


ZAP = kw(1); BROKEN = p0(2); NOTEX = kw(3); YOU = kw(4); SLIDE = p0(5); RUB = kw(6); CHARGE = kw(7)
THOUS = kw(8); WAIT = p0(9); METALT = p0(10); SPARK = kw(11)
WIPE1 = p0(12) - 0.3; TROL = kw(12); TRAP = kw(13); WORSE = p0(14); TRICK = p0(15); HOLD = kw(16); KEY = kw(17)
SO = p0(18)
WL = 0.32
IMPACTS = [ZAP, NOTEX, SPARK]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]
rnd = random.Random(9)
SNOW = [(rnd.uniform(60, 1020), rnd.uniform(0, 1), rnd.uniform(3, 8), rnd.random() * 6.28) for _ in range(40)]
ORB = [(rnd.uniform(0, 6.28), rnd.uniform(0.6, 1.0), rnd.uniform(0.7, 1.4)) for _ in range(22)]


def loopwave(t, k=1):
    """periodic in DUR, so the last frame equals frame 1"""
    return math.sin(2 * math.pi * k * t / DUR)


# ---------------- small parts ----------------
def minus(c, x, y, s, a, colr=CHG):
    if a <= 0: return
    c.drawCircle(x, y, 22 * s, paint(colr, 0.22 * a, blur=8))
    c.drawCircle(x, y, 15 * s, paint(colr, a))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 8 * s, y - 2.5 * s, x + 8 * s, y + 2.5 * s), 2, 2, paint(INK, a))


def bolt(c, x1, y1, x2, y2, t, a, width=7, seed=0, colr=ZAPC):
    if a <= 0: return
    r = random.Random(int(t * 30) * 7 + seed)
    n = 9
    pts = []
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / L, dx / L
    for i in range(n + 1):
        u = i / n
        off = 0 if i in (0, n) else r.uniform(-1, 1) * L * 0.09
        pts.append((x1 + dx * u + nx * off, y1 + dy * u + ny * off))
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    c.drawPath(p, paint(colr, 0.45 * a, stroke=width * 4, blur=14))
    c.drawPath(p, paint(colr, a, stroke=width))
    c.drawPath(p, paint("#ffffff", a, stroke=width * 0.4))
    # small branch
    k = r.randint(2, n - 3)
    bx, by = pts[k]
    p2 = skia.Path(); p2.moveTo(bx, by); p2.lineTo(bx + nx * L * 0.15 + dx * 0.08, by + ny * L * 0.15 + dy * 0.08)
    c.drawPath(p2, paint(colr, 0.8 * a, stroke=width * 0.5))


def hand(c, x, y, ang, s, a=1.0, sleeve=COAT, curl=0.0):
    """pointing hand: fingertip at (x, y), finger along +x rotated by ang degrees."""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-760, -96, -235, 104), 60, 60, paint("#000000", 0.25 * a, blur=16))
    c.drawRoundRect(skia.Rect.MakeLTRB(-760, -100, -240, 96), 60, 60, paint(shader=linear((0, -100), (0, 96), [col("#4a5a7c", a), col(sleeve, a), col("#1b2438", a)], [0, 0.5, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(-300, -104, -232, 100), 30, 30, paint(shader=linear((0, -104), (0, 100), [col("#56688e", a), col("#1f2a42", a)])))
    sk = linear((0, -80), (0, 80), [col("#F3C6A2", a), col(SKIN, a), col("#B97F59", a)], [0, 0.5, 1])
    c.drawRoundRect(skia.Rect.MakeLTRB(-250, -72, -96, 74), 52, 52, paint(shader=sk))                 # palm
    # curled fingers (knuckles)
    for k in range(3):
        c.drawRoundRect(skia.Rect.MakeLTRB(-150 + k * 6, -4 + k * 24, -66 + k * 4, 34 + k * 24), 19, 19, paint(shader=sk))
        c.drawLine(-120 + k * 6, 6 + k * 24, -120 + k * 6, 26 + k * 24, paint("#9b6646", 0.35 * a, stroke=2))
    # thumb
    c.save(); c.translate(-165, -34); c.rotate(-3)
    c.drawRoundRect(skia.Rect.MakeLTRB(-20, -22, 66, 18), 20, 20, paint(shader=sk))
    c.drawLine(40, -10, 40, 10, paint("#9b6646", 0.3 * a, stroke=2)); c.restore()
    # index finger
    fl = 150 * (1 - 0.35 * curl)
    c.drawRoundRect(skia.Rect.MakeLTRB(-150 + (150 - fl), -22, 2, 22), 22, 22, paint(shader=linear((0, -22), (0, 22), [col("#F6CDAA", a), col(SKIN, a), col("#B97F59", a)], [0, 0.5, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(-36, -20, -6, -6), 6, 6, paint("#fde6d6", 0.9 * a))           # nail
    c.drawLine(-62, -16, -62, 16, paint("#9b6646", 0.35 * a, stroke=2))
    c.restore()


# ---------------- car door close-up (hook) ----------------
def door_close(c, t, flash=0.0):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#0d1220"), col("#141b2e"), col("#0a0d16")], [0, 0.5, 1])))
    dx = 10 * loopwave(t); dy = 6 * loopwave(t, 2)
    c.save(); c.translate(dx, dy)
    # window glass
    gl = skia.Path(); gl.moveTo(40, 760); gl.lineTo(140, 470); gl.lineTo(1080, 470); gl.lineTo(1080, 760); gl.close()
    c.drawPath(gl, paint(shader=linear((0, 470), (0, 760), [col("#2c3f63"), col("#121a2c")])))
    for k, (x0, w) in enumerate(((300, 80), (430, 30), (760, 120))):
        rp = skia.Path(); rp.moveTo(x0, 760); rp.lineTo(x0 + 120, 470); rp.lineTo(x0 + 120 + w, 470); rp.lineTo(x0 + w, 760); rp.close()
        c.drawPath(rp, paint("#9fc2ff", 0.10 + 0.04 * k))
    c.drawPath(gl, paint("#05070c", 1, stroke=14))
    # body panel
    body = skia.Rect.MakeLTRB(0, 760, W, 1560)
    c.drawRect(body, paint(shader=linear((0, 760), (0, 1560), [col("#ff5a6a"), col(CAR), col("#8c1424"), col("#5a0c18")], [0, 0.25, 0.75, 1])))
    # body line + reflection streaks (slow drift)
    c.drawLine(0, 905, W, 885, paint("#ffb3bb", 0.55, stroke=4))
    c.drawLine(0, 912, W, 892, paint("#5a0c18", 0.5, stroke=4))
    for k in range(3):
        x = (180 + k * 330 + 40 * loopwave(t)) % (W + 300) - 150
        rp = skia.Path(); rp.moveTo(x, 760); rp.lineTo(x + 90, 760); rp.lineTo(x - 60, 1560); rp.lineTo(x - 150, 1560); rp.close()
        c.drawPath(rp, paint("#ffffff", 0.07, blur=10))
    # door seam
    c.drawLine(110, 760, 70, 1560, paint("#3a060d", 0.9, stroke=6))
    c.drawLine(116, 760, 76, 1560, paint("#ff8b96", 0.35, stroke=2))
    # handle recess + chrome handle
    c.drawRoundRect(skia.Rect.MakeLTRB(470, 960, 790, 1060), 46, 46, paint(shader=linear((0, 960), (0, 1060), [col("#5a0c18"), col("#a51c2e")])))
    c.drawRoundRect(skia.Rect.MakeLTRB(490, 985, 770, 1040), 28, 28, paint("#000000", 0.35, blur=8))
    c.drawRoundRect(skia.Rect.MakeLTRB(490, 975, 770, 1030), 28, 28, paint(shader=linear((0, 975), (0, 1030), [col("#ffffff"), col(METAL), col("#7d8590"), col("#d9dde3")], [0, 0.35, 0.7, 1])))
    c.drawLine(520, 986, 740, 986, paint("#ffffff", 0.9, stroke=4))
    # side mirror shadow / glow on handle at zap
    if flash > 0:
        c.drawCircle(500, 1000, 260, paint(shader=radial(500, 1000, 260, [col(ZAPC, 0.6 * flash), col(ZAPC, 0)])))
    c.restore()


def hook_scene(c, t):
    door_close(c, t)
    hand(c, 300 + 14 * loopwave(t), 1260 + 10 * loopwave(t, 2), -32, 1.0)


def scene_door(c, t):
    r = eio(prog(t, 0.12, ZAP - 0.22)) if t > 0.12 else 0
    recoil = eout(prog(t, ZAP + 0.08, 0.35))
    fl = window(t, ZAP - 0.02, ZAP + 0.45, 0.04, 0.3)
    door_close(c, t, fl)
    hx = lerp(300 + 14 * loopwave(t), 470, r) - 170 * recoil
    hy = lerp(1260 + 10 * loopwave(t, 2), 1030, r) + 160 * recoil
    hand(c, hx, hy, -32 + 22 * r - 10 * recoil, 1.0, curl=0.3 * recoil)
    if t >= ZAP - 0.03 and t < ZAP + 0.35:
        bolt(c, 470, 1030, 520, 1005, t, 1 - prog(t, ZAP + 0.15, 0.2), width=8)
        bolt(c, 470, 1030, 560, 1040, t, 0.7 * (1 - prog(t, ZAP + 0.1, 0.2)), width=5, seed=3)
    if fl > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#e8f6ff", 0.55 * fl * (1 - prog(t, ZAP, 0.25))))
    pill(c, t, "ZAP!", 640, 1210, ZAPC, ZAP + 0.05, BROKEN - 0.1)


# ---------------- whole car (dark studio) ----------------
def car_side(c, x, y, s, a=1.0, glow=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-420, 150, 420, 210), paint("#000000", 0.45 * a, blur=18))
    bp = skia.Path()
    bp.moveTo(-400, 120); bp.lineTo(-405, 20); bp.cubicTo(-400, -20, -360, -40, -300, -50)
    bp.lineTo(-170, -70); bp.cubicTo(-110, -150, -60, -175, 40, -175); bp.cubicTo(130, -175, 170, -150, 230, -70)
    bp.lineTo(350, -50); bp.cubicTo(395, -40, 410, -10, 410, 30); bp.lineTo(405, 120); bp.close()
    c.drawPath(bp, paint(shader=linear((0, -175), (0, 130), [col("#ff6b7a", a), col(CAR, a), col("#7a1020", a)], [0, 0.45, 1])))
    gp = skia.Path(); gp.moveTo(-150, -70); gp.cubicTo(-100, -140, -60, -155, 30, -155); gp.lineTo(30, -70); gp.close()
    c.drawPath(gp, paint(shader=linear((0, -155), (0, -70), [col("#4a6fa8", a), col("#1a2740", a)])))
    gp2 = skia.Path(); gp2.moveTo(50, -155); gp2.cubicTo(120, -155, 160, -130, 205, -70); gp2.lineTo(50, -70); gp2.close()
    c.drawPath(gp2, paint(shader=linear((0, -155), (0, -70), [col("#4a6fa8", a), col("#1a2740", a)])))
    c.drawLine(-380, -10, 400, -18, paint("#ffb3bb", 0.5 * a, stroke=3))
    c.drawLine(40, -70, 40, 110, paint("#4a0912", 0.8 * a, stroke=3))
    c.drawLine(-170, -70, -175, 110, paint("#4a0912", 0.8 * a, stroke=3))
    c.drawRoundRect(skia.Rect.MakeLTRB(-90, -30, -40, -16), 7, 7, paint(METAL, a))
    c.drawRoundRect(skia.Rect.MakeLTRB(110, -30, 160, -16), 7, 7, paint(METAL, a))
    c.drawRoundRect(skia.Rect.MakeLTRB(370, -30, 410, 0), 10, 10, paint("#fff3c4", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-408, -24, -385, 4), 6, 6, paint("#ff3b30", a))
    for wx in (-250, 250):
        c.drawCircle(wx, 120, 82, paint("#0b0b0e", a))
        c.drawCircle(wx, 120, 82, paint("#26262c", a, stroke=6))
        c.drawCircle(wx, 120, 48, paint(shader=radial(wx - 10, 110, 60, [col("#f2f4f7", a), col("#8b929c", a)])))
        for k in range(5):
            ang = k * 72 * math.pi / 180
            c.drawLine(wx, 120, wx + 40 * math.cos(ang), 120 + 40 * math.sin(ang), paint("#5d636c", a, stroke=6))
        c.drawCircle(wx, 120, 10, paint("#3a3f46", a))
    if glow > 0:
        c.drawPath(bp, paint(ZAPC, 0.5 * glow * a, stroke=6, blur=4))
    c.restore()


def person(c, x, y, s, a=1.0, charged=0.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if charged > 0:
        c.drawCircle(0, -150, 300, paint(shader=radial(0, -150, 300, [col(CHG, 0.30 * charged * a), col(CHG, 0)])))
    for sx in (-1, 1):
        c.drawRoundRect(skia.Rect.MakeLTRB(sx * 34 - 26, 20, sx * 34 + 26, 270), 26, 26, paint(shader=linear((sx * 34 - 26, 0), (sx * 34 + 26, 0), [col("#4c5a7c", a), col("#28324a", a)])))
        c.drawRoundRect(skia.Rect.MakeLTRB(sx * 34 - 34, 255, sx * 34 + 40, 285), 15, 15, paint("#1a1a1e", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-88, -180, 88, 70), 50, 50, paint(shader=linear((-88, 0), (88, 0), [col("#5d7096", a), col(COAT, a), col("#1b2438", a)], [0, 0.5, 1])))
    c.drawLine(0, -170, 0, 60, paint("#141b2b", 0.8 * a, stroke=4))
    for sx in (-1, 1):
        c.drawLine(sx * 84, -150, sx * 104, -10, paint(COAT, a, stroke=42))
        c.drawCircle(sx * 106, 14, 22, paint(SKIN, a))
    c.drawCircle(0, -245, 70, paint(shader=radial(-20, -270, 100, [col("#F6C9A8", a), col(SKIN, a), col("#B57D58", a)], [0, 0.55, 1])))
    hp = skia.Path(); hp.moveTo(-72, -245); hp.cubicTo(-80, -335, 70, -355, 74, -255); hp.cubicTo(40, -295, -30, -305, -72, -245); hp.close()
    c.drawPath(hp, paint(shader=linear((0, -345), (0, -245), [col("#4a2f1e", a), col("#24160d", a)])))
    if charged > 0.4:   # hair a little on end
        for k in range(7):
            ang = math.radians(-160 + k * 23)
            c.drawLine(70 * math.cos(ang), -265 + 70 * math.sin(ang), 92 * math.cos(ang), -265 + 92 * math.sin(ang), paint("#24160d", a * (charged - 0.4) / 0.6, stroke=5))
    for sx in (-1, 1):
        c.drawCircle(sx * 24, -245, 8, paint("#2e1c11", a))
    c.drawArc(skia.Rect.MakeLTRB(-18, -228, 18, -206), 20, 140, False, paint("#8a4a3a", a, stroke=4))
    c.restore()
    if charged > 0:
        for i, (ph, rr, sp) in enumerate(ORB[:int(6 + 16 * charged)]):
            ang = ph + t * sp
            ox = x + math.cos(ang) * 150 * s * rr
            oy = y - 120 * s + math.sin(ang) * 260 * s * rr
            minus(c, ox, oy, 0.9 * s / 0.9, charged * a)


def scene_car(c, t):
    studio_dark(c)
    zo = eio(prog(t, BROKEN - 0.15, 0.5))
    mv = eio(prog(t, YOU - 0.25, 0.5))
    car_side(c, lerp(540, 380, mv), lerp(1080, 1120, mv), lerp(1.6, 0.85, zo) * lerp(1, 0.78, mv), 1.0)
    if t < NOTEX + 0.2:
        pill(c, t, "BROKEN?", 490, 1360, "#FFFFFF", BROKEN + 0.1, YOU - 0.2)
    else:
        pill(c, t, "BROKEN?", 490, 1360, "#FFFFFF", BROKEN + 0.1, YOU - 0.2)
    if t > NOTEX:
        xa = eout(prog(t, NOTEX, 0.18)) * (1 - prog(t, YOU - 0.25, 0.2))
        c.drawLine(380, 1360, lerp(380, 600, xa), 1360, paint(RED, xa, stroke=8))
    pa = eout(prog(t, YOU - 0.15, 0.4))
    if pa > 0:
        ch = eout(prog(t, YOU, 0.5))
        person(c, lerp(900, 740, pa), 1060, 0.9, pa, ch, t)
        pill(c, t, "IT'S YOU", 740, 1400, CHG, YOU + 0.1, SLIDE - 0.15)


# ---------------- car seat close-up ----------------
def scene_seat(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#1a1f2c"), col("#10141d")])))
    # seat cushion + backrest (side view)
    c.drawRoundRect(skia.Rect.MakeLTRB(60, 560, 260, 1260), 60, 60, paint(shader=linear((60, 0), (260, 0), [col("#4a4f5c"), col("#2b2f38")])))
    for k in range(6):
        c.drawLine(80, 640 + k * 100, 240, 640 + k * 100, paint("#1c1f26", 0.8, stroke=4))
    c.drawRoundRect(skia.Rect.MakeLTRB(120, 1120, 900, 1330), 70, 70, paint(shader=linear((0, 1120), (0, 1330), [col("#5a606e"), col("#353a45"), col("#22252d")], [0, 0.5, 1])))
    for k in range(7):
        x = 220 + k * 105
        c.drawLine(x, 1140, x, 1310, paint("#1c1f26", 0.6, stroke=4))
    # stitched texture dots
    for k in range(40):
        c.drawCircle(150 + k * 19, 1150, 2, paint("#8a909c", 0.5))
    # leg (jeans) sliding to the right
    sl = eio(prog(t, SLIDE, 1.9))
    lx = lerp(0, 150, sl)
    # lower leg + shoe hanging off the front of the seat
    kx = 700 + lx
    c.drawRoundRect(skia.Rect.MakeLTRB(kx - 120, 1040, kx - 10, 1400), 50, 50, paint(shader=linear((kx - 120, 0), (kx - 10, 0), [col("#4f73ad"), col("#2a426b")])))
    c.drawRoundRect(skia.Rect.MakeLTRB(kx - 140, 1370, kx + 50, 1430), 28, 28, paint(shader=linear((0, 1370), (0, 1430), [col("#3a3a40"), col("#141416")])))
    c.drawRect(skia.Rect.MakeLTRB(kx - 140, 1418, kx + 50, 1430), paint("#e8e8e8", 0.8))
    jp = skia.Path(); jp.addRoundRect(skia.Rect.MakeLTRB(170 + lx, 980, 720 + lx, 1128), 70, 70)
    c.drawPath(jp, paint("#000000", 0.3, blur=12))
    c.drawPath(jp, paint(shader=linear((0, 980), (0, 1128), [col("#6c8fc7"), col("#3f5f94"), col("#2a426b")], [0, 0.5, 1])))
    for k in range(9):
        c.drawLine(200 + lx + k * 62, 990, 230 + lx + k * 62, 1120, paint("#8fb0e0", 0.18, stroke=3))
    c.drawLine(190 + lx, 1040, 700 + lx, 1040, paint("#d9a441", 0.5, stroke=3))
    # rub marks
    ra = window(t, RUB - 0.1, THOUS - 0.3, 0.15, 0.3)
    if ra > 0:
        for k in range(5):
            x = 260 + lx + k * 110 + 30 * math.sin(t * 18 + k)
            c.drawLine(x, 1135, x - 60, 1135, paint("#ffffff", 0.7 * ra, stroke=4))
        for k in range(4):
            bolt(c, 300 + lx + k * 130, 1128, 320 + lx + k * 130, 1110, t, 0.5 * ra, width=2, seed=k)
    # charges hopping from seat into the jeans
    ca = prog(t, RUB, 0.2)
    if ca > 0:
        n = int(4 + 18 * prog(t, RUB, 2.4))
        for k in range(n):
            u = ((t * 0.8 + k * 0.137) % 1)
            sx = 240 + (k * 83) % 560 + lx * 0.6
            settled = k < int(18 * prog(t, CHARGE - 0.3, 1.6))
            if settled:
                yy = 1010 + (k * 37) % 100 + 6 * math.sin(t * 5 + k)
                xx = 200 + lx + (k * 71) % 540
            else:
                yy = lerp(1180, 1030, u); xx = sx
            minus(c, xx, yy, 0.8, ca)
    pill(c, t, "FRICTION", 490, 840, "#FFFFFF", RUB, CHARGE - 0.1)
    pill(c, t, "EXTRA CHARGE", 490, 840, CHG, CHARGE, THOUS - 0.2)


# ---------------- voltage gauge ----------------
def scene_gauge(c, t):
    studio_dark(c)
    cx, cy, R = 490, 1080, 330
    ga = eout(prog(t, THOUS - 0.25, 0.35))
    c.save(); c.translate(cx, cy); c.scale(0.8 + 0.2 * ga, 0.8 + 0.2 * ga); c.translate(-cx, -cy)
    c.drawCircle(cx, cy, R + 40, paint("#000000", 0.4, blur=20))
    c.drawCircle(cx, cy, R + 30, paint(shader=radial(cx, cy - 60, R + 40, [col("#2c3242"), col("#151923")])))
    c.drawCircle(cx, cy, R + 30, paint(METAL, 0.6, stroke=6))
    arc = skia.Rect.MakeLTRB(cx - R + 30, cy - R + 30, cx + R - 30, cy + R - 30)
    for (a0, sw, cc) in ((180, 70, GREEN), (250, 60, CHG), (310, 50, RED)):
        c.drawArc(arc, a0, sw, False, paint(cc, 0.9, stroke=26))
    for k in range(21):
        ang = math.radians(180 + k * 9)
        r1, r2 = R - 70, R - (88 if k % 5 == 0 else 80)
        c.drawLine(cx + r1 * math.cos(ang), cy + r1 * math.sin(ang), cx + r2 * math.cos(ang), cy + r2 * math.sin(ang), paint("#ffffff", 0.8, stroke=3 if k % 5 == 0 else 2))
    c.drawString("VOLTS", cx - skia.Font(TF_MONO, 34).measureText("VOLTS") / 2, cy + 120, skia.Font(TF_MONO, 34), paint("#ffffff", 0.7))
    lvl = eout(prog(t, THOUS - 0.1, 0.8))
    jit = 2.5 * math.sin(t * 40) * prog(t, WAIT, 0.3)
    ang = math.radians(180 + lerp(5, 162, lvl) + jit)
    c.drawLine(cx, cy, cx + (R - 90) * math.cos(ang), cy + (R - 90) * math.sin(ang), paint("#ffffff", 1, stroke=10))
    c.drawCircle(cx, cy, 26, paint(shader=radial(cx - 6, cy - 6, 30, [col("#ffffff"), col("#8b929c")])))
    c.restore()
    # crackle around the rim while waiting
    wa = prog(t, WAIT, 0.3)
    if wa > 0:
        for k in range(3):
            if int(t * 10 + k * 3) % 3 == 0:
                a0 = math.radians(200 + (k * 53 + int(t * 7) * 31) % 140)
                bolt(c, cx + (R + 30) * math.cos(a0), cy + (R + 30) * math.sin(a0), cx + (R + 110) * math.cos(a0 + 0.15), cy + (R + 110) * math.sin(a0 + 0.15), t, 0.7 * wa, width=3, seed=k)
    pill(c, t, "THOUSANDS OF VOLTS", 490, 1400, CHG, THOUS + 0.15, METALT - 0.15)


# ---------------- fingertip macro ----------------
def scene_finger(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (W, 0), [col("#151a26"), col("#0c0f16")])))
    # chrome surface on the right
    c.drawRect(skia.Rect.MakeLTRB(700, 0, W, H), paint(shader=linear((700, 0), (W, 0), [col("#f4f6f9"), col("#9aa2ad"), col("#5d646e"), col("#c8ced6")], [0, 0.3, 0.7, 1])))
    for k in range(5):
        c.drawLine(700, 300 + k * 260 + 20 * math.sin(t), W, 340 + k * 260, paint("#ffffff", 0.18, stroke=20, blur=10))
    c.drawLine(700, 0, 700, H, paint("#ffffff", 0.9, stroke=4))
    app = eio(prog(t, METALT - 0.1, SPARK - METALT - 0.05))
    rec = eout(prog(t, SPARK + 0.25, 0.4))
    tipx = lerp(330, 660, app) - 140 * rec
    tipy = 1000
    hand(c, tipx, tipy, 0, 1.2, curl=0.4 * rec)
    # charges crowding at the fingertip
    if t < SPARK + 0.02:
        crowd = prog(t, METALT, SPARK - METALT)
        for k in range(14):
            u = ((t * 0.6 + k / 14) % 1)
            sx = lerp(tipx - 520, tipx - 30, lerp(u, 1, crowd * 0.8))
            sy = tipy + 50 * math.sin(k * 2.1 + t * 3) * (1 - crowd * 0.8)
            minus(c, sx, sy, 0.75, prog(t, METALT, 0.3))
    fl = window(t, SPARK - 0.02, SPARK + 0.5, 0.03, 0.35)
    if fl > 0:
        bolt(c, tipx + 4, tipy, 700, tipy - 10, t, fl, width=10)
        bolt(c, tipx + 4, tipy, 700, tipy + 40, t, 0.6 * fl, width=5, seed=5)
        c.drawCircle(700, tipy, 180, paint(shader=radial(700, tipy, 180, [col("#ffffff", 0.9 * fl), col(ZAPC, 0)])))
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#e8f6ff", 0.45 * fl * (1 - prog(t, SPARK, 0.2))))
    pill(c, t, "METAL", 790, 760, METAL, METALT + 0.15, SPARK - 0.1, anchor=(700, 860))
    pill(c, t, "ONE SPARK", 490, 1300, ZAPC, SPARK + 0.1, WIPE1 + 0.1)


# ---------------- white: trolley, dry air, the trick ----------------
def trolley(c, x, y, s, t, a=1.0, trap=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-330, 300, 300, 340), paint("#000000", 0.15 * a, blur=10))
    bk = skia.Path(); bk.moveTo(-300, -200); bk.lineTo(280, -200); bk.lineTo(200, 120); bk.lineTo(-240, 120); bk.close()
    c.drawPath(bk, paint("#dfe4ea", 0.35 * a))
    c.save(); c.clipPath(bk, doAntiAlias=True)
    for k in range(16):
        xx = -300 + k * 38
        c.drawLine(xx, -200, xx + 10, 120, paint("#8a929c", a, stroke=3))
    for k in range(8):
        c.drawLine(-300, -200 + k * 42, 300, -200 + k * 42, paint("#8a929c", a, stroke=3))
    c.restore()
    c.drawPath(bk, paint("#6b737e", a, stroke=7))
    # frame + handle
    c.drawLine(-240, 120, -260, 260, paint("#7d858f", a, stroke=10))
    c.drawLine(200, 120, 220, 260, paint("#7d858f", a, stroke=10))
    c.drawLine(-280, 250, 240, 250, paint("#7d858f", a, stroke=12))
    c.drawLine(-300, -200, -380, -260, paint("#7d858f", a, stroke=10))
    c.drawRoundRect(skia.Rect.MakeLTRB(-420, -285, -340, -240), 20, 20, paint("#e5484d", a))
    # wheels (rubber)
    for wx in (-250, 210):
        if trap > 0:
            c.drawCircle(wx, 285, 62, paint(RED, 0.25 * trap * a, blur=6))
        c.drawCircle(wx, 285, 40, paint("#1c1c20", a))
        c.drawCircle(wx, 285, 16, paint("#9aa2ad", a))
        c.drawRect(skia.Rect.MakeLTRB(wx - 10, 250, wx + 10, 268), paint("#7d858f", a))
    c.restore()


def drop_icon(c, x, y, s, a, level):
    c.save(); c.translate(x, y); c.scale(s, s)
    dp = skia.Path(); dp.moveTo(0, -110); dp.cubicTo(60, -30, 90, 10, 90, 50); dp.cubicTo(90, 105, 45, 130, 0, 130)
    dp.cubicTo(-45, 130, -90, 105, -90, 50); dp.cubicTo(-90, 10, -60, -30, 0, -110); dp.close()
    c.drawPath(dp, paint("#d6eefc", a))
    c.save(); c.clipPath(dp, doAntiAlias=True)
    top = lerp(130, -110, level)
    c.drawRect(skia.Rect.MakeLTRB(-100, top, 100, 140), paint(shader=linear((0, -110), (0, 130), [col("#7fd3ff", a), col("#2fa6e0", a)])))
    c.restore()
    c.drawPath(dp, paint("#2fa6e0", a, stroke=5))
    c.restore()


def snowflake(c, x, y, r, rot, a, colr="#8fc8f0"):
    c.save(); c.translate(x, y); c.rotate(rot)
    for k in range(6):
        c.save(); c.rotate(k * 60)
        c.drawLine(0, 0, 0, -r, paint(colr, a, stroke=max(2, r * 0.09)))
        for u in (0.45, 0.7):
            c.drawLine(0, -r * u, r * 0.22, -r * u - r * 0.18, paint(colr, a, stroke=max(1.5, r * 0.06)))
            c.drawLine(0, -r * u, -r * 0.22, -r * u - r * 0.18, paint(colr, a, stroke=max(1.5, r * 0.06)))
        c.restore()
    c.restore()


def door_frame_hold(c, t, a, k_on):
    """white-studio close-up: hand gripping the metal door frame, charge flows away gently."""
    c.save()
    c.drawRoundRect(skia.Rect.MakeLTRB(120, 560, 860, 1340), 40, 40, paint("#000000", 0.12 * a, blur=20))
    c.drawRoundRect(skia.Rect.MakeLTRB(120, 540, 860, 1320), 40, 40, paint(shader=linear((0, 540), (0, 1320), [col("#ff6b7a", a), col(CAR, a), col("#8c1424", a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(200, 600, 780, 1260), 30, 30, paint(shader=linear((0, 600), (0, 1260), [col("#2a2f3a", a), col("#15181f", a)])))
    # metal frame bar (B-pillar)
    c.drawRoundRect(skia.Rect.MakeLTRB(430, 560, 520, 1300), 20, 20, paint(shader=linear((430, 0), (520, 0), [col("#f4f6f9", a), col("#9aa2ad", a), col("#5d646e", a)])))
    c.restore()


def gripping_hand(c, x, y, a):
    sk = linear((0, y - 80), (0, y + 80), [col("#F3C6A2", a), col(SKIN, a), col("#B97F59", a)], [0, 0.5, 1])
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 520, y - 90, x - 90, y + 90), 60, 60, paint(shader=linear((0, y - 90), (0, y + 90), [col("#4a5a7c", a), col(COAT, a), col("#1b2438", a)], [0, 0.5, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 130, y - 75, x + 20, y + 75), 50, 50, paint(shader=sk))
    for k in range(4):
        yy = y - 66 + k * 38
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 10, yy, x + 110, yy + 34), 17, 17, paint(shader=sk))
        c.drawLine(x + 70, yy + 6, x + 70, yy + 28, paint("#9b6646", 0.35 * a, stroke=2))


def key_hand(c, x, y, a, t):
    """hand holding a key, key tip at (x, y) pointing right."""
    c.save(); c.translate(x, y)
    # key
    c.drawCircle(-230, 0, 52, paint(shader=radial(-240, -12, 60, [col("#ffe39a", a), col("#d4a32a", a), col("#8a6a1a", a)], [0, 0.6, 1])))
    c.drawCircle(-238, 0, 16, paint("#F4F2EE", a))
    kp = skia.Path(); kp.moveTo(-185, -14); kp.lineTo(0, -14); kp.lineTo(0, 6); kp.lineTo(-30, 6); kp.lineTo(-38, 18); kp.lineTo(-56, 6)
    kp.lineTo(-74, 20); kp.lineTo(-92, 6); kp.lineTo(-185, 14); kp.close()
    c.drawPath(kp, paint(shader=linear((0, -14), (0, 20), [col("#ffe7a8", a), col("#c9971f", a)])))
    c.restore()
    # fingers pinching the key bow
    sk = linear((0, y - 70), (0, y + 70), [col("#F3C6A2", a), col(SKIN, a), col("#B97F59", a)], [0, 0.5, 1])
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 760, y - 90, x - 330, y + 90), 60, 60, paint(shader=linear((0, y - 90), (0, y + 90), [col("#4a5a7c", a), col(COAT, a), col("#1b2438", a)], [0, 0.5, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 360, y - 72, x - 230, y + 72), 50, 50, paint(shader=sk))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 280, y - 56, x - 190, y - 20), 18, 18, paint(shader=sk))    # thumb over bow
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 280, y + 20, x - 200, y + 56), 18, 18, paint(shader=sk))


def scene_white(c, t):
    studio_white(c)
    # trolley
    ta = window(t, WIPE1 + 0.1, WORSE - 0.05, 0.3, 0.25)
    if ta > 0:
        tr = eout(prog(t, TRAP - 0.1, 0.3))
        trolley(c, 520, 980, 1.05 * (0.9 + 0.1 * eback(prog(t, WIPE1 + 0.1, 0.4))), t, ta, tr)
        # charges moving on the metal frame; on "trap" they bounce back from the wheels
        for k in range(12):
            u = ((t * 0.5 + k / 12) % 1)
            if tr > 0.5:
                yb = 1240 - abs(math.sin((t * 1.6 + k * 0.4) * math.pi)) * 420
                xb = 260 + (k * 53) % 520
                minus(c, xb, min(yb, 1240), 0.75, ta)
            else:
                xb = lerp(220, 800, u); yb = 900 + 60 * math.sin(k + t * 2)
                minus(c, xb, yb, 0.75, ta * prog(t, TROL - 0.1, 0.3))
        if tr > 0:
            for wx in (520 - 250 * 1.05, 520 + 210 * 1.05):
                c.drawLine(wx - 40, 1280 + 20, wx + 40, 1280 + 20, paint(RED, tr * ta, stroke=8))
        pill(c, t, "TROLLEYS TOO", 490, 640, "#141313", TROL, TRAP - 0.1, text_col="#FFFFFF")
        pill(c, t, "RUBBER WHEELS", 490, 640, RED, TRAP, WORSE - 0.15)
    # dry winter air
    da = window(t, WORSE - 0.15, TRICK - 0.02, 0.3, 0.2)
    if da > 0:
        for (x, y0, r, ph) in SNOW:
            yy = (y0 * 1300 + t * 120) % 1300 + 420
            snowflake(c, x, yy, r * 2.2, t * 40 + ph * 57, 0.6 * da)
        snowflake(c, 330, 980, 170 * eback(prog(t, WORSE - 0.1, 0.4)), t * 25, da, "#5fa8e0")
        lvl = lerp(0.8, 0.15, eio(prog(t, WORSE + 0.1, 1.2)))
        drop_icon(c, 700, 1000, 1.5, da, lvl)
        pill(c, t, "DRY AIR = WORSE", 490, 1360, BLUE, WORSE + 0.15, TRICK - 0.05)
    # the trick: hold the metal
    ha = window(t, TRICK - 0.05, KEY - 0.05, 0.3, 0.25)
    if ha > 0:
        door_frame_hold(c, t, ha, 0)
        gx = lerp(300, 440, eout(prog(t, TRICK, 0.5)))
        gripping_hand(c, gx, 930, ha)
        if t > HOLD - 0.1:
            fa = prog(t, HOLD - 0.1, 0.3) * ha
            for k in range(8):
                u = ((t * 0.7 + k / 8) % 1)
                minus(c, 475, lerp(960, 1300, u), 0.7, fa * (1 - u), GREEN)
            c.drawLine(475, 1300, 475, 1420, paint(GREEN, 0.6 * fa, stroke=4))
            for k in range(3):
                c.drawLine(475 - 50 + k * 15, 1420 + k * 14, 475 + 50 - k * 15, 1420 + k * 14, paint(GREEN, 0.6 * fa, stroke=4))
        pill(c, t, "HOLD THE METAL", 490, 640, GREEN, HOLD + 0.05, KEY - 0.1)
    # or use your key
    ka = window(t, KEY - 0.1, SO + 0.6, 0.3, 0.2)
    if ka > 0:
        c.drawRect(skia.Rect.MakeLTRB(700, 520, 940, 1400), paint(shader=linear((700, 0), (940, 0), [col("#f4f6f9", ka), col("#9aa2ad", ka), col("#6d747e", ka)])))
        c.drawLine(700, 520, 700, 1400, paint("#ffffff", ka, stroke=4))
        kx = lerp(560, 696, eio(prog(t, KEY - 0.05, 0.5)))
        key_hand(c, kx, 980, ka, t)
        sp = window(t, KEY + 0.45, KEY + 0.9, 0.03, 0.25)
        if sp > 0:
            bolt(c, kx, 976, 700, 970, t, sp, width=5)
            c.drawCircle(700, 975, 70, paint(shader=radial(700, 975, 70, [col("#ffffff", 0.9 * sp), col(ZAPC, 0)])))
        pill(c, t, "USE YOUR KEY", 490, 640, "#D4A32A", KEY + 0.05, SO + 0.4)
        if t > KEY + 0.8:
            ck = eback(prog(t, KEY + 0.8, 0.35)) * ka
            c.save(); c.translate(400, 1260); c.scale(ck, ck)
            c.drawCircle(0, 0, 54, paint(GREEN))
            cp = skia.Path(); cp.moveTo(-24, 2); cp.lineTo(-6, 20); cp.lineTo(26, -16)
            c.drawPath(cp, paint("#ffffff", 1, stroke=10))
            c.restore()


def draw_world(c, t):
    if t < BROKEN - 0.15:
        scene_door(c, t); return
    if t < SLIDE - 0.1:
        scene_car(c, t)
        q = 1 - prog(t, BROKEN - 0.15, 0.25)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_door(c, t); c.restore()
        return
    if t < THOUS - 0.25:
        scene_seat(c, t); return
    if t < METALT - 0.1:
        scene_gauge(c, t); return
    if t < WIPE1 + WL / 2:
        scene_finger(c, t); return
    if t < SO - 0.05:
        scene_white(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    hook_scene(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_white(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.025 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"car door": CAR, "ZAP": ZAPC, "broken": "#FFFFFF", "exactly": RED, "you": CHG, "rub": "#FFFFFF",
         "charge": CHG, "Thousands": CHG, "metal": "#8a929c", "spark": ZAPC, "Trolleys": "#FFFFFF", "trap": RED,
         "worse": BLUE, "key": "#D4A32A"}
CAPS = Captions(P, KWCOL, {"Not", "ZAP!"}, DUR)


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
    light = WIPE1 + WL / 2 <= t < SO - 0.05 + (DUR - SO) * 0.5
    vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 700), paint(shader=linear((0, 0), (0, 700), [col("#000000", 0.45), col("#000000", 0)])))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, ZAPC, "#F4F2EE")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.3), ("hit", ZAP), ("riser", ZAP - 0.4), ("whoosh", BROKEN - 0.15), ("pop", BROKEN + 0.1),
          ("hit", NOTEX), ("pop", YOU), ("whoosh", SLIDE), ("pop", RUB), ("pop", CHARGE), ("whoosh", THOUS - 0.25),
          ("riser", THOUS - 0.1), ("pop", THOUS + 0.15), ("whoosh", METALT - 0.1), ("riser", SPARK - 0.8),
          ("hit", SPARK), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", TROL), ("pop", TRAP), ("pop", WORSE + 0.15),
          ("pop", TRICK), ("pop", HOLD), ("pop", KEY), ("ding", KEY + 0.8), ("whoosh", SO - 0.05)]
    for k in range(5):
        ev.append(("tick", WAIT + k * 0.18))
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

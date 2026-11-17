# HIW07 — why you jerk awake as you fall asleep (hypnic jerk). Basic + useful, detailed objects, "So," loop.
# Sources: Cleveland Clinic (≈70% experience sleep starts; happen in sleep transitions; normal), Live Science / Cleveland
#  Clinic Sleep Disorders Center (evening exercise), Medical News Today (harmless, not a sign of illness),
#  common explanation: brain misreads muscle relaxation as falling; triggers: caffeine, stress, sleep deprivation.
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
NIGHT = "#7FA8FF"; MOON = "#FFE7A3"; ALERT = "#FF5A5F"; CALM = "#6FD3FF"; SKIN = "#E6B08A"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


JUMP = kw(1); FALL = kw(2); NAME = kw(3); SEVEN = kw(4); DRIFT = p0(5); RELAX = kw(6); SLOWS = kw(7)
MISREAD = kw(8); ASFALL = p0(9); PANIC = kw(10); GRAB = kw(11)
WIPE1 = p0(12) - 0.3; BAD = p0(12); NOTALL = kw(13); NORMAL = kw(14)
CAFF = kw(15); STRESS = kw(16); TIRED = kw(17); MORE = p0(18); SO = p0(19)
WL = 0.32
IMPACTS = [JUMP, GRAB]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]
rnd = random.Random(8)
STARS = [(rnd.uniform(0, 1), rnd.uniform(0, 1), rnd.uniform(1, 3), rnd.random() * 6.28) for _ in range(60)]


# ---------------- bedroom (detailed) ----------------
def bedroom(c, t, jump=0.0, shake=0.0):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#141b33"), col("#1d2747"), col("#0d1224")], [0, 0.55, 1])))
    # window with moon + stars
    win = skia.Rect.MakeLTRB(560, 330, 960, 780)
    c.drawRect(win.makeOutset(18, 18), paint(shader=linear((560, 330), (960, 780), [col("#3a4670"), col("#252d4d")])))
    c.drawRect(win, paint(shader=linear((0, 330), (0, 780), [col("#0e1a3a"), col("#27407a")])))
    c.save(); c.clipRect(win)
    for (u, v, r, ph) in STARS:
        c.drawCircle(560 + u * 400, 330 + v * 450, r, paint("#ffffff", 0.4 + 0.4 * math.sin(t * 2 + ph)))
    c.drawCircle(820, 450, 120, paint(shader=radial(820, 450, 120, [col(MOON, 0.35), col(MOON, 0)])))
    c.drawCircle(820, 450, 56, paint(shader=radial(800, 432, 70, [col("#FFF6D8"), col(MOON), col("#E8C877")], [0, 0.6, 1])))
    for (dx, dy, r) in ((-14, -10, 9), (12, 14, 7), (18, -16, 5)):
        c.drawCircle(820 + dx, 450 + dy, r, paint("#d9b867", 0.45))
    c.restore()
    c.drawLine(760, 330, 760, 780, paint("#3a4670", 1, stroke=10)); c.drawLine(560, 555, 960, 555, paint("#3a4670", 1, stroke=10))
    # curtains with folds
    for sx, x0 in ((-1, 520), (1, 1000)):
        cp = skia.Path(); cp.moveTo(x0, 300)
        cp.lineTo(x0 - sx * 110, 300); cp.cubicTo(x0 - sx * 90, 600, x0 - sx * 140, 800, x0 - sx * 70, 860); cp.lineTo(x0 + sx * 40, 860); cp.close()
        c.drawPath(cp, paint(shader=linear((x0 - sx * 110, 0), (x0 + sx * 40, 0), [col("#3c2f63"), col("#5a4a8e"), col("#2b2148")])))
        for k in range(4):
            fx = x0 - sx * (20 + k * 25)
            c.drawLine(fx, 310, fx - sx * 10, 850, paint("#000000", 0.18, stroke=6, blur=4))
    # moonlight on wall
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(760, 700, 700, [col(NIGHT, 0.10), col(NIGHT, 0)])))
    c.save(); c.translate(shake * math.sin(t * 90), shake * math.cos(t * 77))
    # headboard
    c.drawRoundRect(skia.Rect.MakeLTRB(60, 860, 700, 1180), 40, 40, paint(shader=linear((0, 860), (0, 1180), [col("#6b4a35"), col("#4a301f")])))
    for k in range(5):
        c.drawLine(120 + k * 120, 900, 120 + k * 120, 1160, paint("#2e1c11", 0.35, stroke=4))
    c.drawRoundRect(skia.Rect.MakeLTRB(60, 860, 700, 1180), 40, 40, paint("#ffffff", 0.08, stroke=3))
    # mattress
    c.drawRoundRect(skia.Rect.MakeLTRB(40, 1120, 1120, 1300), 30, 30, paint(shader=linear((0, 1120), (0, 1300), [col("#e8ecf6"), col("#a9b2c8")])))
    # pillow
    c.drawRoundRect(skia.Rect.MakeLTRB(110, 1040, 460, 1170), 60, 60, paint("#000000", 0.25, blur=12))
    c.drawRoundRect(skia.Rect.MakeLTRB(100, 1020, 450, 1150), 60, 60, paint(shader=radial(220, 1050, 260, [col("#ffffff"), col("#dfe5f2"), col("#b7c1d8")], [0, 0.6, 1])))
    # sleeper head (lifts on jump)
    hy = -110 * jump
    c.save(); c.translate(0, hy)
    c.drawCircle(300, 1040, 78, paint(shader=radial(280, 1010, 110, [col("#F6C9A8"), col(SKIN), col("#B57D58")], [0, 0.55, 1])))
    hair = skia.Path(); hair.moveTo(222, 1040); hair.cubicTo(215, 950, 330, 930, 375, 1000); hair.cubicTo(340, 985, 290, 990, 262, 1020); hair.close()
    c.drawPath(hair, paint(shader=linear((222, 940), (375, 1040), [col("#5a3a26"), col("#2e1c11")])))
    if jump > 0.3:
        c.drawCircle(330, 1040, 10, paint("#ffffff")); c.drawCircle(333, 1040, 5, paint("#1b1b1b"))
    else:
        c.drawArc(skia.Rect.MakeLTRB(316, 1032, 346, 1050), 10, 160, False, paint("#6b4330", 1, stroke=4))
    c.drawOval(skia.Rect.MakeLTRB(262, 1030, 286, 1062), paint("#C98E68"))
    c.restore()
    # duvet with folds (jumps too)
    dy = -70 * jump
    du = skia.Path(); du.moveTo(330, 1090 + dy); du.cubicTo(500, 1040 + dy, 800, 1060 + dy, 1100, 1080 + dy)
    du.lineTo(1120, 1330); du.lineTo(300, 1330); du.close()
    c.drawPath(du, paint("#000000", 0.3, blur=14))
    c.drawPath(du, paint(shader=linear((300, 1050), (1120, 1330), [col("#5f86ff"), col("#3b5bdb"), col("#26388f")], [0, 0.5, 1])))
    for k in range(5):
        fp = skia.Path(); x = 420 + k * 150
        fp.moveTo(x, 1080 + dy); fp.cubicTo(x + 40, 1160 + dy * 0.5, x - 20, 1240, x + 30, 1320)
        c.drawPath(fp, paint("#1c2b70", 0.35, stroke=12, blur=6))
        c.drawPath(fp, paint("#9fb6ff", 0.25, stroke=3, blur=1))
    c.drawPath(du, paint("#ffffff", 0.08, stroke=3))
    c.restore()
    # bedside table + glowing clock
    c.drawRoundRect(skia.Rect.MakeLTRB(860, 1050, 1060, 1330), 14, 14, paint(shader=linear((0, 1050), (0, 1330), [col("#7a563d"), col("#4a301f")])))
    c.drawRoundRect(skia.Rect.MakeLTRB(880, 1150, 1040, 1180), 6, 6, paint("#2e1c11", 0.6))
    c.drawRoundRect(skia.Rect.MakeLTRB(880, 975, 1040, 1050), 16, 16, paint(shader=linear((0, 975), (0, 1050), [col("#2b2f3a"), col("#14161c")])))
    f = skia.Font(TF_BLACK, 46); s = "00:14"
    c.drawString(s, 960 - f.measureText(s) / 2, 1030, f, paint(ALERT, 0.35, blur=6))
    c.drawString(s, 960 - f.measureText(s) / 2, 1030, f, paint("#FF7A7F"))
    # zzz
    if jump < 0.2:
        fz = skia.Font(TF_BLACK, 40)
        for k in range(3):
            u = (t * 0.5 + k / 3) % 1
            c.drawString("z", 360 + 50 * u + k * 10, 950 - 120 * u, fz, paint("#ffffff", 0.7 * (1 - u)))


def motion_lines(c, x, y, a):
    for k in range(6):
        an = -math.pi / 2 + (k - 2.5) * 0.35
        c.drawLine(x + math.cos(an) * 110, y + math.sin(an) * 110, x + math.cos(an) * 170, y + math.sin(an) * 170, paint("#ffffff", a, stroke=7))


CLOUDS = [(rnd.uniform(-200, 1280), rnd.uniform(0, 1), rnd.uniform(90, 180)) for _ in range(12)]


def falling_dream(c, t, a):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#2a2366", a), col("#5a3f9e", a), col("#1b1640", a)])))
    for (x, ph, r) in CLOUDS:
        y = ((ph - t * 0.55) % 1) * (H + 400) - 200
        for k in range(3):
            c.drawCircle(x + k * r * 0.6, y + (k % 2) * 20, r * (0.8 + 0.2 * k), paint("#ffffff", 0.10 * a, blur=10))
    for k in range(14):
        y = ((k / 14 - t * 1.4) % 1) * H
        c.drawLine(140 + k * 60, y, 140 + k * 60, y + 160, paint("#ffffff", 0.18 * a, stroke=3))
    # falling sleeper silhouette (pyjamas, detailed-ish)
    c.save(); c.translate(500, 1000 + 20 * math.sin(t * 3)); c.rotate(18 * math.sin(t * 1.6))
    body = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-70, -60, 70, 140), 50, 50)
    c.drawRRect(body, paint(shader=linear((-70, 0), (70, 0), [col("#7ea2ff", a), col("#3b5bdb", a)])))
    for k in range(4):
        c.drawLine(-60, -30 + k * 40, 60, -30 + k * 40, paint("#ffffff", 0.25 * a, stroke=6))
    for sx in (-1, 1):
        c.drawRoundRect(skia.Rect.MakeLTRB(sx * 70 - (40 if sx < 0 else 0), -40, sx * 70 + (0 if sx < 0 else 40), -10), 15, 15, paint("#5f86ff", a))
        c.drawLine(sx * 90, -30, sx * 150, -110, paint("#5f86ff", a, stroke=34))
        c.drawCircle(sx * 152, -114, 22, paint(SKIN, a))
        c.drawLine(sx * 30, 130, sx * 50, 230, paint("#3b5bdb", a, stroke=40))
    c.drawCircle(0, -120, 64, paint(shader=radial(-15, -140, 90, [col("#F6C9A8", a), col(SKIN, a), col("#B57D58", a)], [0, 0.55, 1])))
    c.drawCircle(-20, -125, 9, paint("#1b1b1b", a)); c.drawCircle(20, -125, 9, paint("#1b1b1b", a))
    c.drawOval(skia.Rect.MakeLTRB(-14, -92, 14, -70), paint("#7a3b3b", a))
    c.restore()


def heads_grid(c, t, a):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#141b33", a), col("#0d1224", a)])))
    for i in range(10):
        x = 150 + (i % 5) * 190; y = 820 + (i // 5) * 330
        jumpers = (0, 1, 3, 4, 5, 7, 8)
        q = eback(prog(t, SEVEN - 0.3 + i * 0.04, 0.3))
        if q <= 0: continue
        j = 0
        if i in jumpers:
            d = (t - (SEVEN + 0.3 + 0.08 * jumpers.index(i)))
            j = max(0, math.sin(min(max(d, 0), 0.4) / 0.4 * math.pi)) if d > 0 else 0
        c.save(); c.translate(x, y - 50 * j); c.scale(q, q)
        c.drawRoundRect(skia.Rect.MakeLTRB(-80, 40, 80, 110), 30, 30, paint(shader=radial(-30, 50, 120, [col("#ffffff", a), col("#c9d2e6", a)])))
        c.drawCircle(0, 20, 48, paint(shader=radial(-12, 0, 70, [col("#F6C9A8", a), col(SKIN, a), col("#B57D58", a)], [0, 0.55, 1])))
        c.drawRoundRect(skia.Rect.MakeLTRB(-90, 70, 90, 150), 34, 34, paint(shader=linear((0, 70), (0, 150), [col("#5f86ff" if i in jumpers else "#5a6280", a), col("#26388f" if i in jumpers else "#343a52", a)])))
        if i in jumpers and t > SEVEN + 0.3:
            c.drawString("!", 50, -20, skia.Font(TF_BLACK, 52), paint(ALERT, a))
        c.restore()
    big_number(c, "7 IN 10", "", 500, 700, 120, "#FFFFFF", eout(prog(t, SEVEN - 0.1, 0.3)) * a)


def body_scene(c, t):
    relax = eout(prog(t, RELAX - 0.2, 0.8))
    panic = eout(prog(t, PANIC - 0.1, 0.3))
    d = t - (GRAB - 0.05)
    grab = math.sin(min(max(d, 0), 0.45) / 0.45 * math.pi) if 0 < d < 0.45 else 0
    bedroom(c, t, grab, 6 * grab)
    # soft relaxing glow over the sleeper, turning to alarm on panic
    gcol = mixhex(CALM, ALERT, panic)
    for k in range(3):
        u = ((t * 0.5 + k / 3) % 1)
        c.drawOval(skia.Rect.MakeLTRB(220 - 60 * u, 980 - 40 * u, 1120 + 40 * u, 1330 + 30 * u), paint(gcol, 0.22 * max(relax, panic) * (1 - u), stroke=5))
    c.drawOval(skia.Rect.MakeLTRB(240, 1000, 1110, 1320), paint(gcol, 0.10 * max(relax, panic), blur=30))
    if grab > 0.1:
        motion_lines(c, 330, 940 - 110 * grab, grab)
    # breathing wave slowing
    ba = window(t, SLOWS - 0.3, PANIC, 0.3, 0.3)
    if ba > 0:
        freq = lerp(0.05, 0.022, eio(prog(t, SLOWS, 1.0)))
        p = skia.Path(); p.moveTo(120, 1430)
        for x in range(120, 900, 6):
            p.lineTo(x, 1430 - 60 * math.sin((x - t * 220) * freq))
        c.drawPath(p, paint(CALM, 0.35 * ba, stroke=14, blur=8)); c.drawPath(p, paint(CALM, ba, stroke=5))
    # brain misread alert
    ma = window(t, MISREAD - 0.2, WIPE1, 0.3, 0.3)
    if ma > 0:
        bx, by = 800, 760
        c.drawCircle(bx, by, 140, paint(ALERT, 0.25 * ma * (0.6 + 0.4 * math.sin(t * 10)) * panic + 0.0, blur=20))
        brain(c, bx, by, 1.0, ma, panic)
        if t > ASFALL:
            fa = eback(prog(t, ASFALL, 0.3))
            c.save(); c.translate(bx, by - 190); c.scale(fa, fa)
            c.drawRoundRect(skia.Rect.MakeLTRB(-130, -44, 130, 44), 44, 44, paint(ALERT))
            f = skia.Font(TF_BLACK, 40); s = "FALLING?!"
            c.drawString(s, -f.measureText(s) / 2, 14, f, paint("#ffffff"))
            c.restore()


def brain(c, x, y, s, a, panic):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.addOval(skia.Rect.MakeLTRB(-120, -90, 120, 90))
    c.drawPath(p, paint(shader=radial(-40, -40, 170, [col("#FFE1E8", a), col("#F2A4B8", a), col("#C96A86", a)], [0, 0.5, 1])))
    for k in range(5):
        q = skia.Path(); q.moveTo(-100, -60 + k * 30)
        for xx in range(-100, 101, 20):
            q.lineTo(xx, -60 + k * 30 + 10 * math.sin(xx / 14 + k))
        c.drawPath(q, paint("#a8506b", 0.55 * a, stroke=5))
    c.drawLine(0, -88, 0, 88, paint("#a8506b", 0.6 * a, stroke=5))
    if panic > 0:
        c.drawPath(p, paint(ALERT, 0.35 * panic * a))
    c.restore()


def coffee(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-110, 100, 110, 130), paint("#000000", 0.25 * a, blur=10))
    c.drawOval(skia.Rect.MakeLTRB(-130, 92, 130, 128), paint(shader=linear((0, 92), (0, 128), [col("#ffffff", a), col("#cfd4dd", a)])))
    cup = skia.Path(); cup.moveTo(-90, -70); cup.lineTo(90, -70); cup.cubicTo(88, 60, 60, 105, 0, 105); cup.cubicTo(-60, 105, -88, 60, -90, -70); cup.close()
    c.drawPath(cup, paint(shader=linear((-90, 0), (90, 0), [col("#ffffff", a), col("#e9ecf1", a), col("#b9c0cc", a)])))
    c.drawArc(skia.Rect.MakeLTRB(70, -40, 150, 50), -90, 180, False, paint("#cfd4dd", a, stroke=16))
    c.drawOval(skia.Rect.MakeLTRB(-88, -84, 88, -56), paint(shader=radial(-20, -74, 90, [col("#9a5a2e", a), col("#4a2610", a)])))
    c.drawOval(skia.Rect.MakeLTRB(-40, -78, 10, -66), paint("#d9a07a", 0.6 * a))
    for k in range(3):
        sp = skia.Path(); sx = -40 + k * 40
        sp.moveTo(sx, -100)
        for j in range(8):
            sp.lineTo(sx + 14 * math.sin(j * 0.9 + c_t * 3 + k), -100 - j * 22)
        c.drawPath(sp, paint("#ffffff", 0.35 * a, stroke=8, blur=4))
    c.restore()


c_t = 0.0


def phone_late(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-85, -170, 85, 170), 28, 28, paint("#000000", 0.35 * a, blur=10))
    c.drawRoundRect(skia.Rect.MakeLTRB(-80, -165, 80, 165), 26, 26, paint("#1c1d22", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -152, 70, 152), 18, 18, paint(shader=linear((0, -152), (0, 152), [col("#2a2f55", a), col("#141833", a)])))
    f = skia.Font(TF_BLACK, 52); s_ = "02:47"
    c.drawString(s_, -f.measureText(s_) / 2, -60, f, paint("#ffffff", a))
    for k in range(3):
        c.drawRoundRect(skia.Rect.MakeLTRB(-58, -20 + k * 54, 58, 22 + k * 54), 12, 12, paint("#ffffff", 0.18 * a))
        c.drawCircle(-38, 1 + k * 54, 10, paint(["#FF5A5F", "#3EE6A8", "#FFD23F"][k], a))
    c.restore()


def battery_low(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-110, -55, 100, 55), 18, 18, paint("#000000", 0.25 * a, blur=10))
    c.drawRoundRect(skia.Rect.MakeLTRB(-110, -55, 100, 55), 18, 18, paint(shader=linear((0, -55), (0, 55), [col("#ffffff", a), col("#d6dbe4", a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(100, -22, 122, 22), 6, 6, paint("#bfc6d2", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-96, -40, -50, 40), 10, 10, paint(shader=linear((0, -40), (0, 40), [col("#FF8A8E", a), col(ALERT, a)])))
    c.restore()


def scene_white(c, t):
    global c_t
    c_t = t
    studio_white(c)
    sa = window(t, BAD - 0.2, CAFF - 0.15, 0.3, 0.25)
    if sa > 0:
        q = eback(prog(t, NOTALL - 0.1, 0.35))
        c.save(); c.translate(500, 1000); c.scale(q, q)
        sh = skia.Path(); sh.moveTo(0, -200); sh.cubicTo(110, -170, 170, -170, 170, -170); sh.lineTo(170, 10)
        sh.cubicTo(170, 130, 60, 200, 0, 230); sh.cubicTo(-60, 200, -170, 130, -170, 10); sh.lineTo(-170, -170); sh.cubicTo(-170, -170, -110, -170, 0, -200); sh.close()
        c.drawPath(sh, paint("#000000", 0.2, blur=16))
        c.drawPath(sh, paint(shader=linear((-170, -200), (170, 230), [col("#7CF2C2"), col("#1fb98a"), col("#0f7a5a")], [0, 0.5, 1])))
        ck = skia.Path(); ck.moveTo(-70, 10); ck.lineTo(-15, 70); ck.lineTo(85, -50)
        c.drawPath(ck, paint("#ffffff", 1, stroke=30))
        c.drawPath(sh, paint("#ffffff", 0.3, stroke=4))
        c.restore()
    if t > CAFF - 0.2:
        coffee(c, 220, 1030, 0.95 * eback(prog(t, CAFF - 0.15, 0.3)), 1)
        if t > STRESS - 0.15:
            phone_late(c, 500, 1010, 0.95 * eback(prog(t, STRESS - 0.1, 0.3)), 1)
        if t > TIRED - 0.15:
            battery_low(c, 790, 1020, 0.95 * eback(prog(t, TIRED - 0.1, 0.3)), 1)
        if t > MORE - 0.1:
            for k, x in enumerate((220, 500, 790)):
                ua = eback(prog(t, MORE + k * 0.1, 0.3))
                if ua > 0:
                    c.save(); c.translate(x, 790); c.scale(ua, ua)
                    c.drawCircle(0, 0, 36, paint(ALERT)); ar = skia.Path(); ar.moveTo(0, -20); ar.lineTo(18, 6); ar.lineTo(-18, 6); ar.close()
                    c.drawPath(ar, paint("#ffffff")); c.drawRect(skia.Rect.MakeLTRB(-6, 4, 6, 20), paint("#ffffff"))
                    c.restore()
    pill(c, t, "TOTALLY NORMAL", 500, 1360, "#1fb98a", NORMAL, CAFF - 0.15, light=True)
    pill(c, t, "MAKES IT MORE LIKELY", 500, 1360, ALERT, MORE, SO, light=True)


def draw_world(c, t):
    if t < FALL - 0.3:
        j = 0
        if t > JUMP - 0.1:
            d = t - (JUMP - 0.1)
            j = math.sin(min(d, 0.45) / 0.45 * math.pi) if d < 0.45 else 0
        bedroom(c, t, j, 6 * j)
        if j > 0.2:
            motion_lines(c, 330, 940 - 110 * j, j)
        pill(c, t, "JOLT!", 500, 1400, ALERT, JUMP, FALL - 0.3)
        return
    if t < NAME - 0.2:
        falling_dream(c, t, eout(prog(t, FALL - 0.3, 0.35)))
        return
    if t < SEVEN - 0.3:
        bedroom(c, t, 0, 0)
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 0.25))
        q = eback(prog(t, NAME - 0.1, 0.35))
        c.save(); c.translate(500, 1460); c.scale(q, q)
        c.drawRoundRect(skia.Rect.MakeLTRB(-260, -56, 260, 56), 56, 56, paint(shader=linear((-260, 0), (260, 0), [col("#9B6BFF"), col("#5f86ff")])))
        f = skia.Font(TF_BLACK, 48); s = "HYPNIC JERK"
        c.drawString(s, -f.measureText(s) / 2, 17, f, paint("#ffffff"))
        c.restore()
        return
    if t < DRIFT - 0.15:
        heads_grid(c, t, 1); return
    if t < WIPE1 + WL / 2:
        body_scene(c, t)
        pill(c, t, "RELAXING", 300, 1360, CALM, RELAX, MISREAD - 0.2, text_col=INK)
        pill(c, t, "GRAB ON!", 500, 1360, YELLOW, GRAB, WIPE1 + 0.1)
        return
    if t < SO - 0.05:
        scene_white(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    bedroom(c, t, 0, 0)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_white(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.025 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"falling": NIGHT, "jumps": ALERT, "hypnic": "#9B6BFF", "seven": "#FFFFFF", "relax": CALM, "slows": CALM,
         "misread": ALERT, "panics": ALERT, "grab": YELLOW, "at all": "#1fb98a", "normal": "#1fb98a",
         "caffeine": "#C9895A", "stress": ALERT, "overtired": ALERT}
CAPS = Captions(P, KWCOL, {"jumps.", "seven"}, DUR)


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    sx = sy = 0
    for ti in IMPACTS:
        d = t - ti
        if 0 <= d < 0.3:
            amp = 8 * (1 - d / 0.3); sx += amp * math.sin(d * 97); sy += amp * math.cos(d * 83)
    ps = cut_punch(t)
    c.save(); c.translate(sx, sy); c.translate(540, 960); c.scale(ps, ps); c.translate(-540, -960)
    draw_world(c, t)
    c.restore()
    light = WIPE1 + WL / 2 <= t < SO - 0.05 + (DUR - SO) * 0.5
    vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 700), paint(shader=linear((0, 0), (0, 700), [col("#000000", 0.45), col("#000000", 0)])))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, "#1fb98a", "#F4F2EE")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("hit", JUMP), ("whoosh", FALL - 0.3), ("riser", FALL - 0.2), ("pop", NAME), ("whoosh", SEVEN - 0.3),
          ("ding", SEVEN + 0.3), ("whoosh", DRIFT - 0.15), ("pop", RELAX), ("pop", MISREAD), ("pop", ASFALL),
          ("hit", GRAB), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("ding", NOTALL), ("pop", CAFF), ("pop", STRESS),
          ("pop", TIRED), ("pop", MORE), ("whoosh", SO - 0.05)]
    for k in range(7):
        ev.append(("tick", SEVEN + 0.3 + k * 0.08))
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

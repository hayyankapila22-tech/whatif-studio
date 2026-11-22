# HIW23 — "How does a mosquito find you?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-23):
#  - Houston Methodist, "Why are mosquitoes attracted to some people more than others?" (2022): they sense the carbon
#    dioxide you breathe out "upwards of 50 feet" (~15 m) away; skin odours incl. byproducts "created by the bacteria
#    naturally living on your skin" attract them, which is part of why some people get bitten more; body heat is the
#    final cue up close; females bite because "your blood contains nutrients they need to make eggs".
#  - HealthDay / Drugs.com, "Mosquitos have another way to find you: body heat" (2024, on a Nature paper): heat is an
#    effective cue up to about 2.5 feet (< 1 m); mosquito vision is poor; loose clothing helps by blocking bites and
#    interfering with heat detection.
#  - Arizona State Univ. Ask A Biologist "Mosquito magnet": female mosquitoes need blood to develop their eggs; cover
#    skin with loose, thick clothing.
#  Plain words: CO2 = "carbon dioxide", skin bacteria = "tiny germs on your skin".
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
SKIN = "#E9B08A"; SKIN_L = "#F7CFAE"; SKIN_D = "#C4835E"; CO2 = "#8FA8C8"; SMELL = "#6EDB8F"; HEAT = "#FF7A3D"
BLOOD = "#E23B4A"; NIGHT = "#5B6CFF"; MOSQ = "#3a3430"; CLOTH = "#4F7DD9"; GREEN = "#1fb98a"; LOVE = "#FF5C8A"


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


FIND = kw(ph("how does"))
WIPE1 = p0(ph("step one")) - 0.3; S1 = p0(ph("step one")); BREATH = kw(ph("your breath")); CO2t = kw(ph("you breathe"))
SENSE = p0(ph("and they can")); M15 = kw(ph("from about"))
S2 = p0(ph("step two")); SMELLt = kw(ph("your smell")); GERMS = p0(ph("tiny germs")); LOVEt = kw(ph("make a scent"))
MORE = p0(ph("that's why")); MORE2 = kw(ph("that's why"))
S3 = p0(ph("step three")); CLOSE = p0(ph("up close")); HEATt = kw(ph("they feel"))
WIPE2 = p0(ph("and only")) - 0.3; FEM = kw(ph("and only")); BLOODt = p0(ph("they need")); EGGS = kw(ph("to make"))
TRICK = p0(ph("the trick")); CLOTHt = kw(ph("loose")); BLOCK = p0(ph("block")); HIDE = p0(ph("and hide"))
SO = p0(len(P) - 1)
WL = 0.32
IMPACTS = [BREATH, M15, MORE2, FEM]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1, ph_=0.0):
    return math.sin(2 * math.pi * k * t / DUR + ph_)


def bg_night(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.45, 1300, [col("#141a33"), col("#0b0f1f"), col("#05060c")], [0, 0.55, 1])))
    c.drawCircle(780 + 20 * lw(t), 760, 520, paint(shader=radial(780, 760, 520, [col(NIGHT, 0.10), col(NIGHT, 0)])))
    for k in range(26):
        rr = random.Random(k)
        x, y = rr.uniform(40, 1040), rr.uniform(620, 1300)
        c.drawCircle(x, y, rr.uniform(1.5, 3), paint("#ffffff", 0.25 + 0.2 * math.sin(2 * math.pi * 3 * t / DUR + k)))


# ---------------- mosquito ----------------
def mosquito(c, t, x, y, s, rot=0.0, a=1.0, female_glow=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    # legs (long, thin, bent)
    for k, (bx, sgn) in enumerate(((-10, 1), (5, 1), (20, 1), (-10, -1), (5, -1), (20, -1))):
        kx = bx + 20 * (k % 3 - 1) * 1.6; ky = 70 * sgn
        lp = skia.Path(); lp.moveTo(bx, 6 * sgn); lp.lineTo(kx - 10, ky); lp.lineTo(kx - 40 + (k % 3) * 30, ky + 70 * sgn)
        c.drawPath(lp, paint("#2a2420", 0.9 * a, stroke=3.5))
    # wings (fast flap -> two soft ghost positions)
    fl = math.sin(t * 2 * math.pi * 7.5)
    for w_, al in ((fl, 0.35), (-fl, 0.18)):
        c.save(); c.translate(0, -8); c.rotate(-20 + 25 * w_)
        c.drawOval(skia.Rect.MakeLTRB(-120, -30, 10, 10), paint("#DCE6FF", al * a))
        c.drawOval(skia.Rect.MakeLTRB(-120, -30, 10, 10), paint("#ffffff", al * a, stroke=2))
        c.restore()
    # abdomen
    ab = skia.Rect.MakeLTRB(-150, -18, -10, 18)
    c.drawOval(ab, paint(shader=linear((-150, 0), (-10, 0), [col("#2d2622", a), col("#5a4c42", a)])))
    for k in range(5):
        xx = -135 + k * 25
        c.drawLine(xx, -15, xx, 15, paint("#E9E4DA", 0.75 * a, stroke=5))
    # thorax + head
    c.drawOval(skia.Rect.MakeLTRB(-20, -26, 40, 22), paint(shader=radial(10, -10, 40, [col("#6b5a4c", a), col(MOSQ, a)])))
    c.drawCircle(52, -4, 16, paint(MOSQ, a)); c.drawCircle(57, -9, 6, paint("#B23B3B", a))
    # proboscis + antennae
    c.drawLine(64, 0, 150, 18, paint("#2a2420", a, stroke=4))
    for sgn in (-1, 1):
        ap = skia.Path(); ap.moveTo(60, -12); ap.quadTo(100, -40 * sgn - 20, 120, -50 * sgn - 10)
        c.drawPath(ap, paint("#2a2420", a, stroke=3))
        for j in range(5):
            px, py = lerp(70, 116, j / 4), lerp(-18, -50 * sgn - 10, j / 4)
            c.drawLine(px, py, px - 6, py - 10, paint("#2a2420", 0.7 * a, stroke=1.6))
    if female_glow > 0:
        c.drawOval(ab, paint(BLOOD, 0.5 * female_glow * a, blur=10))
    c.restore()


def bzz(c, t, x, y, a):
    if a <= 0: return
    for k in range(3):
        u = ((t / (DUR / 10)) + k / 3) % 1.0
        r = 40 + 70 * u
        al = a * math.sin(math.pi * u)
        c.drawArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), -40, 80, False, paint("#ffffff", 0.5 * al, stroke=5))
        c.drawArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), 140, 80, False, paint("#ffffff", 0.5 * al, stroke=5))


def arm(c, t, y, a, heat=0.0, light=False, x0=-60, x1=900):
    """a forearm lying across the screen, hand to the right."""
    if a <= 0: return
    if heat > 0:
        for k in range(3):
            g = 60 + 40 * k + 12 * math.sin(t * 4 + k)
            c.drawRoundRect(skia.Rect.MakeLTRB(x0 - g, y - 90 - g, x1 + g, y + 90 + g), 90 + g, 90 + g, paint(HEAT, (0.38 if light else 0.22) * heat * a, blur=30))
    c.drawRoundRect(skia.Rect.MakeLTRB(x0, y - 85, x1, y + 85), 85, 85, paint("#000000", 0.3 * a, blur=16))
    c.drawRoundRect(skia.Rect.MakeLTRB(x0, y - 85, x1, y + 85), 85, 85, paint(shader=linear((0, y - 85), (0, y + 85), [col(SKIN_L, a), col(SKIN, a), col(SKIN_D, a)])))
    c.drawOval(skia.Rect.MakeLTRB(x1 - 120, y - 110, x1 + 90, y + 100), paint(shader=radial(x1, y - 20, 140, [col(SKIN_L, a), col(SKIN, a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(x0 + 40, y - 60, x1 - 60, y - 40), 10, 10, paint("#ffffff", 0.25 * a))
    if heat > 0:
        for k in range(6):
            u = ((t * 0.8 + k / 6) % 1.0)
            hx = 120 + k * 130
            hp = skia.Path(); hp.moveTo(hx, y - 110 - 140 * u)
            for j in range(1, 5):
                hp.lineTo(hx + 12 * math.sin(j * 1.6 + t * 6), y - 110 - 140 * u - j * 18)
            c.drawPath(hp, paint(HEAT, heat * a * math.sin(math.pi * u), stroke=6))


def fly_path(t, cx, cy, rx, ry, k=2):
    u = 2 * math.pi * k * t / DUR
    return cx + rx * math.sin(u), cy + ry * math.sin(2 * u) / 2, math.degrees(math.atan2(ry * math.cos(2 * u), rx * math.cos(u))) * 0.25


def scene_hook(c, t):
    bg_night(c, t)
    c.drawCircle(820, 760, 60, paint("#F4F0D8", 0.9)); c.drawCircle(845, 745, 55, paint("#0f1428"))
    arm(c, t, 1330, 0.9, heat=0.35)
    mx, my, r = fly_path(t, 470, 980, 230, 200, 2)
    mosquito(c, t, mx, my, 1.7, r)
    bzz(c, t, mx, my, 1.0)


def scene_open(c, t):
    scene_hook(c, t)
    # radar ring on "find"
    ra = window(t, FIND - 0.1, WIPE1, 0.2, 0.2)
    if ra > 0:
        for k in range(3):
            u = ((t - FIND) * 0.9 + k / 3) % 1.0
            c.drawCircle(495, 1330, 120 + 380 * u, paint(NIGHT, ra * (1 - u) * 0.8, stroke=4))
    pill(c, t, "HOW DOES IT FIND YOU?", 495, 560, NIGHT, 0.35, WIPE1 + 0.1)


# ---------------- white lab: step 1 breath, step 2 smell, step 3 heat ----------------
def head(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    p.moveTo(-40, 220); p.lineTo(-40, 130)
    p.cubicTo(-150, 110, -160, -60, -110, -130)
    p.cubicTo(-50, -210, 90, -200, 120, -90)
    p.lineTo(150, -20); p.lineTo(118, -8)
    p.cubicTo(122, 20, 120, 50, 100, 70)
    p.cubicTo(80, 90, 40, 100, 30, 130)
    p.lineTo(30, 220); p.close()
    c.drawPath(p, paint("#000000", 0.18 * a, blur=12))
    c.drawPath(p, paint(shader=linear((-160, -200), (150, 220), [col(SKIN_L, a), col(SKIN, a), col(SKIN_D, a)])))
    hair = skia.Path(); hair.moveTo(-120, -110); hair.cubicTo(-60, -230, 120, -200, 120, -95); hair.cubicTo(40, -140, -40, -120, -120, -40); hair.close()
    c.drawPath(hair, paint("#3a2a20", a))
    c.drawCircle(70, -50, 9, paint("#2a2420", a))
    c.drawLine(80, 42, 108, 40, paint(SKIN_D, a, stroke=5))
    c.restore()


def puff(c, x, y, r, a, label=True):
    if a <= 0: return
    for (dx, dy, rr) in ((0, 0, 1), (-0.6, 0.15, 0.7), (0.6, 0.18, 0.72), (0.1, -0.45, 0.6)):
        c.drawCircle(x + dx * r, y + dy * r, rr * r, paint(CO2, 0.55 * a))
    if label:
        f = skia.Font(TF_MONO, int(r * 0.5))
        c.drawString("CO2", x - f.measureText("CO2") / 2, y + r * 0.18, f, paint("#ffffff", a))


def germ_blob(c, t, x, y, r, colr, a, k):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(20 * math.sin(t * 2 + k))
    c.drawRoundRect(skia.Rect.MakeLTRB(-r * 1.5, -r, r * 1.5, r), r, r, paint(colr, a))
    c.drawCircle(-r * 0.5, -r * 0.3, r * 0.25, paint("#ffffff", 0.6 * a))
    c.restore()


def person(c, x, y, s, colr, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, -110, 48, paint(colr, a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -50, 70, 130), 60, 60, paint(colr, a))
    c.restore()


def heart(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    h = skia.Path(); h.moveTo(0, 30); h.cubicTo(-60, -10, -40, -60, 0, -30); h.cubicTo(40, -60, 60, -10, 0, 30); h.close()
    c.drawPath(h, paint(LOVE, a)); c.restore()


def step_dots(c, t, a):
    if a <= 0: return
    cur = 0 if t < S2 - 0.1 else (1 if t < S3 - 0.1 else 2)
    f = skia.Font(TF_MONO, 30)
    for k in range(3):
        x = 375 + k * 120; y = 690
        on = k <= cur
        q = eback(prog(t, (S1, S2, S3)[k] - 0.1, 0.3)) if on else 1
        c.drawCircle(x, y, 32 * q, paint(NIGHT if on else "#D6D3CC", a))
        s = str(k + 1)
        c.drawString(s, x - f.measureText(s) / 2, y + 11, f, paint("#ffffff", a))
        if k < 2:
            c.drawLine(x + 38, y, x + 82, y, paint(NIGHT if k < cur else "#D6D3CC", a, stroke=5))


def scene_lab(c, t):
    studio_white(c)
    a = eout(prog(t, WIPE1, 0.4))
    step_dots(c, t, a)
    s1 = a * (1 - eio(prog(t, S2 - 0.15, 0.35)))
    s2 = a * eio(prog(t, S2 - 0.15, 0.35)) * (1 - eio(prog(t, S3 - 0.15, 0.35)))
    s3 = a * eio(prog(t, S3 - 0.15, 0.35))
    # ---- step 1: breath -> CO2 cloud -> mosquito 15 m away
    if s1 > 0:
        head(c, 230, 1080, 1.0, s1)
        for k in range(7):
            u = ((t - BREATH) * 0.35 + k / 7) % 1.0 if t > BREATH - 0.2 else 0
            if t < BREATH - 0.2: continue
            px = lerp(370, 760, u); py = 1040 + 40 * math.sin(u * 6 + k) - 60 * u
            puff(c, px, py, lerp(28, 60, u), s1 * math.sin(math.pi * min(1, u * 1.2)) * clamp((t - BREATH + 0.2) * 3), label=t > CO2t - 0.1)
        mz = eout(prog(t, SENSE - 0.2, 0.4))
        mosquito(c, t, 790 + 10 * math.sin(t * 3), 900 + 14 * math.sin(t * 4), 0.75, 180 + 6 * math.sin(t * 5), s1 * mz)
        if mz > 0:
            ap = 0.5 + 0.5 * math.sin(t * 10)
            c.drawCircle(700, 910, 30 + 20 * ap, paint(CO2, 0.6 * s1 * mz, stroke=4))
        da = eout(prog(t, M15 - 0.2, 0.4)) * s1
        if da > 0:
            dp = paint(INK, 0.6 * da, stroke=4); dp.setPathEffect(skia.DashPathEffect.Make([16, 12], t * 30))
            c.drawLine(330, 1320, 800, 1320, dp)
            c.drawLine(330, 1295, 330, 1345, paint(INK, 0.6 * da, stroke=4)); c.drawLine(800, 1295, 800, 1345, paint(INK, 0.6 * da, stroke=4))
            big_number(c, "15", "m", 565, 1290, 120 * clamp(eback(prog(t, M15 - 0.2, 0.4)), 0, 1.2), NIGHT, da)
    # ---- step 2: smell from skin germs; some people get bitten more
    if s2 > 0:
        more = eio(prog(t, MORE - 0.1, 0.5))
        sk = s2 * (1 - more)
        if sk > 0:
            c.drawRoundRect(skia.Rect.MakeLTRB(130, 1080, 860, 1420), 60, 60, paint("#000000", 0.15 * sk, blur=14))
            c.drawRoundRect(skia.Rect.MakeLTRB(130, 1080, 860, 1420), 60, 60, paint(shader=linear((0, 1080), (0, 1420), [col(SKIN_L, sk), col(SKIN, sk), col(SKIN_D, sk)])))
            ga = eout(prog(t, GERMS - 0.1, 0.4)) * sk
            for k in range(12):
                rr = random.Random(600 + k)
                germ_blob(c, t, rr.uniform(190, 800), rr.uniform(1140, 1370), rr.uniform(16, 24) * clamp(eback(prog(t, GERMS + k * 0.03, 0.3)), 0, 1.3),
                          rr.choice(["#9B6BFF", "#3DBE8B", "#FFB020", "#4AA3DF"]), ga, k)
            sm = eout(prog(t, SMELLt - 0.1, 0.4)) * sk
            for k in range(6):
                u = ((t * 0.6 + k / 6) % 1.0)
                sx = 220 + k * 110
                sp = skia.Path(); sp.moveTo(sx, 1060 - 260 * u)
                for j in range(1, 6):
                    sp.lineTo(sx + 16 * math.sin(j * 1.4 + t * 5 + k), 1060 - 260 * u - j * 22)
                c.drawPath(sp, paint(SMELL, sm * math.sin(math.pi * u), stroke=7))
            la = eout(prog(t, LOVEt - 0.15, 0.4)) * sk
            mosquito(c, t, 720 + 10 * math.sin(t * 3), 830 + 10 * math.sin(t * 4), 0.65, 160, la)
            heart(c, 640, 760 + 8 * math.sin(t * 6), 1.0 * eback(prog(t, LOVEt - 0.1, 0.35)), la)
        if more > 0:
            for k, x in enumerate((220, 495, 770)):
                person(c, x, 1230, 1.0, "#B9B5AD" if k != 1 else "#8D7BE0", s2 * more)
            n = 7
            for k in range(n):
                u = 2 * math.pi * (t * 0.5 + k / n)
                mosquito(c, t, 495 + 170 * math.cos(u), 1130 + 110 * math.sin(u), 0.38, math.degrees(u) + 90, s2 * eout(prog(t, MORE + 0.4 + k * 0.25, 0.3)))
            for k, x in enumerate((220, 770)):
                u = 2 * math.pi * (t * 0.4 + k * 0.5)
                mosquito(c, t, x + 120 * math.cos(u), 1100 + 60 * math.sin(u), 0.38, math.degrees(u) + 90, s2 * more)
    # ---- step 3: up close, body heat
    if s3 > 0:
        heat = eout(prog(t, HEATt - 0.15, 0.4))
        arm(c, t, 1260, s3, heat=heat, light=True, x0=60, x1=820)
        near = eio(prog(t, CLOSE - 0.1, 0.8))
        mx = lerp(820, 560, near) + 12 * math.sin(t * 4); my = lerp(860, 1010, near) + 10 * math.sin(t * 5)
        mosquito(c, t, mx, my, 0.8, 150 + 6 * math.sin(t * 3), s3)
        if heat > 0:
            f = skia.Font(TF_MONO, 26)
            c.drawString("< 1 m", 300, 960, f, paint(HEAT, 0.0))
    pill(c, t, "STEP 1: YOUR BREATH", 495, 560, NIGHT, S1, CO2t - 0.05)
    pill(c, t, "CARBON DIOXIDE", 495, 560, "#6A84A8", CO2t, M15 - 0.05)
    pill(c, t, "SENSED FROM ~15 M", 495, 560, NIGHT, M15, S2 - 0.05)
    pill(c, t, "STEP 2: YOUR SMELL", 495, 560, NIGHT, S2, GERMS - 0.05)
    pill(c, t, "TINY SKIN GERMS", 495, 560, "#3DBE8B", GERMS, MORE - 0.05)
    pill(c, t, "SOME GET BITTEN MORE", 495, 560, "#8D7BE0", MORE, S3 - 0.05)
    pill(c, t, "STEP 3: YOUR HEAT", 495, 560, NIGHT, S3, HEATt - 0.05)
    pill(c, t, "BODY HEAT, UP CLOSE", 495, 560, "#E0602A", HEATt, WIPE2 + 0.1, text_col="#FFFFFF")


# ---------------- dark: females, eggs, loose clothes ----------------
def eggs(c, t, x, y, a, n):
    if a <= 0: return
    c.drawOval(skia.Rect.MakeLTRB(x - 260, y - 20, x + 260, y + 50), paint(NIGHT, 0.18 * a))
    for k in range(n):
        rr = random.Random(800 + k)
        ex = x - 160 + (k % 12) * 28 + rr.uniform(-3, 3); ey = y + (k // 12) * 22
        q = eback(clamp((t - EGGS) * 4 - k * 0.04))
        c.save(); c.translate(ex, ey); c.rotate(-10); c.scale(q, q)
        c.drawOval(skia.Rect.MakeLTRB(-9, -18, 9, 18), paint("#EDE7D9", a)); c.drawOval(skia.Rect.MakeLTRB(-9, -18, 9, 18), paint("#8E8676", a, stroke=2))
        c.restore()


def sleeve(c, t, y, cover, a):
    if a <= 0 or cover <= 0: return
    x1 = lerp(-80, 860, cover)
    c.drawRoundRect(skia.Rect.MakeLTRB(-120, y - 130, x1, y + 130), 90, 90, paint("#000000", 0.35 * a, blur=16))
    c.drawRoundRect(skia.Rect.MakeLTRB(-120, y - 130, x1, y + 130), 90, 90, paint(shader=linear((0, y - 130), (0, y + 130), [col("#7EA3EE", a), col(CLOTH, a), col("#2E57AE", a)])))
    for k in range(6):
        fx = -60 + k * 150
        if fx > x1 - 60: break
        fp = skia.Path(); fp.moveTo(fx, y - 120); fp.quadTo(fx + 50 + 10 * math.sin(t * 2 + k), y, fx + 10, y + 120)
        c.drawPath(fp, paint("#2E57AE", 0.6 * a, stroke=6))
    c.drawRoundRect(skia.Rect.MakeLTRB(x1 - 40, y - 130, x1, y + 130), 20, 20, paint("#3A64BE", a))


def scene_end(c, t):
    bg_night(c, t)
    a = eout(prog(t, WIPE2, 0.4))
    fem = window(t, WIPE2 + 0.1, TRICK, 0.3, 0.3) * a
    if fem > 0:
        z = eout(prog(t, WIPE2 + 0.1, 0.6))
        mosquito(c, t, 560 + 8 * math.sin(t * 3), 960 + 12 * math.sin(t * 4), 2.1 * lerp(0.8, 1, z), -8 + 3 * math.sin(t * 2), fem, female_glow=eout(prog(t, BLOODt - 0.1, 0.4)))
        ba = eback(prog(t, BLOODt - 0.1, 0.35))
        if ba > 0 and t < EGGS - 0.1:
            c.save(); c.translate(250, 1250); c.scale(ba, ba)
            d = skia.Path(); d.moveTo(0, -80); d.cubicTo(50, -20, 60, 20, 60, 40); d.cubicTo(60, 80, 30, 100, 0, 100); d.cubicTo(-30, 100, -60, 80, -60, 40); d.cubicTo(-60, 20, -50, -20, 0, -80)
            c.drawPath(d, paint(BLOOD, 0.4 * fem, blur=14)); c.drawPath(d, paint(BLOOD, fem)); c.drawCircle(-20, 30, 12, paint("#ffffff", 0.5 * fem))
            c.restore()
        eggs(c, t, 495, 1300, fem * eout(prog(t, EGGS - 0.15, 0.3)), 36)
    ta = eout(prog(t, TRICK - 0.2, 0.4)) * a
    if ta > 0:
        cover = eio(prog(t, CLOTHt - 0.1, 0.8))
        heat = 1 - cover
        arm(c, t, 1150, ta, heat=heat * 0.9)
        sleeve(c, t, 1150, cover, ta)
        bl = prog(t, BLOCK - 0.1, 0.6)
        if t < BLOCK - 0.1:
            mx, my = 640 + 10 * math.sin(t * 5), 860 + 10 * math.sin(t * 4)
        else:
            mx = lerp(560, 760, eout(bl)) + 10 * math.sin(t * 5); my = 940 - 260 * eout(bl) + 120 * math.sin(math.pi * min(1, bl * 2)) * 0.4
        mosquito(c, t, mx, my, 0.9, 150 if t < BLOCK else 200 + 30 * math.sin(t * 6), ta)
        if BLOCK - 0.05 < t < BLOCK + 0.5:
            u = (t - BLOCK + 0.05) / 0.55
            for k in range(8):
                an = k * math.pi / 4
                c.drawLine(600 + 40 * u * math.cos(an), 1010 + 40 * u * math.sin(an), 600 + 80 * u * math.cos(an), 1010 + 80 * u * math.sin(an), paint("#ffffff", (1 - u) * ta, stroke=5))
    pill(c, t, "ONLY FEMALES BITE", 495, 560, BLOOD, FEM, BLOODt - 0.05)
    pill(c, t, "THEY NEED BLOOD", 495, 560, BLOOD, BLOODt, EGGS - 0.05)
    pill(c, t, "TO MAKE EGGS", 495, 560, "#8E8676", EGGS, TRICK - 0.05)
    pill(c, t, "THE TRICK", 495, 560, "#5a5a66", TRICK, CLOTHt - 0.05)
    pill(c, t, "LOOSE CLOTHES", 495, 560, CLOTH, CLOTHt, BLOCK - 0.05)
    pill(c, t, "BLOCK THE BITE", 495, 560, CLOTH, BLOCK, HIDE - 0.05)
    pill(c, t, "HIDE YOUR HEAT", 495, 560, "#E0602A", HIDE, SO + 0.3, text_col="#FFFFFF")


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_lab(c, t); return
    if t < SO - 0.05:
        scene_end(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_end(c, t); c.restore()


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


KWCOL = {"find": NIGHT, "breath": CO2, "carbon": CO2, "dioxide": CO2, "15": NIGHT, "metres": NIGHT, "smell": SMELL,
         "love": LOVE, "more": "#B48CFF", "heat": HEAT, "females": BLOOD, "eggs": "#EDE7D9", "clothes": CLOTH}
CAPS = Captions(split_long(P), KWCOL, {"breath!", "more!"}, DUR)


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
    wipe(c, t, WIPE1, WL, NIGHT, "#F4F2EE")
    wipe(c, t, WIPE2, WL, BLOOD, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("pop", FIND), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", S1),
          ("hit", BREATH), ("pop", CO2t), ("pop", SENSE), ("hit", M15), ("pop", S2), ("pop", SMELLt), ("pop", GERMS),
          ("ding", LOVEt), ("hit", MORE2), ("pop", S3), ("whoosh", CLOSE), ("pop", HEATt), ("whoosh", WIPE2),
          ("hit", FEM), ("pop", BLOODt), ("pop", EGGS), ("whoosh", TRICK), ("pop", CLOTHt), ("hit", BLOCK),
          ("ding", HIDE), ("whoosh", SO - 0.05)]
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

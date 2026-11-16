import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
ICE = "#7FD3FF"; BLOOD = "#E0525A"; WARM = "#FF9F43"
SLATE = "#2E3A4F"; SLATE_L = "#46597A"


def p0(i):
    return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


# ---------------- beats (all from timings) ----------------
FREEZING = kw(1)
ELSE = kw(3); ROOF = kw(4)
ZOOM1 = p0(5) - 0.2
CHILLS = kw(6); TIGHTEN = kw(7); RUSH = kw(8)
NERVESHOT = p0(9) - 0.25
TRIG = kw(10); ALARM = kw(11)
ADDRESS = kw(12); FOREHEAD = kw(14)
LAB = p0(15) - 0.25
HAPPEN = kw(16); VOL = kw(17); SIP = p0(18)
ARTERY = p0(19); WIDEN = kw(20); NARROW = p0(21); STOPPED = kw(22)
BLOODQ = kw(23); NOTEX = kw(25)
NERVES = kw(26); DEBATED = kw(28)
WIPE1 = p0(29) - 0.3
AVOID = kw(29); Y2002 = p0(30); GRADER = kw(31); N145 = kw(31, 1)
GULP = p0(32); FIVE = kw(33); TWICE = kw(35)
FIX = p0(36) - 0.15; TONGUE = kw(37); EASES = kw(40)
WIPE2 = p0(41) - 0.3
FOREHEAD2 = kw(42)
LOOP = WIPE2 + 0.2
WL = 0.32
IMPACTS = [FOREHEAD, NOTEX]


def mode_at(t):
    if t < LAB: return "head"
    if t < NOTEX: return "lab"
    if t < WIPE1 + WL / 2: return "scale"
    if t < FIX: return "study"
    if t < WIPE2 + WL / 2: return "fix"
    return "end"


def light_at(t):
    return mode_at(t) in ("study", "fix")


rnd = random.Random(11)
FLAKES = [(rnd.uniform(0, W), rnd.random(), rnd.uniform(2, 6), rnd.uniform(0.03, 0.07), rnd.random() * 6.28) for _ in range(30)]


def cold_bg(c, t, a=1.0):
    studio_dark(c)
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W * 0.7, H * 0.45, 900, [col("#1d3a55", 0.55 * a), col("#0b0a0b", 0)])))
    for (x, ph, r, sp, ph2) in FLAKES:
        u = (t * sp + ph) % 1
        y = -40 + u * (H + 80)
        xx = x + 22 * math.sin(t * 0.8 + ph2)
        aa = a * 0.35 * min(1, u * 6) * min(1, (1 - u) * 6)
        c.save(); c.translate(xx, y); c.rotate(t * 20 + ph2 * 30)
        for k in range(3):
            c.rotate(60)
            c.drawLine(-r, 0, r, 0, paint("#cfeeff", aa, stroke=1.4))
        c.restore()


# ---------------- head model (local coords, facing right) ----------------
def head_path():
    p = skia.Path()
    p.moveTo(-150, 560)
    p.cubicTo(-160, 380, -200, 300, -290, 200)
    p.cubicTo(-380, 80, -380, -260, -230, -380)
    p.cubicTo(-110, -470, 120, -460, 220, -340)
    p.cubicTo(275, -270, 290, -180, 280, -120)
    p.cubicTo(278, -100, 290, -80, 300, -60)
    p.cubicTo(330, -10, 360, 20, 362, 45)
    p.cubicTo(362, 65, 330, 75, 300, 72)
    p.cubicTo(300, 90, 318, 110, 314, 126)
    p.cubicTo(312, 136, 300, 142, 292, 146)
    p.lineTo(292, 160)
    p.cubicTo(318, 168, 316, 190, 296, 205)
    p.cubicTo(290, 225, 300, 250, 300, 280)
    p.cubicTo(298, 320, 260, 335, 200, 330)
    p.cubicTo(150, 330, 110, 350, 100, 400)
    p.cubicTo(95, 440, 95, 500, 100, 560)
    p.close()
    return p


HEAD = head_path()


def brain_path():
    p = skia.Path()
    p.moveTo(-270, -150)
    p.cubicTo(-290, -300, -120, -390, 0, -375)
    p.cubicTo(150, -370, 240, -290, 228, -180)
    p.cubicTo(222, -110, 190, -60, 120, -40)
    p.cubicTo(60, -25, 0, -30, -50, -40)
    p.cubicTo(-120, -20, -170, 0, -220, -20)
    p.cubicTo(-260, -40, -265, -90, -270, -150)
    p.close()
    return p


BRAIN = brain_path()
GYRI = []
_r = random.Random(5)
for k in range(11):
    p = skia.Path()
    x0 = -240 + k * 42; y0 = -330 + _r.uniform(-20, 20)
    p.moveTo(x0, y0)
    for j in range(1, 9):
        p.lineTo(x0 + 18 * math.sin(j * 1.7 + k), y0 + j * 36 + _r.uniform(-6, 6))
    GYRI.append(p)
STEM = skia.Path(); STEM.moveTo(-60, -45); STEM.cubicTo(-70, 40, -80, 120, -95, 260)
CEREB = skia.Rect.MakeLTRB(-250, -70, -130, 10)


def palate_path(lift=0.0):
    p = skia.Path(); p.moveTo(292, 140); p.cubicTo(240, 110, 160, 104, 70, 118)
    return p


VESS_PAL = []
for k in range(3):
    p = skia.Path(); y = 98 - k * 9
    p.moveTo(276, y + 18)
    for x in range(270, 70, -12):
        p.lineTo(x, y + 6 * math.sin(x / 19 + k * 2) + (x - 70) * 0.05)
    VESS_PAL.append(p)
NERVE = skia.Path(); NERVE.moveTo(210, 104); NERVE.cubicTo(150, 50, 40, 60, -20, 10); NERVE.cubicTo(-45, -10, -55, -25, -58, -38)
NLEN = skia.PathMeasure(NERVE, False).getLength()
WRONG = skia.Path(); WRONG.moveTo(-50, -60); WRONG.cubicTo(-10, -250, 120, -300, 190, -250)
ACA = skia.Path(); ACA.moveTo(-50, -45); ACA.cubicTo(30, -80, 100, -130, 150, -200); ACA.cubicTo(175, -240, 180, -290, 150, -320)
PAIN_AT = (205, -235)


def tongue_path(lift):
    p = skia.Path(); dy = -46 * lift
    p.moveTo(80, 215)
    p.cubicTo(110, 160 + dy, 200, 150 + dy * 1.1, 262, 160 + dy * 0.8)
    p.cubicTo(286, 165 + dy * 0.6, 290, 185, 270, 200)
    p.cubicTo(220, 222, 140, 228, 80, 215)
    p.close()
    return p


def pain_burst(c, t, x, y, a, s=1.0):
    if a <= 0:
        return
    pu = 1 + 0.08 * math.sin(t * 14)
    c.drawCircle(x, y, 120 * s * pu, paint(shader=radial(x, y, 120 * s * pu, [col(RED, 0.75 * a), col(RED, 0)])))
    for k in range(3):
        u = (t * 1.6 + k / 3) % 1
        c.drawCircle(x, y, (30 + 110 * u) * s, paint(RED, a * (1 - u) * 0.8, stroke=4))
    c.save(); c.translate(x, y); c.scale(s, s)
    b = skia.Path(); b.moveTo(-10, -42); b.lineTo(14, -6); b.lineTo(-2, -4); b.lineTo(12, 40); b.lineTo(-16, -2); b.lineTo(0, -4); b.close()
    c.drawPath(b, paint("#FFFFFF", a))
    c.restore()


def popsicle(c, t, off, a=1.0):
    """Ice lolly entering the mouth from the right. off: 0 = tip touching the roof of the mouth, 1 = far right."""
    c.save(); c.translate(off * 260, 0); c.rotate(-6, 292, 140)
    x0, y0 = 232, 118
    c.drawLine(x0 + 210, y0 + 20, x0 + 300, y0 + 20, paint("#C9A26B", a, stroke=16))
    body = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y0 - 18, 220, 76), 36, 36)
    c.drawRRect(body, paint(shader=linear((0, y0 - 18), (0, y0 + 58), [col("#E8F7FF", a), col(ICE, a), col("#4FA8E0", a)])))
    c.drawRRect(body, paint("#ffffff", 0.5 * a, stroke=2))
    for k in range(5):
        c.drawCircle(x0 + 40 + k * 38, y0 - 2 + 6 * (k % 2), 4, paint("#ffffff", 0.7 * a))
    c.restore()


def draw_head(c, t, cx, cy, s, st, light=False):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    br = 1 + 0.004 * math.sin(t * 1.7); c.scale(br, br)
    c.drawPath(HEAD, paint("#000000", 0.5 if not light else 0.18, blur=34))
    c.drawPath(HEAD, paint(shader=linear((-380, -400), (360, 300), [col(SLATE_L), col(SLATE), col("#202a3a")])))
    c.save(); c.clipPath(HEAD)
    c.drawRect(skia.Rect.MakeLTRB(-400, 440, 400, 600), paint(shader=linear((0, 440), (0, 580), [col("#000000", 0), col("#0b0a0b" if not light else "#E4E1DB", 1)])))
    # brain
    c.drawPath(BRAIN, paint(shader=radial(40, -260, 360, [col("#F2B8BF"), col("#D98A96"), col("#B86675")])))
    c.drawOval(CEREB, paint("#C77584"))
    c.save(); c.clipPath(BRAIN)
    for g in GYRI:
        c.drawPath(g, paint("#9E4F60", 0.45, stroke=3))
    c.restore()
    c.drawPath(STEM, paint("#C77584", 1, stroke=34))
    fr = st.get("frost", 0)
    if fr > 0:
        c.drawPath(BRAIN, paint(ICE, 0.55 * fr))
        c.save(); c.clipPath(BRAIN)
        for k in range(14):
            x = -230 + (k * 37) % 440; y = -330 + (k * 53) % 280
            c.save(); c.translate(x, y); c.rotate(k * 17)
            for j in range(3):
                c.rotate(60); c.drawLine(-16, 0, 16, 0, paint("#ffffff", 0.8 * fr, stroke=2.5))
            c.restore()
        c.restore()
    # artery (anterior cerebral)
    aa = st.get("artery", 0)
    if aa > 0:
        w = lerp(9, 22, st.get("dil", 0))
        c.drawPath(ACA, paint(BLOOD, 0.35 * aa * (0.4 + st.get("dil", 0)), stroke=w * 2.2, blur=10))
        c.drawPath(ACA, paint("#B8323C", aa, stroke=w))
        c.drawPath(ACA, paint("#FF9AA0", 0.5 * aa, stroke=max(2, w * 0.25)))
        pm = skia.PathMeasure(ACA, False); L = pm.getLength()
        for k in range(6):
            u = (t * (0.5 + 0.9 * st.get("dil", 0)) + k / 6) % 1
            pos, _ = pm.getPosTan(L * u)
            c.drawCircle(pos.x(), pos.y(), w * 0.32, paint("#FFE1E3", aa * 0.9))
    # mouth cavity
    cav = skia.Path(); cav.moveTo(292, 146); cav.cubicTo(240, 112, 150, 108, 70, 122); cav.lineTo(70, 215); cav.cubicTo(150, 236, 250, 220, 292, 162); cav.close()
    c.drawPath(cav, paint("#1a0d12"))
    lift = st.get("tongue", 0)
    tp = tongue_path(lift)
    c.drawPath(tp, paint(shader=linear((0, 150), (0, 225), [col("#E58A93"), col("#B95B67")])))
    # palate vessels
    con = st.get("con", 0); rush = st.get("rush", 0)
    vw = lerp(5, 2, con) + 3 * rush
    vc = mixhex(BLOOD, "#7d6a70", con * 0.8)
    for p in VESS_PAL:
        if rush > 0:
            c.drawPath(p, paint(BLOOD, 0.5 * rush, stroke=vw * 3, blur=8))
        c.drawPath(p, paint(vc, 0.95, stroke=vw))
    if rush > 0:
        pm = skia.PathMeasure(VESS_PAL[1], False); L = pm.getLength()
        for k in range(7):
            u = (t * 1.4 + k / 7) % 1
            pos, _ = pm.getPosTan(L * u)
            c.drawCircle(pos.x(), pos.y(), 4, paint("#FFE1E3", rush))
    # palate
    pal = palate_path()
    c.drawPath(pal, paint("#E8DCC8", 1, stroke=12))
    cold = st.get("cold", 0)
    if cold > 0:
        c.drawPath(pal, paint(ICE, cold * (0.75 + 0.25 * math.sin(t * 6)), stroke=22, blur=9))
        c.drawPath(pal, paint("#DFF4FF", cold, stroke=8))
    warm = st.get("warm", 0)
    if warm > 0:
        c.drawPath(pal, paint(WARM, warm * (0.8 + 0.2 * math.sin(t * 4)), stroke=26, blur=10))
        c.drawPath(pal, paint("#FFE3C4", warm, stroke=8))
    # nerve
    nv = st.get("nerve", 0)
    if nv > 0:
        c.drawPath(NERVE, paint(YELLOW, 0.35 * nv, stroke=16, blur=8))
        c.drawPath(NERVE, paint("#E8C547", nv, stroke=6))
        pa = st.get("pulse", 0)
        if pa > 0:
            pm = skia.PathMeasure(NERVE, False)
            for k in range(4):
                u = (t * 1.1 + k / 4) % 1
                pos, _ = pm.getPosTan(NLEN * u)
                c.drawCircle(pos.x(), pos.y(), 20, paint(YELLOW, 0.35 * pa, blur=8))
                c.drawCircle(pos.x(), pos.y(), 8, paint("#FFF6C8", pa))
    wr = st.get("wrong", 0)
    if wr > 0:
        pp = paint("#FFFFFF", 0.9 * st.get("wrong_a", 1), stroke=5)
        eff = skia.DashPathEffect.Make([16, 12], -t * 40)
        pp.setPathEffect(eff)
        c.save()
        clipp = skia.PathMeasure(WRONG, False); L = clipp.getLength()
        seg = skia.Path(); clipp.getSegment(0, L * wr, seg, True)
        c.drawPath(seg, pp)
        if wr > 0.05:
            pos, tan = clipp.getPosTan(L * wr)
            ah = skia.Path(); x, y, dx, dy = pos.x(), pos.y(), tan.x(), tan.y()
            ah.moveTo(x + dx * 16, y + dy * 16); ah.lineTo(x - dy * 11, y + dx * 11); ah.lineTo(x + dy * 11, y - dx * 11); ah.close()
            c.drawPath(ah, paint("#FFFFFF", 0.9 * st.get("wrong_a", 1)))
        c.restore()
    c.restore()  # clip
    pain_burst(c, t, PAIN_AT[0], PAIN_AT[1], st.get("pain", 0))
    # popsicle sits in front (outside clip)
    po = st.get("pop", None)
    if po is not None:
        popsicle(c, t, po, st.get("pop_a", 1.0))
    c.drawPath(HEAD, paint("#9fc2ff" if not light else "#5b6b85", 0.35, stroke=3, blur=1.5))
    c.restore()


# ---------------- camera for the head chapter ----------------
SHOT_FULL = (470, 1020, 1.04, 0, 0)        # screen cx, cy, scale, local focus x, y
SHOT_MOUTH = (540, 1020, 2.5, 185, 135)
SHOT_NERVE = (540, 1000, 1.55, 80, -70)


def cam(shot_a, shot_b, q):
    ax, ay, asc, afx, afy = shot_a; bx, by, bsc, bfx, bfy = shot_b
    s = lerp(asc, bsc, q); fx = lerp(afx, bfx, q); fy = lerp(afy, bfy, q)
    sx = lerp(ax, bx, q); sy = lerp(ay, by, q)
    return sx - fx * s, sy - fy * s, s


def head_cam(t):
    if t < ZOOM1 - 0.6:
        x, y, s = cam(SHOT_FULL, SHOT_FULL, 0)
        push = 1 + 0.03 * prog(t, 0, ZOOM1)
        return x - (540 - x) * (push - 1) * 0, y, s * push
    if t < NERVESHOT:
        q = eio(prog(t, ZOOM1 - 0.6, 1.0))
        x, y, s = cam(SHOT_FULL, SHOT_MOUTH, q)
        return x, y, s * (1 + 0.02 * prog(t, ZOOM1, NERVESHOT - ZOOM1))
    q = eio(prog(t, NERVESHOT, 0.9))
    x, y, s = cam(SHOT_MOUTH, SHOT_NERVE, q)
    return x, y, s * (1 + 0.03 * prog(t, NERVESHOT + 0.9, LAB - NERVESHOT))


def head_state(t):
    st = {}
    st["pop"] = lerp(0.55, 0.0, eout(prog(t, 0.0, 1.1)))
    st["frost"] = window(t, 0.15, FREEZING + 0.6, 0.35, 0.5)
    st["cold"] = eout(prog(t, ROOF - 0.15, 0.4))
    st["con"] = eio(prog(t, TIGHTEN, 0.7)) * (1 - eout(prog(t, RUSH, 0.35)))
    st["rush"] = eout(prog(t, RUSH, 0.35))
    st["nerve"] = eout(prog(t, NERVESHOT + 0.3, 0.5))
    st["pulse"] = window(t, ALARM - 0.1, FOREHEAD + 0.8, 0.2, 0.4)
    st["wrong"] = eio(prog(t, ADDRESS, 1.0))
    st["wrong_a"] = 1 - prog(t, FOREHEAD + 0.3, 0.4)
    st["pain"] = eout(prog(t, FOREHEAD, 0.2))
    return st


def draw_head_scene(c, t):
    cold_bg(c, t)
    x, y, s = head_cam(t)
    st = head_state(t)
    draw_head(c, t, x, y, s, st)
    L = lambda lx, ly: (x + lx * s, y + ly * s)
    # hook: brain frozen? -> struck
    if t < FREEZING + 1.6:
        fall = ein(prog(t, FREEZING + 0.75, 0.6))
        c.save(); c.translate(0, 600 * fall); c.rotate(-8 * fall)
        bx, by = L(-20, -200)
        pill(c, t, "BRAIN FROZEN?", bx, by - 0, ICE, 0.35, FREEZING + 1.3, text_col=INK)
        sp = eout(prog(t, FREEZING + 0.15, 0.2))
        if sp > 0:
            c.drawLine(bx - 160, by + 2, lerp(bx - 160, bx + 160, sp), by - 2, paint(RED, 1 - prog(t, FREEZING + 1.2, 0.2), stroke=6))
        c.restore()
    pill(c, t, "ROOF OF MOUTH", 300, 1440, ICE, ROOF, CHILLS - 0.1, anchor=L(200, 110), text_col=INK)
    pill(c, t, "BLOOD VESSELS", 300, 1440, BLOOD, TIGHTEN - 0.1, NERVESHOT, anchor=L(150, 98))
    pill(c, t, "SQUEEZE", 760, 700, "#FFFFFF", TIGHTEN + 0.1, RUSH)
    pill(c, t, "RUSH OPEN", 760, 700, BLOOD, RUSH + 0.05, NERVESHOT)
    pill(c, t, "TRIGEMINAL NERVE", 640, 1470, YELLOW, TRIG, ADDRESS, anchor=L(120, 48))
    pill(c, t, "WRONG ADDRESS?", 300, 700, "#FFFFFF", ADDRESS + 0.3, FOREHEAD - 0.05)
    pill(c, t, "REFERRED PAIN", 700, 1470, RED, FOREHEAD + 0.35, LAB)
    footnote(c, t, "Simplified illustration", 0.4, ZOOM1)
    footnote(c, t, "Magnified · simplified", ZOOM1 + 0.3, NERVESHOT)
    footnote(c, t, "Leading explanation (UCLA Health)", NERVESHOT + 0.4, LAB)
    if t > LAB - 0.05:
        pass


# ---------------- 2012 lab ----------------
def flow_value(t):
    base = 0.3
    up = eio(prog(t, WIDEN - 0.3, 0.8)); down = eio(prog(t, NARROW + 0.5, 1.0))
    return base + 0.55 * up * (1 - down) + 0.03 * math.sin(t * 9)


def monitor(c, t, a):
    if a <= 0:
        return
    r = skia.Rect.MakeLTRB(80, 1200, 1000, 1470)
    rr = skia.RRect.MakeRectXY(r, 22, 22)
    c.drawRRect(rr, paint("#0E1218", 0.92 * a)); c.drawRRect(rr, paint("#ffffff", 0.18 * a, stroke=1.5))
    f = skia.Font(TF_MONO_M, 22)
    c.drawString("BLOOD FLOW · BRAIN ARTERY", 110, 1240, f, paint("#ffffff", 0.6 * a))
    # 13 volunteer icons
    va = prog(t, VOL, 0.6)
    for k in range(13):
        q = clamp(va * 13 - k)
        if q <= 0: continue
        x = 640 + k * 26
        c.drawCircle(x, 1226, 6 * q, paint(ICE, a)); c.drawRoundRect(skia.Rect.MakeXYWH(x - 8 * q, 1235, 16 * q, 12 * q), 5, 5, paint(ICE, a))
    # trace
    t0 = LAB; span = 6.0
    p = skia.Path(); first = True
    now = t
    for k in range(0, 121):
        tt = now - span + span * k / 120
        if tt < t0: continue
        v = flow_value(tt)
        x = 110 + 860 * k / 120; y = 1440 - 170 * v
        p.moveTo(x, y) if first else p.lineTo(x, y); first = False
    if not first:
        c.drawPath(p, paint(BLOOD, 0.4 * a, stroke=10, blur=8))
        c.drawPath(p, paint(BLOOD, a, stroke=4))
        y = 1440 - 170 * flow_value(now)
        c.drawCircle(970, y, 8, paint("#FFFFFF", a))
    c.drawLine(110, 1440, 970, 1440, paint("#ffffff", 0.15 * a, stroke=1.5))


SHOT_LAB = (540, 880, 1.45, -10, -190)


def draw_lab(c, t):
    cold_bg(c, t)
    q = eout(prog(t, LAB, 0.8))
    x, y, s = cam(SHOT_NERVE, SHOT_LAB, q)
    s *= 1 + 0.03 * prog(t, LAB + 0.8, NOTEX - LAB)
    st = {"pop": None, "cold": 1 - prog(t, LAB, 0.6) * 0.5, "rush": 0.4, "nerve": 1 - prog(t, LAB, 0.5),
          "artery": eout(prog(t, ARTERY - 0.2, 0.5)),
          "dil": eio(prog(t, WIDEN - 0.1, 0.6)) * (1 - eio(prog(t, NARROW + 0.6, 0.9))),
          "pain": (1 - prog(t, LAB, 0.6) * 0.6) * (1 - eout(prog(t, STOPPED, 0.4)))}
    draw_head(c, t, x, y, s, st)
    L = lambda lx, ly: (x + lx * s, y + ly * s)
    monitor(c, t, eout(prog(t, HAPPEN - 0.3, 0.4)))
    pill(c, t, "2012 · 13 VOLUNTEERS", 540, 1150, ICE, VOL, NOTEX, text_col=INK)
    pill(c, t, "ARTERY WIDENS", 800, 640, BLOOD, WIDEN, NARROW + 0.2, anchor=L(150, -200))
    pill(c, t, "NARROWS · PAIN STOPS", 700, 640, "#FFFFFF", STOPPED, BLOODQ - 0.1, anchor=L(150, -200))
    pill(c, t, "ALL ABOUT BLOOD?", 540, 640, BLOOD, BLOODQ, NOTEX + 0.1)
    footnote(c, t, "Serrador et al. · Experimental Biology 2012 (conference study)", HAPPEN, NOTEX)


# ---------------- debate scale ----------------
def draw_scale(c, t):
    cold_bg(c, t, 0.6)
    ang = 0.0
    tilt = eio(prog(t, NERVES, 0.8))
    ang = 9 * tilt * (1 - 0.0 * prog(t, DEBATED, 0.3))
    wob = prog(t, DEBATED - 0.2, 0.4)
    ang = ang * (1 - wob) + wob * 7 * math.sin((t - DEBATED) * 3.2)
    ang += 1.2 * math.sin(t * 1.5)
    cx, cy = 540, 950
    s = 1 + 0.03 * prog(t, NOTEX, WIPE1 - NOTEX)
    ent = eback(prog(t, NOTEX + 0.05, 0.45), 1.2)
    c.save(); c.translate(cx, cy + 260); c.scale(s * ent, s * ent); c.translate(-cx, -(cy + 260))
    # stand
    c.drawOval(skia.Rect.MakeLTRB(cx - 150, cy + 480, cx + 150, cy + 520), paint("#000000", 0.5, blur=14))
    c.drawRoundRect(skia.Rect.MakeLTRB(cx - 110, cy + 460, cx + 110, cy + 500), 12, 12, paint("#3a4150"))
    c.drawRect(skia.Rect.MakeLTRB(cx - 10, cy, cx + 10, cy + 470), paint("#5a6476"))
    c.drawCircle(cx, cy, 22, paint("#cfd6e2"))
    for side, colr, lab in ((-1, BLOOD, "BLOOD VESSELS"), (1, YELLOW, "NERVES")):
        th = math.radians(ang)
        px = cx + side * 320 * math.cos(th); py = cy + side * 320 * math.sin(th)
        c.drawLine(px, py, px - 110, py + 230, paint("#9aa3b3", 0.8, stroke=2.5))
        c.drawLine(px, py, px + 110, py + 230, paint("#9aa3b3", 0.8, stroke=2.5))
        pan = skia.Path(); pan.moveTo(px - 140, py + 230); pan.cubicTo(px - 120, py + 300, px + 120, py + 300, px + 140, py + 230); pan.close()
        c.drawPath(pan, paint("#5a6476"))
        c.drawPath(pan, paint("#ffffff", 0.25, stroke=2))
        # icon on pan
        if side < 0:
            ic = skia.Path(); ic.moveTo(px - 90, py + 200)
            for k in range(13):
                ic.lineTo(px - 90 + k * 15, py + 195 + 16 * math.sin(k * 0.9 + t * 3))
            c.drawPath(ic, paint(BLOOD, 0.4, stroke=22, blur=6)); c.drawPath(ic, paint(BLOOD, 1, stroke=12))
        else:
            ic = skia.Path(); ic.moveTo(px - 90, py + 205); ic.cubicTo(px - 40, py + 150, px + 40, py + 240, px + 90, py + 185)
            c.drawPath(ic, paint(YELLOW, 0.4, stroke=18, blur=8)); c.drawPath(ic, paint("#E8C547", 1, stroke=7))
            pm = skia.PathMeasure(ic, False)
            u = (t * 1.2) % 1
            pos, _ = pm.getPosTan(pm.getLength() * u)
            c.drawCircle(pos.x(), pos.y(), 9, paint("#FFF6C8"))
        pill(c, t, lab, px, py + 340, colr, NOTEX + 0.25 + (0.12 if side > 0 else 0), WIPE1 + 0.2, text_col=INK if side > 0 else None)
    c.save(); c.translate(cx, cy); c.rotate(ang)
    c.drawRoundRect(skia.Rect.MakeLTRB(-340, -10, 340, 10), 10, 10, paint("#cfd6e2"))
    c.restore()
    c.restore()
    qa = eback(prog(t, DEBATED, 0.35))
    if qa > 0:
        f = skia.Font(TF_BLACK, 190)
        c.save(); c.translate(540, 740); c.scale(qa, qa); c.rotate(4 * math.sin(t * 2.5))
        c.drawString("?", -f.measureText("?") / 2, 66, f, paint("#FFFFFF", clamp(qa)))
        c.restore()
    pill(c, t, "STILL DEBATED", 540, 560 + 0, "#FFFFFF", DEBATED + 0.2, WIPE1 + 0.2)
    footnote(c, t, "UCLA Health: sensory nerves now suspected as the main driver", NERVES, WIPE1 + 0.2)


# ---------------- white chapter: the 2002 study ----------------
def cup(c, t, cx, cy, s, a=1.0):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-150, 150, 150, 185), paint("#000000", 0.16 * a, blur=14))
    for (x, y, r, colr) in ((-60, -40, 85, "#F6E3C8"), (60, -40, 85, "#F2A7B8"), (0, -110, 90, "#8C5A43")):
        c.drawCircle(x, y + 4 * math.sin(t * 2 + x), r, paint(shader=radial(x - r * 0.4, y - r * 0.4, r * 1.6, [col("#ffffff", a), col(colr, a)], [0, 0.5])))
    cp = skia.Path(); cp.moveTo(-150, 0); cp.lineTo(150, 0); cp.lineTo(110, 170); cp.lineTo(-110, 170); cp.close()
    c.drawPath(cp, paint(shader=linear((-150, 0), (150, 0), [col("#3B5BDB", a), col("#6E86F0", a), col("#2E47B8", a)])))
    for k in range(5):
        c.drawLine(-120 + k * 60, 4, -90 + k * 45, 166, paint("#ffffff", 0.25 * a, stroke=3))
    c.drawRoundRect(skia.Rect.MakeLTRB(-160, -12, 160, 12), 8, 8, paint("#F4F2EE", a))
    c.restore()


def dot_pos(i, split):
    # grid (15 cols) -> two groups (left 73, right 72)
    col_, row = i % 15, i // 15
    gx, gy = 155 + col_ * 55, 760 + row * 52
    if i < 73:
        g = i; cx_, cy_ = 120 + (g % 8) * 46, 820 + (g // 8) * 46
    else:
        g = i - 73; cx_, cy_ = 600 + (g % 8) * 46, 820 + (g // 8) * 46
    return lerp(gx, cx_, split), lerp(gy, cy_, split)


HEADACHE_L = set(random.Random(2).sample(range(73), 20))
HEADACHE_R = set(73 + k for k in random.Random(4).sample(range(72), 9))


def stopwatch(c, t, x, y, label, colr, a, speed):
    if a <= 0: return
    c.drawCircle(x, y, 44, paint("#FFFFFF", a)); c.drawCircle(x, y, 44, paint(INK, a, stroke=4))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 10, y - 62, 20, 14), 4, 4, paint(INK, a))
    ang = (t * speed) % 360
    c.save(); c.translate(x, y); c.rotate(ang)
    c.drawLine(0, 0, 0, -32, paint(colr, a, stroke=5)); c.restore()
    f = skia.Font(TF_MONO, 30)
    c.drawString(label, x + 64, y + 11, f, paint(INK, a))


def draw_study(c, t):
    studio_white(c)
    # cup intro, then fades away as the dots arrive
    ca = 1 - prog(t, Y2002, 0.4)
    if ca > 0:
        sc = eback(prog(t, WIPE1 + 0.1, 0.5), 1.2) * (1 + 0.03 * prog(t, WIPE1, 2))
        cup(c, t, 540, 960, 1.6 * sc, ca)
        qa = eback(prog(t, AVOID, 0.3)) * ca
        if qa > 0:
            f = skia.Font(TF_BLACK, 150)
            c.save(); c.translate(820, 680); c.scale(qa, qa); c.rotate(8)
            c.drawString("?", -f.measureText("?") / 2, 50, f, paint(INK, ca)); c.restore()
    da = eout(prog(t, Y2002, 0.4)) * (1 - prog(t, FIX - 0.3, 0.3))
    if da > 0:
        n_on = int(145 * eio(prog(t, Y2002 + 0.1, N145 + 0.5 - Y2002)))
        split = eio(prog(t, FIVE - 0.2, 0.8))
        red = eout(prog(t, TWICE - 0.6, 0.5))
        for i in range(145):
            if i >= n_on and t < N145 + 1: continue
            x, y = dot_pos(i, split)
            ap = da
            base = ICE if (split > 0.5 and i < 73) else "#9AA3B3"
            if i < 73 and split > 0: base = mixhex("#9AA3B3", "#3B5BDB", split)
            cc = mixhex(base, RED, red) if (i in HEADACHE_L or i in HEADACHE_R) else base
            c.drawCircle(x, y, 17, paint(cc, ap))
            c.drawCircle(x - 5, y - 5, 5, paint("#ffffff", 0.45 * ap))
        sa = window(t, FIVE - 0.1, FIX - 0.2, 0.3, 0.3)
        stopwatch(c, t, 160, 700, "< 5 SEC", "#3B5BDB", sa, 900)
        stopwatch(c, t, 640, 700, "> 30 SEC", "#8a8f98", sa, 120)
        ra = eout(prog(t, TWICE - 0.4, 0.4))
        if ra > 0:
            v1 = 27 * eexpo(prog(t, TWICE - 0.4, 0.8)); v2 = 13 * eexpo(prog(t, TWICE - 0.4, 0.8))
            big_number(c, f"{int(round(v1))}%", "", 280, 1330, 110, RED, ra * da)
            big_number(c, f"{int(round(v2))}%", "", 760, 1330, 110, "#8a8f98", ra * da)
            f = skia.Font(TF_MONO, 24)
            for (x, s_) in ((280, "GOT BRAIN FREEZE"), (760, "GOT BRAIN FREEZE")):
                c.drawString(s_, x - f.measureText(s_) / 2, 1380, f, paint(INK, 0.6 * ra * da))
        xa = eback(prog(t, TWICE + 0.25, 0.35))
        if xa > 0:
            c.save(); c.translate(520, 1290); c.scale(xa, xa)
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-70, -60, 140, 100), 24, 24)
            c.drawRRect(rr, paint(RED, da)); f = skia.Font(TF_BLACK, 76)
            c.drawString("2×", -f.measureText("2×") / 2, 16, f, paint("#FFFFFF", da))
            c.restore()
    pill(c, t, "2002 · 145 STUDENTS", 540, 640, "#3B5BDB", N145 - 0.1, FIVE - 0.25, light=True)
    pill(c, t, "STUDY BY AN 8TH GRADER", 540, 1440, "#FFFFFF", GRADER, FIVE - 0.25, light=True, outline=True)
    footnote(c, t, "Kaczorowski & Kaczorowski 2002 · BMJ (randomised, not blinded)", Y2002, FIX)


SHOT_FIX = (540, 1000, 2.6, 185, 135)


def draw_fix(c, t):
    studio_white(c)
    x, y, s = cam(SHOT_FIX, SHOT_FIX, 0)
    ent = eout(prog(t, FIX, 0.6))
    s *= lerp(1.12, 1.0, ent) * (1 + 0.03 * prog(t, FIX + 0.6, WIPE2 - FIX))
    x = 540 - 185 * s; y = 1010 - 135 * s
    lift = eback(prog(t, TONGUE - 0.1, 0.5), 1.2)
    st = {"pop": None, "cold": 1 - eio(prog(t, EASES - 0.4, 1.0)), "tongue": lift,
          "warm": eout(prog(t, TONGUE + 0.4, 1.2)) * (0.6 + 0.4 * eout(prog(t, EASES, 0.6)))}
    box = skia.Rect.MakeLTRB(90, 600, 990, 1400)
    rr = skia.RRect.MakeRectXY(box, 48, 48)
    c.saveLayerAlpha(None, int(255 * ent))
    c.drawRRect(rr, paint("#000000", 0.25, blur=30))
    c.save(); c.clipRRect(rr, True)
    cold_bg(c, t, 0.8)
    draw_head(c, t, x, y, s, st)
    c.restore()
    c.drawRRect(rr, paint("#FFFFFF", 1, stroke=8))
    c.restore()
    L = lambda lx, ly: (x + lx * s, y + ly * s)
    pill(c, t, "TONGUE → ROOF", 720, 1455, WARM, TONGUE, WIPE2 + 0.2, anchor=L(190, 170), light=True, text_col=INK)
    pill(c, t, "WARMS IT UP", 760, 640, WARM, p0(39), WIPE2 + 0.2, anchor=L(170, 112), light=True, text_col=INK)
    footnote(c, t, "Educational only, not medical advice", FIX, WIPE2 + 0.2, light=True)


def draw_end(c, t):
    cold_bg(c, t)
    x, y, s = cam(SHOT_FULL, SHOT_FULL, 0)
    k = eio(prog(t, LOOP, DUR - 0.4 - LOOP))
    s *= lerp(1.04, 1.0, k)
    pop = lerp(0.18, 0.55, eio(prog(t, FOREHEAD2 + 0.6, DUR - FOREHEAD2 - 1.0)))
    pain = window(t, FOREHEAD2 - 0.05, DUR - 0.6, 0.2, 0.5)
    st = {"pop": pop, "cold": 0.6 * (1 - prog(t, DUR - 1.2, 0.8)), "pain": pain, "frost": prog(t, DUR - 0.8, 0.6) * 0}
    draw_head(c, t, x, y, s, st)
    footnote(c, t, "Sources: BMJ 2002 · Experimental Biology 2012 · UCLA Health", WIPE2 + 0.4, DUR + 1)


def draw_world(c, t):
    m = mode_at(t)
    if m == "head":
        draw_head_scene(c, t)
        if t > LAB - 0.05:
            pass
    elif m == "lab": draw_lab(c, t)
    elif m == "scale": draw_scale(c, t)
    elif m == "study": draw_study(c, t)
    elif m == "fix": draw_fix(c, t)
    else: draw_end(c, t)


def hud_val(t):
    m = mode_at(t)
    if m == "head":
        if t < ROOF - 0.1: return ("BRAIN FREEZE", "INCOMING", ICE)
        if t < ALARM: return ("BRAIN FREEZE", "COLD PALATE", ICE)
        if t < FOREHEAD: return ("BRAIN FREEZE", "SIGNAL SENT", YELLOW)
        return ("BRAIN FREEZE", "PAIN · FOREHEAD", RED)
    if m == "lab":
        if t < STOPPED: return ("LAB TEST · 2012", "MEASURING", BLOOD)
        return ("LAB TEST · 2012", "PAIN STOPPED", "#FFFFFF")
    if m == "scale": return ("CAUSE", "DEBATED", "#8a8a8a")
    if m == "study":
        if t < TWICE: return ("STUDY · 2002", "ICE CREAM TEST", "#3B5BDB")
        return ("STUDY · 2002", "FAST = 2× RISK", RED)
    if m == "fix": return ("BRAIN FREEZE", "WARMING UP", WARM)
    return ("BRAIN FREEZE", "INCOMING", ICE)


KWCOL = {"freezing": ICE, "else": ICE, "roof": ICE, "chills": ICE, "tighten": BLOOD, "rush": BLOOD,
         "trigeminal": YELLOW, "alarm": YELLOW, "forehead": RED, "widened": BLOOD, "blood": BLOOD,
         "not exactly": RED, "nerves": YELLOW, "avoid": "#3B5BDB", "145": "#3B5BDB", "five": "#3B5BDB", "twice": RED,
         "tongue": "#E8770E", "eases": "#E8770E"}
CAPS = Captions(P, KWCOL, {"twice", "not", "forehead."}, DUR)


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
    ha = prog(t, 0.3, 0.3) * (1 - prog(t, DUR - 0.9, 0.4))
    hud(c, t, lab, val, dc, ha, light)
    rw = math.sin(math.pi * prog(t, NOTEX, 0.45))
    if rw > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.24 * rw))
    for ti in IMPACTS:
        if 0 <= t - ti < 2 / FPS:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#FFFFFF", 0.3))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, "#3B5BDB", "#F4F2EE")
    wipe(c, t, WIPE2, WL, "#3B5BDB", INK)
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.05), ("pop", 0.4), ("tick", FREEZING + 0.15), ("whoosh", ZOOM1 - 0.6), ("pop", ROOF),
          ("pop", TIGHTEN - 0.1), ("pop", RUSH), ("whoosh", NERVESHOT), ("pop", TRIG), ("riser", ALARM - 0.2),
          ("pop", ADDRESS + 0.3), ("hit", FOREHEAD), ("pop", FOREHEAD + 0.35), ("whoosh", LAB), ("pop", VOL),
          ("pop", WIDEN), ("ding", STOPPED), ("pop", BLOODQ), ("hit", NOTEX), ("pop", NOTEX + 0.25), ("pop", NOTEX + 0.37),
          ("pop", DEBATED + 0.2), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", AVOID), ("pop", N145 - 0.1),
          ("pop", GRADER), ("whoosh", FIVE - 0.2), ("ding", TWICE + 0.25), ("pop", TONGUE), ("pop", p0(39)),
          ("whoosh", WIPE2), ("riser", FOREHEAD2 - 1.0), ("whoosh", DUR - 0.8)]
    for k in range(10):
        ev.append(("tick", N145 - 0.2 + 0.07 * k * (1 + k * 0.2)))
    for k in range(6):
        ev.append(("tick", TWICE - 0.4 + 0.07 * k * (1 + k * 0.25)))
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

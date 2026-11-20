# HIW17 — "What are the squiggly things floating in your eyes?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-21):
#  - Mayo Clinic "Eye floaters" (mayoclinic.org/diseases-conditions/eye-floaters/symptoms-causes/syc-20372346, 2024):
#    spots / strings / cobwebs that drift when you move your eyes and seem to dart away when you try to look at them;
#    most noticeable against a plain bright background like blue sky or a white wall; mostly age-related: the vitreous
#    (jelly-like substance inside the eye) liquefies and contracts, collagen fibres clump and cast tiny shadows on the
#    retina — those shadows are the floaters; many people over 50 have them; they often settle out of the line of vision.
#    See an eye specialist immediately for: many more floaters than usual, sudden onset of new floaters, flashes of light,
#    a grey curtain / darkness blocking part of your vision (possible retinal tear/detachment = emergency).
#  Owner rule: no studies, plain words ("jelly", "threads", "back of your eye"). Footnote: "Educational only, not medical advice."
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
SKY = "#6EC3FF"; SKY_D = "#2B6FD6"; JELLY = "#BFE9FF"; THREAD = "#8C7BFF"; SHADOW = "#3B3550"; LIGHT = "#FFE27A"
RETINA = "#FF8C8C"; GREEN = "#1fb98a"; ORANGE = "#FF9F43"; IRIS = "#3E8E7E"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


SKYt = kw(1); THERE = p0(2); LOOK = p0(3); ZOOM = kw(4)
WIPE1 = p0(5) - 0.3; JELLYt = kw(6); OVER = p0(7); THREADS = kw(8); LIGHTt = p0(9); SHAD = kw(10)
NOTT = p0(11); SHAD2 = kw(12)
WIPE2 = p0(13) - 0.3; MOVES = kw(13); DART = kw(14); COMMON = kw(15); FIFTY = kw(16)
SUDDEN = kw(17); FLASH = kw(18); CURTAIN = kw(19); FAST = kw(20); SO = p0(21)
WL = 0.32
IMPACTS = [ZOOM, SUDDEN]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1, ph=0.0):
    return math.sin(2 * math.pi * k * t / DUR + ph)


def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#1b1d27"), col("#12131a"), col("#08090c")], [0, 0.55, 1])))
    c.drawCircle(800 + 30 * lw(t), 720, 520, paint(shader=radial(800, 720, 520, [col(THREAD, 0.10), col(THREAD, 0)])))
    c.drawCircle(220, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1450, 600, [col(SKY, 0.07), col(SKY, 0)])))


def cloud(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, dy, r in ((-70, 10, 55), (-10, -20, 75), (60, 5, 60), (0, 25, 60)):
        c.drawCircle(dx, dy, r, paint("#ffffff", a))
    c.restore()


def floater(c, x, y, s, rot, t, a, seed=0, color="#1d2a44"):
    """translucent squiggly string with little beads, like a real floater."""
    if a <= 0: return
    rr = random.Random(seed)
    n = 26
    L = rr.uniform(220, 340)
    ph = rr.uniform(0, 6.28); k1 = rr.uniform(2, 4)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path()
    pts = []
    for i in range(n + 1):
        u = i / n
        px = (u - 0.5) * L
        py = 38 * math.sin(u * k1 * math.pi + ph + 0.6 * math.sin(t * 0.8 + seed)) + 18 * math.sin(u * 9 + seed)
        pts.append((px, py))
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    c.drawPath(p, paint(color, 0.16 * a, stroke=26, blur=10))
    c.drawPath(p, paint(color, 0.32 * a, stroke=7, blur=2.5))
    for i in range(0, n + 1, 5):
        c.drawCircle(pts[i][0], pts[i][1], 11, paint(color, 0.22 * a, blur=4))
        c.drawCircle(pts[i][0], pts[i][1], 7, paint("#ffffff", 0.12 * a, stroke=2))
    c.restore()


FL = [(300, 900, 0.9, 20, 0), (690, 760, 1.1, -30, 1), (560, 1230, 0.8, 60, 2), (240, 1330, 0.7, -10, 3), (780, 1120, 0.75, 10, 4)]


def floaters_layer(c, t, a, dx=0.0, dy=0.0, lag=0.0):
    for i, (x, y, s, r, sd) in enumerate(FL):
        fx = x + 40 * lw(t, 1, sd) + dx * (1 + 0.15 * i)
        fy = y + 50 * lw(t, 2, sd * 1.7) + dy * (1 + 0.1 * i)
        floater(c, fx, fy, s, r + 12 * lw(t, 1, sd), t, a, seed=sd)


def sky_bg(c, t, a=1.0):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#2F7FE0", a), col("#6EC3FF", a), col("#CFEFFF", a)])))
    for k in range(4):
        rr = random.Random(50 + k)
        x = (rr.uniform(0, 1200) + t * 1300 / DUR) % 1300 - 110
        cloud(c, x, rr.uniform(1300, 1500), rr.uniform(1.0, 1.6), 0.85 * a)
    c.drawCircle(860, 330, 260, paint("#ffffff", 0.25 * a, blur=60))


# ---------------- hook ----------------
def scene_hook(c, t):
    sky_bg(c, t)
    floaters_layer(c, t, 1.0)


def reticle(c, x, y, r, a):
    if a <= 0: return
    c.drawCircle(x, y, r, paint("#ffffff", a, stroke=5))
    for k in range(4):
        an = k * math.pi / 2
        c.drawLine(x + math.cos(an) * (r - 18), y + math.sin(an) * (r - 18), x + math.cos(an) * (r + 18), y + math.sin(an) * (r + 18), paint("#ffffff", a, stroke=5))


def scene_open(c, t):
    sky_bg(c, t)
    # the floater you try to look at zooms away from the reticle
    away = eio(prog(t, ZOOM - 0.15, 0.6))
    floaters_layer(c, t, 1.0, dx=-260 * away, dy=180 * away)
    ra = window(t, LOOK - 0.1, WIPE1 + 0.2, 0.2, 0.2)
    if ra > 0:
        tx, ty = FL[0][0] + 40 * lw(t, 1, 0), FL[0][1] + 50 * lw(t, 2, 0)
        rx = lerp(540, tx, eio(prog(t, LOOK, 0.5))); ry = lerp(1100, ty, eio(prog(t, LOOK, 0.5)))
        reticle(c, rx, ry, 110 + 6 * math.sin(t * 8), ra)
    ga = window(t, THERE - 0.1, LOOK, 0.15, 0.2)
    if ga > 0:
        for i, (x, y, s, r, sd) in enumerate(FL[:3]):
            fx = x + 40 * lw(t, 1, sd); fy = y + 50 * lw(t, 2, sd * 1.7)
            c.drawCircle(fx, fy, 170 * s, paint(YELLOW, 0.9 * ga, stroke=5))
    pill(c, t, "WHAT ARE THESE?", 495, 560, SKY_D, 0.35, SKYt - 0.05)
    pill(c, t, "PLAIN BRIGHT SKY", 495, 560, SKY_D, SKYt, LOOK - 0.05)
    pill(c, t, "TRY TO LOOK...", 495, 560, "#8a8f98", LOOK, ZOOM - 0.05)
    pill(c, t, "ZOOMS AWAY!", 495, 560, ORANGE, ZOOM, WIPE1 + 0.1)


# ---------------- white: inside the eye ----------------
EX, EY, ER = 520, 1000, 330


def eye_side(c, t, a, threads, clump, light, shadow):
    # eyeball side view: front (lens) on the left, back wall (retina) on the right
    c.drawCircle(EX, EY + 20, ER, paint("#000000", 0.15 * a, blur=24))
    c.drawCircle(EX, EY, ER, paint(shader=radial(EX - 60, EY - 80, ER * 1.2, [col("#ffffff", a), col("#EAF7FF", a), col(JELLY, a)], [0, 0.6, 1])))
    # retina band on the back
    c.drawArc(skia.Rect.MakeLTRB(EX - ER + 14, EY - ER + 14, EX + ER - 14, EY + ER - 14), -70, 140, False, paint(RETINA, 0.9 * a, stroke=22))
    # white of the eye wall
    c.drawCircle(EX, EY, ER, paint("#ffffff", a, stroke=16))
    c.drawCircle(EX, EY, ER + 8, paint("#C9CFD8", 0.8 * a, stroke=3))
    # cornea bump + lens at the front (left)
    c.drawArc(skia.Rect.MakeLTRB(EX - ER - 70, EY - 140, EX - ER + 130, EY + 140), 110, 140, False, paint("#9FD6FF", 0.8 * a, stroke=8))
    c.drawOval(skia.Rect.MakeLTRB(EX - ER + 50, EY - 110, EX - ER + 140, EY + 110), paint(shader=radial(EX - ER + 80, EY - 30, 120, [col("#ffffff", a), col("#CDEBFF", a)])))
    c.drawOval(skia.Rect.MakeLTRB(EX - ER + 50, EY - 110, EX - ER + 140, EY + 110), paint("#7FB8E6", a, stroke=4))
    for sy in (-1, 1):
        c.drawLine(EX - ER + 60, EY + sy * 150, EX - ER + 95, EY + sy * 112, paint(IRIS, a, stroke=16))
    # light rays from the left through the lens to the back
    if light > 0:
        for k in range(5):
            y0 = EY - 160 + k * 80
            u = eout(clamp(light * 1.3 - k * 0.06))
            x1 = lerp(-40, EX + ER - 30, u)
            yb = lerp(y0, EY + (k - 2) * 46, clamp((x1 - (EX - ER + 95)) / (2 * ER)))
            p = skia.Path(); p.moveTo(-40, y0); p.lineTo(min(x1, EX - ER + 95), y0)
            if x1 > EX - ER + 95:
                p.lineTo(x1, yb)
            c.drawPath(p, paint(LIGHT, 0.75 * a, stroke=8, blur=1.5))
            c.drawPath(p, paint(LIGHT, 0.25 * a, stroke=26, blur=10))
    # threads in the jelly that clump together
    if threads > 0:
        for k in range(9):
            rr = random.Random(70 + k)
            cx0, cy0 = EX + rr.uniform(-170, 170), EY + rr.uniform(-200, 200)
            cx1, cy1 = EX + 110 + rr.uniform(-25, 25), EY - 30 + rr.uniform(-25, 25)
            x = lerp(cx0, cx1, eio(clump)); y = lerp(cy0, cy1, eio(clump))
            p = skia.Path(); ln = lerp(110, 60, clump)
            for i in range(11):
                u = i / 10
                px = x + (u - 0.5) * ln * math.cos(rr.uniform(0, 3)) + 6 * math.sin(t * 2 + k)
                py = y + (u - 0.5) * ln + 14 * math.sin(u * 8 + k + t)
                p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
            c.drawPath(p, paint(THREAD, 0.85 * threads * a, stroke=6))
    # shadow cast onto the retina
    if shadow > 0:
        sx, sy = EX + ER - 30, EY - 28
        c.drawOval(skia.Rect.MakeLTRB(sx - 28, sy - 60, sx + 22, sy + 60), paint(SHADOW, 0.85 * shadow * a, blur=10))
        # the blocked rays (dark cone behind the clump)
        cone = skia.Path(); cone.moveTo(EX + 110, EY - 70); cone.lineTo(sx, sy - 60); cone.lineTo(sx, sy + 60); cone.lineTo(EX + 110, EY + 10); cone.close()
        c.drawPath(cone, paint(SHADOW, 0.25 * shadow * a, blur=8))


def scene_eye(c, t):
    studio_white(c)
    ga = eout(prog(t, WIPE1, 0.4))
    th = eout(prog(t, THREADS - 0.2, 0.4))
    cl = prog(t, THREADS + 0.2, 1.0)
    li = prog(t, LIGHTt - 0.1, 0.8)
    sh = eout(prog(t, SHAD - 0.1, 0.4))
    # camera: settle, then push into the retina for "you're seeing their shadows"
    z = lerp(1.2, 1.0, eio(prog(t, WIPE1, 1.0)))
    zz = eio(prog(t, NOTT - 0.1, 0.9))
    cx = lerp(495, EX + ER * 0.55, zz); cy = lerp(1000, EY - 60, zz)
    z *= lerp(1.0, 1.5, zz)
    c.save(); c.translate(495, 1000); c.scale(z, z); c.translate(-cx, -cy)
    eye_side(c, t, ga, th, cl, li, sh)
    c.restore()
    # inset: what you see = the shadow as a floater on a bright view
    ia = eback(prog(t, SHAD2 - 0.15, 0.35))
    if ia > 0:
        c.save(); c.translate(560, 1300); c.scale(0.85 * ia, 0.85 * ia)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-200, -140, 200, 140), 30, 30)
        c.drawRRect(rr, paint("#000000", 0.2, blur=14))
        c.save(); c.clipRRect(rr, doAntiAlias=True)
        c.drawRect(skia.Rect.MakeLTRB(-200, -140, 200, 140), paint(shader=linear((0, -140), (0, 140), [col("#4F9BEA"), col("#BFE6FF")])))
        floater(c, 10 * math.sin(t * 1.3), 0, 0.9, 15, t, 1.2, seed=1)
        c.restore()
        c.drawRRect(rr, paint("#ffffff", 1, stroke=5))
        f = skia.Font(TF_MONO, 22); s = "WHAT YOU SEE"
        c.drawString(s, -f.measureText(s) / 2, 175, f, paint(INK, 0.7))
        c.restore()
    f = skia.Font(TF_MONO, 24)
    la = ga * prog(t, JELLYt, 0.3) * (1 - zz)
    if la > 0:
        c.drawString("FRONT", 90, 1420, f, paint(INK, 0.5 * la))
        c.drawString("BACK OF EYE", 690, 1420, f, paint(RETINA, la))
    pill(c, t, "CLEAR JELLY", 495, 560, "#2A9ED6", JELLYt, OVER - 0.05)
    pill(c, t, "OVER TIME...", 495, 560, "#8a8f98", OVER, THREADS - 0.05)
    pill(c, t, "THREADS CLUMP", 495, 560, THREAD, THREADS, LIGHTt - 0.05)
    pill(c, t, "LIGHT IN", 495, 560, "#C9A100", LIGHTt, SHAD - 0.05, text_col="#FFFFFF")
    pill(c, t, "SHADOWS!", 495, 560, SHADOW, SHAD, NOTT - 0.05)
    pill(c, t, "NOT THE THREADS", 495, 560, "#8a8f98", NOTT, SHAD2 - 0.05)
    pill(c, t, "THEIR SHADOWS", 495, 560, SHADOW, SHAD2, WIPE2 + 0.1)


# ---------------- dark: eye moves, common, warning ----------------
def front_eye(c, t, x, y, s, gaze, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    e = skia.Path(); e.moveTo(-300, 0); e.cubicTo(-160, -200, 160, -200, 300, 0); e.cubicTo(160, 180, -160, 180, -300, 0); e.close()
    c.drawOval(skia.Rect.MakeLTRB(-420, -300, 420, 280), paint(shader=radial(0, -20, 440, [col("#F1BE9B", a), col("#D99C76", a), col("#B97B57", a)], [0, 0.7, 1])))
    c.drawPath(e, paint(shader=radial(0, 0, 300, [col("#ffffff", a), col("#EDE7E3", a), col("#cfc5bf", a)], [0, 0.7, 1])))
    c.save(); c.clipPath(e)
    gx = gaze * 150
    c.drawCircle(gx, 0, 110, paint(shader=radial(gx, 0, 110, [col("#2c5f55", a), col(IRIS, a), col("#1d3d36", a)], [0, 0.7, 1])))
    c.drawCircle(gx, 0, 48, paint("#0d0806", a))
    c.drawCircle(gx - 34, -40, 20, paint("#ffffff", 0.9 * a))
    c.restore()
    c.drawPath(e, paint("#8a4f33", 0.9 * a, stroke=8))
    for k in range(9):
        u = (k + 0.5) / 9
        xx = lerp(-230, 230, u); yy = -170 * math.sin(math.pi * (0.12 + 0.76 * u)) * 0.98
        c.drawLine(xx, yy, xx * 1.12, yy - 50, paint("#2a1a12", a, stroke=6))
    c.restore()


def gaze_at(t):
    # look left - right - left (eye moves), floaters follow with a lag
    return 0.8 * math.sin((t - WIPE2) * 2.4)


def scene_move(c, t):
    bg_dark(c, t)
    a = eout(prog(t, WIPE2, 0.4))
    out = prog(t, COMMON - 0.25, 0.3)
    g = gaze_at(t)
    gl = gaze_at(t - 0.35)
    # view panel (what you see) above the eye
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(110, 650, 880, 1060), 34, 34)
    c.drawRRect(rr, paint("#000000", 0.3 * a, blur=16))
    c.save(); c.clipRRect(rr, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeLTRB(110, 650, 880, 1060), paint(shader=linear((0, 650), (0, 1060), [col("#3D8BEA", a), col("#BFE6FF", a)])))
    for i in range(3):
        floater(c, 330 + i * 170 + 220 * gl + 30 * lw(t, 1, i), 820 + i * 50, 0.7, 10 + 20 * i, t, a * 1.1, seed=i)
    c.restore()
    c.drawRRect(rr, paint("#ffffff", 0.5 * a, stroke=3))
    front_eye(c, t, 495, 1260, 0.62, g, a)
    for sx in (-1, 1):
        if (g - gaze_at(t - 0.05)) * sx > 0.002:
            p = skia.Path(); p.moveTo(495 + sx * 230, 1260); p.lineTo(495 + sx * 300, 1260)
            c.drawPath(p, paint(ORANGE, 0.8 * a, stroke=10))
    pill(c, t, "EYE MOVES", 495, 560, IRIS, MOVES, DART - 0.05)
    pill(c, t, "THEY TAG ALONG", 495, 560, ORANGE, DART, COMMON - 0.1)


def scene_common(c, t):
    bg_dark(c, t)
    a = eout(prog(t, COMMON - 0.25, 0.35))
    # rows of little people, more lit up after 50
    lit2 = eio(prog(t, FIFTY - 0.1, 0.6))
    for r in range(4):
        for k in range(7):
            x = 175 + k * 110; y = 760 + r * 140
            q = eback(prog(t, COMMON - 0.25 + (r * 7 + k) * 0.012, 0.3))
            if q <= 0: continue
            on = (r * 7 + k) % 3 == 0 or (lit2 > 0 and (r * 7 + k) % 3 == 1 and r >= 1)
            cc = THREAD if on else "#5a5d6a"
            if (r * 7 + k) % 3 == 1 and r >= 1:
                cc = mixhex("#5a5d6a", THREAD, lit2)
            c.save(); c.translate(x, y); c.scale(q, q)
            c.drawCircle(0, -40, 22, paint(cc, a))
            c.drawRoundRect(skia.Rect.MakeLTRB(-30, -12, 30, 50), 22, 22, paint(cc, a))
            c.restore()
    na = eback(prog(t, FIFTY - 0.1, 0.35))
    if na > 0:
        big_number(c, "50+", "", 495, 1420, 150, "#ffffff", clamp(na), pulse=clamp(na, 0, 1.1))
    pill(c, t, "SUPER COMMON", 495, 560, GREEN, COMMON, FIFTY - 0.05, text_col="#FFFFFF")
    pill(c, t, "MORE AFTER 50", 495, 560, THREAD, FIFTY, SUDDEN - 0.1)


def warn_card(c, t, x, y, kind, a, hl):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    rect = skia.Rect.MakeLTRB(-125, -170, 125, 170)
    c.drawRoundRect(rect, 30, 30, paint("#000000", 0.3, blur=14))
    c.drawRoundRect(rect, 30, 30, paint("#25222a"))
    c.drawRoundRect(rect, 30, 30, paint(mixhex("#4a4652", RED, hl), 1, stroke=3 + 2 * hl))
    view = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-95, -140, 95, 60), 22, 22)
    c.save(); c.clipRRect(view, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeLTRB(-95, -140, 95, 60), paint(shader=linear((0, -140), (0, 60), [col("#4F9BEA"), col("#BFE6FF")])))
    if kind == "shower":
        for k in range(26):
            rr = random.Random(k)
            px = rr.uniform(-90, 90); py = ((rr.uniform(-140, 60) + t * 60 * rr.uniform(0.5, 1.5)) % 200) - 140
            c.drawCircle(px, py, rr.uniform(3, 7), paint("#1d2a44", 0.55))
    elif kind == "flash":
        fl = max(0, math.sin(t * 9)) ** 6
        c.drawRect(skia.Rect.MakeLTRB(-95, -140, 95, 60), paint("#ffffff", 0.8 * fl))
        z = skia.Path(); z.moveTo(10, -120); z.lineTo(-30, -30); z.lineTo(5, -30); z.lineTo(-20, 40); z.lineTo(40, -50); z.lineTo(5, -50); z.lineTo(30, -120); z.close()
        c.drawPath(z, paint(LIGHT, 0.6 + 0.4 * fl))
    else:
        u = 0.5 + 0.12 * math.sin(t * 1.5)
        c.drawRect(skia.Rect.MakeLTRB(-95, -140, 95, lerp(-140, 60, u)), paint("#141218", 0.92))
        c.drawLine(-95, lerp(-140, 60, u), 95, lerp(-140, 60, u), paint("#000000", 0.6, stroke=10, blur=6))
    c.restore()
    c.drawRRect(view, paint("#ffffff", 0.4, stroke=2))
    f = skia.Font(TF_MONO, 24)
    lab = {"shower": "NEW SHOWER", "flash": "FLASHES", "curtain": "DARK CURTAIN"}[kind]
    c.drawString(lab, -f.measureText(lab) / 2, 125, f, paint(mixhex("#ffffff", RED, hl * 0.6)))
    c.restore()


def scene_warn(c, t):
    bg_dark(c, t)
    c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.05 * (0.5 + 0.5 * math.sin(t * 4))))
    for x, y, kind, tin in ((225, 850, "shower", SUDDEN), (495, 1170, "flash", FLASH), (765, 850, "curtain", CURTAIN)):
        q = eback(prog(t, tin - 0.15, 0.35))
        warn_card(c, t, x, y, kind, clamp(q, 0, 1.2), eout(prog(t, tin, 0.3)) * (1 - 0.5 * prog(t, FAST, 0.3)))
    da = eback(prog(t, FAST - 0.1, 0.35))
    if da > 0:
        c.save(); c.translate(495, 640); c.scale(da, da)
        c.restore()
    pill(c, t, "SUDDEN NEW ONES", 495, 560, RED, SUDDEN, p0(20) - 0.05)
    pill(c, t, "SEE AN EYE DOCTOR FAST", 495, 560, RED, p0(20), SO + 0.3)
    footnote(c, t, "Educational only, not medical advice.", SUDDEN - 0.2, SO + 0.4)


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_eye(c, t); return
    if t < COMMON - 0.25:
        scene_move(c, t); return
    if t < SUDDEN - 0.25:
        scene_common(c, t)
        q = 1 - prog(t, COMMON - 0.25, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_move(c, t); c.restore()
        return
    if t < SO - 0.05:
        scene_warn(c, t)
        q = 1 - prog(t, SUDDEN - 0.25, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_common(c, t); c.restore()
        return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_warn(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.022 * (1 - d / 0.25) ** 2
    return s



def split_long(PH, maxw=9):
    """caption-only: split phrases longer than maxw words in two so captions never wrap to 3 lines."""
    out = []
    for p in PH:
        ws = p["words"]
        if len(ws) <= maxw:
            out.append(p); continue
        k = (len(ws) + 1) // 2
        out.append(dict(p, words=ws[:k], t1=ws[k - 1]["t1"]))
        out.append(dict(p, words=ws[k:], t0=ws[k]["t0"]))
    return out

KWCOL = {"floating": SKY, "sky": SKY, "zooms": ORANGE, "jelly": "#2A9ED6", "threads": THREAD,
         "shadows": THREAD, "moves": IRIS, "dart": ORANGE, "common": GREEN, "50": THREAD, "sudden": RED,
         "flashes": RED, "curtain": RED, "fast": RED}
CAPS = Captions(split_long(P), KWCOL, {"zooms", "shadows!"}, DUR)


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
    wipe(c, t, WIPE1, WL, SKY, "#F4F2EE")
    wipe(c, t, WIPE2, WL, THREAD, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("pop", SKYt), ("pop", THERE), ("whoosh", LOOK), ("hit", ZOOM),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", JELLYt), ("pop", THREADS), ("riser", LIGHTt - 0.1),
          ("hit", SHAD), ("whoosh", NOTT - 0.1), ("pop", SHAD2), ("whoosh", WIPE2), ("pop", MOVES), ("pop", DART),
          ("whoosh", COMMON - 0.25), ("pop", COMMON), ("pop", FIFTY), ("whoosh", SUDDEN - 0.25), ("hit", SUDDEN),
          ("pop", FLASH), ("pop", CURTAIN), ("ding", FAST), ("whoosh", SO - 0.05)]
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

# HIW04 — "What is this?" (dandruff). Sources:
#  ~50% of adults: dermatology reviews (Wikipedia/Dandruff; J Clin Investig Dermatol review)
#  Malassezia globosa on nearly every scalp, eats sebum, releases oleic acid: Dawson 2007 J Investig Dermatol Symp Proc
#  scalp cells ~1 month normally, ~1 week (2–7 days) with dandruff: Kligman et al., J Soc Cosmet Chem; reviews
#  a 2 mm flake can hold thousands of cells: J Soc Cosmet Chem v27
#  not caused by poor hygiene; zinc pyrithione / ketoconazole / selenium sulfide, leave on 5–10 min: AAD
#  bacteria may matter too (2016 study): still debated
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
TONE = os.environ.get("TONE", "#D7A47E")
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
LIME = "#B7F34A"; LIME_INK = "#5E8F0E"
TONE_DARK = mixhex(TONE, "#3a2418", 0.38); TONE_LIGHT = mixhex(TONE, "#ffffff", 0.28)


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


# ---------------- beats (phrase indices from timings) ----------------
REVEAL = p0(1); HAIR = kw(3); SKIN = p0(4); THOUS = p0(5); TOGETHER = kw(6)
SCALP = p0(7) - 0.15; ALLTIME = p0(8); MONTH = kw(9); FALLS = p0(11); SEE = kw(12)
HALF = p0(13) - 0.1; SPEEDS = p0(14)
YEAST = p0(15) - 0.15; EVERY = kw(16); OIL = kw(17); ACID = kw(18)
OVER = p0(19) - 0.1; WEEK = kw(20); CLUMPS = kw(21)
WIPE1 = p0(22) - 0.3; WASH = kw(22); NOTEX = kw(23); HYG = p0(24); SHAMPOO = p0(25); FIVE = kw(26)
WIPE2 = p0(27) - 0.3; BACT = kw(27); PART = p0(28); SO = p0(29)
WL = 0.32
IMPACTS = [NOTEX, CLUMPS]


def mode_at(t):
    if t < SKIN - 0.15: return "flake_out"      # macro flake -> zoom out to hair
    if t < SCALP: return "cells"                # zoom into flake mosaic
    if t < HALF: return "block"                 # scalp cross-section, normal month
    if t < YEAST: return "heads"                # 1 in 2 adults
    if t < OVER: return "yeast"                 # surface macro: yeast, oil, acid
    if t < WIPE1 + WL / 2: return "block2"      # overreact, week, clumps
    if t < WIPE2 + WL / 2: return "white"       # washing? not exactly, shampoo, timer
    if t < PART + 0.1: return "bact"            # bacteria
    return "end"                                # back to frame 1 (loop)


rnd = random.Random(21)


def make_flake(seed, n=70, R=300):
    r = random.Random(seed)
    outline = []
    for k in range(28):
        a = k / 28 * 2 * math.pi
        rr = R * (0.72 + 0.28 * r.random()) * (1 + 0.25 * math.cos(2 * a + 0.6))
        outline.append((rr * math.cos(a), rr * 0.72 * math.sin(a)))
    cells = []
    for _ in range(n):
        x, y = r.uniform(-R, R), r.uniform(-R * 0.8, R * 0.8)
        s = r.uniform(46, 78); rot = r.uniform(0, 180)
        pts = [(s * (0.8 + 0.3 * r.random()) * math.cos(math.radians(rot + j * 60 + r.uniform(-10, 10))),
                s * (0.8 + 0.3 * r.random()) * math.sin(math.radians(rot + j * 60 + r.uniform(-10, 10)))) for j in range(6)]
        cells.append((x, y, pts, r.random()))
    return outline, cells


FLAKE = make_flake(4)
SMALL_FLAKES = [make_flake(10 + i, 22, 60) for i in range(7)]


def smooth_path(pts):
    p = skia.Path(); n = len(pts)
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    p.moveTo(*mids[-1])
    for i in range(n):
        p.quadTo(pts[i][0], pts[i][1], mids[i][0], mids[i][1])
    p.close()
    return p


def draw_flake(c, x, y, s, rot, flake, a=1.0, detail=1.0, glow=True):
    outline, cells = flake
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    op = smooth_path(outline)
    if glow:
        c.drawPath(op, paint("#ffffff", 0.18 * a, blur=26))
    c.save(); c.clipPath(op)
    c.drawPath(op, paint("#EDEBE4", 0.55 * a))
    for (cx, cy, pts, r) in cells:
        pp = skia.Path(); pp.moveTo(cx + pts[0][0], cy + pts[0][1])
        for q in pts[1:]:
            pp.lineTo(cx + q[0], cy + q[1])
        pp.close()
        c.drawPath(pp, paint(mixhex("#FFFFFF", "#D9D2C2", r), 0.5 * a))
        if detail > 0:
            c.drawPath(pp, paint("#9d9584", 0.55 * a * detail, stroke=2.2 / max(s, 0.3)))
            c.drawCircle(cx + 4, cy - 3, 4.5, paint("#b8ae99", 0.35 * a * detail))
    c.restore()
    c.drawPath(op, paint("#ffffff", 0.7 * a, stroke=2.5 / max(s, 0.3)))
    c.restore()


def dark_bg(c, t, tint="#121012"):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.48, 1300, [col("#221e20"), col(tint), col("#070607")], [0, 0.5, 1])))


# ---- hair strands scene ----
STRANDS = []
for i in range(9):
    x0 = -200 + i * 170 + rnd.uniform(-40, 40)
    STRANDS.append((x0, rnd.uniform(-0.5, 0.5), rnd.uniform(9, 14), rnd.uniform(0, 6.28)))
STUCK = [(rnd.uniform(120, 960), rnd.uniform(520, 1480), rnd.uniform(0.35, 0.7), rnd.uniform(0, 360), i % 7) for i in range(14)]


def hair_scene(c, t, a, hair_hi=0.0):
    for k, (x0, bend, w, ph) in enumerate(STRANDS):
        p = skia.Path(); p.moveTo(x0, -100)
        p.cubicTo(x0 + 300 * bend, 600, x0 - 260 * bend + 40 * math.sin(t * 0.6 + ph), 1200, x0 + 120 * bend, 2050)
        hi = hair_hi if k == 4 else 0
        c.drawPath(p, paint("#000000", 0.4 * a, stroke=w + 8, blur=8))
        c.drawPath(p, paint(mixhex("#3b2416", "#5a3a26", 0.4), a, stroke=w))
        c.drawPath(p, paint("#a9805f", 0.45 * a, stroke=w * 0.25))
        if hi > 0:
            c.drawPath(p, paint(RED, 0.8 * hi * a, stroke=w + 8, blur=3))
    for (x, y, s, rot, fi) in STUCK:
        draw_flake(c, x + 6 * math.sin(t + x), y, s, rot + 5 * math.sin(t * 0.7 + y), SMALL_FLAKES[fi], a, detail=0.6)


def macro_flake_pose(t):
    # periodic in DUR so the last frame == the first frame (perfect loop)
    ph = 2 * math.pi * t / DUR
    return 540 + 10 * math.sin(ph), 1000 + 8 * math.sin(ph * 2), 2.05 + 0.04 * math.sin(ph), 8 * math.sin(ph)


def draw_macro(c, t, a=1.0, box=1.0):
    dark_bg(c, t)
    # out-of-focus fibres in the background
    for k in range(6):
        y = 300 + k * 280
        c.drawLine(-50, y + 80 * math.sin(k), W + 50, y - 60 * math.cos(k), paint("#4a3022", 0.35 * a, stroke=30, blur=18))
    x, y, s, rot = macro_flake_pose(t)
    draw_flake(c, x, y, s * 0.5, rot, FLAKE, a)
    if box > 0:
        r = skia.Rect.MakeLTRB(x - 330, y - 260, x + 330, y + 260)
        c.drawRect(r, paint("#ffffff", 0.05 * box))
        c.drawPath(skia.Path().addRect(r), paint("#ffffff", box, stroke=2.5))
        for qx, qy in ((r.left(), r.top()), (r.right(), r.top()), (r.left(), r.bottom()), (r.right(), r.bottom())):
            c.drawCircle(qx, qy, 8, paint("#ffffff", box)); c.drawCircle(qx, qy, 8, paint("#7aa2ff", box, stroke=2))
        f = skia.Font(TF_MONO, 26)
        c.drawString("?", r.right() - 26, r.top() - 14, skia.Font(TF_BLACK, 40), paint("#ffffff", box))


def scene_flake_out(c, t):
    z = eio(prog(t, REVEAL - 0.1, 0.6))           # zoom out to hair
    if z < 1:
        c.save(); c.translate(540, 1000); c.scale(lerp(1, 0.18, z), lerp(1, 0.18, z)); c.translate(-540, -1000)
        draw_macro(c, t, 1, box=1 - prog(t, REVEAL - 0.1, 0.2))
        c.restore()
    if z > 0:
        c.saveLayerAlpha(None, int(255 * clamp(z * 1.6)))
        if z < 1:
            dark_bg(c, t)
        c.save(); c.translate(540, 1000); c.scale(lerp(2.4, 1.0, z), lerp(2.4, 1.0, z)); c.translate(-540, -1000)
        if z >= 1:
            dark_bg(c, t)
        hair_scene(c, t, 1, hair_hi=window(t, HAIR, SKIN, 0.2, 0.2))
        draw_flake(c, 540, 1000, 0.36, macro_flake_pose(t)[3], FLAKE, 1, detail=0.6)
        c.restore()
        c.restore()
    pill(c, t, "DANDRUFF", 540, 820, "#FFFFFF", REVEAL + 0.1, HAIR, anchor=(540, 950))
    pill(c, t, "NOT HAIR", 760, 700, RED, HAIR + 0.1, SKIN, anchor=(650, 800))
    footnote(c, t, "Magnified illustration", REVEAL + 0.2, SKIN)


def scene_cells(c, t):
    dark_bg(c, t)
    z = eio(prog(t, SKIN - 0.15, 0.6))
    s = lerp(0.36, 1.25, z) * (1 + 0.04 * prog(t, SKIN, SCALP - SKIN))
    draw_flake(c, 540, 1000, s, macro_flake_pose(t)[3] * 0.5, FLAKE, 1, detail=1)
    # count cells popping
    if t > THOUS:
        outline, cells = FLAKE
        for i, (cx, cy, pts, r) in enumerate(cells[:40]):
            q = eback(prog(t, THOUS + i * 0.025, 0.2))
            if q > 0:
                c.drawCircle(540 + cx * s, 1000 + cy * s * 1.0, 7 * q, paint("#ffffff", 0.9 * (1 - prog(t, TOGETHER, 0.4))))
    if t > TOGETHER - 0.1:
        g = eout(prog(t, TOGETHER - 0.1, 0.4))
        outline, cells = FLAKE
        c.save(); c.translate(540, 1000); c.scale(s, s)
        for (cx, cy, pts, r) in cells[:30]:
            c.drawCircle(cx, cy, 30, paint(YELLOW, 0.18 * g, blur=8))
        c.restore()
    big_number(c, "1,000s", "OF CELLS", 540, 1470, 120, "#FFFFFF", eout(prog(t, THOUS, 0.3)) * (1 - prog(t, SCALP - 0.3, 0.3)))
    pill(c, t, "DEAD SKIN CELLS", 540, 640, "#F4F2EE", SKIN + 0.1, SCALP)
    pill(c, t, "GLUED BY OIL", 800, 760, YELLOW, TOGETHER, SCALP)
    footnote(c, t, "A 2 mm flake can hold thousands of cells", THOUS, SCALP)


# ---------------- scalp block ----------------
FW, TOPY, BOTY = 400, -230, 330
DX, DY = 70, -120
SKIN_IMG = None


def skin_img():
    global SKIN_IMG
    if SKIN_IMG is None:
        SKIN_IMG = skia.Image.open(f"{D}/skin_{TONE[1:]}.png")
    return SKIN_IMG


COLS = 13


def block(c, t, cx, cy, s, speed, inflame=0.0, clumps=0.0, hi_cell=None, sheds=1.0):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-FW - 30, BOTY - 30, FW + DX + 60, BOTY + 50), paint("#000000", 0.45, blur=26))
    def side(y0, y1, colr):
        p = skia.Path(); p.moveTo(FW, y0); p.lineTo(FW + DX, y0 + DY); p.lineTo(FW + DX, y1 + DY); p.lineTo(FW, y1); p.close()
        c.drawPath(p, paint(colr))
    side(TOPY, 40, mixhex(TONE, "#000000", 0.35)); side(40, BOTY, mixhex("#E3BFAA", "#000000", 0.3))
    top = skia.Path(); top.moveTo(-FW, TOPY); top.lineTo(FW, TOPY); top.lineTo(FW + DX, TOPY + DY); top.lineTo(-FW + DX, TOPY + DY); top.close()
    m = skia.Matrix(); m.setAll(0.6, -0.07 * 0.42, -FW + DX, 0, 0.3, TOPY + DY, 0, 0, 1)
    c.drawPath(top, paint(shader=skin_img().makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, SAMP, m)))
    if inflame > 0:
        c.drawPath(top, paint(RED, 0.35 * inflame))
    # dermis
    c.drawRect(skia.Rect.MakeLTRB(-FW, 40, FW, BOTY), paint(shader=linear((0, 40), (0, BOTY), [col("#E8C2AE"), col("#DDB49D")])))
    for k in range(5):
        p = skia.Path(); y = 80 + k * 50; p.moveTo(-FW, y)
        for xx in range(-FW, FW + 1, 40):
            p.lineTo(xx, y + 8 * math.sin(xx / 55 + k * 1.7))
        c.drawPath(p, paint("#c99a86", 0.35, stroke=1.6))
    # epidermis: columns of cells travelling up
    c.drawRect(skia.Rect.MakeLTRB(-FW, TOPY, FW, 40), paint(mixhex(TONE, "#f3d9c6", 0.45)))
    c.save(); c.clipRect(skia.Rect.MakeLTRB(-FW, TOPY, FW, 40))
    H_EP = 40 - TOPY
    cw = 2 * FW / COLS
    for col_i in range(COLS):
        for row in range(6):
            u = ((row / 6) + speed + col_i * 0.037) % 1        # 0 bottom -> 1 top
            y = 40 - u * H_EP
            flat = u ** 2
            h = lerp(34, 8, flat); w = cw * lerp(0.8, 1.02, flat)
            colr = mixhex(mixhex(TONE, "#f0c9b0", 0.3), "#F3EFE6", flat)
            x = -FW + col_i * cw + cw / 2
            c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 8, 8, paint(colr, 0.95))
            c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 8, 8, paint(TONE_DARK, 0.35, stroke=1.4))
            if flat < 0.3:
                c.drawCircle(x, y, 5, paint(TONE_DARK, 0.5))
    if hi_cell is not None:
        u = hi_cell
        y = 40 - u * H_EP; x = -FW + 6 * cw + cw / 2
        h = lerp(34, 8, u ** 2)
        c.drawRoundRect(skia.Rect.MakeXYWH(x - cw * 0.5, y - h / 2, cw, h), 8, 8, paint(LIME, 0.95))
    c.restore()
    if inflame > 0:
        c.drawRect(skia.Rect.MakeLTRB(-FW, TOPY, FW, 40), paint(shader=linear((0, TOPY), (0, 40), [col(RED, 0.35 * inflame), col(RED, 0.05 * inflame)])))
    # hair follicles + shafts
    for hx in (-250, 20, 260):
        c.drawRoundRect(skia.Rect.MakeLTRB(hx - 16, TOPY - 2, hx + 16, 230), 16, 16, paint(mixhex(TONE, "#7a5444", 0.5)))
        c.drawCircle(hx + 34, 150, 22, paint("#F6D271")); c.drawCircle(hx - 34, 160, 18, paint("#F6D271"))
        p = skia.Path(); p.moveTo(hx, 220); p.lineTo(hx, TOPY); p.cubicTo(hx + 10, TOPY - 220, hx + 60, TOPY - 360, hx + 40, TOPY - 520)
        c.drawPath(p, paint("#3b2416", 1, stroke=12)); c.drawPath(p, paint("#a9805f", 0.4, stroke=3))
    c.drawRect(skia.Rect.MakeLTRB(-FW, TOPY, FW, BOTY), paint(shader=linear((-FW, 0), (FW, 0), [col("#ffffff", 0.06), col("#000000", 0), col("#000000", 0.16)])))
    # shedding: invisible specks (normal) or clumps (dandruff)
    for k in range(18):
        u = (t * 0.35 + k / 18) % 1
        x = -FW + 40 + (k * 97) % (2 * FW - 60) + 30 * math.sin(t + k)
        y = TOPY - 10 - u * 300
        a = sheds * (1 - u)
        c.drawCircle(x + DX * 0.3, y + DY * 0.3, 2.2, paint("#ffffff", 0.6 * a))
    if clumps > 0:
        for k in range(7):
            u = clamp(clumps * 1.2 - k * 0.06)
            x = -FW + 80 + k * 110
            y = TOPY - 20 - eout(u) * (260 + 60 * (k % 3))
            draw_flake(c, x + DX * 0.3, y + DY * 0.3, 0.32, k * 40 + 60 * u, SMALL_FLAKES[k % 7], clamp(u * 4), detail=0.5, glow=False)
    c.restore()


def scene_block(c, t, second=False):
    studio_dark(c)
    if not second:
        settle = eout(prog(t, SCALP, 0.6))
        s = lerp(1.25, 1.0, settle) * (1 + 0.03 * prog(t, SCALP, HALF - SCALP))
        speed = (t - SCALP) * 0.06
        hi = None
        if MONTH - 0.2 < t < SEE + 0.8:
            hi = clamp((t - (MONTH - 0.2)) / (FALLS - MONTH + 0.6))
        block(c, t, 500, 1100, s, speed, hi_cell=hi, sheds=1.0 - 0.6 * prog(t, SEE, 0.4) * 0 + 0)
        pill(c, t, "SCALP SKIN", 300, 650, TONE_LIGHT, SCALP + 0.2, MONTH)
        pill(c, t, "1 CELL", 800, 650, LIME, MONTH, SEE + 0.6, anchor=(500 + (-FW + 6.5 * 800 / 13) * s, 1100 + (-100) * s))
        pill(c, t, "TOO SMALL TO SEE", 540, 560, "#FFFFFF", SEE, HALF)
        footnote(c, t, "Normal scalp: ~1 month from bottom to top", MONTH, HALF)
    else:
        s = 1.0 + 0.04 * prog(t, OVER, WIPE1 - OVER)
        fast = eio(prog(t, WEEK - 0.2, 0.6))
        speed = (t - OVER) * lerp(0.08, 0.5, fast)
        block(c, t, 500, 1100, s, speed, inflame=eout(prog(t, OVER, 0.5)), clumps=prog(t, CLUMPS - 0.1, 1.2), sheds=0.6)
        pill(c, t, "IRRITATED", 300, 650, RED, OVER + 0.1, WIPE1 + 0.1)
        pill(c, t, "CLUMPS", 800, 600, "#FFFFFF", CLUMPS, WIPE1 + 0.1)
        footnote(c, t, "With dandruff: ~1 week (2–7 days)", WEEK, WIPE1)


HEADS = [(150 + (i % 5) * 195, 860 + (i // 5) * 380) for i in range(10)]


def scene_heads(c, t):
    dark_bg(c, t)
    for i, (x, y) in enumerate(HEADS):
        q = eback(prog(t, HALF + i * 0.05, 0.3))
        hl = eout(prog(t, HALF + 0.6 + (i % 5) * 0.07, 0.3)) if i in (0, 2, 4, 6, 8) else 0
        c.save(); c.translate(x, y); c.scale(q, q)
        colr = mixhex("#5a5558", "#F4F2EE", hl)
        c.drawCircle(0, -70, 58, paint(colr))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-82, 0, 82, 120), 60, 60), paint(colr))
        if hl > 0:
            for k in range(7):
                c.drawCircle(-50 + k * 17, 6 + (k % 2) * 10, 4, paint("#ffffff", hl))
            c.drawCircle(0, -70, 70, paint(LIME, 0.25 * hl, blur=10))
        c.restore()
    if t > SPEEDS:
        sp = (t - SPEEDS) * 2.5
        for k in range(3):
            x = 540 + ((sp * 300 + k * 140) % 600) - 300
            c.drawPath(chevron(x, 1560 - 160, 26), paint(LIME, 0.9 * prog(t, SPEEDS, 0.2)))
    big_number(c, "1 IN 2", "ADULTS", 540, 700, 120, "#FFFFFF", eout(prog(t, HALF + 0.2, 0.3)))
    footnote(c, t, "≈50% of adults · dermatology reviews", HALF + 0.3, YEAST)


def chevron(x, y, s):
    p = skia.Path(); p.moveTo(x - s, y - s); p.lineTo(x + s * 0.4, y); p.lineTo(x - s, y + s); p.lineTo(x - s * 0.5, y); p.close()
    return p


YEASTS = [(rnd.uniform(140, 940), rnd.uniform(620, 1420), rnd.uniform(0.8, 1.2), rnd.uniform(0, 360)) for _ in range(16)]
OILS = [(rnd.uniform(140, 940), rnd.uniform(620, 1420), rnd.uniform(10, 22)) for _ in range(14)]


def yeast_cell(c, x, y, s, rot, a, t):
    c.save(); c.translate(x, y); c.rotate(rot + 6 * math.sin(t * 1.5 + x)); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-30, -22, 30, 22), paint(shader=radial(-10, -8, 40, [col("#E6FFB0", a), col(LIME, a), col("#6E9E1C", a)], [0, 0.5, 1])))
    c.drawOval(skia.Rect.MakeLTRB(24, -11, 46, 11), paint(shader=radial(32, -4, 16, [col("#E6FFB0", a), col(LIME, a)])))
    c.drawOval(skia.Rect.MakeLTRB(-30, -22, 30, 22), paint("#4d7410", 0.6 * a, stroke=2))
    c.restore()


def scene_yeast(c, t):
    push = lerp(1.3, 1.0, eout(prog(t, YEAST, 0.6)))
    c.save(); c.translate(540, 1000); c.scale(push, push); c.translate(-540, -1000)
    c.drawImageRect(skin_img(), skia.Rect.MakeXYWH(-150, -200, 1380, 2400), SAMP)
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(540, 1000, 1100, [col("#000000", 0.05), col("#000000", 0.6)])))
    eat = prog(t, OIL, 1.4)
    for i, (x, y, r) in enumerate(OILS):
        a = eout(prog(t, OIL - 0.3 + i * 0.03, 0.3)) * (1 - prog(t, ACID + i * 0.05, 0.5))
        if a > 0:
            c.drawCircle(x, y, r, paint(shader=radial(x - r * 0.3, y - r * 0.3, r * 1.3, [col("#FFF7CF", a), col(YELLOW, a), col("#D9A12B", a)], [0, 0.5, 1])))
            c.drawCircle(x - r * 0.35, y - r * 0.4, r * 0.25, paint("#ffffff", 0.8 * a))
    for i, (x, y, s, rot) in enumerate(YEASTS):
        q = eback(prog(t, YEAST + 0.1 + (i % 6) * 0.05, 0.3)) if i < 6 else eback(prog(t, EVERY + (i - 6) * 0.04, 0.3))
        if q <= 0:
            continue
        ox, oy, _ = OILS[i % len(OILS)]
        xx = lerp(x, ox + 30, eat * 0.6); yy = lerp(y, oy, eat * 0.6)
        yeast_cell(c, xx, yy, s * q, rot, clamp(q), t)
        if t > ACID:
            for k in range(4):
                u = ((t - ACID) * 0.8 + k / 4 + i * 0.13) % 1
                ax = xx + 20 + u * 70 * math.cos(i + k); ay = yy - u * 90
                c.drawCircle(ax, ay, 6 * (1 - u * 0.5), paint("#FF7A3D", 0.85 * (1 - u) * prog(t, ACID, 0.3)))
    c.restore()
    pill(c, t, "MALASSEZIA YEAST", 540, 560, LIME, YEAST + 0.2, OIL)
    pill(c, t, "ON EVERYONE", 820, 650, "#FFFFFF", EVERY, OIL)
    pill(c, t, "SCALP OIL", 300, 650, YELLOW, OIL, OVER)
    pill(c, t, "OLEIC ACID", 780, 650, "#FF7A3D", ACID, OVER)
    footnote(c, t, "Malassezia globosa · lives on nearly everyone's scalp", YEAST + 0.2, OVER)


def shower(c, t, x, y, a):
    c.drawLine(x + 120, y - 160, x + 30, y - 40, paint("#9aa1ad", a, stroke=16))
    c.drawOval(skia.Rect.MakeLTRB(x - 120, y - 50, x + 120, y + 30), paint("#c6ccd6", a))
    c.drawOval(skia.Rect.MakeLTRB(x - 120, y - 50, x + 120, y + 30), paint("#8a909c", a, stroke=3))
    for k in range(16):
        u = (t * 1.6 + k / 16) % 1
        xx = x - 100 + (k * 53) % 200 + u * 30 * math.sin(k)
        yy = y + 30 + u * 360
        c.drawLine(xx, yy, xx + 2, yy + 26, paint("#8fb3ef", a * (1 - u), stroke=4))


def bottle(c, t, x, y, a, foam):
    c.save(); c.translate(x, y)
    c.drawOval(skia.Rect.MakeLTRB(-150, 330, 150, 370), paint("#000000", 0.18 * a, blur=14))
    body = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-130, -180, 130, 350), 60, 60)
    c.drawRRect(body, paint(shader=linear((-130, 0), (130, 0), [col("#e4e7ec", a), col("#ffffff", a), col("#d5d9e0", a)], [0, 0.4, 1])))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-60, -260, 60, -170), 18, 18), paint("#2d3036", a))
    c.drawRect(skia.Rect.MakeLTRB(-130, 20, 130, 170), paint(LIME, 0.9 * a))
    f = skia.Font(TF_MONO, 30); s_ = "ANTI-YEAST"
    c.drawString(s_, -f.measureText(s_) / 2, 108, f, paint(INK, a))
    c.drawRRect(body, paint("#9aa1ad", 0.8 * a, stroke=3))
    c.restore()
    for k in range(12):
        q = eback(prog(t, foam + k * 0.05, 0.3))
        if q > 0:
            bx = x - 120 + (k * 47) % 240; by = y - 300 - (k % 3) * 30
            c.drawCircle(bx, by, 22 * q, paint("#ffffff", 0.9)); c.drawCircle(bx, by, 22 * q, paint("#cfd6e0", 0.9, stroke=2))


def timer_ring(c, t, x, y, a):
    q = prog(t, FIVE, 1.4)
    c.drawCircle(x, y, 110, paint(INK, 0.08 * a, stroke=18))
    arc = skia.Path(); arc.addArc(skia.Rect.MakeLTRB(x - 110, y - 110, x + 110, y + 110), -90, 360 * eio(q))
    c.drawPath(arc, paint(LIME_INK, a, stroke=18))
    secs = int(300 * (1 - eio(q)))
    s_ = f"{secs // 60}:{secs % 60:02d}"
    f = skia.Font(TF_BLACK, 64)
    c.drawString(s_, x - f.measureText(s_) / 2, y + 22, f, paint(INK, a))


def scene_white(c, t):
    studio_white(c)
    sa = window(t, WIPE1, SHAMPOO + 0.1, 0.2, 0.35)
    if sa > 0:
        shower(c, t, 540, 820, sa)
        f = skia.Font(TF_BLACK, 220)
        qa = eback(prog(t, WASH, 0.3)) * (1 - prog(t, NOTEX, 0.2))
        if qa > 0:
            c.drawString("?", 540 - f.measureText("?") / 2, 1420, f, paint(INK, clamp(qa)))
        xa = eout(prog(t, NOTEX, 0.2)) * (1 - prog(t, SHAMPOO - 0.2, 0.3))
        if xa > 0:
            c.drawLine(380, 1080, 700, 1400, paint(RED, xa, stroke=22)); c.drawLine(700, 1080, 380, 1400, paint(RED, xa, stroke=22))
        pill(c, t, "NOT ABOUT HYGIENE", 540, 1480, RED, HYG, SHAMPOO, light=True)
    ba = eout(prog(t, SHAMPOO - 0.2, 0.4))
    if ba > 0:
        c.save(); c.translate(0, 300 * (1 - ba))
        bottle(c, t, 330, 1030, ba, SHAMPOO + 0.2)
        c.restore()
        pill(c, t, "ZINC PYRITHIONE", 760, 760, "#F4F2EE", SHAMPOO + 0.3, WIPE2, light=True)
        pill(c, t, "KETOCONAZOLE", 760, 840, "#F4F2EE", SHAMPOO + 0.45, WIPE2, light=True)
        pill(c, t, "SELENIUM SULFIDE", 760, 920, "#F4F2EE", SHAMPOO + 0.6, WIPE2, light=True)
        if t > FIVE - 0.1:
            timer_ring(c, t, 760, 1200, eout(prog(t, FIVE - 0.1, 0.3)))
    footnote(c, t, "AAD: dandruff isn't caused by poor hygiene", HYG, SHAMPOO, light=True)
    footnote(c, t, "AAD: leave on 5–10 min · not medical advice", SHAMPOO + 0.3, WIPE2 + 0.2, light=True)


RODS = [(rnd.uniform(160, 920), rnd.uniform(640, 1400), rnd.uniform(0, 180)) for _ in range(12)]


def scene_bact(c, t):
    c.drawImageRect(skin_img(), skia.Rect.MakeXYWH(-150, -200, 1380, 2400), SAMP)
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(540, 1000, 1100, [col("#000000", 0.1), col("#000000", 0.6)])))
    for i, (x, y, s, rot) in enumerate(YEASTS[:8]):
        yeast_cell(c, x, y, s, rot, 0.9, t)
    for i, (x, y, rot) in enumerate(RODS):
        q = eback(prog(t, BACT + i * 0.04, 0.3))
        if q <= 0:
            continue
        c.save(); c.translate(x + 8 * math.sin(t * 2 + i), y); c.rotate(rot + 10 * math.sin(t + i)); c.scale(q, q)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-34, -11, 34, 11), 11, 11)
        c.drawRRect(rr, paint(shader=linear((0, -11), (0, 11), [col("#cfe0ff"), col("#7d9ad8")])))
        c.drawRRect(rr, paint("#3d5aa8", 0.7, stroke=2))
        c.restore()
    pill(c, t, "BACTERIA", 540, 560, "#9db6ee", BACT + 0.1, PART + 0.3, text_col=INK)
    pill(c, t, "STILL BEING STUDIED", 540, 1460, "#FFFFFF", BACT + 0.4, PART + 0.3)
    footnote(c, t, "2016 study: bacteria may matter more than thought · debated", BACT + 0.2, PART + 0.3)


def draw_world(c, t):
    m = mode_at(t)
    if m == "flake_out": scene_flake_out(c, t)
    elif m == "cells": scene_cells(c, t)
    elif m == "block":
        scene_block(c, t)
    elif m == "heads": scene_heads(c, t)
    elif m == "yeast": scene_yeast(c, t)
    elif m == "block2": scene_block(c, t, second=True)
    elif m == "white": scene_white(c, t)
    elif m == "bact":
        scene_bact(c, t)
    else:
        # zoom from the surface into the single flake -> exactly frame 1 at t = DUR
        z = eio(prog(t, PART + 0.1, SO - PART))
        draw_macro(c, t, 1, box=eout(prog(t, SO - 0.25, 0.25)))
        if z < 1:
            c.saveLayerAlpha(None, int(255 * (1 - z)))
            c.save(); c.translate(540, 1000); c.scale(1 + 2 * z, 1 + 2 * z); c.translate(-540, -1000)
            scene_bact(c, t)
            c.restore(); c.restore()


SHIFTS = [REVEAL, HAIR, SKIN, THOUS, TOGETHER, SCALP, ALLTIME, MONTH, FALLS, SEE, HALF, SPEEDS, YEAST, EVERY, OIL, ACID,
          OVER, WEEK, CLUMPS, WASH, NOTEX, HYG, SHAMPOO, FIVE, BACT, PART, SO]


def cut_punch(t):
    """tiny 3% scale punch on every beat change -> a 'shift' every ~2 s"""
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.03 * (1 - d / 0.25) ** 2
    return s


def hud_val(t):
    m = mode_at(t)
    if m in ("flake_out", "end"):
        z = 200 if t < REVEAL or m == "end" else 5
        return ("ZOOM", f"×{z}", "#9a9a9a")
    if m == "cells": return ("ZOOM", "×400", "#9a9a9a")
    if m == "block": return ("CELL JOURNEY", "30 DAYS", LIME)
    if m == "heads": return ("HOW COMMON", "1 IN 2", LIME)
    if m == "yeast": return ("ZOOM", "×1000", "#9a9a9a")
    if m == "block2":
        d = int(round(lerp(30, 7, eexpo(prog(t, WEEK - 0.1, 0.8)))))
        return ("CELL JOURNEY", f"{d} DAYS", RED if d < 30 else LIME)
    if m == "white": return ("THE FIX", "ANTI-YEAST", LIME_INK)
    return ("ZOOM", "×1000", "#9a9a9a")


KWCOL = {"dandruff": "#FFFFFF", "hair": RED, "skin": "#FFFFFF", "together": YELLOW, "all the time": "#FFFFFF",
         "month": LIME, "see": "#FFFFFF", "half": LIME, "yeast": LIME, "everyone": LIME, "oil": YELLOW, "acid": "#FF7A3D",
         "overreact": RED, "week": RED, "clumps": "#FFFFFF", "washing": "#FFFFFF", "exactly": RED, "not": RED,
         "anti-yeast": LIME, "five minutes": LIME, "bacteria": "#9db6ee", "is": "#FFFFFF"}
CAPS = Captions(P, KWCOL, {"half", "Not", "week,"}, DUR)


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    sx = sy = 0
    for ti in IMPACTS:
        d = t - ti
        if 0 <= d < 0.33:
            amp = 9 * (1 - d / 0.33); sx += amp * math.sin(d * 97); sy += amp * math.cos(d * 83)
    ps = cut_punch(t)
    c.save(); c.translate(sx, sy); c.translate(540, 960); c.scale(ps, ps); c.translate(-540, -960)
    draw_world(c, t)
    c.restore()
    light = mode_at(t) == "white"
    dust(c, t, light); vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 620), paint(shader=linear((0, 0), (0, 620), [col("#000000", 0.45), col("#000000", 0)])))
    lab, val, dc = hud_val(t)
    hud(c, t, lab, val, dc, 1.0, light)
    rw = math.sin(math.pi * prog(t, NOTEX, 0.45))
    if rw > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.24 * rw))
    for ti in IMPACTS:
        if 0 <= t - ti < 2 / FPS:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#FFFFFF", 0.3))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, LIME, "#F4F2EE")
    wipe(c, t, WIPE2, WL, LIME, INK)
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", REVEAL - 0.1), ("pop", REVEAL + 0.1), ("pop", HAIR + 0.1), ("whoosh", SKIN - 0.15),
          ("ding", THOUS + 0.9), ("pop", TOGETHER), ("whoosh", SCALP), ("pop", MONTH), ("pop", SEE), ("whoosh", HALF),
          ("riser", SPEEDS - 0.2), ("whoosh", YEAST), ("pop", YEAST + 0.2), ("pop", EVERY), ("pop", OIL), ("pop", ACID),
          ("whoosh", OVER), ("pop", OVER + 0.1), ("hit", CLUMPS), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12),
          ("pop", WASH), ("hit", NOTEX), ("pop", HYG), ("pop", SHAMPOO + 0.3), ("pop", SHAMPOO + 0.45), ("pop", SHAMPOO + 0.6),
          ("whoosh", WIPE2), ("pop", BACT + 0.1), ("pop", BACT + 0.4), ("whoosh", PART + 0.1)]
    for k in range(10):
        ev.append(("tick", THOUS + k * 0.08))
    for k in range(6):
        ev.append(("tick", WEEK + k * 0.12))
    for k in range(6):
        ev.append(("tick", FIVE + k * 0.22))
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

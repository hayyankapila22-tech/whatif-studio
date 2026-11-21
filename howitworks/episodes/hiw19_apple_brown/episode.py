# HIW19 — "Why does a cut apple turn brown?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-22):
#  - Britannica, "Why Do Sliced Apples Turn Brown?" (britannica.com/story/why-do-sliced-apples-turn-brown): cutting exposes
#    the tissue to oxygen; the enzyme polyphenol oxidase turns the apple's polyphenols into compounds that make brown
#    melanins; lemon / pineapple juice acids slow it; keep slices refrigerated to slow it; pears, bananas, eggplants also brown.
#  - Scientific American, "Why do cut apples turn brown?" (scientificamerican.com/article/experts-why-cut-apples-turn-brown/):
#    the enzyme (kept in the cell's plastids) rapidly oxidises phenolic compounds once the cell is broken and oxygen gets in;
#    a lower pH (acid) makes the enzyme less active.
#  - UW-Madison News, "Curiosities: Why do apple slices turn brown?" (news.wisc.edu): "As soon as you break the apple cells,
#    you expose (the enzyme) to polyphenols and oxygen"; the brown pigments are melanins (same family as skin tan);
#    enzymatic browning also in avocados and potatoes.
#  Plain words: enzyme = "tiny helper", polyphenols = "natural colour chemicals", melanin = "same kind of colour as your tan".
#  "Not rotting, it's chemistry": enzymatic browning is a chemical reaction, not decay (all three sources).
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
APPLE = "#E5343F"; APPLE_D = "#A9161F"; FLESH = "#FFF4D6"; BROWN = "#B07A3C"; BROWN_D = "#7A4E22"; HELP = "#FFC83D"
CHEM = "#9B7BFF"; O2 = "#5AB8FF"; LEMON = "#FFE14D"; GREEN = "#1fb98a"; LEAF = "#4CAF50"; ORANGE = "#FF9F43"; ICE = "#8FD8FF"


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


SLICE = p0(ph("slice it")); LEAVE = p0(ph("leave it")); RUSTY = kw(ph("and it looks"))
WIPE1 = p0(ph("okay")) - 0.3; ROT = kw(ph("it's not")); CHEMY = p0(ph("it's chemistry"))
INSIDE = p0(ph("inside every")); HELPER = kw(ph("a tiny")); COLS = kw(ph("and some")); BURST = kw(ph("your knife"))
MIX = kw(ph("they mix")); AIR = kw(ph("and air")); OXY = kw(ph("the helper grabs")); BRN = kw(ph("and turns"))
TAN = p0(ph("same kind")) + 0.25
WIPE2 = p0(ph("bananas")) - 0.3; BAN = p0(ph("bananas")); PEAR = p0(ph("pears")); AVO = p0(ph("avocados")); POT = p0(ph("potatoes"))
SAME = p0(ph("same thing"))
TRICK = p0(ph("the trick")); LEM = kw(ph("a squeeze")); SLOW = kw(ph("the acid")); COLD = kw(ph("or keep"))
SO = p0(len(P) - 1)
WL = 0.32
IMPACTS = [RUSTY, BURST, BRN]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1, ph_=0.0):
    return math.sin(2 * math.pi * k * t / DUR + ph_)


def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#22191a"), col("#151012"), col("#0a0809")], [0, 0.55, 1])))
    c.drawCircle(800 + 30 * lw(t), 720, 520, paint(shader=radial(800, 720, 520, [col(APPLE, 0.10), col(APPLE, 0)])))
    c.drawCircle(220, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1450, 600, [col(LEAF, 0.07), col(LEAF, 0)])))


# ---------------- apple pieces ----------------
def apple_half(c, t, x, y, R, brown, a=1.0, rot=0.0, seed=3):
    """cut face of an apple, seen head-on; brown = 0..1 browning."""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot)
    shape = skia.Path()
    shape.moveTo(0, -R * 0.82)
    shape.cubicTo(R * 0.35, -R * 1.08, R * 1.05, -R * 0.95, R * 1.0, -R * 0.1)
    shape.cubicTo(R * 0.98, R * 0.65, R * 0.45, R * 1.02, 0, R * 0.9)
    shape.cubicTo(-R * 0.45, R * 1.02, -R * 0.98, R * 0.65, -R * 1.0, -R * 0.1)
    shape.cubicTo(-R * 1.05, -R * 0.95, -R * 0.35, -R * 1.08, 0, -R * 0.82)
    c.drawPath(shape, paint("#000000", 0.3 * a, blur=22))
    c.drawPath(shape, paint(shader=radial(-R * 0.3, -R * 0.4, R * 1.6, [col("#FF5A63", a), col(APPLE, a), col(APPLE_D, a)], [0, 0.5, 1])))
    inner = skia.Path(); m = skia.Matrix.Scale(0.93, 0.93); shape.transform(m, inner)
    fl = mixhex(FLESH, BROWN, 0.85 * brown)
    c.drawPath(inner, paint(shader=radial(0, 0, R, [col(mixhex("#FFFBEA", BROWN, 0.6 * brown), a), col(fl, a), col(mixhex("#F2E2B0", BROWN_D, 0.85 * brown), a)], [0, 0.7, 1])))
    if brown > 0:
        c.save(); c.clipPath(inner, doAntiAlias=True)
        for k in range(26):
            rr = random.Random(seed * 100 + k)
            px, py = rr.uniform(-R, R), rr.uniform(-R, R)
            c.drawCircle(px, py, rr.uniform(10, 40) * R / 300, paint(BROWN_D, 0.35 * brown * a, blur=12))
        c.restore()
    # core: soft star + seeds
    core = skia.Path()
    for k in range(10):
        an = -math.pi / 2 + k * math.pi / 5
        rr_ = R * (0.32 if k % 2 == 0 else 0.15)
        px, py = rr_ * math.cos(an), rr_ * math.sin(an) + R * 0.05
        core.moveTo(px, py) if k == 0 else core.lineTo(px, py)
    core.close()
    c.drawPath(core, paint(mixhex("#E9D79D", BROWN_D, 0.7 * brown), 0.7 * a, stroke=max(2, R * 0.012)))
    for k in (0, 2, 4):
        an = -math.pi / 2 + k * math.pi / 5
        sx, sy = R * 0.2 * math.cos(an), R * 0.2 * math.sin(an) + R * 0.05
        c.save(); c.translate(sx, sy); c.rotate(math.degrees(an) + 90)
        c.drawOval(skia.Rect.MakeLTRB(-R * 0.035, -R * 0.07, R * 0.035, R * 0.07), paint("#3B2210", a))
        c.drawOval(skia.Rect.MakeLTRB(-R * 0.012, -R * 0.05, R * 0.012, R * 0.0), paint("#ffffff", 0.35 * a))
        c.restore()
    # stem notch
    c.drawLine(0, -R * 0.82, 0, -R * 1.02, paint("#6B4423", a, stroke=R * 0.04))
    c.restore()


def apple_whole(c, t, x, y, R, a=1.0, rot=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot)
    sh = skia.Path()
    sh.moveTo(0, -R * 0.75)
    sh.cubicTo(R * 0.4, -R * 1.05, R * 1.08, -R * 0.9, R * 1.0, -R * 0.05)
    sh.cubicTo(R * 0.95, R * 0.7, R * 0.45, R * 1.0, 0, R * 0.88)
    sh.cubicTo(-R * 0.45, R * 1.0, -R * 0.95, R * 0.7, -R * 1.0, -R * 0.05)
    sh.cubicTo(-R * 1.08, -R * 0.9, -R * 0.4, -R * 1.05, 0, -R * 0.75)
    c.drawPath(sh, paint("#000000", 0.3 * a, blur=22))
    c.drawPath(sh, paint(shader=radial(-R * 0.35, -R * 0.35, R * 1.7, [col("#FF7A80", a), col(APPLE, a), col(APPLE_D, a)], [0, 0.45, 1])))
    c.drawOval(skia.Rect.MakeLTRB(-R * 0.6, -R * 0.6, -R * 0.25, -R * 0.15), paint("#ffffff", 0.35 * a, blur=R * 0.06))
    c.drawLine(0, -R * 0.75, R * 0.06, -R * 1.05, paint("#6B4423", a, stroke=R * 0.06))
    lf = skia.Path(); lf.moveTo(R * 0.06, -R * 0.95); lf.quadTo(R * 0.35, -R * 1.25, R * 0.55, -R * 1.0); lf.quadTo(R * 0.3, -R * 0.85, R * 0.06, -R * 0.95)
    c.drawPath(lf, paint(LEAF, a))
    c.restore()


def knife(c, x, y, rot, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot)
    bl = skia.Path(); bl.moveTo(-20, -300); bl.lineTo(30, -300); bl.lineTo(30, 160); bl.quadTo(0, 220, -20, 260); bl.close()
    c.drawPath(bl, paint("#000000", 0.25 * a, blur=10))
    c.drawPath(bl, paint(shader=linear((-20, 0), (30, 0), [col("#F4F6F8", a), col("#AEB6BF", a)])))
    c.drawLine(-12, -280, -12, 200, paint("#ffffff", 0.7 * a, stroke=3))
    c.drawRoundRect(skia.Rect.MakeLTRB(-28, -520, 38, -300), 20, 20, paint("#2B2B2E", a))
    for k in range(3):
        c.drawCircle(5, -470 + k * 70, 7, paint("#C9CDD2", a))
    c.restore()


def clock(c, t, x, y, r, a, speed=6):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    c.drawCircle(0, 0, r + 8, paint("#000000", 0.3, blur=10))
    c.drawCircle(0, 0, r, paint("#ffffff"))
    c.drawCircle(0, 0, r, paint(ORANGE, 1, stroke=8))
    an = t * speed
    c.drawLine(0, 0, r * 0.7 * math.cos(an), r * 0.7 * math.sin(an), paint(INK, 1, stroke=7))
    c.drawLine(0, 0, r * 0.45 * math.cos(an / 12), r * 0.45 * math.sin(an / 12), paint(INK, 1, stroke=10))
    c.restore()


# ---------------- hook: fresh half vs brown half ----------------
def scene_hook(c, t):
    bg_dark(c, t)
    apple_half(c, t, 270, 1060 + 16 * lw(t, 2), 165, 0.0, rot=-6 + 3 * lw(t, 1))
    apple_half(c, t, 725, 1040 + 16 * lw(t, 2, 1.5), 165, 1.0, rot=6 + 3 * lw(t, 1, 2), seed=5)
    # "?" bounce between them
    f = skia.Font(TF_BLACK, 130)
    c.drawString("?", 497 - f.measureText("?") / 2, 1100 + 18 * lw(t, 3), f, paint("#ffffff", 0.9))


def scene_open(c, t):
    q = eio(prog(t, SLICE - 0.2, 0.3))
    if q < 1:
        scene_hook(c, t)
        if q <= 0: return
        c.saveLayerAlpha(None, int(255 * q))
    bg_dark(c, t)
    cut = prog(t, SLICE + 0.05, 0.35)
    if cut < 1:
        apple_whole(c, t, 495, 1060, 300, 1.0, rot=3 * math.sin(t * 2))
        knife(c, 495 + 10, lerp(300, 1100, eio(cut)), 0, window(t, SLICE - 0.2, SLICE + 0.5, 0.15, 0.1))
    else:
        sep = eback(prog(t, SLICE + 0.4, 0.4))
        br = eout(prog(t, RUSTY - 0.4, 0.7))
        apple_half(c, t, 495, 1060, 300 * lerp(0.9, 1.0, sep), br, rot=2 * math.sin(t * 1.5))
        if cut < 1.3:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#ffffff", 0.5 * (1 - prog(t, SLICE + 0.4, 0.2))))
    clock(c, t, 800, 760, 75, eback(prog(t, LEAVE - 0.05, 0.3)) * (1 - prog(t, WIPE1, 0.2)), speed=9)
    if q < 1: c.restore()
    pill(c, t, "WHY BROWN?", 495, 560, BROWN, 0.35, SLICE - 0.05)
    pill(c, t, "SLICE IT", 495, 560, "#8a8f98", SLICE, LEAVE - 0.05)
    pill(c, t, "LEAVE IT...", 495, 560, ORANGE, LEAVE, RUSTY - 0.05)
    pill(c, t, "RUSTY!", 495, 560, BROWN, RUSTY, WIPE1 + 0.1)


# ---------------- white: inside the cells ----------------
CELLS = []
for r in range(5):
    for k in range(4):
        cx = 190 + k * 205 + (r % 2) * 50 - 25
        cy = 760 + r * 160
        CELLS.append((cx, cy, r, k))
CUTX = 560   # knife line through the cells


def helper(c, x, y, s, a, t, chomp=1.0, sleepy=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    mo = 30 * chomp * (0.5 + 0.5 * math.sin(t * 14)) * (1 - sleepy) + 6
    c.drawCircle(0, 4, 26, paint("#000000", 0.15 * a, blur=6))
    c.drawArc(skia.Rect.MakeLTRB(-24, -24, 24, 24), mo, 360 - 2 * mo, True, paint(HELP, a))
    c.drawCircle(-2, -12, 4, paint(INK, a)) if sleepy < 0.5 else c.drawLine(-7, -12, 3, -12, paint(INK, a, stroke=3))
    c.restore()


def chem(c, x, y, a, br, seed):
    rr = random.Random(seed)
    for k in range(5):
        px, py = x + rr.uniform(-18, 18), y + rr.uniform(-16, 16)
        c.drawCircle(px, py, 8, paint(mixhex(CHEM, BROWN, br), a))


def scene_cells(c, t):
    studio_white(c)
    a = eout(prog(t, WIPE1, 0.4))
    hl = eout(prog(t, HELPER - 0.15, 0.3))
    cl = eout(prog(t, COLS - 0.15, 0.3))
    burst = eout(prog(t, BURST - 0.05, 0.3))
    mix = eio(prog(t, MIX - 0.1, 0.6))
    air = eout(prog(t, AIR - 0.15, 0.5))
    grab = eio(prog(t, OXY - 0.1, 0.5))
    brn = eout(prog(t, BRN - 0.05, 0.6))
    z = lerp(1.2, 1.0, eio(prog(t, WIPE1, 1.0)))
    tan_out = eio(prog(t, TAN - 0.2, 0.4))
    c.save(); c.translate(495, 1080); c.scale(z * lerp(1, 0.75, tan_out), z * lerp(1, 0.75, tan_out)); c.translate(-495, -1080 - 150 * tan_out)
    for (cx, cy, r, k) in CELLS:
        q = eback(prog(t, WIPE1 + 0.1 + (r * 4 + k) * 0.02, 0.35)) * a
        if q <= 0: continue
        hit = abs(cx - CUTX) < 140
        wob = 3 * math.sin(t * 3 + r + k)
        rect = skia.Rect.MakeLTRB(cx - 95, cy - 70 + wob, cx + 95, cy + 70 + wob)
        broken = burst if hit else 0
        c.drawRoundRect(rect, 40, 40, paint(mixhex("#FFF7DF", "#F1D9A8", broken * brn), q))
        pe = paint("#C9A86A", q * (1 - 0.8 * broken), stroke=5)
        if broken > 0:
            pe.setPathEffect(skia.DashPathEffect.Make([30 * (1 - broken) + 6, 18 * broken + 2], 0))
        c.drawRoundRect(rect, 40, 40, pe)
        # helper pocket (left) + colour-chemical pocket (right), apart until the cell bursts
        hx0, hy0 = cx - 45, cy + wob; chx0, chy0 = cx + 40, cy + wob
        m_ = mix * broken
        hx = lerp(hx0, cx + 10, m_) + 10 * grab * broken * math.sin(t * 6); hy = hy0
        if hl > 0:
            c.drawCircle(hx0, hy0, 38, paint(HELP, 0.18 * q * hl * (1 - m_), stroke=4))
            helper(c, hx, hy, 0.85, q * hl, t + r + k, chomp=0.3 + 0.7 * grab * broken)
        if cl > 0:
            c.drawCircle(chx0, chy0, 38, paint(CHEM, 0.25 * q * cl * (1 - m_), stroke=4))
            chem(c, lerp(chx0, cx + 30, m_), chy0, q * cl, brn * broken, r * 10 + k)
    # knife line + air bubbles
    if burst > 0:
        kx = CUTX
        c.drawLine(kx, lerp(600, 1600, burst), kx, 600, paint("#AEB6BF", 0.9 * a * (1 - prog(t, MIX, 0.4)), stroke=10))
    if air > 0:
        for k in range(14):
            rr = random.Random(200 + k)
            bx = CUTX + rr.uniform(-130, 130) + 10 * math.sin(t * 3 + k)
            by0 = rr.uniform(650, 1450)
            by = lerp(by0 - 260, by0, air) - 20 * math.sin(t * 2 + k)
            bub = O2 if brn < 0.5 or (k % 3) else BROWN
            al = a * air * (1 - grab * 0.8)
            c.drawCircle(bx, by, 17, paint(bub, 0.8 * al))
            c.drawCircle(bx - 5, by - 5, 5, paint("#ffffff", 0.8 * al))
    c.restore()
    # suntan comparison
    if tan_out > 0:
        for k, (lab, cc) in enumerate((("APPLE", BROWN), ("SUNTAN", "#C68B59"))):
            x = 330 + k * 330; y = 1335
            sw = eback(prog(t, TAN + k * 0.15, 0.35))
            c.save(); c.translate(x, y); c.scale(sw, sw)
            c.drawCircle(0, 0, 70, paint("#000000", 0.2, blur=10))
            c.drawCircle(0, 0, 64, paint(cc))
            f = skia.Font(TF_MONO, 24)
            c.drawString(lab, -f.measureText(lab) / 2, 104, f, paint(INK, 0.8))
            c.restore()
        f = skia.Font(TF_BLACK, 70)
        c.drawString("=", 495 - f.measureText("=") / 2, 1360, f, paint(INK, 0.7 * tan_out))
    pill(c, t, "NOT ROTTING", 495, 560, GREEN, ROT, CHEMY - 0.05, text_col="#FFFFFF")
    pill(c, t, "IT'S CHEMISTRY", 495, 560, CHEM, CHEMY, HELPER - 0.05)
    pill(c, t, "TINY HELPER", 495, 560, "#C9A100", HELPER, COLS - 0.05, text_col="#FFFFFF")
    pill(c, t, "+ COLOUR CHEMICALS", 495, 560, CHEM, COLS, BURST - 0.05)
    pill(c, t, "CELLS BURST", 495, 560, "#8a8f98", BURST, MIX - 0.05)
    pill(c, t, "THEY MIX", 495, 560, CHEM, MIX, AIR - 0.05)
    pill(c, t, "+ AIR", 495, 560, O2, AIR, OXY - 0.05)
    pill(c, t, "GRABS OXYGEN", 495, 560, O2, OXY, BRN - 0.05)
    pill(c, t, "= BROWN!", 495, 560, BROWN, BRN, TAN - 0.05)
    pill(c, t, "LIKE A TAN", 495, 560, "#C68B59", TAN, WIPE2 + 0.1)


# ---------------- dark: other foods, lemon, fridge ----------------
def banana(c, x, y, s, a, br, t):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-20)
    p = skia.Path(); p.moveTo(-130, -40); p.cubicTo(-60, 100, 80, 100, 140, -50); p.cubicTo(80, 25, -60, 25, -130, -40); p.close()
    c.drawPath(p, paint("#000000", 0.25 * a, blur=10))
    c.drawPath(p, paint(mixhex("#FFD93D", "#C9A26A", 0.5 * br), a))
    c.drawLine(-130, -30, -150, -45, paint("#5a4020", a, stroke=10))
    for k in range(6):
        rr = random.Random(k)
        if br > rr.random() * 0.8:
            c.drawCircle(rr.uniform(-80, 90), rr.uniform(10, 30), rr.uniform(5, 10), paint(BROWN_D, a * 0.8))
    c.restore()


def pear(c, x, y, s, a, br, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 40, 85, paint("#000000", 0.25 * a, blur=10))
    cc = mixhex("#B5D96B", "#B08A4E", 0.6 * br)
    c.drawCircle(0, 40, 80, paint(cc, a)); c.drawCircle(0, -40, 52, paint(cc, a))
    c.drawOval(skia.Rect.MakeLTRB(-40, 0, 40, 110), paint(mixhex("#FFF6D0", BROWN, br), a))
    c.drawLine(0, -90, 8, -125, paint("#6B4423", a, stroke=8))
    c.restore()


def avocado(c, x, y, s, a, br, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-80, -110, 80, 110), paint("#000000", 0.25 * a, blur=10))
    c.drawOval(skia.Rect.MakeLTRB(-75, -105, 75, 105), paint("#2E5E1E", a))
    c.drawOval(skia.Rect.MakeLTRB(-63, -92, 63, 92), paint(mixhex("#D8EC8C", "#8A7A3A", br), a))
    c.drawCircle(0, 25, 34, paint("#8A5A2B", a)); c.drawCircle(-10, 14, 9, paint("#ffffff", 0.3 * a))
    c.restore()


def potato(c, x, y, s, a, br, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.addOval(skia.Rect.MakeLTRB(-110, -75, 110, 75))
    c.drawPath(p, paint("#000000", 0.25 * a, blur=10))
    c.drawPath(p, paint("#C9A26A", a))
    c.drawOval(skia.Rect.MakeLTRB(-10, -60, 100, 60), paint(mixhex("#FFF1C2", "#9C6E3A", br), a))
    for (ex, ey) in ((-70, -20), (-50, 30)):
        c.drawCircle(ex, ey, 6, paint("#7A5A30", a))
    c.restore()


def scene_foods(c, t):
    bg_dark(c, t)
    a = eout(prog(t, WIPE2, 0.4))
    items = ((banana, 300, 850, BAN), (pear, 700, 850, PEAR), (avocado, 300, 1230, AVO), (potato, 700, 1230, POT))
    for fn, x, y, tin in items:
        q = eback(prog(t, tin - 0.1, 0.35))
        if q <= 0: continue
        br = eout(prog(t, tin + 0.2, 1.0))
        c.drawCircle(x, y, 160, paint("#ffffff", 0.05 * a * q))
        fn(c, x, y + 8 * math.sin(t * 2 + x), 1.15 * q, a, br, t)
    sa = eback(prog(t, SAME - 0.05, 0.3))
    if sa > 0:
        c.save(); c.translate(495, 1040); c.scale(sa, sa)
        c.drawCircle(0, 0, 70, paint(BROWN, 0.95)); c.drawCircle(0, 0, 70, paint("#ffffff", 0.8, stroke=5))
        f = skia.Font(TF_BLACK, 60); c.drawString("=", -f.measureText("=") / 2, 22, f, paint("#ffffff"))
        c.restore()
    pill(c, t, "BANANAS", 495, 560, "#C9A100", BAN, PEAR - 0.05, text_col="#FFFFFF")
    pill(c, t, "PEARS", 495, 560, "#7FA83A", PEAR, AVO - 0.05)
    pill(c, t, "AVOCADOS", 495, 560, "#2E5E1E", AVO, POT - 0.05)
    pill(c, t, "POTATOES", 495, 560, "#A07A45", POT, SAME - 0.05)
    pill(c, t, "SAME THING!", 495, 560, BROWN, SAME, TRICK + 0.1)


def lemon(c, x, y, s, rot, a, squeeze=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * (1 + 0.1 * squeeze), s * (1 - 0.15 * squeeze))
    c.drawOval(skia.Rect.MakeLTRB(-120, -78, 120, 78), paint("#000000", 0.25 * a, blur=12))
    c.drawOval(skia.Rect.MakeLTRB(-120, -78, 120, 78), paint(shader=radial(-30, -30, 160, [col("#FFF28A", a), col(LEMON, a), col("#E0B800", a)], [0, 0.5, 1])))
    c.drawCircle(-124, 0, 14, paint("#E0B800", a))
    # cut face
    c.drawOval(skia.Rect.MakeLTRB(80, -70, 140, 70), paint("#FFF6B0", a))
    for k in range(6):
        an = k * math.pi / 3
        c.drawLine(110, 0, 110 + 24 * math.cos(an), 60 * math.sin(an), paint("#F2D64B", a, stroke=4))
    c.restore()


def fridge(c, t, x, y, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    c.drawRoundRect(skia.Rect.MakeLTRB(-130, -190, 130, 190), 30, 30, paint("#000000", 0.3, blur=14))
    c.drawRoundRect(skia.Rect.MakeLTRB(-130, -190, 130, 190), 30, 30, paint(shader=linear((0, -190), (0, 190), [col("#F4FBFF"), col("#C9E2EE")])))
    c.drawLine(-130, -60, 130, -60, paint("#9FB7C4", 1, stroke=4))
    c.drawRoundRect(skia.Rect.MakeLTRB(90, -170, 105, -90), 6, 6, paint("#9FB7C4"))
    c.drawRoundRect(skia.Rect.MakeLTRB(90, -40, 105, 60), 6, 6, paint("#9FB7C4"))
    for k in range(6):
        rr = random.Random(k)
        sx = rr.uniform(-170, 170); sy = ((rr.uniform(-220, 220) + t * 70) % 440) - 220
        for j in range(3):
            an = j * math.pi / 3 + t
            c.drawLine(sx - 16 * math.cos(an), sy - 16 * math.sin(an), sx + 16 * math.cos(an), sy + 16 * math.sin(an), paint(ICE, 0.9, stroke=4))
    c.restore()


def scene_trick(c, t):
    bg_dark(c, t)
    a = eout(prog(t, TRICK - 0.3, 0.35))
    cold = eio(prog(t, COLD - 0.15, 0.5))
    ax = lerp(495, 330, cold)
    apple_half(c, t, ax, 1130, 230 * lerp(1, 0.8, cold), 0.05, a, rot=3 * math.sin(t * 1.4))
    la = window(t, LEM - 0.2, COLD + 0.1, 0.25, 0.25) * a
    sq = 0.5 + 0.5 * math.sin(t * 8) if t > LEM else 0
    lemon(c, 690, 790, 0.95, 25, la, sq)
    if la > 0 and t > LEM:
        for k in range(8):
            u = ((t - LEM) * 1.3 + k / 8) % 1.0
            dx = lerp(610, ax + 40 * math.sin(k * 2.1), u); dy = lerp(860, 1080, u * u)
            c.drawCircle(dx, dy, 11, paint(LEMON, la * (1 - u * 0.3)))
    # slowed-down helper
    ha = window(t, SLOW - 0.1, COLD + 0.1, 0.25, 0.25) * a
    if ha > 0:
        helper(c, 260, 820, 2.0, ha, t * 0.25, chomp=0.4, sleepy=1.0)
        f = skia.Font(TF_BLACK, 50)
        for k in range(3):
            u = ((t / 0.9) + k / 3) % 1.0
            c.drawString("z", 310 + 50 * u, 770 - 120 * u, f, paint(HELP, ha * math.sin(math.pi * u)))
    fridge(c, t, 730, 1080, eback(prog(t, COLD - 0.05, 0.35)) * a)
    pill(c, t, "THE TRICK?", 495, 560, "#8a8f98", TRICK, LEM - 0.05)
    pill(c, t, "LEMON JUICE", 495, 560, "#C9A100", LEM, SLOW - 0.05, text_col="#FFFFFF")
    pill(c, t, "ACID SLOWS IT", 495, 560, "#C9A100", SLOW, COLD - 0.05, text_col="#FFFFFF")
    pill(c, t, "KEEP IT COLD", 495, 560, "#2A9ED6", COLD, SO + 0.3)


def xfade(c, t, t0, d, new, old):
    q = 1 - prog(t, t0, d)
    new(c, t)
    if q > 0:
        c.saveLayerAlpha(None, int(255 * q)); old(c, t); c.restore()


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_cells(c, t); return
    if t < TRICK - 0.3:
        scene_foods(c, t); return
    if t < SO - 0.05:
        xfade(c, t, TRICK - 0.3, 0.3, scene_trick, scene_foods); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_trick(c, t); c.restore()


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


KWCOL = {"brown": BROWN, "rusty": BROWN, "rotting": GREEN, "helper": HELP, "colour": CHEM, "chemicals": CHEM,
         "bursts": "#8a8f98", "mix": CHEM, "air": O2, "oxygen": O2, "tan": "#C68B59", "bananas": HELP,
         "potatoes": "#C9A26A", "lemon": LEMON, "down": LEMON, "cold": ICE}
CAPS = Captions(split_long(P), KWCOL, {"bursts", "brown!"}, DUR)


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
    wipe(c, t, WIPE1, WL, APPLE, "#F4F2EE")
    wipe(c, t, WIPE2, WL, BROWN, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("whoosh", SLICE), ("pop", LEAVE), ("hit", RUSTY),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", ROT), ("pop", CHEMY), ("pop", HELPER), ("pop", COLS),
          ("hit", BURST), ("pop", MIX), ("riser", AIR - 0.1), ("pop", OXY), ("hit", BRN), ("pop", TAN),
          ("whoosh", WIPE2), ("pop", BAN), ("pop", PEAR), ("pop", AVO), ("pop", POT), ("ding", SAME),
          ("whoosh", TRICK - 0.3), ("pop", LEM), ("pop", SLOW), ("pop", COLD), ("whoosh", SO - 0.05)]
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

# HIW20 — "Why does spinach make your teeth feel squeaky?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-22):
#  - Live Science, "Why Does Spinach Make Your Teeth Feel Weird?" (livescience.com/56237-why-spinach-makes-teeth-feel-weird.html,
#    2016): gritty film on teeth; when you chew spinach the oxalic acid combines with calcium to form calcium oxalate crystals
#    that don't dissolve well in water; squeeze lemon juice on top to reduce the film; spinach has more oxalic acid than
#    other crops.
#  - BBC Science Focus, "Why does eating spinach make my teeth feel weird?" (sciencefocus.com, 2017/2023): calcium in your
#    saliva reacts with oxalic acid -> insoluble calcium oxalate crystals that stick to teeth (gritty / chalky);
#    "spinach does not damage your teeth"; milk's high calcium content makes it worse.
#  - America's Test Kitchen, "Spinach and chalky residue": oxalic acid released by chewing combines with calcium in saliva;
#    effect exaggerated with dairy (milk and cheese contain far more calcium than saliva).
#  Plain words: oxalic acid = "a natural acid", saliva = "spit".
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
SPIN = "#2F9E44"; SPIN_D = "#1B6B2C"; ACID = "#B6F25A"; CALC = "#5AB8FF"; CRYS = "#F4F7FF"; GUM = "#F28B9B"
TOOTH = "#FFFDF6"; CHEESE = "#FFC93D"; LEMON = "#FFE14D"; GREEN = "#1fb98a"; ORANGE = "#FF9F43"; PURPLE = "#8C7BFF"


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


CHALK = kw(ph("that chalky")); GRIT1 = p0(ph("gritty")); DIRT = p0(ph("it's not dirt"))
WIPE1 = p0(ph("okay")) - 0.3; ACIDt = kw(ph("spinach is packed")); CHEW = p0(ph("when you chew")); CALt = kw(ph("it meets"))
LOCK = kw(ph("they lock")); NODIS = p0(ph("that don't")); STICK = kw(ph("and they stick"))
WIPE2 = p0(ph("that's the grit")) - 0.3; GRIT = kw(ph("that's the grit")); RELAX = p0(ph("relax")); DMG = kw(ph("it doesn't"))
DAIRY = kw(ph("add milk")); MORECA = p0(ph("more calcium")); MORE = kw(ph("even more"))
TRICK = p0(ph("the trick")); LEM = kw(ph("a squeeze")); CUTS = p0(ph("cuts down"))
VEG = p0(ph("and spinach has")); VEG2 = kw(ph("than almost")); SO = p0(len(P) - 1)
WL = 0.32
IMPACTS = [CHALK, LOCK, MORE]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1, ph_=0.0):
    return math.sin(2 * math.pi * k * t / DUR + ph_)


def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#16211a"), col("#0f1612"), col("#080b09")], [0, 0.55, 1])))
    c.drawCircle(800 + 30 * lw(t), 720, 520, paint(shader=radial(800, 720, 520, [col(SPIN, 0.12), col(SPIN, 0)])))
    c.drawCircle(220, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1450, 600, [col(CALC, 0.06), col(CALC, 0)])))


# ---------------- teeth ----------------
def tooth_path(w, h):
    p = skia.Path()
    p.moveTo(-w / 2, 0)
    p.lineTo(-w / 2 + 4, h * 0.75)
    p.quadTo(-w / 2 + 6, h, -w / 2 + 30, h)
    p.lineTo(w / 2 - 30, h)
    p.quadTo(w / 2 - 6, h, w / 2 - 4, h * 0.75)
    p.lineTo(w / 2, 0)
    p.close()
    return p


def film_dots(c, path, a, seed, t, n=60, size=1.0):
    if a <= 0: return
    c.save(); c.clipPath(path, doAntiAlias=True)
    b = path.getBounds()
    for k in range(n):
        rr = random.Random(seed * 1000 + k)
        x = rr.uniform(b.left(), b.right()); y = rr.uniform(b.top(), b.bottom())
        s = rr.uniform(3, 8) * size
        tw = 0.6 + 0.4 * math.sin(t * rr.uniform(3, 7) + k)
        c.save(); c.translate(x, y); c.rotate(45 + rr.uniform(-20, 20))
        c.drawRect(skia.Rect.MakeLTRB(-s, -s, s, s), paint("#E6E2D6", 0.85 * a))
        c.drawRect(skia.Rect.MakeLTRB(-s * 0.4, -s * 0.4, s * 0.2, s * 0.2), paint("#ffffff", 0.9 * a * tw))
        c.restore()
    c.restore()


def teeth(c, t, x, y, s, film=0.0, a=1.0, shine=0.0):
    """front view of the four upper front teeth under a gum line."""
    c.save(); c.translate(x, y); c.scale(s, s)
    # gum
    g = skia.Path(); g.moveTo(-330, -120); g.lineTo(330, -120); g.lineTo(330, 10)
    for k in range(4, -1, -1):
        gx = -300 + k * 150
        g.quadTo(gx + 75, -40, gx, 10) if k < 4 else None
    g.close()
    c.drawRoundRect(skia.Rect.MakeLTRB(-340, -150, 340, 30), 60, 60, paint(shader=linear((0, -150), (0, 30), [col("#F6A2B0", a), col(GUM, a), col("#D9667A", a)])))
    widths = (130, 160, 160, 130); xs = (-225, -80, 80, 225); hs = (230, 270, 270, 230)
    for k in range(4):
        tp = tooth_path(widths[k], hs[k])
        c.save(); c.translate(xs[k], 0)
        c.drawPath(tp, paint("#000000", 0.18 * a, blur=10))
        c.drawPath(tp, paint(shader=linear((0, 0), (0, hs[k]), [col("#FFFFFF", a), col(TOOTH, a), col("#EDE6D2", a)], [0, 0.6, 1])))
        c.drawPath(tp, paint("#D8D0BC", 0.8 * a, stroke=3))
        c.drawOval(skia.Rect.MakeLTRB(-widths[k] * 0.3, 30, -widths[k] * 0.1, hs[k] * 0.7), paint("#ffffff", 0.7 * a, blur=6))
        film_dots(c, tp, film * a, k, t, n=int(40 + 30 * film))
        if shine > 0:
            sx = lerp(-widths[k], widths[k], (t * 0.8 + k * 0.2) % 1.0)
            c.save(); c.clipPath(tp, doAntiAlias=True)
            c.drawLine(sx, 0, sx + 60, hs[k], paint("#ffffff", 0.6 * shine * a, stroke=18, blur=6))
            c.restore()
        c.restore()
    # gum overlap edge
    c.drawRoundRect(skia.Rect.MakeLTRB(-340, -150, 340, 22), 60, 60, paint("#C95569", 0.5 * a, stroke=3))
    c.restore()


def leaf(c, t, x, y, s, rot, a, glow=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, -200); p.cubicTo(150, -160, 170, 80, 0, 200); p.cubicTo(-170, 80, -150, -160, 0, -200)
    c.drawPath(p, paint("#000000", 0.25 * a, blur=14))
    c.drawPath(p, paint(shader=radial(-40, -60, 260, [col("#5CC46B", a), col(SPIN, a), col(SPIN_D, a)], [0, 0.6, 1])))
    c.drawLine(0, -190, 0, 260, paint("#9BE08F", 0.9 * a, stroke=8))
    for k in range(5):
        yy = -130 + k * 60
        for sx in (-1, 1):
            v = skia.Path(); v.moveTo(0, yy); v.quadTo(sx * 50, yy - 10, sx * 95, yy - 50)
            c.drawPath(v, paint("#9BE08F", 0.6 * a, stroke=4))
    if glow > 0:
        c.drawPath(p, paint(ACID, 0.25 * glow * a, blur=20))
    c.restore()


# ---------------- hook ----------------
def squeak_lines(c, t, x, y, a):
    if a <= 0: return
    for k in range(3):
        u = ((t / (DUR / 8)) + k / 3) % 1.0
        r = 60 + 90 * u
        al = a * math.sin(math.pi * u)
        c.drawArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), -40, 80, False, paint("#ffffff", 0.8 * al, stroke=8))
        c.drawArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), 140, 80, False, paint("#ffffff", 0.8 * al, stroke=8))


def scene_hook(c, t):
    bg_dark(c, t)
    teeth(c, t, 495, 980 + 10 * lw(t, 2), 1.15, film=0.0, shine=1.0)
    leaf(c, t, 250 + 20 * lw(t, 1), 1350 + 15 * lw(t, 2), 0.55, -30 + 8 * lw(t, 3), 1.0)
    squeak_lines(c, t, 495, 1130, 1.0)


def scene_open(c, t):
    bg_dark(c, t)
    film = eout(prog(t, CHALK - 0.15, 0.5))
    teeth(c, t, 495, 980 + 10 * lw(t, 2), 1.15 + 0.15 * eio(prog(t, GRIT1 - 0.1, 0.5)), film=film, shine=1 - film)
    leaf(c, t, 250 + 20 * lw(t, 1), 1350 + 15 * lw(t, 2), 0.55, -30 + 8 * lw(t, 3), 1 - film)
    squeak_lines(c, t, 495, 1130, 1 - film)
    # "not dirt" stamp
    da = eback(prog(t, DIRT - 0.05, 0.3)) * (1 - prog(t, WIPE1, 0.2))
    if da > 0:
        c.save(); c.translate(780, 1340); c.rotate(-12); c.scale(da, da)
        c.drawCircle(0, 0, 95, paint("#000000", 0.3, blur=10))
        c.drawCircle(0, 0, 90, paint("#2a2d33"))
        for k in range(7):
            rr = random.Random(k)
            c.drawCircle(rr.uniform(-40, 40), rr.uniform(-40, 40), rr.uniform(8, 18), paint("#6b5a44"))
        c.drawCircle(0, 0, 90, paint(RED, 1, stroke=10))
        c.drawLine(-62, 62, 62, -62, paint(RED, 1, stroke=12))
        c.restore()
    pill(c, t, "SQUEAKY TEETH?", 495, 560, SPIN, 0.35, CHALK - 0.05)
    pill(c, t, "CHALKY", 495, 560, "#8a8f98", CHALK, GRIT1 - 0.05)
    pill(c, t, "GRITTY FILM", 495, 560, "#8a8f98", GRIT1, DIRT - 0.05)
    pill(c, t, "NOT DIRT!", 495, 560, RED, DIRT, WIPE1 + 0.1)


# ---------------- white: acid + calcium -> crystals ----------------
def ion(c, x, y, r, colr, label, a, inkc=INK):
    if a <= 0: return
    c.drawCircle(x, y + 4, r, paint("#000000", 0.15 * a, blur=6))
    c.drawCircle(x, y, r, paint(colr, a))
    c.drawCircle(x - r * 0.35, y - r * 0.35, r * 0.25, paint("#ffffff", 0.5 * a))
    if label:
        f = skia.Font(TF_MONO, int(r * 0.8))
        c.drawString(label, x - f.measureText(label) / 2, y + r * 0.3, f, paint(inkc, a))


def crystal(c, x, y, s, rot, a, sparkle=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, -34); p.lineTo(22, 0); p.lineTo(0, 34); p.lineTo(-22, 0); p.close()
    c.drawPath(p, paint("#000000", 0.18 * a, blur=6))
    c.drawPath(p, paint(shader=linear((-22, -34), (22, 34), [col("#ffffff", a), col("#DDE6F5", a), col("#B8C6DE", a)])))
    c.drawPath(p, paint("#8EA0BF", a, stroke=2.5))
    c.drawLine(0, -34, 0, 34, paint("#ffffff", 0.7 * a, stroke=2))
    if sparkle > 0:
        c.drawCircle(-6, -12, 6, paint("#ffffff", sparkle * a, blur=3))
    c.restore()


NPAIR = 9


def pair_pos(k, t, phase):
    """acid (from the leaf, left) and calcium (from spit, right) travel to a meeting point."""
    rr = random.Random(30 + k)
    mx = 330 + (k % 3) * 170 + rr.uniform(-25, 25)
    my = 860 + (k // 3) * 150 + rr.uniform(-25, 25)
    return mx, my, rr


def scene_lab(c, t):
    studio_white(c)
    a = eout(prog(t, WIPE1, 0.4))
    acid = eout(prog(t, ACIDt - 0.1, 0.4))
    chew = eio(prog(t, CHEW, 0.6))
    cal = eout(prog(t, CALt - 0.15, 0.4))
    meet = eio(prog(t, CALt + 0.1, 0.6))
    lock = eback(prog(t, LOCK - 0.05, 0.3))
    nod = eio(prog(t, NODIS - 0.1, 0.4))
    stick = eio(prog(t, STICK - 0.15, 0.6))
    # leaf on the left, slides out when chewing
    leaf(c, t, lerp(495, 170, chew), lerp(1060, 1000, chew), lerp(1.3, 0.6, chew), -10 + 4 * math.sin(t * 2), a * (1 - 0.5 * stick), glow=acid)
    # spit droplet on the right
    sa = a * cal * (1 - stick)
    if sa > 0:
        c.save(); c.translate(860, 1000 + 8 * math.sin(t * 2.5)); c.scale(cal, cal)
        d = skia.Path(); d.moveTo(0, -110); d.cubicTo(60, -40, 80, 10, 80, 40); d.cubicTo(80, 95, 40, 120, 0, 120); d.cubicTo(-40, 120, -80, 95, -80, 40); d.cubicTo(-80, 10, -60, -40, 0, -110)
        c.drawPath(d, paint("#000000", 0.12 * sa, blur=10))
        c.drawPath(d, paint(shader=radial(-20, 20, 140, [col("#E9F6FF", sa), col("#A9DBFF", sa)])))
        c.drawPath(d, paint(CALC, sa, stroke=4))
        f = skia.Font(TF_MONO, 22); c.drawString("SPIT", -f.measureText("SPIT") / 2, 175, f, paint(INK, 0.6 * sa))
        c.restore()
    # water bath for "don't dissolve"
    if nod > 0:
        wa = a * nod * (1 - stick)
        c.drawRoundRect(skia.Rect.MakeLTRB(230, 760, 760, 1250), 40, 40, paint(CALC, 0.12 * wa))
        for k in range(10):
            rr = random.Random(400 + k)
            bx = rr.uniform(260, 730); by = 1230 - ((t * 120 * rr.uniform(0.6, 1.2) + rr.uniform(0, 470)) % 470)
            c.drawCircle(bx, by, rr.uniform(5, 10), paint("#ffffff", 0.8 * wa, stroke=2))
    # pairs
    for k in range(NPAIR):
        mx, my, rr = pair_pos(k, t, 0)
        ax0, ay0 = lerp(495, 170, chew) + rr.uniform(-110, 110), 1060 + rr.uniform(-180, 180)
        cx0, cy0 = 860 + rr.uniform(-60, 60), 1000 + rr.uniform(-60, 90)
        wob = 8 * math.sin(t * 4 + k)
        axp = lerp(ax0, mx - 24, meet) + wob * (1 - lock); ayp = lerp(ay0, my, meet)
        cxp = lerp(cx0, mx + 24, meet) - wob * (1 - lock); cyp = lerp(cy0, my, meet)
        # tooth target for "stick"
        tx = 330 + (k % 5) * 85 + rr.uniform(-10, 10); ty = 1170 + (k // 5) * 90 + rr.uniform(-10, 10)
        if lock < 0.6:
            ion(c, axp, ayp, 22, ACID, "", a * acid * (1 - lock / 0.6))
            ion(c, cxp, cyp, 22, CALC, "", a * cal * (1 - lock / 0.6))
        if lock > 0:
            jit = (1 - nod) * 0
            px = lerp(mx, tx, stick); py = lerp(my, ty, stick) + 6 * math.sin(t * 3 + k) * (1 - stick)
            crystal(c, px, py, clamp(lock, 0, 1.3) * 1.1, 20 * k + 30 * math.sin(t + k) * (1 - stick), a, sparkle=0.5 + 0.5 * math.sin(t * 6 + k))
    # tooth that the crystals stick to
    if stick > 0:
        tp = tooth_path(520, 340)
        c.save(); c.translate(495, lerp(1700, 1080, eout(prog(t, STICK - 0.4, 0.5))))
        c.drawPath(tp, paint("#000000", 0.15 * a, blur=12))
        c.drawPath(tp, paint(shader=linear((0, 0), (0, 340), [col("#FFFFFF", a), col(TOOTH, a), col("#EDE6D2", a)])))
        c.drawPath(tp, paint("#D8D0BC", a, stroke=4))
        c.restore()
        # re-draw the stuck crystals on top of the tooth
        for k in range(NPAIR):
            mx, my, rr = pair_pos(k, t, 0)
            tx = 330 + (k % 5) * 85 + rr.uniform(-10, 10); ty = 1170 + (k // 5) * 90 + rr.uniform(-10, 10)
            px = lerp(mx, tx, stick); py = lerp(my, ty, stick)
            crystal(c, px, py, 1.1, 20 * k + 30 * math.sin(t + k) * (1 - stick), a * stick, sparkle=0.5 + 0.5 * math.sin(t * 6 + k))
    # legend
    f = skia.Font(TF_MONO, 24)
    lg = a * window(t, CALt, LOCK, 0.3, 0.3)
    if lg > 0:
        ion(c, 300, 1440, 16, ACID, "", lg); c.drawString("ACID", 326, 1449, f, paint(INK, 0.7 * lg))
        ion(c, 560, 1440, 16, CALC, "", lg); c.drawString("CALCIUM", 586, 1449, f, paint(INK, 0.7 * lg))
    pill(c, t, "A NATURAL ACID", 495, 560, "#5E9E1E", ACIDt, CHEW - 0.05)
    pill(c, t, "YOU CHEW...", 495, 560, "#8a8f98", CHEW, CALt - 0.05)
    pill(c, t, "+ CALCIUM IN SPIT", 495, 560, "#2A9ED6", CALt, LOCK - 0.05)
    pill(c, t, "= TINY CRYSTALS", 495, 560, "#6F7FA0", LOCK, NODIS - 0.05)
    pill(c, t, "DON'T DISSOLVE", 495, 560, "#2A9ED6", NODIS, STICK - 0.05)
    pill(c, t, "STICK TO TEETH", 495, 560, "#6F7FA0", STICK, WIPE2 + 0.1)


# ---------------- dark: grit close-up, safe, dairy, lemon, veggie ----------------
def cheese(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-110, 60); p.lineTo(110, 60); p.lineTo(110, -20); p.lineTo(-110, -60); p.close()
    c.drawPath(p, paint("#000000", 0.25 * a, blur=10))
    c.drawPath(p, paint(shader=linear((0, -60), (0, 60), [col("#FFE08A", a), col(CHEESE, a)])))
    for (hx, hy, r) in ((-50, 10, 14), (20, 30, 10), (60, -2, 12), (-10, -18, 7)):
        c.drawCircle(hx, hy, r, paint("#E0A800", a))
    c.restore()


def milk(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    g = skia.Path(); g.moveTo(-60, -110); g.lineTo(60, -110); g.lineTo(48, 110); g.lineTo(-48, 110); g.close()
    c.drawPath(g, paint("#000000", 0.25 * a, blur=10))
    c.drawPath(g, paint("#ffffff", 0.25 * a))
    m = skia.Path(); m.moveTo(-56, -60); m.lineTo(56, -60); m.lineTo(48, 110); m.lineTo(-48, 110); m.close()
    c.drawPath(m, paint("#FBFBF6", a))
    c.drawPath(g, paint("#ffffff", 0.8 * a, stroke=4))
    c.restore()


def lemon(c, x, y, s, rot, a, squeeze=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * (1 + 0.1 * squeeze), s * (1 - 0.15 * squeeze))
    c.drawOval(skia.Rect.MakeLTRB(-120, -78, 120, 78), paint("#000000", 0.25 * a, blur=12))
    c.drawOval(skia.Rect.MakeLTRB(-120, -78, 120, 78), paint(shader=radial(-30, -30, 160, [col("#FFF28A", a), col(LEMON, a), col("#E0B800", a)], [0, 0.5, 1])))
    c.drawCircle(-124, 0, 14, paint("#E0B800", a))
    c.drawOval(skia.Rect.MakeLTRB(80, -70, 140, 70), paint("#FFF6B0", a))
    for k in range(6):
        an = k * math.pi / 3
        c.drawLine(110, 0, 110 + 24 * math.cos(an), 60 * math.sin(an), paint("#F2D64B", a, stroke=4))
    c.restore()


def scene_grit(c, t):
    bg_dark(c, t)
    a = eout(prog(t, WIPE2, 0.4))
    dairy = eio(prog(t, DAIRY - 0.1, 0.4))
    more = eout(prog(t, MORE - 0.1, 0.5))
    lem = eio(prog(t, LEM - 0.1, 0.4))
    cuts = eout(prog(t, CUTS - 0.1, 0.9))
    film = clamp(0.75 + 0.6 * more - 0.9 * cuts)
    zoom = lerp(1.7, 1.15, eio(prog(t, RELAX - 0.1, 0.6)))
    ty = lerp(820, 1000, eio(prog(t, RELAX - 0.1, 0.6)))
    teeth(c, t, 495, ty, zoom, film=film, a=a, shine=cuts)
    # finger swipe on "grit"
    sw = window(t, GRIT - 0.1, RELAX, 0.15, 0.2) * a
    if sw > 0:
        u = ((t - GRIT) * 1.6) % 1.0
        fx = lerp(220, 780, eio(u)); fy = 1100
        c.drawRoundRect(skia.Rect.MakeLTRB(fx - 60, fy - 40, fx + 60, fy + 260), 60, 60, paint("#E8A07A", sw))
        c.drawRoundRect(skia.Rect.MakeLTRB(fx - 42, fy - 22, fx + 42, fy + 50), 30, 30, paint("#FFD9C6", sw))
        for k in range(3):
            c.drawLine(fx - 90 - k * 25, fy - 70 + k * 30, fx - 120 - k * 25, fy - 90 + k * 30, paint("#ffffff", 0.7 * sw, stroke=6))
    # safe shield
    sa = eback(prog(t, DMG - 0.1, 0.35)) * (1 - prog(t, DAIRY - 0.2, 0.25)) * a
    if sa > 0:
        c.save(); c.translate(495, 1400); c.scale(sa, sa)
        sh = skia.Path(); sh.moveTo(0, -90); sh.lineTo(80, -60); sh.lineTo(70, 30); sh.quadTo(40, 80, 0, 100); sh.quadTo(-40, 80, -70, 30); sh.lineTo(-80, -60); sh.close()
        c.drawPath(sh, paint("#000000", 0.3, blur=10)); c.drawPath(sh, paint(GREEN))
        ck = skia.Path(); ck.moveTo(-32, 0); ck.lineTo(-8, 26); ck.lineTo(36, -26)
        c.drawPath(ck, paint("#ffffff", 1, stroke=14))
        c.restore()
    # dairy -> more calcium
    da = dairy * (1 - prog(t, TRICK - 0.2, 0.25)) * a
    if da > 0:
        cheese(c, 280, lerp(1500, 1380, dairy), 0.9, da)
        milk(c, 720, lerp(1500, 1360, dairy), 0.85, da)
        if t > MORECA - 0.1:
            for k in range(12):
                rr = random.Random(500 + k)
                u = ((t - MORECA) * 0.9 + rr.random()) % 1.0
                sx = 280 if k % 2 == 0 else 720
                bx = lerp(sx, rr.uniform(320, 680), u); by = lerp(1330, rr.uniform(980, 1150), u)
                ion(c, bx, by, 14, CALC, "", da * math.sin(math.pi * u))
    # lemon squeeze
    la = window(t, LEM - 0.2, VEG, 0.25, 0.25) * a
    if la > 0:
        sq = 0.5 + 0.5 * math.sin(t * 8)
        lemon(c, 780, 1380, 0.85, -25, la, sq)
        for k in range(7):
            u = ((t - LEM) * 1.4 + k / 7) % 1.0
            dx = lerp(700, 400 + 60 * math.sin(k * 2.1), u); dy = lerp(1330, 1150, u)
            c.drawCircle(dx, dy, 10, paint(LEMON, la * (1 - u)))
    # spinach "acid king": big leaf with a crown, other veggies small and dim (no invented numbers)
    va = eout(prog(t, VEG - 0.1, 0.4)) * a
    if va > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#0b0f0c", 0.93 * va))
        for k, (x, cc) in enumerate(((170, "#9BD37A"), (330, ORANGE), (660, "#4E9F3D"), (820, "#C0392B"))):
            q = eback(prog(t, VEG + k * 0.08, 0.35)) * va
            if q <= 0: continue
            c.save(); c.translate(x, 1330 + 8 * math.sin(t * 2 + k)); c.scale(q, q)
            c.drawCircle(0, 0, 52, paint(cc, 0.45))
            for j in range(3):
                ion(c, -20 + j * 20, -70, 7, ACID, "", 0.6)
            c.restore()
        g = eback(prog(t, VEG2 - 0.15, 0.4))
        leaf(c, t, 495, 1040 + 10 * math.sin(t * 3), 0.85 * clamp(g, 0, 1.2), -6 + 4 * math.sin(t * 2), va, glow=1.0)
        if g > 0:
            for k in range(14):
                rr = random.Random(700 + k)
                an = rr.uniform(0, 6.28) + t * 0.6
                rad = 230 + 30 * math.sin(t * 3 + k)
                ion(c, 495 + rad * math.cos(an), 1040 + rad * math.sin(an), 12, ACID, "", va * clamp(g))
            # crown
            c.save(); c.translate(495, 820 + 6 * math.sin(t * 4)); c.scale(clamp(g), clamp(g))
            cr = skia.Path(); cr.moveTo(-80, 40); cr.lineTo(-90, -40); cr.lineTo(-40, 0); cr.lineTo(0, -60); cr.lineTo(40, 0); cr.lineTo(90, -40); cr.lineTo(80, 40); cr.close()
            c.drawPath(cr, paint("#000000", 0.3, blur=8)); c.drawPath(cr, paint(CHEESE)); c.drawPath(cr, paint("#C99700", 1, stroke=4))
            c.restore()
    pill(c, t, "THE GRIT!", 495, 560, "#6F7FA0", GRIT, RELAX - 0.05)
    pill(c, t, "RELAX...", 495, 560, GREEN, RELAX, DMG - 0.05, text_col="#FFFFFF")
    pill(c, t, "NO DAMAGE", 495, 560, GREEN, DMG, DAIRY - 0.05, text_col="#FFFFFF")
    pill(c, t, "MILK OR CHEESE?", 495, 560, "#C9A100", DAIRY, MORECA - 0.05, text_col="#FFFFFF")
    pill(c, t, "MORE CALCIUM", 495, 560, "#2A9ED6", MORECA, MORE - 0.05)
    pill(c, t, "MORE GRIT", 495, 560, "#6F7FA0", MORE, TRICK - 0.05)
    pill(c, t, "THE TRICK", 495, 560, "#8a8f98", TRICK, LEM - 0.05)
    pill(c, t, "LEMON ON TOP", 495, 560, "#C9A100", LEM, VEG - 0.05, text_col="#FFFFFF")
    pill(c, t, "MOST ACID", 495, 560, "#5E9E1E", VEG2, SO + 0.3)


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_lab(c, t); return
    if t < SO - 0.05:
        scene_grit(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_grit(c, t); c.restore()


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


KWCOL = {"squeaky": SPIN, "chalky": "#B8C6DE", "acid": ACID, "calcium": CALC, "crystals": "#B8C6DE", "stick": "#B8C6DE",
         "grit": "#B8C6DE", "damage": GREEN, "cheese": CHEESE, "more": CALC, "lemon": LEMON, "veggie": SPIN}
CAPS = Captions(split_long(P), KWCOL, {"crystals", "grit!"}, DUR)


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
    wipe(c, t, WIPE1, WL, SPIN, "#F4F2EE")
    wipe(c, t, WIPE2, WL, CALC, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("hit", CHALK), ("pop", GRIT1), ("pop", DIRT),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", ACIDt), ("whoosh", CHEW), ("pop", CALt), ("hit", LOCK),
          ("pop", NODIS), ("pop", STICK), ("whoosh", WIPE2), ("pop", GRIT), ("pop", RELAX), ("ding", DMG),
          ("pop", DAIRY), ("pop", MORECA), ("hit", MORE), ("whoosh", TRICK), ("pop", LEM), ("ding", CUTS),
          ("riser", VEG - 0.1), ("pop", VEG2), ("whoosh", SO - 0.05)]
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

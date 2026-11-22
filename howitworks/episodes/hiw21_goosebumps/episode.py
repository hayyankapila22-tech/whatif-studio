# HIW21 — "Why do you get goosebumps?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-23):
#  - Live Science, "Why do we get goosebumps?" (livescience.com/32349-what-causes-goose-bumps.html, 2022): tiny muscles
#    under the skin, "one for each hair on the body", raise the hair and form a goosebump; common when cold, scared or
#    inspired / other strong emotions; in furry animals it fluffs fur into a thick layer of insulation and makes them
#    look larger when threatened (chimpanzees named); in humans "it really doesn't do anything" — a vestigial trait.
#  - Popular Science, "The evolutionary mystery of goosebumps" (2018): the muscle at each hair root contracts and the
#    hair stands up; triggers incl. cold, fear and music; part of the fight-or-flight response, adrenaline triggers
#    goosebumps; fluffed hair traps a layer of air close to the skin.
#  - Cats puffing their fur when frightened (piloerection) = common knowledge, same reflex.
#  Plain words: arrector pili = "tiny muscle", piloerection = "fluffed-up fur", adrenaline = "a big rush".
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
SKIN = "#E9B08A"; SKIN_L = "#F7CFAE"; SKIN_D = "#C4835E"; HAIR = "#4A2F1F"; MUS = "#E0525F"
COLD = "#7CC8FF"; RUSH = "#FFC93D"; FUR = "#E39A52"; FUR_D = "#B86E2E"; WARM = "#FF9F43"; GREEN = "#1fb98a"


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


GB = kw(ph("why do you")); AIR = p0(ph("cold air")); MOVIE = p0(ph("a scary")); SONG = kw(ph("your favourite"))
WIPE1 = p0(ph("okay")) - 0.3; EVERY = p0(ph("every hair")); MUSCLE = kw(ph("has its own"))
SQZ = kw(ph("when it")); STAND = p0(ph("the hair stands")); BUMP = kw(ph("and pulls"))
OWN = p0(ph("it happens")); COLDt = kw(ph("when you're")); RUSHt = kw(ph("or feel"))
WIPE2 = p0(ph("but why")) - 0.3; FURRY = kw(ph("our ancestors")); FLUFF = p0(ph("fluffed")); WARMt = kw(ph("fluffed"))
BIG = kw(ph("and makes")); CAT = p0(ph("ever seen")); PUFF = kw(ph("ever seen")); SAME = p0(ph("same trick"))
LOST = p0(ph("we lost")); KEPT = kw(ph("but kept")); SO = p0(len(P) - 1)
WL = 0.32
IMPACTS = [MUSCLE, BUMP, PUFF, KEPT]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1, ph_=0.0):
    return math.sin(2 * math.pi * k * t / DUR + ph_)


def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#211915"), col("#15100d"), col("#090706")], [0, 0.55, 1])))
    c.drawCircle(780 + 30 * lw(t), 700, 520, paint(shader=radial(780, 700, 520, [col(WARM, 0.10), col(WARM, 0)])))
    c.drawCircle(220, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1450, 600, [col(COLD, 0.06), col(COLD, 0)])))


# ---------------- skin landscape (close-up of an arm) ----------------
def skin_land(c, t, ybase, s, bump, a=1.0, hair_a=1.0):
    """three rows of skin seen low and close; each hair sits on a bump that rises with `bump`."""
    if a <= 0: return
    for r in range(3):
        depth = 2 - r                       # 2 = back row
        yr = ybase - depth * 150 * s
        sc = s * (1 - 0.22 * depth)
        off = (r * 97) % 180
        fxs = [x for x in range(-120 + off, 1240, int(220 * sc))]
        shade = 1 - 0.18 * depth

        def ys(x):
            y = yr
            for k, fx in enumerate(fxs):
                bk = bump * (0.85 + 0.15 * math.sin(k * 1.7 + r))
                y -= bk * 85 * sc * math.exp(-((x - fx) / (60 * sc)) ** 2)
            return y
        p = skia.Path(); p.moveTo(-60, H + 50)
        for x in range(-60, W + 70, 10):
            p.lineTo(x, ys(x))
        p.lineTo(W + 60, H + 50); p.close()
        c.drawPath(p, paint(shader=linear((0, yr - 60 * sc), (0, yr + 260 * sc),
                                         [col(mixhex(SKIN_L, "#3a2a22", 1 - shade), a), col(mixhex(SKIN, "#2a1d17", 1 - shade), a), col(mixhex(SKIN_D, "#1a120e", 1 - shade), a)], [0, 0.4, 1])))
        edge = skia.Path(); edge.moveTo(-60, ys(-60))
        for x in range(-60, W + 70, 10):
            edge.lineTo(x, ys(x))
        c.drawPath(edge, paint("#FFE6D2", 0.45 * a * shade, stroke=3 * sc))
        # skin texture: tiny crease lines
        for k in range(16):
            rr = random.Random(r * 100 + k)
            x = rr.uniform(0, W); y = ys(x) + rr.uniform(30, 200) * sc
            c.drawLine(x - 18 * sc, y, x + 18 * sc, y + rr.uniform(-4, 4), paint(SKIN_D, 0.35 * a, stroke=2))
        # hairs
        for k, fx in enumerate(fxs):
            bk = bump * (0.85 + 0.15 * math.sin(k * 1.7 + r))
            y0 = ys(fx)
            c.drawOval(skia.Rect.MakeLTRB(fx - 34 * sc, y0 + 2 * sc, fx - 4 * sc, y0 + 40 * sc), paint("#FFF1E4", 0.35 * a * bk * shade, blur=8 * sc))
            c.drawOval(skia.Rect.MakeLTRB(fx - 9 * sc, y0 - 4 * sc, fx + 9 * sc, y0 + 5 * sc), paint("#7a4a33", 0.6 * a))
            ang = math.radians(lerp(72, 6, bk) + 4 * math.sin(t * 2 + k + r))
            L = 175 * sc
            ex, ey = fx + L * math.sin(ang), y0 - L * math.cos(ang)
            hp = skia.Path(); hp.moveTo(fx, y0)
            hp.quadTo(fx + L * 0.5 * math.sin(ang) - 12 * sc * math.cos(ang), y0 - L * 0.5 * math.cos(ang) - 10 * sc, ex, ey)
            c.drawPath(hp, paint(HAIR, 0.95 * a * hair_a, stroke=6 * sc))
            c.drawPath(hp, paint("#a77a5a", 0.35 * a * hair_a, stroke=1.5 * sc))


def snowflake(c, x, y, s, a, rot=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for k in range(6):
        c.save(); c.rotate(k * 60)
        c.drawLine(0, 0, 0, -70, paint(COLD, a, stroke=9))
        c.drawLine(0, -42, -18, -58, paint(COLD, a, stroke=7)); c.drawLine(0, -42, 18, -58, paint(COLD, a, stroke=7))
        c.restore()
    c.drawCircle(0, 0, 12, paint("#ffffff", a))
    c.restore()


def clapper(c, x, y, s, a, open_=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-75, -30, 75, 65), 10, 10, paint("#2b2b33", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-75, -30, 75, 65), 10, 10, paint("#ffffff", 0.8 * a, stroke=4))
    c.save(); c.translate(-75, -32); c.rotate(-25 * open_)
    c.drawRect(skia.Rect.MakeLTRB(0, -28, 150, 0), paint("#ffffff", a))
    for k in range(5):
        q = skia.Path(); q.moveTo(8 + k * 30, -28); q.lineTo(24 + k * 30, -28); q.lineTo(12 + k * 30, 0); q.lineTo(-4 + k * 30, 0); q.close()
        c.drawPath(q, paint("#2b2b33", a))
    c.restore(); c.restore()


def note(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeLTRB(-46, 20, 6, 58), paint("#B48CFF", a))
    c.drawOval(skia.Rect.MakeLTRB(34, 4, 86, 42), paint("#B48CFF", a))
    c.drawLine(2, 38, 2, -70, paint("#B48CFF", a, stroke=10)); c.drawLine(82, 22, 82, -86, paint("#B48CFF", a, stroke=10))
    c.drawLine(2, -70, 82, -86, paint("#B48CFF", a, stroke=20))
    c.restore()


def bolt(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    b = skia.Path(); b.moveTo(10, -80); b.lineTo(-40, 10); b.lineTo(0, 10); b.lineTo(-14, 80); b.lineTo(42, -14); b.lineTo(4, -14); b.close()
    c.drawPath(b, paint(RUSH, 0.4 * a, blur=14)); c.drawPath(b, paint(RUSH, a)); c.drawPath(b, paint("#ffffff", 0.7 * a, stroke=3))
    c.restore()


def hook_bump(t):
    return 0.78 + 0.22 * lw(t, 3)


def scene_hook(c, t):
    bg_dark(c, t)
    skin_land(c, t, 1270 + 12 * lw(t, 2), 1.45, hook_bump(t))


def scene_open(c, t):
    bg_dark(c, t)
    spike = max(window(t, AIR, AIR + 0.5, 0.1, 0.3), window(t, MOVIE, MOVIE + 0.5, 0.1, 0.3), window(t, SONG - 0.1, SONG + 0.5, 0.1, 0.3))
    skin_land(c, t, 1270 + 12 * lw(t, 2), 1.45 + 0.08 * eio(prog(t, AIR - 0.2, 1.5)), clamp(hook_bump(t) + 0.25 * spike))
    out = 1 - prog(t, WIPE1 - 0.1, 0.2)
    for k, (tt, fn) in enumerate(((AIR, "snow"), (MOVIE, "clap"), (SONG - 0.1, "note"))):
        q = eback(prog(t, tt - 0.05, 0.3)) * out
        if q <= 0: continue
        x = 230 + k * 265; y = 715 + 10 * math.sin(t * 3 + k)
        c.drawCircle(x, y, 88 * q, paint("#000000", 0.35 * out, blur=10)); c.drawCircle(x, y, 88 * q, paint("#2a211c", 0.9 * out)); c.drawCircle(x, y, 88 * q, paint("#ffffff", 0.3 * out, stroke=3))
        if fn == "snow": snowflake(c, x, y, 0.8 * q, out, rot=t * 30)
        elif fn == "clap": clapper(c, x, y + 10, 0.72 * q, out, open_=0.5 + 0.5 * math.sin(t * 9))
        else: note(c, x - 18, y + 14, 0.72 * q, out)
    pill(c, t, "GOOSEBUMPS?", 495, 560, FUR_D, 0.35, AIR - 0.05)
    pill(c, t, "COLD AIR", 495, 560, "#2A9ED6", AIR, MOVIE - 0.05)
    pill(c, t, "A SCARY MOVIE", 495, 560, "#5a5a66", MOVIE, SONG - 0.15)
    pill(c, t, "YOUR SONG", 495, 560, "#8C6BE0", SONG - 0.1, WIPE1 + 0.1)


# ---------------- white: cut-away skin with hair + tiny muscle ----------------
SURF = 900


def squeeze(t):
    s = eio(prog(t, SQZ - 0.1, 0.45)) * (1 - 0.75 * eio(prog(t, OWN, 0.5)))
    s = max(s, eio(prog(t, COLDt - 0.15, 0.35)), window(t, RUSHt - 0.15, WIPE2 + 0.5, 0.2, 0.3))
    return s


def section(c, t, a, sq, show_mus, glow):
    L, R, B = 100, 890, 1440
    fxs = (260, 490, 720)
    def surf_y(x):
        y = SURF
        for fx in fxs:
            y -= 48 * sq * math.exp(-((x - (fx + 40)) / 60) ** 2)
        return y
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(L, SURF - 300, R, B), 36, 36), doAntiAlias=True)
    # block
    p = skia.Path(); p.moveTo(L, B)
    for x in range(L, R + 10, 8): p.lineTo(x, surf_y(x))
    p.lineTo(R, B); p.close()
    c.drawPath(p, paint(shader=linear((0, SURF), (0, B), [col("#F6CBA8", a), col("#EBB08F", a), col("#E59A86", a), col("#F2C7A0", a)], [0, 0.12, 0.6, 1])))
    # layer line + fat dots
    lay = skia.Path(); lay.moveTo(L, SURF + 60)
    for x in range(L, R + 10, 8): lay.lineTo(x, surf_y(x) + 60)
    c.drawPath(lay, paint("#C9806A", 0.5 * a, stroke=3))
    for k in range(14):
        rr = random.Random(900 + k)
        c.drawCircle(rr.uniform(L + 30, R - 30), rr.uniform(1340, 1430), rr.uniform(18, 30), paint("#FFE2A8", 0.7 * a))
    # top edge
    e = skia.Path(); e.moveTo(L, surf_y(L))
    for x in range(L, R + 10, 8): e.lineTo(x, surf_y(x))
    c.drawPath(e, paint("#FFF0E2", 0.9 * a, stroke=5))
    c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(L, SURF - 300, R, B), 36, 36), paint(INK, 0.0))
    for k, fx in enumerate(fxs):
        sy = surf_y(fx)
        ang = lerp(-28, -3, sq) + 2 * math.sin(t * 2 + k)       # follicle tilt (degrees)
        c.save(); c.translate(fx, sy); c.rotate(ang)
        # follicle sheath + bulb
        c.drawRoundRect(skia.Rect.MakeLTRB(-20, 0, 20, 300), 20, 20, paint("#C97762", 0.9 * a))
        c.drawCircle(0, 305, 38, paint(shader=radial(-10, 295, 40, [col("#E89A7E", a), col("#B65F4B", a)])))
        c.drawLine(0, 300, 0, -230, paint(HAIR, a, stroke=9))
        c.drawLine(-2, -40, -2, -220, paint("#9a6a4a", 0.5 * a, stroke=2.5))
        c.restore()
        # muscle: from follicle mid (rotated) to an anchor just under the skin
        if show_mus > 0:
            r = math.radians(ang)
            mx0 = fx - 190 * math.sin(r) - 16 * math.cos(r)
            my0 = sy + 190 * math.cos(r) - 16 * math.sin(r)
            ax, ay = fx - 120, SURF + 55
            th = lerp(28, 44, sq)
            mp = skia.Path(); mp.moveTo(mx0, my0)
            mx, my = (mx0 + ax) / 2, (my0 + ay) / 2
            mp.quadTo(mx - 10, my + 18 * (1 - sq), ax, ay)
            q = show_mus
            c.drawPath(mp, paint(MUS, 0.35 * glow * a * q, stroke=th + 26, blur=12))
            c.drawPath(mp, paint(shader=linear((mx0, my0), (ax, ay), [col("#C23B48", a * q), col(MUS, a * q), col("#F07A84", a * q)]), stroke=th))
            for j in range(4):
                u = (j + 1) / 5
                c.drawLine(lerp(mx0, ax, u) - 6, lerp(my0, ay, u) - 8, lerp(mx0, ax, u) + 6, lerp(my0, ay, u) + 8, paint("#ffffff", 0.35 * a * q, stroke=2))


def scene_lab(c, t):
    studio_white(c)
    a = eout(prog(t, WIPE1, 0.4))
    sq = squeeze(t)
    mus = eback(prog(t, MUSCLE - 0.1, 0.35))
    glow = 0.4 + 0.6 * max(window(t, MUSCLE - 0.1, MUSCLE + 0.8, 0.1, 0.4), sq)
    zoom = lerp(1.08, 1.0, eio(prog(t, WIPE1, 1.2)))
    c.save(); c.translate(495, 1100); c.scale(zoom, zoom); c.translate(-495, -1100)
    section(c, t, a, sq, mus, glow)
    c.restore()
    # "every hair" highlight rings
    ev = window(t, EVERY, MUSCLE + 0.2, 0.2, 0.3) * a
    for k, fx in enumerate((260, 490, 720)):
        q = eback(prog(t, EVERY + k * 0.12, 0.3)) * ev
        if q > 0:
            c.drawCircle(fx, 760, 46 * q, paint(FUR_D, 0.9 * ev, stroke=5))
            f = skia.Font(TF_MONO, 30); s = str(k + 1)
            c.drawString(s, fx - f.measureText(s) / 2, 771, f, paint(FUR_D, ev))
    # bump arrows on "bump"
    ba = window(t, BUMP - 0.1, OWN + 0.2, 0.15, 0.3) * a
    for fx in (260, 490, 720):
        if ba > 0:
            yy = SURF - 70 - 16 * math.sin(t * 8)
            c.drawLine(fx + 40, yy, fx + 40, yy - 50, paint(INK, 0.7 * ba, stroke=5))
            ar = skia.Path(); ar.moveTo(fx + 24, yy - 40); ar.lineTo(fx + 40, yy - 62); ar.lineTo(fx + 56, yy - 40)
            c.drawPath(ar, paint(INK, 0.7 * ba, stroke=5))
    # triggers
    sa = window(t, COLDt - 0.2, RUSHt - 0.05, 0.25, 0.2) * a
    snowflake(c, 790, 700, 0.7 * eback(prog(t, COLDt - 0.2, 0.3)), sa, rot=t * 40)
    ra = window(t, RUSHt - 0.2, WIPE2 + 0.3, 0.25, 0.2) * a
    bolt(c, 790, 700, 0.9 * eback(prog(t, RUSHt - 0.2, 0.3)), ra)
    # "on its own" auto badge
    oa = window(t, OWN, COLDt - 0.1, 0.2, 0.2) * a
    if oa > 0:
        c.save(); c.translate(790, 700); c.rotate(t * 90)
        for k in range(8):
            c.save(); c.rotate(k * 45); c.drawRect(skia.Rect.MakeLTRB(-14, -78, 14, -50), paint("#8a8f98", oa)); c.restore()
        c.drawCircle(0, 0, 58, paint("#8a8f98", oa)); c.drawCircle(0, 0, 24, paint("#F4F2EE", oa))
        c.restore()
    pill(c, t, "EVERY HAIR", 495, 560, FUR_D, EVERY, MUSCLE - 0.05)
    pill(c, t, "ITS OWN TINY MUSCLE", 495, 560, MUS, MUSCLE, SQZ - 0.05)
    pill(c, t, "SQUEEZE!", 495, 560, MUS, SQZ, STAND - 0.05)
    pill(c, t, "HAIR STANDS UP", 495, 560, "#6b4a35", STAND, BUMP - 0.05)
    pill(c, t, "= A LITTLE BUMP", 495, 560, FUR_D, BUMP, OWN - 0.05)
    pill(c, t, "ON ITS OWN", 495, 560, "#8a8f98", OWN, COLDt - 0.05)
    pill(c, t, "COLD", 495, 560, "#2A9ED6", COLDt, RUSHt - 0.05)
    pill(c, t, "A BIG RUSH", 495, 560, "#D9A400", RUSHt, WIPE2 + 0.1, text_col="#FFFFFF")


# ---------------- dark: furry ancestors, cat puff, lost the fur ----------------
def cat(c, t, x, y, s, puff, a, warm=0.0, arch=0.0, scared=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Path()
    body.moveTo(-210, 30)
    body.cubicTo(-220, -80 - 90 * arch, 150, -110 - 90 * arch, 200, -20)
    body.cubicTo(230, 60, 120, 110, 0, 110)
    body.cubicTo(-150, 110, -205, 90, -210, 30)
    head = skia.Path(); head.addCircle(250, -110 - 40 * arch, 88)
    ears = skia.Path()
    hy = -110 - 40 * arch
    ears.moveTo(190, hy - 50); ears.lineTo(200, hy - 140); ears.lineTo(250, hy - 80); ears.close()
    ears.moveTo(260, hy - 82); ears.lineTo(310, hy - 140); ears.lineTo(325, hy - 50); ears.close()
    tail = skia.Path(); tail.moveTo(-200, 10); tail.cubicTo(-320, -20, -330, -200, -260, -260)
    legs = [(-150, 60), (-90, 70), (90, 70), (150, 60)]
    fl = lerp(6, 58, puff)
    sil = skia.Path(); sil.addPath(body); sil.addPath(head); sil.addPath(ears)
    # warm air layer
    if warm > 0:
        c.drawPath(sil, paint(WARM, 0.55 * warm * a, stroke=2 * fl + 40, blur=22))
        c.drawPath(tail, paint(WARM, 0.45 * warm * a, stroke=40 + 3 * fl, blur=22))
    c.drawPath(sil, paint("#000000", 0.3 * a, blur=16))
    for lx, ly in legs:
        c.drawRoundRect(skia.Rect.MakeLTRB(lx - 22, ly, lx + 22, ly + 120 + 30 * arch), 20, 20, paint(FUR_D, a))
    # fuzzy outline that grows with puff
    c.drawPath(sil, paint(FUR, 0.55 * a, stroke=fl * 1.6, blur=fl * 0.35 + 1))
    c.drawPath(tail, paint(FUR, a, stroke=30 + 3.2 * fl, blur=fl * 0.3 + 1))
    c.drawPath(sil, paint(shader=radial(60, -60, 340, [col("#F2B573", a), col(FUR, a), col(FUR_D, a)], [0, 0.6, 1])))
    # stripes
    for k in range(5):
        sx = -120 + k * 60
        c.drawLine(sx, -60 - 70 * arch + abs(sx) * 0.1, sx + 20, 10, paint(FUR_D, 0.6 * a, stroke=12))
    # fur strands around the back and tail
    pm = skia.PathMeasure(body, False)
    Lb = pm.getLength()
    for k in range(46):
        d = Lb * k / 46
        pos, tan = pm.getPosTan(d)
        if pos.y() > 30: continue
        nx, ny = tan.y(), -tan.x()
        ln = fl * (0.7 + 0.5 * math.sin(k * 2.3)) * (1 + 0.05 * math.sin(t * 8 + k))
        c.drawLine(pos.x(), pos.y(), pos.x() + nx * ln, pos.y() + ny * ln, paint(FUR, a, stroke=7))
    # face
    ex = 280; ey = hy - 10
    er = lerp(12, 20, scared)
    c.drawCircle(ex - 40, ey, er, paint("#1b1b1b", a)); c.drawCircle(ex + 20, ey, er, paint("#1b1b1b", a))
    c.drawCircle(ex - 44, ey - 5, er * 0.35, paint("#ffffff", a)); c.drawCircle(ex + 16, ey - 5, er * 0.35, paint("#ffffff", a))
    c.drawCircle(ex - 8, ey + 30, 8, paint("#E77B8A", a))
    for sgn in (-1, 1):
        c.drawLine(ex + 30, ey + 36 + sgn * 6, ex + 100, ey + 30 + sgn * 18, paint("#ffffff", 0.7 * a, stroke=3))
    c.restore()


def scene_fur(c, t):
    bg_dark(c, t)
    a = eout(prog(t, WIPE2, 0.4))
    lost = eio(prog(t, LOST - 0.1, 0.7))
    # question mark
    qa = window(t, WIPE2 + 0.1, FURRY, 0.2, 0.25) * a
    if qa > 0:
        f = skia.Font(TF_BLACK, 300)
        q = eback(prog(t, WIPE2 + 0.1, 0.35))
        c.save(); c.translate(495, 1050); c.scale(q, q); c.rotate(6 * math.sin(t * 4))
        c.drawString("?", -f.measureText("?") / 2, 100, f, paint(RUSH, qa))
        c.restore()
    appear = eback(prog(t, FURRY - 0.15, 0.4))
    puff = clamp(0.25 + 0.75 * eio(prog(t, FLUFF - 0.1, 0.6)) - 0.5 * eio(prog(t, BIG + 0.9, 0.4)) + 0.5 * eio(prog(t, PUFF - 0.15, 0.35)))
    warm = window(t, WARMt - 0.15, BIG + 0.8, 0.3, 0.3)
    big = eio(prog(t, BIG - 0.1, 0.5)) * (1 - eio(prog(t, BIG + 0.9, 0.4)))
    arch = eio(prog(t, PUFF - 0.15, 0.35))
    s = 1.0 * (1 + 0.16 * big + 0.1 * arch) * appear
    ca = a * (1 - lost) * clamp(appear)
    cx = lerp(470, 300, lost); cy = 1060 + 8 * math.sin(t * 2)
    if ca > 0:
        if big > 0:
            # ghost outline of the normal size
            gp = paint("#ffffff", 0.35 * big * ca, stroke=4)
            gp.setPathEffect(skia.DashPathEffect.Make([18, 14], t * 40))
            c.drawOval(skia.Rect.MakeLTRB(cx - 250, cy - 180, cx + 340, cy + 200), gp)
        cat(c, t, cx, cy, 0.95 * s, puff, ca, warm=warm, arch=arch, scared=arch)
        # warm-air label arrows
        if warm > 0:
            for k in range(6):
                u = ((t * 0.7 + k / 6) % 1.0)
                an = -2.4 + k * 0.5
                rx = cx + 60 + 330 * math.cos(an); ry = cy - 40 + 260 * math.sin(an)
                c.drawCircle(rx, ry - 30 * u, 10, paint(WARM, 0.6 * warm * ca * math.sin(math.pi * u)))
    # tick for "same trick"
    ta = window(t, SAME - 0.05, LOST + 0.1, 0.2, 0.2) * a
    if ta > 0:
        q = eback(prog(t, SAME - 0.05, 0.3))
        c.save(); c.translate(800, 760); c.scale(q, q)
        c.drawCircle(0, 0, 62, paint(GREEN, ta))
        ck = skia.Path(); ck.moveTo(-26, 0); ck.lineTo(-6, 22); ck.lineTo(30, -22)
        c.drawPath(ck, paint("#ffffff", ta, stroke=12))
        c.restore()
    # lost the fur -> human skin with bumps comes back
    if lost > 0:
        kb = eout(prog(t, KEPT - 0.1, 0.4))
        skin_land(c, t, lerp(1900, 1270, lost) + 12 * lw(t, 2), 1.45, clamp(0.2 + 0.8 * kb) if t < SO else hook_bump(t), a * lost)
        # falling fur strands
        for k in range(18):
            rr = random.Random(1200 + k)
            u = clamp((t - LOST) * 0.8 - rr.random() * 0.3)
            if 0 < u < 1:
                fx = rr.uniform(200, 800); fy = lerp(800, 1500, u)
                c.save(); c.translate(fx, fy); c.rotate(rr.uniform(0, 180) + u * 200)
                c.drawLine(-20, 0, 20, 0, paint(FUR, (1 - u) * a, stroke=6)); c.restore()
    pill(c, t, "BUT WHY?", 495, 560, "#5a5a66", WIPE2 + 0.1, FURRY - 0.05)
    pill(c, t, "FURRY ANCESTORS", 495, 560, FUR_D, FURRY, FLUFF - 0.05)
    pill(c, t, "FLUFFED-UP FUR", 495, 560, FUR_D, FLUFF, WARMt - 0.05)
    pill(c, t, "TRAPS WARM AIR", 495, 560, "#E07B1A", WARMt, BIG - 0.05, text_col="#FFFFFF")
    pill(c, t, "LOOKS BIGGER", 495, 560, "#5a5a66", BIG, CAT - 0.05)
    pill(c, t, "SCARED CAT = PUFF", 495, 560, FUR_D, PUFF - 0.1, SAME - 0.05)
    pill(c, t, "SAME TRICK!", 495, 560, GREEN, SAME, LOST - 0.05, text_col="#FFFFFF")
    pill(c, t, "FUR: GONE", 495, 560, "#5a5a66", LOST, KEPT - 0.05)
    pill(c, t, "BUMPS: KEPT", 495, 560, FUR_D, KEPT, SO + 0.3)


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_lab(c, t); return
    if t < SO - 0.05:
        scene_fur(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_fur(c, t); c.restore()


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


KWCOL = {"goosebumps": FUR, "song": "#B48CFF", "muscle": MUS, "squeezes": MUS, "bump": FUR, "cold": COLD, "rush": RUSH,
         "furry": FUR, "warm": WARM, "bigger": FUR, "puff": FUR, "bumps": FUR}
CAPS = Captions(split_long(P), KWCOL, {"furry!", "bumps!"}, DUR)


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
    wipe(c, t, WIPE1, WL, FUR, "#F4F2EE")
    wipe(c, t, WIPE2, WL, MUS, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("pop", AIR), ("pop", MOVIE), ("pop", SONG),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", EVERY), ("hit", MUSCLE), ("pop", SQZ), ("whoosh", STAND),
          ("hit", BUMP), ("pop", OWN), ("pop", COLDt), ("pop", RUSHt), ("whoosh", WIPE2), ("pop", WIPE2 + 0.15),
          ("pop", FURRY), ("pop", FLUFF), ("ding", WARMt), ("whoosh", BIG), ("hit", PUFF), ("ding", SAME),
          ("whoosh", LOST), ("hit", KEPT), ("whoosh", SO - 0.05)]
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

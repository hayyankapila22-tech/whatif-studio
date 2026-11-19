# HIW12 — "Try to tickle yourself. Go on!" Why you can't tickle yourself. Bubbly Liam voice, "So," loop.
# Sources (fact-checked 2026-11-20):
#  - Scientific American, "Why can't a person tickle himself?" (2003, S.-J. Blakemore): the back of the brain (cerebellum)
#    predicts the sensation when your own movement causes it and uses that prediction to cancel the response; it can't
#    predict someone else's touch, so that one tickles.
#  - Mental Floss "Why can't you tickle yourself?" / ScienceAlert: the brain uses a copy of the movement command to predict
#    and dampen self-made touch, which helps it tell self-made sensations from outside ones.
#  Owner rule: no studies on screen, plain words (no "cerebellum").
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
SKIN = "#E9B48F"; SKIN_D = "#C98E6A"; MINE = "#FF8A3D"; OTHER = "#4D8DFF"; PINKB = "#F4A9C0"; GREEN = "#1fb98a"
SHIRT = "#2E3A59"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


GOON = p0(1); NOTHING = p0(2); ELSE = kw(3); TORTURE = kw(4)
WIPE1 = p0(5) - 0.3; TRICK = p0(5); MOVE = p0(6); COPY = kw(7); KNOWS = kw(8); DOWN = kw(9)
WIPE2 = p0(10) - 0.3; FINGERS = p0(10); SURPRISE = kw(11); NOWARN = p0(12); EVERY = kw(13)
YOURS = p0(14); ONYOU = kw(15); SO = p0(16)
WL = 0.32
IMPACTS = [TORTURE, EVERY]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1):
    return math.sin(2 * math.pi * k * t / DUR)


# ---------------- parts ----------------
def bg_warm(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.55, 1300, [col("#2a1d1a"), col("#171112"), col("#0b090a")], [0, 0.55, 1])))
    c.drawCircle(260 + 30 * lw(t), 760, 520, paint(shader=radial(260, 760, 520, [col(MINE, 0.13), col(MINE, 0)])))
    c.drawCircle(860, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(860, 1450, 600, [col(OTHER, 0.10), col(OTHER, 0)])))


def torso(c, x, y, s, t, laugh=0.0, mood=None):
    """Person in a t-shirt (shoulders, side/ribs), head = emoji face on top. laugh = wobble."""
    c.save(); c.translate(x, y); c.scale(s, s)
    wob = laugh * 10 * math.sin(t * 38)
    c.translate(wob, 0)
    body = skia.Path()
    body.moveTo(-150, -400); body.cubicTo(-60, -370, 60, -370, 150, -400)
    body.cubicTo(230, -380, 280, -330, 280, -250); body.lineTo(250, -120)
    body.cubicTo(225, 50, 220, 250, 215, 460); body.lineTo(-215, 460); body.cubicTo(-220, 250, -225, 50, -250, -120)
    body.lineTo(-280, -250); body.cubicTo(-280, -330, -230, -380, -150, -400); body.close()
    # neck
    c.drawRoundRect(skia.Rect.MakeLTRB(-55, -470, 55, -360), 30, 30, paint(shader=linear((-55, 0), (55, 0), [col("#E9B48F"), col("#C98E6A")])))
    c.drawPath(body, paint("#000000", 0.35, blur=30))
    c.drawPath(body, paint(shader=linear((-260, 0), (260, 0), [col("#4a5c88"), col(SHIRT), col("#1c243a")])))
    c.save(); c.clipPath(body)
    for k in range(4):
        p = skia.Path(); p.moveTo(-220, -60 + k * 110); p.cubicTo(-120, -30 + k * 110, -60, -80 + k * 110, 40, -50 + k * 110)
        c.drawPath(p, paint("#ffffff", 0.06, stroke=6))
    # sleeves seams
    c.drawLine(-235, -250, -205, -110, paint("#000000", 0.25, stroke=5)); c.drawLine(235, -250, 205, -110, paint("#000000", 0.25, stroke=5))
    c.drawRect(skia.Rect.MakeLTRB(150, -100, 260, 300), paint(shader=linear((150, 0), (260, 0), [col("#ffffff", 0), col("#ffffff", 0.07)])))
    c.restore()
    c.drawArc(skia.Rect.MakeLTRB(-80, -440, 80, -340), 10, 160, False, paint("#1a2135", 1, stroke=14))
    if mood is not None:
        face(c, 0, -560, 150, mood, t, 1.0)
    c.restore()


def hand(c, x, y, s, rot, t, sleeve, a=1.0, wiggle=1.0, ph=0.0):
    """Hand pointing left (fingers toward -x) with sleeve to the right. Wiggling fingers."""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(60, -70, 520, 70), 40, 40, paint("#000000", 0.3 * a, blur=16))
    # forearm skin + sleeve
    c.drawRoundRect(skia.Rect.MakeLTRB(40, -52, 300, 52), 50, 50, paint(shader=linear((0, -52), (0, 52), [col("#F3C6A4", a), col(SKIN, a), col(SKIN_D, a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(230, -74, 560, 74), 30, 30, paint(shader=linear((0, -74), (0, 74), [col(mixhex(sleeve, "#ffffff", 0.25), a), col(sleeve, a), col(mixhex(sleeve, "#000000", 0.35), a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(230, -74, 262, 74), 14, 14, paint(mixhex(sleeve, "#000000", 0.2), a))
    # fingers (behind palm)
    for k in range(4):
        fy = -45 + k * 30
        ang = 14 * wiggle * math.sin(2 * math.pi * 14 * t / DUR + k * 1.3 + ph) + (k - 1.5) * 6
        c.save(); c.translate(-20, fy); c.rotate(ang)
        L = 128 - abs(k - 1.2) * 14
        c.drawRoundRect(skia.Rect.MakeLTRB(-L, -14, 10, 14), 14, 14, paint(shader=linear((0, -14), (0, 14), [col("#F6CDAE", a), col(SKIN, a), col(SKIN_D, a)])))
        c.drawRoundRect(skia.Rect.MakeLTRB(-L + 4, -9, -L + 26, 7), 6, 6, paint("#FBE3D2", 0.8 * a))
        c.drawLine(-L * 0.45, -10, -L * 0.45, 10, paint(SKIN_D, 0.6 * a, stroke=2))
        c.restore()
    # palm
    c.drawRoundRect(skia.Rect.MakeLTRB(-40, -66, 90, 66), 46, 46, paint(shader=linear((0, -66), (0, 66), [col("#F6CDAE", a), col(SKIN, a), col(SKIN_D, a)])))
    # thumb
    c.save(); c.translate(30, 52); c.rotate(-20 + 6 * wiggle * math.sin(2 * math.pi * 7 * t / DUR + ph))
    c.drawRoundRect(skia.Rect.MakeLTRB(-80, -16, 10, 16), 16, 16, paint(shader=linear((0, -16), (0, 16), [col("#F6CDAE", a), col(SKIN_D, a)])))
    c.restore()
    c.restore()


def meter(c, t, x, y, v, a, light=False):
    """TICKLE METER horizontal bar, v in 0..1."""
    if a <= 0: return
    w, h = 640, 58
    fg = INK if light else "#FFFFFF"
    f = skia.Font(TF_MONO, 26)
    c.drawString("TICKLE METER", x - w / 2, y - 26, f, paint(fg, 0.75 * a))
    v = clamp(v)
    pct = f"{int(round(v * 100))}%"
    c.drawString(pct, x + w / 2 - f.measureText(pct), y - 26, f, paint(fg, 0.75 * a))
    r = skia.Rect.MakeXYWH(x - w / 2, y, w, h)
    c.drawRoundRect(r, h / 2, h / 2, paint(fg, 0.10 * a))
    c.drawRoundRect(r, h / 2, h / 2, paint(fg, 0.3 * a, stroke=2))
    if v > 0.01:
        cc = mixhex(GREEN, RED, clamp(v * 1.2))
        rr = skia.Rect.MakeXYWH(x - w / 2 + 6, y + 6, max(h - 12, (w - 12) * v), h - 12)
        c.drawRoundRect(rr, (h - 12) / 2, (h - 12) / 2, paint(cc, 0.35 * a, blur=10))
        c.drawRoundRect(rr, (h - 12) / 2, (h - 12) / 2, paint(cc, a))
        c.drawRoundRect(skia.Rect.MakeXYWH(rr.left() + 10, rr.top() + 6, max(0, rr.width() - 20), 10), 5, 5, paint("#ffffff", 0.35 * a))


def face(c, x, y, r, mood, t, a=1.0):
    """mood 0 = flat/bored, 1 = laughing hard."""
    if a <= 0: return
    c.save(); c.translate(x, y)
    sh = mood * 6 * math.sin(t * 40)
    c.translate(sh, 0)
    c.drawCircle(0, 8, r, paint("#000000", 0.3 * a, blur=14))
    c.drawCircle(0, 0, r, paint(shader=radial(-r * 0.3, -r * 0.4, r * 1.4, [col("#FFE48A", a), col("#FFC93C", a), col("#E9A21B", a)], [0, 0.6, 1])))
    ink = paint("#5a3410", a, stroke=r * 0.09)
    if mood < 0.5:
        c.drawLine(-r * 0.42, -r * 0.15, -r * 0.18, -r * 0.15, ink); c.drawLine(r * 0.18, -r * 0.15, r * 0.42, -r * 0.15, ink)
        c.drawLine(-r * 0.3, r * 0.38, r * 0.3, r * 0.38, ink)
    else:
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(sx * r * 0.45, -r * 0.1); p.lineTo(sx * r * 0.22, -r * 0.22); p.lineTo(sx * r * 0.45, -r * 0.34)
            c.drawPath(p, ink)
        m = skia.Path(); m.moveTo(-r * 0.5, r * 0.1); m.cubicTo(-r * 0.4, r * 0.75, r * 0.4, r * 0.75, r * 0.5, r * 0.1); m.close()
        c.drawPath(m, paint("#5a3410", a)); c.save(); c.clipPath(m)
        c.drawCircle(0, r * 0.62, r * 0.25, paint("#ff6b7a", a)); c.restore()
        # tears of laughter
        for sx in (-1, 1):
            d = (t * 1.6 + (0 if sx < 0 else 0.5)) % 1
            c.drawCircle(sx * r * (0.62 + 0.25 * d), -r * 0.05 + r * 0.6 * d, r * 0.08, paint("#9fd8ff", a * (1 - d)))
    c.restore()


def brain(c, x, y, s, a=1.0, glow=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    p.moveTo(-200, 40); p.cubicTo(-240, -60, -170, -160, -70, -150); p.cubicTo(-30, -200, 80, -200, 120, -140)
    p.cubicTo(220, -130, 250, -20, 200, 50); p.cubicTo(200, 120, 120, 150, 60, 120); p.cubicTo(20, 160, -80, 160, -110, 110)
    p.cubicTo(-180, 120, -220, 90, -200, 40); p.close()
    if glow > 0:
        c.drawPath(p, paint(PINKB, 0.6 * glow * a, blur=30))
    c.drawPath(p, paint("#000000", 0.18 * a, blur=16))
    c.drawPath(p, paint(shader=radial(-40, -100, 300, [col("#FFE1EA", a), col(PINKB, a), col("#DD7F9C", a)], [0, 0.55, 1])))
    for k, (x0, y0, x1, y1) in enumerate(((-160, -40, 40, -110), (-150, 40, 150, -20), (-60, 110, 170, 60), (60, -150, 40, 120))):
        q = skia.Path(); q.moveTo(x0, y0); q.cubicTo((x0 + x1) / 2 - 30, y0 - 50, (x0 + x1) / 2 + 30, y1 + 50, x1, y1)
        c.drawPath(q, paint("#C9667F", 0.55 * a, stroke=7))
    c.drawCircle(-70, -100, 30, paint("#ffffff", 0.35 * a, blur=10))
    c.restore()


def card(c, x, y, w, h, a, light=True):
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2 + 8, w, h), 28, 28, paint("#000000", 0.14 * a, blur=14))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 28, 28, paint("#ffffff" if light else "#2a2729", a))


def slider(c, t, x, y, v, a):
    """Vertical 'FEELING' volume slider, v 0..1."""
    if a <= 0: return
    card(c, x, y, 200, 480, a)
    f = skia.Font(TF_MONO, 24)
    c.drawString("FEELING", x - f.measureText("FEELING") / 2, y - 196, f, paint(INK, 0.7 * a))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 14, y - 160, x + 14, y + 200), 14, 14, paint("#e4e1db", a))
    ty = lerp(y + 190, y - 150, v)
    cc = mixhex(GREEN, MINE, v)
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 14, ty, x + 14, y + 200), 14, 14, paint(cc, a))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 54, ty - 22, x + 54, ty + 22), 18, 18, paint("#000000", 0.2 * a, blur=6))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 54, ty - 22, x + 54, ty + 22), 18, 18, paint(INK, a))
    c.drawLine(x - 24, ty, x + 24, ty, paint("#ffffff", 0.7 * a, stroke=4))


def envelope(c, x, y, s, a, colr=MINE):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -48, 70, 48), 12, 12, paint("#000000", 0.18 * a, blur=8))
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -48, 70, 48), 12, 12, paint("#ffffff", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -48, 70, 48), 12, 12, paint(colr, a, stroke=5))
    p = skia.Path(); p.moveTo(-64, -42); p.lineTo(0, 8); p.lineTo(64, -42)
    c.drawPath(p, paint(colr, a, stroke=5))
    c.restore()


# ---------------- hook ----------------
def hook_pose(t):
    return 660 + 18 * lw(t), 1250 + 14 * lw(t, 2)


def scene_hook(c, t, a_meter=0.0, v=0.0):
    bg_warm(c, t)
    torso(c, 320, 1290, 0.9, t, mood=0.0)
    hx, hy = hook_pose(t)
    hand(c, hx, hy, 1.0, -8, t, MINE)
    # little "tickle" motion arcs at the fingertips
    for k in range(3):
        u = ((t * 1.1 + k / 3) % 1)
        c.drawArc(skia.Rect.MakeXYWH(hx - 230 - 40 * u, hy - 60 - 40 * u, 80 + 80 * u, 120 + 80 * u), 140, 80, False, paint("#ffffff", 0.35 * (1 - u), stroke=4))


def scene_open(c, t):
    """0 .. WIPE1: hook, nothing, someone else, torture."""
    scene_hook(c, t)
    pill(c, t, "TICKLE YOURSELF?", 495, 560, MINE, 0.35, NOTHING - 0.1)
    # meter + face for 'nothing'
    ma = eout(prog(t, NOTHING - 0.15, 0.35))
    if ma > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 0.35 * ma))
        v = lerp(0.04, 1.0, eback(prog(t, TORTURE - 0.05, 0.4), 1.2))
        v = min(v, 1.0)
        mood = prog(t, TORTURE - 0.05, 0.15)
        torso(c, 320, 1290, 0.9, t, laugh=mood, mood=mood)
        hx, hy = hook_pose(t)
        hand(c, hx, hy, 1.0, -8, t, MINE)
        meter(c, t, 495, 1380, v, ma)
    # other person's hand slides in from the left
    oa = eout(prog(t, ELSE - 0.25, 0.45))
    if oa > 0:
        hand(c, lerp(-360, 20, oa), 1110, -1.0, 8, t, OTHER, 1.0, wiggle=1.6, ph=1.0)
    pill(c, t, "NOTHING", 495, 560, "#8a8f98", NOTHING, ELSE - 0.1)
    pill(c, t, "SOMEONE ELSE", 495, 560, OTHER, ELSE, TORTURE - 0.05)
    pill(c, t, "TORTURE!", 495, 560, RED, TORTURE, WIPE1 + 0.1)
    if TORTURE - 0.05 < t < TORTURE + 0.8:
        u = prog(t, TORTURE - 0.05, 0.8)
        for k in range(3):
            c.drawCircle(320, 786, 160 + 260 * clamp(u - k * 0.15), paint(RED, 0.6 * (1 - u), stroke=8))


# ---------------- white: the copy of the plan ----------------
BR = (495, 740)
HANDW = (700, 1340)


def scene_white(c, t):
    studio_white(c)
    ga = eout(prog(t, WIPE1, 0.4))
    # brain top, own hand (orange sleeve) bottom-right, pointing left at a body side (simple arm silhouette)
    bx, by = BR
    brain(c, bx, by, 0.9 * ga, ga, glow=window(t, COPY - 0.1, DOWN + 0.5, 0.2, 0.3))
    hx, hy = HANDW
    hand(c, hx + 20 * lw(t), hy, 0.85, 0, t, MINE, ga, wiggle=1.0)
    # 'move' command: dot travels brain -> hand
    ma = window(t, MOVE - 0.1, KNOWS + 0.3, 0.2, 0.3)
    if ma > 0:
        p = skia.Path(); p.moveTo(bx + 150, by + 100); p.cubicTo(bx + 330, by + 240, hx + 180, hy - 280, hx + 120, hy - 90)
        c.drawPath(p, paint(MINE, 0.35 * ma, stroke=6))
        pm = skia.PathMeasure(p, False); L = pm.getLength()
        for k in range(3):
            u = ((t * 0.9 + k / 3) % 1)
            pos, _ = pm.getPosTan(L * u)
            c.drawCircle(pos.x(), pos.y(), 18, paint(MINE, 0.35 * ma, blur=6)); c.drawCircle(pos.x(), pos.y(), 9, paint(MINE, ma))
        pill(c, t, "MOVE!", bx + 300, by + 190, MINE, MOVE + 0.1, COPY - 0.05, light=True)
    # copy of the plan: envelope duplicates and flies into a prediction bubble on the left
    ca = prog(t, COPY - 0.1, 0.01)
    if ca > 0 and t < WIPE2 + 0.3:
        u = eio(prog(t, COPY, 0.7))
        ex, ey = lerp(bx + 120, 250, u), lerp(by + 40, 1100, u) - 120 * math.sin(math.pi * u)
        bub = eback(prog(t, COPY + 0.4, 0.4))
        if bub > 0:
            c.save(); c.translate(250, 1100); c.scale(bub, bub)
            c.drawCircle(0, 8, 165, paint("#000000", 0.12, blur=14))
            c.drawCircle(0, 0, 165, paint("#ffffff"))
            c.drawCircle(0, 0, 165, paint(MINE, 1, stroke=5))
            c.drawCircle(120, -170, 26, paint("#ffffff")); c.drawCircle(120, -170, 26, paint(MINE, 1, stroke=4))
            c.drawCircle(150, -225, 14, paint("#ffffff")); c.drawCircle(150, -225, 14, paint(MINE, 1, stroke=3))
            kn = prog(t, KNOWS - 0.1, 0.3)
            if kn > 0:   # predicted feeling: mini hand + tick
                hand(c, 40, -20, 0.36, 0, t, MINE, kn, wiggle=1.0)
                ck = eout(prog(t, KNOWS + 0.3, 0.3))
                c.drawCircle(-10, 90, 34, paint(GREEN, kn))
                p = skia.Path(); p.moveTo(-26, 90); p.lineTo(-14, 104); p.lineTo(10, 76)
                pp = paint("#ffffff", kn, stroke=8)
                if ck < 0.999:
                    te = skia.TrimPathEffect.Make(0, max(ck, 0.001))
                    if te: pp.setPathEffect(te)
                c.drawPath(p, pp)
            c.restore()
        envelope(c, ex, ey, 0.9 * (1 - 0.6 * prog(t, COPY + 0.55, 0.2)), 1 - prog(t, COPY + 0.6, 0.2))
        envelope(c, bx + 120, by + 40, 0.9, window(t, COPY - 0.1, COPY + 0.5, 0.1, 0.2))
    pill(c, t, "COPY OF THE PLAN", 495, 560, MINE, COPY, KNOWS - 0.05)
    pill(c, t, "IT KNOWS", 495, 560, GREEN, KNOWS, DOWN - 0.05)
    # volume slider turns the feeling down
    sa = eback(prog(t, DOWN - 0.35, 0.35))
    if sa > 0:
        v = lerp(0.95, 0.1, eio(prog(t, DOWN, 0.6)))
        c.save(); c.translate(790, 1030); c.scale(clamp(sa), clamp(sa)); c.translate(-790, -1030)
        slider(c, t, 790, 1030, v, clamp(sa) * (1 - prog(t, WIPE2, 0.2)))
        c.restore()
    pill(c, t, "TURNED DOWN", 495, 560, GREEN, DOWN, WIPE2 + 0.1, text_col="#FFFFFF")


# ---------------- dark: surprise ----------------
def scene_surprise(c, t):
    bg_warm(c, t)
    lg = prog(t, EVERY - 0.05, 0.1)
    torso(c, 320, 1290, 0.9, t, laugh=lg, mood=lg)
    oa = eout(prog(t, WIPE2 + 0.05, 0.5))
    hand(c, lerp(1250, 660, oa), 1250 + 12 * lw(t, 3), 1.0, -6, t, OTHER, 1.0, wiggle=1.5, ph=2.0)
    # prediction bubble: empty "???"
    qa = window(t, SURPRISE - 0.25, NOWARN - 0.05, 0.25, 0.2)
    if qa > 0:
        s = eback(prog(t, SURPRISE - 0.25, 0.35))
        c.save(); c.translate(740, 790); c.scale(s, s)
        c.drawCircle(0, 0, 120, paint("#2a2729", qa)); c.drawCircle(0, 0, 120, paint(OTHER, qa, stroke=5))
        f = skia.Font(TF_BLACK, 110)
        txt = "?"
        c.drawString(txt, -f.measureText(txt) / 2, 38 + 6 * math.sin(t * 9), f, paint("#ffffff", qa))
        c.restore()
    # no-warning sign
    na = window(t, NOWARN - 0.1, EVERY + 0.1, 0.2, 0.2)
    if na > 0:
        s = eback(prog(t, NOWARN - 0.1, 0.3))
        c.save(); c.translate(740, 790); c.scale(s, s)
        tri = skia.Path(); tri.moveTo(0, -95); tri.lineTo(100, 75); tri.lineTo(-100, 75); tri.close()
        c.drawPath(tri, paint(YELLOW, na)); c.drawPath(tri, paint(INK, na, stroke=8))
        f = skia.Font(TF_BLACK, 100); c.drawString("!", -f.measureText("!") / 2, 60, f, paint(INK, na))
        x = eout(prog(t, NOWARN + 0.25, 0.25))
        c.drawLine(-120, -110, lerp(-120, 120, x), lerp(-110, 110, x), paint(RED, na, stroke=16))
        c.restore()
    ea = window(t, EVERY - 0.2, YOURS + 0.1, 0.2, 0.25)
    if ea > 0:
        meter(c, t, 495, 1380, min(1.0, lerp(0.1, 1.0, eback(prog(t, EVERY - 0.05, 0.4), 1.2))), ea)
        u = prog(t, EVERY - 0.05, 0.8)
        for k in range(3):
            c.drawCircle(320, 786, 120 + 260 * clamp(u - k * 0.15), paint(RED, 0.6 * ea * (1 - u), stroke=8))
    pill(c, t, "SURPRISE!", 495, 560, OTHER, SURPRISE, NOWARN - 0.05)
    pill(c, t, "NO WARNING", 495, 560, YELLOW, NOWARN, EVERY - 0.05)
    pill(c, t, "FULL FEELING", 495, 560, RED, EVERY, YOURS - 0.1)


def scene_split(c, t):
    bg_warm(c, t)
    a = eout(prog(t, YOURS - 0.25, 0.35))
    for i, (x, sleeve, label, v, tin) in enumerate(((270, MINE, "YOUR TOUCH", 0.08, YOURS), (720, OTHER, "TOUCH ON YOU", 0.95, ONYOU))):
        q = eback(prog(t, tin - 0.2, 0.35))
        if q <= 0: continue
        c.save(); c.translate(x, 960); c.scale(q, q)
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -330, 200, 330), 34, 34, paint("#000000", 0.3, blur=18))
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -330, 200, 330), 34, 34, paint("#221c1d"))
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -330, 200, 330), 34, 34, paint(sleeve, 0.9, stroke=4))
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-200, -330, 200, 330), 34, 34), doAntiAlias=True)
        hand(c, 20, -110, 0.6, 0, t, sleeve, 1.0, wiggle=1.2, ph=i)
        c.restore()
        face(c, 0, 90, 90, 0.0 if i == 0 else 1.0, t, 1.0)
        # mini meter
        c.drawRoundRect(skia.Rect.MakeLTRB(-150, 230, 150, 262), 16, 16, paint("#ffffff", 0.12))
        vv = v * eout(prog(t, tin, 0.5))
        cc = mixhex(GREEN, RED, v)
        c.drawRoundRect(skia.Rect.MakeLTRB(-150, 230, -150 + max(32, 300 * vv), 262), 16, 16, paint(cc))
        c.restore()
    pill(c, t, "YOUR TOUCH = QUIET", 495, 560, MINE, YOURS + 0.1, ONYOU - 0.05)
    pill(c, t, "TOUCH ON YOU = LOUD", 495, 560, OTHER, ONYOU, SO + 0.3)


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_white(c, t); return
    if t < YOURS - 0.25:
        scene_surprise(c, t); return
    if t < SO - 0.05:
        scene_split(c, t)
        q = 1 - prog(t, YOURS - 0.25, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_surprise(c, t); c.restore()
        return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_split(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.022 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"tickle": MINE, "right": "#8a8f98", "else": OTHER, "torture": RED, "copy": MINE, "knows": GREEN, "down": GREEN,
         "surprise": OTHER, "everything": RED, "your": MINE, "on": OTHER}
CAPS = Captions(P, KWCOL, {"torture!", "everything."}, DUR)


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
    wipe(c, t, WIPE1, WL, MINE, "#F4F2EE")
    wipe(c, t, WIPE2, WL, OTHER, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("pop", NOTHING), ("whoosh", ELSE - 0.25), ("riser", ELSE), ("hit", TORTURE),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", MOVE + 0.1), ("pop", COPY), ("whoosh", COPY + 0.1),
          ("pop", KNOWS), ("pop", DOWN - 0.3), ("tick", DOWN + 0.1), ("tick", DOWN + 0.3), ("whoosh", WIPE2),
          ("pop", SURPRISE), ("pop", NOWARN), ("hit", EVERY), ("whoosh", YOURS - 0.25), ("pop", YOURS + 0.1),
          ("pop", ONYOU), ("whoosh", SO - 0.05)]
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

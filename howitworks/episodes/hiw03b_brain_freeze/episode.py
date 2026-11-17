# HIW03b — brain freeze (clean remake, standard format). Sources:
#  cold palate -> vessels constrict then rapidly dilate; trigeminal nerve; referred pain to forehead;
#  warming the palate (tongue) eases it; usually passes within a minute: UCLA Health; Houston Methodist
#  fast vs slow eating, ~2x (27% vs 13%), 145 students: Kaczorowski & Kaczorowski, BMJ 2002;325:1445
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
COBALT = "#3B5BDB"; ICE = "#A9C8FF"; COPPER = "#D9783A"; PINK = "#F6B6C8"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


REVEAL = kw(1); FREEZE = kw(2); ROOF = p0(3); SHRINK = kw(4); RUSH = kw(5)
NERVE = p0(6); ALARM = kw(7); ADDRESS = p0(8); FOREHEAD = kw(10)
WORSE = p0(11); STUDY = p0(12); TWICE = kw(13)
WIPE1 = p0(14) - 0.3; COLD = kw(14); NOTEX = kw(15); WARM = p0(16)
WIPE2 = p0(18) - 0.3; FIX = p0(18); TONGUE = kw(19); FADES = kw(22); MINUTE = p0(23); SO = p0(24)
WL = 0.32
IMPACTS = [FOREHEAD, NOTEX]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def mode_at(t):
    if t < REVEAL - 0.1: return "hook"
    if t < STUDY - 0.15: return "head"
    if t < WIPE1 + WL / 2: return "bars"
    if t < WIPE2 + WL / 2: return "white"
    if t < SO - 0.05: return "head2"
    return "end"


# ---------------- background ----------------
def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#1d2748"), col("#111832"), col("#080b18")], [0, 0.5, 1])))
    c.drawCircle(220 + 40 * math.sin(t * 0.3), 600, 520, paint(shader=radial(220, 600, 520, [col("#3B5BDB", 0.16), col("#3B5BDB", 0)])))
    c.drawCircle(880, 1500 + 30 * math.cos(t * 0.25), 600, paint(shader=radial(880, 1500, 600, [col("#D9783A", 0.10), col("#D9783A", 0)])))


rnd = random.Random(9)
SPARK = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(2, 6), rnd.random() * 6.28) for _ in range(60)]


def ice_cream(c, x, y, s, rot=0, a=1.0, t=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    cone = skia.Path(); cone.moveTo(-74, 0); cone.lineTo(74, 0); cone.lineTo(0, 270); cone.close()
    c.drawPath(cone, paint(shader=linear((-74, 0), (74, 0), [col("#E9B477", a), col("#D99A5B", a), col("#B97A3F", a)])))
    c.save(); c.clipPath(cone)
    for k in range(-6, 7):
        c.drawLine(k * 26 - 80, 0, k * 26 + 80, 270, paint("#a86c35", 0.5 * a, stroke=3))
        c.drawLine(k * 26 + 80, 0, k * 26 - 80, 270, paint("#a86c35", 0.5 * a, stroke=3))
    c.restore()
    scoop = skia.Path(); scoop.addCircle(0, -70, 100)
    for dx, r in ((-70, 26), (-30, 30), (15, 28), (58, 30)):
        scoop.addCircle(dx, 8, r)
    c.drawPath(scoop, paint("#000000", 0.18 * a, blur=10))
    c.drawPath(scoop, paint(shader=radial(-35, -110, 190, [col("#FFE3EC", a), col(PINK, a), col("#E48AA6", a)], [0, 0.45, 1])))
    c.drawCircle(-38, -118, 22, paint("#ffffff", 0.5 * a, blur=6))
    c.restore()


def hook_pose(t):
    ph = 2 * math.pi * t / DUR
    return 540 + 14 * math.sin(ph), 1180 + 10 * math.sin(2 * ph), 3.1 + 0.06 * math.sin(ph)


def draw_hook(c, t, a=1.0):
    bg_dark(c, t)
    x, y, s = hook_pose(t)
    ice_cream(c, x, y, s, 0, a, t)
    for (u, v, r, ph) in SPARK:
        sx = x + u * 420; sy = y - 200 + v * 300
        tw = 0.5 + 0.5 * math.sin(2 * math.pi * t / DUR * 3 + ph)
        c.drawCircle(sx, sy, r, paint("#ffffff", 0.7 * tw * a))
        c.drawCircle(sx, sy, r * 3, paint(ICE, 0.12 * tw * a, blur=4))


# ---------------- head (world coords, facing right, centre at 0,0) ----------------
HEAD = skia.Path()
HEAD.moveTo(-200, 320)
HEAD.cubicTo(-210, 150, -265, 40, -252, -80)
HEAD.cubicTo(-240, -260, -80, -335, 60, -305)
HEAD.cubicTo(170, -285, 215, -205, 220, -125)
HEAD.cubicTo(222, -85, 215, -62, 226, -40)
HEAD.cubicTo(252, 0, 278, 40, 262, 62)
HEAD.cubicTo(255, 72, 240, 75, 232, 80)
HEAD.cubicTo(240, 96, 242, 106, 233, 113)
HEAD.cubicTo(238, 123, 238, 133, 229, 141)
HEAD.cubicTo(233, 170, 220, 200, 180, 213)
HEAD.cubicTo(140, 223, 112, 232, 92, 320)
HEAD.close()
ROOF_P = skia.Path(); ROOF_P.moveTo(95, 104); ROOF_P.cubicTo(140, 82, 190, 84, 226, 100)
NERVE_P = skia.Path(); NERVE_P.moveTo(160, 92); NERVE_P.cubicTo(100, 30, 110, -90, 196, -160)
NLEN = skia.PathMeasure(NERVE_P, False).getLength()
FH = (196, -168)


def vessels(c, t, w, colr, a):
    for (y0, y1) in ((122, 112), (140, 132)):
        p = skia.Path(); p.moveTo(100, y0); p.cubicTo(140, y0 - 14, 185, y1 - 10, 224, y1)
        c.drawPath(p, paint(colr, 0.25 * a, stroke=w + 10, blur=6))
        c.drawPath(p, paint(colr, a, stroke=w))


def draw_head(c, t, cam, st):
    cx, cy, z = cam
    c.save(); c.translate(540, 1060); c.scale(z, z); c.translate(-cx, -cy)
    c.drawPath(HEAD, paint("#000000", 0.35, blur=40))
    c.drawPath(HEAD, paint(shader=linear((-260, -300), (270, 300), [col("#F2C3A0"), col("#E2A882"), col("#C88A65")])))
    c.save(); c.clipPath(HEAD)
    # brain (soft, simple)
    c.drawOval(skia.Rect.MakeLTRB(-215, -285, 175, -40), paint(shader=radial(-40, -200, 260, [col("#FBE1E4", 0.85), col("#F2BFC6", 0.75)])))
    for k in range(3):
        p = skia.Path(); p.moveTo(-170 + k * 20, -170 + k * 45)
        p.cubicTo(-90, -230 + k * 45, 20, -120 + k * 45, 130, -190 + k * 45)
        c.drawPath(p, paint("#e6a3ae", 0.55, stroke=5))
    # mouth cavity hint
    c.drawOval(skia.Rect.MakeLTRB(90, 96, 236, 150), paint("#7a3b3b", 0.35 * st.get("mouth", 0)))
    # roof glow
    rg = st.get("roof", 0)
    if rg > 0:
        c.drawPath(ROOF_P, paint(ICE, 0.6 * rg, stroke=26, blur=10))
        c.drawPath(ROOF_P, paint("#E9F1FF", rg, stroke=6))
        for k in range(3):
            u = ((t * 0.9 + k / 3) % 1)
            c.drawOval(skia.Rect.MakeLTRB(160 - 60 * u, 96 - 22 * u, 160 + 60 * u, 96 + 22 * u), paint(ICE, rg * (1 - u), stroke=3))
    warm = st.get("warmroof", 0)
    if warm > 0:
        c.drawPath(ROOF_P, paint(COPPER, 0.7 * warm, stroke=30, blur=12))
    va = st.get("vess", 0)
    if va > 0:
        vessels(c, t, st.get("vw", 7), st.get("vcol", "#D8566A"), va)
    # tongue
    tg = st.get("tongue", 0)
    if tg > 0:
        y = lerp(160, 118, tg)
        tp = skia.Path(); tp.moveTo(96, 170); tp.cubicTo(110, y - 6, 200, y - 10, 226, y + 12); tp.lineTo(226, 175); tp.close()
        c.drawPath(tp, paint(shader=linear((0, y - 10), (0, 175), [col("#F08A98"), col("#D9667A")])))
    # nerve
    na = st.get("nerve", 0)
    if na > 0:
        pp = paint("#FFF4D6", 0.95, stroke=5)
        if na < 0.999:
            te = skia.TrimPathEffect.Make(0, na)
            if te: pp.setPathEffect(te)
        c.drawPath(NERVE_P, paint(YELLOW, 0.35 * min(na, 1), stroke=18, blur=8))
        c.drawPath(NERVE_P, pp)
        sig = st.get("signal", 0)
        if sig > 0:
            pm = skia.PathMeasure(NERVE_P, False)
            for k in range(3):
                u = ((t * 1.2 + k / 3) % 1)
                pos, _ = pm.getPosTan(NLEN * u)
                c.drawCircle(pos.x(), pos.y(), 16, paint(YELLOW, 0.4 * sig, blur=6))
                c.drawCircle(pos.x(), pos.y(), 7, paint("#ffffff", sig))
    c.restore()
    c.drawPath(HEAD, paint("#ffffff", 0.25, stroke=3, blur=2))
    # pain rings at the forehead
    pr = st.get("pain", 0)
    if pr > 0:
        for k in range(3):
            u = ((t * 0.8 + k / 3) % 1)
            c.drawCircle(FH[0] + 30, FH[1], 30 + 110 * u, paint(RED, pr * (1 - u), stroke=6))
        c.drawCircle(FH[0] + 30, FH[1], 34, paint(RED, 0.5 * pr, blur=14))
    # wrong-address pin
    pa = st.get("pin", -1)
    if pa >= 0:
        u = eio(pa)
        px = lerp(165, FH[0] + 30, u); py = lerp(95, FH[1], u) - math.sin(math.pi * u) * 120
        pin(c, px, py, 1.0, RED if u > 0.95 else "#ffffff")
    # cone near the mouth
    ca = st.get("cone", 0)
    if ca > 0:
        ice_cream(c, lerp(420, 330, ca), 170, 0.55, -35, ca, t)
    c.restore()


def pin(c, x, y, s, colr):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 0); p.cubicTo(-26, -30, -30, -50, -30, -62)
    p.arcTo(skia.Rect.MakeLTRB(-30, -92, 30, -32), 180, 180, False); p.cubicTo(30, -50, 26, -30, 0, 0); p.close()
    c.drawPath(p, paint("#000000", 0.3, blur=6)); c.drawPath(p, paint(colr)); c.drawCircle(0, -62, 11, paint("#141313"))
    c.restore()


CAMS = [  # (time, cx, cy, zoom)
    (REVEAL, 40, -20, 1.35), (ROOF - 0.1, 165, 110, 3.2), (NERVE - 0.1, 140, -20, 1.9), (ADDRESS, 30, -20, 1.35),
    (WORSE, 90, -10, 1.1)]
CAMS2 = [(WIPE2, 165, 110, 3.2), (FADES - 0.3, 40, -20, 1.35)]


def cam_at(t, keys):
    if t <= keys[0][0]:
        return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t < t1:
            q = eio(prog(t, t1 - 0.55, 0.55)) if t > t1 - 0.55 else 0
            return tuple(lerp(x, y, q) for x, y in zip(a, b))
    return keys[-1][1:]


def scene_head(c, t):
    bg_dark(c, t)
    cam = cam_at(t, CAMS)
    st = dict(cone=eout(prog(t, REVEAL, 0.5)) * (1 - prog(t, ADDRESS, 0.4)), mouth=prog(t, ROOF - 0.2, 0.4) * (1 - prog(t, ADDRESS, 0.4)))
    st["roof"] = window(t, ROOF - 0.1, RUSH + 0.6, 0.3, 0.3)
    st["vess"] = window(t, SHRINK - 0.3, NERVE + 0.6, 0.3, 0.3)
    w = 8
    w = lerp(w, 3, eio(prog(t, SHRINK, 0.6)))
    w = lerp(w, 13, eback(prog(t, RUSH, 0.5), 1.6))
    st["vw"] = w
    st["vcol"] = mixhex(mixhex("#D8566A", "#7f9be8", prog(t, SHRINK, 0.6)), "#E8644A", prog(t, RUSH, 0.4))
    st["nerve"] = eout(prog(t, NERVE, 0.7)) * (1 - prog(t, WORSE, 0.3))
    st["signal"] = window(t, ALARM - 0.1, WORSE, 0.2, 0.3)
    if ADDRESS - 0.05 < t < WORSE:
        st["pin"] = clamp((t - ADDRESS) / 1.1)
    st["pain"] = eout(prog(t, FOREHEAD - 0.1, 0.3)) * (1 - prog(t, STUDY - 0.4, 0.3))
    draw_head(c, t, cam, st)
    # eating fast: scoops racing in
    fa = window(t, WORSE, STUDY, 0.15, 0.25)
    if fa > 0:
        for k in range(4):
            u = ((t - WORSE) * 1.6 + k * 0.25) % 1
            x = lerp(1180, 760, u); y = 1110 + k * 30 - 60
            for j in range(4):
                c.drawLine(x + 30 + j * 26, y + (j - 1.5) * 8, x + 90 + j * 26, y + (j - 1.5) * 8, paint("#ffffff", 0.35 * fa * (1 - u), stroke=3))
            c.drawCircle(x, y, 26, paint(shader=radial(x - 8, y - 8, 34, [col("#FFE3EC", fa), col(PINK, fa)])))
    pill(c, t, "NOT FREEZING", 540, 600, COBALT, FREEZE, ROOF)
    if FREEZE < t < ROOF + 0.3:
        sa = eback(prog(t, FREEZE - 0.05, 0.3)) * (1 - prog(t, ROOF - 0.1, 0.3))
        snowflake(c, 300, 820, 70 * sa, ICE, clamp(sa))
        xp = eout(prog(t, FREEZE + 0.35, 0.2))
        if xp > 0:
            c.drawLine(240, 760, lerp(240, 360, xp), lerp(760, 880, xp), paint(RED, clamp(sa), stroke=10))
    pill(c, t, "COLD", 300, 640, ICE, ROOF + 0.1, SHRINK, text_col=INK)
    pill(c, t, "SHRINK", 300, 640, COBALT, SHRINK, RUSH)
    pill(c, t, "RUSH OPEN", 300, 640, COPPER, RUSH, NERVE)
    pill(c, t, "ALARM!", 300, 640, YELLOW, ALARM, ADDRESS)
    pill(c, t, "WRONG ADDRESS", 300, 640, "#FFFFFF", ADDRESS + 0.3, FOREHEAD)
    pill(c, t, "OUCH", 820, 640, RED, FOREHEAD, WORSE)
    pill(c, t, "FAST = WORSE", 300, 640, RED, WORSE, STUDY)


def snowflake(c, x, y, r, colr, a):
    if r <= 0: return
    for k in range(6):
        an = k * math.pi / 3
        ex, ey = x + r * math.cos(an), y + r * math.sin(an)
        c.drawLine(x, y, ex, ey, paint(colr, a, stroke=r * 0.12))
        for sgn in (-1, 1):
            bx, by = x + r * 0.6 * math.cos(an), y + r * 0.6 * math.sin(an)
            c.drawLine(bx, by, bx + r * 0.25 * math.cos(an + sgn * 0.8), by + r * 0.25 * math.sin(an + sgn * 0.8), paint(colr, a, stroke=r * 0.09))


def scene_bars(c, t):
    bg_dark(c, t)
    a = eout(prog(t, STUDY - 0.15, 0.4))
    f = skia.Font(TF_BOLD, 40); fs = skia.Font(TF_MONO, 26)
    for i, (lab, v, colr, dl) in enumerate((("SLOW EATERS", 13, "#8d93a8", 0.0), ("FAST EATERS", 27, COPPER, 0.25))):
        x = 290 + i * 330
        q = eexpo(prog(t, STUDY + 0.3 + dl, 0.9 if i == 0 else 1.2))
        h = 22 * v * q
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 90, 1330 - 600, x + 90, 1330), 26, 26, paint("#ffffff", 0.05 * a))
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 90, 1330 - h, x + 90, 1330), 26, 26, paint(colr, a))
        s = f"{int(round(v * q))}%"
        c.drawString(s, x - f.measureText(s) / 2, 1330 - h - 24, f, paint("#ffffff", a))
        c.drawString(lab, x - fs.measureText(lab) / 2, 1390, fs, paint("#ffffff", 0.7 * a))
    ta = eback(prog(t, TWICE, 0.35))
    if ta > 0:
        c.save(); c.translate(780, 620); c.scale(ta, ta)
        fb = skia.Font(TF_BLACK, 150)
        c.drawString("2×", -fb.measureText("2×") / 2, 50, fb, paint(COPPER, clamp(ta)))
        c.restore()
    footnote(c, t, "145 students, fast vs slow · BMJ 2002", STUDY + 0.3, WIPE1 + 0.3)


def thermo(c, x, y, q, a):
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 34, y - 380, x + 34, y), 34, 34, paint(INK, 0.08 * a))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 34, y - 380, x + 34, y), 34, 34, paint(INK, 0.35 * a, stroke=3))
    colr = mixhex(COBALT, COPPER, q)
    h = lerp(60, 340, q)
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 18, y - h, x + 18, y), 18, 18, paint(colr, a))
    c.drawCircle(x, y + 10, 62, paint(colr, a)); c.drawCircle(x, y + 10, 62, paint(INK, 0.35 * a, stroke=3))


def scene_white(c, t):
    studio_white(c)
    sa = eback(prog(t, COLD - 0.2, 0.35)) * (1 - prog(t, WARM - 0.1, 0.3))
    if sa > 0:
        snowflake(c, 540, 980, 210 * sa, COBALT, clamp(sa))
        qa = eback(prog(t, COLD + 0.2, 0.3)) * (1 - prog(t, NOTEX, 0.2))
        if qa > 0:
            fb = skia.Font(TF_BLACK, 150); c.drawString("?", 780, 860, fb, paint(INK, clamp(qa)))
        xa = eout(prog(t, NOTEX, 0.2))
        if xa > 0:
            c.drawLine(360, 800, lerp(360, 720, xa), lerp(800, 1160, xa), paint(RED, clamp(sa), stroke=22))
            c.drawLine(720, 800, lerp(720, 360, xa), lerp(800, 1160, xa), paint(RED, clamp(sa), stroke=22))
    wa = eout(prog(t, WARM - 0.1, 0.4))
    if wa > 0:
        q = eio(prog(t, WARM + 0.1, 1.6))
        thermo(c, 330, 1260, q, wa)
        # vessels opening, big and simple
        w = lerp(10, 36, eback(prog(t, WARM + 1.2, 0.6), 1.4))
        for k, yy in enumerate((900, 1060)):
            p = skia.Path(); p.moveTo(520, yy); p.cubicTo(640, yy - 40, 760, yy + 40, 900, yy)
            c.drawPath(p, paint(COPPER, 0.25 * wa, stroke=w + 22, blur=10))
            c.drawPath(p, paint("#E8644A", wa, stroke=w))
        pill(c, t, "THE WARM-UP", 710, 760, COPPER, WARM, WIPE2 + 0.2, light=True)
    footnote(c, t, "Main explanation from UCLA Health · still studied", WARM + 0.2, WIPE2 + 0.2, light=True)


def timer(c, t, x, y, a):
    q = eio(prog(t, MINUTE, 1.3))
    c.drawCircle(x, y, 90, paint("#ffffff", 0.1 * a, stroke=16))
    arc = skia.Path(); arc.addArc(skia.Rect.MakeLTRB(x - 90, y - 90, x + 90, y + 90), -90, 360 * q)
    c.drawPath(arc, paint(COPPER, a, stroke=16))
    s = f"0:{int(60 * (1 - q)):02d}"
    f = skia.Font(TF_BLACK, 52)
    c.drawString(s, x - f.measureText(s) / 2, y + 18, f, paint("#ffffff", a))


def scene_head2(c, t):
    bg_dark(c, t)
    cam = cam_at(t, CAMS2)
    st = dict(mouth=1 - prog(t, FADES - 0.3, 0.5))
    st["tongue"] = eout(prog(t, TONGUE - 0.1, 0.7))
    st["warmroof"] = eout(prog(t, TONGUE + 0.4, 0.8))
    st["pain"] = prog(t, FADES - 0.6, 0.3) * (1 - eout(prog(t, FADES + 0.2, 0.9)))
    draw_head(c, t, cam, st)
    pill(c, t, "TONGUE UP", 300, 640, PINK, TONGUE, FADES - 0.2, text_col=INK)
    pill(c, t, "WARMS IT UP", 300, 640, COPPER, TONGUE + 0.9, FADES)
    pill(c, t, "PAIN FADES", 300, 640, "#FFFFFF", FADES, SO)
    if t > MINUTE - 0.1:
        timer(c, t, 820, 650, eout(prog(t, MINUTE - 0.1, 0.3)))
    footnote(c, t, "Educational only, not medical advice", FIX + 0.3, SO)


def draw_world(c, t):
    m = mode_at(t)
    if m == "hook":
        draw_hook(c, t)
    elif m == "head":
        scene_head(c, t)
        if t < REVEAL + 0.45:   # snap zoom from the scoop out to the head
            q = eio(prog(t, REVEAL - 0.1, 0.5))
            c.saveLayerAlpha(None, int(255 * (1 - q)))
            c.save(); c.translate(540, 1100); c.scale(1 - 0.75 * q, 1 - 0.75 * q); c.translate(-540, -1100)
            draw_hook(c, t); c.restore(); c.restore()
    elif m == "bars":
        scene_bars(c, t)
        if t < STUDY + 0.3:
            c.saveLayerAlpha(None, int(255 * (1 - eout(prog(t, STUDY - 0.15, 0.4))))); scene_head(c, t); c.restore()
    elif m == "white":
        scene_white(c, t)
    elif m == "head2":
        scene_head2(c, t)
    else:
        q = eio(prog(t, SO - 0.05, DUR - SO - 0.02))
        draw_hook(c, t)
        if q < 1:
            c.saveLayerAlpha(None, int(255 * (1 - q)))
            c.save(); c.translate(540, 1100); c.scale(1 + 1.4 * q, 1 + 1.4 * q); c.translate(-540, -1100)
            scene_head2(c, t); c.restore(); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.025 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"head": RED, "freezing": COBALT, "roof": COBALT, "shrink": COBALT, "rush": COPPER, "alarm": YELLOW,
         "address": "#FFFFFF", "forehead": RED, "worse": RED, "twice": COPPER, "cold": COBALT, "exactly": RED,
         "warm-up": COPPER, "tongue": PINK, "fades": "#FFFFFF", "minute": COPPER}
CAPS = Captions(P, KWCOL, {"twice", "Not"}, DUR)


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    sx = sy = 0
    for ti in IMPACTS:
        d = t - ti
        if 0 <= d < 0.3:
            amp = 7 * (1 - d / 0.3); sx += amp * math.sin(d * 97); sy += amp * math.cos(d * 83)
    ps = cut_punch(t)
    c.save(); c.translate(sx, sy); c.translate(540, 960); c.scale(ps, ps); c.translate(-540, -960)
    draw_world(c, t)
    c.restore()
    light = mode_at(t) == "white"
    vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 560), paint(shader=linear((0, 0), (0, 560), [col("#000000", 0.35), col("#000000", 0)])))
    rw = math.sin(math.pi * prog(t, NOTEX, 0.4))
    if rw > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.18 * rw))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, COBALT, "#F4F2EE")
    wipe(c, t, WIPE2, WL, COPPER, "#111832")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", REVEAL - 0.1), ("pop", FREEZE), ("tick", FREEZE + 0.35), ("whoosh", ROOF - 0.1), ("pop", ROOF + 0.1),
          ("pop", SHRINK), ("pop", RUSH), ("whoosh", NERVE), ("pop", ALARM), ("whoosh", ADDRESS), ("hit", FOREHEAD),
          ("pop", WORSE), ("whoosh", STUDY - 0.15), ("ding", TWICE), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12),
          ("pop", COLD), ("hit", NOTEX), ("pop", WARM), ("riser", WARM + 0.2), ("whoosh", WIPE2), ("pop", TONGUE),
          ("pop", TONGUE + 0.9), ("pop", FADES), ("whoosh", SO - 0.05)]
    for k in range(6):
        ev.append(("tick", STUDY + 0.3 + k * 0.15))
    for k in range(6):
        ev.append(("tick", MINUTE + k * 0.2))
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

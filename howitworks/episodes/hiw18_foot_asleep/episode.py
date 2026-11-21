# HIW18 — "Why does your foot fall asleep?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-22):
#  - MSD Manual (Consumer), "When the Foot Is Asleep" (msdmanuals.com/home/multimedia/table/when-the-foot-is-asleep):
#    the foot falls asleep when pressure is put on the nerve that supplies it; pressure interferes with the blood supply
#    to the nerve, making it give off abnormal signals (pins and needles); relieving the pressure (moving around) restores it.
#  - The Conversation, "What happens when your foot falls asleep?" (theconversation.com/...-164655): nerves that connect
#    the brain to the foot get squished by the way you sit; once you move, pressure is released, nerves "wake up" -> pins
#    and needles; lasts "a minute or two"; tips: switch position often, don't cross legs too long, stand up every so often.
#  - Cleveland Clinic, "Should you worry about pins and needles?" (health.clevelandclinic.org/worry-pins-needles, 2023):
#    usually harmless and temporary, goes away after a couple of minutes; get checked if tingling comes suddenly without an
#    obvious cause or is constant / long-lasting.
#  Owner rule: no studies, plain words. Footnote: "Educational only, not medical advice."
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
SKIN = "#F1BE9B"; SKIN_D = "#D99C76"; NUMB = "#9FB3D6"; NERVE = "#FFC83D"; BLOOD = "#FF4D5E"; SPARK = "#FFE27A"
PURPLE = "#8C7BFF"; GREEN = "#1fb98a"; ORANGE = "#FF9F43"; BLUE = "#3E7BFA"; LAV = "#B9A8FF"


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


STAND = p0(ph("you stand")); NUMB1 = kw(ph("and it's")); PINS = kw(ph("then come"))
WIPE1 = p0(ph("okay")) - 0.3; NERVES = kw(ph("your foot talks")); CABLES = p0(ph("like cables"))
SIT = p0(ph("sit on")); CROSS = p0(ph("or cross")); SQUISH = kw(ph("and you squish"))
SQD = p0(ph("squished")); BLOODt = kw(ph("it gets less")); QUIET = kw(ph("so the messages")); NUMBP = kw(ph("that's the numb"))
WIPE2 = p0(ph("now you")) - 0.3; MOVE = kw(ph("now you")); OFF = p0(ph("the pressure's")); FIRE = kw(ph("and the nerve wakes"))
TINGLE = kw(ph("that's the tingle")); MIN = kw(ph("and it's gone"))
TRICK = p0(ph("the trick")); SWITCH = kw(ph("switch")); OFTEN = p0(ph("and stand up"))
NOWHERE = kw(ph("but tingling")); AWAY = kw(ph("or that won't")); DOC = p0(ph("see a doctor")); SO = p0(len(P) - 1)
WL = 0.32
IMPACTS = [NUMB1, SQUISH, FIRE]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1, ph_=0.0):
    return math.sin(2 * math.pi * k * t / DUR + ph_)


def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#1d1b2b"), col("#13121c"), col("#09080d")], [0, 0.55, 1])))
    c.drawCircle(800 + 30 * lw(t), 720, 520, paint(shader=radial(800, 720, 520, [col(PURPLE, 0.12), col(PURPLE, 0)])))
    c.drawCircle(220, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1450, 600, [col(NERVE, 0.06), col(NERVE, 0)])))


# ---------------- the foot (side view, toes right) ----------------
def foot_path():
    p = skia.Path()
    p.moveTo(-175, -390)
    p.lineTo(-150, -160)
    p.cubicTo(-148, -70, -235, -50, -235, 35)
    p.cubicTo(-235, 110, -175, 132, -100, 132)
    p.lineTo(205, 132)
    p.cubicTo(272, 132, 302, 110, 302, 78)
    p.cubicTo(302, 38, 262, 18, 205, 8)
    p.cubicTo(120, -6, 45, -60, -5, -150)
    p.lineTo(-25, -390)
    p.close()
    return p


FOOT = foot_path()


def foot(c, t, x, y, s, numb=0.0, a=1.0, sleepy=0.0, rot=0.0, sparks=0.0, fade=False):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if fade:
        c.saveLayer(None)
    c.drawOval(skia.Rect.MakeLTRB(-250, 120, 320, 175), paint("#000000", 0.22 * a, blur=18))
    top = mixhex("#F6CDAE", "#C7D5EE", numb); mid = mixhex(SKIN, NUMB, numb); bot = mixhex(SKIN_D, "#7E93BC", numb)
    c.drawPath(FOOT, paint(shader=linear((0, -390), (0, 132), [col(top, a), col(mid, a), col(bot, a)], [0, 0.6, 1])))
    # soft side highlight + arch shadow
    c.save(); c.clipPath(FOOT, doAntiAlias=True)
    c.drawOval(skia.Rect.MakeLTRB(-140, 40, 160, 190), paint(mixhex("#B97B57", "#6F82AA", numb), 0.35 * a, blur=26))
    c.drawOval(skia.Rect.MakeLTRB(-120, -300, -40, 0), paint("#ffffff", 0.18 * a, blur=22))
    c.restore()
    # toes (little bumps on top of the front)
    for k, (tx, ty, r) in enumerate(((262, 30, 34), (222, 18, 26), (190, 12, 22))):
        c.drawCircle(tx, ty + 6, r, paint(mixhex("#E9AD88", "#93A7CC", numb), 0.55 * a, stroke=3))
    c.drawRoundRect(skia.Rect.MakeLTRB(252, 22, 292, 48), 12, 12, paint("#FFE7DA", 0.9 * a))
    c.drawRoundRect(skia.Rect.MakeLTRB(252, 22, 292, 48), 12, 12, paint(mixhex("#D9937A", "#7F93BC", numb), 0.6 * a, stroke=2))
    # ankle bone
    c.drawCircle(-95, -110, 26, paint(mixhex("#E3A98A", "#90A4CA", numb), 0.55 * a, blur=6))
    c.drawPath(FOOT, paint(mixhex("#B5704E", "#5F739E", numb), 0.65 * a, stroke=4))
    # sleepy face on the side of the foot
    if sleepy > 0:
        ex, ey = 70, 40
        pth = skia.Path(); pth.moveTo(ex - 34, ey); pth.quadTo(ex, ey + 26, ex + 34, ey)
        c.drawPath(pth, paint("#5a3524", sleepy * a, stroke=6))
        for k in range(4):
            u = (k + 0.5) / 4
            lx = lerp(ex - 30, ex + 30, u); ly = ey + 13 * math.sin(math.pi * u)
            c.drawLine(lx, ly, lx + (u - 0.5) * 14, ly + 14, paint("#5a3524", sleepy * a, stroke=4))
        c.drawCircle(ex + 70, ey + 30, 18, paint("#FF8C8C", 0.35 * sleepy * a, blur=6))
    # pins & needles sparkles over the foot
    if sparks > 0:
        c.save(); c.clipPath(FOOT, doAntiAlias=True)
        for k in range(34):
            rr = random.Random(k)
            px = rr.uniform(-220, 290); py = rr.uniform(-380, 125)
            if not FOOT.contains(px, py): continue
            fl = 0.5 + 0.5 * math.sin(t * rr.uniform(14, 22) + rr.uniform(0, 6.28))
            sz = rr.uniform(9, 16) * (0.6 + 0.6 * fl)
            al = sparks * a * (0.35 + 0.65 * fl)
            c.drawLine(px - sz, py, px + sz, py, paint(SPARK, al, stroke=4))
            c.drawLine(px, py - sz, px, py + sz, paint(SPARK, al, stroke=4))
            c.drawCircle(px, py, sz * 0.9, paint(SPARK, 0.25 * al, blur=6))
        c.restore()
    if fade:
        m = skia.Paint(); m.setBlendMode(skia.BlendMode.kDstIn)
        m.setShader(linear((0, -390), (0, -170), [col("#000000", 0), col("#000000", 1)]))
        c.drawRect(skia.Rect.MakeLTRB(-400, -420, 400, 200), m)
        c.restore()
    c.restore()


def zzz(c, t, x, y, a):
    if a <= 0: return
    per = DUR / 6
    for k in range(3):
        u = ((t / per) + k / 3) % 1.0
        al = a * math.sin(math.pi * u)
        f = skia.Font(TF_BLACK, 44 + 30 * u)
        c.drawString("Z", x + 70 * u + 20 * math.sin(u * 6), y - 230 * u, f, paint(LAV, al))


# ---------------- hook ----------------
def scene_hook(c, t, a=1.0):
    bg_dark(c, t)
    foot(c, t, 470, 1080 + 14 * lw(t, 3), 1.1, 0.0, a, sleepy=1.0, rot=2 * lw(t, 2), fade=True)
    zzz(c, t, 640, 760, a)


def scene_open(c, t):
    bg_dark(c, t)
    nb = eout(prog(t, NUMB1 - 0.15, 0.4))
    sp = eout(prog(t, PINS - 0.1, 0.3))
    up = eio(prog(t, STAND - 0.1, 0.5))
    sl = 1 - prog(t, STAND - 0.1, 0.3)
    jit = sp * 5 * math.sin(t * 60)
    foot(c, t, 470 + jit, 1080 + 14 * lw(t, 3) - 40 * up, 1.1 + 0.08 * up, nb, 1.0, sleepy=sl, rot=2 * lw(t, 2), sparks=sp, fade=True)
    zzz(c, t, 640, 760, sl)
    if nb > 0:
        # dashed "numb" outline pulse
        r = 1 + 0.03 * math.sin(t * 6)
        c.save(); c.translate(470, 1080 - 40 * up); c.scale(1.1 * r, 1.1 * r); c.clipRect(skia.Rect.MakeLTRB(-400, -250, 400, 300))
        pe = paint(NUMB, 0.6 * nb * (1 - sp * 0.6), stroke=5); pe.setPathEffect(skia.DashPathEffect.Make([18, 14], t * 40))
        c.drawPath(FOOT, pe); c.restore()
    pill(c, t, "FOOT ASLEEP?", 495, 560, PURPLE, 0.35, STAND - 0.05)
    pill(c, t, "STAND UP...", 495, 560, "#8a8f98", STAND, NUMB1 - 0.05)
    pill(c, t, "NUMB!", 495, 560, BLUE, NUMB1, PINS - 0.05)
    pill(c, t, "PINS AND NEEDLES", 495, 560, "#C9A100", PINS, WIPE1 + 0.1, text_col="#FFFFFF")


# ---------------- white: nerve cable diagram ----------------
BRX, BRY = 215, 700


def cable_path(pinch=0.0, dy=0.0):
    p = skia.Path()
    p.moveTo(BRX, BRY + 60)
    p.lineTo(BRX, 935 + dy)
    p.lineTo(380, 935 + dy)
    p.quadTo(420, 935 + dy + 34 * pinch, 460, 935 + dy)
    p.lineTo(600, 935 + dy)
    p.quadTo(640 + dy * 0.2, 935 + dy, 640 + dy * 0.2, 990)
    p.lineTo(640 + dy * 0.2, 1270)
    p.quadTo(640 + dy * 0.2, 1320, 720, 1325)
    p.lineTo(830, 1330)
    return p


def brain(c, x, y, a, glow=0.0):
    if a <= 0: return
    c.drawCircle(x, y, 95, paint("#FF8FB1", 0.25 * glow * a, blur=30))
    c.drawOval(skia.Rect.MakeLTRB(x - 85, y - 62, x + 85, y + 62), paint(shader=radial(x - 20, y - 30, 120, [col("#FFC2D4", a), col("#FF8FB1", a)])))
    for k in range(3):
        pp = skia.Path(); pp.moveTo(x - 60, y - 25 + k * 24)
        pp.cubicTo(x - 30, y - 45 + k * 24, x - 10, y - 5 + k * 24, x + 20, y - 25 + k * 24)
        pp.cubicTo(x + 40, y - 40 + k * 24, x + 55, y - 15 + k * 24, x + 66, y - 22 + k * 24)
        c.drawPath(pp, paint("#D9577F", 0.7 * a, stroke=5))
    c.drawLine(x, y - 58, x, y + 58, paint("#D9577F", 0.5 * a, stroke=4))


def leg(c, a, numb):
    lp = skia.Path(); lp.moveTo(150, 960); lp.lineTo(610, 960); lp.lineTo(640, 1270)
    pe = paint(mixhex(SKIN, NUMB, numb * 0.4), a, stroke=150); pe.setStrokeJoin(skia.Paint.kRound_Join)
    c.drawPath(lp, paint("#000000", 0.12 * a, stroke=160, blur=16))
    c.drawPath(lp, pe)
    hl = paint("#ffffff", 0.22 * a, stroke=30, blur=8); c.drawLine(170, 915, 590, 915, hl)


def pulses(c, t, path, a, n, speed, color, upto=1.0, fade_after=None, size=13):
    m = skia.PathMeasure(path, False); L = m.getLength()
    for k in range(n):
        u = ((t * speed) + k / n) % 1.0
        if u > upto: continue
        ok, pt, tg = (True,) + tuple(m.getPosTan(u * L))
        al = a
        if fade_after is not None and u > fade_after:
            al *= clamp(1 - (u - fade_after) / 0.06)
        if al <= 0: continue
        c.drawCircle(pt.x(), pt.y(), size * 2.2, paint(color, 0.3 * al, blur=10))
        c.drawCircle(pt.x(), pt.y(), size, paint(color, al))


def other_leg(c, t, a, press):
    if a <= 0: return
    y = lerp(560, 815, press)
    c.drawRoundRect(skia.Rect.MakeLTRB(290, y - 70 + 10, 560, y + 70 + 10), 70, 70, paint("#000000", 0.18 * a, blur=14))
    c.drawRoundRect(skia.Rect.MakeLTRB(290, y - 70, 560, y + 70), 70, 70,
                    paint(shader=linear((0, y - 70), (0, y + 70), [col("#9AA7FF", a), col("#6E7BE6", a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(290, y - 70, 560, y + 70), 70, 70, paint("#4f5ac4", a, stroke=4))
    c.drawLine(320, y - 40, 530, y - 40, paint("#ffffff", 0.25 * a, stroke=10, blur=3))


def diagram(c, t, a, dark):
    """shared leg + nerve + blood diagram, used in WHITE and DARK chapters."""
    press = clamp(eio(prog(t, SQUISH - 0.2, 0.35)) * (1 - eout(prog(t, MOVE - 0.1, 0.35))))
    ol_a = a * clamp(prog(t, SIT - 0.1, 0.3)) * (1 - prog(t, OFF, 0.35))
    numb = eout(prog(t, QUIET - 0.1, 0.5)) * (1 - eout(prog(t, MIN, 0.8)))
    leg(c, a, numb)
    foot(c, t, 690, 1350, 0.5, numb, a, sparks=eout(prog(t, FIRE, 0.25)) * (1 - prog(t, MIN + 0.5, 0.6)))
    bp = cable_path(press, dy=26)
    np_ = cable_path(press)
    show_b = a * eout(prog(t, BLOODt - 0.2, 0.3))
    c.drawPath(bp, paint(BLOOD, 0.35 * show_b, stroke=12))
    c.drawPath(np_, paint(NERVE, 0.35 * a, stroke=14, blur=3))
    c.drawPath(np_, paint(mixhex(NERVE, "#B8B8B8", numb * (1 - prog(t, MOVE, 0.3))), 0.95 * a, stroke=8))
    # flows: blood + nerve messages; blocked past the pinch while squished
    m = skia.PathMeasure(np_, False); L = m.getLength()
    pin_u = (abs(935 - (BRY + 60)) + (420 - BRX)) / L
    blocked = clamp(press * 1.2) * (1 - prog(t, OFF, 0.2))
    fire = eout(prog(t, FIRE - 0.1, 0.3)) * (1 - prog(t, MIN + 0.4, 0.8))
    spd = 0.45 * (1 - 0.6 * blocked) + 0.6 * fire
    if show_b > 0:
        pulses(c, t, bp, show_b * 0.9, 9, 0.30 * (1 - 0.8 * blocked), BLOOD, fade_after=(pin_u if blocked > 0.5 else None), size=9)
    quiet = eout(prog(t, QUIET - 0.1, 0.4)) * (1 - prog(t, OFF, 0.2))
    pulses(c, t, np_, a * (1 - quiet * 0.85), 7 + int(10 * fire), spd, NERVE if fire < 0.3 else SPARK,
           fade_after=(pin_u if blocked > 0.5 else None), size=12 + 5 * fire)
    brain(c, BRX, BRY, a * eout(prog(t, NERVES - 0.2, 0.35)) if not dark else a, glow=0.5 + 0.5 * math.sin(t * 5))
    other_leg(c, t, ol_a, press)
    # the pinch marker
    if blocked > 0.3 and a > 0:
        c.drawCircle(420, 935, 46 + 6 * math.sin(t * 9), paint(RED, 0.8 * a * blocked, stroke=5))
    return numb


def scene_cable(c, t):
    studio_white(c)
    a = eout(prog(t, WIPE1, 0.4))
    z = lerp(1.15, 1.0, eio(prog(t, WIPE1, 1.0)))
    c.save(); c.translate(495, 1020); c.scale(z, z); c.translate(-495, -1020)
    numb = diagram(c, t, a, False)
    c.restore()
    f = skia.Font(TF_MONO, 24)
    la = a * window(t, NERVES, SIT, 0.3, 0.3)
    if la > 0:
        c.drawString("BRAIN", BRX - 40, BRY - 90, f, paint(INK, 0.6 * la))
        c.drawString("NERVE = CABLE", 700, 900, f, paint("#B8860B", la))
    pill(c, t, "LONG NERVES", 495, 560, "#C9A100", NERVES, CABLES - 0.05, text_col="#FFFFFF")
    pill(c, t, "LIKE CABLES", 495, 560, "#C9A100", CABLES, SIT - 0.05, text_col="#FFFFFF")
    pill(c, t, "SIT ON IT", 495, 560, "#6E7BE6", SIT, CROSS - 0.05)
    pill(c, t, "CROSSED LEGS", 495, 560, "#6E7BE6", CROSS, SQUISH - 0.05)
    pill(c, t, "SQUISHED!", 495, 560, RED, SQUISH, BLOODt - 0.05)
    pill(c, t, "LESS BLOOD", 495, 560, BLOOD, BLOODt, QUIET - 0.05)
    pill(c, t, "MESSAGES GO QUIET", 495, 560, "#8a8f98", QUIET, NUMBP - 0.05)
    pill(c, t, "= NUMB", 495, 560, BLUE, NUMBP, WIPE2 + 0.1)


# ---------------- dark: wake up, tingle, timer ----------------
def scene_wake(c, t):
    bg_dark(c, t)
    a = eout(prog(t, WIPE2, 0.4))
    zin = eio(prog(t, TINGLE - 0.2, 0.6))
    cx = lerp(495, 690, zin); cy = lerp(1020, 1220, zin); z = lerp(1.0, 1.55, zin)
    c.save(); c.translate(495, 1020); c.scale(z, z); c.translate(-cx, -cy)
    diagram(c, t, a, True)
    c.restore()
    # timer ring for "a minute or two"
    ta = eback(prog(t, MIN - 0.15, 0.35)) * (1 - prog(t, TRICK - 0.3, 0.25))
    if ta > 0:
        x, y = 790, 800
        c.save(); c.translate(x, y); c.scale(ta, ta)
        c.drawCircle(0, 0, 120, paint("#000000", 0.35, blur=12))
        c.drawCircle(0, 0, 110, paint("#1d1b2b"))
        c.drawCircle(0, 0, 100, paint("#ffffff", 0.15, stroke=14))
        u = eio(prog(t, MIN, 0.55))
        c.drawArc(skia.Rect.MakeLTRB(-100, -100, 100, 100), -90, 360 * u, False, paint(GREEN, 1, stroke=14))
        secs = int(120 * u); s = f"{secs // 60}:{secs % 60:02d}"
        f = skia.Font(TF_MONO, 52)
        c.drawString(s, -f.measureText(s) / 2, 18, f, paint("#ffffff"))
        c.restore()
    pill(c, t, "YOU MOVE", 495, 560, GREEN, MOVE, OFF - 0.05, text_col="#FFFFFF")
    pill(c, t, "PRESSURE OFF", 495, 560, GREEN, OFF, FIRE - 0.05, text_col="#FFFFFF")
    pill(c, t, "ALL AT ONCE!", 495, 560, "#C9A100", FIRE, TINGLE - 0.05, text_col="#FFFFFF")
    pill(c, t, "THE TINGLE", 495, 560, "#C9A100", TINGLE, MIN - 0.05, text_col="#FFFFFF")
    pill(c, t, "1-2 MINUTES", 495, 560, GREEN, MIN, TRICK + 0.1, text_col="#FFFFFF")


def sitter(c, x, y, s, stand, cross, a):
    """simple rounded person: sits (stand=0) or stands (stand=1); cross = legs crossed."""
    c.save(); c.translate(x, y); c.scale(s, s)
    colr = mixhex("#9AA7FF", GREEN, stand)
    # chair
    c.drawRoundRect(skia.Rect.MakeLTRB(-150, 40, 40, 70), 14, 14, paint("#5a5d6a", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-150, -150, -120, 70), 14, 14, paint("#5a5d6a", a))
    c.drawLine(-140, 70, -140, 230, paint("#5a5d6a", a, stroke=16)); c.drawLine(30, 70, 30, 230, paint("#5a5d6a", a, stroke=16))
    c.translate(130 * stand, 0)
    hip = (lerp(-70, -40, stand), lerp(20, -60, stand))
    sh = (lerp(-95, -40, stand), lerp(-200, -300, stand))
    c.drawLine(hip[0], hip[1], sh[0], sh[1], paint(colr, a, stroke=70))
    c.drawCircle(sh[0] + lerp(10, 0, stand), sh[1] - 85, 50, paint(colr, a))
    # legs
    for k in (0, 1):
        knee = (lerp(60, -40 + k * 10, stand), lerp(20 - k * 4 - 40 * cross * k, 80, stand))
        foot_ = (lerp(70 + 50 * cross * k, -30 + k * 20, stand), lerp(220 - 120 * cross * k, 230, stand))
        cc = colr if k == 0 else mixhex(colr, "#ffffff", 0.18)
        c.drawLine(hip[0], hip[1], knee[0], knee[1], paint(cc, a, stroke=52))
        c.drawLine(knee[0], knee[1], foot_[0], foot_[1], paint(cc, a, stroke=46))
    c.restore()


def scene_tips(c, t):
    bg_dark(c, t)
    a = eout(prog(t, TRICK - 0.3, 0.35))
    # switch positions: legs cross / uncross; then stand up
    cr = 0.5 + 0.5 * math.sin((t - SWITCH) * 5) if t > SWITCH else 1.0
    st = eio(prog(t, OFTEN, 0.6))
    cr = lerp(cr, 0, st)
    sitter(c, 560, 1150, 1.15, st, cr, a)
    # swap arrows
    sa = a * window(t, SWITCH - 0.1, OFTEN + 0.1, 0.2, 0.2)
    if sa > 0:
        for k in (0, 1):
            ang = t * 3 + k * math.pi
            c.drawArc(skia.Rect.MakeLTRB(560 + 40, 1110, 560 + 240, 1310), math.degrees(ang), 120, False, paint(ORANGE, sa, stroke=10))
    # clock icon for "every so often"
    ca = eback(prog(t, OFTEN + 0.1, 0.35)) * a
    if ca > 0:
        c.save(); c.translate(230, 790); c.scale(ca, ca)
        c.drawCircle(0, 0, 80, paint("#ffffff", 0.95))
        c.drawCircle(0, 0, 80, paint(GREEN, 1, stroke=8))
        an = t * 4
        c.drawLine(0, 0, 50 * math.cos(an), 50 * math.sin(an), paint(INK, 1, stroke=8))
        c.drawLine(0, 0, 0, -38, paint(INK, 1, stroke=10))
        c.restore()
    pill(c, t, "THE TRICK", 495, 560, "#8a8f98", TRICK, SWITCH - 0.05)
    pill(c, t, "SWITCH POSITIONS", 495, 560, ORANGE, SWITCH, OFTEN - 0.05)
    pill(c, t, "STAND UP OFTEN", 495, 560, GREEN, OFTEN, NOWHERE - 0.1, text_col="#FFFFFF")


def warn_card(c, t, x, y, kind, a, hl):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    rect = skia.Rect.MakeLTRB(-170, -190, 170, 190)
    c.drawRoundRect(rect, 34, 34, paint("#000000", 0.3, blur=14))
    c.drawRoundRect(rect, 34, 34, paint("#25222a"))
    c.drawRoundRect(rect, 34, 34, paint(mixhex("#4a4652", RED, hl), 1, stroke=3 + 2 * hl))
    if kind == "bolt":
        fl = 0.6 + 0.4 * max(0, math.sin(t * 7)) ** 4
        z = skia.Path(); z.moveTo(20, -140); z.lineTo(-50, -10); z.lineTo(0, -10); z.lineTo(-30, 90); z.lineTo(60, -40); z.lineTo(10, -40); z.lineTo(50, -140); z.close()
        c.drawPath(z, paint(SPARK, fl))
    else:
        c.drawCircle(0, -30, 95, paint("#ffffff", 0.12, stroke=12))
        an = t * 2.2
        c.drawArc(skia.Rect.MakeLTRB(-95, -125, 95, 65), math.degrees(an), 270, False, paint(ORANGE, 1, stroke=12))
        hx, hy = 95 * math.cos(an + math.radians(270)), -30 + 95 * math.sin(an + math.radians(270))
        c.drawCircle(hx, hy, 16, paint(ORANGE))
    f = skia.Font(TF_MONO, 26)
    lab = {"bolt": "OUT OF NOWHERE", "loop": "WON'T GO AWAY"}[kind]
    c.drawString(lab, -f.measureText(lab) / 2, 150, f, paint(mixhex("#ffffff", RED, hl * 0.6)))
    c.restore()


def scene_warn(c, t):
    bg_dark(c, t)
    c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.05 * (0.5 + 0.5 * math.sin(t * 4))))
    for x, y, kind, tin in ((300, 960, "bolt", NOWHERE), (690, 1060, "loop", AWAY)):
        q = eback(prog(t, tin - 0.15, 0.35))
        warn_card(c, t, x, y, kind, clamp(q, 0, 1.2), eout(prog(t, tin, 0.3)) * (1 - 0.5 * prog(t, DOC, 0.3)))
    pill(c, t, "OUT OF NOWHERE?", 495, 560, RED, NOWHERE, AWAY - 0.05)
    pill(c, t, "WON'T GO AWAY?", 495, 560, RED, AWAY, DOC - 0.05)
    pill(c, t, "SEE A DOCTOR", 495, 560, RED, DOC, SO + 0.3)
    footnote(c, t, "Educational only, not medical advice.", NOWHERE - 0.2, SO + 0.4)


def xfade(c, t, t0, d, new, old):
    q = 1 - prog(t, t0, d)
    new(c, t)
    if q > 0:
        c.saveLayerAlpha(None, int(255 * q)); old(c, t); c.restore()


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_cable(c, t); return
    if t < TRICK - 0.3:
        scene_wake(c, t); return
    if t < NOWHERE - 0.25:
        xfade(c, t, TRICK - 0.3, 0.3, scene_tips, scene_wake); return
    if t < SO - 0.05:
        xfade(c, t, NOWHERE - 0.25, 0.3, scene_warn, scene_tips); return
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
    out = []
    for p in PH:
        ws = p["words"]
        if len(ws) <= maxw:
            out.append(p); continue
        k = (len(ws) + 1) // 2
        out.append(dict(p, words=ws[:k], t1=ws[k - 1]["t1"]))
        out.append(dict(p, words=ws[k:], t0=ws[k]["t0"]))
    return out


KWCOL = {"asleep": PURPLE, "numb": BLUE, "pins": "#C9A100", "needles": "#C9A100", "nerves": "#C9A100", "squish": RED,
         "blood": BLOOD, "quiet": "#8a8f98", "move": GREEN, "firing": "#C9A100", "tingle": "#C9A100",
         "minute": GREEN, "two": GREEN, "switch": ORANGE, "often": GREEN, "nowhere": RED, "away": RED}
CAPS = Captions(split_long(P), KWCOL, {"squish", "firing"}, DUR)


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
    wipe(c, t, WIPE1, WL, PURPLE, "#F4F2EE")
    wipe(c, t, WIPE2, WL, NERVE, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("whoosh", STAND), ("hit", NUMB1), ("pop", PINS),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", NERVES), ("pop", CABLES), ("whoosh", SIT - 0.1),
          ("pop", CROSS), ("hit", SQUISH), ("pop", BLOODt), ("pop", QUIET), ("pop", NUMBP), ("whoosh", WIPE2),
          ("pop", MOVE), ("riser", OFF - 0.1), ("hit", FIRE), ("pop", TINGLE), ("ding", MIN + 1.2),
          ("whoosh", TRICK - 0.3), ("pop", SWITCH), ("pop", OFTEN), ("whoosh", NOWHERE - 0.25), ("hit", NOWHERE),
          ("pop", AWAY), ("ding", DOC), ("whoosh", SO - 0.05)]
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

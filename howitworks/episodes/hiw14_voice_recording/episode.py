# HIW14 — "Ever heard your voice on a recording... and thought, ew?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-20):
#  - Popular Science "Why does my voice sound different when I hear it on a recording?" (Vanderbilt audiology): your voice
#    reaches your ears two ways, through the air and through vibrations in your skull/bones; the bone route carries more
#    low frequencies, so you sound deeper/fuller to yourself; a recording only captures the air route, so it sounds thinner;
#    it feels strange because you're not used to it.
#  - Wonderopolis / How Everything Works "Why does your voice sound different to you?": same two-path explanation; the
#    recording is how everyone else hears you.
#  Owner rule: no studies, plain words.
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
AIR = "#4DB8FF"; BONE = "#FF9A3D"; REC = "#FF3B5C"; PURP = "#9B7BFF"; GREEN = "#1fb98a"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


EW = kw(2); NOT = kw(3); WELL = p0(4); ITIS = kw(5); ELSE1 = kw(6)
WIPE1 = p0(7) - 0.3; TWO = kw(8); AIRt = kw(9); SKULL = kw(10); DEEP = kw(11); INHEAD = p0(12); RICH = kw(13)
WIPE2 = p0(14) - 0.3; MIC = p0(14); MICAIR = kw(14); THIN = kw(15); ELSE2 = kw(16); WEIRD = p0(17); USED = kw(18); SO = p0(19)
WL = 0.32
IMPACTS = [EW, ITIS]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1):
    return math.sin(2 * math.pi * k * t / DUR)


# ---------------- parts ----------------
def bg(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#1f1a2c"), col("#121019"), col("#08070b")], [0, 0.55, 1])))
    c.drawCircle(250 + 30 * lw(t), 800, 520, paint(shader=radial(250, 800, 520, [col(AIR, 0.12), col(AIR, 0)])))
    c.drawCircle(850, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(850, 1450, 600, [col(BONE, 0.10), col(BONE, 0)])))


def waveform(c, x, y, w, h, t, colr, a, rich=0.0, n=46, speed=1.0, play=None):
    """Bar waveform centred at x,y. rich adds low 'body'."""
    if a <= 0: return
    bw = w / n
    for i in range(n):
        u = i / (n - 1)
        env = 0.35 + 0.65 * abs(math.sin(u * 9.3 + 1.1) * math.sin(u * 3.1 + 0.4))
        wob = 0.75 + 0.25 * math.sin(2 * math.pi * 6 * t / DUR * speed * 4 + i * 0.7)
        hh = h * env * wob * (0.55 + 0.45 * rich)
        cc = colr
        if play is not None and u > play:
            cc = "#ffffff"; aa = 0.25 * a
        else:
            aa = a
        xx = x - w / 2 + i * bw
        c.drawRoundRect(skia.Rect.MakeLTRB(xx + bw * 0.2, y - hh / 2, xx + bw * 0.8, y + hh / 2), bw * 0.3, bw * 0.3, paint(cc, aa))


def phone(c, t, x, y, s, a=1.0, play=None, rich=0.0, wcol=None):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    body = skia.Rect.MakeLTRB(-200, -400, 200, 400)
    c.drawRoundRect(body.makeOffset(0, 20), 60, 60, paint("#000000", 0.45 * a, blur=30))
    c.drawRoundRect(body, 60, 60, paint(shader=linear((-200, -400), (200, 400), [col("#3a3a44", a), col("#1b1b22", a)])))
    scr = skia.Rect.MakeLTRB(-184, -384, 184, 384)
    c.drawRoundRect(scr, 48, 48, paint(shader=linear((0, -384), (0, 384), [col("#16151d", a), col("#0d0c12", a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(-50, -370, 50, -344), 13, 13, paint("#000000", a))
    f = skia.Font(TF_MONO, 24); fb = skia.Font(TF_BOLD, 34)
    c.drawString("Voice Memo", -150, -250, fb, paint("#ffffff", a))
    c.drawCircle(-138, -196, 9, paint(REC, a * (0.6 + 0.4 * math.sin(2 * math.pi * 10 * t / DUR))))
    c.drawString("New Recording 7", -118, -188, f, paint("#ffffff", 0.55 * a))
    waveform(c, 0, -20, 320, 230, t, wcol or REC, a, rich=rich, n=30, play=play)
    # scrubber
    pp = play if play is not None else (t / DUR)
    c.drawRoundRect(skia.Rect.MakeLTRB(-150, 170, 150, 176), 3, 3, paint("#ffffff", 0.2 * a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-150, 170, -150 + 300 * pp, 176), 3, 3, paint(wcol or REC, a))
    c.drawCircle(-150 + 300 * pp, 173, 11, paint("#ffffff", a))
    tt = f"0:{int(7 * pp):02d}"
    c.drawString(tt, -150, 216, f, paint("#ffffff", 0.5 * a)); c.drawString("0:07", 150 - f.measureText("0:07"), 216, f, paint("#ffffff", 0.5 * a))
    # pause button
    c.drawCircle(0, 300, 52, paint("#ffffff", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-18, 278, -6, 322), 4, 4, paint("#0d0c12", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(6, 278, 18, 322), 4, 4, paint("#0d0c12", a))
    c.restore()


def face(c, x, y, r, mood, t, a=1.0):
    """mood: 'neutral', 'cringe', 'shock', 'smile'"""
    if a <= 0: return
    c.save(); c.translate(x, y)
    c.drawCircle(0, 8, r, paint("#000000", 0.3 * a, blur=14))
    c.drawCircle(0, 0, r, paint(shader=radial(-r * 0.3, -r * 0.4, r * 1.4, [col("#FFE48A", a), col("#FFC93C", a), col("#E9A21B", a)], [0, 0.6, 1])))
    ink = paint("#5a3410", a, stroke=r * 0.09)
    fill = paint("#5a3410", a)
    if mood == "cringe":
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(sx * r * 0.48, -r * 0.08); p.lineTo(sx * r * 0.2, -r * 0.18); p.lineTo(sx * r * 0.48, -r * 0.3)
            c.drawPath(p, ink)
        m = skia.Path(); m.moveTo(-r * 0.45, r * 0.42)
        for k in range(1, 7):
            m.lineTo(-r * 0.45 + k * r * 0.15, r * (0.42 + (0.1 if k % 2 else -0.0)))
        c.drawPath(m, ink)
        c.drawOval(skia.Rect.MakeLTRB(-r * 0.75, r * 0.05, -r * 0.45, r * 0.25), paint("#ff8a8a", 0.5 * a))
        c.drawOval(skia.Rect.MakeLTRB(r * 0.45, r * 0.05, r * 0.75, r * 0.25), paint("#ff8a8a", 0.5 * a))
    elif mood == "shock":
        for sx in (-1, 1):
            c.drawCircle(sx * r * 0.32, -r * 0.15, r * 0.13, fill)
            c.drawLine(sx * r * 0.18, -r * 0.45, sx * r * 0.48, -r * 0.5, ink)
        c.drawOval(skia.Rect.MakeLTRB(-r * 0.18, r * 0.25, r * 0.18, r * 0.65), fill)
    elif mood == "smile":
        for sx in (-1, 1):
            c.drawArc(skia.Rect.MakeLTRB(sx * r * 0.32 - r * 0.15, -r * 0.3, sx * r * 0.32 + r * 0.15, -r * 0.05), 200, 140, False, ink)
        c.drawArc(skia.Rect.MakeLTRB(-r * 0.4, r * 0.0, r * 0.4, r * 0.55), 20, 140, False, ink)
    else:
        for sx in (-1, 1):
            c.drawCircle(sx * r * 0.32, -r * 0.12, r * 0.09, fill)
        c.drawLine(-r * 0.25, r * 0.38, r * 0.25, r * 0.38, ink)
    c.restore()


def listener(c, t, x, y, s, a, hear=0.0, colr=REC, seed=0):
    """Small person (head+shoulders) with sound arcs arriving at the ear."""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    sh = skia.Path(); sh.moveTo(-110, 200); sh.cubicTo(-110, 80, 110, 80, 110, 200); sh.close()
    cc = ["#5B6CFF", "#2fb39a", "#d9637f"][seed % 3]
    c.drawPath(sh, paint(cc, a))
    face(c, 0, 0, 80, "neutral", t, a)
    if hear > 0:
        for k in range(3):
            u = ((t * 1.2 + k / 3) % 1)
            c.drawArc(skia.Rect.MakeXYWH(-60 - 60 * u - 120, -60 - 60 * u, 120 + 120 * u, 120 + 120 * u), 150, 60, False, paint(colr, hear * a * (1 - u), stroke=6))
    c.restore()


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
EAR = (-60, -40)
MOUTH = (238, 112)
THROAT = (120, 250)


def wave_path(p, colr, a, t, width=8, amp=14, wl=60, speed=8):
    """Draw a wavy line along a path (by sampling)."""
    if a <= 0: return
    pm = skia.PathMeasure(p, False); L = pm.getLength()
    q = skia.Path(); n = max(10, int(L / 6))
    for i in range(n + 1):
        s = L * i / n
        pos, tan = pm.getPosTan(s)
        nx, ny = -tan.y(), tan.x()
        o = amp * math.sin(2 * math.pi * s / wl - t * speed)
        x, y = pos.x() + nx * o, pos.y() + ny * o
        q.moveTo(x, y) if i == 0 else q.lineTo(x, y)
    c_ = paint(colr, 0.3 * a, stroke=width * 3, blur=8)
    return q, c_, paint(colr, a, stroke=width)


def draw_head(c, t, cx, cy, z, st):
    c.save(); c.translate(cx, cy); c.scale(z, z)
    c.drawPath(HEAD, paint("#000000", 0.25, blur=40))
    c.drawPath(HEAD, paint(shader=linear((-260, -300), (270, 300), [col("#F2C3A0"), col("#E2A882"), col("#C88A65")])))
    sk = st.get("skull", 0)
    c.save(); c.clipPath(HEAD)
    if sk > 0:
        inner = skia.Path(); inner.addOval(skia.Rect.MakeLTRB(-235, -290, 200, 60))
        c.drawPath(inner, paint("#FFF4E6", 0.55 * sk))
        c.drawPath(inner, paint("#E9D2B8", sk, stroke=18))
        c.drawRoundRect(skia.Rect.MakeLTRB(150, 60, 240, 210), 30, 30, paint("#FFF4E6", 0.5 * sk))
        # bone vibration route throat -> ear
        bp = skia.Path(); bp.moveTo(*THROAT); bp.cubicTo(60, 160, 0, 60, EAR[0] + 20, EAR[1] + 10)
        r = wave_path(bp, BONE, sk * st.get("boneflow", 0), t, width=9, amp=lerp(10, 22, st.get("deep", 0)), wl=lerp(50, 110, st.get("deep", 0)))
        if r:
            q, g, pp = r; c.drawPath(q, g); c.drawPath(q, pp)
        if st.get("boneflow", 0) > 0:
            for k in range(3):
                u = ((t * 0.8 + k / 3) % 1)
                c.drawCircle(EAR[0], EAR[1], 30 + 90 * u, paint(BONE, 0.6 * sk * (1 - u) * st.get("boneflow", 0), stroke=5))
    c.restore()
    c.drawPath(HEAD, paint("#ffffff", 0.25, stroke=3, blur=2))
    c.drawArc(skia.Rect.MakeLTRB(130, -110, 180, -80), 20, 140, False, paint("#7a4a32", 0.9, stroke=5))
    c.drawLine(120, -140, 185, -150, paint("#8a5a3a", 0.8, stroke=7))
    # ear
    c.drawOval(skia.Rect.MakeLTRB(EAR[0] - 34, EAR[1] - 56, EAR[0] + 34, EAR[1] + 56), paint("#D99A76"))
    c.drawOval(skia.Rect.MakeLTRB(EAR[0] - 18, EAR[1] - 34, EAR[0] + 18, EAR[1] + 34), paint("#B97B57"))
    # air route: from mouth out and around to the ear (outside)
    aa = st.get("air", 0)
    if aa > 0:
        ap = skia.Path(); ap.moveTo(MOUTH[0] + 20, MOUTH[1]); ap.cubicTo(360, 120, 380, -370, 80, -380)
        ap.cubicTo(-200, -390, -300, -150, EAR[0] - 40, EAR[1] - 10)
        pm = skia.PathMeasure(ap, False); L = pm.getLength()
        dash = skia.Path()
        rr = wave_path(ap, AIR, aa, t, width=7, amp=10, wl=46)
        if rr:
            q, g, pp = rr
            pr = st.get("airp", 1.0)
            if pr < 0.999:
                te = skia.TrimPathEffect.Make(0, max(0.001, pr))
                if te: pp.setPathEffect(te); g.setPathEffect(skia.TrimPathEffect.Make(0, max(0.001, pr)))
            c.drawPath(q, g); c.drawPath(q, pp)
        for k in range(3):
            u = ((t * 0.8 + k / 3) % 1)
            c.drawArc(skia.Rect.MakeXYWH(MOUTH[0] + 10, MOUTH[1] - 30 - 40 * u, 60 + 80 * u, 60 + 80 * u), -60, 120, False, paint(AIR, aa * (1 - u), stroke=5))
    c.restore()


def mic(c, x, y, s, a):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -170, 70, 40), 70, 70, paint("#000000", 0.3 * a, blur=12))
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -170, 70, 40), 70, 70, paint(shader=linear((-70, 0), (70, 0), [col("#e9ecf1", a), col("#9aa2ad", a), col("#5d636c", a)])))
    for k in range(6):
        c.drawLine(-60, -140 + k * 28, 60, -140 + k * 28, paint("#4a4f57", 0.5 * a, stroke=3))
    c.drawArc(skia.Rect.MakeLTRB(-110, -60, 110, 140), 0, 180, False, paint("#c9ced6", a, stroke=12))
    c.drawLine(0, 140, 0, 250, paint("#c9ced6", a, stroke=12))
    c.drawLine(-80, 250, 80, 250, paint("#c9ced6", a, stroke=14))
    c.restore()


# ---------------- scenes ----------------
def hook_pose(t):
    return 495 + 10 * lw(t), 1060 + 12 * lw(t, 2), 1.15 + 0.015 * lw(t)


def scene_hook(c, t):
    bg(c, t)
    x, y, s = hook_pose(t)
    phone(c, t, x, y, s, 1.0, play=(3 * t / DUR) % 1)
    for k in range(3):
        u = ((t * 1.0 + k / 3) % 1)
        c.drawArc(skia.Rect.MakeXYWH(x + 250 * s, y - 120 - 80 * u, 80 + 160 * u, 160 + 160 * u), -50, 100, False, paint(REC, 0.6 * (1 - u), stroke=6))


def scene_open(c, t):
    scene_hook(c, t)
    pill(c, t, "YOUR VOICE", 495, 560, REC, 0.35, EW - 0.05)
    fa = window(t, EW - 0.15, WELL, 0.2, 0.2)
    if fa > 0:
        s = eback(prog(t, EW - 0.15, 0.35))
        mood = "cringe" if t < NOT - 0.05 else "shock"
        c.save(); c.translate(790, 760); c.scale(s, s); c.translate(-790, -760)
        face(c, 790, 760, 120, mood, t, fa)
        c.restore()
    pill(c, t, "EW?!", 495, 560, REC, EW, NOT - 0.05)
    pill(c, t, "NOT ME!", 495, 560, "#8a8f98", NOT, ITIS - 0.05)
    # 'it is' -> everyone else hears this
    ia = window(t, ITIS - 0.15, WIPE1 + 0.25, 0.2, 0.2)
    if ia > 0:
        c.saveLayerAlpha(None, int(255 * ia)); bg(c, t); c.restore()
        x, y, s = hook_pose(t)
        sz = lerp(1.0, 0.62, eio(prog(t, ELSE1 - 0.2, 0.4)))
        phone(c, t, x, lerp(y, 890, eio(prog(t, ELSE1 - 0.2, 0.4))), s * sz, ia, play=(3 * t / DUR) % 1)
        for k in range(3):
            q = eback(prog(t, ELSE1 - 0.05 + k * 0.12, 0.35))
            listener(c, t, 230 + k * 265, 1330, 0.8 * clamp(q, 0, 1.2), ia * clamp(q), hear=1.0, seed=k)
    pill(c, t, "IT IS.", 495, 560, GREEN, ITIS, ELSE1 - 0.05, text_col="#FFFFFF")
    pill(c, t, "TO EVERYONE ELSE", 495, 560, REC, ELSE1, WIPE1 + 0.1)


def scene_white(c, t):
    studio_white(c)
    ga = eout(prog(t, WIPE1, 0.4))
    z = lerp(1.12, 1.2, eio(prog(t, DEEP - 0.3, 0.6)))
    cx = lerp(450, 480, eio(prog(t, DEEP - 0.3, 0.6)))
    st = dict(air=window(t, AIRt - 0.15, WIPE2 + 0.3, 0.25, 0.2), airp=eio(prog(t, AIRt - 0.15, 0.7)),
              skull=eout(prog(t, SKULL - 0.15, 0.4)), boneflow=eout(prog(t, SKULL, 0.4)), deep=eio(prog(t, DEEP - 0.1, 0.5)))
    c.saveLayerAlpha(None, int(255 * ga))
    draw_head(c, t, cx, 1110, z * (0.9 + 0.1 * ga), st)
    c.restore()
    # 2-ways badge
    ta = window(t, TWO - 0.1, AIRt + 0.2, 0.2, 0.2)
    if ta > 0:
        f = skia.Font(TF_BLACK, 150); s = "2"
        c.drawString(s, 830 - f.measureText(s) / 2, 860, f, paint(INK, ta))
    # 'in your head' = rich combined waveform card at the bottom
    ra = eback(prog(t, INHEAD - 0.15, 0.35)) * (1 - prog(t, WIPE2, 0.2))
    if ra > 0:
        c.save(); c.translate(495, 1370); c.scale(clamp(ra, 0, 1.2), clamp(ra, 0, 1.2))
        c.drawRoundRect(skia.Rect.MakeLTRB(-330, -70, 330, 70), 30, 30, paint("#000000", 0.12, blur=12))
        c.drawRoundRect(skia.Rect.MakeLTRB(-330, -70, 330, 70), 30, 30, paint("#ffffff"))
        waveform(c, 30, 0, 480, 110, t, BONE, 1.0, rich=1.0, n=34)
        waveform(c, 30, 0, 480, 70, t, AIR, 0.85, rich=0.5, n=34)
        f = skia.Font(TF_MONO, 22)
        c.drawString("IN YOUR", -310, -6, f, paint(INK, 0.7)); c.drawString("HEAD", -310, 22, f, paint(INK, 0.7))
        c.restore()
    pill(c, t, "TWO WAYS", 495, 560, PURP, TWO, AIRt - 0.05, light=True)
    pill(c, t, "THROUGH THE AIR", 495, 560, AIR, AIRt, SKULL - 0.05, light=True)
    pill(c, t, "THROUGH YOUR SKULL", 495, 560, BONE, SKULL, DEEP - 0.05, light=True)
    pill(c, t, "BONES = DEEP NOTES", 495, 560, BONE, DEEP, RICH - 0.05, light=True)
    pill(c, t, "RICHER", 495, 560, PURP, RICH, WIPE2 + 0.1, light=True)


def compare(c, t, y, label, rich, colr2, a, lab_col="#ffffff"):
    if a <= 0: return
    c.save(); c.translate(495, y); c.scale(a, a)
    c.drawRoundRect(skia.Rect.MakeLTRB(-360, -100, 360, 100), 30, 30, paint("#000000", 0.3, blur=14))
    c.drawRoundRect(skia.Rect.MakeLTRB(-360, -100, 360, 100), 30, 30, paint("#221e2a"))
    c.drawRoundRect(skia.Rect.MakeLTRB(-360, -100, 360, 100), 30, 30, paint(colr2, 0.8, stroke=3))
    if rich:
        waveform(c, 70, 0, 480, 160, t, BONE, 1.0, rich=1.0, n=34)
        waveform(c, 70, 0, 480, 100, t, AIR, 0.9, rich=0.5, n=34)
    else:
        waveform(c, 70, 0, 480, 80, t, AIR, 1.0, rich=0.2, n=34)
    f = skia.Font(TF_MONO, 22)
    for i, ln in enumerate(label.split("\n")):
        c.drawString(ln, -335, -6 + i * 28, f, paint(lab_col, 0.8))
    c.restore()


def scene_mic(c, t):
    bg(c, t)
    ma = eout(prog(t, WIPE2 + 0.05, 0.4)) * (1 - prog(t, THIN - 0.3, 0.3))
    if ma > 0:
        mic(c, 330, 1010, 1.4, ma)
        # air arrives at mic, bone route blocked
        for k in range(3):
            u = ((t * 1.0 + k / 3) % 1)
            x = lerp(900, 470, u)
            c.drawArc(skia.Rect.MakeXYWH(x - 60, 900 - 70, 120, 140), 130, 100, False, paint(AIR, ma * (1 - u * 0.6), stroke=7))
        ba = ma * eout(prog(t, MICAIR, 0.3))
        if ba > 0:
            c.save(); c.translate(720, 1230); c.scale(1.4 * ba, 1.4 * ba)
            c.drawRoundRect(skia.Rect.MakeLTRB(-150, -50, 150, 50), 25, 25, paint("#2a2232"))
            f = skia.Font(TF_MONO, 24)
            c.drawString("BONE", -60, 9, f, paint(BONE))
            c.drawLine(-120, -30, 120, 30, paint(RED, 1, stroke=8))
            c.restore()
    ca = eout(prog(t, THIN - 0.3, 0.4))
    if ca > 0:
        compare(c, t, 860, "IN YOUR\nHEAD", True, BONE, ca)
        compare(c, t, 1120, "RECORD-\nING", False, AIR, eout(prog(t, THIN - 0.1, 0.35)))
        la = eback(prog(t, ELSE2 - 0.1, 0.35))
        if la > 0:
            for k in range(3):
                listener(c, t, 260 + k * 235, 1390, 0.55 * clamp(la, 0, 1.2), clamp(la), hear=1.0, colr=AIR, seed=k)
    pill(c, t, "MIC = AIR ONLY", 495, 560, AIR, MIC + 0.2, THIN - 0.05, text_col=INK)
    pill(c, t, "THINNER", 495, 560, AIR, THIN, ELSE2 - 0.05, text_col=INK)
    pill(c, t, "WHAT EVERYONE HEARS", 495, 560, REC, ELSE2, WEIRD - 0.1)


def scene_used(c, t):
    bg(c, t)
    x, y, s = hook_pose(t)
    phone(c, t, x - 120, y, s * 0.85, 1.0, play=(3 * t / DUR) % 1)
    mood = "neutral" if t < USED + 0.2 else "smile"
    q = eback(prog(t, WEIRD - 0.1, 0.35))
    c.save(); c.translate(790, 820); c.scale(clamp(q, 0, 1.2), clamp(q, 0, 1.2))
    face(c, 0, 0, 120, mood, t, 1.0)
    c.restore()
    pill(c, t, "FEELS WEIRD", 495, 560, "#8a8f98", WEIRD, USED - 0.05)
    pill(c, t, "JUST NOT USED TO IT", 495, 560, GREEN, USED, SO + 0.3, text_col="#FFFFFF")


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_white(c, t); return
    if t < WEIRD - 0.25:
        scene_mic(c, t); return
    if t < SO - 0.05:
        scene_used(c, t)
        q = 1 - prog(t, WEIRD - 0.25, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_mic(c, t); c.restore()
        return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_used(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.022 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"recording": REC, "ew": REC, "not": "#8a8f98", "is": GREEN, "else": REC, "two": PURP, "air": AIR, "skull": BONE,
         "deep": BONE, "richer": PURP, "thinner": AIR, "used": GREEN}
CAPS = Captions(P, KWCOL, {"ew?", "is."}, DUR)


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
    wipe(c, t, WIPE1, WL, PURP, "#F4F2EE")
    wipe(c, t, WIPE2, WL, AIR, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("hit", EW), ("pop", NOT), ("hit", ITIS), ("pop", ELSE1), ("pop", ELSE1 + 0.12),
          ("pop", ELSE1 + 0.24), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", TWO), ("whoosh", AIRt - 0.1),
          ("riser", SKULL - 0.2), ("pop", DEEP), ("pop", INHEAD), ("pop", RICH), ("whoosh", WIPE2), ("pop", MICAIR),
          ("whoosh", THIN - 0.3), ("pop", THIN), ("pop", ELSE2), ("whoosh", WEIRD - 0.25), ("pop", USED), ("whoosh", SO - 0.05)]
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

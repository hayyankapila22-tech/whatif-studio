# HIW16 — "Why do your ears pop on a plane?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-21):
#  - Mayo Clinic "Airplane ear" (mayoclinic.org/diseases-conditions/airplane-ear/symptoms-causes/syc-20351701, 2025):
#    the eustachian tube is a narrow passage from the middle ear to the back of the nose/throat that evens out air
#    pressure; when pressure changes fast (climb or descent) it can't keep up, the eardrum can't move normally ->
#    fullness / blocked, muffled hearing. Tips: yawn, swallow, chew gum or suck candy, gentle Valsalva, don't sleep
#    during takeoff and landing; babies: bottle/pacifier. See a doctor if it lasts more than a few days or is severe.
#  - patient.info "Ears and flying" (2024): usually worse on descent/landing because air pressure is higher near the
#    ground; air pushed up the tube makes the ears "pop"; stay awake for the descent.
#  - Cabin altitude: US FAA rule 14 CFR 25.841 — cabin pressure altitude no higher than 8,000 ft (~2,400 m) in normal
#    operation, i.e. the cabin air "can be as thin as" on a ~2,400 m mountain.
#  On climb, outside pressure drops -> the higher-pressure air in the middle ear pushes the eardrum outward; on descent
#  the reverse (eardrum pushed in). Opening the tube lets air through -> pressures equal -> pop.
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
SKY = "#6EC3FF"; SKY_D = "#2B6FD6"; AIRC = "#3EA8FF"; DRUM = "#FF7A9A"; TUBE = "#FFB347"; GREEN = "#1fb98a"
SKIN = "#E7B08A"; SKIN_D = "#B97B57"; PURPLE = "#9B6BFF"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


WIPE1 = p0(1) - 0.3; AIR = kw(2)
MTN = p0(3); M2400 = kw(5)
DIAG2 = p0(6); THIN = kw(6); DRUMt = kw(7); DOWN = p0(8); OPP = kw(9); IN_ = kw(10); BLOCK = kw(11)
TUBEt = kw(12); THROAT = p0(13); OPENS = p0(14); RUSH = p0(15); POP = kw(16)
WIPE2 = p0(17) - 0.3; WORSE = kw(17); AWAKE = kw(18); YAWN = kw(19, 0); SWALLOW = kw(19, 1); GUM = kw(19, 2); SO = p0(20)
WL = 0.32
IMPACTS = [POP, OPP]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1):
    return math.sin(2 * math.pi * k * t / DUR)


def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#1a1d26"), col("#12141b"), col("#08090c")], [0, 0.55, 1])))
    c.drawCircle(800 + 30 * lw(t), 720, 520, paint(shader=radial(800, 720, 520, [col(SKY, 0.10), col(SKY, 0)])))
    c.drawCircle(220, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1450, 600, [col(TUBE, 0.06), col(TUBE, 0)])))


def burst(c, x, y, u, color, n=10, r0=90, r1=220, a=1.0):
    if u <= 0 or u >= 1: return
    for k in range(n):
        an = k * 2 * math.pi / n + 0.2
        ra = lerp(r0, r1, eout(u)); rb = lerp(r0, r1 * 0.7, eout(u))
        c.drawLine(x + math.cos(an) * rb, y + math.sin(an) * rb, x + math.cos(an) * ra, y + math.sin(an) * ra, paint(color, a * (1 - u), stroke=10))


def pop_word(c, x, y, txt, u, color, size=96):
    if u <= 0 or u >= 1: return
    s = eback(clamp(u * 3)) * (1 + 0.1 * u)
    a = 1 - prog(u, 0.7, 0.3)
    f = skia.Font(TF_BLACK, size)
    c.save(); c.translate(x, y); c.rotate(-8); c.scale(s, s)
    w = f.measureText(txt)
    c.drawString(txt, -w / 2 + 5, 6 + size * 0.35, f, paint("#000000", 0.5 * a))
    c.drawString(txt, -w / 2, size * 0.35, f, paint(color, a))
    c.restore()


def cloud(c, x, y, s, a):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx, dy, r in ((-70, 10, 55), (-10, -20, 75), (60, 5, 60), (0, 25, 60)):
        c.drawCircle(dx, dy, r, paint("#ffffff", a))
    c.restore()


# ---------------- hook: plane window ----------------
NPOP = 4


def window_view(c, t, x, y, w, h, a=1.0):
    r = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w / 2, y - h / 2, x + w / 2, y + h / 2), w / 2, w / 2)
    outer = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w / 2 - 50, y - h / 2 - 50, x + w / 2 + 50, y + h / 2 + 50), w / 2 + 50, w / 2 + 50)
    c.drawRRect(outer.makeOffset(0, 20) if hasattr(outer, "makeOffset") else outer, paint("#000000", 0.4 * a, blur=24))
    c.drawRRect(outer, paint(shader=linear((0, y - h / 2 - 50), (0, y + h / 2 + 50), [col("#E9E7E2", a), col("#C9C6BF", a)])))
    c.drawRRect(r, paint("#8d8a84", a, stroke=10))
    c.save(); c.clipRRect(r, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeLTRB(x - w, y - h, x + w, y + h), paint(shader=linear((0, y - h / 2), (0, y + h / 2), [col("#2B6FD6", a), col("#6EC3FF", a), col("#CDEBFF", a)])))
    for k in range(7):
        rr = random.Random(k)
        cy = y - h / 2 - 150 + ((rr.random() * (h + 300) + t * (h + 300) * 3 / DUR) % (h + 300))
        cloud(c, x + rr.uniform(-w / 2, w / 2), cy, rr.uniform(0.7, 1.3), 0.9 * a)
    # wing tip
    wp = skia.Path(); wp.moveTo(x - w / 2 - 10, y + h * 0.22); wp.lineTo(x + w * 0.2, y + h * 0.12); wp.lineTo(x + w * 0.24, y + h * 0.17); wp.lineTo(x - w / 2 - 10, y + h * 0.36); wp.close()
    c.drawPath(wp, paint(shader=linear((0, y + h * 0.1), (0, y + h * 0.36), [col("#F4F6F8", a), col("#AEB6C2", a)])))
    c.restore()
    c.drawRRect(r, paint("#ffffff", 0.18 * a, stroke=4))
    # glare
    c.drawLine(x - w * 0.25, y - h * 0.3, x - w * 0.05, y - h * 0.38, paint("#ffffff", 0.35 * a, stroke=16, blur=6))


def ear_icon(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-10, -120); p.cubicTo(90, -130, 120, -20, 70, 40); p.cubicTo(40, 80, 40, 120, -10, 130)
    p.cubicTo(-60, 135, -70, 90, -60, 60); p.cubicTo(-90, 20, -100, -110, -10, -120); p.close()
    c.drawPath(p, paint("#000000", 0.35 * a, blur=14))
    c.drawPath(p, paint(shader=radial(-20, -40, 180, [col("#F6CDAE", a), col(SKIN, a), col(SKIN_D, a)], [0, 0.6, 1])))
    q = skia.Path(); q.moveTo(-20, -70); q.cubicTo(50, -80, 60, 0, 20, 30); q.cubicTo(0, 50, 10, 70, -20, 80)
    c.drawPath(q, paint(SKIN_D, 0.9 * a, stroke=12))
    c.drawCircle(-10, 10, 18, paint("#5a3420", 0.8 * a))
    c.restore()


def scene_hook(c, t):
    bg_dark(c, t)
    window_view(c, t, 495, 960, 440, 600)
    ph = (t * NPOP / DUR) % 1
    u = (ph - 0.6) / 0.38
    ear_icon(c, 790, 1260, 0.95 + 0.04 * math.sin(math.pi * clamp(u)))
    for k in range(2):
        v = (ph * 2 + k * 0.5) % 1
        c.drawCircle(790, 1260, 140 + 90 * v, paint(SKY, 0.5 * (1 - v), stroke=5))
    burst(c, 790, 1260, u, YELLOW, 10, 150, 270)
    pop_word(c, 700, 1060, "POP!", u, YELLOW, 90)


def scene_open(c, t):
    scene_hook(c, t)
    pill(c, t, "WHY THE POP?", 495, 560, AIRC, 0.35, WIPE1 + 0.1)


# ---------------- white: the ear diagram ----------------
def drum_path(b):
    p = skia.Path(); p.moveTo(430, 790); p.quadTo(430 - 150 * b, 900, 430, 1010)
    return p


def bulge_at(t):
    out = eio(prog(t, DRUMt - 0.1, 0.5))
    inn = eio(prog(t, OPP - 0.05, 0.5))
    pop = eout(prog(t, POP - 0.05, 0.25))
    b = out - 2 * inn
    return lerp(b, 0, pop)


def outside_density(t):
    d = lerp(1.0, 0.3, eio(prog(t, THIN - 0.1, 0.6)))
    return lerp(d, 1.6, eio(prog(t, DOWN, 0.8)))


RD = random.Random(9)
OUT_DOTS = [(RD.uniform(70, 410), RD.uniform(840, 960), RD.random() * 6.28, RD.random()) for _ in range(40)]
IN_DOTS = [(RD.uniform(470, 740), RD.uniform(790, 1030), RD.random() * 6.28) for _ in range(26)]


def tube_pt(u):
    # eustachian tube centreline from the chamber to the throat (bottom right)
    x = lerp(690, 840, u) + 40 * math.sin(u * math.pi)
    y = lerp(1030, 1380, u)
    return x, y


def ear_diagram(c, t, a=1.0):
    # head skin block behind
    c.drawRoundRect(skia.Rect.MakeLTRB(20, 700, 1060, 2300), 60, 60, paint(shader=linear((0, 700), (0, 1600), [col("#F7D8C2", a), col("#EDBE9E", a)])))
    # ear canal
    canal = skia.Path(); canal.moveTo(-40, 820); canal.cubicTo(150, 830, 300, 830, 432, 830); canal.lineTo(432, 970); canal.cubicTo(300, 970, 150, 975, -40, 980); canal.close()
    c.drawPath(canal, paint(shader=linear((0, 820), (0, 980), [col("#F4E9E4", a), col("#E8D4CC", a)])))
    c.drawPath(canal, paint(SKIN_D, 0.6 * a, stroke=4))
    # middle ear chamber
    ch = skia.Path(); ch.moveTo(432, 780); ch.cubicTo(560, 720, 760, 740, 780, 880); ch.cubicTo(800, 1000, 740, 1070, 640, 1060)
    ch.cubicTo(520, 1060, 440, 1050, 432, 1020); ch.close()
    c.drawPath(ch, paint("#000000", 0.12 * a, blur=10))
    c.drawPath(ch, paint(shader=radial(600, 900, 260, [col("#FFF7F2", a), col("#F6E3DA", a)])))
    c.drawPath(ch, paint(SKIN_D, 0.6 * a, stroke=4))
    # tube to the throat
    tg = eout(prog(t, TUBEt - 0.1, 0.4))
    op = eout(prog(t, OPENS - 0.1, 0.4)) * (1 - prog(t, WIPE2, 0.3))
    tp = skia.Path()
    for i in range(21):
        x, y = tube_pt(i / 20)
        tp.moveTo(x, y) if i == 0 else tp.lineTo(x, y)
    c.drawPath(tp, paint(SKIN_D, 0.6 * a, stroke=46 + 22 * op))
    c.drawPath(tp, paint("#F6E3DA", a, stroke=36 + 22 * op))
    if tg > 0:
        c.drawPath(tp, paint(TUBE, 0.35 * tg * a * (0.7 + 0.3 * math.sin(t * 6)), stroke=60 + 22 * op, blur=10))
    if op < 0.2:   # closed: pinch line
        c.drawPath(tp, paint(SKIN_D, 0.7 * a, stroke=6))
    # outside air dots (canal)
    dens = outside_density(t)
    for i, (x, y, ph, r0) in enumerate(OUT_DOTS):
        vis = clamp((dens * 0.6 - r0) * 6 + 0.5) if dens < 1.6 else 1
        if i >= 26 and dens <= 1.0: vis = 0
        if i >= 26: vis = clamp((dens - 1.0) / 0.6) if dens > 1 else 0
        if vis <= 0: continue
        xx = x + 8 * math.sin(t * 2 + ph) - 60 * eio(prog(t, OPP - 0.05, 0.5)) * 0
        yy = y + 8 * math.cos(t * 2.3 + ph)
        c.drawCircle(xx, yy, 9, paint(AIRC, 0.85 * vis * a))
    # inside air dots
    ia = prog(t, AIR - 0.1, 0.4)
    for (x, y, ph) in IN_DOTS:
        xx = x + 10 * math.sin(t * 2 + ph); yy = y + 10 * math.cos(t * 1.7 + ph)
        c.drawCircle(xx, yy, 9, paint(AIRC, 0.85 * ia * a))
    # air rushing through the tube (after it opens)
    ra = window(t, RUSH - 0.2, POP + 0.6, 0.2, 0.4)
    if ra > 0:
        for k in range(10):
            u = ((t * 1.6 + k / 10) % 1)
            x, y = tube_pt(1 - u)
            c.drawCircle(x, y, 10, paint(AIRC, ra * a))
    # eardrum
    b = bulge_at(t)
    dp = drum_path(b)
    c.drawPath(dp, paint(DRUM, 0.35 * a, stroke=26, blur=6))
    c.drawPath(dp, paint(DRUM, a, stroke=10))
    # push arrows
    oa = window(t, DRUMt - 0.1, DOWN, 0.2, 0.2)
    ia2 = window(t, OPP - 0.1, OPENS, 0.2, 0.2)
    for aa, sx, x0 in ((oa, -1, 560), (ia2, 1, 300)):
        if aa <= 0: continue
        for k, y in enumerate((850, 900, 950)):
            w = 12 * math.sin(t * 9 + k)
            p = skia.Path(); p.moveTo(x0 + w, y); p.lineTo(x0 + sx * 70 + w, y)
            c.drawPath(p, paint(PURPLE if sx < 0 else RED, aa * a, stroke=10))
            h = skia.Path(); h.moveTo(x0 + sx * 100 + w, y); h.lineTo(x0 + sx * 66 + w, y - 22); h.lineTo(x0 + sx * 66 + w, y + 22); h.close()
            c.drawPath(h, paint(PURPLE if sx < 0 else RED, aa * a))
    # blocked: sound waves die at the drum
    ba = window(t, BLOCK - 0.1, TUBEt, 0.2, 0.2)
    if ba > 0:
        for k in range(3):
            u = ((t * 1.3 + k / 3) % 1)
            x = lerp(80, 400, u)
            c.drawArc(skia.Rect.MakeLTRB(x - 40, 840, x + 40, 960), -60, 120, False, paint(INK, 0.55 * ba * (1 - u) * a, stroke=6))
    f = skia.Font(TF_MONO, 24)
    la = a * prog(t, AIR, 0.3)
    for s, x, y, cc, tin in (("EARDRUM", 330, 765, DRUM, AIR), ("AIR POCKET", 545, 1110, AIRC, AIR), ("THROAT", 760, 1430, "#C07A2A", THROAT)):
        al = a * prog(t, tin, 0.3)
        if al > 0:
            c.drawString(s, x, y, f, paint(cc, al))


def mountain_card(c, t, a):
    if a <= 0: return
    r = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(90, 650, 900, 1400), 40, 40)
    c.drawRRect(r, paint("#000000", 0.15 * a, blur=18))
    c.save(); c.clipRRect(r, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeLTRB(90, 650, 900, 1400), paint(shader=linear((0, 650), (0, 1400), [col("#3D8BEA", a), col("#9FD6FF", a), col("#E8F5FF", a)])))
    for k in range(4):
        rr = random.Random(20 + k)
        cloud(c, ((rr.uniform(0, 900) - t * 40) % 1000) + 40, rr.uniform(700, 900), rr.uniform(0.5, 0.9), 0.85 * a)
    m = skia.Path(); m.moveTo(60, 1400); m.lineTo(330, 1000); m.lineTo(420, 1090); m.lineTo(560, 860); m.lineTo(920, 1400); m.close()
    c.drawPath(m, paint(shader=linear((0, 860), (0, 1400), [col("#6F7D96", a), col("#3F4A5E", a)])))
    sn = skia.Path(); sn.moveTo(560, 860); sn.lineTo(505, 950); sn.lineTo(535, 940); sn.lineTo(560, 965); sn.lineTo(590, 935); sn.lineTo(612, 945); sn.close()
    c.drawPath(sn, paint("#ffffff", a))
    px = 600 + 40 * math.sin(t * 1.2); py = 760 + 10 * math.sin(t * 2)
    c.save(); c.translate(px, py); c.rotate(-6)
    body = skia.Path(); body.addRoundRect(skia.Rect.MakeLTRB(-120, -18, 120, 18), 18, 18)
    c.drawPath(body, paint("#ffffff", a))
    wing = skia.Path(); wing.moveTo(-20, 0); wing.lineTo(30, 0); wing.lineTo(-30, 60); wing.lineTo(-60, 60); wing.close()
    c.drawPath(wing, paint("#D5DCE6", a))
    tail = skia.Path(); tail.moveTo(-120, -10); tail.lineTo(-100, -10); tail.lineTo(-130, -60); tail.lineTo(-145, -60); tail.close()
    c.drawPath(tail, paint("#D5DCE6", a))
    c.restore()
    c.restore()
    c.drawRRect(r, paint("#ffffff", 0.6 * a, stroke=4))
    na = eback(prog(t, M2400 - 0.1, 0.35))
    if na > 0:
        big_number(c, "2,400", "m", 470, 1300, 120, "#ffffff", clamp(na) * a, pulse=clamp(na, 0, 1.1))


def scene_white(c, t):
    studio_white(c)
    ga = eout(prog(t, WIPE1, 0.4))
    # camera: start zoomed on the drum, settle, then pan down to the tube for the fix
    z = lerp(1.25, 1.0, eio(prog(t, WIPE1, 1.0)))
    tz = eio(prog(t, TUBEt - 0.2, 0.7)) * (1 - eio(prog(t, POP - 0.1, 0.5)))
    z *= 1 + 0.06 * tz
    cy = lerp(960, 1040, tz)
    c.save(); c.translate(495, 960); c.scale(z, z); c.translate(-495, -cy + (960 - 960))
    c.translate(0, 0)
    ear_diagram(c, t, ga)
    burst(c, 430, 900, prog(t, POP, 0.45), YELLOW, 12, 120, 280)
    c.restore()
    ma = window(t, MTN - 0.25, DIAG2 - 0.1, 0.3, 0.3)
    if ma > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#F1EEE8", ma))
        s = lerp(0.9, 1.0, eout(prog(t, MTN - 0.25, 0.4)))
        c.save(); c.translate(495, 1020); c.scale(s, s); c.translate(-495, -1020)
        mountain_card(c, t, ma)
        c.restore()
    pop_word(c, 640, 760, "POP!", prog(t, POP, 0.9), "#E0A100", 110)
    pill(c, t, "AIR POCKET", 495, 560, AIRC, AIR, MTN - 0.05)
    pill(c, t, "CABIN AIR IS THIN", 495, 560, SKY_D, MTN, THIN - 0.05)
    pill(c, t, "THIN AIR OUTSIDE", 495, 560, SKY_D, THIN, DRUMt - 0.05)
    pill(c, t, "PUSHED OUT", 495, 560, PURPLE, DRUMt, DOWN - 0.05)
    pill(c, t, "COMING DOWN", 495, 560, "#8a8f98", DOWN, OPP - 0.05)
    pill(c, t, "SQUEEZED IN", 495, 560, RED, OPP, BLOCK - 0.05)
    pill(c, t, "BLOCKED", 495, 560, INK, BLOCK, TUBEt - 0.05)
    pill(c, t, "TINY TUBE", 495, 560, TUBE, TUBEt, OPENS - 0.05)
    pill(c, t, "IT OPENS", 495, 560, TUBE, OPENS, RUSH - 0.05)
    pill(c, t, "AIR RUSHES IN", 495, 560, AIRC, RUSH, POP - 0.05)
    pill(c, t, "PRESSURE EVENS OUT", 495, 560, GREEN, POP, WIPE2 + 0.1, text_col="#FFFFFF")


# ---------------- dark: tips ----------------
def tip_card(c, t, x, y, kind, a, wcard=250, hcard=290):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    rect = skia.Rect.MakeLTRB(-wcard / 2, -hcard / 2, wcard / 2, hcard / 2)
    c.drawRoundRect(rect, 30, 30, paint("#000000", 0.3, blur=14))
    c.drawRoundRect(rect, 30, 30, paint("#232631"))
    c.drawRoundRect(rect, 30, 30, paint("#ffffff", 0.14, stroke=2))
    f = skia.Font(TF_MONO, 26)
    if kind == "awake":
        op = 0.85 + 0.15 * math.sin(t * 3)
        e = skia.Path(); e.moveTo(-90, -10); e.cubicTo(-40, -70 * op, 40, -70 * op, 90, -10); e.cubicTo(40, 50 * op, -40, 50 * op, -90, -10); e.close()
        c.drawPath(e, paint("#ffffff"))
        c.drawCircle(8 * math.sin(t * 1.5), -10, 30, paint(SKY_D)); c.drawCircle(8 * math.sin(t * 1.5), -10, 13, paint(INK))
        c.drawCircle(8 * math.sin(t * 1.5) - 9, -20, 6, paint("#ffffff"))
        lab, cc = "STAY AWAKE", YELLOW
    elif kind == "yawn":
        c.drawCircle(0, -20, 80, paint("#FFC93C"))
        for sx in (-1, 1):
            c.drawLine(sx * 22, -45, sx * 48, -40, paint("#5a3410", 1, stroke=7))
        m = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(t * 2.5))
        c.drawOval(skia.Rect.MakeLTRB(-26, 0, 26, 0 + 56 * m), paint("#5a3410"))
        lab, cc = "YAWN", "#FFC93C"
    elif kind == "swallow":
        g = skia.Path(); g.moveTo(-50, -100); g.lineTo(50, -100); g.lineTo(38, 50); g.lineTo(-38, 50); g.close()
        c.drawPath(g, paint("#ffffff", 0.2)); c.drawPath(g, paint("#ffffff", 0.7, stroke=4))
        lvl = -40 + 30 * (0.5 + 0.5 * math.sin(t * 1.5))
        wpth = skia.Path(); wpth.moveTo(-46 + (lvl + 100) * 0.03, lvl); wpth.lineTo(46 - (lvl + 100) * 0.03, lvl); wpth.lineTo(38, 50); wpth.lineTo(-38, 50); wpth.close()
        c.drawPath(wpth, paint(AIRC, 0.9))
        lab, cc = "SWALLOW", AIRC
    else:
        s = 1 + 0.08 * math.sin(t * 5)
        c.save(); c.scale(s, 1 / s)
        c.drawRoundRect(skia.Rect.MakeLTRB(-70, -60, 70, 20), 22, 22, paint("#FF8FB8"))
        c.drawRoundRect(skia.Rect.MakeLTRB(-70, -60, 70, 20), 22, 22, paint("#ffffff", 0.5, stroke=3))
        c.restore()
        c.drawCircle(-30, -40, 10, paint("#ffffff", 0.5))
        lab, cc = "CHEW GUM", "#FF8FB8"
    c.drawString(lab, -f.measureText(lab) / 2, hcard / 2 - 34, f, paint(cc))
    c.restore()


def scene_tips(c, t):
    bg_dark(c, t)
    # landing plane (descending) on top
    la = eout(prog(t, WIPE2, 0.4)) * (1 - prog(t, AWAKE - 0.25, 0.3))
    if la > 0:
        u = ((t - WIPE2) * 0.25) % 1
        px = lerp(200, 800, u); py = lerp(760, 940, u)
        c.save(); c.translate(px, py); c.rotate(10); c.scale(1.3, 1.3)
        body = skia.Path(); body.addRoundRect(skia.Rect.MakeLTRB(-120, -18, 120, 18), 18, 18)
        c.drawPath(body, paint("#ffffff", la))
        wing = skia.Path(); wing.moveTo(-20, 0); wing.lineTo(30, 0); wing.lineTo(-30, 60); wing.lineTo(-60, 60); wing.close()
        c.drawPath(wing, paint("#AEB6C2", la))
        c.restore()
        c.drawLine(120, 1010, 900, 1010, paint("#ffffff", 0.25 * la, stroke=4))
    ca = eback(prog(t, AWAKE - 0.15, 0.35))
    tip_card(c, t, 495, 820, "awake", 1.05 * clamp(ca, 0, 1.2), 380, 280)
    for x, kind, tin in ((225, "yawn", YAWN), (495, "swallow", SWALLOW), (765, "gum", GUM)):
        q = eback(prog(t, tin - 0.15, 0.35))
        tip_card(c, t, x, 1220, kind, clamp(q, 0, 1.2))
        if q > 0.9:
            ck = eout(prog(t, tin + 0.25, 0.25))
            c.drawCircle(x + 110, 1220 - 140, 30, paint(GREEN, ck))
            p = skia.Path(); p.moveTo(x + 96, 1080); p.lineTo(x + 106, 1092); p.lineTo(x + 126, 1068)
            c.drawPath(p, paint("#ffffff", ck, stroke=7))
    pill(c, t, "LANDING = WORSE", 495, 560, RED, WORSE, AWAKE - 0.05)
    pill(c, t, "STAY AWAKE", 495, 560, "#C9A100", AWAKE, YAWN - 0.05, text_col="#FFFFFF")
    pill(c, t, "OPEN THE TUBE", 495, 560, GREEN, YAWN, SO + 0.3, text_col="#FFFFFF")


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_white(c, t); return
    if t < SO - 0.05:
        scene_tips(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    scene_hook(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_tips(c, t); c.restore()


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

KWCOL = {"pop": AIRC, "air": AIRC, "2,400": SKY_D, "metre": SKY_D, "thinner": SKY_D, "eardrum": DRUM, "opposite": RED,
         "in": RED, "blocked": "#8a8f98", "tube": TUBE, "worse": RED, "awake": YELLOW, "yawn": "#FFC93C",
         "swallow": AIRC, "gum": "#FF8FB8"}
CAPS = Captions(split_long(P), KWCOL, {"pop!", "opposite!"}, DUR)


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
    wipe(c, t, WIPE1, WL, AIRC, "#F4F2EE")
    wipe(c, t, WIPE2, WL, TUBE, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", AIR), ("whoosh", MTN - 0.25),
          ("pop", M2400), ("whoosh", DIAG2 - 0.1), ("pop", THIN), ("pop", DRUMt), ("whoosh", DOWN), ("hit", OPP),
          ("pop", BLOCK), ("whoosh", TUBEt - 0.2), ("pop", OPENS), ("riser", RUSH - 0.2), ("hit", POP), ("whoosh", WIPE2),
          ("pop", WORSE), ("pop", AWAKE), ("pop", YAWN), ("pop", SWALLOW), ("pop", GUM), ("whoosh", SO - 0.05)]
    for n in range(NPOP):
        tp = (n + 0.6 + 0.12) * DUR / NPOP
        if tp < WIPE1 - 0.1:
            ev.append(("pop", tp))
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

# HIW15 — "What actually happens when you crack your knuckles?" Bubbly Liam voice, no studies, "So," loop.
# Sources (fact-checked 2026-11-21):
#  - Harvard Health "Does knuckle cracking cause arthritis?" (health.harvard.edu/pain/does-knuckle-cracking-cause-arthritis):
#    pulling the bones apart creates negative pressure in the joint (synovial) fluid -> gas bubble -> the pop; cracking
#    "probably won't raise your risk for arthritis".
#  - Harvard Health blog, R. Shmerling 2018 "Knuckle cracking: annoying and harmful, or just annoying?": "probably
#    harmless"; it takes time for the gas to build up again before the same joint can crack again; where exactly the
#    noise comes from has been debated (so the video only says "a gas bubble ... that's the crack", not forming vs collapsing).
#  - Scientific American "What makes the sound when we crack our knuckles?" / HowStuffWorks: gas takes roughly 20-30
#    minutes to dissolve back into the fluid, which is why you can't re-crack straight away (video says "about 20 minutes").
#  - Pain or swelling with cracking is a reason to stop / get it checked (Harvard blog; Cedars-Sinai "Ask a Doc").
#  Owner rule: no studies on screen, plain words. Footnote: "Educational only, not medical advice."
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
SKIN = "#E7B08A"; SKIN_D = "#B97B57"; SKIN_L = "#F6CDAE"; BONE = "#F3EAD8"; BONE_D = "#CDBE9F"
FLUID = "#5EC8FF"; GASB = "#BFF4FF"; CAPSULE = "#FF8FA3"; ORANGE = "#FF9F43"; GREEN = "#1fb98a"; PURPLE = "#9B6BFF"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


RELAX = p0(1); BONES = kw(2)
WIPE1 = p0(3) - 0.3; FLUIDt = kw(3); APART = kw(4); DROPS = kw(5); GAS = kw(6); CRACK = kw(7)
WIPE2 = p0(8) - 0.3; AWAY = kw(8); MIN20 = kw(9)
ARTH = p0(10); NOPE = p0(11); HARMLESS = kw(12); HURTS = kw(13, 0); SWELLS = kw(13, 1); SO = p0(14)
WL = 0.32
IMPACTS = [CRACK, NOPE]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]


def lw(t, k=1):
    return math.sin(2 * math.pi * k * t / DUR)


# ---------------- parts ----------------
def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.5, 1300, [col("#1f1b22"), col("#141216"), col("#0a090b")], [0, 0.55, 1])))
    c.drawCircle(800 + 30 * lw(t), 760, 520, paint(shader=radial(800, 760, 520, [col(FLUID, 0.10), col(FLUID, 0)])))
    c.drawCircle(220, 1450 + 30 * lw(t, 2), 600, paint(shader=radial(220, 1450, 600, [col(ORANGE, 0.07), col(ORANGE, 0)])))


def seg(c, x0, y0, ang, length, thick, a, tip=False):
    """one finger segment from (x0,y0) pointing at angle ang (deg), skin shaded."""
    c.save(); c.translate(x0, y0); c.rotate(ang)
    r = skia.Rect.MakeLTRB(-thick * 0.45, -thick / 2, length + (thick * 0.5 if tip else 0), thick / 2)
    c.drawRoundRect(r.makeOffset(0, 14), thick / 2, thick / 2, paint("#000000", 0.35 * a, blur=16))
    c.drawRoundRect(r, thick / 2, thick / 2, paint(shader=linear((0, -thick / 2), (0, thick / 2), [col(SKIN_L, a), col(SKIN, a), col(SKIN_D, a)], [0, 0.45, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(r.left() + 20, -thick / 2 + 10, r.right() - 30, -thick / 2 + 26), 8, 8, paint("#ffffff", 0.18 * a, blur=4))
    if tip:
        nl = skia.Rect.MakeLTRB(length - 70, -thick / 2 + 8, length + thick * 0.38, -thick / 2 + 44)
        c.drawRoundRect(nl, 18, 18, paint(shader=linear((0, nl.top()), (0, nl.bottom()), [col("#FBE3D6", a), col("#E9B9A4", a)])))
        c.drawRoundRect(nl, 18, 18, paint("#C98F78", 0.7 * a, stroke=2.5))
    c.restore()


def finger(c, x, y, s, bend, a=1.0, glow=0.0, puff=0.0):
    """side view: hand back segment (fixed) + knuckle + two finger segments bending down by `bend` degrees."""
    c.save(); c.translate(x, y); c.scale(s, s)
    th = 150 * (1 + 0.15 * puff)
    seg(c, -420, 0, 0, 420, th + 20, a)                    # back of the hand
    a1 = bend
    seg(c, 0, 0, a1, 230, th, a)
    k2x = 230 * math.cos(math.radians(a1)); k2y = 230 * math.sin(math.radians(a1))
    seg(c, k2x, k2y, a1 + bend * 0.6, 190, th - 18, a, tip=True)
    # knuckle bump + creases
    c.drawCircle(0, -6, th * 0.52, paint(shader=radial(-10, -40, th * 0.6, [col(SKIN_L, a), col(SKIN, a), col(SKIN_D, a)], [0, 0.6, 1])))
    for k in range(3):
        an = math.radians(-100 + a1 / 2 + k * 12)
        r = th * 0.42
        c.drawLine(r * math.cos(an) - 6, r * math.sin(an), r * math.cos(an) + 10, r * math.sin(an) - 12, paint(SKIN_D, 0.7 * a, stroke=3))
    if glow > 0:
        c.drawCircle(0, 0, th * 0.9, paint("#FF3B30", 0.45 * glow * (0.7 + 0.3 * math.sin(14 * 0.5)), blur=30))
    c.restore()


def burst(c, x, y, u, color, n=10, r0=90, r1=220, a=1.0):
    if u <= 0 or u >= 1: return
    for k in range(n):
        an = k * 2 * math.pi / n + 0.2
        ra = lerp(r0, r1, eout(u)); rb = lerp(r0, r1 * 0.7, eout(u))
        c.drawLine(x + math.cos(an) * rb, y + math.sin(an) * rb, x + math.cos(an) * ra, y + math.sin(an) * ra,
                   paint(color, a * (1 - u), stroke=10))


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


# ---------------- hook ----------------
NPOP = 5      # pops per video (periodic in DUR -> perfect loop)


def bend_at(t):
    ph = (t * NPOP / DUR) % 1
    if ph < 0.55:
        return lerp(8, 62, eio(ph / 0.55))
    return lerp(62, 8, eout((ph - 0.55) / 0.45))


def pop_phase(t):
    ph = (t * NPOP / DUR) % 1
    return (ph - 0.5) / 0.4      # 0..1 right at full bend


def scene_hook(c, t):
    bg_dark(c, t)
    zoom = 1.05 + 0.03 * lw(t, 2)
    c.save(); c.translate(495, 900); c.scale(zoom, zoom); c.translate(-495, -900)
    finger(c, 400, 900, 1.0, bend_at(t))
    u = pop_phase(t)
    burst(c, 400, 900, u, YELLOW, 10, 120, 260)
    pop_word(c, 620, 700, "POP!", u, YELLOW)
    c.restore()


def bone_icon(c, x, y, s, a, crack=0.0):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-20)
    p = skia.Path()
    p.addRoundRect(skia.Rect.MakeLTRB(-200, -40, 200, 40), 30, 30)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.addCircle(sx * 205, sy * 46, 58)
    c.drawPath(p, paint("#000000", 0.4 * a, blur=16))
    c.drawPath(p, paint(shader=linear((0, -110), (0, 110), [col("#FFFDF6", a), col(BONE, a), col(BONE_D, a)])))
    if crack > 0:
        q = skia.Path(); q.moveTo(-10, -42); q.lineTo(14, -12); q.lineTo(-12, 6); q.lineTo(16, 42)
        pp = paint("#3a2a1a", a, stroke=7)
        te = skia.TrimPathEffect.Make(0, crack)
        if te is not None and crack < 0.999: pp.setPathEffect(te)
        c.drawPath(q, pp)
    c.restore()


def scene_open(c, t):
    scene_hook(c, t)
    pill(c, t, "WHAT'S THAT CRACK?", 495, 560, ORANGE, 0.35, RELAX - 0.05)
    sa = window(t, RELAX - 0.1, WIPE1 + 0.2, 0.2, 0.2)
    if sa > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 0.6 * sa))
        s = eback(prog(t, RELAX - 0.1, 0.35)) * (1 + 0.02 * math.sin(t * 3))
        bone_icon(c, 495, 960, 1.15 * s, sa, crack=eout(prog(t, RELAX + 0.1, 0.35)))
        x = eout(prog(t, BONES + 0.15, 0.25))
        if x > 0:
            for d in (1, -1):
                c.drawLine(495 - 230 * d, 740, lerp(495 - 230 * d, 495 + 230 * d, x), lerp(740, 1180, x), paint(RED, sa, stroke=24))
    pill(c, t, "NOT BROKEN BONES", 495, 560, RED, BONES, WIPE1 + 0.1)


# ---------------- white: inside the joint ----------------
JX, JY = 495, 960


def gap_at(t):
    return lerp(30, 170, eio(prog(t, APART - 0.1, 0.6)))


def joint(c, t, gap, bub, crackflash, a=1.0, dark=False):
    # capsule (the little bag) around the joint, fluid inside
    cw = 250 + gap * 0.6; ch = 250
    cap = skia.Rect.MakeLTRB(JX - cw, JY - ch, JX + cw, JY + ch)
    c.drawOval(cap.makeOffset(0, 18), paint("#000000", 0.18 * a, blur=22))
    c.drawOval(cap, paint(shader=radial(JX, JY - 40, cw * 1.1, [col("#DDF4FF", 0.95 * a), col(FLUID, 0.55 * a)], [0, 1])))
    # fluid shimmer
    for k in range(12):
        rr = random.Random(k)
        px = JX + rr.uniform(-cw * 0.75, cw * 0.75); py = JY + rr.uniform(-ch * 0.7, ch * 0.7) + 14 * math.sin(t * 2 + k)
        c.drawCircle(px, py, rr.uniform(4, 9), paint("#ffffff", 0.45 * a))
    # bones: long shaft + rounded head with a smooth cartilage cap
    for sx in (-1, 1):
        ex = JX + sx * gap / 2
        c.save(); c.translate(ex, JY); c.scale(-sx, 1)
        shaft = skia.Rect.MakeLTRB(-760, -78, -120, 78)
        head = skia.Rect.MakeLTRB(-230, -150, 0, 150)
        sh = skia.Path(); sh.addRect(shaft); sh.addOval(head)
        c.drawPath(sh, paint("#000000", 0.25 * a, blur=14))
        bs = linear((0, -150), (0, 150), [col("#FFFDF6", a), col(BONE, a), col(BONE_D, a)])
        c.drawRect(shaft, paint(shader=bs))
        c.drawOval(head, paint(shader=radial(-130, -60, 220, [col("#FFFDF6", a), col(BONE, a), col(BONE_D, a)], [0, 0.6, 1])))
        c.drawArc(head.makeInset(6, 6), -70, 140, False, paint("#BFE7FF", 0.95 * a, stroke=14))
        c.drawLine(-700, -40, -300, -40, paint("#ffffff", 0.35 * a, stroke=8, blur=3))
        c.restore()
    # capsule wall on top
    c.drawOval(cap, paint(CAPSULE, 0.95 * a, stroke=9))
    c.drawOval(cap.makeInset(-10, -10), paint(CAPSULE, 0.25 * a, stroke=6))
    # gas bubble
    if bub > 0:
        r = 70 * bub
        c.drawCircle(JX, JY, r + 6, paint(FLUID, 0.5 * a, blur=6))
        c.drawCircle(JX, JY, r, paint(shader=radial(JX - r * 0.3, JY - r * 0.3, r * 1.2, [col("#ffffff", a), col(GASB, a), col("#7FD6F5", a)], [0, 0.5, 1])))
        c.drawCircle(JX - r * 0.35, JY - r * 0.35, r * 0.22, paint("#ffffff", 0.9 * a))
        c.drawCircle(JX, JY, r, paint("#2A9ED6", 0.8 * a, stroke=3))
    if crackflash > 0:
        c.drawCircle(JX, JY, 300, paint("#ffffff", 0.7 * crackflash * a, blur=40))


def gauge(c, t, x, y, val, a):
    """val 1 = normal pressure, 0 = low"""
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(a, a)
    c.drawRoundRect(skia.Rect.MakeLTRB(-170, -130, 170, 70), 30, 30, paint("#000000", 0.18, blur=16))
    c.drawRoundRect(skia.Rect.MakeLTRB(-170, -130, 170, 70), 30, 30, paint("#ffffff"))
    c.drawRoundRect(skia.Rect.MakeLTRB(-170, -130, 170, 70), 30, 30, paint(INK, 0.12, stroke=2))
    arc = skia.Rect.MakeLTRB(-120, -100, 120, 140)
    c.drawArc(arc, 200, 140, False, paint("#E4E1DB", 1, stroke=18))
    c.drawArc(arc, 200, 140 * val, False, paint(mixhex(PURPLE, FLUID, 1 - val), 1, stroke=18))
    an = math.radians(200 + 140 * val)
    c.drawLine(0, 20, 95 * math.cos(an), 20 + 95 * math.sin(an), paint(INK, 1, stroke=7))
    c.drawCircle(0, 20, 12, paint(INK))
    f = skia.Font(TF_MONO, 22); s = "PRESSURE"
    c.drawString(s, -f.measureText(s) / 2, 58, f, paint(INK, 0.6))
    c.restore()


def pull_arrows(c, t, a):
    if a <= 0: return
    w = 10 * math.sin(t * 8)
    for sx in (-1, 1):
        x = JX + sx * (380 + w)
        p = skia.Path(); p.moveTo(x, JY - 380); p.lineTo(x + sx * 90, JY - 380)
        c.drawPath(p, paint(ORANGE, a, stroke=14))
        h = skia.Path(); h.moveTo(x + sx * 120, JY - 380); h.lineTo(x + sx * 80, JY - 410); h.lineTo(x + sx * 80, JY - 350); h.close()
        c.drawPath(h, paint(ORANGE, a))


def scene_joint(c, t):
    studio_white(c)
    ga = eout(prog(t, WIPE1, 0.4))
    zoom = 1.12 * lerp(1.2, 1.0, eio(prog(t, WIPE1, 1.0))) * (1 + 0.05 * prog(t, GAS - 0.2, 1.2))
    c.save(); c.translate(JX, JY); c.scale(zoom, zoom); c.translate(-JX, -JY)
    bub = eback(prog(t, GAS - 0.1, 0.35)) * (1 + 0.04 * math.sin(t * 7))
    fl = 1 - prog(t, CRACK, 0.35) if t >= CRACK else 0
    joint(c, t, gap_at(t), bub, fl, ga)
    burst(c, JX, JY, prog(t, CRACK, 0.45), ORANGE, 12, 110, 300)
    c.restore()
    pull_arrows(c, t, window(t, APART - 0.1, GAS + 0.3, 0.2, 0.3))
    gauge(c, t, JX, 1365, lerp(1, 0.12, eio(prog(t, DROPS - 0.05, 0.5))), eback(prog(t, DROPS - 0.25, 0.3)) * (1 - prog(t, CRACK + 0.6, 0.3)))
    pop_word(c, 700, 700, "CRACK!", prog(t, CRACK, 0.9), ORANGE, 110)
    pill(c, t, "TINY BAG OF FLUID", 495, 560, "#2A9ED6", FLUIDt, APART - 0.05)
    pill(c, t, "PULL APART", 495, 560, ORANGE, APART, DROPS - 0.05)
    pill(c, t, "PRESSURE DROPS", 495, 560, PURPLE, DROPS, GAS - 0.05)
    pill(c, t, "GAS BUBBLE!", 495, 560, "#2A9ED6", GAS, CRACK - 0.05)


# ---------------- dark: 20 minutes ----------------
def scene_wait(c, t):
    bg_dark(c, t)
    a = eout(prog(t, WIPE2, 0.4))
    # small joint with shrinking bubble on the left/top, clock ring around
    fill = eio(prog(t, MIN20 - 0.1, 1.8))
    s = 0.62
    c.save(); c.translate(495, 980); c.scale(s, s); c.translate(-JX, -JY)
    joint(c, t, 90, (1 - fill) * (1 + 0.04 * math.sin(t * 7)), 0, a, dark=True)
    c.restore()
    R = 320
    rc = skia.Rect.MakeLTRB(495 - R, 980 - R, 495 + R, 980 + R)
    c.drawOval(rc, paint("#ffffff", 0.12 * a, stroke=22))
    if fill > 0:
        c.drawArc(rc, -90, 360 * fill, False, paint(FLUID, a, stroke=22))
        an = math.radians(-90 + 360 * fill)
        c.drawCircle(495 + R * math.cos(an), 980 + R * math.sin(an), 18, paint("#ffffff", a))
    for k in range(12):
        an = math.radians(k * 30)
        c.drawLine(495 + (R - 46) * math.cos(an), 980 + (R - 46) * math.sin(an), 495 + (R - 30) * math.cos(an), 980 + (R - 30) * math.sin(an), paint("#ffffff", 0.4 * a, stroke=4))
    # "can't do it again right away": locked badge before the timer
    la = window(t, AWAY - 0.2, MIN20 - 0.05, 0.2, 0.2)
    if la > 0:
        sh = 12 * math.sin(t * 40) * window(t, AWAY, AWAY + 0.5, 0.05, 0.2)
        c.save(); c.translate(495 + sh, 1385); c.scale(eback(prog(t, AWAY - 0.2, 0.3)), 1)
        c.drawRoundRect(skia.Rect.MakeLTRB(-60, -30, 60, 50), 14, 14, paint(RED, la))
        c.drawArc(skia.Rect.MakeLTRB(-40, -80, 40, 10), 180, 180, False, paint(RED, la, stroke=14))
        c.drawCircle(0, 10, 10, paint("#ffffff", la))
        c.restore()
    na = eback(prog(t, MIN20 - 0.1, 0.35))
    if na > 0:
        big_number(c, "20", "MIN", 495, 1440 - 30, 120, "#ffffff", clamp(na), pulse=clamp(na, 0, 1.1))
    # dissolving gas dots drifting out into the fluid
    if fill > 0:
        for k in range(14):
            rr = random.Random(30 + k)
            an = rr.uniform(0, 6.28); d = 40 + 170 * ((fill + rr.random()) % 1)
            c.drawCircle(495 + math.cos(an) * d, 980 + math.sin(an) * d * 0.9, rr.uniform(4, 8), paint(GASB, 0.7 * a * (1 - fill * 0.5)))
    pill(c, t, "NOT RIGHT AWAY", 495, 560, RED, AWAY, MIN20 - 0.05)
    pill(c, t, "GAS SINKS BACK IN", 495, 560, "#2A9ED6", MIN20, ARTH - 0.1)


# ---------------- arthritis? / harmless ----------------
def hand_xray(c, t, x, y, s, a, tint):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-230, -300, 230, 300), 30, 30, paint("#000000", 0.4 * a, blur=18))
    c.drawRoundRect(skia.Rect.MakeLTRB(-230, -300, 230, 300), 30, 30, paint("#0f1a24", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-230, -300, 230, 300), 30, 30, paint(tint, 0.9 * a, stroke=4))
    bp = paint("#D9F1FF", 0.85 * a, stroke=26)
    for i, (dx, ln) in enumerate(((-120, 190), (-45, 240), (30, 250), (105, 210))):
        y0 = 120
        segs = [ln * 0.42, ln * 0.33, ln * 0.25]
        yy = y0 - 40
        for k, L in enumerate(segs):
            c.drawLine(dx, yy, dx, yy - L + 22, bp)
            c.drawCircle(dx, yy - L + 6, 15, paint("#ffffff", 0.9 * a))
            yy -= L
    for dx, bx in ((-120, -70), (-45, -25), (30, 20), (105, 65)):
        c.drawLine(dx, 70, bx, 220, paint("#D9F1FF", 0.8 * a, stroke=24))
        c.drawCircle(dx, 82, 15, paint("#ffffff", 0.9 * a))
    c.drawLine(-95, 210, -175, 110, bp); c.drawCircle(-175, 105, 15, paint("#ffffff", 0.9 * a))
    c.drawLine(-178, 92, -200, 10, bp)
    c.drawOval(skia.Rect.MakeLTRB(-110, 210, 110, 280), paint("#D9F1FF", 0.5 * a))
    c.restore()


def scene_myth(c, t):
    bg_dark(c, t)
    a = eout(prog(t, ARTH - 0.25, 0.35))
    shake = 8 * math.sin(t * 30) * window(t, NOPE, NOPE + 0.35, 0.02, 0.15)
    tint = mixhex("#ffffff", GREEN, prog(t, HARMLESS - 0.1, 0.3))
    hand_xray(c, t, 495 + shake, 960, 1.05 + 0.02 * math.sin(t * 2), a, tint)
    qa = window(t, ARTH, NOPE + 0.05, 0.2, 0.15)
    if qa > 0:
        f = skia.Font(TF_BLACK, 220); s = "?"
        c.drawString(s, 690 - f.measureText(s) / 2, 820 + 10 * math.sin(t * 4), f, paint(ORANGE, qa))
    ca = eback(prog(t, HARMLESS, 0.35))
    if ca > 0:
        c.save(); c.translate(700, 760); c.scale(ca, ca)
        c.drawCircle(0, 0, 80, paint(GREEN))
        p = skia.Path(); p.moveTo(-36, 0); p.lineTo(-8, 28); p.lineTo(40, -26)
        c.drawPath(p, paint("#ffffff", 1, stroke=16))
        c.restore()
    pop_word(c, 300, 760, "NOPE!", prog(t, NOPE, 0.9), RED, 100)
    pill(c, t, "ARTHRITIS?", 495, 560, ORANGE, ARTH, NOPE - 0.05)
    pill(c, t, "PROBABLY HARMLESS", 495, 560, GREEN, HARMLESS, p0(13) - 0.1, text_col="#FFFFFF")


def scene_warn(c, t):
    bg_dark(c, t)
    for i, (x, kind, tin) in enumerate(((270, "hurts", HURTS), (720, "swells", SWELLS))):
        q = eback(prog(t, p0(13) - 0.2 + 0.2 * i, 0.35))
        hl = eout(prog(t, tin - 0.1, 0.3))
        if q <= 0: continue
        c.save(); c.translate(x, 980); c.scale(1.05 * q, 1.05 * q)
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -300, 200, 300), 34, 34, paint("#000000", 0.3, blur=18))
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -300, 200, 300), 34, 34, paint("#221e24"))
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -300, 200, 300), 34, 34, paint(RED if i == 0 else ORANGE, 0.9, stroke=4))
        g = 0.5 + 0.5 * math.sin(t * 7)
        c.save(); c.clipRect(skia.Rect.MakeLTRB(-196, -296, 196, 296))
        finger(c, 30, 40, 0.48, 25 + 4 * math.sin(t * 2), 1.0, glow=g * hl if i == 0 else 0, puff=(0.35 + 0.1 * g) * hl if i else 0)
        c.restore()
        if i == 0:
            for k in range(3):
                u = ((t * 1.2 + k / 3) % 1)
                c.drawCircle(30, 40, 60 + 110 * u, paint(RED, 0.6 * (1 - u) * hl, stroke=5))
        f = skia.Font(TF_MONO, 30); lab = "HURTS?" if i == 0 else "SWELLS?"
        c.drawString(lab, -f.measureText(lab) / 2, -230, f, paint("#ffffff", 0.9))
        c.restore()
    pill(c, t, "THEN STOP", 495, 560, RED, HURTS, SO + 0.3)
    footnote(c, t, "Educational only, not medical advice.", p0(13), SO + 0.4)


def draw_world(c, t):
    if t < WIPE1 + WL / 2:
        scene_open(c, t); return
    if t < WIPE2 + WL / 2:
        scene_joint(c, t); return
    if t < ARTH - 0.25:
        scene_wait(c, t); return
    if t < p0(13) - 0.25:
        scene_myth(c, t)
        q = 1 - prog(t, ARTH - 0.25, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_wait(c, t); c.restore()
        return
    if t < SO - 0.05:
        scene_warn(c, t)
        q = 1 - prog(t, p0(13) - 0.25, 0.3)
        if q > 0:
            c.saveLayerAlpha(None, int(255 * q)); scene_myth(c, t); c.restore()
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


KWCOL = {"knuckles": ORANGE, "bones": RED, "fluid": "#2A9ED6", "apart": ORANGE, "drops": PURPLE, "gas": "#2A9ED6",
         "bubble": "#2A9ED6", "crack": ORANGE, "right": RED, "away": RED, "20": FLUID, "minutes": FLUID,
         "arthritis": ORANGE, "harmless": GREEN, "hurts": RED, "swells": ORANGE}
CAPS = Captions(P, KWCOL, {"crack!", "Nope!"}, DUR)


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
    wipe(c, t, WIPE1, WL, ORANGE, "#F4F2EE")
    wipe(c, t, WIPE2, WL, FLUID, "#141313")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", 0.4), ("pop", RELAX), ("hit", BONES + 0.15), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12),
          ("pop", FLUIDt), ("whoosh", APART - 0.1), ("riser", DROPS - 0.1), ("pop", GAS), ("hit", CRACK), ("whoosh", WIPE2),
          ("pop", AWAY), ("pop", MIN20), ("whoosh", ARTH - 0.25), ("pop", ARTH), ("hit", NOPE), ("pop", HARMLESS),
          ("whoosh", p0(13) - 0.25), ("pop", HURTS), ("pop", SWELLS), ("whoosh", SO - 0.05)]
    for k in range(5):
        ev.append(("tick", MIN20 + 0.1 + k * 0.3))
    # hook pops (finger cracks) in the opening seconds
    for n in range(NPOP):
        tp = (n + 0.5) * DUR / NPOP
        if tp < RELAX - 0.1:
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

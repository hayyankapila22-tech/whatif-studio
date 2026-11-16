import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import numpy as np
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
TONE = os.environ.get("TONE", "#D7A47E")
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)


def p0(i):
    return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


# ---------------- beats ----------------
DIRT = kw(1)
DIVE = p0(2) - 0.35
TUBE_T = kw(2); OIL = kw(3)
SQ_IN = p0(4) - 0.35            # to 1 cm² macro
N900 = kw(4)
BLK2 = p0(6) - 0.35             # back into the block
SEBUM = kw(6); SOFT = kw(7)
CELLS = kw(8)
TOGETHER = kw(10)
STICKY = kw(12)
CLUMP = p0(13); PLUG = kw(14)
SPLIT = p0(15) - 0.1
WHITEHEAD = kw(16)
OPEN = kw(17)
DARKEN = kw(19)
APPLE = p0(20) - 0.15
BLACKHEAD_T = p0(21) - 0.3
WIPE1 = p0(22) - 0.3
SQUEEZE = kw(23)
NOTEX = kw(25)
TEAR = p0(26); DEEPER = kw(27)
SALIC = kw(28); DISSOLVE = p0(29)
RETIN = kw(30)
WEEKS = kw(32)
WIPE2 = p0(33) - 0.3
TWIST = kw(33)
VS = p0(34) - 0.2
FILA = kw(36); NORMAL = kw(37)
LOOP = p0(38) - 0.3
WL = 0.32
IMPACTS = [PLUG, NOTEX]


def mode_at(t):
    if t < DIVE + 0.45: return "macro1"
    if t < SQ_IN + 0.4: return "blockA"
    if t < BLK2 + 0.4: return "macro900"
    if t < BLACKHEAD_T + 0.4: return "blockB"
    if t < WIPE1 + WL / 2: return "macroBH"
    if t < WIPE2 + WL / 2: return "white"
    if t < VS + 0.4: return "macroGrid"
    if t < LOOP + 0.45: return "vs"
    return "macroEnd"


def light_at(t):
    return mode_at(t) == "white"


# ---------------- assets ----------------
SKIN = skia.Image.open(f"{D}/skin_{TONE[1:]}.png")
PORES = json.load(open(f"{D}/pores.json"))
TEXW, TEXH = 1400, 2400
TONE_DARK = mixhex(TONE, "#3a2418", 0.35)
TONE_LIGHT = mixhex(TONE, "#ffffff", 0.25)
rnd = random.Random(11)
DROPS = [(rnd.random(), rnd.uniform(-0.8, 0.8), rnd.uniform(5, 11), rnd.random() * 6.28) for _ in range(26)]
FLAKES = [(rnd.random(), rnd.choice((-1, 1)), rnd.uniform(10, 20), rnd.random() * 6.28, rnd.uniform(-40, 40)) for _ in range(22)]
O2 = [(rnd.uniform(-160, 160), rnd.uniform(0, 1), rnd.random() * 6.28) for _ in range(14)]
CHUNKS = [(rnd.uniform(-22, 22), rnd.uniform(0, 160), rnd.uniform(9, 18), rnd.uniform(-1, 1)) for _ in range(16)]


# ---------------- macro skin surface ----------------
HERO = (540, 1000)


def macro(c, t, push, hero=True, box=1.0, grid=0.0, extra=None):
    c.save()
    c.translate(HERO[0], HERO[1]); c.scale(push, push); c.translate(-HERO[0], -HERO[1])
    ox, oy = -160, -240
    c.drawImage(SKIN, ox, oy, SAMP)
    # light: soft key top-left, falloff
    c.drawRect(skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), paint(shader=radial(250, 500, 1500, [col("#ffffff", 0.16), col("#ffffff", 0), col("#000000", 0.35)], [0, 0.45, 1])))
    if grid > 0:
        for (px, py) in PORES:
            x, y = px + ox, py + oy
            if -50 < x < W + 50 and -50 < y < H + 50:
                c.drawCircle(x, y, 6.5, paint("#5c514a", 0.75 * grid, blur=1.4))
                c.drawCircle(x - 1.5, y - 1.5, 2.2, paint("#b9aa98", 0.5 * grid))
    if hero:
        hx, hy = HERO
        c.drawCircle(hx + 3, hy + 5, 30, paint("#000000", 0.25, blur=8))
        c.drawCircle(hx, hy, 28, paint(shader=radial(hx - 6, hy - 6, 34, [col(TONE_LIGHT), col(TONE), col(TONE_DARK)], [0, 0.6, 1])))
        c.drawCircle(hx, hy, 15, paint(shader=radial(hx - 3, hy - 3, 16, [col("#3a2a20"), col("#1a120e"), col("#0d0907")], [0, 0.6, 1])))
        c.drawCircle(hx - 5, hy - 6, 3.2, paint("#ffffff", 0.35, blur=1))
    if extra:
        extra(c)
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 760), paint(shader=linear((0, 0), (0, 760), [col("#000000", 0.55), col("#000000", 0)])))
    if hero and box > 0:
        # selection box in screen space around dot
        r = 46 * push / 1.25
        hx, hy = HERO
        rect = skia.Rect.MakeLTRB(hx - r, hy - r, hx + r, hy + r)
        pp = paint("#FFFFFF", box, stroke=2.5)
        c.drawRect(rect, paint("#FFFFFF", 0.08 * box))
        c.drawPath(skia.Path().addRect(rect), pp)
        for qx, qy in ((rect.left(), rect.top()), (rect.right(), rect.top()), (rect.left(), rect.bottom()), (rect.right(), rect.bottom())):
            c.drawCircle(qx, qy, 7, paint("#FFFFFF", box)); c.drawCircle(qx, qy, 7, paint("#7aa2ff", box, stroke=2))


def fingertip(c, x, y, ang, w, L, a=1.0):
    c.save(); c.translate(x, y); c.rotate(ang)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, 0, w, L), w / 2, w / 2)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 14, 22, w, L), w / 2, w / 2), paint("#000000", 0.35 * a, blur=22))
    c.drawRRect(rr, paint(shader=linear((-w / 2, 0), (w / 2, 0), [col(TONE_DARK, a), col(TONE_LIGHT, a), col(TONE, a), col(TONE_DARK, a)], [0, 0.35, 0.7, 1])))
    c.drawRRect(rr, paint(shader=linear((0, 0), (0, L * 0.6), [col("#ffffff", 0.0), col("#000000", 0.0), col("#000000", 0.25 * a)], [0, 0.5, 1])))
    c.save(); c.clipRRect(rr)
    for k in range(9):
        r = 40 + k * 18
        c.drawArc(skia.Rect.MakeLTRB(-r * 0.8, w * 0.55 - r * 0.6, r * 0.8, w * 0.55 + r * 0.6), 190, 160, False, paint(TONE_DARK, 0.28 * a, stroke=2))
    c.restore()
    c.restore()


def ruler_square(c, t, a):
    s = 360; x0, y0 = 540 - s / 2, 1000 - s / 2
    sp = eout(prog(t, SQ_IN + 0.2, 0.5))
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, s, s), paint("#000000", 0.25 * a * sp))
    pr = skia.Path(); pr.addRect(skia.Rect.MakeXYWH(x0, y0, s, s))
    pp = paint("#FFFFFF", 0.95 * a, stroke=3)
    if sp < 0.999:
        te = skia.TrimPathEffect.Make(0, sp)
        if te: pp.setPathEffect(te)
    c.drawPath(pr, pp)
    for k in range(11):
        L = 16 if k % 5 == 0 else 9
        c.drawLine(x0 + k * s / 10, y0, x0 + k * s / 10, y0 - L * sp, paint("#FFFFFF", 0.8 * a, stroke=2))
        c.drawLine(x0, y0 + k * s / 10, x0 - L * sp, y0 + k * s / 10, paint("#FFFFFF", 0.8 * a, stroke=2))
    f = skia.Font(TF_MONO, 24)
    c.drawString("1 cm", x0 + s - 62, y0 - 26, f, paint("#FFFFFF", a * sp))
    # 900 dots wave
    for i in range(30):
        for j in range(30):
            d = (i + j) / 58
            q = eback(prog(t, N900 + d * 1.1, 0.25))
            if q <= 0:
                continue
            x = x0 + 6 + i * 11.6 + 2; y = y0 + 6 + j * 11.6 + 2
            c.drawCircle(x, y, 3.4 * q, paint(YELLOW, 0.95 * a))


# ---------------- the skin block ----------------
FW, TOPY, BOTY = 400, -260, 360        # front face half-width, surface y, bottom y
DX, DY = 70, -120                       # depth offset
EPI, DERM = -215, 200                   # layer boundaries
TUBE_W = 34


def tube_path(depth_extra=0):
    p = skia.Path()
    p.moveTo(-TUBE_W - 8, TOPY - 2)
    p.cubicTo(-TUBE_W, TOPY + 40, -TUBE_W - 6, 40, -TUBE_W - 4, 100)
    p.cubicTo(-TUBE_W - 4, 150, TUBE_W + 4, 150, TUBE_W + 4, 100)
    p.cubicTo(TUBE_W + 6, 40, TUBE_W, TOPY + 40, TUBE_W + 8, TOPY - 2)
    p.close()
    return p


TUBE = tube_path()


def gland(c, t, glow):
    br = 1 + 0.012 * math.sin(t * 2.2)
    for sx in (-1, 1):
        c.save(); c.translate(sx * (TUBE_W + 46), 70); c.scale(br, br)
        if glow > 0:
            c.drawCircle(0, 0, 120, paint(shader=radial(0, 0, 120, [col(YELLOW, 0.45 * glow), col(YELLOW, 0)])))
        for (lx, ly, lr) in ((-10 * sx, -30, 36), (14 * sx, 4, 40), (-8 * sx, 36, 34), (26 * sx, -26, 26)):
            c.drawCircle(lx, ly, lr, paint(shader=radial(lx - lr * 0.3, ly - lr * 0.35, lr * 1.3, [col("#FFF3C4"), col("#F6D271"), col("#D9A93F")], [0, 0.55, 1])))
            c.drawCircle(lx, ly, lr, paint("#b98a2c", 0.5, stroke=1.5))
        c.restore()
    # ducts
    for sx in (-1, 1):
        c.drawLine(sx * (TUBE_W + 4), 40, sx * (TUBE_W + 30), 50, paint("#E9C26A", 1, stroke=10))


def block(c, t, cx, cy, s, st, light=False):
    """st: dict of state params."""
    c.save(); c.translate(cx, cy); c.scale(s, s)
    # contact shadow
    c.drawOval(skia.Rect.MakeLTRB(-FW - 30, BOTY - 30, FW + DX + 60, BOTY + 50), paint("#000000", 0.45 if not light else 0.2, blur=26))
    # right side face (layers, darker)
    def side(y0, y1, colr):
        p = skia.Path(); p.moveTo(FW, y0); p.lineTo(FW + DX, y0 + DY); p.lineTo(FW + DX, y1 + DY); p.lineTo(FW, y1); p.close()
        c.drawPath(p, paint(colr))
    side(TOPY, EPI, mixhex(TONE, "#000000", 0.35))
    side(EPI, DERM, mixhex("#E3BFAA", "#000000", 0.3))
    side(DERM, BOTY, mixhex("#F2E6CF", "#000000", 0.3))
    # top face with skin texture
    top = skia.Path(); top.moveTo(-FW, TOPY); top.lineTo(FW, TOPY); top.lineTo(FW + DX, TOPY + DY); top.lineTo(-FW + DX, TOPY + DY); top.close()
    m = skia.Matrix(); m.setAll(0.6, -0.07 * 0.42, -FW + DX, 0, 0.3, TOPY + DY, 0, 0, 1)
    sh = SKIN.makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, SAMP, m)
    c.drawPath(top, paint(shader=sh))
    c.drawPath(top, paint(shader=linear((0, TOPY + DY), (0, TOPY), [col("#000000", 0.15), col("#ffffff", 0.08)])))
    c.drawOval(skia.Rect.MakeLTRB(-TUBE_W - 10, TOPY - 16, TUBE_W + 10, TOPY + 4), paint("#4a3128", 0.9))
    c.drawOval(skia.Rect.MakeLTRB(-TUBE_W - 14, TOPY - 19, TUBE_W + 14, TOPY + 6), paint(TONE_DARK, 0.6, stroke=3))
    # sebum sheen on surface
    if st.get("sheen", 0) > 0:
        c.drawPath(top, paint(shader=radial(40, TOPY - 50, 330, [col("#FFF2B0", 0.35 * st["sheen"]), col("#FFF2B0", 0)])))
    # front face layers
    c.drawRect(skia.Rect.MakeLTRB(-FW, EPI, FW, DERM), paint(shader=linear((0, EPI), (0, DERM), [col("#E8C2AE"), col("#E3BCA6"), col("#DDB49D")])))
    # collagen wisps
    for k in range(9):
        p = skia.Path(); y = EPI + 30 + k * 44
        p.moveTo(-FW, y)
        for xx in range(-FW, FW + 1, 40):
            p.lineTo(xx, y + 9 * math.sin(xx / 55 + k * 1.7))
        c.drawPath(p, paint("#c99a86", 0.35, stroke=1.6))
    # capillaries
    for (x0, y0, x1, y1) in ((-330, -170, -180, -120), (200, -160, 330, -190), (-260, 160, -120, 120), (150, 150, 300, 175)):
        p = skia.Path(); p.moveTo(x0, y0); p.cubicTo((x0 + x1) / 2, y0 - 30, (x0 + x1) / 2, y1 + 30, x1, y1)
        c.drawPath(p, paint("#c96b6b", 0.55, stroke=3))
    c.drawRect(skia.Rect.MakeLTRB(-FW, TOPY, FW, EPI), paint(shader=linear((0, TOPY), (0, EPI), [col(TONE), col(mixhex(TONE, "#f0d6c4", 0.4))])))
    for k in range(4):
        c.drawLine(-FW, TOPY + 10 + k * 10, FW, TOPY + 10 + k * 10, paint(TONE_DARK, 0.18, stroke=1))
    c.drawRect(skia.Rect.MakeLTRB(-FW, DERM, FW, BOTY), paint("#F2E6CF"))
    for i in range(13):
        for j in range(3):
            x = -FW + 30 + i * 62 + (j % 2) * 31; y = DERM + 30 + j * 50
            c.drawCircle(x, y, 27, paint("#d8c6a2", 0.8, stroke=2))
            c.drawCircle(x - 7, y - 8, 9, paint("#ffffff", 0.35))
    # side lighting on front face
    c.drawRect(skia.Rect.MakeLTRB(-FW, TOPY, FW, BOTY), paint(shader=linear((-FW, 0), (FW, 0), [col("#ffffff", 0.08), col("#000000", 0.0), col("#000000", 0.18)])))
    # inflammation glow (behind tube)
    inf = st.get("inflame", 0)
    if inf > 0:
        c.drawCircle(0, -60, 260, paint(shader=radial(0, -60, 260, [col(RED, 0.55 * inf), col(RED, 0.2 * inf), col(RED, 0)], [0, 0.5, 1])))
    gland(c, t, st.get("glow", 0))
    # tube: lining + interior
    c.drawPath(TUBE, paint(mixhex(TONE, "#f2d9c8", 0.35)))
    inner = skia.Path(); inner.addPath(TUBE)
    c.save()
    c.translate(0, 0)
    c.scale(0.78, 1.0)
    c.drawPath(TUBE, paint(shader=linear((0, TOPY), (0, 140), [col("#6d4a3c"), col("#8a5f4c"), col("#a87862")])))
    c.restore()
    # shimmer along lining (retinoid)
    shm = st.get("shimmer", -1)
    if shm >= 0:
        c.save(); c.clipPath(TUBE)
        y = lerp(140, TOPY - 40, shm)
        c.drawRect(skia.Rect.MakeLTRB(-80, y - 40, 80, y + 40), paint(shader=linear((0, y - 40), (0, y + 40), [col(MINT, 0), col(MINT, 0.8), col(MINT, 0)])))
        c.restore()
    # contents (clipped to tube, but plug may dome above)
    c.save()
    clip = skia.Path(); clip.addPath(TUBE); clip.addRect(skia.Rect.MakeLTRB(-120, TOPY - 140, 120, TOPY + 2))
    c.clipPath(clip)
    tube_contents(c, t, st)
    c.restore()
    # filament (normal pore lining column)
    fil = st.get("filament", 0)
    if fil > 0:
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-13, TOPY - 1, 13, 60), 12, 12)
        c.drawRRect(rr, paint(shader=linear((-13, 0), (13, 0), [col("#e6dcc0", fil), col("#f6efd8", fil), col("#d6c8a6", fil)])))
        c.drawOval(skia.Rect.MakeLTRB(-13, TOPY - 6, 13, TOPY + 6), paint("#8c8478", fil))
    # cracks
    cr = st.get("crack", 0)
    if cr > 0:
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(sx * (TUBE_W + 2), -150)
            pts = [(sx * (TUBE_W + 18), -128), (sx * (TUBE_W + 8), -104), (sx * (TUBE_W + 30), -80), (sx * (TUBE_W + 14), -58), (sx * (TUBE_W + 40), -30)]
            for (px, py) in pts:
                p.lineTo(px, py)
            pp = paint(RED, cr, stroke=4)
            if cr < 0.999:
                te = skia.TrimPathEffect.Make(0, cr)
                if te: pp.setPathEffect(te)
            c.drawPath(p, pp)
    # whitehead lid
    lid = st.get("lid", 0)
    if lid > 0:
        r = skia.Rect.MakeLTRB(-60, TOPY - 34 * lid, 60, TOPY + 14)
        c.drawOval(r, paint(shader=radial(-12, TOPY - 20 * lid, 70, [col("#FFF7EC"), col(mixhex(TONE, "#ffffff", 0.55)), col(TONE)], [0, 0.5, 1])))
        c.drawRect(skia.Rect.MakeLTRB(-TUBE_W - 10, TOPY - 2, TUBE_W + 10, TOPY + 10), paint(mixhex(TONE, "#ffffff", 0.3), lid))
    # O2 specks
    o2 = st.get("o2", 0)
    if o2 > 0:
        f = skia.Font(TF_MONO, 18)
        for (x, ph, ph2) in O2:
            u = ((t * 0.35 + ph) % 1)
            y = lerp(TOPY - 300, TOPY - 6, u)
            xx = lerp(x, 0, u ** 1.5) + 6 * math.sin(t * 2 + ph2)
            a = o2 * math.sin(math.pi * u)
            c.drawCircle(xx, y, 7, paint("#E8F1FF", 0.9 * a))
            c.drawString("O₂", xx + 10, y + 6, f, paint("#E8F1FF", 0.7 * a))
    # mint droplets (salicylic acid)
    md = st.get("mint", 0)
    if md > 0:
        for k in range(10):
            u = clamp(md * 1.6 - k * 0.07)
            if u <= 0 or u >= 1:
                continue
            y = lerp(TOPY - 200, 60, eio(u))
            x = 10 * math.sin(k * 2.1 + t * 2)
            c.drawCircle(x, y, 10, paint(MINT, 0.9 * math.sin(math.pi * u)))
            c.drawCircle(x - 3, y - 3, 3, paint("#ffffff", 0.7 * math.sin(math.pi * u)))
    c.restore()


def tube_contents(c, t, st):
    flow = st.get("flow", 0)           # 0 none, 1 flowing out
    seb = st.get("sebum", 0)
    fl = st.get("flakes", 0)
    stick = st.get("stick", 0)         # slows and clumps
    plug = st.get("plug", 0)
    dark = st.get("dark", 0)
    push = st.get("pushdown", 0)
    dissolve = st.get("dissolve", 0)
    speed = lerp(1.0, 0.15, stick)
    top_exit = TOPY - 130 * flow
    # sebum droplets
    if seb > 0 and plug < 0.98:
        for (ph, xo, r, ph2) in DROPS:
            u = (t * 0.22 * speed + ph) % 1
            y = lerp(50, top_exit, u)
            x = xo * (TUBE_W - 12) + 4 * math.sin(t * 2 + ph2)
            if stick > 0:
                x *= 1 - 0.6 * stick
            a = seb * (1 - plug) * clamp(u * 6) * (1 if flow > 0 or u < 0.85 else (1 - u) * 6)
            c.drawCircle(x, y, r, paint(shader=radial(x - r * 0.35, y - r * 0.35, r * 1.3, [col("#FFF7CF", a), col("#FFD23F", a), col("#D9A12B", a)], [0, 0.5, 1])))
            c.drawCircle(x - r * 0.35, y - r * 0.4, r * 0.25, paint("#ffffff", 0.8 * a))
    if fl > 0 and plug < 0.98:
        for (ph, side, size, rot, wob) in FLAKES:
            u = (t * 0.16 * speed + ph) % 1
            y = lerp(90, top_exit, u)
            x = side * (TUBE_W - 6) * (1 - min(1, u * 3) * 0.6) * (1 - 0.7 * stick)
            a = fl * (1 - plug) * clamp(u * 5) * (1 if flow > 0 or u < 0.85 else (1 - u) * 6)
            c.save(); c.translate(x, y); c.rotate(rot * 30 + wob * math.sin(t + rot))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-size / 2, -4, size, 8), 4, 4), paint("#F4EFE6", 0.85 * a))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-size / 2, -4, size, 8), 4, 4), paint("#b9ab95", 0.6 * a, stroke=1.2))
            c.restore()
    if plug > 0:
        depth = 230 * plug
        dome = 14 * dark + 6
        yoff = 90 * push
        ytop = TOPY - dome * plug + yoff
        pp = skia.Path()
        pp.moveTo(-TUBE_W - 8, TOPY + yoff + 4)
        pp.quadTo(0, ytop - dome, TUBE_W + 8, TOPY + yoff + 4)
        pp.lineTo(TUBE_W + 2, TOPY + depth + yoff)
        pp.quadTo(0, TOPY + depth + 24 + yoff, -TUBE_W - 2, TOPY + depth + yoff)
        pp.close()
        if dissolve > 0:
            c.saveLayerAlpha(None, int(255 * (1 - dissolve)))
        base = mixhex("#F2C94C", "#E7B640", 0.5)
        c.drawPath(pp, paint(shader=linear((0, ytop), (0, TOPY + depth), [col(mixhex(base, "#1a120e", dark)), col(mixhex(base, "#5b3d22", dark * 0.8)), col(base), col("#E2AE3A")], [0, 0.12, 0.35, 1])))
        # packed flakes texture
        for k in range(16):
            yy = TOPY + 16 + (k * 14.3) % max(depth - 20, 1) + yoff
            xx = ((k * 37) % 50) - 25
            c.drawLine(xx - 9, yy, xx + 9, yy + 2, paint("#FBF3DC", 0.55, stroke=3))
        c.drawPath(pp, paint("#b98a2c", 0.6, stroke=2))
        if dissolve > 0:
            c.restore()
            # chunks floating out
            for (dx, dy, r, rot) in CHUNKS:
                u = clamp(dissolve * 1.3 - dy / 400)
                y = lerp(TOPY + dy * plug, TOPY - 220, eio(u))
                x = dx + 25 * u * rot
                a = math.sin(math.pi * clamp(u * 1.05))
                c.drawCircle(x, y, r * (1 - 0.5 * u), paint(mixhex("#F2C94C", "#2a1d15", dark * (dy < 40)), a))


def apple_inset(c, t, a, brown):
    x, y, w, h = 610, 470, 340, 300
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 28, 28)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 4, y + 12, w, h), 28, 28), paint("#000000", 0.4 * a, blur=18))
    c.drawRRect(rr, paint("#1d1b1c", a))
    c.save(); c.clipRRect(rr)
    cx, cy = x + w / 2, y + h / 2 + 10
    p = skia.Path()
    p.moveTo(cx, cy - 92)
    p.cubicTo(cx + 40, cy - 120, cx + 135, cy - 100, cx + 128, cy)
    p.cubicTo(cx + 122, cy + 90, cx + 60, cy + 118, cx, cy + 105)
    p.cubicTo(cx - 60, cy + 118, cx - 122, cy + 90, cx - 128, cy)
    p.cubicTo(cx - 135, cy - 100, cx - 40, cy - 120, cx, cy - 92)
    c.drawPath(p, paint("#C8312B", a))
    c.save(); c.translate(cx, cy); c.scale(0.92, 0.9); c.translate(-cx, -cy)
    flesh = mixhex("#F6E7BC", "#A86D3A", brown)
    c.drawPath(p, paint(shader=radial(cx - 30, cy - 30, 160, [col(mixhex("#FFF5D6", "#C08A50", brown), a), col(flesh, a)])))
    c.restore()
    for k in range(5):
        an = k * 72 * math.pi / 180 - math.pi / 2
        c.drawOval(skia.Rect.MakeXYWH(cx + math.cos(an) * 26 - 6, cy + math.sin(an) * 26 - 10, 12, 20), paint("#3b2414", a))
    c.drawLine(cx, cy - 92, cx + 6, cy - 128, paint("#5b3a1e", a, stroke=7))
    c.restore()
    c.drawRRect(rr, paint("#ffffff", 0.85 * a, stroke=4))
    f = skia.Font(TF_MONO, 20)
    c.drawString("SAME REACTION", x + 18, y + h - 18, f, paint("#ffffff", 0.7 * a))


def calendar(c, t, a, light=True):
    x0, y = 140, 600
    f = skia.Font(TF_MONO, 22)
    for k in range(8):
        q = eback(prog(t, WEEKS + 0.12 * k, 0.2))
        fill = prog(t, WEEKS + 0.12 * k + 0.05, 0.12)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 + k * 96, y, 80, 64), 14, 14)
        c.save(); c.translate(x0 + k * 96 + 40, y + 32); c.scale(q, q); c.translate(-(x0 + k * 96 + 40), -(y + 32))
        c.drawRRect(rr, paint(INK, 0.06 * a)); c.drawRRect(rr, paint(INK, 0.3 * a, stroke=1.5))
        if fill > 0:
            c.drawRRect(rr, paint(MINT, a * fill))
        s = f"W{k + 1}"
        c.drawString(s, x0 + k * 96 + 40 - f.measureText(s) / 2, y + 40, f, paint(INK, a))
        c.restore()


# ---------------- per-mode scene drawing ----------------
def state_main(t):
    """block state through the dark explainer (blockA/blockB)."""
    st = {}
    st["glow"] = eout(prog(t, OIL, 0.4)) * (1 - 0.6 * prog(t, SEBUM + 1, 1))
    st["sebum"] = eout(prog(t, SEBUM - 0.1, 0.5))
    st["sheen"] = eout(prog(t, SOFT, 0.6))
    st["flakes"] = eout(prog(t, CELLS, 0.5))
    st["flow"] = eout(prog(t, TOGETHER - 0.6, 0.6)) * (1 - prog(t, STICKY - 0.2, 0.4))
    st["stick"] = eout(prog(t, STICKY - 0.2, 0.6))
    st["plug"] = eio(prog(t, CLUMP, PLUG - CLUMP + 0.05))
    return st


def hud_state(t):
    if t < TOGETHER - 0.3: return ("?", "#9a9a9a")
    if t < PLUG: return ("CLEAR", MINT)
    if t < OPEN: return ("CLOGGED", YELLOW)
    if t < DARKEN + 0.3: return ("OPEN", "#d9d9d9")
    if t < SALIC: return ("OXIDISED", "#5b3d22")
    return ("CLEARING", MINT)


def draw_world(c, t):
    m = mode_at(t)
    if m == "macro1":
        push = 1.5 * (1 + 0.03 * prog(t, 0, DIVE))
        dz = ein(prog(t, DIVE, 0.45))
        push *= 1 + 3.0 * dz
        macro(c, t, push, box=eout(prog(t, 0, 0.25)) * (1 - prog(t, DIVE, 0.2)))
        # DIRT? pill: pop, strike, fall
        if DIRT - 0.05 < t < DIRT + 1.4:
            fall = ein(prog(t, DIRT + 0.6, 0.6))
            c.save(); c.translate(0, 500 * fall); c.rotate(12 * fall)
            pill(c, t, "DIRT?", 760, 880, "#8a8a8a", DIRT, DIRT + 1.1, anchor=(578, 980))
            sp = eout(prog(t, DIRT + 0.25, 0.18))
            if sp > 0:
                c.drawLine(690, 882, lerp(690, 830, sp), 878, paint(RED, 1 - prog(t, DIRT + 1.0, 0.2), stroke=5))
            c.restore()
        if t > DIVE:
            a = eout(prog(t, DIVE + 0.2, 0.25))
            c.saveLayerAlpha(None, int(255 * a)); draw_block_scene(c, t); c.restore()
        return
    if m == "blockA":
        draw_block_scene(c, t)
        if t > SQ_IN:
            a = eout(prog(t, SQ_IN, 0.4))
            c.saveLayerAlpha(None, int(255 * a)); draw_900(c, t); c.restore()
        return
    if m == "macro900":
        draw_900(c, t)
        if t > BLK2:
            a = eout(prog(t, BLK2, 0.4))
            c.saveLayerAlpha(None, int(255 * a)); draw_block_scene(c, t); c.restore()
        return
    if m == "blockB":
        draw_block_scene(c, t)
        if t > BLACKHEAD_T:
            a = eout(prog(t, BLACKHEAD_T, 0.4))
            c.saveLayerAlpha(None, int(255 * a)); draw_bh_macro(c, t); c.restore()
        return
    if m == "macroBH":
        draw_bh_macro(c, t); return
    if m == "white":
        draw_white(c, t); return
    if m == "macroGrid":
        draw_grid(c, t)
        if t > VS:
            a = eout(prog(t, VS, 0.4))
            c.saveLayerAlpha(None, int(255 * a)); draw_vs(c, t); c.restore()
        return
    if m == "vs":
        draw_vs(c, t)
        if t > LOOP:
            a = eout(prog(t, LOOP, 0.45))
            c.saveLayerAlpha(None, int(255 * a)); draw_end(c, t); c.restore()
        return
    draw_end(c, t)


def draw_block_scene(c, t):
    studio_dark(c)
    st = state_main(t)
    settle = eout(prog(t, DIVE + 0.2, 0.8))
    s = lerp(1.35, 1.0, settle)
    if t > BLK2:
        s = lerp(1.25, 1.0, eout(prog(t, BLK2, 0.7)))
    push = 1 + 0.035 * prog(t, BLK2, SPLIT - BLK2) if t > BLK2 else 1
    sp = eio(prog(t, SPLIT, 0.7))
    cx = lerp(500, 300, sp); cy = lerp(1080, 1110, sp)
    sc = s * push * lerp(1.0, 0.56, sp)
    stl = dict(st)
    if t > SPLIT:
        stl["lid"] = eback(prog(t, SPLIT + 0.25, 0.6), 1.2)
    block(c, t, cx, cy, sc, stl)
    if sp > 0:
        str_ = dict(st)
        str_["o2"] = eout(prog(t, OPEN - 0.1, 0.5))
        str_["dark"] = eio(prog(t, DARKEN - 0.1, 1.0))
        rx = lerp(1400, 790, sp)
        block(c, t, rx, cy, sc, str_)
        # divider
        c.drawLine(540, 760, 540, 1440, paint("#ffffff", 0.18 * sp, stroke=2))
    # pills (single block coords)
    def L(x, y):  # local→screen for main block
        return (cx + x * sc, cy + y * sc)
    if sp < 0.5:
        a = 1 - sp * 2
        pill(c, t, "PORE", 300, 640, "#FFFFFF", TUBE_T, SQ_IN, anchor=L(-20, TOPY - 6))
        pill(c, t, "OIL GLAND", 830, 1330, YELLOW, OIL, SQ_IN, anchor=L(110, 70))
        pill(c, t, "SEBUM", 850, 820, YELLOW, SEBUM, CELLS + 0.2, anchor=L(10, -60))
        pill(c, t, "DEAD SKIN CELLS", 760, 1330, "#F4F2EE", CELLS, TOGETHER + 0.1, anchor=L(-30, -20))
        pill(c, t, "NORMAL", 830, 820, MINT, TOGETHER, STICKY - 0.2, anchor=L(0, TOPY - 80))
        pill(c, t, "PLUG", 830, 820, YELLOW, PLUG, SPLIT, anchor=L(20, TOPY + 60))
    pill(c, t, "WHITEHEAD", 300, 690, "#F4F2EE", WHITEHEAD, BLACKHEAD_T, anchor=(300, cy + (TOPY - 30) * sc))
    pill(c, t, "OPEN", 790, 690, "#FFFFFF", OPEN, DARKEN, anchor=(790, cy + (TOPY - 10) * sc))
    if t > APPLE - 0.1:
        a = eback(prog(t, APPLE, 0.35), 1.1) * (1 - prog(t, BLACKHEAD_T, 0.3))
        if a > 0:
            c.save(); c.translate(780, 620); c.scale(a, a); c.translate(-780, -620)
            apple_inset(c, t, clamp(a), eio(prog(t, APPLE + 0.2, 1.1)))
            c.restore()
    footnote(c, t, "Magnified illustration", DIVE + 0.3, SQ_IN)
    footnote(c, t, "Magnified illustration · simplified", BLK2 + 0.3, DARKEN - 0.2)
    footnote(c, t, "Oxidation of melanin & oils, not dirt", DARKEN, BLACKHEAD_T + 0.3)


def draw_900(c, t):
    push = lerp(1.18, 1.0, eout(prog(t, SQ_IN, 0.8)))
    macro(c, t, push, hero=False, box=0)
    c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 0.25))
    ruler_square(c, t, 1)
    v = 900 * eexpo(prog(t, N900, 1.1))
    pulse = 1 + 0.06 * math.sin(math.pi * prog(t, N900 + 1.1, 0.25))
    big_number(c, f"{int(v)}", "PER cm²", 540, 760, 150, YELLOW, eout(prog(t, N900 - 0.1, 0.2)), pulse)
    fi = eout(prog(t, SQ_IN + 0.3, 0.7))
    fingertip(c, lerp(1200, 900, fi), lerp(1700, 1290, fi), 32, 470, 1100)
    f = skia.Font(TF_MONO_M, 22)
    lab = "FINGERTIP"
    c.drawString(lab, 760, 1180 + 0 * fi, f, paint("#FFFFFF", 0.0))
    footnote(c, t, "Forehead & T-zone: 400–900 per cm² · DermNet", N900 + 0.3, BLK2 + 0.3)


def salt(c, x, y, s):
    p = skia.Path()
    p.moveTo(x, y - s); p.lineTo(x + s, y - s * 0.5); p.lineTo(x + s, y + s * 0.5); p.lineTo(x, y + s); p.lineTo(x - s, y + s * 0.5); p.lineTo(x - s, y - s * 0.5); p.close()
    c.drawPath(p, paint("#ffffff", 0.75))
    top = skia.Path(); top.moveTo(x, y - s); top.lineTo(x + s, y - s * 0.5); top.lineTo(x, y); top.lineTo(x - s, y - s * 0.5); top.close()
    c.drawPath(top, paint("#ffffff", 0.95))
    c.drawPath(p, paint("#c9d6e0", 0.9, stroke=1.5))


def draw_bh_macro(c, t):
    push = lerp(2.4, 2.2, eout(prog(t, BLACKHEAD_T, 1.2)))
    macro(c, t, push, box=0)
    a = eout(prog(t, BLACKHEAD_T + 0.3, 0.3))
    # ruler under dot: 1-3 mm, 1 mm = 40 px
    x0, y = 480, 1110
    c.drawLine(x0, y, x0 + 120, y, paint("#ffffff", a, stroke=3))
    f = skia.Font(TF_MONO, 22)
    for k in range(4):
        c.drawLine(x0 + k * 40, y, x0 + k * 40, y - 14, paint("#ffffff", a, stroke=2))
        c.drawString(str(k), x0 + k * 40 - 6, y + 30, f, paint("#ffffff", a))
    c.drawString("mm", x0 + 132, y + 6, f, paint("#ffffff", 0.8 * a))
    salt(c, 720, 1000, 14)
    c.drawString("GRAIN OF SALT", 680, 1050, skia.Font(TF_MONO_M, 18), paint("#ffffff", 0.75 * a))
    pill(c, t, "BLACKHEAD · 1–3 mm", 540, 820, "#2a1d15", BLACKHEAD_T + 0.35, WIPE1 + 0.3, anchor=(540, 935), text_col="#FFFFFF")
    footnote(c, t, "Magnified illustration · not to scale", BLACKHEAD_T + 0.3, WIPE1 + 0.3)


def draw_white(c, t):
    studio_white(c)
    st = dict(plug=1, dark=1, flakes=0, sebum=0)
    tear = eout(prog(t, TEAR, 0.6)) * (1 - eio(prog(t, SALIC - 0.15, 0.5)))
    st["crack"] = tear
    st["inflame"] = eout(prog(t, TEAR + 0.2, 0.7)) * (1 - eio(prog(t, SALIC - 0.15, 0.6)))
    st["pushdown"] = eout(prog(t, TEAR + 0.3, DEEPER - TEAR)) * (1 - eio(prog(t, SALIC - 0.15, 0.5)))
    st["mint"] = prog(t, SALIC, 1.4)
    st["dissolve"] = eio(prog(t, DISSOLVE - 0.2, 1.4))
    if t > RETIN - 0.1:
        st["shimmer"] = prog(t, RETIN - 0.1, 1.1)
        st["flakes"] = eout(prog(t, RETIN, 0.5)); st["flow"] = 1; st["sebum"] = 0.6 * eout(prog(t, RETIN, 0.5))
    if t > WEEKS:
        st["flakes"] *= 1 - 0.0
    s = 1 + 0.03 * prog(t, WIPE1, WIPE2 - WIPE1)
    cx, cy = 500, 1090
    block(c, t, cx, cy, s, st, light=True)
    # fingertips (squeeze)
    fa = eout(prog(t, SQUEEZE - 0.4, 0.5)) * (1 - eio(prog(t, TEAR + 0.6, 0.5)))
    if fa > 0:
        press = eio(prog(t, NOTEX - 0.12, 0.2)) * (1 - 0.6 * prog(t, TEAR + 0.3, 0.4))
        gap = lerp(150, 85, press)
        sy = cy + (TOPY - 45) * s
        fingertip(c, cx - gap * s, sy, 90 + 10, 110, 360, fa)
        fingertip(c, cx + gap * s, sy, -90 - 10, 110, 360, fa)
    pill(c, t, "SQUEEZE?", 500, 640, RED, SQUEEZE, TEAR + 0.2, light=True, outline=True)
    pill(c, t, "INFLAMMATION", 820, 1330, RED, TEAR + 0.4, SALIC - 0.1, anchor=(cx + 80 * s, cy - 60 * s), light=True)
    pill(c, t, "SALICYLIC ACID", 330, 660, MINT, SALIC, RETIN, anchor=(cx, cy + (TOPY - 60) * s), light=True)
    pill(c, t, "RETINOID", 780, 1330, MINT, RETIN, WEEKS + 1.2, anchor=(cx + 30 * s, cy - 40 * s), light=True)
    if t > WEEKS - 0.1:
        calendar(c, t, 1 - prog(t, WIPE2 - 0.1, 0.2))
    footnote(c, t, "Can lead to marks or scarring", TEAR + 0.4, SALIC, light=True)
    footnote(c, t, "Some retinoids need a prescription. Ask a pharmacist.", RETIN + 0.1, WEEKS + 0.2, light=True)
    footnote(c, t, "AAD: give treatments 6–8 weeks", WEEKS + 0.2, WIPE2 + 0.2, light=True)


def draw_grid(c, t):
    push = lerp(0.9, 0.95, prog(t, WIPE2, 2))
    macro(c, t, push, hero=False, box=0, grid=eout(prog(t, TWIST - 0.3, 0.6)))


def draw_vs(c, t):
    studio_dark(c)
    s = 0.56
    lp = eout(prog(t, VS, 0.6))
    block(c, t, lerp(200, 300, lp), 1110, s, dict(plug=1, dark=1))
    block(c, t, lerp(900, 790, lp), 1110, s, dict(filament=1))
    c.drawLine(540, 760, 540, 1440, paint("#ffffff", 0.18 * lp, stroke=2))
    pill(c, t, "BLACKHEAD", 300, 700, "#2a1d15", VS + 0.3, LOOP, anchor=(300, 1110 + (TOPY - 20) * s), text_col="#FFFFFF")
    pill(c, t, "FILAMENT", 790, 700, "#E9E4DA", FILA, LOOP, anchor=(790, 1110 + (TOPY - 6) * s))
    pill(c, t, "✓ NORMAL", 790, 780, MINT, NORMAL, LOOP)
    footnote(c, t, "Not medical advice. See a GP or dermatologist if spots are painful or not improving.", FILA - 0.2, DUR - 1.9)


def draw_end(c, t):
    push = 1.5 * lerp(1.03, 1.0, eio(prog(t, LOOP, DUR - 0.4 - LOOP)))
    macro(c, t, push, box=eout(prog(t, LOOP + 0.5, 0.3)))
    footnote(c, t, "Sources: AAD · DermNet NZ · Cleveland Clinic", DUR - 2.0, DUR + 1)


KWCOL = {"nose": "#FFFFFF", "dirt": RED, "tube": "#FFFFFF", "oil": YELLOW, "900": YELLOW, "centimetre": "#FFFFFF",
         "sebum": YELLOW, "soft": YELLOW, "dead skin": "#FFFFFF", "together": MINT, "sticky": YELLOW, "plug": YELLOW,
         "whitehead": "#FFFFFF", "open": "#FFFFFF", "darkens": "#FFFFFF", "apple": RED, "blackhead": "#FFFFFF",
         "squeeze": RED, "not exactly": RED, "deeper": RED, "Salicylic": MINT, "retinoid": MINT, "six to": MINT,
         "twist": YELLOW, "sebaceous": MINT, "normal": MINT}
CAPS = Captions(P, KWCOL, {"900", "Not", "not"}, DUR)


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    sx = sy = 0
    for ti in IMPACTS:
        d = t - ti
        if 0 <= d < 0.33:
            amp = 9 * (1 - d / 0.33)
            sx += amp * math.sin(d * 97); sy += amp * math.cos(d * 83)
    c.save(); c.translate(sx, sy)
    draw_world(c, t)
    c.restore()
    light = light_at(t)
    dust(c, t, light)
    vignette(c, light)
    # HUD
    lab, dc = hud_state(t)
    ha = prog(t, 0.3, 0.3) * (1 - prog(t, LOOP - 0.3, 0.3))
    if not (SQ_IN + 0.3 < t < BLK2 + 0.2):
        hud(c, t, "PORE STATUS", lab, dc, ha, light)
    rw = math.sin(math.pi * prog(t, NOTEX, 0.45))
    if rw > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), paint(RED, 0.26 * rw))
    for ti in IMPACTS:
        if 0 <= t - ti < 2 / FPS:
            c.drawRect(skia.Rect.MakeWH(W, H), paint("#FFFFFF", 0.3))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, MINT, "#F4F2EE")
    wipe(c, t, WIPE2, WL, MINT, INK)
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("pop", 0.25), ("pop", DIRT), ("tick", DIRT + 0.25), ("whoosh", DIVE), ("pop", TUBE_T), ("pop", OIL),
          ("whoosh", SQ_IN), ("whoosh", BLK2), ("pop", SEBUM), ("pop", CELLS), ("pop", TOGETHER),
          ("hit", PLUG), ("pop", PLUG + 0.05), ("whoosh", SPLIT), ("pop", WHITEHEAD), ("pop", OPEN),
          ("riser", OPEN - 0.2), ("pop", APPLE), ("pop", BLACKHEAD_T + 0.35), ("whoosh", WIPE1), ("paper", WIPE1 + 0.12),
          ("pop", SQUEEZE), ("hit", NOTEX), ("pop", TEAR + 0.4), ("whoosh", SALIC - 0.15), ("pop", SALIC), ("pop", RETIN),
          ("whoosh", WIPE2), ("riser", TWIST - 0.2), ("whoosh", VS), ("pop", VS + 0.3), ("pop", FILA), ("ding", NORMAL),
          ("whoosh", LOOP)]
    for k in range(10):
        ev.append(("tick", N900 + 0.06 * k * (1 + k * 0.25)))
    ev.append(("ding", N900 + 1.1))
    for k in range(8):
        ev.append(("tick", WEEKS + 0.12 * k + 0.05))
    return sorted(ev, key=lambda e: e[1])


if __name__ == "__main__":
    if sys.argv[1] == "still":
        from PIL import Image
        for ts in sys.argv[2:]:
            Image.fromarray(frame(float(ts))[..., :3]).save(f"{D}/still_{ts}.png")
        sys.exit()
    if sys.argv[1] == "beats":
        for k, v in list(globals().items()):
            if k.isupper() and isinstance(v, float):
                print(k, round(v, 2))
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

"""Reusable locations. Each set returns layers (back -> front) so characters can be slotted between them
and the camera can move each layer with its own parallax depth."""
import math
import random
from art import PAL, INK, W, H, ell, poly, rrect, blob, curve, line, stroke, fill, g, f2

# ============================================================== THRONE ROOM
VP = (540, 610)          # vanishing point
BACK = (300, 150, 780, 790)   # back wall x0,y0,x1,y1


def _fx(z, x):  # back-wall x at depth z (z=1 back wall, smaller = closer)
    return VP[0] + (x - VP[0]) / z


def _fy(z, y):
    return VP[1] + (y - VP[1]) / z


def throne_room(D, t=0.0, light="day"):
    L = {}
    x0, y0, x1, y1 = BACK
    stone, stone_d = "#d3bfa2", "#9a8597"
    # ---------- back: walls, windows, banners, throne
    s = fill(rrect(-200, -200, W + 400, H + 400, 0), "#3a2c4a")
    # side walls (trapezoids to the frame edges)
    zL = 0.18
    lw = poly([(x0, y0), (x0, y1), (_fx(zL, x0), _fy(zL, y1)), (_fx(zL, x0), _fy(zL, y0))])
    rw = poly([(x1, y0), (x1, y1), (_fx(zL, x1), _fy(zL, y1)), (_fx(zL, x1), _fy(zL, y0))])
    s += fill(lw, D.lin([(0, "#a48c86"), (1, "#5e4c70")], 1, 0, 0, 0))
    s += fill(rw, D.lin([(0, "#7a6585"), (1, "#3f3258")], 0, 0, 1, 0))
    # back wall with block pattern
    bw = poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    s += fill(bw, D.lin([(0, "#cdb79c"), (1, "#a38f97")]))
    rnd = random.Random(3)
    for row in range(0, 22):
        yy = y0 + row * 30
        off = 0 if row % 2 else 34
        for col in range(-1, 8):
            xx = x0 + off + col * 68
            if xx + 64 < x0 or xx > x1:
                continue
            a, b = max(xx, x0), min(xx + 64, x1)
            c = rnd.choice(["#d6c2a6", "#c9b49a", "#d1bca5", "#c3ae99"])
            s += fill(rrect(a + 2, yy + 2, b - a - 4, 26, 4), c, 0.55)
    # vaulted ceiling band
    s += fill(poly([(x0, y0), (x1, y0), (_fx(zL, x1), _fy(zL, y0)), (_fx(zL, x0), _fy(zL, y0))]), D.lin([(0, "#4a3a5e"), (1, "#2c2140")]))
    for k in range(5):
        xa = x0 + (x1 - x0) * k / 4
        s += stroke(line(xa, y0, _fx(zL, xa), _fy(zL, y0)), 6, "#22182f", 0.7)
    # windows on the back wall (left and right of the throne) with warm glass
    for wx in (360, 640):
        win = blob([(wx, 300), (wx + 40, 236), (wx + 80, 300)], close=False) + f"L{wx+80},560L{wx},560Z"
        win = f"M{wx},560 L{wx},300 Q{wx},230 {wx+40},226 Q{wx+80},230 {wx+80},300 L{wx+80},560Z"
        s += fill(win, D.lin([(0, "#fff4cf"), (0.6, "#ffd88e"), (1, "#f2a95a")]))
        s += stroke(line(wx + 40, 226, wx + 40, 560), 5)
        s += stroke(line(wx, 400, wx + 80, 400), 5)
        s += stroke(win, 7)
        s += fill(rrect(wx - 10, 556, 100, 16, 4), "#b9a28a") + stroke(rrect(wx - 10, 556, 100, 16, 4), 4)
    # banners between
    for bx in (470, 590):
        ban = poly([(bx - 22, 210), (bx + 22, 210), (bx + 22, 420), (bx, 400), (bx - 22, 420)])
        s += D.shaded(ban, PAL["teal"], PAL["teal_d"], off=(5, 3), sw=4.5)
        s += D.shaded(ell(bx, 290, 12, 12), PAL["gold"], PAL["gold_d"], off=(2, 2), sw=3)
        s += stroke(line(bx - 30, 210, bx + 30, 210), 6, "#5b3f2a")
    L["back"] = s

    # ---------- dais + throne
    s = ""
    for i, (w2, yy, hh) in enumerate([(230, 760, 34), (190, 728, 34), (150, 696, 34)]):
        top = poly([(540 - w2, yy), (540 + w2, yy), (540 + w2 + 12, yy + hh), (540 - w2 - 12, yy + hh)])
        s += D.shaded(top, "#d9c6ab", "#a08c95", off=(6, 4), sw=4.5)
    # red carpet up the steps and down the hall
    carpet = poly([(500, 700), (580, 700), (_fx(0.1, 600), _fy(0.1, 790)), (_fx(0.1, 480), _fy(0.1, 790))])
    s += fill(carpet, D.lin([(0, "#9e2a3a"), (1, "#c23a45")]))
    s += stroke(carpet, 5)
    for side in (-1, 1):
        edge = [(540 + side * 34, 700), (_fx(0.1, 540 + side * 52), _fy(0.1, 790))]
        s += stroke(line(*edge[0], *edge[1]), 6, PAL["gold"], 0.9)
    # throne
    back_ = f"M450,700 L450,420 Q450,330 540,300 Q630,330 630,420 L630,700Z"
    s += D.shaded(back_, PAL["gold"], PAL["gold_d"], off=(10, 6))
    vel = f"M472,690 L472,430 Q472,356 540,334 Q608,356 608,430 L608,690Z"
    s += D.shaded(vel, PAL["crimson"], PAL["crimson_d"], off=(8, 5), sw=4)
    s += D.shaded(ell(540, 300, 22, 22), "#fff0b0", PAL["gold_d"], off=(4, 3), sw=4)
    for side in (-1, 1):
        s += D.shaded(rrect(540 + side * 120 - 22, 560, 44, 140, 10), PAL["gold"], PAL["gold_d"], off=(5, 3))
        s += D.shaded(ell(540 + side * 120, 556, 26, 14), "#f7d06a", PAL["gold_d"], off=(3, 2), sw=4)
    L["throne"] = s

    # ---------- floor (tiles in perspective)
    s = ""
    fl = poly([(x0, y1), (x1, y1), (_fx(0.1, x1), _fy(0.1, y1)), (_fx(0.1, x0), _fy(0.1, y1))])
    s += fill(fl, D.lin([(0, "#a8918c"), (0.45, "#c9b096"), (1, "#7d6878")]))
    s += f'<g clip-path="{D.clip(fl)}">'
    for k in range(-6, 13):
        xa = x0 + (x1 - x0) * k / 6
        s += stroke(line(xa, y1, _fx(0.1, xa), _fy(0.1, y1)), 3, "#5d4a63", 0.45)
    z = 1.0
    while z > 0.1:
        yy = _fy(z, y1)
        s += stroke(line(-50, yy, W + 50, yy), 3, "#5d4a63", 0.45)
        z *= 0.82
    s += "</g>"
    L["floor"] = s

    # ---------- pillars (mid depth) with candles
    s = ""
    for z in (0.85, 0.55, 0.38):
        for side in (-1, 1):
            xb = 540 + side * 250
            cx = _fx(z, xb)
            wpx = 34 / z
            top, bot = _fy(z, y0 - 40), _fy(z, y1)
            col = rrect(cx - wpx, top, 2 * wpx, bot - top, 6)
            lit = "#e3cfb2" if side < 0 else "#bda594"
            s += D.shaded(col, lit, "#7b6784", off=(-wpx * 0.35 * side if side > 0 else wpx * 0.35, 0), sw=4 / max(z, 0.5))
            s += D.shaded(rrect(cx - wpx * 1.25, bot - 40 / z, 2.5 * wpx, 40 / z, 6), lit, "#7b6784", off=(4, 3), sw=4)
            s += D.shaded(rrect(cx - wpx * 1.25, top, 2.5 * wpx, 36 / z, 6), lit, "#7b6784", off=(4, 3), sw=4)
    L["pillars"] = s

    # ---------- candle stands near the dais (flicker with t)
    s = ""
    for cx, cy, sc in ((350, 790, 1.0), (730, 790, 1.0)):
        s += stroke(line(cx, cy, cx, cy - 170 * sc), 12, INK) + stroke(line(cx, cy, cx, cy - 170 * sc), 6, PAL["gold_d"])
        s += D.shaded(ell(cx, cy - 172 * sc, 26, 8), PAL["gold"], PAL["gold_d"], off=(3, 2), sw=4)
        for dx in (-14, 0, 14):
            s += D.shaded(rrect(cx + dx - 5, cy - 210 * sc, 10, 36, 3), PAL["cream"], "#d8c7a8", off=(2, 1), sw=3)
            fl_ = 1 + 0.12 * math.sin(t * 11 + dx) + 0.06 * math.sin(t * 23 + dx * 2)
            fx, fy = cx + dx, cy - 220 * sc
            s += fill(ell(fx, fy - 4 * fl_, 6, 12 * fl_), "#ffe38a")
            s += fill(ell(fx, fy - 2, 3, 6 * fl_), "#ffffff")
        glow = D.rad([(0, "#ffcf6a", 0.55 * (0.92 + 0.08 * math.sin(t * 9))), (1, "#ffcf6a", 0)])
        s += fill(ell(cx, cy - 215 * sc, 120, 120), glow)
    L["candles"] = s
    return L


def light_shafts(D, t=0.0, strength=1.0):
    """Warm god-rays from the two back windows falling toward camera-right + drifting dust."""
    s = ""
    bl = D.blur(18)
    for wx, a in ((360, 0.5), (640, 0.4)):
        sh = poly([(wx + 6, 300), (wx + 76, 300), (wx + 420, 1500), (wx - 40, 1500)])
        grad = D.lin([(0, "#fff0c2", a * strength), (1, "#ffd27a", 0)])
        s += f'<path d="{sh}" fill="{grad}" filter="{bl}" style="mix-blend-mode:screen"/>'
    rnd = random.Random(11)
    for i in range(46):
        x = rnd.uniform(330, 1000)
        y = rnd.uniform(320, 1400)
        sp = rnd.uniform(4, 12)
        x += math.sin(t * 0.6 + i) * 18 + t * sp * 0.6
        y += math.cos(t * 0.5 + i * 1.7) * 14 - t * sp * 0.4
        r = rnd.uniform(1.6, 3.6)
        s += fill(ell(x, y, r, r), "#fff2c8", rnd.uniform(0.35, 0.8))
    return s


def grade(D, warm=0.18, vignette=0.55, tint="#ffcf8a"):
    """Finishing pass shared by every shot: warm key wash top-left + plum vignette."""
    s = fill(rrect(-10, -10, W + 20, H + 20, 0), D.rad([(0, tint, warm), (1, tint, 0)], cx=0.3, cy=0.25, r=0.75))
    s += f'<rect x="-10" y="-10" width="{W+20}" height="{H+20}" fill="{D.rad([(0.55, "#1d1030", 0), (1, "#1d1030", vignette)], r=0.75)}"/>'
    return s


# ============================================================== PALACE EXTERIOR (golden hour)
def palace_exterior(D, t=0.0):
    L = {}
    # sky
    s = fill(rrect(-200, -200, W + 400, H + 400, 0), D.lin([(0, "#5b4b8f"), (0.38, "#d8829a"), (0.62, "#ffc98a"), (1, "#ffe7b5")]))
    sun = D.rad([(0, "#fff6d8", 1), (0.25, "#ffe2a0", 0.9), (1, "#ffbf7a", 0)])
    s += fill(ell(250, 860, 360, 360), sun)
    s += fill(ell(250, 860, 70, 70), "#fff7df")
    # clouds (layered, drifting)
    for cx, cy, sc, sp, col in ((820, 380, 1.3, 6, "#f7b9a6"), (240, 520, 1.0, 9, "#ffd3b0"), (700, 640, 0.8, 12, "#ffe0bd")):
        x = cx + t * sp
        cl = blob([(x - 160 * sc, cy), (x - 110 * sc, cy - 50 * sc), (x - 30 * sc, cy - 80 * sc), (x + 60 * sc, cy - 60 * sc), (x + 150 * sc, cy - 20 * sc), (x + 170 * sc, cy + 20 * sc), (x - 150 * sc, cy + 24 * sc)])
        s += fill(cl, col, 0.95) + fill(cl, "#ffffff", 0.25, f'transform="translate(-6,-10)"')
    # far mountains (atmospheric)
    s += fill(blob([(-100, 1100), (60, 900), (200, 980), (360, 860), (520, 1000), (700, 880), (880, 960), (1180, 900), (1180, 1200), (-100, 1200)]), "#b98aa6", 0.85)
    s += fill(blob([(-100, 1150), (120, 1020), (300, 1090), (500, 1010), (760, 1080), (1000, 1000), (1180, 1060), (1180, 1250), (-100, 1250)]), "#a2789c")
    L["sky"] = s

    # ---------- castle on the hill (upper right third)
    s = ""
    wall, wall_d = "#f1dcc0", "#b996a8"
    roof, roof_d = "#3f6f8a", "#2a4a66"
    hill = blob([(-100, 1300), (200, 1180), (520, 1090), (800, 1080), (1180, 1130), (1180, 2100), (-100, 2100)])
    s += D.shaded(hill, "#7aa45c", "#557d4e", off=(0, -14), sw=5)
    # main keep
    def tower(x, base, top, w, rh):
        o = D.shaded(rrect(x - w, top, 2 * w, base - top, 4), wall, wall_d, off=(-w * 0.35, 0))
        for yy in range(int(top + 40), int(base - 30), 70):
            o += D.shaded(f"M{x-10},{yy+40} L{x-10},{yy+12} Q{x},{yy} {x+10},{yy+12} L{x+10},{yy+40}Z", "#ffd27a", "#e09a4f", off=(2, 2), sw=3.5)
        o += D.shaded(poly([(x - w - 14, top + 4), (x, top - rh), (x + w + 14, top + 4)]), roof, roof_d, off=(-8, 0))
        o += stroke(line(x, top - rh, x, top - rh - 50), 4)
        flag = poly([(x, top - rh - 50), (x + 46 + 6 * math.sin(t * 4 + x), top - rh - 40), (x, top - rh - 28)])
        o += D.shaded(flag, PAL["gold"], PAL["gold_d"], off=(2, 2), sw=3.5)
        return o
    s += D.shaded(rrect(560, 860, 380, 260, 4), wall, wall_d, off=(-30, 0))
    for k in range(10):  # crenellations
        s += D.shaded(rrect(560 + k * 38, 836, 26, 30, 3), wall, wall_d, off=(-6, 0), sw=4)
    s += tower(600, 1110, 700, 46, 120)
    s += tower(900, 1110, 720, 42, 110)
    s += tower(750, 1000, 560, 60, 170)
    gate = "M710,1112 L710,1020 Q750,970 790,1020 L790,1112Z"
    s += D.shaded(gate, "#4a2f3a", "#2c1b26", off=(3, 2))
    s += fill(gate, "#ffcf7a", 0.25)
    L["castle"] = s

    # ---------- winding road from bottom-left to the gate + the three travellers
    s = ""
    road = blob([(742, 1112), (690, 1170), (560, 1230), (400, 1320), (330, 1460), (330, 1640), (280, 1800), (220, 2000), (560, 2000), (560, 1800), (560, 1640), (580, 1480), (640, 1340), (730, 1220), (790, 1112)], t=0.9)
    s += D.shaded(road, "#e8c99a", "#b89778", off=(-8, 0), sw=5)
    L["road"] = s

    # ---------- foreground trees + grass (big, dark, framing)
    s = ""
    def tree(x, y, sc, lit="#5f9a4e", sh="#2f5a45"):
        o = D.shaded(rrect(x - 18 * sc, y - 160 * sc, 36 * sc, 170 * sc, 10), "#8a5a3e", "#5a3a2e", off=(-6, 0))
        pts = []
        for k in range(14):
            a = 3.14159 * 2 * k / 14
            rr = (1.0 if k % 2 == 0 else 0.86) * 150 * sc
            pts.append((x + math.cos(a) * rr * 1.05, y - 270 * sc + math.sin(a) * rr * 0.9))
        crown = blob(pts)
        o += D.shaded(crown, lit, sh, off=(-28 * sc, -6 * sc), rim="#ffd27a")
        return o
    s += tree(1010, 1640, 1.5)
    s += tree(130, 1270, 0.85, "#6ea85a", "#3c6a4e")
    L["trees"] = s
    return L

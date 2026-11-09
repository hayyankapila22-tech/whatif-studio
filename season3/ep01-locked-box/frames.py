import sys; sys.path.insert(0, "/home/claude/whatif-studio/season3/kit")
from art import Doc, g, fill, rrect, stroke, line, ell, blob, poly, PAL, W, H
from chars import king_seated, corvin, bram, wren, guard
from sets import throne_room, light_shafts, grade, palace_exterior
from props import chest
from captions import subtitle
from render import Renderer
R = Renderer()

def finish(D, b, sub, out):
    R.frame(D.svg(f'<g filter="{D.sat(1.12)}">{b}</g>' + sub), out)

# ---------------- A: throne room wide
D = Doc(); t = 1.3
L = throne_room(D, t)
b = L["back"] + L["floor"] + L["pillars"] + L["throne"]
b += g(guard(D, {}, 1), 236, 860, s=0.62) + g(guard(D, {}, -1), 844, 860, s=0.62)
b += L["candles"]
b += g(king_seated(D, {"look": (0.15, 0.5), "brow": (10, -8), "mouth": "flat"}), 540, 702, s=0.74)
b += g(corvin(D, {"look": (0.7, -0.2), "brow": (4, 6), "mouth": "smirk", "arm": {"r": -10}}), 196, 1330, s=0.92)
b += g(bram(D, {"look": (-0.7, -0.1), "brow": (2, -6), "mouth": "frown"}), 892, 1334, s=0.92)
b += g(wren(D, {"look": (0, -0.6), "brow": (6, 0), "mouth": "talk", "lid": 0.15}), 548, 1338, s=0.9)
b += light_shafts(D, t)
bl = D.blur(9)
b += f'<g filter="{bl}">' + D.shaded(rrect(-120, -40, 190, 2000, 10), "#6d5a72", "#3d2f4f", off=(-30, 0), sw=8) + "</g>"
b += grade(D, warm=0.16, vignette=0.6)
finish(D, b, subtitle(["when", "you're", "wrong."], active=2, y=1418, size=74), "/home/claude/work/s3/A.png")

# ---------------- B: palace exterior, golden hour
D = Doc(); t = 2.0
L = palace_exterior(D, t)
b = L["sky"] + L["castle"] + L["road"]
for x, y, sc, fn, pose in ((420, 1350, 0.5, corvin, {"look": (0.6, -0.4), "arm": {"r": 40}}), (560, 1290, 0.46, bram, {"look": (0.6, -0.4)}), (690, 1222, 0.42, wren, {"look": (0.5, -0.5)})):
    b += g(fn(D, pose), x, y, s=sc)
b += L["trees"]
# foreground grass tufts + flowers along the bottom edge
import math, random
rr = random.Random(5)
for x, y, sc in ((40, 1830, 1.3), (330, 1930, 1.0), (760, 1900, 1.1), (1000, 1800, 1.3), (120, 1490, 0.55), (830, 1430, 0.5)):
    bush = ""
    for dx, dy, r in ((-80, -40, 70), (0, -80, 90), (85, -45, 72), (-30, -10, 80), (50, -10, 80)):
        bush += fill(ell(x + dx * sc, y + dy * sc, r * sc, r * sc * 0.92), "#000")
    from art import ell as _e
    d = " ".join(_e(x + dx * sc, y + dy * sc, r * sc, r * sc * 0.92) for dx, dy, r in ((-80, -40, 70), (0, -80, 90), (85, -45, 72), (-30, -10, 80), (50, -10, 80)))
    b += stroke(d, 10)
    b += D.shaded(d, "#5f9a4e", "#2f5a45", off=(-16 * sc, -10 * sc), sw=0.01, line=False, rim="#ffd27a")
    for k in range(4):
        fx, fy = x + rr.uniform(-110, 110) * sc, y + rr.uniform(-120, -20) * sc
        c = rr.choice(["#ffd25a", "#f7f2e8", "#e86a7a"])
        for a_ in range(5):
            b += fill(ell(fx + 8 * sc * math.cos(a_ * 1.256), fy + 8 * sc * math.sin(a_ * 1.256), 6.5 * sc, 6.5 * sc), c) 
        b += fill(ell(fx, fy, 4.5 * sc, 4.5 * sc), "#c4842c")
b += f'<g filter="{D.blur(2)}">' + "".join(fill(ell(x, y, 3, 3), "#fff2c8", 0.7) for x, y in ((300, 900), (420, 760), (520, 980), (220, 1100), (610, 820))) + "</g>"
b += grade(D, warm=0.2, vignette=0.5, tint="#ffb36b")
finish(D, b, subtitle(["to", "his", "palace"], active=2, y=1418, size=74), "/home/claude/work/s3/B.png")

# ---------------- C: hook - the box close-up
D = Doc(); t = 0.5
L = throne_room(D, t)
bgl = L["back"] + L["floor"] + L["pillars"] + L["throne"] + L["candles"]
b = f'<g filter="{D.blur(14)}"><g transform="translate(540,640) scale(2.3) translate(-540,-520)">{bgl}</g></g>'
b += fill(rrect(-10, -10, W + 20, H + 20, 0), "#2a1838", 0.35)
# table with velvet cloth
cloth = blob([(-60, 1180), (300, 1150), (780, 1150), (1140, 1180), (1140, 1700), (980, 1760), (760, 1700), (540, 1770), (320, 1700), (100, 1760), (-60, 1700)])
b += D.shaded(cloth, PAL["plum"], "#2c1f40", off=(0, -18), sw=6)
b += stroke(blob([(-60, 1690), (100, 1750), (320, 1690), (540, 1760), (760, 1690), (980, 1750), (1140, 1690)], close=False), 10, PAL["gold"])
# light pool from above
b += fill(ell(540, 1190, 420, 70), D.rad([(0, "#ffd99a", 0.55), (1, "#ffd99a", 0)]))
b += f'<path d="M380,-40 L700,-40 L900,1200 L180,1200Z" fill="{D.lin([(0, "#fff0c2", 0.35), (1, "#ffd27a", 0.05)])}" filter="{D.blur(24)}" style="mix-blend-mode:screen"/>'
b += g(chest(D), 540, 1220, s=1.45)
b += light_shafts(D, t, 0.4)
b += grade(D, warm=0.12, vignette=0.7)
finish(D, b, subtitle(["One", "locked", "box."], active=1, y=1418, size=84), "/home/claude/work/s3/C.png")
R.close()

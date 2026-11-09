"""Reusable character rigs. Local coords: feet at (0,0), up = -y, adult ~560-700 units tall.
Every character takes a pose dict:
  look=(x,y) pupil direction -1..1, lid=0..1 (blink / half-lidded), brow=(raise, tilt), mouth=str,
  tilt=head tilt deg, arm=dict of arm angles, bob=breathing offset.
Rig parts (head / eyes / brows / mouth / arms / body) are separate so they animate independently.
"""
from art import PAL, INK, ell, poly, rrect, blob, curve, line, stroke, fill, g, f2, mirror, rot

SW = 5.0


def P(pose, k, d):
    return pose.get(k, d) if pose else d


# ---------------------------------------------------------------- face pieces
def eyes(D, cx, cy, sep, rx, ry, pose, skin, sw=SW, specs=False):
    lx, ly = P(pose, "look", (0, 0))
    lid = P(pose, "lid", 0.0)
    s = ""
    for side in (-1, 1):
        ex = cx + side * sep / 2
        d = ell(ex, cy, rx, ry)
        s += fill(d, PAL["white"])
        px, py = ex + lx * rx * 0.42, cy + ly * ry * 0.38
        s += f'<g clip-path="{D.clip(d)}">'
        s += fill(ell(px, py, rx * 0.56, ry * 0.6), INK)
        s += fill(ell(px - rx * 0.18, py - ry * 0.22, rx * 0.16, ry * 0.15), "#ffffff")
        if lid > 0.01:  # upper lid comes down
            top = cy - ry - 2
            ly2 = top + (2 * ry + 4) * lid
            s += fill(poly([(ex - rx - 4, top - 4), (ex + rx + 4, top - 4), (ex + rx + 4, ly2), (ex - rx - 4, ly2)]), skin)
            s += stroke(line(ex - rx - 4, ly2, ex + rx + 4, ly2), sw * 0.9)
        s += "</g>"
        s += stroke(d, sw * 0.9)
    return s


def brows(cx, cy, sep, w, pose, col=INK, thick=7.0):
    raise_, tilt = P(pose, "brow", (0, 0))
    s = ""
    for side in (-1, 1):
        bx = cx + side * sep / 2
        y = cy - raise_
        inner, outer = (bx - side * w / 2, y + tilt), (bx + side * w / 2, y - tilt * 0.4)
        mid = ((inner[0] + outer[0]) / 2, (inner[1] + outer[1]) / 2 - 5)
        s += stroke(curve(inner, mid, outer), thick, col)
    return s


def mouth(cx, cy, w, kind, sw=SW, inner="#7a2b3a"):
    h = w * 0.5
    if kind == "smile":
        return stroke(curve((cx - w / 2, cy - 3), (cx, cy + h * 0.45), (cx + w / 2, cy - 3)), sw)
    if kind == "smirk":
        return stroke(curve((cx - w / 2, cy + 2), (cx + w * 0.1, cy + h * 0.25), (cx + w / 2, cy - h * 0.35)), sw)
    if kind == "flat":
        return stroke(line(cx - w * 0.4, cy, cx + w * 0.4, cy), sw)
    if kind == "frown":
        return stroke(curve((cx - w / 2, cy + h * 0.3), (cx, cy - h * 0.15), (cx + w / 2, cy + h * 0.3)), sw)
    if kind in ("open", "talk", "o", "grin"):
        if kind == "o":
            d = ell(cx, cy + 4, w * 0.22, h * 0.42)
        elif kind == "grin":
            d = blob([(cx - w / 2, cy - 4), (cx, cy - 2), (cx + w / 2, cy - 4), (cx + w * 0.25, cy + h * 0.6), (cx - w * 0.25, cy + h * 0.6)])
        else:
            hh = h * (0.75 if kind == "open" else 0.45)
            d = blob([(cx - w * 0.42, cy - 2), (cx, cy - hh * 0.15), (cx + w * 0.42, cy - 2), (cx + w * 0.2, cy + hh), (cx - w * 0.2, cy + hh)])
        return fill(d, inner) + stroke(d, sw)
    return ""


def limb(D, pts, width, lit, shade, sw=SW, cap=None):
    """Sleeve/arm as a thick smooth stroke with ink edge (ink stroke underneath, colour on top)."""
    d = curve(*pts)
    s = f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width + 2 * sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{d}" fill="none" stroke="{shade}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{d}" fill="none" stroke="{lit}" stroke-width="{width * 0.62}" stroke-linecap="round" stroke-linejoin="round" transform="translate(-3,-3)"/>'
    return s


def hand(D, x, y, r, skin, skin_d, sw=SW):
    return D.shaded(ell(x, y, r, r * 0.92), skin, skin_d, off=(r * 0.25, r * 0.2), sw=sw)


def shadow(rx, ry=None, op=0.35):
    ry = ry or rx * 0.18
    return fill(ell(0, 0, rx, ry), "#1b1030", op)


# ---------------------------------------------------------------- KING OSWIN (seated)
def king_seated(D, pose=None):
    p = pose or {}
    bob = P(p, "bob", 0)
    s = ""
    # robe (pooled on the seat), shoes
    for side in (-1, 1):
        s += D.shaded(ell(side * 46, -14, 34, 18), PAL["gold"], PAL["gold_d"], off=(4, 3))
    robe = blob([(0, -300 + bob), (82, -270 + bob), (118, -170), (150, -60), (140, -8), (60, -2), (0, -10), (-60, -2), (-140, -8), (-150, -60), (-118, -170), (-82, -270 + bob)])
    s += D.shaded(robe, PAL["crimson"], PAL["crimson_d"], off=(14, 8))
    # ermine hem + centre trim
    hem = blob([(-146, -40), (0, -52), (146, -40), (142, -6), (0, -16), (-142, -6)])
    s += D.shaded(hem, PAL["white"], PAL["white_d"], off=(6, 4))
    trim = poly([(-16, -280 + bob), (16, -280 + bob), (22, -48), (-22, -48)])
    s += D.shaded(trim, PAL["white"], PAL["white_d"], off=(4, 2))
    for (x, y) in [(-6, -240), (6, -190), (-5, -140), (7, -95), (-90, -28), (-40, -34), (40, -34), (95, -28)]:
        s += fill(poly([(x, y - 7), (x + 4, y + 3), (x - 4, y + 3)]), INK)
    # arms on the armrests
    for side in (-1, 1):
        s += limb(D, [(side * 70, -250 + bob), (side * 118, -190), (side * 150, -150)], 46, PAL["crimson"], PAL["crimson_d"])
        s += hand(D, side * 156, -146, 22, PAL["skin1"], PAL["skin1_d"])
    # ermine collar / cape shoulders
    collar = blob([(-112, -262 + bob), (-60, -300 + bob), (0, -290 + bob), (60, -300 + bob), (112, -262 + bob), (80, -236 + bob), (0, -250 + bob), (-80, -236 + bob)])
    s += D.shaded(collar, PAL["white"], PAL["white_d"], off=(6, 5))
    for x in (-80, -44, 44, 80):
        s += fill(poly([(x, -270 + bob), (x + 4, -260 + bob), (x - 4, -260 + bob)]), INK)
    s += g(king_head(D, p), 0, -360 + bob, s=1.12, r=P(p, "tilt", 0))
    return s


def king_head(D, p):
    sk, skd = PAL["skin1"], PAL["skin1_d"]
    s = ""
    head = blob([(0, -78), (56, -58), (70, 0), (58, 52), (0, 70), (-58, 52), (-70, 0), (-56, -58)])
    s += D.shaded(head, sk, skd, off=(9, 6))
    # ears
    for side in (-1, 1):
        s += D.shaded(ell(side * 70, 6, 13, 18), sk, skd, off=(3, 2))
    s += eyes(D, 0, -4, 54, 15, 16, p, sk)
    s += brows(0, -34, 58, 40, p, col=INK, thick=17)
    s += brows(0, -34, 58, 40, p, col="#f1edf4", thick=10)
    # beard (big white cloud) with moustache and mouth peeking
    beard = blob([(-60, 20), (-30, 34), (0, 30), (30, 34), (60, 20), (70, 70), (52, 120), (20, 150), (-20, 150), (-52, 120), (-70, 70)])
    s += D.shaded(beard, PAL["white"], PAL["white_d"], off=(9, 7))
    for x, y in ((-30, 80), (10, 100), (-8, 125), (30, 70)):
        s += stroke(curve((x - 10, y), (x, y + 8), (x + 10, y)), 3, "#a99fb5")
    s += g(mouth(0, 52, 30, P(p, "mouth", "flat"), sw=4.5), 0, 0)
    stache = blob([(0, 26), (30, 22), (56, 40), (30, 44), (0, 36), (-30, 44), (-56, 40), (-30, 22)])
    s += D.shaded(stache, PAL["white"], PAL["white_d"], off=(4, 3))
    nose = blob([(0, 0), (16, 14), (14, 30), (0, 34), (-14, 30), (-16, 14)])
    s += D.shaded(nose, "#f0b597", "#cf8b7a", off=(4, 3), sw=4.5)
    # crown
    crown = poly([(-60, -52), (-66, -112), (-40, -84), (-20, -128), (0, -92), (20, -128), (40, -84), (66, -112), (60, -52)])
    s += D.shaded(crown, PAL["gold"], PAL["gold_d"], off=(7, 4))
    band = rrect(-64, -66, 128, 22, 8)
    s += D.shaded(band, "#f7cd62", PAL["gold_d"], off=(4, 2))
    for x, c in ((-34, "#c8343f"), (0, "#2aa5a0"), (34, "#c8343f")):
        s += D.shaded(ell(x, -55, 8, 8), c, INK, off=(2, 2), sw=3)
    for x, y in ((-66, -112), (-20, -128), (20, -128), (66, -112)):
        s += D.shaded(ell(x, y, 7, 7), "#fff1b8", PAL["gold_d"], off=(2, 2), sw=3)
    return s


# ---------------------------------------------------------------- CORVIN the Scholar
def corvin(D, pose=None):
    p = pose or {}
    bob = P(p, "bob", 0)
    sk, skd = PAL["skin1"], PAL["skin1_d"]
    s = shadow(110)
    for side in (-1, 1):  # pointed slippers
        s += D.shaded(blob([(side * 18, -14), (side * 64, -8), (side * 74, -2), (side * 20, 0)]), "#5b2a4a", "#3b1a33", off=(4, 3))
    robe = blob([(0, -420 + bob), (52, -410 + bob), (68, -330), (84, -150), (98, -16), (0, -8), (-98, -16), (-84, -150), (-68, -330), (-52, -410 + bob)])
    s += D.shaded(robe, PAL["navy"], PAL["navy_d"], off=(14, 6), rim="#8fa6ff")
    s += D.shaded(poly([(-10, -400 + bob), (10, -400 + bob), (16, -14), (-16, -14)]), PAL["gold"], PAL["gold_d"], off=(3, 2), sw=4)
    s += D.shaded(blob([(-98, -36), (0, -30), (98, -36), (98, -14), (0, -8), (-98, -14)]), PAL["gold"], PAL["gold_d"], off=(3, 2), sw=4)
    for x, y in ((-48, -250), (44, -190), (-40, -120), (50, -320)):  # embroidered stars
        st = poly([(x + 9 * __import__("math").cos(a * 3.14159 / 5 - 1.5708) * (1 if i % 2 == 0 else 0.45),
                    y + 9 * __import__("math").sin(a * 3.14159 / 5 - 1.5708) * (1 if i % 2 == 0 else 0.45)) for i, a in enumerate(range(10))])
        s += fill(st, PAL["gold"], 0.9)
    # left arm holds a big book against the chest
    s += limb(D, [(-50, -392 + bob), (-74, -300), (-30, -255)], 40, PAL["navy"], PAL["navy_d"])
    book = poly([(-70, -340), (20, -352), (26, -250), (-64, -238)])
    s += D.shaded(book, "#b03a35", "#7c2430", off=(6, 4))
    s += D.shaded(poly([(-58, -334), (14, -344), (18, -334), (-56, -324)]), PAL["gold"], PAL["gold_d"], off=(2, 1), sw=3)
    s += hand(D, -24, -262, 19, sk, skd)
    # right arm: raised lecturing finger (angle from pose)
    a = P(p, "arm", {}).get("r", -60)
    ex, ey = rot(52 + 70, -392 + bob, a, 52, -392 + bob)
    hx, hy = rot(ex + 60, ey, a - 40, ex, ey)
    s += limb(D, [(50, -392 + bob), (ex, ey), (hx, hy)], 38, PAL["navy"], PAL["navy_d"])
    s += hand(D, hx, hy, 18, sk, skd)
    s += limb(D, [(hx + 2, hy - 12), (hx + 4, hy - 34)], 9, sk, skd, sw=3.5)
    # neck + head
    s += D.shaded(rrect(-18, -440 + bob, 36, 40, 10), sk, skd, off=(4, 2))
    s += g(corvin_head(D, p), 0, -500 + bob, s=1.12, r=P(p, "tilt", 0))
    return s


def corvin_head(D, p):
    sk, skd = PAL["skin1"], PAL["skin1_d"]
    s = ""
    head = blob([(0, -78), (48, -62), (58, 0), (44, 58), (0, 80), (-44, 58), (-58, 0), (-48, -62)])
    s += D.shaded(head, sk, skd, off=(8, 6))
    for side in (-1, 1):
        s += D.shaded(ell(side * 58, 4, 10, 16), sk, skd, off=(3, 2))
    s += eyes(D, 0, -6, 46, 14, 15, p, sk)
    # round spectacles
    for side in (-1, 1):
        s += stroke(ell(side * 22, -6, 19, 19), 4.5, "#3a2a1a")
        s += fill(ell(side * 22 - 6, -14, 6, 4), "#ffffff", 0.6)
    s += stroke(line(-4, -8, 4, -8), 4.5, "#3a2a1a")
    s += brows(0, -36, 46, 30, p, thick=6)
    nose = blob([(0, -4), (9, 10), (16, 32), (4, 38), (-9, 33), (-6, 12)])
    s += D.shaded(nose, sk, skd, off=(4, 3), sw=4.5)
    s += mouth(4, 54, 26, P(p, "mouth", "smirk"), sw=4.5)
    goatee = blob([(-14, 66), (14, 66), (6, 104), (0, 112), (-6, 104)])
    s += D.shaded(goatee, "#a9a6b8", "#77738a", off=(3, 2), sw=4)
    # tall scholar hat with gold band and tassel
    hat = poly([(-50, -60), (-42, -168), (42, -178), (50, -60)])
    s += D.shaded(hat, PAL["navy"], PAL["navy_d"], off=(8, 4))
    s += D.shaded(rrect(-62, -74, 124, 22, 10), PAL["navy_d"], "#161c40", off=(4, 2))
    s += D.shaded(poly([(-46, -112), (46, -118), (46, -98), (-46, -94)]), PAL["gold"], PAL["gold_d"], off=(3, 2), sw=4)
    s += stroke(curve((40, -176), (66, -150), (70, -110)), 4, PAL["gold_d"])
    s += D.shaded(ell(70, -104, 8, 12), PAL["gold"], PAL["gold_d"], off=(2, 2), sw=3.5)
    return s


# ---------------------------------------------------------------- BRAM the Inventor
def bram(D, pose=None):
    p = pose or {}
    bob = P(p, "bob", 0)
    sk, skd = PAL["skin2"], PAL["skin2_d"]
    s = shadow(120)
    for side in (-1, 1):
        s += D.shaded(rrect(side * 44 - 26, -90, 52, 76, 14), "#5b4a5a", "#3c2f40", off=(5, 3))  # trousers
        s += D.shaded(blob([(side * 44 - 30, -26), (side * 44 + 30, -26), (side * 44 + 40, -2), (side * 44 - 34, 0)]), "#3b2a26", "#24181a", off=(4, 2))  # boots
    torso = blob([(0, -330 + bob), (78, -312 + bob), (118, -230), (112, -120), (86, -80), (0, -72), (-86, -80), (-112, -120), (-118, -230), (-78, -312 + bob)])
    s += D.shaded(torso, PAL["mustard"], PAL["mustard_d"], off=(12, 8))
    apron = blob([(-64, -250 + bob), (64, -250 + bob), (84, -150), (80, -66), (0, -58), (-80, -66), (-84, -150)])
    s += D.shaded(apron, PAL["brown"], PAL["brown_d"], off=(10, 6))
    s += stroke(curve((-60, -250 + bob), (0, -300 + bob), (60, -250 + bob)), 6, PAL["brown_d"])
    s += D.shaded(rrect(-34, -170, 68, 44, 8), PAL["brown_d"], "#4c3224", off=(4, 3), sw=4)  # pocket
    s += D.shaded(rrect(-6, -200, 10, 50, 4), "#9aa3ad", "#6a7280", off=(2, 1), sw=3.5)  # wrench handle
    s += D.shaded(ell(-1, -204, 13, 11), "#9aa3ad", "#6a7280", off=(2, 1), sw=3.5)
    # belt
    s += D.shaded(rrect(-110, -110, 220, 22, 8), "#4a3230", "#2e1f1f", off=(3, 2))
    s += D.shaded(rrect(-14, -114, 28, 30, 5), PAL["gold"], PAL["gold_d"], off=(2, 2), sw=4)
    # arms: left resting fist on hip, right carries a hammer on the shoulder
    s += limb(D, [(-92, -290 + bob), (-140, -210), (-104, -150)], 46, PAL["mustard"], PAL["mustard_d"])
    s += hand(D, -102, -146, 24, sk, skd)
    ra = P(p, "arm", {}).get("r", 0)
    hx, hy = rot(118, -330, ra, 92, -290)
    s += limb(D, [(92, -290 + bob), (150, -250), (hx, hy)], 46, PAL["mustard"], PAL["mustard_d"])
    hammer = g(D.shaded(rrect(-6, -10, 12, 150, 5), "#a0723f", "#77502c", off=(2, 1), sw=4)
               + D.shaded(rrect(-36, -40, 72, 34, 6), "#8d96a3", "#5f6675", off=(4, 3), sw=4.5), hx, hy, r=-35 + ra)
    s += hammer
    s += hand(D, hx, hy, 24, sk, skd)
    s += g(bram_head(D, p), 0, -380 + bob, s=1.1, r=P(p, "tilt", 0))
    return s


def bram_head(D, p):
    sk, skd = PAL["skin2"], PAL["skin2_d"]
    hair = "#9a4426"
    s = ""
    for side in (-1, 1):  # side tufts behind
        s += D.shaded(blob([(side * 58, -40), (side * 84, -20), (side * 82, 20), (side * 60, 24)]), hair, "#6f2c19", off=(4, 3))
    head = blob([(0, -72), (60, -56), (76, 0), (62, 50), (0, 66), (-62, 50), (-76, 0), (-60, -56)])
    s += D.shaded(head, sk, skd, off=(9, 7))
    for side in (-1, 1):
        s += D.shaded(ell(side * 76, 6, 12, 17), sk, skd, off=(3, 2))
    s += eyes(D, 0, -4, 52, 15, 15, p, sk)
    s += brows(0, -28, 52, 34, p, col=hair, thick=10)
    nose = blob([(0, -2), (20, 14), (18, 32), (0, 36), (-18, 32), (-20, 14)])
    s += D.shaded(nose, "#ef9c7c", "#c46c5c", off=(5, 3), sw=4.5)
    s += mouth(0, 52, 32, P(p, "mouth", "grin"), sw=4.5)
    stache = blob([(0, 32), (40, 24), (74, 40), (56, 50), (0, 44), (-56, 50), (-74, 40), (-40, 24)])
    s += D.shaded(stache, hair, "#6f2c19", off=(5, 4))
    # goggles on the forehead
    s += D.shaded(rrect(-72, -64, 144, 16, 6), "#4a3230", "#2e1f1f", off=(2, 2), sw=4)
    for side in (-1, 1):
        s += D.shaded(ell(side * 26, -58, 24, 20), "#c98d3a", "#8f5d22", off=(4, 3), sw=4.5)
        s += D.shaded(ell(side * 26, -58, 15, 12), "#7fd0d6", "#3e8d9b", off=(3, 2), sw=3.5)
        s += fill(ell(side * 26 - 5, -63, 5, 3), "#ffffff", 0.8)
    return s


# ---------------------------------------------------------------- WREN the Shepherd
def wren(D, pose=None):
    p = pose or {}
    bob = P(p, "bob", 0)
    sk, skd = PAL["skin3"], PAL["skin3_d"]
    s = shadow(90)
    # crook (behind the body on his left)
    s += stroke(curve((-92, -2), (-96, -300), (-94, -560), (-80, -610), (-46, -612), (-36, -580)), 16, INK)
    s += stroke(curve((-92, -2), (-96, -300), (-94, -560), (-80, -610), (-46, -612), (-36, -580)), 8, "#b07f45")
    # cloak behind
    cloak = blob([(-58, -380 + bob), (58, -380 + bob), (92, -200), (98, -40), (0, -60), (-98, -40), (-92, -200)])
    s += D.shaded(cloak, PAL["brown"], PAL["brown_d"], off=(10, 6))
    s += D.shaded(rrect(50, -170, 34, 40, 4), "#b98b5c", "#8c6448", off=(3, 2), sw=3.5)  # patch
    for i in range(4):
        s += stroke(line(54 + i * 8, -176, 54 + i * 8, -164), 2.5)
    for side in (-1, 1):  # legs + boots
        s += D.shaded(rrect(side * 22 - 15, -130, 30, 118, 12), "#cdb68f", "#a08a6a", off=(4, 2))
        s += D.shaded(blob([(side * 22 - 20, -26), (side * 22 + 22, -26), (side * 22 + 30, -2), (side * 22 - 22, 0)]), PAL["brown_d"], "#3f2a1f", off=(3, 2))
    tunic = blob([(0, -372 + bob), (50, -360 + bob), (62, -250), (72, -118), (0, -106), (-72, -118), (-62, -250), (-50, -360 + bob)])
    s += D.shaded(tunic, PAL["sage"], PAL["sage_d"], off=(10, 6))
    s += stroke(curve((-64, -200), (0, -190), (64, -200)), 9, "#a07a4f")  # rope belt
    s += stroke(curve((-10, -196), (-14, -160), (-6, -140)), 6, "#a07a4f")
    # arms: left holds the crook, right relaxed (or lifting from pose)
    s += limb(D, [(-44, -348 + bob), (-76, -280), (-92, -240)], 30, PAL["sage"], PAL["sage_d"])
    s += hand(D, -94, -236, 17, sk, skd)
    ra = P(p, "arm", {}).get("r", 0)
    hx, hy = rot(66, -190, ra, 44, -348)
    s += limb(D, [(44, -348 + bob), (64, -270), (hx, hy)], 30, PAL["sage"], PAL["sage_d"])
    s += hand(D, hx, hy, 17, sk, skd)
    # cloak clasp + collar
    s += D.shaded(blob([(-48, -376 + bob), (0, -350 + bob), (48, -376 + bob), (30, -390 + bob), (-30, -390 + bob)]), PAL["brown"], PAL["brown_d"], off=(4, 3))
    s += D.shaded(ell(0, -360 + bob, 9, 9), "#d9c27a", "#a8904a", off=(2, 2), sw=3.5)
    s += g(wren_head(D, p), 0, -440 + bob, s=1.12, r=P(p, "tilt", 0))
    return s


def wren_head(D, p):
    sk, skd = PAL["skin3"], PAL["skin3_d"]
    hair, hair_d = "#d39a4e", "#a3702f"
    s = ""
    back = blob([(-58, -30), (-44, -66), (0, -80), (44, -66), (60, -30), (58, 10), (-58, 10)])
    s += D.shaded(back, hair, hair_d, off=(5, 4))
    head = blob([(0, -64), (48, -52), (58, 0), (46, 50), (0, 66), (-46, 50), (-58, 0), (-48, -52)])
    s += D.shaded(head, sk, skd, off=(8, 6))
    for side in (-1, 1):
        s += D.shaded(ell(side * 58, 6, 10, 15), sk, skd, off=(3, 2))
    s += eyes(D, 0, 0, 46, 14, 15, {**p, "lid": P(p, "lid", 0.22)}, sk)
    s += brows(0, -24, 46, 26, p, col=hair_d, thick=6)
    nose = blob([(0, 6), (10, 22), (0, 28), (-8, 22)])
    s += D.shaded(nose, sk, skd, off=(3, 2), sw=4)
    s += mouth(0, 44, 26, P(p, "mouth", "smile"), sw=4.5)
    # messy fringe tufts on top
    fr = blob([(-56, -24), (-50, -60), (-20, -78), (14, -82), (46, -64), (58, -30), (36, -40), (24, -26), (8, -44), (-10, -30), (-28, -46), (-40, -28)])
    s += D.shaded(fr, hair, hair_d, off=(5, 4))
    return s


# ---------------------------------------------------------------- background guard
def guard(D, pose=None, flip=1):
    p = pose or {}
    s = shadow(60)
    sk, skd = PAL["skin1"], PAL["skin1_d"]
    sx = 52 * flip
    s += stroke(line(sx, 0, sx, -560), 12, INK) + stroke(line(sx, 0, sx, -560), 5, "#8a6440")
    s += D.shaded(poly([(sx - 14, -560), (sx, -600), (sx + 14, -560)]), "#c9ced8", "#8e95a6", off=(3, 2), sw=4)
    for side in (-1, 1):
        s += D.shaded(rrect(side * 18 - 13, -120, 26, 110, 8), "#3d3a55", "#2a2740", off=(3, 2))
        s += D.shaded(rrect(side * 18 - 16, -24, 34, 24, 8), "#2c2333", "#1b1520", off=(2, 1))
    body = blob([(0, -330), (44, -320), (56, -200), (58, -110), (0, -100), (-58, -110), (-56, -200), (-44, -320)])
    s += D.shaded(body, PAL["teal"], PAL["teal_d"], off=(8, 5))
    s += D.shaded(poly([(-20, -320), (20, -320), (24, -110), (-24, -110)]), PAL["gold"], PAL["gold_d"], off=(3, 2), sw=4)
    s += limb(D, [(36 * flip, -300), (sx, -230)], 26, PAL["teal"], PAL["teal_d"])
    s += hand(D, sx, -226, 14, sk, skd)
    s += limb(D, [(-36 * flip, -300), (-50 * flip, -200)], 26, PAL["teal"], PAL["teal_d"])
    head = ell(0, -380, 44, 48)
    s += D.shaded(head, sk, skd, off=(6, 4))
    s += eyes(D, 0, -376, 32, 8, 9, {"look": (0, 0), "lid": 0.2}, sk)
    s += stroke(line(-10, -350, 10, -350), 4)
    helm = blob([(-50, -380), (-46, -420), (0, -440), (46, -420), (50, -380), (0, -392)])
    s += D.shaded(helm, "#c9ced8", "#8e95a6", off=(5, 3))
    s += D.shaded(poly([(-4, -440), (4, -440), (2, -470), (-2, -470)]), PAL["crimson"], PAL["crimson_d"], off=(2, 1), sw=3.5)
    return s

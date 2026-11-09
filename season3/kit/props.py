"""Reusable props. Local coords: bottom-centre at (0,0)."""
import math
from art import PAL, INK, ell, poly, rrect, blob, curve, line, stroke, fill, g, f2


def chest(D, lid=0.0, shackle_open=False, glow=0.0, sw=5.0):
    """Wooden chest with iron bands and a padlock on the hasp.
    lid: 0 closed .. 1 open (lid swings up/back). shackle_open: the padlock was never closed (the twist)."""
    s = fill(ell(0, 4, 190, 22), "#1b1030", 0.35)
    wood, wood_d = "#a5683f", "#6e3f2a"
    iron, iron_d = "#6d6a82", "#3f3b55"
    # inner glow when the lid opens (the diamond)
    if lid > 0.02:
        gl = D.rad([(0, "#e6fbff", 0.95 * lid), (0.4, "#9be8ff", 0.5 * lid), (1, "#9be8ff", 0)])
        s += fill(ell(0, -200, 260, 220 * (0.5 + lid)), gl)
    body = rrect(-170, -190, 340, 190, 18)
    s += D.shaded(body, wood, wood_d, off=(16, 10), sw=sw)
    for yy in (-150, -100, -50):  # planks
        s += stroke(line(-160, yy, 160, yy), 3, "#5a2f20", 0.6)
    for x in (-120, 120):  # iron bands
        s += D.shaded(rrect(x - 16, -190, 32, 190, 4), iron, iron_d, off=(4, 3), sw=sw * 0.9)
        for yy in (-170, -100, -30):
            s += D.shaded(ell(x, yy, 5, 5), "#c9c6da", iron_d, off=(1, 1), sw=2.5)
    # lid (rotates about the back hinge as it opens)
    ang = -100 * lid
    lidd = "M-176,0 L-176,-60 Q-176,-120 0,-130 Q176,-120 176,-60 L176,0Z"
    lid_g = D.shaded(lidd, "#b5754a", wood_d, off=(16, 8), sw=sw)
    for x in (-120, 120):
        lid_g += D.shaded(f"M{x-16},0 L{x-16},-110 Q{x},-114 {x+16},-110 L{x+16},0Z", iron, iron_d, off=(4, 3), sw=sw * 0.9)
    # hasp plate hanging from the lid front
    lid_g += D.shaded(rrect(-22, -24, 44, 64, 8), iron, iron_d, off=(3, 2), sw=sw * 0.9)
    if lid < 0.02:
        s += g(lid_g, 0, -190)
    else:
        s += g(g(lid_g, 0, 0, s=1, r=0), 0, -190, extra=f'transform="translate(0,-190) scale(1,{max(0.15, math.cos(math.radians(-ang)) ):.3f})"')
    # padlock (on the body staple, under the hasp)
    if lid < 0.02:
        px, py = 0, -150
        if shackle_open:
            sh = f"M{px-18},{py-14} L{px-18},{py-46} Q{px-18},{py-74} {px+6},{py-74} Q{px+30},{py-74} {px+30},{py-46} L{px+30},{py-30}"
        else:
            sh = f"M{px-18},{py-14} L{px-18},{py-46} Q{px-18},{py-70} {px},{py-70} Q{px+18},{py-70} {px+18},{py-46} L{px+18},{py-14}"
        s += f'<path d="{sh}" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
        s += f'<path d="{sh}" fill="none" stroke="#c9c6da" stroke-width="8" stroke-linecap="round"/>'
        lock = rrect(px - 34, py - 18, 68, 62, 12)
        s += D.shaded(lock, PAL["gold"], PAL["gold_d"], off=(6, 4), sw=sw)
        s += fill(ell(px, py + 8, 7, 8), INK) + fill(poly([(px - 3, py + 10), (px + 3, py + 10), (px + 5, py + 28), (px - 5, py + 28)]), INK)
    return s


def diamond(D, x, y, r, t=0.0):
    s = fill(ell(x, y, r * 2.4, r * 2.4), D.rad([(0, "#ffffff", 0.9), (0.3, "#aef0ff", 0.5), (1, "#aef0ff", 0)]))
    d = poly([(x - r, y - r * 0.3), (x - r * 0.5, y - r * 0.8), (x + r * 0.5, y - r * 0.8), (x + r, y - r * 0.3), (x, y + r)])
    s += D.shaded(d, "#cdf6ff", "#5fbcd8", off=(r * 0.2, r * 0.1), sw=4)
    s += stroke(f"M{x-r},{y-r*0.3} L{x+r},{y-r*0.3} M{x-r*0.5},{y-r*0.8} L{x-r*0.2},{y-r*0.3} L{x},{y+r} L{x+r*0.2},{y-r*0.3} L{x+r*0.5},{y-r*0.8}", 2.5, "#3a7a95")
    for k in range(4):  # sparkle
        a = t * 2 + k * 1.57
        sx, sy = x + math.cos(a) * r * 1.6, y + math.sin(a) * r * 1.2
        sz = 6 + 4 * math.sin(t * 5 + k)
        s += fill(poly([(sx, sy - sz), (sx + sz * 0.25, sy), (sx, sy + sz), (sx - sz * 0.25, sy)]), "#ffffff", 0.9)
    return s

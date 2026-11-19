# HIW10 — "Find the C in 5 seconds" challenge -> why it's hard. Casual, no studies, "So," loop.
# Sources (fact-checked 2026-11-19):
#  - ScienceDaily / Bielefeld University (2014): only the fovea sees precisely, a sharp zone "about the size of a thumb
#    nail at the end of an outstretched arm"; the brain predicts/fills in the blurry periphery from experience.
#  - SR Research eye-tracking glossary: people make "around 3 saccades each second" (fixations ~200-300 ms).
#  - Visual crowding (standard vision science): similar letters in peripheral vision blur together, so C ~ O.
#  - The "genius" line is a playful hook and is walked back on screen ("NOT AN IQ TEST").
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import skia
from engine import *

D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
HI = "#FFD23F"; FOUND = "#FF5A5F"; EYE = "#6FD3FF"; GREEN = "#1fb98a"; CREAM = "#F4F2EE"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


CW = kw(0); GENIUS = kw(1); COUNT = [p0(i) for i in range(2, 7)]; THERE = p0(7); WHILE = p0(8); SMART = kw(10)
SHARP = p0(11); THUMB = kw(12); ELSE = p0(13); BLURRY = kw(14); JUMP = p0(15); THREE = kw(16)
INBLUR = p0(17); SAME = kw(18); GUESS = p0(19); MORE = p0(20)
WIPE1 = p0(21) - 0.3; TRICK = p0(21); ROW = kw(22); READ = p0(23); SO = p0(24)
WL = 0.32
IMPACTS = [THERE, BLURRY]
SHIFTS = [P[i]["t0"] for i in range(1, len(P))]

COLS, ROWS, CWD, CHT = 11, 14, 72, 59
GX0, GY0 = 490 - COLS * CWD / 2, 590
CR, CC = 9, 7
GR = 19
LET_FONT = skia.Font(TF_BOLD, 70)


def glyph(c, x, y, r, is_c, colr, a, w=None):
    w = w or r * 0.36
    if is_c:
        c.drawArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), 28, 304, False, paint(colr, a, stroke=w))
    else:
        c.drawCircle(x, y, r, paint(colr, a, stroke=w))


def cell(r, c):
    return GX0 + c * CWD + CWD / 2, GY0 + r * CHT + CHT / 2


CX, CY = cell(CR, CC)


def loopwave(t, k=1):
    return math.sin(2 * math.pi * k * t / DUR)


def panel(c, light, a=1.0):
    r = skia.Rect.MakeLTRB(GX0 - 34, GY0 - 34, GX0 + COLS * CWD + 34, GY0 + ROWS * CHT + 34)
    c.drawRoundRect(r.makeOffset(0, 12), 40, 40, paint("#000000", (0.12 if light else 0.4) * a, blur=24))
    if light:
        c.drawRoundRect(r, 40, 40, paint(shader=linear((0, r.top()), (0, r.bottom()), [col("#ffffff", a), col("#f1eee8", a)])))
        c.drawRoundRect(r, 40, 40, paint("#d9d4cb", a, stroke=2))
    else:
        c.drawRoundRect(r, 40, 40, paint(shader=linear((0, r.top()), (0, r.bottom()), [col("#232127", a), col("#18171b", a)])))
        c.drawRoundRect(r, 40, 40, paint("#ffffff", 0.10 * a, stroke=2))


def letters(c, t, light, a=1.0, dim=0.0, c_as_o=False, rowhi=None):
    fg = INK if light else CREAM
    for r in range(ROWS):
        for k in range(COLS):
            x, y = cell(r, k)
            ch = "C" if (r, k) == (CR, CC) and not c_as_o else "O"
            al = a
            if dim > 0 and (r, k) != (CR, CC):
                al *= 1 - 0.75 * dim
            if rowhi is not None:
                al *= 1.0 if r <= rowhi + 0.5 else 0.35
            glyph(c, x, y, GR, ch == "C", fg, al)


def grid(c, t, light, a=1.0, dim=0.0, c_as_o=False, rowhi=None):
    panel(c, light, a)
    letters(c, t, light, a, dim, c_as_o, rowhi)


def blurred_grid(c, t, sigma, spot=None, spot_r=95, c_as_o=False, light=False):
    panel(c, light)
    bp = skia.Paint(); bp.setImageFilter(skia.ImageFilters.Blur(sigma, sigma))
    c.saveLayer(None, bp); letters(c, t, light, 1.0, c_as_o=c_as_o); c.restore()
    if spot is not None:
        sx, sy = spot
        c.save(); pth = skia.Path(); pth.addCircle(sx, sy, spot_r); c.clipPath(pth, doAntiAlias=True)
        panel(c, light); letters(c, t, light)
        c.restore()
        c.drawCircle(sx, sy, spot_r, paint(EYE, 0.9, stroke=4))
        c.drawCircle(sx, sy, spot_r + 14, paint(EYE, 0.25, stroke=10, blur=6))


def timer_bar(c, t, a):
    if a <= 0: return
    x0, x1, y = 120, 860, 1438
    c.drawRoundRect(skia.Rect.MakeLTRB(x0, y - 7, x1, y + 7), 7, 7, paint("#ffffff", 0.15 * a))
    left = 1 - prog(t, COUNT[0], (COUNT[4] + 0.7) - COUNT[0])
    colr = mixhex(GREEN, FOUND, 1 - left)
    c.drawRoundRect(skia.Rect.MakeLTRB(x0, y - 7, x0 + (x1 - x0) * left, y + 7), 7, 7, paint(colr, a))


# ---------------- scenes ----------------
def hook_scene(c, t):
    studio_dark(c)
    c.save(); c.translate(0, 6 * loopwave(t))
    grid(c, t, False)
    c.restore()


def scene_challenge(c, t):
    studio_dark(c)
    c.save(); c.translate(0, 6 * loopwave(t))
    # count punches
    s = 1.0
    for ts in COUNT:
        d = t - ts
        if 0 <= d < 0.3:
            s += 0.015 * (1 - d / 0.3) ** 2
    c.translate(490, 1000); c.scale(s, s); c.translate(-490, -1000)
    grid(c, t, False)
    c.restore()
    timer_bar(c, t, eout(prog(t, GENIUS + 0.2, 0.4)))
    pill(c, t, "5 SECONDS", 490, 528, HI, GENIUS + 0.1, COUNT[0] - 0.1)
    for i, ts in enumerate(COUNT):
        pill(c, t, str(5 - i), 490, 528, mixhex(GREEN, FOUND, i / 4), ts, (COUNT[i + 1] if i < 4 else THERE) - 0.05, text_col="#FFFFFF")


def scene_found(c, t):
    studio_dark(c)
    z = eio(prog(t, THERE, 0.45)) * (1 - eio(prog(t, WHILE - 0.1, 0.45)))
    dim = eout(prog(t, THERE, 0.3)) * (1 - prog(t, SMART - 0.2, 0.4))
    c.save(); c.translate(lerp(CX, 490, z), lerp(CY, 1010, z)); c.scale(1 + 0.6 * z, 1 + 0.6 * z); c.translate(-CX, -CY)
    grid(c, t, False, 1.0, dim)
    ring = eout(prog(t, THERE + 0.05, 0.35))
    if ring > 0:
        rr = skia.Rect.MakeXYWH(CX - 36, CY - 36, 72, 72)
        pp = paint(FOUND, 1 - 0.6 * prog(t, SMART, 0.4), stroke=8)
        te = skia.TrimPathEffect.Make(0, ring) if ring < 0.999 else None
        if te: pp.setPathEffect(te)
        pth = skia.Path(); pth.addOval(rr); c.drawPath(pth, pp)
        c.drawCircle(CX, CY, 48, paint(FOUND, 0.25 * ring * (1 - prog(t, SMART, 0.4)), blur=14))
    c.restore()
    pill(c, t, "FOUND IT!", 490, 528, FOUND, THERE + 0.1, WHILE - 0.05)
    pill(c, t, "TOOK A WHILE?", 490, 528, "#FFFFFF", WHILE, SMART - 0.1)
    pill(c, t, "NOT AN IQ TEST", 490, 528, GREEN, SMART, SHARP - 0.1, text_col="#FFFFFF")


def wander(t):
    return 330 + 260 * math.sin(t * 0.9), 900 + 260 * math.sin(t * 0.63 + 1.0)


rnd = random.Random(10)
JUMPS = [(rnd.randrange(COLS), rnd.randrange(ROWS)) for _ in range(40)]


def saccade_pos(t):
    k = int((t - JUMP) * 3)
    a = cell(*JUMPS[k % 40][::-1]); b = cell(*JUMPS[(k + 1) % 40][::-1])
    u = ((t - JUMP) * 3) % 1
    q = eout(clamp(u / 0.15))       # quick jump, then hold (fixation)
    prev = a
    return lerp(a[0], b[0], q), lerp(a[1], b[1], q), prev, b, u


def scene_spot(c, t):
    studio_dark(c)
    sig = lerp(0, 7, eout(prog(t, SHARP, 0.5))) + lerp(0, 7, eout(prog(t, BLURRY - 0.1, 0.4)))
    if t < JUMP:
        sx, sy = wander(t)
        r = 95 * eout(prog(t, SHARP + 0.1, 0.5))
        blurred_grid(c, t, max(sig, 0.01), (sx, sy) if r > 1 else None, max(r * 0.8, 1))
        pill(c, t, "SHARP SPOT", 490, 528, EYE, SHARP + 0.2, THUMB - 0.1)
        pill(c, t, "= A THUMBNAIL", 490, 528, EYE, THUMB, ELSE - 0.1)
        pill(c, t, "BLURRY", 490, 528, "#9aa0ad", BLURRY, JUMP - 0.1, text_col="#FFFFFF")
        if t > THUMB - 0.1:
            th = eback(prog(t, THUMB - 0.1, 0.35)) * (1 - prog(t, ELSE, 0.3))
            if th > 0:      # little thumb icon beside the spot
                c.save(); c.translate(sx + 150, sy - 40); c.scale(th, th)
                c.drawRoundRect(skia.Rect.MakeLTRB(-34, -70, 34, 70), 34, 34, paint(shader=linear((-34, 0), (34, 0), [col("#F3C6A2"), col("#B97F59")])))
                c.drawRoundRect(skia.Rect.MakeLTRB(-24, -62, 24, -10), 18, 18, paint("#fde6d6"))
                c.restore()
        return
    sx, sy, a, b, u = saccade_pos(t)
    blurred_grid(c, t, sig, (sx, sy), 76)
    # saccade trail
    if u < 0.4:
        c.drawLine(a[0], a[1], sx, sy, paint(EYE, 0.6 * (1 - u / 0.4), stroke=6))
    pill(c, t, "JUMP", 490, 528, EYE, JUMP + 0.1, THREE - 0.1)
    pill(c, t, "3 JUMPS / SECOND", 490, 528, EYE, THREE, INBLUR - 0.1)


def scene_same(c, t):
    studio_dark(c)
    bl = eio(prog(t, INBLUR + 0.7, 1.4))
    sig = 0.01 + 16 * bl
    f = skia.Font(TF_BOLD, 330)
    for i, (ch, x) in enumerate((("C", 300), ("O", 690))):
        pa = eback(prog(t, INBLUR - 0.05 + i * 0.12, 0.35))
        c.save(); c.translate(x, 1000); c.scale(pa, pa)
        c.drawRoundRect(skia.Rect.MakeLTRB(-170, -210, 170, 210), 40, 40, paint("#232127"))
        c.drawRoundRect(skia.Rect.MakeLTRB(-170, -210, 170, 210), 40, 40, paint("#ffffff", 0.1, stroke=2))
        bp = skia.Paint(); bp.setImageFilter(skia.ImageFilters.Blur(sig, sig))
        c.saveLayer(None, bp)
        glyph(c, 0, 0, 120, ch == "C", CREAM, 1.0, 44)
        c.restore()
        c.restore()
    if t > SAME - 0.1:
        ea = eback(prog(t, SAME - 0.1, 0.3))
        big_number(c, "=", "", 495, 1060, 160, HI, clamp(ea), pulse=ea)
    pill(c, t, "SAME BLOB", 490, 1340, HI, SAME, GUESS - 0.1)


def scene_guess(c, t):
    studio_dark(c)
    blurred_grid(c, t, 12, None, c_as_o=False)
    ga = eout(prog(t, GUESS + 0.3, 0.4))
    if ga > 0:      # brain "fills in": sharp O's pop over the blur, the C gets covered too
        for r in range(ROWS):
            for k in range(COLS):
                d = ((r * 7 + k * 3) % 11) / 11 * 0.8
                pa = eback(prog(t, GUESS + 0.3 + d, 0.25))
                if pa <= 0: continue
                x, y = cell(r, k)
                c.save(); c.translate(x, y); c.scale(pa, pa)
                glyph(c, 0, 0, GR, False, CREAM if (r, k) != (CR, CC) else HI, 0.9)
                c.restore()
    pill(c, t, "BRAIN GUESSES", 490, 528, "#FFFFFF", GUESS + 0.2, MORE - 0.05)
    pill(c, t, "\"MORE O'S\"", 490, 528, HI, MORE, WIPE1 + 0.1)


def scene_white(c, t):
    studio_white(c)
    rowp = prog(t, ROW - 0.1, (SO - 0.2) - (ROW - 0.1))
    rowhi = None
    if t > ROW - 0.1:
        rowpos = min(CR + (CC + 0.5) / COLS, rowp * (CR + 0.999) * 1.25)
        rowhi = rowpos
    grid(c, t, True, 1.0, 0, rowhi=rowhi if rowhi is not None else (ROWS if t < ROW - 0.1 else 0))
    if rowhi is not None:
        r = int(rowhi); u = rowhi - r
        x0 = GX0 + 10; x1 = GX0 + COLS * CWD - 10
        y = GY0 + r * CHT + CHT / 2
        xh = lerp(x0, x1, u)
        c.drawRoundRect(skia.Rect.MakeLTRB(x0 - 10, y - 27, xh + 10, y + 27), 14, 14, paint(HI, 0.35))
        # scanning eye dot
        c.drawCircle(xh, y, 16, paint(EYE, 0.9))
    TF = ROW - 0.1 + ((CR + (CC + 0.5) / COLS) / ((CR + 0.999) * 1.25)) * ((SO - 0.2) - (ROW - 0.1))
    if rowhi is not None and t > TF:
        found = eout(prog(t, TF, 0.35))
        c.drawCircle(CX, CY, 34, paint(GREEN, found, stroke=6))
        if t > TF + 0.2:
            ck = eback(prog(t, TF + 0.2, 0.35))
            c.save(); c.translate(CX + 50, CY - 50); c.scale(ck * 0.8, ck * 0.8)
            c.drawCircle(0, 0, 34, paint(GREEN))
            cp = skia.Path(); cp.moveTo(-15, 1); cp.lineTo(-4, 12); cp.lineTo(16, -10)
            c.drawPath(cp, paint("#ffffff", 1, stroke=7))
            c.restore()
    pill(c, t, "THE TRICK", 490, 528, "#141313", TRICK, ROW - 0.05, text_col="#FFFFFF")
    pill(c, t, "ROW BY ROW", 490, 528, GREEN, ROW, SO + 0.4, text_col="#FFFFFF")


def draw_world(c, t):
    if t < COUNT[0] - 0.05:
        scene_challenge(c, t) if t > GENIUS else hook_scene(c, t); return
    if t < THERE:
        scene_challenge(c, t); return
    if t < SHARP:
        scene_found(c, t); return
    if t < INBLUR - 0.1:
        scene_spot(c, t); return
    if t < GUESS - 0.1:
        scene_same(c, t); return
    if t < WIPE1 + WL / 2:
        scene_guess(c, t); return
    if t < SO - 0.05:
        scene_white(c, t); return
    q = eio(prog(t, SO - 0.05, DUR - SO))
    hook_scene(c, t)
    if q < 1:
        c.saveLayerAlpha(None, int(255 * (1 - q))); scene_white(c, t); c.restore()


def cut_punch(t):
    s = 1.0
    for ts in SHIFTS:
        if ts in COUNT[1:]:
            continue
        d = t - ts
        if 0 <= d < 0.25:
            s += 0.02 * (1 - d / 0.25) ** 2
    return s


KWCOL = {"C": HI, "genius": HI, "Five": GREEN, "four": GREEN, "three...": HI, "two": FOUND, "one": FOUND,
         "There": FOUND, "smart": GREEN, "thumbnail": EYE, "blur": "#9aa0ad", "three": EYE, "same": HI,
         "guesses": "#FFFFFF", "yep,": "#FFFFFF", "row": GREEN}
CAPS = Captions(P, KWCOL, {"genius.", "There"}, DUR)


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
    light = WIPE1 + WL / 2 <= t < SO - 0.05 + (DUR - SO) * 0.5
    vignette(c, light)
    if not light:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 560), paint(shader=linear((0, 0), (0, 560), [col("#000000", 0.35), col("#000000", 0)])))
    CAPS.draw(c, t, light)
    wipe(c, t, WIPE1, WL, GREEN, "#F4F2EE")
    grain(c, t, D)
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    ev = [("whoosh", 0.2), ("pop", CW), ("riser", GENIUS - 0.3), ("pop", GENIUS + 0.1),
          ("hit", THERE), ("pop", WHILE), ("pop", SMART), ("whoosh", SHARP), ("pop", THUMB), ("hit", BLURRY),
          ("pop", THREE), ("whoosh", INBLUR - 0.1), ("pop", SAME), ("whoosh", GUESS - 0.1), ("pop", MORE),
          ("whoosh", WIPE1), ("paper", WIPE1 + 0.12), ("pop", ROW), ("ding", ROW - 0.1 + ((CR + (CC + 0.5) / COLS) / ((CR + 0.999) * 1.25)) * ((SO - 0.2) - (ROW - 0.1)) + 0.2), ("whoosh", SO - 0.05)]
    for ts in COUNT:
        ev.append(("tick", ts))
    k = 0
    while JUMP + k / 3 < INBLUR - 0.2:
        ev.append(("tick", JUMP + k / 3)); k += 1
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

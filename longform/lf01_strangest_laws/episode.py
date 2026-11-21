# LF01 — "The 10 Strangest Laws Still on the Books" — 16:9 long-form test clip (intro + #10 teaser).
# Fact (checked 2026-11-21, Wikipedia "Chewing gum sales ban in Singapore"): importing and selling chewing gum has been
# illegal in Singapore since 3 Jan 1992; chewing itself is legal; since 2004 therapeutic/dental/nicotine gum can be
# bought from a doctor or registered pharmacist (footnote on screen).
import math, sys, os, json, subprocess, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "howitworks"))
import skia
import engine as E
from engine import (paint, col, linear, radial, prog, eout, eio, eback, window, lerp, clamp, mixhex,
                    TF_BLACK, TF_BOLD, TF_REG, TF_MONO, INK, RED)

W, H, FPS = 1920, 1080, 30
D = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(f"{D}/timings.json"))
P = T["phrases"]; DUR = round(T["duration"], 3)
GOLD = "#E8B54A"; PAPER = "#F3E9D2"; NAVY = "#101626"; GUM = "#FF7BB0"; SG = "#E5484D"


def p0(i): return P[i]["t0"]


def kw(i, n=0):
    ks = [w for w in P[i]["words"] if w["kw"]]
    return (ks[n] if ks else P[i]["words"][0])["t0"]


MADE = kw(0); REAL = kw(1); TEN = p0(2); SING = kw(3); GUMT = kw(4); BAN = p0(5); YEAR = kw(5)
IMPACTS = [REAL, TEN, YEAR]
rnd = random.Random(3)
DUSTL = [(rnd.random() * W, rnd.random() * H, rnd.uniform(1, 3), rnd.random() * 6.28) for _ in range(40)]


def text_c(c, s, x, y, font, colr, a=1.0, track=0.0):
    w = sum(font.measureText(ch) + track for ch in s) - track
    xx = x - w / 2
    for ch in s:
        c.drawString(ch, xx, y, font, paint(colr, a))
        xx += font.measureText(ch) + track
    return w


def bg_dark(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.45, 1300, [col("#1b2440"), col(NAVY), col("#070a12")], [0, 0.6, 1])))
    for (x, y, r, ph) in DUSTL:
        xx = (x + t * 14) % W; yy = (y - t * 8 + 20 * math.sin(t * 0.5 + ph)) % H
        c.drawCircle(xx, yy, r, paint("#ffffff", 0.12 * (0.6 + 0.4 * math.sin(t * 2 + ph)), blur=1.5))


def law_book(c, x, y, s, t, a=1.0, open_=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-330, 200, 330, 250), 30, 30, paint("#000000", 0.45 * a, blur=24))
    if open_ < 0.5:
        # closed leather book with gold lettering
        c.drawRoundRect(skia.Rect.MakeLTRB(-260, -220, 260, 220), 16, 16, paint(shader=linear((0, -220), (0, 220), [col("#7a2a22", a), col("#4e1712", a)])))
        c.drawRoundRect(skia.Rect.MakeLTRB(-260, -220, -215, 220), 10, 10, paint("#3a100c", a))
        c.drawRoundRect(skia.Rect.MakeLTRB(-200, -180, 230, 180), 10, 10, paint(GOLD, 0.8 * a, stroke=4))
        f = skia.Font(TF_BLACK, 54)
        text_c(c, "LAWS", 15, -10, f, GOLD, a, 10)
        text_c(c, "VOL. X", 15, 60, skia.Font(TF_BOLD, 26), GOLD, 0.8 * a, 6)
    else:
        for sx in (-1, 1):
            pg = skia.Path(); pg.moveTo(0, -200); pg.cubicTo(sx * 120, -230, sx * 250, -210, sx * 300, -200)
            pg.lineTo(sx * 300, 210); pg.cubicTo(sx * 250, 200, sx * 120, 220, 0, 230); pg.close()
            c.drawPath(pg, paint(shader=linear((0, -200), (0, 230), [col("#fbf4e2", a), col("#e9dcc0", a)])))
            for k in range(12):
                yy = -150 + k * 28
                c.drawLine(sx * 40, yy, sx * (260 - (k % 3) * 30), yy, paint("#8a7a5a", 0.45 * a, stroke=4))
        c.drawLine(0, -200, 0, 230, paint("#c9b88f", a, stroke=3))
    c.restore()


def gavel(c, x, y, s, ang, a=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-14, -10, 14, 300), 12, 12, paint(shader=linear((-14, 0), (14, 0), [col("#a8683a", a), col("#5e3418", a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(-110, -70, 110, 10), 24, 24, paint(shader=linear((0, -70), (0, 10), [col("#b97644", a), col("#6b3a1a", a)])))
    for xx in (-80, 80):
        c.drawRect(skia.Rect.MakeLTRB(xx - 8, -72, xx + 8, 12), paint(GOLD, a))
    c.restore()


def stamp(c, txt, x, y, size, colr, a, sc, rot=-8):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    f = skia.Font(TF_BLACK, size)
    w = f.measureText(txt) + size * 0.8
    r = skia.Rect.MakeLTRB(-w / 2, -size * 0.85, w / 2, size * 0.45)
    c.drawRoundRect(r, 14, 14, paint(colr, a, stroke=8))
    text_c(c, txt, 0, size * 0.1, f, colr, a)
    c.restore()


def skyline(c, t, a):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=linear((0, 0), (0, H), [col("#1d2a4d", a), col("#c4566a", a), col("#f2a65a", a)], [0, 0.65, 1])))
    c.drawCircle(1450, 690, 120, paint("#ffd7a0", 0.6 * a, blur=30))
    r = random.Random(5)
    x = 0
    while x < W:
        w = r.uniform(60, 150); h = r.uniform(180, 460)
        c.drawRect(skia.Rect.MakeLTRB(x, 820 - h, x + w - 6, 830), paint("#14182a", a))
        for wy in range(int(820 - h + 20), 800, 34):
            for wx in range(int(x + 12), int(x + w - 20), 26):
                if r.random() < 0.35:
                    c.drawRect(skia.Rect.MakeLTRB(wx, wy, wx + 10, wy + 14), paint("#ffe3a0", 0.5 * a))
        x += w
    # three-tower hotel-like silhouette (generic)
    for k in range(3):
        c.drawRect(skia.Rect.MakeLTRB(760 + k * 140, 380, 860 + k * 140, 830), paint("#0e1120", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(730, 350, 1190, 395), 22, 22, paint("#0e1120", a))
    c.drawRect(skia.Rect.MakeLTRB(0, 830, W, H), paint(shader=linear((0, 830), (0, H), [col("#2b3557", a), col("#0b0f1d", a)])))
    for k in range(8):
        c.drawLine(0, 860 + k * 28, W, 860 + k * 28, paint("#ffd7a0", 0.05 * a, stroke=3))


def gum_pack(c, x, y, s, a, t):
    c.save(); c.translate(x, y); c.rotate(-6 + 3 * math.sin(t * 2)); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-190, -90, 210, 110), 22, 22, paint("#000000", 0.4 * a, blur=18))
    c.drawRoundRect(skia.Rect.MakeLTRB(-200, -100, 200, 100), 22, 22, paint(shader=linear((0, -100), (0, 100), [col("#ff9cc4", a), col(GUM, a), col("#d94f8a", a)])))
    c.drawRoundRect(skia.Rect.MakeLTRB(-200, -30, 200, 30), 0, 0, paint("#ffffff", 0.9 * a))
    text_c(c, "GUM", 0, 18, skia.Font(TF_BLACK, 52), "#d94f8a", a, 14)
    for k in range(3):
        c.drawRoundRect(skia.Rect.MakeLTRB(-150 + k * 110, 130, -70 + k * 110, 160), 15, 15, paint("#ffd0e2", a))
    c.restore()


def no_sign(c, x, y, r, a, sc):
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.drawCircle(0, 0, r, paint(RED, 0.3 * a, stroke=50, blur=12))
    c.drawCircle(0, 0, r, paint(RED, a, stroke=30))
    c.save(); c.rotate(-45); c.drawLine(-r, 0, r, 0, paint(RED, a, stroke=30)); c.restore()
    c.restore()


def pill(c, t, txt, x, y, colr, tin, tout, txtcol=INK):
    if t < tin or t > tout + 0.25: return
    a = 1 - prog(t, tout, 0.2); sc = eback(prog(t, tin, 0.25))
    f = skia.Font(TF_MONO, 34)
    w = sum(f.measureText(ch) + 3 for ch in txt) + 50
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.drawRoundRect(skia.Rect.MakeLTRB(-w / 2, -32, w / 2, 32), 32, 32, paint(colr, a))
    text_c(c, txt, 0, 12, f, txtcol, a, 3)
    c.restore()


def subtitles(c, t):
    for i, ph in enumerate(P):
        nxt = P[i + 1]["t0"] if i + 1 < len(P) else DUR
        if not (ph["t0"] - 0.05 <= t < nxt):
            continue
        a = prog(t, ph["t0"], 0.12) * (1 - prog(t, nxt - 0.12, 0.12))
        f = skia.Font(TF_BOLD, 50)
        words = ph["words"]
        tw = sum(f.measureText(w["w"]) for w in words) + f.measureText(" ") * (len(words) - 1)
        x = W / 2 - tw / 2; y = 1000
        c.drawRoundRect(skia.Rect.MakeLTRB(x - 28, y - 52, x + tw + 28, y + 20), 18, 18, paint("#000000", 0.45 * a))
        for w in words:
            on = t >= w["t0"]
            colr = GOLD if w["kw"] else "#FFFFFF"
            c.drawString(w["w"], x, y, f, paint(colr, a * (1.0 if on else 0.35)))
            x += f.measureText(w["w"] + " ")


def draw_world(c, t):
    if t < TEN - 0.15:
        bg_dark(c, t)
        push = 1 + 0.04 * t
        c.save(); c.translate(W / 2, H / 2); c.scale(push, push); c.translate(-W / 2, -H / 2)
        op = prog(t, MADE - 0.2, 0.01)
        law_book(c, 960, 520, 1.0 * eback(prog(t, 0.0, 0.5)), t, 1.0, op)
        # title
        ta = eout(prog(t, 0.15, 0.5))
        text_c(c, "THE 10 STRANGEST LAWS", 960, 150 - 30 * (1 - ta), skia.Font(TF_BLACK, 92), "#FFFFFF", ta, 4)
        text_c(c, "STILL ON THE BOOKS", 960, 225, skia.Font(TF_BOLD, 46), GOLD, eout(prog(t, 0.45, 0.4)), 14)
        # gavel slams on "real"
        g = prog(t, REAL - 0.35, 0.35)
        ang = lerp(-50, 8, eio(g)) if t < REAL else 8 - 6 * math.exp(-(t - REAL) * 8) * math.cos((t - REAL) * 30)
        gavel(c, 1430, 420, 1.1, ang, eout(prog(t, REAL - 0.6, 0.25)))
        if t > REAL:
            ring = prog(t, REAL, 0.5)
            c.drawCircle(1340, 560, 60 + 260 * ring, paint(GOLD, 0.6 * (1 - ring), stroke=6))
        stamp(c, "REAL", 620, 700, 80, RED, prog(t, REAL, 0.05), 1 + 0.6 * (1 - eout(prog(t, REAL, 0.2))))
        c.restore()
        return
    if t < SING - 0.15:
        bg_dark(c, t)
        u = prog(t, TEN - 0.15, 0.3)
        sc = 1.8 - 0.8 * eout(u)
        c.save(); c.translate(960, 560); c.scale(sc, sc)
        c.drawCircle(0, -40, 300, paint(GOLD, 0.12 * u, blur=40))
        text_c(c, "#10", 0, 60, skia.Font(TF_BLACK, 330), GOLD, u)
        c.restore()
        return
    skyline(c, t, 1.0)
    pill(c, t, "SINGAPORE", 960, 150, SG, SING, DUR, "#FFFFFF")
    ga = eback(prog(t, GUMT - 0.25, 0.4))
    if ga > 0:
        gum_pack(c, 960, 560, 1.2 * clamp(ga, 0, 1.2), clamp(ga), t)
        no_sign(c, 960, 560, 300, prog(t, GUMT + 0.25, 0.1), eback(prog(t, GUMT + 0.25, 0.3)))
    stamp(c, "BANNED SINCE 1992", 1460, 820, 58, "#FFFFFF", prog(t, YEAR, 0.05), 1 + 0.5 * (1 - eout(prog(t, YEAR, 0.2))), -6)
    fa = prog(t, YEAR + 0.3, 0.4)
    if fa > 0:
        c.drawString("Selling & importing gum is illegal. Medical gum from pharmacists is allowed (since 2004).",
                     60, 1050, skia.Font(TF_REG, 24), paint("#FFFFFF", 0.55 * fa))


def frame(t):
    surf = skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = surf.getCanvas()
    sx = sy = 0
    for ti in IMPACTS:
        d = t - ti
        if 0 <= d < 0.3:
            amp = 10 * (1 - d / 0.3); sx += amp * math.sin(d * 97); sy += amp * math.cos(d * 83)
    c.save(); c.translate(sx, sy)
    draw_world(c, t)
    c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H / 2, 1200, [col("#000000", 0), col("#000000", 0.45)], [0.55, 1])))
    subtitles(c, t)
    fade = min(prog(t, 0, 0.3), 1 - prog(t, DUR - 0.4, 0.4))
    if fade < 1:
        c.drawRect(skia.Rect.MakeWH(W, H), paint("#000000", 1 - fade))
    return surf.makeImageSnapshot().toarray()


def sfx_events():
    return sorted([("riser", 0.0), ("whoosh", 0.2), ("pop", MADE), ("whoosh", REAL - 0.35), ("hit", REAL),
                   ("whoosh", TEN - 0.15), ("hit", TEN), ("whoosh", SING - 0.15), ("pop", SING), ("pop", GUMT),
                   ("hit", GUMT + 0.25), ("hit", YEAR)], key=lambda e: e[1])


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

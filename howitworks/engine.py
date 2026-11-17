"""Shared drawing engine: fonts, easing, pills, HUD, captions, wipes, post."""
import math, random, json
import skia

W, H, FPS = 1080, 1920, 30
# Platform safe area (TikTok / Instagram Reels / YouTube Shorts on 1080x1920), owner direction 2026-11-17:
#   top tabs/header end ~y 300 · right action column (avatar/follow, like, comment, save, share) x > 920 from y ~700 down
#   bottom username / description / sound / Subscribe from y ~1440. Keep ALL text and key subjects inside.
SAFE_TOP, SAFE_BOTTOM, SAFE_LEFT, SAFE_RIGHT = 300, 1440, 60, 920
import os
A = os.environ.get("HIW_ASSETS", "/home/claude/hiw_assets").rstrip("/") + "/"
FONT = "/usr/share/fonts/opentype/inter/"
TF_BOLD = skia.Typeface.MakeFromFile(FONT + "InterDisplay-Bold.otf")
TF_BLACK = skia.Typeface.MakeFromFile(FONT + "InterDisplay-Black.otf")
TF_REG = skia.Typeface.MakeFromFile(FONT + "Inter-Regular.otf")
TF_MONO = skia.Typeface.MakeFromFile(A + "jbm/fonts/ttf/JetBrainsMono-Bold.ttf")
TF_MONO_M = skia.Typeface.MakeFromFile(A + "jbm/fonts/ttf/JetBrainsMono-Medium.ttf")
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)

INK = "#141313"; WHITE = "#FFFFFF"
YELLOW = "#FFD23F"; MINT = "#3EE6A8"; RED = "#FF3B30"
MINT_INK = "#0C9A68"; YELLOW_INK = "#B8860B"


def hexc(h, a=1.0):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return skia.Color4f(r, g, b, a)


def col(h, a=1.0):
    return hexc(h, a).toColor()


def mixhex(h1, h2, x):
    a = [int(h1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(h2[i:i + 2], 16) for i in (1, 3, 5)]
    x = max(0, min(1, x))
    return "#" + "".join(f"{int(p + (q - p) * x):02x}" for p, q in zip(a, b))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, a, d):
    return clamp((t - a) / d) if d > 0 else float(t >= a)


def eio(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def eout(x):
    return 1 - (1 - x) ** 3


def ein(x):
    return x ** 3


def eexpo(x):
    return 1 if x >= 1 else 1 - 2 ** (-10 * x)


def eback(x, s=1.4):
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def lerp(a, b, x):
    return a + (b - a) * x


def window(t, a, b, fi=0.25, fo=0.25):
    return prog(t, a, fi) * (1 - prog(t, b - fo, fo))


def paint(c=None, a=1.0, stroke=None, shader=None, blur=None):
    p = skia.Paint(AntiAlias=True)
    if c is not None:
        p.setColor4f(hexc(c, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
    if shader is not None:
        p.setShader(shader)
        p.setAlphaf(a)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def radial(cx, cy, r, cols, pos=None):
    return skia.GradientShader.MakeRadial(skia.Point(cx, cy), max(r, 0.1), cols, pos)


def linear(p1, p2, cols, pos=None):
    return skia.GradientShader.MakeLinear([skia.Point(*p1), skia.Point(*p2)], cols, pos)


def studio_dark(c):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.55, 1250, [col("#1A1819"), col("#0B0A0B")])))
    c.drawOval(skia.Rect.MakeXYWH(-200, 1330, W + 400, 520), paint(shader=radial(W / 2, 1590, 700, [col("#2a2829", 0.55), col("#141313", 0)])))


def studio_white(c):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H * 0.45, 1300, [col("#F7F5F1"), col("#E4E1DB")])))


# ---------------- pills / labels ----------------
PILL_FONT = skia.Font(TF_MONO, 28)


def pill(c, t, txt, x, y, color, tin, tout, anchor=None, light=False, outline=False, text_col=None):
    if t < tin or t > tout + 0.25:
        return
    pin = eback(prog(t, tin, 0.22))
    aout = 1 - prog(t, tout, 0.2)
    if aout <= 0:
        return
    f = PILL_FONT
    track = 2.2
    tw = sum(f.measureText(ch) + track for ch in txt) - track
    w, h = tw + 36, 50
    lc = INK if light else "#FFFFFF"
    if anchor:
        lp = eout(prog(t, tin + 0.05, 0.16))
        ax, ay = anchor
        p = skia.Path(); p.moveTo(x, y); p.lineTo(lerp(x, ax, lp), lerp(y, ay, lp))
        c.drawPath(p, paint(lc, 0.7 * aout, stroke=1.6))
        c.drawCircle(lerp(x, ax, lp), lerp(y, ay, lp), 4.5 * lp, paint(lc, 0.95 * aout))
    c.save(); c.translate(x, y); c.scale(pin, pin)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 2, -h / 2 + 6, w, h), h / 2, h / 2), paint("#000000", 0.22 * aout, blur=8))
    if outline:
        c.drawRRect(rr, paint(INK if light else "#141313", 0.85 * aout))
        c.drawRRect(rr, paint(color, aout, stroke=3))
        tc = color
    else:
        c.drawRRect(rr, paint(color, aout))
        tc = INK if color in (YELLOW, MINT, "#FFFFFF", "#F4F2EE", "#E9E4DA") else "#FFFFFF"
    if text_col:
        tc = text_col
    xx = -tw / 2
    for ch in txt:
        c.drawString(ch, xx, 10, f, paint(tc, aout))
        xx += f.measureText(ch) + track
    c.restore()


def footnote(c, t, text, tin, tout, light=False):
    a = window(t, tin, tout, 0.3, 0.3)
    if a <= 0:
        return
    c.drawString(text, 64, 1400, skia.Font(TF_REG, 22), paint(INK if light else "#FFFFFF", 0.5 * a))


def hud(c, t, label, value, dot_col, a, light=False):
    if a <= 0:
        return
    f1 = skia.Font(TF_MONO_M, 22); f2 = skia.Font(TF_MONO, 32)
    x, y = 64, 500
    fg = INK if light else "#FFFFFF"
    w = max(f1.measureText(label) + 40, f2.measureText(value) + 64)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, 92), 16, 16)
    c.drawRRect(rr, paint(fg, 0.07 * a)); c.drawRRect(rr, paint(fg, 0.22 * a, stroke=1.5))
    c.drawString(label, x + 22, y + 34, f1, paint(fg, 0.6 * a))
    c.drawCircle(x + 32, y + 66, 8, paint(dot_col, a))
    c.drawCircle(x + 32, y + 66, 14, paint(dot_col, 0.25 * a * (0.5 + 0.5 * math.sin(t * 6))))
    c.drawString(value, x + 52, y + 77, f2, paint(fg, a))


def big_number(c, txt, unit, x, y, size, color, a, pulse=1.0):
    fb = skia.Font(TF_BLACK, size); fu = skia.Font(TF_BOLD, size * 0.38)
    w1 = fb.measureText(txt); w2 = fu.measureText(unit) + 14 if unit else 0
    c.save(); c.translate(x, y - size * 0.35); c.scale(pulse, pulse); c.translate(-x, -(y - size * 0.35))
    x0 = x - (w1 + w2) / 2
    c.drawString(txt, x0, y, fb, paint(color, a))
    if unit:
        c.drawString(unit, x0 + w1 + 14, y, fu, paint(color, a * 0.8))
    c.restore()


# ---------------- captions ----------------
CAP_FONT = skia.Font(TF_BOLD, 68)
CAP_FONT.setEdging(skia.Font.Edging.kSubpixelAntiAlias)
SPACE = CAP_FONT.measureText(" ")


class Captions:
    def __init__(self, phrases, kwcol, emph, dur):
        self.P = phrases; self.kwcol = kwcol; self.emph = emph; self.dur = dur
        self.layouts = [self.layout(p) for p in phrases]

    def layout(self, ph):
        words = ph["words"]
        lines, cur = [], []
        for w in words:
            trial = cur + [w]
            wid = sum(CAP_FONT.measureText(x["w"]) for x in trial) + SPACE * (len(trial) - 1)
            if cur and (len(trial) > 5 or wid > 800):
                lines.append(cur); cur = [w]
            else:
                cur = trial
        lines.append(cur)
        out = []
        y0 = 400 if len(lines) == 1 else 362
        for li, ln in enumerate(lines):
            wid = sum(CAP_FONT.measureText(x["w"]) for x in ln) + SPACE * (len(ln) - 1)
            x = 495 - wid / 2
            for w in ln:
                ww = CAP_FONT.measureText(w["w"])
                out.append(dict(w=w, x=x, y=y0 + li * 84, ww=ww, line=li))
                x += ww + SPACE
        # keyword groups: consecutive kw words on same line
        groups, g = [], None
        for i, o in enumerate(out):
            if o["w"]["kw"] and g is not None and out[i - 1]["w"]["kw"] and out[i - 1]["line"] == o["line"]:
                g.append(i)
            elif o["w"]["kw"]:
                g = [i]; groups.append(g)
            else:
                g = None
        for gi, g in enumerate(groups):
            key = " ".join(out[i]["w"]["w"] for i in g)
            for i in g:
                out[i]["group"] = (gi, key)
        return dict(words=out, groups=groups)

    def color_for(self, key):
        for k, v in self.kwcol.items():
            if k in key:
                return v
        return "#FFFFFF"

    def draw(self, c, t, light):
        fg = INK if light else WHITE
        P = self.P
        for i, ph in enumerate(P):
            nxt = P[i + 1]["t0"] if i + 1 < len(P) else self.dur + 5
            if t < ph["t0"] - 0.05 or t > nxt + 0.05:
                continue
            exit_a = 1 - prog(t, nxt - 0.12, 0.16)
            exit_blur = 6 * prog(t, nxt - 0.12, 0.16)
            if i == len(P) - 1:
                exit_a = 1 - prog(t, self.dur - 0.45, 0.3)
            L = self.layouts[i]
            words = L["words"]
            # keyword boxes (behind text)
            for g in L["groups"]:
                first = words[g[0]]
                t0 = first["w"]["t0"]
                if t < t0:
                    continue
                shown = [words[j] for j in g if t >= words[j]["w"]["t0"]]
                key = " ".join(words[j]["w"]["w"] for j in g)
                kc = self.color_for(key)
                neutral = kc == "#FFFFFF"
                bc = (INK if light else "#FFFFFF") if neutral else kc
                bp = eout(prog(t, t0 + 0.06, 0.18))
                a = exit_a
                pad = 8
                x0 = shown[0]["x"]; x1 = shown[-1]["x"] + shown[-1]["ww"]
                y = first["y"]
                rect = skia.Rect.MakeLTRB(x0 - pad, y - 58 - pad + 6, x1 + pad, y + 14 + pad - 4)
                if bp > 0 and a > 0:
                    c.drawRect(rect, paint(bc, (0.12 if neutral else (0.18 if not light else 0.22)) * bp * a))
                    path = skia.Path(); path.addRect(rect)
                    pp = paint(bc, a, stroke=2)
                    if bp < 0.999:
                        te = skia.TrimPathEffect.Make(0, bp)
                        if te is not None:
                            pp.setPathEffect(te)
                    c.drawPath(path, pp)
                    hs = eback(prog(t, t0 + 0.18, 0.2))
                    if hs > 0:
                        for hx, hy in ((rect.left(), rect.top()), (rect.right(), rect.top()), (rect.left(), rect.bottom()), (rect.right(), rect.bottom())):
                            c.drawCircle(hx, hy, 6.5 * hs, paint("#FFFFFF", a))
                            c.drawCircle(hx, hy, 6.5 * hs, paint(bc, a, stroke=2))
            for j, o in enumerate(words):
                w = o["w"]
                if t < w["t0"]:
                    continue
                e = eout(prog(t, w["t0"], 0.14))
                nt = ph["words"][j + 1]["t0"] if j + 1 < len(ph["words"]) else 1e9
                dim = 1 - 0.55 * prog(t, nt, 0.2)
                a = e * exit_a
                if a <= 0.01:
                    continue
                blur = 8 * (1 - e) + exit_blur
                dy = 10 * (1 - e)
                sc = 1.0
                if w["w"].strip(".,?") in self.emph:
                    sc = 1 + 0.08 * math.sin(math.pi * prog(t, w["t0"], 0.3))
                x, y, ww = o["x"], o["y"], o["ww"]
                c.save()
                c.translate(x + ww / 2, y - 24 + dy); c.scale(sc, sc); c.translate(-(x + ww / 2), -(y - 24))
                if "group" in o:
                    kc = self.color_for(o["group"][1])
                    if kc == "#FFFFFF":
                        tcol = fg
                    elif light:
                        tcol = {YELLOW: YELLOW_INK, MINT: MINT_INK}.get(kc, kc)
                    else:
                        tcol = kc
                    pt = paint(tcol, a, blur=blur if blur > 0.3 else None)
                else:
                    pt = paint(fg, a * dim, blur=blur if blur > 0.3 else None)
                if not light:
                    c.drawString(w["w"], x, y + 3, CAP_FONT, paint("#000000", 0.4 * a, blur=10))
                c.drawString(w["w"], x, y, CAP_FONT, pt)
                c.restore()


# ---------------- post ----------------
rnd = random.Random(3)
DUST = [(rnd.random() * W, rnd.random() * H, rnd.random() * 2.5 + 1.5, rnd.random() * 6.28, rnd.random() * 6.28) for _ in range(16)]


def dust(c, t, light):
    for (x, y, r, p1, p2) in DUST:
        xx = (x + 30 * math.sin(t * 0.21 + p1) + t * 6) % W
        yy = (y + 40 * math.sin(t * 0.17 + p2) - t * 9) % H
        c.drawCircle(xx, yy, r, paint(INK if light else "#ffffff", (0.10 if light else 0.15) * (0.6 + 0.4 * math.sin(t + p1)), blur=1.2))


def wipe(c, t, t0, dur, accent, second):
    p = (t - t0) / dur
    if p <= 0 or p >= 1.6:
        return
    for colr, delay in ((accent, 0), (second, 0.18)):
        q = eio(clamp((p - delay) / 1.0))
        if q <= 0 or q >= 1:
            continue
        c.save(); c.translate(W / 2, H / 2); c.rotate(20)
        x = lerp(-3200, 3200, q)
        c.drawRect(skia.Rect.MakeXYWH(x - 900, -2400, 1800, 4800), paint(colr))
        c.restore()


def vignette(c, light):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(shader=radial(W / 2, H / 2, 1150, [col("#000000", 0), col("#000000", 0.12 if light else 0.45)], [0.55, 1])))


GRAIN = None


def grain(c, t, path):
    global GRAIN
    if GRAIN is None:
        GRAIN = [skia.Image.open(f"{path}/grain{i}.png") for i in range(4)]
    gp = skia.Paint(); gp.setBlendMode(skia.BlendMode.kOverlay); gp.setAlphaf(0.10)
    c.drawImage(GRAIN[int(t * FPS) % 4], 0, 0, SAMP, gp)

"""PAPER-CUTOUT kit for HOW DOES IT WORK? Shorts (owner-approved look, 2026-11-23).

Real photo props as white-bordered paper stickers, crumpled-paper colour backgrounds that change on every line,
torn-paper wipes, stop-motion jitter (15 poses/s), camera punch on every scene, shakes on big hits, paper labels,
stamps, sunburst rays, photo-paper water, music + lots of sound effects.

Usage from an episode file (see episodes/p01_onions/episode.py, the reference):
    from paperkit import *
    K = Kit(starts=[...voice segment start times...], dur=..., palette=[...indices...])
    def scene(c, t, s): ...   # draw one frame; s = Frame helper (beat, tq, jitter...)
    K.run(scene, sys.argv)    # 'stills t1,t2' | 'video' | 'mix' | 'all'
"""
import os, sys, math, random, json, subprocess, io
import numpy as np, skia
from PIL import Image, ImageFilter, ImageOps
from scipy import ndimage as nd

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, 'library'); TEX = os.path.join(HERE, 'textures'); SFX = os.path.join(HERE, 'sfx'); MUS = os.path.join(HERE, 'music')
CACHE = os.path.join(HERE, '.cache'); os.makedirs(CACHE, exist_ok=True)
W, H, FPS = 1080, 1920, 30
FONT = skia.Typeface.MakeFromFile(os.path.join(HERE, 'fonts', 'Poppins-Bold.ttf'))
YEL = (1, .86, .15); RED = (.93, .20, .22); BLK = (.07, .07, .1); WHT = (1, 1, 1)
# background colours (crumpled paper is tinted with these)
PALETTE = {'blue': (0.10, 0.36, 1.00), 'purple': (0.52, 0.22, 0.98), 'pink': (1.00, 0.22, 0.52), 'orange': (1.00, 0.62, 0.08),
           'mint': (0.08, 0.80, 0.55), 'navy': (0.10, 0.10, 0.28), 'red': (0.95, 0.20, 0.22), 'teal': (0.05, 0.74, 0.68),
           'yellow': (1.0, 0.80, 0.10), 'coral': (0.99, 0.45, 0.40)}

# ---------------- easing ----------------
def clamp(x, a=0, b=1): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a))
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x, s=1.7): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
def lerp(a, b, t): return a + (b - a) * t
def off(p, dx, dy): q = skia.Path(p); q.offset(dx, dy); return q
def _img(arr): return skia.Image.fromarray(np.ascontiguousarray(arr))

# ---------------- encoder (skia surfaces are BGRA here) ----------------
class Enc:
    def __init__(s, out, crf=16):
        pf = 'bgra' if skia.Surface(2, 2).imageInfo().colorType() == skia.ColorType.kBGRA_8888_ColorType else 'rgba'
        s.out = out
        s.p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', pf, '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                '-c:v', 'libx264', '-preset', 'medium', '-crf', str(crf), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out + '.tmp.mp4'], stdin=subprocess.PIPE)
    def write(s, surf): s.p.stdin.write(surf.makeImageSnapshot().tobytes())
    def close(s): s.p.stdin.close(); assert s.p.wait() == 0; os.replace(s.out + '.tmp.mp4', s.out)

# ---------------- backgrounds ----------------
def paper_bg(col, seed=0):
    key = os.path.join(CACHE, f'bg_{"_".join(f"{c:.2f}" for c in col)}_{seed}.png')
    if not os.path.exists(key):
        src = Image.open(os.path.join(TEX, 'crumpled_paper.jpg')).convert('L')
        im = src.rotate(90 if seed % 2 == 0 else -90, expand=True)
        if seed % 3 == 1: im = ImageOps.mirror(im)
        sc = max(W / im.width, H / im.height) * (1.0 + 0.12 * (seed % 3))
        im = im.resize((round(im.width * sc) + 2, round(im.height * sc) + 2), Image.LANCZOS)
        ox = (im.width - W) // 2 + (seed * 37) % 40; oy = (im.height - H) // 2; im = im.crop((ox, oy, ox + W, oy + H))
        a = np.asarray(im).astype(np.float32) / 255; low = nd.gaussian_filter(a, 120); a = a - low + low.mean()
        t = (a - a.mean()) / (a.std() + 1e-6)
        Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
        vig = 1 - 0.22 * (((X - W / 2) / (W * 0.75)) ** 2 + ((Y - H * 0.45) / (H * 0.7)) ** 2)
        key_l = 1 + 0.14 * np.exp(-(((X - W * 0.25) / (W * 0.9)) ** 2 + ((Y - H * 0.18) / (H * 0.6)) ** 2))
        dark = sum(col) < 0.8
        m = (1 + (0.16 if dark else 0.10) * np.clip(t, -3, 3)) * vig * key_l
        img = np.stack([m * c for c in col], -1)
        if dark: img = img + 0.03 * np.clip(t, 0, 3)[..., None]
        Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).save(key)
    arr = np.asarray(Image.open(key).convert('RGB'))
    return _img(np.dstack([arr, np.full((H, W, 1), 255, np.uint8)]))
def shader(img): return img.makeShader(skia.TileMode.kClamp, skia.TileMode.kClamp, skia.SamplingOptions(skia.FilterMode.kLinear))
def torn(y_edge, seed, amp=18):
    r = random.Random(seed); p = skia.Path(); p.moveTo(-60, -60); p.lineTo(W + 60, -60); p.lineTo(W + 60, y_edge); x = W + 60
    while x > -60: x -= r.uniform(14, 40); p.lineTo(x, y_edge + r.uniform(-amp, amp))
    p.close(); return p

_g = np.random.default_rng(3)
_gr = (_g.normal(0.5, 0.07, (H // 2, W // 2)) * 255).clip(0, 255).astype(np.uint8)
_gr = np.asarray(Image.fromarray(_gr).filter(ImageFilter.GaussianBlur(0.8)))
GRAIN = _img(np.dstack([_gr, _gr, _gr, np.full_like(_gr, 255)]))

# ---------------- stickers (real photo props with a white paper border) ----------------
_ST = {}
def sticker(name, maxd=500, border=22):
    """Load library/<name>.png (transparent PNG) as a paper sticker. Cached per (name, size)."""
    k = (name, maxd, border)
    if k in _ST: return _ST[k]
    im = Image.open(os.path.join(LIB, name + '.png')).convert('RGBA')
    im = im.crop(im.getbbox()); sc = maxd / max(im.size)
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    cw, ch = im.width + 2 * border, im.height + 2 * border
    cv = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); cv.paste(im, (border, border), im)
    a = np.asarray(cv)[..., 3] > 40
    bd = nd.binary_fill_holes(nd.binary_dilation(a, structure=np.ones((3, 3)), iterations=border - 4))
    bmask = Image.fromarray((bd * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    rg = np.random.default_rng(abs(hash(name)) % 1000)
    pap = (246 + rg.normal(0, 5, (ch, cw))).clip(0, 255).astype(np.uint8)
    pap = Image.fromarray(np.dstack([pap, pap, (pap * 0.985).astype(np.uint8)])).convert('RGBA'); pap.putalpha(bmask)
    pap.alpha_composite(cv); arr = np.asarray(pap).copy()
    _ST[k] = (_img(arr), _img(np.dstack([np.zeros_like(arr[..., :3]), arr[..., 3:]])), cw, ch, (a * 255).astype(np.uint8))
    return _ST[k]
def stk(c, name, x, y, s=1.0, rot=0, k=1.0, maxd=500, alpha=1.0):
    """Draw sticker centred at (x, y). k = pop-in progress 0..1 (overshoot), s = scale, rot = degrees."""
    if k <= 0: return
    img, sh, cw, ch, _ = sticker(name, maxd); s = s * back(min(1, k))
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.translate(-cw / 2, -ch / 2)
    c.save(); c.translate(12, 20)
    c.drawImage(sh, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(ImageFilter=skia.ImageFilters.Blur(12, 12), Alphaf=0.42 * alpha)); c.restore()
    c.drawImage(img, 0, 0, skia.SamplingOptions(skia.CubicResampler.Mitchell()), skia.Paint(Alphaf=alpha))
    c.restore()

# ---------------- text & graphic elements ----------------
def label(c, txt, cx, cy, size, rot, bgcol=WHT, fg=BLK, k=1, seed=0):
    """Torn paper label, evenly padded around the cap height. Keep cy between ~300 and ~1500 (app UI safe zone)."""
    if k <= 0: return
    font = skia.Font(FONT, size); tw = font.measureText(txt)
    cap = font.getMetrics().fCapHeight; padx = size * 0.42; pady = size * 0.30
    c.save(); c.translate(cx, cy); c.rotate(rot); s = back(min(1, k)); c.scale(s, s)
    r = random.Random(seed); p = skia.Path(); x0, y0, x1, y1 = -tw / 2 - padx, -cap - pady, tw / 2 + padx, pady
    p.moveTo(x0, y0); x = x0
    while x < x1: x += r.uniform(10, 22); p.lineTo(min(x, x1), y0 + r.uniform(-3, 3))
    y = y0
    while y < y1: y += r.uniform(10, 18); p.lineTo(x1 + r.uniform(-3, 3), min(y, y1))
    x = x1
    while x > x0: x -= r.uniform(10, 22); p.lineTo(max(x, x0), y1 + r.uniform(-3, 3))
    p.close()
    c.drawPath(off(p, 6, 10), skia.Paint(Color=skia.Color4f(0, 0, 0, .3), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(*bgcol, 1), AntiAlias=True))
    c.drawString(txt, -tw / 2, 0, font, skia.Paint(Color=skia.Color4f(*fg, 1), AntiAlias=True))
    c.restore()
def stamp(c, txt, x, y, size, rot, k, col=RED):
    """Slammed rubber stamp (pair with sfx 'impact1' and a shake)."""
    if k <= 0: return
    s = lerp(2.2, 1.0, eo(min(1, k * 1.4))); a = min(1, k * 3)
    font = skia.Font(FONT, size); w = font.measureText(txt); cap = font.getMetrics().fCapHeight
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w / 2 - 40, -cap - 36, w / 2 + 40, 36), 24, 24)
    c.drawRRect(rr, skia.Paint(Color=skia.Color4f(.98, .98, .96, a), AntiAlias=True))
    c.drawRRect(rr, skia.Paint(Color=skia.Color4f(*col, a), Style=skia.Paint.kStroke_Style, StrokeWidth=14, AntiAlias=True))
    c.drawString(txt, -w / 2, 0, font, skia.Paint(Color=skia.Color4f(*col, a), AntiAlias=True)); c.restore()
def rays(c, x, y, R, col, rot, k=1, n=14, a=0.35):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(eo(min(1, k)), eo(min(1, k))); p = skia.Path()
    for i in range(n):
        a0 = i / n * 2 * math.pi; a1 = a0 + math.pi / n
        p.moveTo(0, 0); p.lineTo(R * math.cos(a0), R * math.sin(a0)); p.lineTo(R * math.cos(a1), R * math.sin(a1)); p.close()
    c.drawPath(p, skia.Paint(Color=skia.Color4f(*col, a), AntiAlias=True)); c.restore()
def glyph(c, ch, x, y, size, rot, k, col=YEL):
    """A big paper character, e.g. '?' or '!' with a white border."""
    if k <= 0: return
    font = skia.Font(FONT, size); w = font.measureText(ch)
    c.save(); c.translate(x, y); c.rotate(rot); s = back(min(1, k)); c.scale(s, s)
    tb = skia.TextBlob.MakeFromString(ch, font)
    c.drawTextBlob(tb, -w / 2 + 8, size * 0.35 + 12, skia.Paint(Color=skia.Color4f(0, 0, 0, .3), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)))
    c.drawTextBlob(tb, -w / 2, size * 0.35, skia.Paint(Color=skia.Color4f(.98, .98, .96, 1), Style=skia.Paint.kStroke_Style, StrokeWidth=size * 0.16, StrokeJoin=skia.Paint.kRound_Join, AntiAlias=True))
    c.drawTextBlob(tb, -w / 2, size * 0.35, skia.Paint(Color=skia.Color4f(*col, 1), AntiAlias=True)); c.restore()
def bolt(c, x, y, s, rot, k):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); kk = back(min(1, k)); c.scale(s * kk, s * kk)
    p = skia.Path()
    for i, (px, py) in enumerate([(-30, -150), (60, -150), (10, -30), (70, -30), (-50, 160), (-10, 10), (-70, 10)]): (p.moveTo if i == 0 else p.lineTo)(px, py)
    p.close()
    c.drawPath(off(p, 8, 12), skia.Paint(Color=skia.Color4f(0, 0, 0, .3), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(.98, .98, .96, 1), Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=22, StrokeJoin=skia.Paint.kRound_Join, AntiAlias=True))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(*YEL, 1), AntiAlias=True)); c.restore()
def halftone(c, x, y, col=WHT, a=0.18):
    for i in range(-6, 7):
        for j in range(-6, 7):
            d = math.hypot(i, j) / 6
            if d <= 1: c.drawCircle(x + i * 26, y + j * 26, 9 * (1 - d) + 1, skia.Paint(Color=skia.Color4f(*col, a), AntiAlias=True))
def cloud(c, x, y, R, col, k, seed=0, a=1.0):
    """Paper puff cloud (gas, smoke, steam). Draw several with offsets for a plume."""
    if k <= 0: return
    r = random.Random(seed); s = eo(min(1, k))
    c.save(); c.translate(x, y); c.scale(s, s); p = skia.Path()
    for i in range(7):
        ang = i / 7 * 2 * math.pi; rr = R * r.uniform(0.45, 0.65)
        p.addCircle(R * 0.55 * math.cos(ang), R * 0.45 * math.sin(ang), rr)
    p.addCircle(0, 0, R * 0.6)
    p.setFillType(skia.PathFillType.kWinding)
    c.drawPath(off(p, 8, 12), skia.Paint(Color=skia.Color4f(0, 0, 0, .22 * a), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(.98, .98, .96, a), Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=26, StrokeJoin=skia.Paint.kRound_Join, AntiAlias=True))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(*col, a), AntiAlias=True)); c.restore()

# ---------------- photo-paper water ----------------
_OC = None
def _ocean():
    global _OC
    if _OC is None:
        o = Image.open(os.path.join(TEX, 'ocean.jpg')).convert('RGB').crop((0, 110, 1280, 720)).resize((1800, 858), Image.LANCZOS)
        _OC = _img(np.asarray(o.convert('RGBA')))
    return _OC
def ocean_shader(dx, dy, sc=1.0):
    m = skia.Matrix(); m.setScale(sc, sc); m.postTranslate(dx, dy)
    return _ocean().makeShader(skia.TileMode.kMirror, skia.TileMode.kMirror, skia.SamplingOptions(skia.FilterMode.kLinear), m)
def water(c, level, tq, amp=30):
    """Three torn-paper layers cut from a real sea photo, thick white edges. level = top y."""
    for li in range(3):
        yb = level + li * 85; ph = tq * (2.0 + li * 0.6) + li * 2.1
        p = skia.Path(); p.moveTo(-60, H + 600); p.lineTo(-60, yb); rr = random.Random(li * 11 + int(tq * 15) // 4)
        for k in range(0, 46):
            x = -60 + k * (W + 120) / 45
            p.lineTo(x, yb + amp * math.sin(k * 0.5 + ph) + amp * 0.35 * math.sin(k * 1.4 - ph * 1.3) + rr.uniform(-1.5, 1.5))
        p.lineTo(W + 60, H + 600); p.close()
        c.drawPath(off(p, 0, -22), skia.Paint(Color=skia.Color4f(0, 0, 0, .30), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)))
        c.drawPath(p, skia.Paint(Color=skia.Color4f(.97, .97, .95, 1), Style=skia.Paint.kStroke_Style, StrokeWidth=46, AntiAlias=True, StrokeJoin=skia.Paint.kRound_Join))
        sc = 2.3 + li * 0.2; c.drawPath(p, skia.Paint(Shader=ocean_shader(-(250 + li * 180) * sc, yb - (170 + li * 25) * sc, sc), AntiAlias=True))
def drop(c, x, y, r, rot, seed=0):
    """Photo-water drop with a paper border."""
    c.save(); c.translate(x, y); c.rotate(rot)
    p = skia.Path(); p.moveTo(0, -r * 2.1); p.cubicTo(r * .3, -r * 1.1, r, -r * .3, r, r * .2); p.cubicTo(r, r * .8, r * .55, r * 1.1, 0, r * 1.1)
    p.cubicTo(-r * .55, r * 1.1, -r, r * .8, -r, r * .2); p.cubicTo(-r, -r * .3, -r * .3, -r * 1.1, 0, -r * 2.1); p.close()
    c.drawPath(off(p, 5, 8), skia.Paint(Color=skia.Color4f(0, 0, 0, .3), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5)))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(.97, .97, .95, 1), AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=max(20, r * 0.62), StrokeJoin=skia.Paint.kRound_Join))
    sc = r / 38; c.drawPath(p, skia.Paint(Shader=ocean_shader(-(700 + (seed % 5) * 60) * sc, -(300 + (seed % 3) * 25) * sc, sc), AntiAlias=True))
    c.drawOval(skia.Rect.MakeXYWH(-r * .55, -r * .35, r * .28, r * .5), skia.Paint(Color=skia.Color4f(1, 1, 1, .85), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.5)))
    c.restore()

# ---------------- the kit: timing, camera, render, mix ----------------
class Frame:
    def __init__(s, t, K):
        s.t = t; s.tq = math.floor(t * 15) / 15; s.r = random.Random(int(s.tq * 15))
        s.jx, s.jy, s.jr = s.r.uniform(-4, 4), s.r.uniform(-4, 4), s.r.uniform(-1.2, 1.2)
        s.beat = max(i for i in range(len(K.B)) if s.tq >= K.B[i]); s.K = K
    def k(s, a, b): return prog(s.tq, a, b)

class Kit:
    def __init__(s, starts, dur, colors, shakes=(), music='funk_music1', voice_files=None):
        s.S = list(starts); s.B = [0.0] + [x - 0.2 for x in s.S[1:]]; s.DUR = dur; s.shakes = list(shakes)
        s.BG = [paper_bg(PALETTE[c] if isinstance(c, str) else c, seed=i) for i, c in enumerate(colors)]
        s.EV = []; s.music = music; s.voice_files = voice_files or []
    def sfx(s, t, name, gain=1.0): s.EV.append((t, name, gain))
    def default_sfx(s):
        for i in range(1, len(s.B)): s.sfx(s.B[i] - 0.05, 'swoosh1' if i % 2 else 'swoosh2', 0.8); s.sfx(s.B[i] + 0.05, 'paper', 0.9)
    def frame(s, c, t, scene):
        f = Frame(t, s); tq = f.tq; b = f.beat
        punch = 1 + 0.07 * (1 - eo(prog(tq, s.B[b], s.B[b] + 0.35))); sh = 0
        for ts in s.shakes:
            if 0 <= tq - ts < 0.35: sh = 18 * (1 - (tq - ts) / 0.35)
        c.save(); c.translate(W / 2 + f.r.uniform(-sh, sh), H / 2 + f.r.uniform(-sh, sh)); c.scale(punch, punch); c.translate(-W / 2, -H / 2)
        if b > 0 and tq < s.B[b] + 0.4:
            c.drawPaint(skia.Paint(Shader=shader(s.BG[b - 1])))
            yy = lerp(-80, H + 80, eio(prog(tq, s.B[b], s.B[b] + 0.4)))
            c.drawPath(off(torn(yy, b), 0, 16), skia.Paint(Color=skia.Color4f(0, 0, 0, .3), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12)))
            c.drawPath(torn(yy, b), skia.Paint(Shader=shader(s.BG[b]), AntiAlias=True))
        else: c.drawPaint(skia.Paint(Shader=shader(s.BG[b])))
        halftone(c, 90, 260); halftone(c, W - 90, H - 300)
        scene(c, t, f)
        c.restore()
        c.drawImageRect(GRAIN, skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(BlendMode=skia.BlendMode.kOverlay, Alphaf=0.22))
    def stills(s, scene, ts, prefix='still'):
        surf = skia.Surface(W, H); outs = []
        for t in ts:
            c = surf.getCanvas(); c.clear(0); s.frame(c, t, scene); fn = f'{prefix}_{t:.2f}.png'; surf.makeImageSnapshot().save(fn); outs.append(fn)
        return outs
    def video(s, scene, out='video.mp4'):
        surf = skia.Surface(W, H); e = Enc(out)
        for i in range(int(s.DUR * FPS)):
            c = surf.getCanvas(); c.clear(0); s.frame(c, i / FPS, scene); e.write(surf)
        e.close()
    def mix(s, out='mix.wav'):
        SR = 48000; N = int(s.DUR * SR)
        def load(p):
            r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True)
            return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
        MAXL = {'pop': 0.6, 'whoosh': 1.3, 'snip': 1.0, 'impact2': 2.0, 'impact1': 1.6, 'sparkle1': 1.6, 'sparkle2': 1.6, 'bubble': 1.8, 'splash1': 1.8, 'splash2': 1.8,
                'swoosh1': 1.0, 'swoosh2': 1.0, 'swoosh3': 1.5, 'paper': 0.9, 'scratch1': 1.4, 'scratch2': 1.4, 'ding1': 1.8, 'ding2': 0.7}
        def trim(a, ml):
            e = np.abs(a).max(1); thr = max(0.02, e.max() * 0.08); i = int(np.argmax(e > thr)); a = a[max(0, i - 200):][:int(ml * SR)].copy()
            f = min(len(a), int(0.08 * SR)); a[-f:] *= np.linspace(1, 0, f)[:, None]; return a / max(1e-6, np.abs(a).max())
        cache = {}
        out_a = np.zeros((N, 2), np.float32); voice = np.zeros((N, 2), np.float32)
        for st, vf in zip(s.S, s.voice_files):
            v = load(vf); v /= max(1e-6, np.abs(v).max()); a = int(st * SR); v = v[:max(0, N - a)]; voice[a:a + len(v)] += v * 0.95
        m = load(os.path.join(MUS, s.music + '.mp3'))[:N]; m /= max(1e-6, np.abs(m).max())
        env = np.convolve((np.abs(voice).mean(1) > 0.02).astype(np.float32), np.ones(int(0.25 * SR)) / (0.25 * SR), 'same')
        gain = 0.42 - 0.24 * np.clip(env * 3, 0, 1); m *= gain[:len(m), None]
        fi = int(0.3 * SR); m[:fi] *= np.linspace(0, 1, fi)[:, None]; fo = int(1.0 * SR); m[-fo:] *= np.linspace(1, 0, fo)[:, None]
        out_a[:len(m)] += m
        for t, n, g in s.EV:
            if n not in cache: cache[n] = trim(load(os.path.join(SFX, n + '.mp3')), MAXL.get(n, 1.5))
            a = cache[n]; i = int(max(0, t) * SR); L = min(len(a), N - i)
            if L > 0: out_a[i:i + L] += a[:L] * 0.55 * g
        out_a += voice; out_a /= max(1.0, np.abs(out_a).max() / 0.95)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', out], input=out_a.tobytes(), check=True)
    def run(s, scene, argv, name='episode'):
        mode = argv[1] if len(argv) > 1 else 'all'
        if mode == 'stills':
            ts = [float(x) for x in argv[2].split(',')] if len(argv) > 2 else [b + 1.2 for b in s.B]
            print('\n'.join(s.stills(scene, ts)))
        if mode in ('video', 'all'): s.video(scene, f'{name}_video.mp4')
        if mode in ('mix', 'all'): s.mix(f'{name}_mix.wav')
        if mode == 'all':
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{name}_video.mp4', '-i', f'{name}_mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                            '-af', 'loudnorm=I=-14:TP=-1.0', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', f'{name}_final.mp4'], check=True)
            # upload copy < 9.3 MB for Buffer
            dur = s.DUR; kbps = int(9.0 * 8192 / dur) - 200
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{name}_final.mp4', '-c:v', 'libx264', '-b:v', f'{kbps}k', '-maxrate', f'{kbps}k', '-bufsize', f'{2*kbps}k',
                            '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', f'{name}_upload.mp4'], check=True)
            print('built', f'{name}_final.mp4', f'{name}_upload.mp4')

def timeline(voice_files, head=0.2, gap=0.22, tail=0.6):
    """Voice segment start times and total duration from the segment wav lengths."""
    starts = []; t = head
    for vf in voice_files:
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vf], capture_output=True, text=True).stdout)
        starts.append(t); t += d + gap
    return starts, t - gap + tail

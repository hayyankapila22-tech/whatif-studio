"""P13 — Why is the sky blue, but sunsets are orange? (PAPER-CUTOUT format)
Facts (plain words, no studies): sunlight looks white but is a mix of all colours (a prism / rainbow splits it). Air
molecules scatter short-wavelength blue light much more than red (Rayleigh scattering), so blue light is bounced all over
the sky and reaches our eyes from every direction. At sunrise/sunset the sun is low, so its light passes through much more
atmosphere; most of the blue is scattered out along the way and mostly orange and red get through. On Mars it's the
reverse: fine dust makes the daytime sky butterscotch and the sunsets blue (NASA Curiosity photographed a blue sunset, 2015).
Sources: NASA SVS "Curiosity Sees Blue Sunset On Mars"; NASA Space Place "Why is the sky blue?"; EarthDate "Blue Sky, Blue
Sunset"; NBC News "What makes skies blue ... or red?"; IFLScience "Why are Mars sunsets blue?".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['blue', 'orange', 'purple', 'mint', 'coral', 'red'], shakes=[S[2] + 2.0, S[4] + 2.0, DUR - 1.6], voice_files=VO, music=MUSIC)
B = K.B
SKY = (.25, .6, 1.0); ORG = (1, .55, .1)
MARS = 'mars2' if os.path.exists(os.path.join(LIB, 'mars2.png')) else 'mars'
SHADES = 'sunglasses2' if os.path.exists(os.path.join(LIB, 'sunglasses2.png')) else None

def dot(c, x, y, r, col, k=1):
    if k <= 0: return
    r *= back(min(1, k))
    c.drawCircle(x + 4, y + 7, r, skia.Paint(Color=skia.Color4f(0, 0, 0, .25), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4)))
    c.drawCircle(x, y, r + 7, skia.Paint(Color=skia.Color4f(.98, .98, .96, 1), AntiAlias=True))
    c.drawCircle(x, y, r, skia.Paint(Color=skia.Color4f(*col, 1), AntiAlias=True))

def bouncers(c, tq, t0, n, cx, cy, R, col, k, seed=0, out=0.0):
    """paper dots ping-ponging inside a circle (scattered light); out>0 pushes them off screen"""
    r = random.Random(seed)
    for i in range(n):
        a0 = r.uniform(0, 2*math.pi); sp = r.uniform(1.5, 3.0); ph = r.uniform(0, 6)
        x = cx + R*math.sin(sp*(tq - t0) + ph)*math.cos(a0) + out*1400*math.cos(a0)
        y = cy + R*math.sin(sp*1.3*(tq - t0) + ph*0.7)*math.sin(a0) + out*1400*math.sin(a0)
        dot(c, x, y, 28, col, k - i*0.03)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook
        rays(c, W*0.36, 1050, 1100, WHT, tq*12, f.k(0.05, 0.45), a=0.25)
        stk(c, 'sun', W*0.36 + jx, 1050 + jy, 1.0, jr*2, f.k(0.0, 0.3), maxd=560)
        cloud(c, W*0.78 + jx, 900 + jy, 130, WHT, f.k(0.4, 0.7), seed=1)
        cloud(c, W*0.70 + jx, 1500 + jy, 110, (1, .75, .45), f.k(0.7, 1.0), seed=2)
        glyph(c, '?', 930, 1250, 130, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "why is the sky BLUE", W/2 + jx*.4, 330, 84, -3 + jr*.5, bgcol=(.8, .92, 1), k=f.k(0.1, 0.35), seed=1)
        label(c, "but sunsets ORANGE?", W/2 + 10, 470, 84, 2 - jr*.5, bgcol=ORG, k=f.k(1.1, 1.35), seed=2)
    elif b == 1:  # white light = all colours
        s0 = S[1]
        stk(c, 'sun', W*0.24 + jx, 960 + jy, 0.8, jr*2, f.k(B[1] + 0.1, B[1] + 0.35), maxd=420)
        arrow(c, W*0.36, 1080, 260, 35, f.k(s0 + 0.6, s0 + 1.0), col=WHT)
        stk(c, 'prism', W*0.62 + jx, 1400 + jy, 1.25, -4 + jr, f.k(s0 + 1.6, s0 + 1.85), maxd=560)
        stk(c, 'crayons', W*0.80 + jx, 860 + jy, 0.75, 18 + jr, f.k(s0 + 2.4, s0 + 2.65), maxd=360)
        label(c, "SUNLIGHT looks WHITE", W/2, 330, 80, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=3)
        label(c, "but it's EVERY colour!", W/2 + 15, 470, 80, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.6, s0 + 1.85), seed=4)
    elif b == 2:  # blue bounces most
        s0 = S[2]
        stk(c, 'earth', W/2 + jx, 1300 + jy, 1.25, jr, f.k(B[2] + 0.1, B[2] + 0.35), maxd=440)
        bouncers(c, tq, s0, 12, W/2, 1150, 400, SKY, f.k(s0 + 0.8, s0 + 1.3), seed=3)
        for i, col in enumerate([(1, .25, .2), ORG, (1, .9, .2)]):
            arrow(c, 70, 760 + i*60, 940, 0, f.k(s0 + 0.5 + i*0.1, s0 + 1.0 + i*0.1), col=col, w=22)
        if tq > s0 + 2.0: stamp(c, "BOING!", W*0.5, 1680, 110, -6, f.k(s0 + 2.0, s0 + 2.25), col=(.1, .4, .95))
        label(c, "BLUE bounces", W/2, 330, 100, -2 + jr*.5, bgcol=(.8, .92, 1), k=f.k(s0 + 0.6, s0 + 0.85), seed=5)
        label(c, "around the MOST!", W/2 + 15, 470, 92, 3 - jr*.5, k=f.k(s0 + 1.3, s0 + 1.55), seed=6)
    elif b == 3:  # sunset = long path through air
        s0 = S[3]
        gk = eo(f.k(B[3] + 0.1, B[3] + 0.4))
        c.drawCircle(W*0.5, 2250, 1100*gk, skia.Paint(Color=skia.Color4f(.75, .9, 1, .55), AntiAlias=True))   # air layer
        c.drawCircle(W*0.5, 2250, 720*gk + 10, skia.Paint(Color=skia.Color4f(.98, .98, .96, 1), AntiAlias=True))
        c.drawCircle(W*0.5, 2250, 720*gk, skia.Paint(Color=skia.Color4f(.2, .62, .3, 1), AntiAlias=True))      # ground
        dot(c, W*0.5, 1530, 26, (1, .9, .2), f.k(s0 + 0.2, s0 + 0.4))
        label(c, "YOU", W*0.5 + 110, 1505, 56, 4, k=f.k(s0 + 0.2, s0 + 0.45), seed=21)
        arrow(c, W*0.5, 1250, 240, 90, f.k(s0 + 0.5, s0 + 0.9), col=WHT, w=26)
        stk(c, 'sun', W*0.12 + jx, 1100 + jy, 0.5, jr*2, f.k(s0 + 0.3, s0 + 0.55), maxd=380)
        arrow(c, W*0.16, 1200, 450, 45, f.k(s0 + 1.0, s0 + 2.0), col=ORG, w=30)
        if tq > s0 + 2.0: stamp(c, "SO MUCH AIR!", W*0.62, 960, 84, -5, f.k(s0 + 2.0, s0 + 2.25), col=(.1, .4, .95))
        label(c, "at SUNSET, light goes", W/2, 330, 80, -2 + jr*.5, k=f.k(s0 + 0.1, s0 + 0.35), seed=7)
        label(c, "through WAY MORE AIR", W/2 + 10, 470, 74, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.0, s0 + 1.25), seed=8)
    elif b == 4:  # blue bounced away, orange/red through
        s0 = S[4]
        bouncers(c, tq, s0, 14, W/2, 1150, 330, SKY, 1, seed=4, out=eio(f.k(s0 + 0.6, s0 + 2.2)))
        rays(c, W/2, 1150, 800, ORG, tq*15, f.k(s0 + 1.6, s0 + 2.0), a=0.4)
        stk(c, 'sun', W/2 + jx, 1150 + jy, 0.85, jr*2, f.k(B[4] + 0.1, B[4] + 0.35), maxd=480)
        if SHADES: stk(c, SHADES, W*0.74 + jx, 1580 + jy, 0.6, 12 + jr, f.k(s0 + 2.4, s0 + 2.65), maxd=380)
        label(c, "BLUE gets bounced AWAY", W/2, 330, 72, -2 + jr*.5, bgcol=(.8, .92, 1), k=f.k(s0 + 0.2, s0 + 0.45), seed=9)
        label(c, "ORANGE + RED win!", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=ORG, k=f.k(s0 + 1.6, s0 + 1.85), seed=10)
    else:         # Mars: blue sunsets
        s0 = S[5]
        if tq <= s0 + 1.6: stk(c, MARS, W*0.5 + jx, 1180 + jy, 1.1, jr, f.k(s0 + 0.2, s0 + 0.45), maxd=600)
        if tq > s0 + 1.6:
            rays(c, W*0.5, 1180, 1000, SKY, tq*12, f.k(s0 + 1.6, s0 + 2.0), a=0.55)
            c.drawCircle(W*0.5, 1180, 470, skia.Paint(Color=skia.Color4f(*SKY, .8 * f.k(s0 + 1.6, s0 + 2.0)), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60)))
            stk(c, MARS, W*0.5 + jx, 1180 + jy, 1.1, jr, 1, maxd=600)
        glyph(c, '!', 900, 900, 150, 12 - jr*2, f.k(s0 + 1.0, s0 + 1.25), col=SKY)
        label(c, "and on MARS?", W/2, 330, 100, -2 + jr*.5, bgcol=(1, .6, .4), k=f.k(s0 + 0.2, s0 + 0.45), seed=11)
        label(c, "it's the OPPOSITE!", W/2 + 15, 470, 90, 3 - jr*.5, k=f.k(s0 + 1.0, s0 + 1.25), seed=12)
        if tq > DUR - 1.6: stamp(c, "BLUE SUNSETS!", W*0.5, 1690, 96, -5, f.k(DUR - 1.6, DUR - 1.35), col=(.1, .4, .95))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'sparkle2', 0.4); K.sfx(0.4, 'pop', 0.6); K.sfx(0.55, 'pop', 0.6); K.sfx(0.7, 'pop', 0.6); K.sfx(1.1, 'pop', 0.7); K.sfx(1.15, 'ding1', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.2, 'pop', 0.6); K.sfx(S[1] + 0.6, 'swoosh3', 0.5); K.sfx(S[1] + 1.6, 'pop', 0.7); K.sfx(S[1] + 1.65, 'sparkle1', 0.6); K.sfx(S[1] + 2.4, 'pop', 0.6)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.5, 'whoosh', 0.5); K.sfx(S[2] + 0.6, 'pop', 0.6)
for i in range(4): K.sfx(S[2] + 0.8 + i*0.25, 'bubble' if i % 2 else 'pop', 0.4)
K.sfx(S[2] + 1.3, 'pop', 0.6); K.sfx(S[2] + 2.0, 'impact2', 0.9)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.1, 'pop', 0.6); K.sfx(S[3] + 0.3, 'pop', 0.6); K.sfx(S[3] + 1.0, 'swoosh3', 0.6); K.sfx(S[3] + 1.0, 'pop', 0.6); K.sfx(S[3] + 2.0, 'impact1', 0.9)
K.sfx(S[4] + 0.2, 'whoosh', 0.6); K.sfx(S[4] + 0.2, 'pop', 0.6); K.sfx(S[4] + 1.6, 'pop', 0.7); K.sfx(S[4] + 1.65, 'sparkle2', 0.6); K.sfx(S[4] + 2.0, 'impact2', 0.6); K.sfx(S[4] + 2.4, 'pop', 0.6)
K.sfx(S[5] + 0.2, 'pop', 0.7); K.sfx(S[5] + 1.0, 'pop', 0.6); K.sfx(S[5] + 1.0, 'ding2', 0.5); K.sfx(S[5] + 1.6, 'sparkle1', 0.6)
K.sfx(DUR - 1.6, 'impact1', 0.9); K.sfx(DUR - 1.55, 'sparkle2', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p13_sky_colours')

"""P12 — How do fireflies light up? (PAPER-CUTOUT format)
Facts (plain words, no studies): fireflies make light with a chemical reaction in light organs in their lower abdomen
(bioluminescence): a chemical (luciferin) and a helper enzyme (luciferase) react with oxygen (plus the cell's energy
molecule) and give off light. It's "cold light": nearly all the energy becomes light, almost no heat (an old-style bulb
loses most of its energy as heat). Each firefly species has its own flash pattern; males flash and females answer to
find a mate. Artificial light at night makes it harder for them to see each other's signals -> turn off outdoor lights.
Sources: Britannica "How Do Fireflies Light Up?"; Live Science "How do fireflies light up?"; Scientific American "How and
why do fireflies light up?"; EarthSky "How do fireflies make light?"; Xerces Society / Firefly Conservation (light pollution).
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['navy', 'orange', 'purple', 'teal', 'pink', 'blue'], shakes=[S[1] + 1.0, S[2] + 2.3, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
GLOW = (.78, 1.0, .25)

def glow(c, x, y, r, a=1.0):
    if a <= 0: return
    c.drawCircle(x, y, r * 1.8, skia.Paint(Color=skia.Color4f(*GLOW, .35 * a), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * .8)))
    c.drawCircle(x, y, r, skia.Paint(Color=skia.Color4f(*GLOW, .85 * a), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * .35)))
    c.drawCircle(x, y, r * .45, skia.Paint(Color=skia.Color4f(1, 1, .85, a), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * .15)))

def fly(c, x, y, s, rot, k, lit, maxd=520):
    """firefly sticker with a glowing tail (tail = right end of the photo)"""
    if k <= 0: return
    stk(c, 'firefly', x, y, s, rot, k, maxd=maxd)
    a = math.radians(rot); d = 0.40 * maxd * s * back(min(1, k)); dy = -0.06 * maxd * s
    glow(c, x + d * math.cos(a) - dy * math.sin(a), y + d * math.sin(a) + dy * math.cos(a), 70 * s, lit * min(1, k))

def pulse(tq, sp=4.0): return 0.55 + 0.45 * math.sin(tq * sp * 2 * math.pi) ** 2

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook
        rays(c, W/2, 1080, 1100, WHT, tq*12, f.k(0.05, 0.45), a=0.18)
        stk(c, 'moon', W*0.80 + jx, 820 + jy, 0.55, 10 + jr, f.k(0.5, 0.75), maxd=380)
        fly(c, W*0.45 + jx, 1150 + jy, 1.25, -8 + jr, f.k(0.0, 0.3), pulse(tq, 1.5))
        glyph(c, '?', 150, 1500, 140, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 940, 1520, 120, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "how do FIREFLIES", W/2 + jx*.4, 330, 88, -3 + jr*.5, k=f.k(0.1, 0.35), seed=1)
        label(c, "LIGHT UP?", W/2 + 10, 470, 110, 2 - jr*.5, bgcol=GLOW, k=f.k(0.6, 0.85), seed=2)
    elif b == 1:  # no batteries, chemical reaction
        s0 = S[1]
        stk(c, 'battery', W*0.30 + jx, 900 + jy, 0.85, -10 + jr, f.k(B[1] + 0.1, B[1] + 0.35), maxd=420)
        if tq > s0 + 0.9: stamp(c, "NOPE!", W*0.30, 1120, 110, -10, f.k(s0 + 0.9, s0 + 1.15))
        fly(c, W*0.62 + jx, 1420 + jy, 1.0, 6 + jr, f.k(s0 + 1.5, s0 + 1.75), pulse(tq) * f.k(s0 + 2.0, s0 + 2.3))
        label(c, "NO BATTERIES!", W/2, 330, 100, -2 + jr*.5, k=f.k(s0 + 0.1, s0 + 0.35), seed=3)
        label(c, "a CHEMICAL REACTION", W/2 + 15, 470, 80, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.5, s0 + 1.75), seed=4)
    elif b == 2:  # two chemicals + oxygen -> glow
        s0 = S[2]
        m = eio(f.k(s0 + 1.2, s0 + 2.2))
        blob(c, lerp(W*0.25, W*0.44, m) + jx, 1000 + jy, 110, (1, .45, .2), jr*3, f.k(s0 + 0.2, s0 + 0.45), seed=3)
        blob(c, lerp(W*0.75, W*0.56, m) + jx, 1000 + jy, 110, (.3, .7, 1), -jr*3, f.k(s0 + 0.5, s0 + 0.75), seed=5)
        for i in range(3): cloud(c, W*(0.30 + i*0.2) + jx, 1300 + 20*math.sin(tq*6 + i) + jy, 80, (.9, .97, 1), f.k(s0 + 1.0 + i*0.1, s0 + 1.3 + i*0.1), seed=i)
        if tq > s0 + 2.3:
            rays(c, W/2, 1100, 900, GLOW, tq*20, f.k(s0 + 2.3, s0 + 2.6), a=0.35)
            glow(c, W/2, 1050, 200, f.k(s0 + 2.3, s0 + 2.5) * pulse(tq, 2))
            stamp(c, "GLOW!", W*0.5, 1600, 130, -6, f.k(s0 + 2.3, s0 + 2.55), col=(.2, .55, .1))
        label(c, "2 CHEMICALS", W/2, 330, 100, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=5)
        label(c, "+ OXYGEN", W/2 + 15, 470, 100, 3 - jr*.5, bgcol=(.75, .9, 1), k=f.k(s0 + 1.0, s0 + 1.25), seed=6)
    elif b == 3:  # cold light vs bulb
        s0 = S[3]
        fly(c, W*0.30 + jx, 1000 + jy, 0.85, -12 + jr, f.k(B[3] + 0.1, B[3] + 0.35), pulse(tq, 2))
        stk(c, 'thermometer', W*0.22 + jx, 1440 + jy, 0.55, 10 + jr, f.k(s0 + 0.9, s0 + 1.15), maxd=380)
        if tq > s0 + 1.2: stamp(c, "COOL", W*0.30, 1700, 90, -8, f.k(s0 + 1.2, s0 + 1.45), col=(.1, .45, .95))
        if tq > s0 + 2.2: rays(c, W*0.72, 1180, 380, (1, .5, .1), tq*30, f.k(s0 + 2.2, s0 + 2.5), a=0.5)
        stk(c, 'bulb3', W*0.72 + jx, 1180 + jy, 0.95, 8 + jr, f.k(s0 + 2.2, s0 + 2.45), maxd=440)
        if tq > s0 + 2.7: stamp(c, "HOT!", W*0.74, 1600, 110, 8, f.k(s0 + 2.7, s0 + 2.95))
        label(c, "it's COLD LIGHT", W/2, 330, 92, -2 + jr*.5, k=f.k(s0 + 0.1, s0 + 0.35), seed=7)
        label(c, "almost NO HEAT", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=(.75, .9, 1), k=f.k(s0 + 0.9, s0 + 1.15), seed=8)
    elif b == 4:  # secret flash code -> date
        s0 = S[4]
        code1 = 1.0 if (int(tq * 6) % 4 in (0, 2)) else 0.15
        code2 = 1.0 if (int(tq * 6 + 1) % 3 == 0) else 0.15
        fly(c, W*0.30 + jx, 900 + jy, 0.8, -15 + jr, f.k(B[4] + 0.1, B[4] + 0.35), code1 * f.k(s0 + 0.6, s0 + 0.7))
        fly(c, W*0.66 + jx, 1300 + jy, 0.8, 18 + jr, f.k(s0 + 0.5, s0 + 0.75), code2 * f.k(s0 + 1.0, s0 + 1.1))
        stk(c, 'heart', W*0.50 + jx, 1620 + jy, 0.8*(1 + 0.08*math.sin(tq*12)), jr*2, f.k(s0 + 2.6, s0 + 2.85), maxd=360)
        label(c, "a SECRET flash CODE", W/2, 330, 82, -2 + jr*.5, bgcol=GLOW, k=f.k(s0 + 0.6, s0 + 0.85), seed=9)
        label(c, "to find a DATE!", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=(1, .7, .8), k=f.k(s0 + 2.6, s0 + 2.85), seed=10)
    else:         # tip: turn off garden lights
        s0 = S[5]
        lamp = 'bulb3'
        stk(c, lamp, W*0.28 + jx, 1080 + jy, 0.95, -6 + jr, f.k(s0 + 0.1, s0 + 0.35), maxd=560)
        if tq > s0 + 1.0: stamp(c, "OFF!", W*0.28, 1480, 120, -8, f.k(s0 + 1.0, s0 + 1.25), col=BLK)
        stk(c, 'moon', W*0.78 + jx, 800 + jy, 0.5, 10 + jr, f.k(s0 + 0.5, s0 + 0.75), maxd=360)
        for i, (x, y) in enumerate([(0.70, 1150), (0.82, 1350), (0.62, 1420)]):
            fly(c, W*x + jx, y + jy + 15*math.sin(tq*3 + i), 0.45, 10 + i*40 + jr, f.k(s0 + 1.8 + i*0.15, s0 + 2.05 + i*0.15), pulse(tq + i*0.3, 1.2), maxd=420)
        label(c, "lights OFF at night", W/2, 330, 86, -2 + jr*.5, k=f.k(s0 + 0.9, s0 + 1.15), seed=11)
        label(c, "HELPS fireflies!", W/2 + 15, 470, 94, 3 - jr*.5, bgcol=GLOW, k=f.k(s0 + 2.0, s0 + 2.25), seed=12)
        if tq > DUR - 1.5: stamp(c, "TIP!", W*0.72, 1660, 130, 6, f.k(DUR - 1.5, DUR - 1.25), col=(.1, .6, .3))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'sparkle2', 0.5); K.sfx(0.1, 'pop', 0.6); K.sfx(0.35, 'pop', 0.6); K.sfx(0.5, 'pop', 0.6); K.sfx(0.55, 'pop', 0.6); K.sfx(0.6, 'ding1', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.1, 'pop', 0.6); K.sfx(S[1] + 0.9, 'impact1', 0.9); K.sfx(S[1] + 0.95, 'scratch1', 0.4); K.sfx(S[1] + 1.5, 'pop', 0.7); K.sfx(S[1] + 2.0, 'sparkle1', 0.5)
K.sfx(S[2] + 0.2, 'pop', 0.7); K.sfx(S[2] + 0.5, 'pop', 0.7); K.sfx(S[2] + 1.0, 'bubble', 0.5); K.sfx(S[2] + 1.2, 'swoosh3', 0.5); K.sfx(S[2] + 2.3, 'impact2', 0.9); K.sfx(S[2] + 2.35, 'sparkle2', 0.6)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.1, 'pop', 0.6); K.sfx(S[3] + 0.9, 'pop', 0.6); K.sfx(S[3] + 1.2, 'impact1', 0.7); K.sfx(S[3] + 2.2, 'pop', 0.7); K.sfx(S[3] + 2.7, 'impact1', 0.9)
K.sfx(B[4] + 0.1, 'pop', 0.7); K.sfx(S[4] + 0.5, 'pop', 0.6); K.sfx(S[4] + 0.6, 'ding2', 0.5); K.sfx(S[4] + 1.0, 'ding2', 0.5); K.sfx(S[4] + 1.6, 'ding2', 0.4); K.sfx(S[4] + 2.6, 'pop', 0.7); K.sfx(S[4] + 2.65, 'sparkle1', 0.6)
K.sfx(S[5] + 0.1, 'pop', 0.7); K.sfx(S[5] + 0.5, 'pop', 0.6); K.sfx(S[5] + 1.0, 'impact1', 0.9); K.sfx(S[5] + 1.05, 'snip', 0.5)
for i in range(3): K.sfx(S[5] + 1.8 + i*0.15, 'sparkle1' if i % 2 else 'pop', 0.45)
K.sfx(S[5] + 2.0, 'pop', 0.6); K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle2', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p12_fireflies')

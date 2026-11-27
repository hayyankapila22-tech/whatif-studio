"""P15 — Why does popcorn pop? (PAPER-CUTOUT format)
Facts (plain words, no studies): every popcorn kernel has a little water inside (roughly 13-14 %) and a very hard,
waterproof shell (the hull). Heating turns the water into steam; the steam can't escape, so pressure builds. At about
180 °C (~355 °F) the hull bursts, the soft starch inside puffs up into a foam that sets as it cools, and the kernel
turns inside out. Kernels that dry out (or have a cracked hull) don't pop -> store them in an airtight container.
Sources: Scientific American / Science Buddies "Explore the POP in popcorn"; USDA National Agricultural Library
"How does popcorn pop?"; Science News Explores "How popcorn got its pop"; Farmers' Almanac "Why does popcorn explode?".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['red', 'teal', 'orange', 'purple', 'blue', 'mint'], shakes=[S[3] + 2.85, S[2] + 1.9, S[5] + 3.6], voice_files=VO, music=MUSIC)
B = K.B
CORN = (1.0, .82, .25); STEAM = (.92, .95, 1.0)
def has(n): return os.path.exists(os.path.join(LIB, n + '.png'))
KER = None   # Pixabay has no clean single-kernel cut-out (kernel_a/kernel_b are popcorn boxes) -> paper kernel

def kernel(c, x, y, r, rot, k=1, glow=0.0):
    """one popcorn kernel: prop if we have it, else a paper kernel"""
    if k <= 0: return
    if KER: stk(c, KER, x, y, r / 120, rot, k, maxd=300); return
    s = back(min(1, k)); c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, -r * 0.95)
    p.cubicTo(r * 0.75, -r * 0.98, r * 0.95, -r * 0.35, r * 0.7, r * 0.3)
    p.cubicTo(r * 0.48, r * 0.8, r * 0.18, r * 1.25, 0, r * 1.3)
    p.cubicTo(-r * 0.18, r * 1.25, -r * 0.48, r * 0.8, -r * 0.7, r * 0.3)
    p.cubicTo(-r * 0.95, -r * 0.35, -r * 0.75, -r * 0.98, 0, -r * 0.95); p.close()
    c.drawPath(off(p, 8, 12), skia.Paint(Color=skia.Color4f(0, 0, 0, .3), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(.98, .98, .96, 1), Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=r * .28, StrokeJoin=skia.Paint.kRound_Join, AntiAlias=True))
    col = (lerp(.95, 1, glow), lerp(.62, .35, glow), lerp(.12, .1, glow))
    c.drawPath(p, skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(-r * .3, -r * .4), r * 1.6,
               [skia.Color4f(1, .9, .45, 1), skia.Color4f(*col, 1)]), AntiAlias=True))
    tip = skia.Path(); tip.moveTo(-r * .3, r * .78); tip.cubicTo(-r * .1, r * .7, r * .1, r * .7, r * .3, r * .78)
    tip.cubicTo(r * .2, r * 1.05, r * .1, r * 1.25, 0, r * 1.3); tip.cubicTo(-r * .1, r * 1.25, -r * .2, r * 1.05, -r * .3, r * .78); tip.close()
    c.drawPath(tip, skia.Paint(Color=skia.Color4f(1, .95, .78, 1), AntiAlias=True))
    c.drawPath(skia.Path.Line((0, -r * .3), (0, r * .55)) if hasattr(skia.Path, 'Line') else skia.Path(), skia.Paint(Color=skia.Color4f(1, .97, .8, .5), Style=skia.Paint.kStroke_Style, StrokeWidth=r * .12, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
    c.drawOval(skia.Rect.MakeXYWH(-r * .5, -r * .7, r * .22, r * .55), skia.Paint(Color=skia.Color4f(1, 1, 1, .7), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3)))
    c.restore()

def puffs(c, tq, t0, n=10, seed=0, cx=W/2, cy=1150, R=420):
    """popped pieces flying out of a centre point"""
    if tq < t0: return
    r = random.Random(seed); p = eo(min(1, (tq - t0) / 0.6))
    for i in range(n):
        a = r.uniform(0, 2 * math.pi); d = R * r.uniform(0.5, 1.0) * p
        cloud(c, cx + d * math.cos(a), cy + d * math.sin(a) + 120 * p * p, r.uniform(45, 70), (1, .96, .82), min(1, (tq - t0) * 6), seed=seed * 10 + i)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook
        rays(c, W/2, 1200, 1100, WHT, tq*12, f.k(0.05, 0.45), a=0.25)
        stk(c, 'popcorn_bowl', W*0.5 + jx, 1250 + jy, 1.15, -3 + jr, f.k(0.0, 0.3), maxd=640)
        stk(c, 'corn_cob', W*0.72 + jx, 820 + jy, 0.62, -28 + jr, f.k(0.35, 0.6), maxd=520)
        glyph(c, '?', 170, 860, 150, -12 + jr*2, f.k(0.5, 0.75))
        label(c, "why does POPCORN", W/2 + jx*.4, 330, 88, -3 + jr*.5, k=f.k(0.1, 0.35), seed=1)
        label(c, "POP?!", W/2 + 10, 470, 120, 2 - jr*.5, bgcol=YEL, k=f.k(1.15, 1.4), seed=2)
    elif b == 1:  # a drop of water inside every kernel
        s0 = S[1]
        stk(c, 'corn_cob', W*0.5 + jx, 1500 + jy, 0.85, 6 + jr, f.k(B[1] + 0.1, B[1] + 0.35), maxd=640)
        kernel(c, W*0.42 + jx, 1000 + jy, 175, -8 + jr, f.k(s0 + 0.3, s0 + 0.55))
        stk(c, 'magnifier', W*0.62 + jx, 1180 + jy, 0.7, 30 + jr, f.k(s0 + 0.6, s0 + 0.85), maxd=480) if has('magnifier') else None
        if tq > s0 + 1.4:
            kk = back(min(1, (tq - s0 - 1.4) * 4)); drop(c, W*0.78 + jx, 920 + jy + 8*math.sin(tq*6), 60*kk, 6*math.sin(tq*5), seed=2)
            arrow(c, W*0.70, 990, 120, 160, f.k(s0 + 1.6, s0 + 1.9), col=(.4, .7, 1))
        label(c, "every KERNEL hides", W/2, 330, 84, -2 + jr*.5, k=f.k(s0 + 0.1, s0 + 0.35), seed=3)
        label(c, "a drop of WATER!", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=(.55, .8, 1), k=f.k(s0 + 1.6, s0 + 1.85), seed=4)
    elif b == 2:  # heat -> steam, trapped behind a tough shell
        s0 = S[2]
        stk(c, 'flame2', W*0.5 + jx, 1520 + jy + 10*math.sin(tq*20), 0.8, jr*2, f.k(B[2] + 0.1, B[2] + 0.35), maxd=460)
        stk(c, 'pot2', W*0.5 + jx, 1230 + jy, 1.0, jr, f.k(B[2] + 0.2, B[2] + 0.45), maxd=600)
        kernel(c, W*0.5 + jx + 6*math.sin(tq*40)*f.k(s0 + 1.5, s0 + 2.5), 830 + jy, 150, jr, f.k(s0 + 0.4, s0 + 0.65), glow=f.k(s0 + 0.6, s0 + 2.0))
        for i in range(3):
            cloud(c, W*0.5 + (i - 1)*55, 800 + (i % 2)*40 + 6*math.sin(tq*7 + i), 34, STEAM, f.k(s0 + 0.9 + i*.15, s0 + 1.2 + i*.15), seed=i, a=0.85)
        if tq > s0 + 1.9: stamp(c, "TRAPPED!", W*0.5, 640, 100, -6, f.k(s0 + 1.9, s0 + 2.15))
        label(c, "HEAT makes STEAM", W/2, 330, 100, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.1, s0 + 0.35), seed=5)
        label(c, "super TOUGH shell", W/2 + 15, 470, 90, 3 - jr*.5, k=f.k(s0 + 2.9, s0 + 3.15), seed=6)
    elif b == 3:  # pressure builds ... POP
        s0 = S[3]; tp = s0 + 2.85
        if tq < tp:
            g = f.k(s0, tp); sh = 22 * g * math.sin(tq * 60)
            kernel(c, W*0.5 + jx + sh, 1150 + jy, 180 + 50*g, jr + sh*.4, f.k(B[3] + 0.1, B[3] + 0.35), glow=0.6 + 0.4*g)
            for i in range(4):
                a = i * math.pi / 2 + 0.6
                arrow(c, W*0.5 + 330*math.cos(a), 1150 + 330*math.sin(a), 120, math.degrees(a) + 180, f.k(s0 + 0.3 + i*.12, s0 + 0.6 + i*.12), col=(1, .45, .2))
            stk(c, 'flame2', W*0.5 + jx, 1640 + jy + 10*math.sin(tq*20), 0.55, jr*2, f.k(B[3] + 0.2, B[3] + 0.45), maxd=420)
            label(c, "PRESSURE builds...", W/2, 330, 90, -2 + jr*.5, k=f.k(s0 + 0.1, s0 + 0.35), seed=7)
        else:
            rays(c, W/2, 1150, 1100, YEL, tq*30, f.k(tp, tp + 0.2), a=0.45)
            stk(c, 'popcorn_bowl', W*0.5 + jx, 1300 + jy, 0.9, jr, f.k(tp + 0.05, tp + 0.3), maxd=560)
            puffs(c, tq, tp, n=9, seed=3, cy=1050)
            stamp(c, "POP!", W*0.5, 820, 170, -8, f.k(tp, tp + 0.25))
            label(c, "PRESSURE builds...", W/2, 330, 90, -2 + jr*.5, k=1, seed=7)
            label(c, "the SHELL BURSTS!", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=YEL, k=f.k(tp + 1.0, tp + 1.25), seed=8)
    elif b == 4:  # starch -> fluffy foam, inside out
        s0 = S[4]
        stk(c, 'popcorn_bowl', W*0.42 + jx, 1250 + jy, 1.05, 4*math.sin(tq*3) + jr, f.k(B[4] + 0.1, B[4] + 0.35), maxd=620)
        stk(c, 'kernel_b', W*0.78 + jx, 860 + jy, 0.7, 10 + jr, f.k(s0 + 1.3, s0 + 1.55), maxd=460)
        cloud(c, W*0.18, 860, 100, (1, .97, .85), f.k(s0 + 1.0, s0 + 1.3), seed=4)
        if tq > s0 + 4.3: stamp(c, "INSIDE OUT!", W*0.5, 1620, 100, 5, f.k(s0 + 4.3, s0 + 4.55), col=(.1, .45, .95))
        label(c, "STARCH puffs up", W/2, 330, 96, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=9)
        label(c, "into FLUFFY FOAM", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=(1, .97, .85), k=f.k(s0 + 2.3, s0 + 2.55), seed=10)
    else:         # tip: sealed jar
        s0 = S[5]
        stk(c, 'popcorn', W*0.36 + jx, 1180 + jy, 1.0, -6 + jr, f.k(s0 + 0.1, s0 + 0.35), maxd=560)
        if tq > s0 + 1.5: stamp(c, "SEALED", W*0.36, 1520, 90, -6, f.k(s0 + 1.5, s0 + 1.75), col=(.1, .6, .3))
        kernel(c, W*0.76 + jx, 1060 + jy, 120, 14 + jr, f.k(s0 + 2.6, s0 + 2.85), glow=0.0)
        if tq > s0 + 3.6: stamp(c, "DRY = NO POP", W*0.66, 1330, 70, 7, f.k(s0 + 3.6, s0 + 3.85))
        label(c, "TIP: keep them SEALED", W/2, 330, 80, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.1, s0 + 0.35), seed=11)
        label(c, "DRIED OUT = won't pop", W/2 + 15, 470, 80, 3 - jr*.5, k=f.k(s0 + 2.7, s0 + 2.95), seed=12)

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.4); K.sfx(0.35, 'pop', 0.6); K.sfx(0.5, 'pop', 0.6); K.sfx(1.15, 'pop', 0.8); K.sfx(1.2, 'sparkle1', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.3, 'pop', 0.6); K.sfx(S[1] + 0.6, 'pop', 0.5); K.sfx(S[1] + 1.6, 'bubble', 0.6); K.sfx(S[1] + 1.65, 'pop', 0.6)
K.sfx(B[2] + 0.1, 'whoosh', 0.5); K.sfx(B[2] + 0.2, 'pop', 0.6); K.sfx(S[2] + 0.4, 'pop', 0.6); K.sfx(S[2] + 0.9, 'splash2', 0.3); K.sfx(S[2] + 2.9, 'pop', 0.6); K.sfx(S[2] + 1.9, 'impact1', 0.9)
K.sfx(B[3] + 0.1, 'pop', 0.6); K.sfx(S[3] + 0.3, 'swoosh3', 0.5); K.sfx(S[3] + 0.8, 'scratch2', 0.4)
for i in range(6): K.sfx(S[3] + 2.85 + i * 0.09, 'pop', 0.9 - i * 0.08)
K.sfx(S[3] + 2.85, 'impact2', 0.9); K.sfx(S[3] + 3.85, 'pop', 0.6)
K.sfx(B[4] + 0.1, 'pop', 0.7); K.sfx(S[4] + 0.2, 'pop', 0.6); K.sfx(S[4] + 1.0, 'sparkle2', 0.5); K.sfx(S[4] + 2.3, 'pop', 0.6); K.sfx(S[4] + 4.3, 'impact1', 0.8)
K.sfx(S[5] + 0.1, 'pop', 0.7); K.sfx(S[5] + 1.5, 'impact2', 0.6); K.sfx(S[5] + 2.6, 'pop', 0.7); K.sfx(S[5] + 2.7, 'pop', 0.6); K.sfx(S[5] + 3.6, 'impact1', 0.8)
K.sfx(S[5] + 3.65, 'ding1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p15_popcorn')

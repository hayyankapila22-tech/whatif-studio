"""P16 — How does your heart beat all by itself? (PAPER-CUTOUT format) — educational only, not medical advice.
Facts (plain words, no studies): the heartbeat doesn't need the brain to start it. A small patch of special cells in
the top right of the heart (the sinoatrial / SA node, the heart's natural pacemaker) fires an electrical signal on its
own. At rest that happens about 60-100 times a minute (roughly once a second). The signal spreads across the top
chambers first (they squeeze), passes a relay point, then spreads through the bottom chambers (they squeeze and pump
blood out). That adds up to roughly 100,000 beats a day. The brain/nerves only speed it up or slow it down.
Sources: Michigan Medicine / HealthLinkBC "Electrical System of the Heart"; Science News Explores "Explainer: Anatomy
of a heartbeat"; HowStuffWorks "What makes your heart beat?"; American Heart Association (about 100,000 beats a day).
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['pink', 'navy', 'blue', 'teal', 'purple', 'orange'], shakes=[S[2] + 1.5, S[5] + 1.5], voice_files=VO, music=MUSIC)
B = K.B
PINK = (1, .75, .82)
def has(n): return os.path.exists(os.path.join(LIB, n + '.png'))

def beat(t, period=0.85, amp=0.09):
    """lub-dub pulse factor"""
    p = (t % period) / period
    return 1 + amp * (math.exp(-((p - 0.05) / 0.05) ** 2) + 0.6 * math.exp(-((p - 0.25) / 0.05) ** 2))

def zzz(c, x, y, tq, k):
    if k <= 0: return
    for i in range(3):
        ph = (tq * 0.8 + i / 3) % 1
        font = skia.Font(FONT, 70 + i * 22); a = min(1, k) * (1 - ph)
        c.drawString('Z', x + i * 50 + ph * 40, y - i * 70 - ph * 60, font, skia.Paint(Color=skia.Color4f(1, 1, 1, a), AntiAlias=True))

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook
        rays(c, W/2, 1150, 1100, WHT, tq*12, f.k(0.05, 0.45), a=0.25)
        stk(c, 'human_heart2', W*0.5 + jx, 1150 + jy, 1.15*beat(t), -4 + jr, f.k(0.0, 0.3), maxd=640)
        glyph(c, '?', 170, 1550, 150, -12 + jr*2, f.k(0.5, 0.75))
        stk(c, 'stethoscope2', W*0.76 + jx, 1600 + jy, 0.6, 14 + jr, f.k(0.4, 0.65), maxd=440)
        label(c, "how does your HEART", W/2 + jx*.4, 330, 82, -3 + jr*.5, k=f.k(0.1, 0.35), seed=1)
        label(c, "BEAT BY ITSELF?", W/2 + 10, 470, 96, 2 - jr*.5, bgcol=PINK, k=f.k(1.2, 1.45), seed=2)
    elif b == 1:  # no thinking, even asleep
        s0 = S[1]
        stk(c, 'brain', W*0.33 + jx, 900 + jy, 0.75, -8 + jr, f.k(B[1] + 0.1, B[1] + 0.35), maxd=460)
        if tq > s0 + 0.9: stamp(c, "NOT NEEDED", W*0.33, 1140, 64, -8, f.k(s0 + 0.9, s0 + 1.15))
        stk(c, 'sleeping_cat', W*0.6 + jx, 1400 + jy, 1.0, 4 + jr, f.k(s0 + 1.7, s0 + 1.95), maxd=560)
        zzz(c, W*0.72, 1220, tq, f.k(s0 + 2.0, s0 + 2.3))
        label(c, "NO thinking needed", W/2, 330, 88, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=3)
        label(c, "even ASLEEP!", W/2 + 15, 470, 100, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.4, s0 + 2.65), seed=4)
    elif b == 2:  # its own spark maker = natural pacemaker
        s0 = S[2]
        stk(c, 'human_heart3', W*0.5 + jx, 1180 + jy, 1.1*beat(t), jr, f.k(B[2] + 0.1, B[2] + 0.35), maxd=640)
        fl = 0.8 + 0.25*abs(math.sin(tq*14))
        rays(c, W*0.34, 860, 260, YEL, tq*40, f.k(s0 + 1.5, s0 + 1.8), n=10, a=0.55)
        bolt(c, W*0.34 + jx, 860 + jy, fl, -10, f.k(s0 + 1.5, s0 + 1.75))
        arrow(c, W*0.12, 1000, 150, -40, f.k(s0 + 1.8, s0 + 2.1), col=YEL)
        stk(c, 'battery', W*0.8 + jx, 820 + jy, 0.5, 10 + jr, f.k(s0 + 0.5, s0 + 0.75), maxd=380)
        if tq > s0 + 3.2: stamp(c, "BUILT IN!", W*0.6, 1680, 90, 5, f.k(s0 + 3.2, s0 + 3.45), col=(.1, .45, .95))
        label(c, "its OWN SPARK MAKER", W/2, 330, 82, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 1.2, s0 + 1.45), seed=5)
        label(c, "a natural PACEMAKER", W/2 + 15, 470, 84, 3 - jr*.5, k=f.k(s0 + 2.6, s0 + 2.85), seed=6)
    elif b == 3:  # electric signal about once a second
        s0 = S[3]
        stk(c, 'stopwatch', W*0.74 + jx, 860 + jy, 0.6, 10 + jr, f.k(s0 + 1.4, s0 + 1.65), maxd=400)
        stk(c, 'human_heart2', W*0.42 + jx, 1250 + jy, 0.95*beat(t - s0, 1.0, 0.1), -4 + jr, f.k(B[3] + 0.1, B[3] + 0.35), maxd=600)
        ph = ((tq - s0) % 1.0)
        if tq > s0 + 0.5 and ph < 0.35: bolt(c, W*0.3 + jx, 980 + jy, 0.7, -12, 1)
        if tq > s0 + 2.2: stamp(c, "1x / SECOND", W*0.55, 1680, 80, -5, f.k(s0 + 2.2, s0 + 2.45))
        label(c, "a tiny ELECTRIC signal", W/2, 330, 78, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.5, s0 + 0.75), seed=7)
        label(c, "about once a SECOND", W/2 + 15, 470, 84, 3 - jr*.5, k=f.k(s0 + 1.6, s0 + 1.85), seed=8)
    elif b == 4:  # spreads, squeezes top first then bottom
        s0 = S[4]
        # squeeze cycle: top half (0-0.3), bottom half (0.35-0.65)
        ph = ((tq - s0) % 1.2) / 1.2
        sqt = math.exp(-((ph - 0.12) / 0.08) ** 2); sqb = math.exp(-((ph - 0.48) / 0.1) ** 2)
        img, sh, cw, ch, _ = sticker('human_heart3', 620)
        k = f.k(B[4] + 0.1, B[4] + 0.35)
        if k > 0:
            s = back(min(1, k)); cx, cy = W*0.5 + jx, 1180 + jy
            for half, sq in ((0, sqt), (1, sqb)):
                c.save(); c.translate(cx, cy); c.scale(s, s)
                c.clipRect(skia.Rect.MakeLTRB(-cw, -ch/2 - 40 if half == 0 else -ch*0.08, cw, -ch*0.08 if half == 0 else ch/2 + 40))
                c.scale(1 - 0.07*sq, 1 - 0.07*sq); c.translate(-cw/2, -ch/2)
                if half == 0:
                    c.save(); c.translate(12, 20); c.drawImage(sh, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(ImageFilter=skia.ImageFilters.Blur(12, 12), Alphaf=0.42)); c.restore()
                c.drawImage(img, 0, 0, skia.SamplingOptions(skia.CubicResampler.Mitchell())); c.restore()
        stk(c, 'stethoscope2', W*0.8 + jx, 1650 + jy, 0.55, -10 + jr, f.k(s0 + 0.6, s0 + 0.85), maxd=420)
        a1 = f.k(s0 + 2.6, s0 + 2.9); a2 = f.k(s0 + 4.0, s0 + 4.3)
        arrow(c, W*0.88, 880, 200, 180, a1, col=YEL); arrow(c, W*0.88, 1420, 200, 180, a2, col=(1, .45, .3))
        if tq > s0 + 2.6: stamp(c, "1. TOP", W*0.18, 900, 64, -8, a1, col=(.1, .45, .95))
        if tq > s0 + 4.0: stamp(c, "2. BOTTOM", W*0.22, 1640, 64, 6, a2)
        label(c, "the signal SPREADS", W/2, 330, 86, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=9)
        label(c, "and it SQUEEZES!", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=PINK, k=f.k(s0 + 2.0, s0 + 2.25), seed=10)
    else:         # ~100,000 beats a day
        s0 = S[5]
        stk(c, 'alarm_clock', W*0.28 + jx, 880 + jy, 0.62, -8 + jr, f.k(s0 + 0.1, s0 + 0.35), maxd=420)
        stk(c, 'human_heart2', W*0.68 + jx, 1180 + jy, 0.85*beat(t, 0.6, 0.12), 6 + jr, f.k(s0 + 0.3, s0 + 0.55), maxd=560)
        stk(c, 'drum', W*0.24 + jx, 1340 + jy, 0.7, 6 + jr, f.k(s0 + 0.6, s0 + 0.85), maxd=440)
        if tq > s0 + 1.5: stamp(c, "100,000!", W*0.5, 1700, 130, -6, f.k(s0 + 1.5, s0 + 1.75))
        label(c, "~100,000 BEATS", W/2, 330, 100, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.5, s0 + 0.75), seed=11)
        label(c, "EVERY. SINGLE. DAY.", W/2 + 15, 470, 86, 3 - jr*.5, bgcol=PINK, k=f.k(s0 + 1.8, s0 + 2.05), seed=12)

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.5); K.sfx(0.5, 'pop', 0.6); K.sfx(1.2, 'pop', 0.8); K.sfx(1.25, 'sparkle1', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.2, 'pop', 0.6); K.sfx(S[1] + 0.9, 'impact1', 0.8); K.sfx(S[1] + 1.7, 'pop', 0.6); K.sfx(S[1] + 2.4, 'pop', 0.6); K.sfx(S[1] + 2.0, 'sparkle2', 0.4)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 1.2, 'pop', 0.6); K.sfx(S[2] + 1.5, 'scratch1', 0.5); K.sfx(S[2] + 1.5, 'impact2', 0.7); K.sfx(S[2] + 1.55, 'sparkle1', 0.5); K.sfx(S[2] + 1.8, 'swoosh3', 0.4); K.sfx(S[2] + 2.6, 'pop', 0.6); K.sfx(S[2] + 3.2, 'impact1', 0.8)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.5, 'pop', 0.6); K.sfx(S[3] + 1.4, 'pop', 0.6); K.sfx(S[3] + 1.6, 'pop', 0.6); K.sfx(S[3] + 2.2, 'impact2', 0.7)
for i in range(1, 4): K.sfx(S[3] + i * 1.0, 'snip', 0.35)
K.sfx(B[4] + 0.1, 'pop', 0.7); K.sfx(S[4] + 0.2, 'pop', 0.6); K.sfx(S[4] + 2.0, 'pop', 0.6); K.sfx(S[4] + 2.6, 'impact2', 0.6); K.sfx(S[4] + 4.0, 'impact2', 0.6)
K.sfx(S[5] + 0.1, 'pop', 0.7); K.sfx(S[5] + 0.3, 'pop', 0.6); K.sfx(S[5] + 0.6, 'pop', 0.6); K.sfx(S[5] + 0.5, 'pop', 0.6); K.sfx(S[5] + 1.5, 'impact1', 0.9); K.sfx(S[5] + 1.55, 'ding2', 0.5); K.sfx(S[5] + 1.8, 'pop', 0.7)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p16_heartbeat')

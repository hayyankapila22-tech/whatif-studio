"""P07 — How do noise-cancelling headphones make the world go quiet? (PAPER-CUTOUT format)
Facts (plain words, no studies): active noise cancelling uses small microphones on the outside of the ear cups that
constantly pick up the surrounding sound; a chip creates a mirror-image ("opposite", inverted) sound wave and plays it
through the speakers; the peaks of one meet the dips of the other and they cancel out (destructive interference) —
so the headphones actually ADD sound to make quiet; it works best on steady, low, predictable sounds (plane/train
engines, air-conditioning hum); sudden or higher sounds like voices are harder to predict and partly get through
(the padding blocks some of the high sounds passively).
Sources: HowStuffWorks "How noise-canceling headphones work"; Sonos blog "How does noise canceling work?";
SoundGuys "How do noise cancelling headphones work?"; Science Focus "How do noise-cancelling headphones work?".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['blue', 'pink', 'mint', 'navy', 'orange', 'purple'], shakes=[S[1] + 1.4, S[3] + 2.6, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
NOISE = (1.0, .35, .35); ANTI = (.25, .75, 1.0)

def wave(c, x0, x1, y, amp, ph, col, k, wl=180, w=26):
    """Paper sound wave (thick sine strip with a white border), drawn from x0 to x0 + (x1-x0)*k."""
    if k <= 0: return
    xe = lerp(x0, x1, eo(min(1, k))); p = skia.Path(); n = max(2, int((xe - x0) / 8))
    for i in range(n + 1):
        x = x0 + (xe - x0) * i / n; yy = y + amp * math.sin((x - x0) / wl * 2 * math.pi + ph)
        (p.moveTo if i == 0 else p.lineTo)(x, yy)
    c.drawPath(off(p, 6, 10), skia.Paint(Color=skia.Color4f(0, 0, 0, .28), Style=skia.Paint.kStroke_Style, StrokeWidth=w + 18, AntiAlias=True, StrokeCap=skia.Paint.kRound_Cap, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(.98, .98, .96, 1), Style=skia.Paint.kStroke_Style, StrokeWidth=w + 18, AntiAlias=True, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(*col, 1), Style=skia.Paint.kStroke_Style, StrokeWidth=w, AntiAlias=True, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join))

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook: headphones, noisy world
        rays(c, W/2, 1080, 1100, WHT, tq*12, f.k(0.05, 0.45))
        wave(c, 80, 1000, 1500, 60, -tq*10, NOISE, f.k(0.3, 0.9), wl=160)
        stk(c, 'headphones', W/2 + jx, 1020 + jy, 1.2, jr - 4, f.k(0.0, 0.3), maxd=640)
        glyph(c, '?', 160, 780, 140, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 930, 760, 120, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "NOISE-CANCELLING", W/2 + jx*.4, 330, 88, -3 + jr*.5, k=f.k(0.15, 0.4), seed=1)
        label(c, "how do they WORK?", W/2 + 10, 470, 90, 2 - jr*.5, bgcol=YEL, k=f.k(0.8, 1.05), seed=2)
    elif b == 1:  # plot twist: they ADD sound
        s0 = S[1]
        stk(c, 'headphones', W*0.36 + jx, 1060 + jy, 0.95, -8 + jr, f.k(B[1] + 0.1, B[1] + 0.4), maxd=520)
        boom = 1 + 0.05*abs(math.sin(tq*14)) if tq > s0 + 1.4 else 1
        stk(c, 'megaphone', W*0.70 + jx, 1480 + jy, 0.95*boom, -16 + jr*2, f.k(s0 + 1.3, s0 + 1.55), maxd=460)
        if tq > s0 + 1.4: stamp(c, "MORE SOUND?!", W*0.46, 1760, 100, -6, f.k(s0 + 1.4, s0 + 1.65))
        label(c, "PLOT TWIST...", W/2, 330, 96, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=3)
        label(c, "they ADD sound!", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 1.4, s0 + 1.65), seed=4)
    elif b == 2:  # tiny mics on the outside listen to the noise
        s0 = S[2]
        stk(c, 'airplane', W*0.30 + jx, 880 + jy, 0.9, -8 + jr, f.k(s0 + 1.6, s0 + 1.85), maxd=480)
        wave(c, 120, 640, 1300, 55, -tq*10, NOISE, f.k(s0 + 1.8, s0 + 2.6), wl=150)
        stk(c, 'microphone', W*0.74 + jx, 1320 + jy, 0.9, 6 + jr, f.k(B[2] + 0.1, B[2] + 0.4), maxd=480)
        glyph(c, '!', 900, 900, 120, 10 + jr*2, f.k(s0 + 2.4, s0 + 2.6))
        label(c, "tiny MICS outside", W/2, 330, 92, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=5)
        label(c, "LISTEN to the noise", W/2 + 15, 470, 86, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.6, s0 + 1.85), seed=6)
    elif b == 3:  # chip makes the opposite wave -> cancel -> silence
        s0 = S[3]
        stk(c, 'microchip', W*0.50 + jx, 760 + jy, 0.6, -4 + jr, f.k(B[3] + 0.1, B[3] + 0.4), maxd=420)
        merge = eio(f.k(s0 + 2.2, s0 + 2.8))
        amp = 70 * (1 - merge)
        wave(c, 110, 970, lerp(1150, 1350, merge), amp, -tq*8, NOISE, f.k(s0 + 0.2, s0 + 0.9))
        wave(c, 110, 970, lerp(1550, 1350, merge), amp, -tq*8 + math.pi, ANTI, f.k(s0 + 1.0, s0 + 1.7))
        if merge >= 1: wave(c, 110, 970, 1350, 0, 0, WHT, 1)
        if tq > s0 + 2.6: stamp(c, "SILENCE!", W/2, 1640, 130, -6, f.k(s0 + 2.6, s0 + 2.85), col=(.1, .45, .95))
        label(c, "the OPPOSITE wave", W/2, 330, 90, -2 + jr*.5, bgcol=ANTI, k=f.k(s0 + 1.0, s0 + 1.25), seed=7)
        label(c, "they CANCEL OUT!", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.2, s0 + 2.45), seed=8)
    elif b == 4:  # best on steady hums, voices sneak through
        s0 = S[4]
        stk(c, 'airplane', W*0.30 + jx, 900 + jy, 0.75, -6 + jr, f.k(B[4] + 0.1, B[4] + 0.4), maxd=420)
        stk(c, 'train', W*0.74 + jx, 940 + jy, 0.7, 6 + jr, f.k(s0 + 0.9, s0 + 1.1), maxd=400)
        sneak = eio(f.k(s0 + 2.4, s0 + 3.4))
        stk(c, 'parrot', lerp(-220, W*0.40, sneak) + jx, 1520 + jy, 0.9, -8 + 6*math.sin(tq*10) + jr, f.k(s0 + 2.3, s0 + 2.5), maxd=440)
        if tq > s0 + 2.9: glyph(c, '!', W*0.74, 1440, 150, 10 + jr*2, f.k(s0 + 2.9, s0 + 3.1), col=RED)
        label(c, "BEST on steady HUMS", W/2, 330, 84, -2 + jr*.5, k=f.k(s0 + 0.3, s0 + 0.55), seed=9)
        label(c, "VOICES sneak through!", W/2 + 15, 470, 80, 3 - jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 2.4, s0 + 2.65), seed=10)
    else:         # payoff: you still hear your name
        s0 = S[5]
        rays(c, W/2, 1150, 1100, WHT, tq*8, f.k(B[5] + 0.2, B[5] + 0.6), a=0.3)
        stk(c, 'headphones', W*0.30 + jx, 1100 + jy, 0.8, -10 + jr, f.k(s0 + 0.2, s0 + 0.45), maxd=440)
        stk(c, 'megaphone', W*0.72 + jx, 1060 + jy, 0.85, 14 + jr*2, f.k(s0 + 1.2, s0 + 1.45), maxd=420)
        label(c, "you still HEAR", W/2, 330, 96, -2 + jr*.5, k=f.k(s0 + 0.4, s0 + 0.65), seed=11)
        label(c, "someone call your NAME", W/2 + 15, 470, 74, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.3, s0 + 1.55), seed=12)
        if tq > DUR - 1.5: stamp(c, "BUSTED!", W/2, 1550, 140, -6, f.k(DUR - 1.5, DUR - 1.25))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.5); K.sfx(0.3, 'whoosh', 0.5); K.sfx(0.35, 'pop', 0.6); K.sfx(0.55, 'pop', 0.6); K.sfx(0.8, 'pop', 0.7); K.sfx(1.0, 'ding2', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.2, 'pop', 0.7); K.sfx(S[1] + 1.3, 'pop', 0.7); K.sfx(S[1] + 1.4, 'impact1', 0.9); K.sfx(S[1] + 1.45, 'scratch1', 0.6)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.2, 'pop', 0.6); K.sfx(S[2] + 1.6, 'pop', 0.7); K.sfx(S[2] + 1.8, 'whoosh', 0.6); K.sfx(S[2] + 2.4, 'ding1', 0.5)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.2, 'swoosh3', 0.6); K.sfx(S[3] + 1.0, 'swoosh3', 0.6); K.sfx(S[3] + 1.0, 'pop', 0.6); K.sfx(S[3] + 2.2, 'pop', 0.6)
K.sfx(S[3] + 2.6, 'impact1', 0.9); K.sfx(S[3] + 2.65, 'sparkle1', 0.6)
K.sfx(B[4] + 0.1, 'pop', 0.7); K.sfx(S[4] + 0.3, 'pop', 0.6); K.sfx(S[4] + 0.9, 'pop', 0.7); K.sfx(S[4] + 2.3, 'swoosh1', 0.6); K.sfx(S[4] + 2.4, 'pop', 0.7); K.sfx(S[4] + 2.9, 'ding2', 0.6)
K.sfx(S[5] + 0.2, 'pop', 0.7); K.sfx(S[5] + 0.4, 'pop', 0.6); K.sfx(S[5] + 1.2, 'pop', 0.7); K.sfx(S[5] + 1.3, 'pop', 0.6); K.sfx(S[5] + 1.35, 'ding1', 0.4)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p07_noise_cancelling')

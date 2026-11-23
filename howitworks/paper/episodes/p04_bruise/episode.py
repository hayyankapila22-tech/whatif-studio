"""P04 — Why do bruises change colour? (PAPER-CUTOUT format) — educational only, not medical advice.
Facts (plain words, no studies): a knock breaks tiny blood vessels (capillaries) under the skin and blood leaks into the
tissue; fresh trapped blood looks red, then darkens to purple/blue as it loses oxygen; the body breaks the red pigment
(haemoglobin) down step by step — first into a green pigment (biliverdin), then a yellow one (bilirubin), then a
golden-brown one (haemosiderin) — while clean-up cells clear it away; most bruises fade within about 2 weeks;
first aid: a cold compress / ice pack wrapped in a towel (never ice straight on skin) for ~10–20 min right after the
knock limits the bleeding and swelling.
Sources: NHS "Bruises" (nhs.uk/conditions/bruises); Cleveland Clinic "Bruise colors"; Science Focus "What causes the
diverse colouring of bruises?"; The Scientist "What makes bruises change color over time?".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['pink', 'navy', 'yellow', 'purple', 'teal', 'blue'], shakes=[S[1] + 0.25, DUR - 1.3], voice_files=VO, music=MUSIC)
B = K.B
C_RED, C_PUR, C_BLU = (.85, .12, .18), (.50, .16, .55), (.22, .24, .70)
C_GRN, C_YEL, C_BRN = (.42, .66, .22), (.96, .82, .25), (.58, .40, .22)
SKIN = (.96, .80, .68)

def bruise(c, x, y, R, col, k, seed=3):
    blob(c, x, y, R, SKIN, 0, k, seed=seed + 50)
    blob(c, x + 6, y + 4, R * 0.62, col, 8, k, seed=seed)

def mix(a, b, t): return tuple(lerp(a[i], b[i], t) for i in range(3))

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook: rainbow of bruise colours
        rays(c, W/2, 1050, 1100, WHT, tq*12, f.k(0.05, 0.45))
        stk(c, 'banana', W/2 + jx, 1290 + jy, 1.0, jr - 12, f.k(0.0, 0.35), maxd=620)
        for i, col in enumerate([C_RED, C_PUR, C_BLU, C_GRN, C_YEL, C_BRN]):
            ang = -150 + i * 24
            blob(c, W/2 + 400*math.cos(math.radians(ang)) + jx, 1250 + 420*math.sin(math.radians(ang)) + jy, 62, col, jr*3, f.k(0.3 + i*0.12, 0.5 + i*0.12), seed=i)
        stk(c, 'plaster', W*0.78 + jx, 1660 + jy, 0.65, 12 + jr, f.k(1.0, 1.25), maxd=380)
        glyph(c, '?', 170, 1600, 130, -12 + jr*2, f.k(0.9, 1.1))
        label(c, "WHY do BRUISES", W/2 + jx*.4, 330, 92, -3 + jr*.5, k=f.k(0.15, 0.4), seed=1)
        label(c, "change COLOUR?", W/2 + 10, 470, 92, 2 - jr*.5, bgcol=YEL, k=f.k(0.9, 1.15), seed=2)
    elif b == 1:  # bump -> tiny vessels break and leak
        s0 = S[1]
        stk(c, 'table', W*0.30 + jx, 1560 + jy, 1.0, -4 + jr, f.k(B[1] + 0.1, B[1] + 0.35), maxd=560)
        if tq < s0 + 1.1: stamp(c, "BUMP!", W*0.55, 1100, 150, -8, f.k(s0 + 0.2, s0 + 0.45))
        # a patch of skin with tiny vessels that snap and leak
        blob(c, W/2 + jx, 1010 + jy, 360, SKIN, 0, f.k(s0 + 1.0, s0 + 1.3), seed=53)
        for i in range(6):
            if tq < s0 + 1.2: break
            tp = s0 + 1.5 + i*0.2; brk = f.k(tp, tp + 0.15)
            x = 360 + (i % 3)*180 + jx; y = 900 + (i // 3)*220 + jy; ang = math.radians((i*47) % 70 - 35)
            gap = 22 * brk; dx, dy = math.cos(ang), math.sin(ang)
            pp = skia.Paint(Color=skia.Color4f(*C_RED, 1), StrokeWidth=16, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True)
            c.drawLine(x - 70*dx, y - 70*dy, x - gap*dx, y - gap*dy, pp); c.drawLine(x + gap*dx, y + gap*dy, x + 70*dx, y + 70*dy, pp)
            lk = f.k(tp + 0.1, tp + 1.4)
            for j in range(5):
                if lk > 0: c.drawCircle(x + (j - 2)*18*lk, y + 20 + j*14*lk, 14*lk*(1 - j*0.12), skia.Paint(Color=skia.Color4f(*C_RED, 0.9), AntiAlias=True))
        stk(c, 'magnifier', W*0.80 + jx, 1560 + jy, 0.8, 16 + jr, f.k(s0 + 1.2, s0 + 1.45), maxd=360)
        label(c, "tiny BLOOD VESSELS", W/2, 330, 80, -2 + jr*.5, k=f.k(s0 + 1.2, s0 + 1.45), seed=3)
        label(c, "BREAK and LEAK", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=C_RED, fg=WHT, k=f.k(s0 + 2.2, s0 + 2.45), seed=4)
    elif b == 2:  # red -> purple -> blue
        s0 = S[2]
        t1 = f.k(s0 + 1.4, s0 + 1.9); t2 = f.k(s0 + 2.3, s0 + 2.8)
        col = mix(mix(C_RED, C_PUR, t1), C_BLU, t2)
        bruise(c, W/2 + jx, 1050 + jy, 300, col, f.k(B[2] + 0.1, B[2] + 0.4))
        stk(c, 'crayons', W*0.24 + jx, 1560 + jy, 0.9, -10 + jr, f.k(s0 + 0.4, s0 + 0.65), maxd=380)
        stk(c, 'plaster', W*0.78 + jx, 1580 + jy, 0.7, 14 + jr, f.k(s0 + 0.8, s0 + 1.05), maxd=320)
        label(c, "RED at first...", W/2, 330, 92, -2 + jr*.5, bgcol=C_RED, fg=WHT, k=f.k(s0 + 0.3, s0 + 0.55), seed=5)
        label(c, "then PURPLE + BLUE", W/2 + 15, 470, 80, 3 - jr*.5, bgcol=(.72, .62, 1), k=f.k(s0 + 1.5, s0 + 1.75), seed=6)
    elif b == 3:  # body breaks it down -> green
        s0 = S[3]
        rays(c, W/2, 1050, 1100, WHT, tq*14, f.k(B[3] + 0.1, B[3] + 0.5))
        col = mix(C_BLU, C_GRN, f.k(s0 + 1.6, s0 + 2.2))
        bruise(c, W/2 + jx, 1060 + jy, 280, col, 1)
        stk(c, 'calendar', W*0.24 + jx, 1580 + jy, 0.8, -8 + jr, f.k(s0 + 0.5, s0 + 0.75), maxd=340)
        stk(c, 'banana', W*0.78 + jx, 1600 + jy, 0.7, 20 + jr, f.k(s0 + 1.0, s0 + 1.25), maxd=360)
        label(c, "your body BREAKS IT DOWN", W/2, 330, 66, -2 + jr*.5, k=f.k(s0 + 0.5, s0 + 0.75), seed=7)
        label(c, "it turns GREEN!", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=C_GRN, fg=WHT, k=f.k(s0 + 1.8, s0 + 2.05), seed=8)
    elif b == 4:  # yellow -> brown, clean-up crew
        s0 = S[4]
        t1 = f.k(s0 + 0.2, s0 + 0.7); t2 = f.k(s0 + 1.0, s0 + 1.5); fade_k = f.k(s0 + 2.3, S[4] + 3.4)
        col = mix(mix(C_GRN, C_YEL, t1), C_BRN, t2)
        bruise(c, W/2 + jx, 1020 + jy, lerp(270, 120, fade_k), col, 1)
        sweep = eio(f.k(s0 + 1.6, s0 + 3.0))
        stk(c, 'broom', lerp(-100, W*0.38, sweep) + jx, 1500 + jy, 0.9, -20 + 10*math.sin(tq*9) + jr, f.k(s0 + 1.5, s0 + 1.7), maxd=440)
        stk(c, 'vacuum', W*0.78 + jx, 1520 + jy, 0.8, 6 + jr, f.k(s0 + 1.9, s0 + 2.15), maxd=380)
        label(c, "YELLOW, then BROWN", W/2, 330, 82, -2 + jr*.5, bgcol=C_YEL, k=f.k(s0 + 0.2, s0 + 0.45), seed=9)
        label(c, "the CLEAN-UP crew!", W/2 + 15, 470, 84, 3 - jr*.5, bgcol=WHT, k=f.k(s0 + 1.6, s0 + 1.85), seed=10)
    else:         # tip: ice pack in a towel right after the bump
        s0 = S[5]
        rays(c, W/2, 1150, 1100, (.55, .85, 1), tq*8, f.k(B[5] + 0.2, B[5] + 0.6))
        stk(c, 'towel', W*0.34 + jx, 1180 + jy, 1.0, -6 + jr, f.k(s0 + 1.0, s0 + 1.3), maxd=520)
        stk(c, 'ice_cube', W*0.70 + jx, 1060 + jy, 0.9, 14 + jr, f.k(s0 + 0.7, s0 + 0.95), maxd=340)
        stk(c, 'ice_cube', W*0.80 + jx, 1330 + jy, 0.6, -18 + jr, f.k(s0 + 0.9, s0 + 1.15), maxd=300)
        label(c, "ICE PACK in a TOWEL", W/2, 330, 84, -2 + jr*.5, bgcol=(.55, .85, 1), k=f.k(s0 + 0.9, s0 + 1.15), seed=11)
        label(c, "RIGHT after the bump", W/2 + 15, 470, 80, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.1, s0 + 2.35), seed=12)
        label(c, "educational only, not medical advice", W/2, 1530, 34, 0, bgcol=WHT, k=f.k(s0 + 0.5, s0 + 0.7), seed=13)
        if tq > DUR - 1.3: stamp(c, "SMALLER!", W/2, 1420, 100, -6, f.k(DUR - 1.3, DUR - 1.05), col=RED)

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.0, 'sparkle1', 0.5)
for i in range(6): K.sfx(0.3 + i*0.12, 'pop', 0.5)
K.sfx(0.9, 'pop', 0.7); K.sfx(1.0, 'ding2', 0.6)
K.sfx(B[1] + 0.1, 'pop', 0.6); K.sfx(S[1] + 0.25, 'impact2', 1.0)
for i in range(6): K.sfx(S[1] + 1.3 + i*0.18, 'snip', 0.4)
K.sfx(S[1] + 1.2, 'pop', 0.7); K.sfx(S[1] + 2.2, 'pop', 0.7); K.sfx(S[1] + 2.4, 'bubble', 0.4)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.3, 'pop', 0.7); K.sfx(S[2] + 0.4, 'pop', 0.5); K.sfx(S[2] + 0.8, 'pop', 0.5); K.sfx(S[2] + 1.4, 'sparkle1', 0.4); K.sfx(S[2] + 1.5, 'pop', 0.7); K.sfx(S[2] + 2.3, 'sparkle1', 0.4)
K.sfx(S[3] + 0.5, 'pop', 0.7); K.sfx(S[3] + 1.0, 'pop', 0.6); K.sfx(S[3] + 1.6, 'sparkle2', 0.5); K.sfx(S[3] + 1.8, 'pop', 0.7)
K.sfx(S[4] + 0.2, 'pop', 0.7); K.sfx(S[4] + 1.0, 'sparkle1', 0.4); K.sfx(S[4] + 1.5, 'swoosh3', 0.6); K.sfx(S[4] + 1.6, 'pop', 0.7); K.sfx(S[4] + 1.9, 'pop', 0.6); K.sfx(S[4] + 2.2, 'scratch2', 0.4)
K.sfx(S[5] + 0.5, 'pop', 0.5); K.sfx(S[5] + 0.7, 'pop', 0.7); K.sfx(S[5] + 0.9, 'pop', 0.6); K.sfx(S[5] + 1.0, 'pop', 0.7); K.sfx(S[5] + 1.1, 'ding1', 0.4); K.sfx(S[5] + 2.1, 'pop', 0.7)
K.sfx(DUR - 1.3, 'impact1', 0.8); K.sfx(DUR - 1.2, 'sparkle1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p04_bruise')

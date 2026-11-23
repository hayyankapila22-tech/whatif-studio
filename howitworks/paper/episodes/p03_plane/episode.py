"""P03 — How does a giant plane actually stay up? (PAPER-CUTOUT format)
Facts (plain words, no studies): the "equal transit time" idea (air over the top must meet the air underneath at the
back) is a myth — the air over the top actually arrives earlier; a wing is tilted (angle of attack) and curved, so it
turns a big mass of air downwards, and pushing air down pushes the wing up (Newton's 3rd law) — same as a flat hand
tilted out of a car window; the air over the top speeds up and its pressure drops, so the higher pressure underneath
pushes the wing up too (two descriptions of the same flow); lift grows with speed, which is why planes need a fast
take-off run.
Sources: NASA Glenn "Beginner's Guide to Aeronautics" — Incorrect Lift Theory #1 (equal transit) and "What is Lift?";
Scientific American "No One Can Explain Why Planes Stay in the Air" (2020); explainthatstuff.com "How do planes fly?".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['teal', 'red', 'blue', 'orange', 'purple', 'mint'], shakes=[S[1] + 1.9, S[3] + 0.6, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
SKY = (.62, .85, 1)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook: giant plane in the clouds
        rays(c, W/2, 1050, 1150, WHT, tq*12, f.k(0.05, 0.45))
        for i, (cx, cy, R) in enumerate([(170, 1400, 120), (900, 1500, 140), (820, 760, 90)]):
            cloud(c, cx + jx + math.sin(tq*2 + i)*20, cy, R, WHT, f.k(0.1 + i*0.15, 0.4 + i*0.15), seed=i)
        stk(c, 'airplane', W/2 + jx, 1060 + jy + 20*math.sin(tq*3), 1.25, jr - 8, f.k(0.0, 0.35), maxd=760)
        stk(c, 'paper_plane', W*0.2 + jx, 1580 + jy, 0.7, 14 + jr, f.k(0.8, 1.05), maxd=300)
        glyph(c, '?', 150, 800, 140, -12 + jr*2, f.k(0.4, 0.65)); glyph(c, '?', 930, 700, 120, 14 - jr*2, f.k(0.65, 0.9))
        label(c, "HOW does a GIANT plane", W/2 + jx*.4, 330, 74, -3 + jr*.5, k=f.k(0.15, 0.4), seed=1)
        label(c, "stay UP?!", W/2 + 10, 470, 100, 2 - jr*.5, bgcol=YEL, k=f.k(1.0, 1.25), seed=2)
    elif b == 1:  # the school myth: air on top racing to catch up
        s0 = S[1]
        stk(c, 'books', W*0.3 + jx, 1380 + jy, 1.0, -6 + jr, f.k(B[1] + 0.15, B[1] + 0.45), maxd=520)
        stk(c, 'paper_plane', W*0.74 + jx, 780 + jy, 0.9, 10 + jr, f.k(s0 + 0.4, s0 + 0.7), maxd=440)
        # two racing arrows over/under an imaginary wing
        arrow(c, 110, 960, 500, -8, f.k(s0 + 1.0, s0 + 1.5), col=YEL)
        arrow(c, 110, 1050, 360, 4, f.k(s0 + 1.0, s0 + 1.5), col=SKY)
        if tq > s0 + 1.9: stamp(c, "MYTH!", W*0.64, 1620, 150, -10, f.k(s0 + 1.9, s0 + 2.15))
        label(c, "air on top must", W/2, 330, 84, -2 + jr*.5, k=f.k(s0 + 0.5, s0 + 0.75), seed=3)
        label(c, "'CATCH UP'?  NOPE!", W/2 + 15, 470, 84, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.6, s0 + 1.85), seed=4)
    elif b == 2:  # tilted, curved wing shoves air down
        s0 = S[2]
        rays(c, W/2, 950, 1000, WHT, -tq*10, f.k(B[2] + 0.2, B[2] + 0.6))
        stk(c, 'electric_fan', 190 + jx, 1500 + jy, 0.9, 8 + jr, f.k(B[2] + 0.2, B[2] + 0.45), maxd=340)
        stk(c, 'airplane', W/2 + 60 + jx, 880 + jy, 1.1, -14 + jr, f.k(B[2] + 0.1, B[2] + 0.4), maxd=700)
        for i in range(5):   # air pushed down under the wing
            ph = (tq - s0 - 0.9 - i*0.18)
            if ph > 0:
                yy = 1080 + (ph % 1.2) * 300
                arrow(c, 340 + i*120 + jx, yy, 150, 90, 1, col=SKY, w=30)
        label(c, "the wing is TILTED", W/2, 330, 82, -2 + jr*.5, k=f.k(s0 + 0.4, s0 + 0.65), seed=5)
        label(c, "shoves air DOWN", W/2 + 15, 470, 90, 3 - jr*.5, bgcol=SKY, k=f.k(s0 + 1.6, s0 + 1.85), seed=6)
    elif b == 3:  # air down = plane up, hand out of a car window
        s0 = S[3]
        rays(c, W/2, 1100, 1100, YEL, tq*20, f.k(B[3] + 0.1, B[3] + 0.5))
        stk(c, 'car', W*0.45 + jx, 1500 + jy, 1.15, jr, f.k(B[3] + 0.1, B[3] + 0.4), maxd=660)
        hy = 1080 - 140*eo(f.k(s0 + 0.6, s0 + 1.3)) + 15*math.sin(tq*7)
        stk(c, 'hand_pointing', W*0.40 + jx, hy + jy, 0.95, -12 + jr*2, f.k(s0 + 0.2, s0 + 0.45), maxd=400)
        arrow(c, W*0.82 + jx, hy - 40, 220, -90, f.k(s0 + 0.6, s0 + 0.9), col=YEL, w=44)
        arrow(c, W*0.40 + jx, hy + 110, 170, 90, f.k(s0 + 0.3, s0 + 0.6), col=SKY, w=34)
        for i in range(3):
            ph = (tq - s0 - 0.4 - i*0.25)
            if ph > 0: arrow(c, -180 + ((ph*900) % 640), hy - 50 + i*60, 150, 0, 1, col=WHT, w=18)
        label(c, "air DOWN = plane UP!", W/2, 330, 82, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.5, s0 + 0.75), seed=7)
        label(c, "like your HAND out a car window", W/2 + 10, 470, 56, 3 - jr*.5, bgcol=WHT, k=f.k(s0 + 1.7, s0 + 1.95), seed=8)
    elif b == 4:  # fast air on top = low pressure = sucked up
        s0 = S[4]
        stk(c, 'airplane', W/2 + jx, 1180 - 90*eio(f.k(s0 + 2.3, s0 + 3.2)) + jy, 1.15, -6 + jr, f.k(B[4] + 0.15, B[4] + 0.45), maxd=720)
        for i in range(4):   # fast streaks over the top
            ph = (tq - s0 - 0.5 - i*0.25)
            if ph > 0:
                xx = -200 + ((ph * 900) % 1500)
                arrow(c, xx, 820 + i*45, 240, 0, 1, col=WHT, w=22)
        stk(c, 'magnifier', W*0.80 + jx, 1640 + jy, 0.8, 18 + jr, f.k(s0 + 2.0, s0 + 2.3), maxd=340)
        label(c, "FAST air on top", W/2, 330, 90, -2 + jr*.5, k=f.k(s0 + 0.6, s0 + 0.85), seed=9)
        label(c, "LOW pressure = SUCKED UP", W/2 + 15, 470, 66, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.2, s0 + 2.45), seed=10)
    else:         # speed: take-off run
        s0 = S[5]
        rays(c, W/2, 1150, 1100, (.5, .4, 1), tq*8, f.k(B[5] + 0.2, B[5] + 0.6))
        stk(c, 'speedometer', W*0.24 + jx, 1580 + jy, 0.85, -6 + jr, f.k(s0 + 0.3, s0 + 0.55), maxd=380)
        up = eio(f.k(s0 + 2.0, DUR - 0.3))
        stk(c, 'airplane', lerp(W*0.58, W*0.72, up) + jx, lerp(1180, 820, up) + jy, 0.85, lerp(10, 25, up) + jr, f.k(B[5] + 0.1, B[5] + 0.35), maxd=640)
        stk(c, 'clock', W*0.84 + jx, 1520 + jy, 0.6, 10 + jr, f.k(s0 + 1.0, s0 + 1.25), maxd=240)
        label(c, "NO SPEED = NO LIFT", W/2, 330, 86, -2 + jr*.5, bgcol=WHT, k=f.k(s0 + 0.8, s0 + 1.05), seed=11)
        label(c, "RACE down the runway!", W/2 + 15, 470, 74, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.2, s0 + 2.45), seed=12)
        if tq > DUR - 1.5: stamp(c, "LIFT OFF!", W*0.56, 1360, 110, -6, f.k(DUR - 1.5, DUR - 1.25), col=RED)

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.0, 'whoosh', 0.7); K.sfx(0.02, 'pop', 0.9); K.sfx(0.15, 'pop', 0.6); K.sfx(0.4, 'pop', 0.6); K.sfx(0.65, 'pop', 0.6); K.sfx(0.8, 'pop', 0.6); K.sfx(1.0, 'ding2', 0.6)
K.sfx(B[1] + 0.15, 'pop', 0.7); K.sfx(S[1] + 0.4, 'pop', 0.7); K.sfx(S[1] + 1.0, 'swoosh3', 0.6); K.sfx(S[1] + 1.6, 'pop', 0.7); K.sfx(S[1] + 1.9, 'impact1', 0.9); K.sfx(S[1] + 1.95, 'scratch1', 0.6)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(B[2] + 0.2, 'pop', 0.6); K.sfx(S[2] + 0.4, 'pop', 0.6)
for i in range(4): K.sfx(S[2] + 0.9 + i*0.3, 'swoosh1', 0.35)
K.sfx(S[2] + 1.6, 'pop', 0.7)
K.sfx(S[3] + 0.5, 'pop', 0.7); K.sfx(S[3] + 0.6, 'impact1', 0.8); K.sfx(S[3] + 0.65, 'sparkle1', 0.4); K.sfx(S[3] + 1.5, 'pop', 0.7); K.sfx(S[3] + 1.7, 'pop', 0.6); K.sfx(S[3] + 2.0, 'whoosh', 0.6)
K.sfx(B[4] + 0.15, 'pop', 0.7); K.sfx(S[4] + 0.5, 'whoosh', 0.6); K.sfx(S[4] + 0.6, 'pop', 0.6); K.sfx(S[4] + 2.0, 'pop', 0.6); K.sfx(S[4] + 2.2, 'pop', 0.7); K.sfx(S[4] + 2.6, 'swoosh3', 0.5); K.sfx(S[4] + 2.7, 'ding1', 0.4)
K.sfx(S[5] + 0.5, 'pop', 0.7); K.sfx(S[5] + 0.8, 'pop', 0.6); K.sfx(S[5] + 1.0, 'pop', 0.6); K.sfx(S[5] + 1.2, 'pop', 0.6); K.sfx(S[5] + 2.0, 'whoosh', 0.8); K.sfx(S[5] + 2.2, 'pop', 0.7)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle2', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p03_plane')

"""P09 — Why do cats purr? (PAPER-CUTOUT format)
Facts (plain words, no studies): cats purr with the muscles of the voice box (larynx), which twitch roughly 25–150 times a
second and open/close the gap between the vocal folds; air vibrates as the cat breathes IN and OUT, so the purr is nearly
continuous. Cats purr when content, but also when stressed, injured, frightened, giving birth or at the vet — it is
thought to soothe/calm them. Kittens can purr when only a few days old (used to signal to the mother while nursing).
Sources: Library of Congress "Everyday Mysteries: Why and how do cats purr?"; Scientific American "Why do cats purr?";
Cat Fanciers' Association "The how and why of cats' purrs"; Purina "Why do cats purr?"; WebMD Pets "Why cats purr".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['pink', 'navy', 'orange', 'teal', 'purple', 'yellow'], shakes=[S[1] + 0.6, S[4] + 0.4, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
PNK = (1.0, .55, .75); SKY = (.55, .85, 1.0)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook: cat + yarn
        rays(c, W/2, 1100, 1100, WHT, tq*12, f.k(0.05, 0.45))
        vib = 6*math.sin(tq*70)
        stk(c, 'cat', W/2 + jx + vib, 1080 + jy, 1.15, jr - 3, f.k(0.0, 0.3), maxd=640)
        stk(c, 'yarn_ball', W*0.74 + jx, 1560 + jy, 1.0, 12 + jr, f.k(0.6, 0.85), maxd=380)
        glyph(c, '?', 130, 700, 130, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 920, 820, 120, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "why do CATS", W/2 + jx*.4, 330, 96, -3 + jr*.5, k=f.k(0.1, 0.35), seed=1)
        label(c, "PURRRR?", W/2 + 10, 470, 110, 2 - jr*.5, bgcol=YEL, k=f.k(0.5, 0.75), seed=2)
    elif b == 1:  # not always happy
        s0 = S[1]
        stk(c, 'sleeping_cat', W*0.50 + jx, 1080 + jy, 1.0, -4 + jr, f.k(B[1] + 0.1, B[1] + 0.4), maxd=600)
        stk(c, 'heart', W*0.80 + jx, 800 + jy, 0.6, 12 + jr, f.k(s0 + 1.0, s0 + 1.25), maxd=320)
        if tq > s0 + 0.6: stamp(c, "NOT ALWAYS!", W*0.56, 1560, 100, -8, f.k(s0 + 0.6, s0 + 0.85))
        label(c, "PLOT TWIST!", W/2, 330, 104, -2 + jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 0.1, s0 + 0.35), seed=3)
        label(c, "not just HAPPY", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.0, s0 + 1.25), seed=4)
    elif b == 2:  # throat muscles twitch ~25x a second
        s0 = S[2]
        vib = 7*math.sin(tq*90)
        stk(c, 'cat', W*0.42 + jx + vib, 1150 + jy, 1.0, -4 + jr, f.k(B[2] + 0.1, B[2] + 0.4), maxd=580)
        for i in range(3):
            if tq > s0 + 0.8 + i*0.2: bolt(c, W*0.80 + i*40 - 40, 900 + i*170, 0.7, 15 - i*10 + jr*3, f.k(s0 + 0.8 + i*0.2, s0 + 1.0 + i*0.2))
        stk(c, 'stopwatch', W*0.78 + jx, 1580 + jy, 0.65, 10 + jr, f.k(s0 + 1.6, s0 + 1.85), maxd=360)
        label(c, "TINY throat MUSCLES", W/2, 330, 82, -2 + jr*.5, k=f.k(s0 + 0.3, s0 + 0.55), seed=5)
        label(c, "twitch 25x a SECOND!", W/2 + 10, 470, 76, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.6, s0 + 1.85), seed=6)
    elif b == 3:  # breath in AND out -> never stops
        s0 = S[3]
        br = 1 + 0.12*math.sin((tq - s0)*4.5)
        stk(c, 'lungs2', W/2 + jx, 1130 + jy, 1.0*br, -3 + jr, f.k(B[3] + 0.1, B[3] + 0.4), maxd=560)
        arrow(c, 90, 1620, 240, -40, f.k(s0 + 0.5, s0 + 0.9), col=SKY)
        arrow(c, W - 90, 1620, 240, -140, f.k(s0 + 1.3, s0 + 1.7), col=PNK)
        label(c, "IN", 260, 1440, 80, -6, bgcol=SKY, k=f.k(s0 + 0.6, s0 + 0.85), seed=14)
        label(c, "OUT", W - 260, 1440, 80, 6, bgcol=PNK, k=f.k(s0 + 1.4, s0 + 1.65), seed=15)
        label(c, "breath IN... and OUT!", W/2, 330, 82, -2 + jr*.5, k=f.k(s0 + 0.4, s0 + 0.65), seed=7)
        label(c, "NON-STOP purr!", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.2, s0 + 2.45), seed=8)
    elif b == 4:  # scared, hurt, vet -> calming
        s0 = S[4]
        stk(c, 'stethoscope2', W*0.30 + jx, 1050 + jy, 0.95, -8 + jr, f.k(s0 + 1.4, s0 + 1.65), maxd=480)
        stk(c, 'plaster', W*0.74 + jx, 1000 + jy, 0.8, 14 + jr, f.k(s0 + 0.9, s0 + 1.15), maxd=380)
        stk(c, 'cat', W*0.55 + jx, 1430 + jy, 0.85, 4 + jr, f.k(B[4] + 0.1, B[4] + 0.4), maxd=500)
        label(c, "SCARED? HURT? VET?", W/2, 330, 84, -2 + jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 0.4, s0 + 0.65), seed=9)
        label(c, "purring CALMS them", W/2 + 10, 470, 80, 3 - jr*.5, bgcol=SKY, k=f.k(s0 + 3.0, s0 + 3.25), seed=10)
    else:         # kittens purr at a few days old
        s0 = S[5]
        rays(c, W/2, 1150, 1100, WHT, tq*8, f.k(B[5] + 0.2, B[5] + 0.6), a=0.3)
        stk(c, 'kitten', W*0.48 + jx, 1150 + jy, 1.1, -4 + jr, f.k(s0 + 0.2, s0 + 0.45), maxd=600)
        stk(c, 'heart', W*0.80 + jx, 860 + jy, 0.55, 14 + jr, f.k(s0 + 1.6, s0 + 1.85), maxd=300)
        stk(c, 'calendar', W*0.24 + jx, 1520 + jy, 0.85, -10 + jr, f.k(s0 + 1.8, s0 + 2.05), maxd=340)
        label(c, "KITTENS purr", W/2, 330, 100, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.3, s0 + 0.55), seed=11)
        label(c, "at just a FEW DAYS old!", W/2 + 15, 470, 76, 3 - jr*.5, k=f.k(s0 + 1.8, s0 + 2.05), seed=12)
        if tq > DUR - 1.5: stamp(c, "AWW!", W*0.62, 1580, 130, 6, f.k(DUR - 1.5, DUR - 1.25), col=(.9, .2, .5))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.5); K.sfx(0.1, 'pop', 0.6); K.sfx(0.35, 'pop', 0.6); K.sfx(0.5, 'pop', 0.7); K.sfx(0.55, 'pop', 0.6); K.sfx(0.6, 'ding1', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.6, 'impact1', 1.0); K.sfx(S[1] + 0.65, 'scratch1', 0.6); K.sfx(S[1] + 1.0, 'pop', 0.6)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.3, 'pop', 0.6)
for i in range(3): K.sfx(S[2] + 0.8 + i*0.2, 'sparkle1' if i % 2 else 'bubble', 0.4)
K.sfx(S[2] + 1.6, 'pop', 0.7); K.sfx(S[2] + 1.65, 'ding2', 0.5)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.4, 'pop', 0.6); K.sfx(S[3] + 0.5, 'swoosh3', 0.5); K.sfx(S[3] + 1.3, 'swoosh3', 0.5); K.sfx(S[3] + 2.2, 'pop', 0.7); K.sfx(S[3] + 2.25, 'sparkle2', 0.4)
K.sfx(B[4] + 0.1, 'pop', 0.7); K.sfx(S[4] + 0.4, 'impact2', 0.8); K.sfx(S[4] + 0.9, 'pop', 0.7); K.sfx(S[4] + 1.4, 'pop', 0.7); K.sfx(S[4] + 3.0, 'pop', 0.6); K.sfx(S[4] + 3.05, 'ding1', 0.4)
K.sfx(S[5] + 0.2, 'pop', 0.7); K.sfx(S[5] + 0.3, 'pop', 0.6); K.sfx(S[5] + 1.6, 'pop', 0.6); K.sfx(S[5] + 1.8, 'pop', 0.7); K.sfx(S[5] + 1.85, 'sparkle2', 0.4)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p09_cat_purr')

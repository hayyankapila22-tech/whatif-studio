# remix.py <epdir> <seconds> <seed> : builds an original, subtle "mathematical" music bed and mixes it under sfx.wav -> mix.wav
import sys, wave, numpy as np
ep, T, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
SR = 44100; N = int(SR * T); t_all = np.arange(N) / SR
rng = np.random.default_rng(seed)
PI = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491"
SCALE = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21]          # pentatonic over two octaves: digit -> note
root = [57, 55, 53, 52, 50, 59][seed % 6]             # different key per episode
bpm = [96, 92, 100, 88, 104, 94][seed % 6]; beat = 60 / bpm
prog = [[0, 4, 7], [-3, 0, 4], [-7, -3, 0], [-5, -1, 2]]  # I – vi – IV – V
mf = lambda m: 440 * 2 ** ((m - 69) / 12)
out = np.zeros((N, 2))
def put(sig, t0, gain, pan=0.0):
    i = int(t0 * SR); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[:j - i] * gain; out[i:j, 0] += s * (1 - pan) * .7; out[i:j, 1] += s * (1 + pan) * .7
def tone(f, d, att=.006, dec=.45, harm=(1, .25, .08)):
    t = np.arange(int(d * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * f * (k + 1) * t * (1 + rng.normal(0, .0005))) for k, a in enumerate(harm))
    return s * np.minimum(1, t / att) * np.exp(-t / dec)
def pad(fs, d):
    t = np.arange(int(d * SR)) / SR; s = np.zeros(len(t))
    for f in fs:
        for det in (-.15, .15): s += np.sin(2 * np.pi * f * (1 + det / 100) * t)
    env = np.clip(np.minimum(t / 1.2, (d - t) / 1.2), 0, 1)
    return s * env / (len(fs) * 2) * (0.8 + 0.2 * np.sin(2 * np.pi * .15 * t))
bar = beat * 4; nb = int(T / bar) + 2
# pad + sub bass
for b in range(nb):
    ch = prog[b % 4]; t0 = b * bar
    put(pad([mf(root + c - 12) for c in ch], bar + 1.2), t0, .55)
    put(tone(mf(root - 24 + ch[0]), bar, att=.02, dec=1.2, harm=(1, .1)), t0, .5)
# melody: digits of pi, 8th notes, gentle ping-pong
k = 0; t0 = bar  # melody enters after one bar
while t0 < T:
    d = int(PI[k % len(PI)]); note = root + SCALE[d]
    vel = .22 if k % 4 == 0 else .14
    put(tone(mf(note + 12), .9), t0, vel, pan=(-.45 if k % 2 else .45))
    if k % 8 == 0: put(tone(mf(note + 24), .6, dec=.25, harm=(1,)), t0 + beat * .25, .05, pan=0)
    k += 1; t0 += beat / 2
# soft clock tick on each beat
tick = (lambda t: np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 90))(np.arange(int(.04 * SR)) / SR)
for b in range(int(T / beat)): put(tick, b * beat, .05 if b % 4 else .08, pan=.2)
# shape: fade in, fade out, normalise to a quiet background level
env = np.clip(t_all / 1.5, 0, 1) * np.clip((T - t_all) / 2.0, 0, 1)
out *= env[:, None]
rms = np.sqrt(np.mean(out ** 2)); out *= 0.045 / max(rms, 1e-9)   # ~ -27 dBFS RMS: subtle bed
# sound effects on top
with wave.open(f'{ep}/sfx.wav') as w:
    sfx = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float).reshape(-1, 2) / 32768
sfx = np.pad(sfx, ((0, max(0, N - len(sfx))), (0, 0)))[:N]
full = out + sfx * 0.9
pk = np.max(np.abs(full)); full = full / pk * 0.95 if pk > 0.95 else full
with wave.open(f'{ep}/mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((full * 32767).astype(np.int16).tobytes())
print(ep, 'music rms', round(float(np.sqrt(np.mean(out ** 2))), 4), 'peak', round(float(np.max(np.abs(full))), 3))

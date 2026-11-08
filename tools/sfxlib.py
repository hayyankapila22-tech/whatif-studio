import numpy as np, wave, subprocess, sys
SR = 44100
rng = np.random.default_rng(0)
T = 60.0; N = int(SR*T); mix = np.zeros((N, 2))
def init(total):
    global T, N, mix
    T = total; N = int(SR*T); mix = np.zeros((N, 2))


def add(sig, t0, gain=1.0, pan=0.0):
    global mix
    i = int(t0 * SR); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[:j - i] * gain
    mix[i:j, 0] += s * np.sqrt((1 - pan) / 2) * 1.41
    mix[i:j, 1] += s * np.sqrt((1 + pan) / 2) * 1.41
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, k):
    k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, 'same')

def whoosh(d=0.5):
    t = tt(d); s = rng.normal(0, 1, len(t)); out = np.zeros(len(t))
    ks = np.linspace(30, 4, len(t))
    for i in range(0, len(t), 512):
        seg = s[max(0, i - 64):i + 576]; f = lp(seg, ks[i]) - lp(seg, ks[i] * 5)
        out[i:i + 512] = f[min(64, i):min(64, i) + 512][:len(out[i:i + 512])]
    return out * np.sin(np.pi * t / d) ** 2 * 2.5
def pop(f=900):
    t = tt(0.09); fr = f * (1 + 0.8 * np.exp(-t * 60)); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 45)
def shatter(d=1.3):
    t = tt(d); s = rng.normal(0, 1, len(t)) * np.exp(-t * 4.5)
    tinks = sum(np.sin(2 * np.pi * rng.uniform(2500, 7000) * t) * np.exp(-np.maximum(0, t - x) * 22) * (t > x) for x in rng.uniform(0, .7, 18)) * 0.13
    boom = np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-t * 10)) / SR) * np.exp(-t * 5)
    return s * 0.3 + tinks + boom * 0.9
def riser(d):
    t = tt(d); return (np.sin(2 * np.pi * np.cumsum(180 + 1100 * (t / d) ** 2) / SR) * 0.5 + lp(rng.normal(0, 1, len(t)), 3) * 0.3) * (t / d) ** 2
def tick():
    t = tt(0.05); return rng.normal(0, 1, len(t)) * np.exp(-t * 140) * 0.8 + np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 90) * .5
def buzz(d=0.5, f=110):
    t = tt(d); return np.sign(np.sin(2 * np.pi * f * t)) * 0.35 * np.minimum(1, (d - t) * 20)
def beep(f=2000, d=0.12):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.minimum(1, (d - t) * 60) * 0.5
def dtmf(a, b, d=0.13):
    t = tt(d); return (np.sin(2 * np.pi * a * t) + np.sin(2 * np.pi * b * t)) * 0.3 * np.minimum(1, (d - t) * 60)
def glitch(d=0.8):
    t = tt(d); sq = np.sign(np.sin(2 * np.pi * 140 * t * (1 + 2 * (rng.random(len(t)) > .97))))
    gate = (np.floor(t * 30) % 3 != 0); return (sq * 0.3 + rng.normal(0, .35, len(t))) * gate
def powerdown(d=0.9):
    t = tt(d); f = 600 * np.exp(-t * 4) + 30; return np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - t / d) * 0.6 + rng.normal(0, .1, len(t)) * (1 - t / d)
def ding(f=1318):
    t = tt(0.9); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 5) * .5
def chalk(d):
    t = tt(d); s = rng.normal(0, 1, len(t)); s = s - lp(s, 6)
    g = (np.sin(2 * np.pi * 7 * t) > -0.2) * (0.6 + 0.4 * np.sin(2 * np.pi * 2.3 * t)); return s * g * 0.12
def rumble(d=1.2):
    t = tt(d); return lp(rng.normal(0, 1, len(t)), 60) * 3 * np.minimum(1, t * 4) * np.exp(-t * 1.5)


def chaching():
    t = tt(0.9); bell = sum(np.sin(2*np.pi*f*t)*np.exp(-t*a) for f,a in [(2093,5),(2637,6),(3136,7)]) * 0.25
    clink = rng.normal(0,1,len(t))*np.exp(-t*30)*0.3
    drawer = np.zeros(len(t)); k=int(0.05*SR); drawer[:k] = np.sin(2*np.pi*90*tt(0.05))*0.5
    return bell + clink + drawer
def bong(f=196):
    t = tt(1.6); return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*2.2)*0.6
def boom(d=1.6):
    t = tt(d); return np.sin(2*np.pi*np.cumsum(40+70*np.exp(-t*6))/SR)*np.exp(-t*2.5) + lp(rng.normal(0,1,len(t)),20)*np.exp(-t*4)*0.6
def finish(music_path, out_sfx, out_mix, music_gain=0.42):
    import subprocess, wave
    x = mix / max(1e-6, np.max(np.abs(mix))) * 0.92
    def save(name, y):
        y = np.clip(y, -1, 1)
        with wave.open(name, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y*32767).astype(np.int16).tobytes())
    save(out_sfx, x)
    raw = subprocess.run(['ffmpeg','-loglevel','error','-i',music_path,'-t',str(T),'-ac','2','-ar',str(SR),'-f','s16le','-'],capture_output=True).stdout
    mus = np.frombuffer(raw, np.int16).astype(float).reshape(-1,2)/32768
    mus = np.pad(mus, ((0, max(0, N-len(mus))), (0,0)))[:N]
    t = np.arange(N)/SR
    mus *= (np.clip(t/0.2,0,1)*np.clip((T-t)/1.5,0,1))[:,None]
    full = mus*music_gain + x*1.0
    peak = np.max(np.abs(full)); full = full/max(peak,1e-6)*0.95 if peak>0.95 else full
    save(out_mix, full)

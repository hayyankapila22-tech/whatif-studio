import json, re, os, sys, numpy as np, soundfile as sf
sys.path.insert(0, os.getcwd())
A = os.environ.get("HIW_ASSETS", "/home/claude/hiw_assets").rstrip("/") + "/"
from kokoro_onnx import Kokoro
from script import SENTENCES

VOICE = os.environ.get("HIW_VOICE", "af_heart")  # e.g. af_bella, or "af_heart+af_bella" (50/50 blend)
SPEED = float(os.environ.get("HIW_SPEED", "0.9"))
SR = 24000
# chatterbox (default, human-sounding Liam, owner pick 2026-11-19) | kokoro (old fallback)
_CBPY = os.environ.get("HIW_CB_PY", "/home/claude/cbx/bin/python")
ENGINE = os.environ.get("HIW_TTS", "chatterbox" if os.path.exists(_CBPY) else "kokoro")
if ENGINE == "kokoro":
    print("NOTE: using Kokoro (Chatterbox venv missing) - owner said Kokoro sounds too fake; log this in reports/issues.md")
k = Kokoro(A + "kokoro.onnx", A + "voices.bin")
if "+" in VOICE:
    _vs = VOICE.split("+")
    VOICE = sum(k.get_voice_style(v) for v in _vs) / len(_vs)


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def trim(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    return x[max(0, idx[0] - 240): idx[-1] + 480]


def voiced_mask(x, hop=240):
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x), hop)])
    m = e > max(0.012, e.max() * 0.06)
    # close tiny gaps (<60ms)
    out = m.copy()
    gap = 0
    for i in range(len(m)):
        if not m[i]:
            gap += 1
        else:
            if 0 < gap <= 6:
                out[i - gap:i] = True
            gap = 0
    return out, hop


CB = {}
if ENGINE == "chatterbox":
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs("cb_wav", exist_ok=True)
    items = []
    for i, s in enumerate(SENTENCES):
        say = re.sub(r"\s+", " ", s.get("say") or s["cap"].replace("*", "").replace("||", "")).strip()
        out = os.path.abspath(f"cb_wav/s{i:02d}.wav")
        CB[i] = out
        if not os.path.exists(out) or os.environ.get("HIW_CB_FORCE"):
            items.append(dict(text=say, out=out))
    if items:
        job = dict(ref=os.environ.get("HIW_CB_REF", os.path.join(here, "..", "..", "assets", "voices", "liam_ref.wav")),
                   exaggeration=float(os.environ.get("HIW_CB_EXAG", "0.7")), cfg=float(os.environ.get("HIW_CB_CFG", "0.4")),
                   items=items)
        json.dump(job, open("cb_jobs.json", "w"))
        py = _CBPY
        subprocess.run([py, os.path.join(here, "cb_gen.py"), "cb_jobs.json"], check=True, stderr=subprocess.DEVNULL)


def synth(i, say):
    if ENGINE == "chatterbox":
        x, sr = sf.read(CB[i], dtype="float32")
        if x.ndim > 1:
            x = x[:, 0]
        if sr != SR:
            import scipy.signal as ss
            x = ss.resample_poly(x, SR, sr).astype(np.float32)
        return x, SR
    return k.create(say, voice=VOICE, speed=SPEED, lang="en-us")


HEAD = float(os.environ.get("HIW_HEAD", "0.25"))
audio = [np.zeros(int(HEAD * SR), np.float32)]
t = HEAD
phrases = []
for si, s in enumerate(SENTENCES):
    say = s.get("say") or s["cap"].replace("*", "").replace("||", "")
    say = re.sub(r"\s+", " ", say).strip()
    x, sr = synth(si, say)
    assert sr == SR
    x = trim(x.astype(np.float32))
    # map words onto voiced time
    m, hop = voiced_mask(x)
    vt = np.cumsum(m) * hop / SR  # voiced seconds elapsed at each hop
    total_v = vt[-1]
    caps = [p.strip() for p in s["cap"].split("||")]
    words = []
    for pi, p in enumerate(caps):
        for w in p.split():
            kw = w.startswith("*") or w.endswith("*") or "*" in w
            clean = w.replace("*", "")
            wt = s.get("weights", {}).get(clean.strip(",.?"), syl(clean))
            words.append(dict(w=clean, kw=kw, wt=wt, phrase=pi))
    # multiword keyword like "*not exactly.*": mark words between asterisks
    raw = s["cap"].replace("||", " ").split()
    inside = False
    for i, w in enumerate(raw):
        st = w.startswith("*"); en = w.rstrip(".,?!").endswith("*")
        if st or inside:
            words[i]["kw"] = True
        if st and not en:
            inside = True
        if en:
            inside = False
    W = np.cumsum([0] + [w["wt"] for w in words]) / sum(w["wt"] for w in words)

    def v2t(frac):
        target = frac * total_v
        i = np.searchsorted(vt, target)
        return min(i, len(vt) - 1) * hop / SR

    for i, w in enumerate(words):
        w["t0"] = round(t + v2t(W[i]) - 0.03, 3)
        w["t1"] = round(t + v2t(W[i + 1]), 3)
        del w["wt"]
    for pi in range(len(caps)):
        ws = [w for w in words if w["phrase"] == pi]
        phrases.append(dict(words=ws, t0=ws[0]["t0"], t1=ws[-1]["t1"]))
    audio.append(x)
    t += len(x) / SR
    g = np.zeros(int(s["gap"] * SR), np.float32)
    audio.append(g)
    t += s["gap"]

audio.append(np.zeros(int(float(os.environ.get("HIW_TAIL", "1.0")) * SR), np.float32))
y = np.concatenate(audio)
sf.write("vo_raw.wav", y, SR)
json.dump(dict(duration=len(y) / SR, phrases=phrases), open("timings.json", "w"), indent=1)
print("duration", len(y) / SR, "phrases", len(phrases))
for p in phrases:
    print(f"{p['t0']:6.2f}-{p['t1']:6.2f}", " ".join(("*" if w["kw"] else "") + w["w"] for w in p["words"]))

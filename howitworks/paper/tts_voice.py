"""Generate one wav per line with Chatterbox (free, MIT). Usage (inside an episode folder):
    python3 ../../tts_voice.py            # reads lines.json -> vo_0.wav, vo_1.wav, ...
Voice 2 (bubbly presenter, owner's choice for paper videos) = voices/voice2_bubbly_presenter_ref.wav, exaggeration 0.8, cfg 0.35.
Reference clips are synthetic (Kokoro voices), never a real person's voice. Skips lines whose wav already exists."""
import json, os, sys, torch, torchaudio
HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'voice2': ('voice2_bubbly_presenter_ref.wav', 0.8, 0.35), 'voice1': ('voice1_british_storyteller_ref.wav', 0.55, 0.45)}
torch.set_num_threads(os.cpu_count() or 2)
from chatterbox.tts import ChatterboxTTS
cfg = json.load(open('lines.json')); ref, ex, cw = VOICES[cfg.get('voice', 'voice2')]
m = ChatterboxTTS.from_pretrained(device='cpu')
for i, line in enumerate(cfg['lines']):
    out = f'vo_{i}.wav'
    if os.path.exists(out): continue
    torch.manual_seed(cfg.get('seed', 7))
    w = m.generate(line, audio_prompt_path=os.path.join(HERE, 'voices', ref), exaggeration=ex, cfg_weight=cw)
    torchaudio.save(out, w, m.sr); print('line', i, round(w.shape[-1] / m.sr, 2), flush=True)

"""Chatterbox TTS worker (runs in the chatterbox venv). Usage: cb_gen.py jobs.json
jobs.json = {"ref": "...wav", "exaggeration": 0.7, "cfg": 0.4, "seed": 7, "items": [{"text": "...", "out": "...wav"}]}"""
import json, sys, torch, torchaudio as ta
from chatterbox.tts import ChatterboxTTS
J = json.load(open(sys.argv[1]))
m = ChatterboxTTS.from_pretrained(device="cpu")
for it in J["items"]:
    torch.manual_seed(J.get("seed", 7))
    wav = m.generate(it["text"], audio_prompt_path=J.get("ref"), exaggeration=J.get("exaggeration", 0.7),
                     cfg_weight=J.get("cfg", 0.4), temperature=J.get("temperature", 0.8))
    ta.save(it["out"], wav, m.sr)
    print("ok", it["out"], flush=True)

"""Write grain0-3.png film-grain tiles into the current directory."""
import numpy as np
from PIL import Image
for i in range(4):
    g = np.random.default_rng(100 + i).normal(0.5, 0.18, (960, 540))
    Image.fromarray((np.clip(g, 0, 1) * 255).astype(np.uint8)).resize((1080, 1920), Image.NEAREST).save(f"grain{i}.png")

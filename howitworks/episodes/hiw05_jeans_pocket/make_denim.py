"""Procedural denim (indigo twill) tile -> denim.png (seamless 1024 tile)."""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

N = 1024
rng = np.random.default_rng(3)
y, x = np.mgrid[0:N, 0:N].astype(np.float32)
# 3/1 twill: diagonal ribs
period = 8.0
rib = 0.5 + 0.5 * np.sin(2 * np.pi * (x + y) / period)
rib = rib ** 1.6
# warp slubs (vertical irregular thickness), seamless via wrap-around blur
slub = gaussian_filter(rng.normal(0, 1, (N, N)), (40, 1.5), mode="wrap")
slub = (slub - slub.min()) / (slub.max() - slub.min())
fine = gaussian_filter(rng.normal(0, 1, (N, N)), 0.8, mode="wrap")
fade = gaussian_filter(rng.normal(0, 1, (N, N)), 90, mode="wrap")
fade = (fade - fade.min()) / (fade.max() - fade.min())
indigo = np.array([0.15, 0.24, 0.42]); light = np.array([0.55, 0.64, 0.80]); dark = np.array([0.07, 0.11, 0.22])
w = np.clip(0.25 * rib + 0.25 * slub + 0.06 * fine + 0.18 * fade, 0, 1)
col = dark * (1 - w[..., None]) + indigo * w[..., None] * 1.25
col += (light - indigo) * (np.clip(rib * slub - 0.55, 0, 1) * 0.6)[..., None]   # white weft peeking through
col = np.clip(col, 0, 1)
Image.fromarray((col * 255).astype(np.uint8)).save("denim.png")
print("denim ok")

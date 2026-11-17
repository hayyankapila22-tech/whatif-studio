"""Procedural macro tongue surface (papillae bumps, lit) -> tongue.png 1400x2400."""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

Wt, Ht = 1400, 2400
rng = np.random.default_rng(11)
h = np.zeros((Ht, Wt), np.float32)
yy, xx = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
# filiform papillae: many small soft bumps
pts = rng.random((9000, 2)) * [Wt, Ht]
for x, y in pts:
    r = rng.uniform(5, 9)
    x0, x1 = int(max(0, x - 3 * r)), int(min(Wt, x + 3 * r)); y0, y1 = int(max(0, y - 3 * r)), int(min(Ht, y + 3 * r))
    d2 = (xx[y0:y1, x0:x1] - x) ** 2 + (yy[y0:y1, x0:x1] - y) ** 2
    h[y0:y1, x0:x1] += np.exp(-d2 / (2 * r * r))
h += 0.35 * gaussian_filter(rng.normal(0, 1, (Ht, Wt)), 30)
gy, gx = np.gradient(gaussian_filter(h, 1.0))
L = np.array([-0.45, -0.6, 0.66]); L /= np.linalg.norm(L)
n = np.stack([-gx * 2.2, -gy * 2.2, np.ones_like(h)], -1); n /= np.linalg.norm(n, axis=-1, keepdims=True)
lam = np.clip((n * L).sum(-1), 0, 1)
base = np.array([0.93, 0.52, 0.56])
tint = 1 + 0.06 * gaussian_filter(rng.normal(0, 1, (Ht, Wt)), 60)[..., None]
col = base[None, None, :] * tint * (0.62 + 0.45 * lam[..., None])
spec = (np.clip(lam, 0, 1) ** 24 * 0.35)[..., None]       # wet sheen
col = np.clip(col + spec, 0, 1)
Image.fromarray((col * 255).astype(np.uint8)).save("tongue.png")
print("tongue ok")

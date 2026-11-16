"""Macro skin surface texture (2.5D lit), pore positions, grain."""
import numpy as np, json, sys
from PIL import Image, ImageFilter

TONE = sys.argv[1] if len(sys.argv) > 1 else "#D7A47E"
Wt, Ht = 1400, 2400
rng = np.random.default_rng(5)


def noise(sig, seed):
    r = np.random.default_rng(seed).random((Ht, Wt)).astype(np.float32)
    a = np.asarray(Image.fromarray((r * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sig))).astype(np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)


h = np.zeros((Ht, Wt), np.float32)  # height field
yy, xx = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
# microrelief grooves (two directions, wavy)
for ang, per, amp in ((0.5, 52, 0.55), (-0.75, 64, 0.45), (1.6, 96, 0.3), (2.4, 40, 0.25)):
    u = xx * np.cos(ang) + yy * np.sin(ang) + 30 * noise(70, int(per)) + 8 * noise(15, int(per) + 1)
    h -= amp * ((np.cos(2 * np.pi * u / per) + 1) / 2) ** 6
h += 0.25 * noise(2, 1) + 0.6 * noise(8, 2)
# pores: jittered grid
pores = []
sp = 64
for gy in range(-1, Ht // sp + 2):
    for gx in range(-1, Wt // sp + 2):
        px = gx * sp + (gy % 2) * sp / 2 + rng.normal(0, 9)
        py = gy * sp + rng.normal(0, 9)
        pores.append((float(px), float(py)))
pmask = np.zeros((Ht, Wt), np.float32)
for px, py in pores:
    x0, x1 = int(max(0, px - 14)), int(min(Wt, px + 15))
    y0, y1 = int(max(0, py - 14)), int(min(Ht, py + 15))
    if x0 >= x1 or y0 >= y1:
        continue
    d = np.hypot(xx[y0:y1, x0:x1] - px, yy[y0:y1, x0:x1] - py)
    pmask[y0:y1, x0:x1] = np.maximum(pmask[y0:y1, x0:x1], np.exp(-(d / 6.0) ** 2))
h -= 3.0 * pmask
# shading from height field
from scipy.ndimage import gaussian_filter
gy_, gx_ = np.gradient(gaussian_filter(h, 1.2))
L = np.array([-0.5, -0.6, 0.62]); L /= np.linalg.norm(L)
n = np.stack([-gx_ * 1.4, -gy_ * 1.4, np.ones_like(h)], -1)
n /= np.linalg.norm(n, axis=-1, keepdims=True)
lam = np.clip((n * L).sum(-1), 0, 1)
tone = np.array([int(TONE[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
mott = 1 + 0.035 * noise(60, 9) + 0.02 * noise(16, 10)
redness = 0.03 * np.clip(noise(90, 11), 0, None)
base = tone[None, None, :] * mott[..., None]
base[..., 0] += redness; base[..., 2] -= redness * 0.5
shade = 0.72 + 0.42 * lam
col = base * shade[..., None]
# pore interiors slightly darker/warmer
col *= (1 - 0.22 * pmask)[..., None]
# subsurface warmth + spec sheen
spec = np.clip(lam, 0, 1) ** 18 * 0.10
col += spec[..., None]
col = np.clip(col, 0, 1)
Image.fromarray((col * 255).astype(np.uint8)).save(f"skin_{TONE[1:]}.png")
json.dump(pores, open("pores.json", "w"))

for i in range(4):
    g = np.random.default_rng(100 + i).normal(0.5, 0.18, (960, 540))
    Image.fromarray((np.clip(g, 0, 1) * 255).astype(np.uint8)).resize((1080, 1920), Image.NEAREST).save(f"grain{i}.png")
print("ok", len(pores))

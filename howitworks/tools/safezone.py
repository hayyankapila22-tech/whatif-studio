"""Overlay an approximate TikTok / Reels / Shorts UI on a 1080x1920 still to check nothing important is covered.
usage: python3 safezone.py still.png [out.png] [tiktok|reels|shorts]"""
import sys
from PIL import Image, ImageDraw, ImageFont
src = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else src.replace(".png", "_ui.png")
app = sys.argv[3] if len(sys.argv) > 3 else "tiktok"
im = Image.open(src).convert("RGBA").resize((1080, 1920))
ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
try:
    F = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 40)
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Regular.otf", 34)
except Exception:
    F = f = ImageFont.load_default()
W = (255, 255, 255, 235)
# danger zones (faint red)
for box in ((0, 0, 1080, 300), (920, 700, 1080, 1700), (0, 1440, 1080, 1920)):
    d.rectangle(box, fill=(255, 40, 40, 38))
d.rectangle((0, 1440, 1080, 1920), fill=(0, 0, 0, 70))
if app == "tiktok":
    d.text((330, 140), "Following", font=F, fill=(255, 255, 255, 170)); d.text((560, 140), "For You", font=F, fill=W)
    d.rectangle((600, 196, 680, 202), fill=W)
elif app == "reels":
    d.text((60, 140), "Reels", font=F, fill=W)
else:
    d.text((60, 140), "Shorts", font=F, fill=W)
# right action column
ys = (880, 1060, 1210, 1350, 1490, 1630)
d.ellipse((960, ys[0] - 50, 1060, ys[0] + 50), outline=W, width=5)
d.ellipse((994, ys[0] + 36, 1026, ys[0] + 68), fill=(255, 60, 90, 255))
for y in ys[1:5]:
    d.ellipse((975, y - 38, 1045, y + 32), fill=(255, 255, 255, 200))
    d.text((985, y + 40), "1.2K", font=ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Regular.otf", 24) if f != ImageFont.load_default() else f, fill=W)
# bottom: username, description, sound
d.text((40, 1560), "@whatif_ig  · Follow", font=F, fill=W)
d.text((40, 1625), "What is this? 👀 It's dandruff, up close…", font=f, fill=W)
d.text((40, 1680), "#howitworks #science #didyouknow", font=f, fill=(255, 255, 255, 200))
d.text((40, 1760), "♪ original sound", font=f, fill=(255, 255, 255, 200))
d.rectangle((0, 1830, 1080, 1920), fill=(0, 0, 0, 200))
Image.alpha_composite(im, ov).convert("RGB").save(out)
print(out)

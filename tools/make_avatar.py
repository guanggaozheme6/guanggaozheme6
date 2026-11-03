"""Build the round avatar (assets/avatar.png) from assets/character.jpg.

Centre-crops the source to a square, masks it to a circle and wraps it in a
pink ring. Background is transparent so the PNG sits on any GitHub theme.
"""
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "character.jpg")
DST = os.path.join(ROOT, "assets", "avatar.png")

D = 480          # photo diameter
RING = 7         # ring thickness
PAD = 10         # transparent margin (room for the ring)
SS = 4           # supersample factor

PINK = (255, 111, 165, 255)
CYAN = (111, 227, 255, 120)

img = Image.open(SRC).convert("RGB")
w, h = img.size
s = min(w, h)
box = ((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)
big = img.crop(box).resize((D * SS, D * SS), Image.LANCZOS).convert("RGBA")

# circular alpha on the photo (drawn supersampled, then scaled down for clean edges)
mask = Image.new("L", (D * SS, D * SS), 0)
ImageDraw.Draw(mask).ellipse((0, 0, D * SS - 1, D * SS - 1), fill=255)
big.putalpha(mask)
photo = big.resize((D, D), Image.LANCZOS)

canvas = D + PAD * 2
# ring: white disc minus a smaller disc -> outline only
ring_mask = Image.new("L", (canvas * SS, canvas * SS), 0)
d = ImageDraw.Draw(ring_mask)
c = canvas * SS / 2
r_out = (D + RING * 2) * SS / 2
r_in = D * SS / 2
d.ellipse((c - r_out, c - r_out, c + r_out, c + r_out), fill=255)
d.ellipse((c - r_in, c - r_in, c + r_in, c + r_in), fill=0)
ring_mask = ring_mask.resize((canvas, canvas), Image.LANCZOS)

ring = Image.new("RGBA", (canvas, canvas), PINK)
ring.putalpha(ring_mask)

# thin cyan hairline just inside the ring
hair_mask = Image.new("L", (canvas * SS, canvas * SS), 0)
d2 = ImageDraw.Draw(hair_mask)
r_h = r_in - 3
d2.ellipse((c - r_h, c - r_h, c + r_h, c + r_h), outline=255, width=2 * SS)
hair_mask = hair_mask.resize((canvas, canvas), Image.LANCZOS)
hair = Image.new("RGBA", (canvas, canvas), CYAN)
hair.putalpha(hair_mask)

out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
out.paste(photo, (PAD, PAD), photo)
out = Image.alpha_composite(out, hair)
out = Image.alpha_composite(out, ring)
out = out.quantize(colors=256, method=Image.FASTOCTREE)  # 250KB -> ~50KB, visually identical
out.save(DST, optimize=True)
print("wrote %s  %sx%s  %s bytes  (crop %s of %s)" % (DST, canvas, canvas, os.path.getsize(DST), box, (w, h)))

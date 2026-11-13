"""Build the profile-card image (assets/character.png) from assets/character.jpg.

Rounded-rect crop of the source photo, thin pink hairline border, transparent
corners so the PNG sits on both GitHub light and dark themes.
"""
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "character.jpg")
DST = os.path.join(ROOT, "assets", "character.png")

W = 760          # exported width
RADIUS = 26      # corner radius (at export scale)
BORDER = 3       # pink hairline thickness
SS = 4           # supersample factor

PINK = (255, 111, 165, 255)
CYAN = (111, 227, 255, 140)

src = Image.open(SRC).convert("RGB")
w, h = src.size
out_w, out_h = W, round(W * h / w)
big = src.resize((out_w * SS, out_h * SS), Image.LANCZOS).convert("RGBA")

# rounded-rect alpha mask, drawn supersampled for clean edges
mask = Image.new("L", (out_w * SS, out_h * SS), 0)
ImageDraw.Draw(mask).rounded_rectangle(
    (0, 0, out_w * SS - 1, out_h * SS - 1), radius=RADIUS * SS, fill=255
)
big.putalpha(mask)
photo = big.resize((out_w, out_h), Image.LANCZOS)

# pink hairline just inside the edge
edge_mask = Image.new("L", (out_w * SS, out_h * SS), 0)
ImageDraw.Draw(edge_mask).rounded_rectangle(
    (BORDER * SS // 2, BORDER * SS // 2,
     out_w * SS - 1 - BORDER * SS // 2, out_h * SS - 1 - BORDER * SS // 2),
    radius=max(1, (RADIUS - BORDER) * SS), outline=255, width=BORDER * SS
)
edge_mask = edge_mask.resize((out_w, out_h), Image.LANCZOS)
edge = Image.new("RGBA", (out_w, out_h), PINK)
edge.putalpha(edge_mask)

out = Image.alpha_composite(photo, edge)
out = out.quantize(colors=256, method=Image.FASTOCTREE)
out.save(DST, optimize=True)
print("wrote %s  %sx%s  %s bytes (from %s)" % (DST, out_w, out_h, os.path.getsize(DST), (w, h)))

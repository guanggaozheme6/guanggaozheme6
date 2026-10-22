"""Animated ASCII art: static base layer + a scattered animated overlay.

Only a small, evenly spread fraction of glyphs animate, so the page stays
smooth while still looking alive.
"""
import os
import html

try:
    from PIL import Image
except ImportError:
    raise SystemExit("PIL missing: pip install pillow")

SRC = "assets/character.jpg"
OUT = "assets/art.svg"

COLS = 90
FONT = 9.0
LH = 9.4
PAD_X = 26
PAD_Y = 30
DENSITY = 0.12          # fraction of glyphs that animate

img = Image.open(SRC).convert("L")
w, h = img.size
rows = max(1, int(COLS * h / w * 0.48))
img = img.resize((COLS, rows), Image.LANCZOS)
px = img.load()

ramp = " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
top = len(ramp) - 1

CW = FONT * 0.6
W = int(PAD_X * 2 + COLS * CW)
H = int(PAD_Y * 2 + rows * LH)

grid = []
for i in range(rows):
    row = []
    for j in range(COLS):
        v = 1.0 - (px[j, i] / 255.0)
        v = v ** 0.85
        row.append(ramp[min(top, int(v * top))])
    grid.append(row)

css = """
.in{animation:fade .8s ease-out both}
.s{animation:scan 6s linear infinite}
.b{font-family:Consolas,'Courier New',monospace;font-size:9px;fill:#ff6fa5;
   animation-name:blink;animation-iteration-count:infinite}
.j{font-family:Consolas,'Courier New',monospace;font-size:9px;fill:#ff6fa5;
   animation-name:jit;animation-iteration-count:infinite}
.k{font-family:Consolas,'Courier New',monospace;font-size:9px;fill:#7de6ff;
   animation-name:blink;animation-iteration-count:infinite}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes blink{
  0%,68%,100%{opacity:1}
  72%{opacity:.10}
  76%{opacity:1}
}
@keyframes jit{
  0%,76%,100%{transform:translate(0,0)}
  79%{transform:translate(2px,-1.5px)}
  85%{transform:translate(-1.5px,1.5px)}
  91%{transform:translate(0.8px,0.6px)}
}
@keyframes scan{
  0%{transform:translateY(-80px);opacity:0}
  6%{opacity:1}94%{opacity:1}
  100%{transform:translateY(__H__px);opacity:0}
}
""".replace("__H__", str(H))

parts = []
parts.append(
    '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
    'viewBox="0 0 %d %d" xml:space="preserve" role="img" aria-label="ascii art">'
    % (W, H, W, H)
)
parts.append(
    '<defs>'
    '<linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#6fe3ff" stop-opacity="0"/>'
    '<stop offset="0.5" stop-color="#6fe3ff" stop-opacity="0.34"/>'
    '<stop offset="1" stop-color="#6fe3ff" stop-opacity="0"/>'
    '</linearGradient>'
    '<style>%s</style></defs>' % css
)
parts.append('<rect width="%d" height="%d" fill="#07080c"/>' % (W, H))
parts.append('<g class="in">')

# static base: one text element per line
for i in range(rows):
    line = "".join(grid[i]).rstrip()
    if not line:
        continue
    y = PAD_Y + i * LH + FONT * 0.82
    parts.append(
        '<text x="%d" y="%.1f" font-family="Consolas,\'Courier New\',monospace" '
        'font-size="%.1f" fill="#ff6fa5">%s</text>'
        % (PAD_X, y, FONT, html.escape(line))
    )

# scattered animated overlay
moved = 0
for i in range(rows):
    y = PAD_Y + i * LH + FONT * 0.82
    for j in range(COLS):
        ch = grid[i][j]
        if ch == " ":
            continue
        seed = (i * 7919 + j * 104729) % 1000
        if seed >= int(DENSITY * 1000):
            continue
        x = PAD_X + j * CW
        delay = (seed * 4) / 1000.0 * 3.4
        dur = 2.6 + (seed % 9) * 0.28
        if seed % 7 == 0:
            cls = "k"
        elif seed % 5 < 3:
            cls = "j"
        else:
            cls = "b"
        parts.append(
            '<text class="%s" x="%.1f" y="%.1f" style="animation-delay:%.2fs;animation-duration:%.2fs">%s</text>'
            % (cls, x, y, delay, dur, html.escape(ch))
        )
        moved += 1

parts.append("</g>")
parts.append('<rect class="s" x="0" y="0" width="%d" height="80" fill="url(#g)"/>' % W)
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(parts))

print(
    "wrote %s: %sx%s grid, %s glyphs total, %s animated, %s bytes"
    % (OUT, COLS, rows, sum(1 for r in grid for c in r if c != " "), moved, os.path.getsize(OUT))
)

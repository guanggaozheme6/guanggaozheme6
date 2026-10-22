"""Generate an animated ASCII-art SVG from a source image."""
import os
import html

try:
    from PIL import Image
except ImportError:
    raise SystemExit("PIL missing: pip install pillow")

SRC = "assets/character.jpg"
OUT = "assets/ascii.svg"

COLS = 110
FONT = 9.0
LH = 9.4
PAD_X = 26
PAD_Y = 30

img = Image.open(SRC).convert("L")
w, h = img.size
rows = max(1, int(COLS * h / w * 0.48))
img = img.resize((COLS, rows), Image.LANCZOS)
px = img.load()

ramp = " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
top = len(ramp) - 1

lines = []
for y in range(rows):
    buf = []
    for x in range(COLS):
        v = 1.0 - (px[x, y] / 255.0)
        v = v ** 0.85
        buf.append(ramp[min(top, int(v * top))])
    lines.append("".join(buf).rstrip())

CW = FONT * 0.6
W = int(PAD_X * 2 + COLS * CW)
H = int(PAD_Y * 2 + rows * LH)

css = """
.l{opacity:0;animation:app .45s ease-out forwards}
.s{animation:scan 6s linear infinite}
.c{animation:blink 1.1s steps(1) infinite}
@keyframes app{to{opacity:1}}
@keyframes scan{0%{transform:translateY(-60px);opacity:0}
10%{opacity:1}90%{opacity:1}100%{transform:translateY(__H__px);opacity:0}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
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
    '<stop offset="0.5" stop-color="#6fe3ff" stop-opacity="0.30"/>'
    '<stop offset="1" stop-color="#6fe3ff" stop-opacity="0"/>'
    '</linearGradient>'
    '<style>%s</style></defs>' % css
)
parts.append('<rect width="%d" height="%d" fill="#07080c"/>' % (W, H))

for i, line in enumerate(lines):
    if not line:
        continue
    y = PAD_Y + i * LH + FONT * 0.82
    delay = min(2.6, i * 0.035)
    parts.append(
        '<text class="l" x="%d" y="%.2f" font-family="Consolas,\'Courier New\',monospace" '
        'font-size="%.1f" fill="#ff6fa5" style="animation-delay:%.2fs">%s</text>'
        % (PAD_X, y, FONT, delay, html.escape(line))
    )

parts.append('<rect class="s" x="0" y="0" width="%d" height="70" fill="url(#g)"/>' % W)
parts.append(
    '<rect class="c" x="%d" y="%d" width="8" height="12" fill="#6fe3ff"/>'
    % (PAD_X, int(H - PAD_Y + 2))
)
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(parts))

print("wrote %s: %sx%s chars, %sx%s px, %s bytes" % (OUT, COLS, rows, W, H, os.path.getsize(OUT)))

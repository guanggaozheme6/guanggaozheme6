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

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" xml:space="preserve" role="img" aria-label="ascii art">'
)
parts.append(
    "<defs>"
    '<linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#6fe3ff" stop-opacity="0"/>'
    '<stop offset="0.5" stop-color="#6fe3ff" stop-opacity="0.30"/>'
    '<stop offset="1" stop-color="#6fe3ff" stop-opacity="0"/>'
    "</linearGradient>"
    "<style>"
    ".l{opacity:0;animation:app .45s ease-out forwards}"
    ".s{animation:scan 6s linear infinite}"
    ".c{animation:blink 1.1s steps(1) infinite}"
    "@keyframes app{to{opacity:1}}"
    "@keyframes scan{0%{transform:translateY(-60px);opacity:0}"
    "10%{opacity:1}90%{opacity:1}100%{transform:translateY(%dpx);opacity:0}}"
    "@keyframes blink{0%%,49%%{opacity:1}50%%,100%%{opacity:0}}"
    "</style>"
    "</defs>" % H
)
parts.append(f'<rect width="{W}" height="{H}" fill="#07080c"/>')

for i, line in enumerate(lines):
    if not line:
        continue
    y = PAD_Y + i * LH + FONT * 0.82
    delay = min(2.6, i * 0.035)
    parts.append(
        f'<text class="l" x="{PAD_X}" y="{y:.2f}" font-family="Consolas,\'Courier New\',monospace" '
        f'font-size="{FONT}" fill="#ff6fa5" style="animation-delay:{delay:.2f}s">{html.escape(line)}</text>'
    )

parts.append(f'<rect class="s" x="0" y="0" width="{W}" height="70" fill="url(#g)"/>')
parts.append(
    f'<rect class="c" x="{PAD_X}" y="{int(H - PAD_Y + 2)}" width="8" height="12" fill="#6fe3ff"/>'
)
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(parts))

print(f"wrote {OUT}: {COLS}x{rows} chars, {W}x{H} px, {os.path.getsize(OUT)} bytes")

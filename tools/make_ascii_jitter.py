"""Per-character animated ASCII art: every glyph gets its own jitter."""
import os
import html

try:
    from PIL import Image
except ImportError:
    raise SystemExit("PIL missing: pip install pillow")

SRC = "assets/character.jpg"
OUT = "assets/ascii.svg"

COLS = 90
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

CW = FONT * 0.6
W = int(PAD_X * 2 + COLS * CW)
H = int(PAD_Y * 2 + rows * LH)

css = """
.in{animation:fade .9s ease-out both}
.j{font-family:Consolas,'Courier New',monospace;font-size:9px;fill:#ff6fa5;
   animation-name:jit;animation-iteration-count:infinite}
.k{font-family:Consolas,'Courier New',monospace;font-size:9px;fill:#ff8fb8;
   animation-name:jit;animation-iteration-count:infinite}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes jit{
  0%,88%,100%{transform:translate(0,0);opacity:1}
  90%{transform:translate(1.2px,-0.8px);opacity:.72}
  93%{transform:translate(-1.0px,1.0px);opacity:1}
  96%{transform:translate(0.6px,0.5px);opacity:.85}
}
.s{animation:scan 7s linear infinite}
@keyframes scan{
  0%{transform:translateY(-70px);opacity:0}
  8%{opacity:1}92%{opacity:1}
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
    '<stop offset="0.5" stop-color="#6fe3ff" stop-opacity="0.26"/>'
    '<stop offset="1" stop-color="#6fe3ff" stop-opacity="0"/>'
    '</linearGradient>'
    '<style>%s</style></defs>' % css
)
parts.append('<rect width="%d" height="%d" fill="#07080c"/>' % (W, H))
parts.append('<g class="in">')

count = 0
for i in range(rows):
    base = PAD_Y + i * LH + FONT * 0.82
    for j in range(COLS):
        v = 1.0 - (px[j, i] / 255.0)
        v = v ** 0.85
        ch = ramp[min(top, int(v * top))]
        if ch == " ":
            continue
        x = PAD_X + j * CW
        seed = (i * 7919 + j * 104729) % 1000
        delay = seed / 250.0
        dur = 3.2 + (seed % 7) * 0.35
        cls = "j" if (seed % 3) else "k"
        parts.append(
            '<text class="%s" x="%.1f" y="%.1f" style="animation-delay:%.2fs;animation-duration:%.2fs">%s</text>'
            % (cls, x, base, delay, dur, html.escape(ch))
        )
        count += 1

parts.append("</g>")
parts.append('<rect class="s" x="0" y="0" width="%d" height="70" fill="url(#g)"/>' % W)
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(parts))

print("wrote %s: %sx%s grid, %s glyphs, %s bytes" % (OUT, COLS, rows, count, os.path.getsize(OUT)))

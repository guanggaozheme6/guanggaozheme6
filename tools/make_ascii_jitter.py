"""Per-character animated ASCII art with a visible glitch wave."""
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
.k{font-family:Consolas,'Courier New',monospace;font-size:9px;fill:#7de6ff;
   animation-name:jit;animation-iteration-count:infinite}
.r{animation:rg 5.5s linear infinite}
.s{animation:scan 5s linear infinite}
.f{animation:flash 5.5s linear infinite}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes jit{
  0%,84%,100%{transform:translate(0,0);opacity:1}
  86%{transform:translate(2.0px,-1.4px);opacity:.55}
  90%{transform:translate(-1.8px,1.6px);opacity:1}
  94%{transform:translate(1.0px,0.8px);opacity:.75}
}
@keyframes rg{
  0%,93%,100%{transform:translateX(0)}
  94%{transform:translateX(-8px)}
  96%{transform:translateX(7px)}
  98%{transform:translateX(-2px)}
}
@keyframes scan{
  0%{transform:translateY(-80px);opacity:0}
  6%{opacity:1}94%{opacity:1}
  100%{transform:translateY(__H__px);opacity:0}
}
@keyframes flash{
  0%,93%,100%{opacity:0}
  94%{opacity:.10}
  96%{opacity:0}
  97%{opacity:.07}
  98%{opacity:0}
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
    '<stop offset="0.5" stop-color="#6fe3ff" stop-opacity="0.38"/>'
    '<stop offset="1" stop-color="#6fe3ff" stop-opacity="0"/>'
    '</linearGradient>'
    '<style>%s</style></defs>' % css
)
parts.append('<rect width="%d" height="%d" fill="#07080c"/>' % (W, H))
parts.append('<g class="in">')

count = 0
for i in range(rows):
    base = PAD_Y + i * LH + FONT * 0.82
    parts.append('<g class="r" style="animation-delay:%.2fs">' % (i * 0.045))
    for j in range(COLS):
        v = 1.0 - (px[j, i] / 255.0)
        v = v ** 0.85
        ch = ramp[min(top, int(v * top))]
        if ch == " ":
            continue
        x = PAD_X + j * CW
        seed = (i * 7919 + j * 104729) % 1000
        delay = seed / 220.0
        dur = 2.6 + (seed % 7) * 0.30
        cls = "j" if (seed % 4) else "k"
        parts.append(
            '<text class="%s" x="%.1f" y="%.1f" style="animation-delay:%.2fs;animation-duration:%.2fs">%s</text>'
            % (cls, x, base, delay, dur, html.escape(ch))
        )
        count += 1
    parts.append("</g>")

parts.append("</g>")
parts.append('<rect class="s" x="0" y="0" width="%d" height="80" fill="url(#g)"/>' % W)
parts.append('<rect class="f" x="0" y="0" width="%d" height="%d" fill="#7de6ff"/>' % (W, H))
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(parts))

print("wrote %s: %sx%s grid, %s glyphs, %s bytes" % (OUT, COLS, rows, count, os.path.getsize(OUT)))

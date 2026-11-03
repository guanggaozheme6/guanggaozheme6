"""Generate the slim animated wave strip used under the typing line.

Transparent background so it reads on both GitHub light and dark themes.
Period == PERIOD, so a translateX of exactly -PERIOD loops seamlessly.
"""
import math
import os

W, H = 1200, 130
PERIOD = 600
STEP = 5
SPAN = W + PERIOD          # draw two periods, shift by one

PINK = "#ff6fa5"
CYAN = "#6fe3ff"


def wave(amp, phase, baseline):
    pts = []
    x = 0
    while x <= SPAN:
        y = baseline + amp * math.sin(2 * math.pi * x / PERIOD + phase)
        pts.append((x, y))
        x += STEP
    return pts


def polyline(pts):
    return "M " + " L ".join("%.1f %.2f" % p for p in pts)


def closed(pts):
    return polyline(pts) + " L %.1f %d L 0 %d Z" % (pts[-1][0], H, H)


back = closed(wave(30, 0.0, 70))
mid = closed(wave(20, math.pi, 78))
line = polyline(wave(24, 0.0, 66))
line2 = polyline(wave(13, math.pi * 0.9, 86))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="wave">
  <defs>
    <linearGradient id="f1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{PINK}" stop-opacity="0.20"/>
      <stop offset="0.65" stop-color="{PINK}" stop-opacity="0.04"/>
      <stop offset="1" stop-color="{PINK}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="f2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0.13"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="stroke" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0.15"/>
      <stop offset="0.22" stop-color="{CYAN}" stop-opacity="0.95"/>
      <stop offset="0.5" stop-color="{PINK}"/>
      <stop offset="0.78" stop-color="{CYAN}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0.15"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-120%" width="140%" height="340%">
      <feGaussianBlur stdDeviation="3.5"/>
    </filter>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.10" stop-color="#fff" stop-opacity="1"/>
      <stop offset="0.90" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="fade"><rect x="0" y="0" width="{W}" height="{H}" fill="url(#edge)"/></mask>
    <style>
      .roll {{ animation: roll 11s linear infinite; }}
      .roll2 {{ animation: roll 17s linear infinite reverse; }}
      .roll3 {{ animation: roll 23s linear infinite; }}
      .dot {{ animation: bob 4.5s ease-in-out infinite; }}
      @keyframes roll  {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{PERIOD}px); }} }}
      @keyframes bob   {{ 0%,100% {{ opacity: .25; }} 50% {{ opacity: .95; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .roll, .roll2, .roll3, .dot {{ animation: none; }}
      }}
    </style>
  </defs>

  <g mask="url(#fade)">
  <g class="roll2" opacity="0.9"><path d="{back}" fill="url(#f1)"/></g>
  <g class="roll3"><path d="{mid}" fill="url(#f2)"/></g>

  <g class="roll">
    <path d="{line}" fill="none" stroke="url(#stroke)" stroke-width="7" stroke-linejoin="round" opacity="0.55" filter="url(#glow)"/>
    <path d="{line}" fill="none" stroke="url(#stroke)" stroke-width="2.4" stroke-linejoin="round"/>
    <path d="{line2}" fill="none" stroke="{CYAN}" stroke-opacity="0.28" stroke-width="1.1" stroke-dasharray="3 9" stroke-linejoin="round"/>
  </g>

  <g fill="{PINK}">
    <circle class="dot" cx="180" cy="34" r="2.2" style="animation-delay:0s"/>
    <circle class="dot" cx="520" cy="96" r="1.7" style="animation-delay:1.1s"/>
    <circle class="dot" cx="860" cy="26" r="2" style="animation-delay:2.2s"/>
    <circle class="dot" cx="1060" cy="104" r="1.5" style="animation-delay:3.1s"/>
  </g>
  </g>
</svg>
'''

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "wave.svg")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print("wrote", out, os.path.getsize(out), "bytes")

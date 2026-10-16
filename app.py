import math as m
import random as r
from flask import Flask, render_template_string

app = Flask(__name__)

# --- Your original math and variables ---
SC = 21
OY = 20
GAP = 7
SIZES = (9, 10, 11, 12)
BG = "#060208"

rng = r.Random(11)

PHRASES = [
    "I love you", "Seni seviyorum", "Te amo", "Je t'aime",
    "Ich liebe dich", "Ti amo", "Eu te amo", "Я тебя люблю",
    "사랑해", "愛してる", "我爱你", "मैं तुमसे प्यार करता हूँ",
    "Σ' αγαπώ", "Ik hou van jou", "Jag älskar dig", "Kocham cię",
    "ฉันรักเธอ", "Anh yêu em", "Aku cinta kamu", "Я тебе кохаю",
]

def heart(a):
    x = 16 * (m.sin(a) ** 3)
    y = 13 * m.cos(a) - 5 * m.cos(2 * a) - 2 * m.cos(3 * a) - m.cos(4 * a)
    return x * SC, y * SC + OY

POLY = [heart(2 * m.pi * i / 720) for i in range(720)]
EDGES = list(zip(POLY, POLY[1:] + POLY[:1]))
YMAX = max(p[1] for p in POLY)
YMIN = min(p[1] for p in POLY)
CY = (YMAX + YMIN) / 2

def spans(y):
    xs = []
    for (x1, y1), (x2, y2) in EDGES:
        if (y1 <= y < y2) or (y2 <= y < y1):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    return list(zip(xs[0::2], xs[1::2]))

def intersect(A, B):
    out = []
    for a in A:
        for b in B:
            lo, hi = max(a[0], b[0]), min(a[1], b[1])
            if hi - lo > 14:
                out.append((lo, hi))
    return out

def phrase_cycle():
    while True:
        order = PHRASES[:]
        rng.shuffle(order)
        for p in order:
            yield p

def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))

def math_dist(x, y):
    return m.hypot(x / (16 * SC), (y - CY) / (14.5 * SC))

# --- Modified build function ---
def build():
    cycle = phrase_cycle()
    row_h = 18  # Replaces tkinter line space metric
    half = row_h / 2
    placed = []

    y = YMAX - half
    while y > YMIN + half:
        row = intersect(spans(y + half), spans(y - half))

        for lo, hi in row:
            lo += 4
            hi -= 4
            cur = lo + rng.uniform(0, 8)
            line = []

            while True:
                fit = None
                for _ in range(10):
                    text = next(cycle)
                    size = rng.choice(SIZES)
                    # We estimate text width here to avoid tkinter module
                    w = len(text) * size * 0.65 
                    if cur + w <= hi:
                        fit = (text, size, w)
                        break
                if not fit:
                    break
                text, size, w = fit
                line.append([cur + w / 2, text, size, w])
                cur += w + GAP

            if not line:
                continue

            if len(line) > 1:
                left = hi - (line[-1][0] + line[-1][3] / 2)
                for i, it in enumerate(line):
                    it[0] += left * i / (len(line) - 1)
            else:
                line[0][0] = (lo + hi) / 2

            for i, (x, text, size, w) in enumerate(line):
                edge = i == 0 or i == len(line) - 1
                placed.append(dict(x=x, y=y, text=text, size=size, edge=edge))

        y -= row_h

    wine = (0.58, 0.0, 0.09)
    crimson = (0.90, 0.05, 0.14)
    blood = (0.98, 0.10, 0.16)
    
    for p in placed:
        rad = min(1.0, math_dist(p["x"], p["y"]))
        base = mix(wine, crimson, 0.25 + 0.75 * rad)
        base = mix(base, blood, rng.uniform(0, 0.35) + (0.3 if p["edge"] else 0))
        # Convert RGB floats to HTML Hex colors
        p["color"] = "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in base)
        p["rad"] = rad

    edges = [p for p in placed if p["edge"]]
    inner = [p for p in placed if not p["edge"]]
    edges.sort(key=lambda p: m.atan2(p["x"], p["y"] - CY) % (2 * m.pi))
    inner.sort(key=lambda p: -p["rad"] + rng.uniform(0, 0.08))
    return edges + inner

# --- Web Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<!-- Privacy-friendly analytics by Plausible -->
<script async src="https://plausible.io/js/pa-CbY9wfRmzgUqUEQ3iH5bZ.js"></script>
<script>
  window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
  plausible.init()
</script>
    <title>This is Stupid af</title>
    <style>
        body { 
            background-color: {{ bg }}; 
            margin: 0; 
            font-family: Arial, sans-serif;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        #container {
            position: relative;
            width: 800px;
            height: 800px;
        }
        .phrase {
            position: absolute;
            transform: translate(-50%, -50%);
            white-space: nowrap;
            font-weight: bold;
            opacity: 0;
            animation: fadeIn 0.4s forwards;
        }
        @keyframes fadeIn {
            to { opacity: 1; }
        }
    </style>
</head>
<body>
    <div id="container">
        <!-- Render loops through our Python positions -->
        {% for item in items %}
        <span class="phrase" 
              style="left: calc(50% + {{ item.x }}px); 
                     top: calc(50% - {{ item.y }}px); 
                     font-size: {{ item.size }}px; 
                     color: {{ item.color }}; 
                     animation-delay: {{ loop.index0 * 0.015 }}s;">
            {{ item.text }}
        </span>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Run the heart calculation when someone visits the page
    items = build()
    return render_template_string(HTML_TEMPLATE, items=items, bg=BG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

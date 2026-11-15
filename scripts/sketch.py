"""
sketch.py — hand-drawn drawing primitives (wobbly lines, rounded boxes, circles,
crossed image boxes and simple icons) rendered with 3x supersampling via Pillow.
Coordinates are in output pixels; the canvas is downscaled with LANCZOS on save().
"""
import math, random
from PIL import Image, ImageDraw

S = 3                      # supersampling
W, H = 375, 812
INK = (38, 38, 38)
GRAY = (150, 150, 150)
LIGHT = (205, 205, 205)
FILL = (222, 222, 222)
DARK = (55, 55, 55)

class Sketch:
    def __init__(self, seed=1, w=W, h=H):
        self.rnd = random.Random(seed)
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w * S, h * S), "white")
        self.d = ImageDraw.Draw(self.img)

    # ---------- geometry helpers ----------
    def _wobble(self, pts, amp=0.9):
        """apply smooth perpendicular noise to a polyline (375-space)"""
        out = []
        ph1, ph2 = self.rnd.uniform(0, 6.28), self.rnd.uniform(0, 6.28)
        f1, f2 = self.rnd.uniform(0.02, 0.05), self.rnd.uniform(0.08, 0.14)
        acc = 0
        for i, (x, y) in enumerate(pts):
            if i:
                acc += math.hypot(x - pts[i-1][0], y - pts[i-1][1])
            j = i + 1 if i + 1 < len(pts) else i
            k = i - 1 if i > 0 else i
            dx, dy = pts[j][0] - pts[k][0], pts[j][1] - pts[k][1]
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L, dx / L
            o = amp * (0.65 * math.sin(acc * f1 + ph1) + 0.35 * math.sin(acc * f2 + ph2))
            out.append((x + nx * o, y + ny * o))
        return out

    def _densify(self, pts, step=5):
        out = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            for i in range(1, n + 1):
                out.append((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n))
        return out

    def _poly(self, pts, width=2, color=INK, dashed=False):
        P = [(x * S, y * S) for x, y in pts]
        if not dashed:
            self.d.line(P, fill=color, width=int(width * S), joint="curve")
            for x, y in (P[0], P[-1]):
                r = width * S / 2
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)
            return
        # dashed: walk along
        seg, on, run = [], True, 0
        dash, gap = 7, 5
        for a, b in zip(P, P[1:]):
            l = math.hypot(b[0] - a[0], b[1] - a[1]) / S
            run += l
            if on:
                seg.append(a)
            if run >= (dash if on else gap):
                if on:
                    seg.append(b)
                    self.d.line(seg, fill=color, width=int(width * S), joint="curve")
                seg, on, run = [], not on, 0
        if on and seg:
            seg.append(P[-1])
            self.d.line(seg, fill=color, width=int(width * S), joint="curve")

    # ---------- primitives ----------
    def line(self, x0, y0, x1, y1, width=2, color=INK, dashed=False, overshoot=True):
        if overshoot:
            L = math.hypot(x1 - x0, y1 - y0) or 1
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            e0, e1 = self.rnd.uniform(-1, 2.5), self.rnd.uniform(-1, 2.5)
            x0, y0, x1, y1 = x0 - ux * e0, y0 - uy * e0, x1 + ux * e1, y1 + uy * e1
        pts = self._densify([(x0, y0), (x1, y1)])
        self._poly(self._wobble(pts, 0.8), width, color, dashed)

    def _rr_path(self, x, y, w, h, r):
        r = min(r, w / 2, h / 2)
        pts = []
        def arc(cx, cy, a0, a1):
            n = max(3, int(r / 2))
            for i in range(n + 1):
                a = math.radians(a0 + (a1 - a0) * i / n)
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        if r <= 0.5:
            return [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
        arc(x + w - r, y + r, -90, 0); arc(x + w - r, y + h - r, 0, 90)
        arc(x + r, y + h - r, 90, 180); arc(x + r, y + r, 180, 270)
        pts.append(pts[0])
        return pts

    def rect(self, x, y, w, h, r=4, width=2, color=INK, fill=None, dashed=False):
        base = self._rr_path(x, y, w, h, r)
        if fill is not None:
            self.d.polygon([(px * S, py * S) for px, py in base], fill=fill)
        if r <= 0.5 and not dashed:
            # sketchy separate strokes with overshoot
            c = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            for i in range(4):
                a, b = c[i], c[(i + 1) % 4]
                self.line(a[0], a[1], b[0], b[1], width, color)
            return
        pts = self._densify(base, 4)
        # slight overlap at closing
        pts = pts + pts[1:4]
        self._poly(self._wobble(pts, 0.9), width, color, dashed)

    def circle(self, cx, cy, r, width=2, color=INK, fill=None):
        if fill is not None:
            self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill)
        a0 = self.rnd.uniform(0, 6.28)
        n = max(16, int(r * 1.5))
        pts = []
        for i in range(int(n * 1.12) + 1):
            a = a0 + 2 * math.pi * i / n
            rr = r + self.rnd.uniform(-0.25, 0.25) + 0.6 * math.sin(i / n * 6.28)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self._poly(pts, width, color)


    def ph(self, x, y, w, width=2.2):
        """placeholder text line"""
        self.line(x, y, x + w, y, width, (170, 170, 170))

    def xbox(self, x, y, w, h):
        self.rect(x, y, w, h, 2)
        self.line(x + 2, y + 2, x + w - 2, y + h - 2, 1.4)
        self.line(x + w - 2, y + 2, x + 2, y + h - 2, 1.4)


    # ---------- icons ----------
    def icon(self, name, cx, cy, s=10, width=2):
        L = lambda a, b, c, d: self.line(cx + a, cy + b, cx + c, cy + d, width, overshoot=False)
        if name == "home":
            L(-s, -1, 0, -s); L(0, -s, s, -1)
            self.rect(cx - s * .75, cy - 1, s * 1.5, s * .95, 1, width)
        elif name == "search":
            self.circle(cx - 2, cy - 2, s * .6, width); L(s * .25, s * .25, s * .85, s * .85)
        elif name == "list":
            for k in (-.6, 0, .6):
                L(-s * .8, s * k, s * .8, s * k)
        elif name == "chat":
            self.rect(cx - s, cy - s * .75, s * 2, s * 1.3, 4, width)
            L(-s * .4, s * .55, -s * .7, s)
        elif name == "user":
            self.circle(cx, cy - s * .45, s * .42, width)
            pts = [(cx + s * .85 * math.cos(a), cy + s * .95 + s * .8 * math.sin(a))
                   for a in [math.pi + i * math.pi / 12 for i in range(13)]]
            self._poly(pts, width)
        elif name == "x":
            L(-s * .6, -s * .6, s * .6, s * .6); L(s * .6, -s * .6, -s * .6, s * .6)
        elif name == "back":
            L(-s * .7, 0, s * .7, 0); L(-s * .7, 0, -s * .15, -s * .55); L(-s * .7, 0, -s * .15, s * .55)
        elif name == "chev":
            L(-s * .3, -s * .5, s * .25, 0); L(s * .25, 0, -s * .3, s * .5)
        elif name == "down":
            L(-s * .5, -s * .25, 0, s * .3); L(0, s * .3, s * .5, -s * .25)
        elif name == "plus":
            L(-s * .55, 0, s * .55, 0); L(0, -s * .55, 0, s * .55)
        elif name == "bell":
            pts = [(cx + s * .6 * math.cos(a), cy - s * .1 + s * .7 * math.sin(a))
                   for a in [math.pi + i * math.pi / 12 for i in range(13)]]
            self._poly(pts, width); L(-s * .6, -s * .1, -s * .75, s * .55); L(s * .6, -s * .1, s * .75, s * .55)
            L(-s * .85, s * .55, s * .85, s * .55)



    def save(self, path):
        self.img.resize((self.w, self.h), Image.LANCZOS).save(path)

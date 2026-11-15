"""
lowfi_kit — low-fidelity, hand-drawn (sketch-style) mobile wireframes for any project.

Minimal usage:
    from lowfi_kit import Screen, render_project
    def home(s):
        s.header("My bookings", chip="3")
        s.title("Next appointment")
        s.list_item("Haircut", "Sat 10 am", avatar="AB")
        s.button("+ New booking", "pri")
        s.nav([("home","Home"),("list","Bookings"),("user","Profile")], 1)
    render_project({"Proposal_1_Guided": [("01_Home", home)]}, "out", "My project")

Screens are composed top to bottom with a cursor (s.y); no coordinates needed.
For anything custom, draw with s.d (Sketch) and the functions in hand.py directly.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from sketch import Sketch, S, INK
import hand as _hand
from hand import hand, hatch, bar, hand_width

GRAY = (110, 110, 110)
LIGHT = (140, 140, 140)


class Screen:
    """One mobile screen. Default size 375 × 812 (iPhone X/11 Pro)."""

    def __init__(self, seed=1, w=375, h=812, margin=34):
        self.d = Sketch(seed, w, h)
        self.w, self.h = w, h
        self.x0, self.x1 = margin, w - margin
        self.cw = self.x1 - self.x0
        self.y = 98                     # content starts here
        self.bottom = h - 96            # content limit (above footer / nav bar)
        self._groups = []
        d = self.d
        d.rect(10, 10, w - 20, h - 20, 34, 3.4)
        d.line(10, 84, w - 10, 84, 3)

    # ------------------------------------------------------------ utilities
    def space(self, px=10): self.y += px
    def _fits(self, s, cap, maxw):
        while cap > 6 and hand_width(s, cap) > maxw: cap -= 0.25
        return cap

    # ------------------------------------------------------------ header
    def header(self, title, left=None, right=None, chip=None, link=None, align=None):
        """left: 'back' | 'x' | 'menu' | text  ·  right: text  ·  chip: text in a pill  ·  link: underlined text"""
        d, y = self.d, 50
        align = align or ("left" if not left else "center")
        if align == "left":
            hand(d, self.x0, y, title, self._fits(title, 15, self.cw - 90), width=2.4)
        else:
            hand(d, self.w / 2, y, title, self._fits(title, 13, self.cw - 150), "m", width=2.3)
        if left == "back": d.icon("back", self.x0 + 6, y, 11, 2.6)
        elif left == "x": d.icon("x", self.x0 + 4, y, 11, 2.6)
        elif left == "menu": d.icon("list", self.x0 + 6, y, 11, 2.6)
        elif left:
            d.icon("back", self.x0, y, 8, 2.2); hand(d, self.x0 + 12, y, left, 8)
        if right: hand(d, self.x1, y, right, 9, "r")
        if chip:
            w = hand_width(chip, 9) + 22
            d.rect(self.x1 - w, y - 14, w, 28, 12, 2.4); hand(d, self.x1 - w / 2, y, chip, 9, "m")
        if link: self._link(self.x1, y, link, 8, "r")

    # ------------------------------------------------------------ text
    def title(self, s, cap=12):
        self.y += cap * 0.7
        hand(self.d, self.x0 + self._ind(), self.y, s, self._fits(s, cap, self._w()), width=2.2)
        self.y += cap * 0.9 + 8

    def text(self, s, cap=8.5, gray=False, bold=False):
        self.y += cap * 0.6
        hand(self.d, self.x0 + self._ind(), self.y, s, self._fits(s, cap, self._w()),
             width=1.9 if bold else (1.3 if gray else 1.6), color=GRAY if gray else INK)
        self.y += cap * 0.8 + 6

    def label(self, s): self.text(s, 8.5, bold=True)
    def hint(self, s): self.text(s, 7.5, gray=True)

    def lines(self, n=2, widths=(1, .75, .55)):
        """Filler lines standing in for paragraphs."""
        for i in range(n):
            self.y += 8
            self.d.line(self.x0 + self._ind(), self.y, self.x0 + self._ind() + self._w() * widths[i % len(widths)], self.y, 2.2)
            self.y += 6
        self.y += 6

    def placeholder_bar(self, frac=0.5, h=12):
        bar(self.d, self.x0 + self._ind(), self.y, self._w() * frac, h); self.y += h + 10

    def _link(self, x, y, s, cap=7.5, anchor="r"):
        w = hand(self.d, x, y, s, cap, anchor, width=1.5)
        x0 = x - w if anchor == "r" else x
        self.d.line(x0, y + 7, x0 + w, y + 7, 1.4)
        return w

    def link(self, s, align="left"):
        self.y += 6
        if align == "left": self._link(self.x0 + self._ind(), self.y, s, 8, "l")
        else: self._link(self.x0 + self._ind() + self._w(), self.y, s, 8, "r")
        self.y += 18

    # ------------------------------------------------------------ media
    def image(self, h=120):
        self.d.xbox(self.x0 + self._ind(), self.y, self._w(), h); self.y += h + 12

    def avatar(self, cx, cy, ini, r=16):
        self.d.circle(cx, cy, r, 2.4); hand(self.d, cx, cy, ini, 8, "m", width=1.6)

    # ------------------------------------------------------------ controls
    def button(self, label, kind="sec", h=48, x=None, w=None, advance=True):
        """kind: 'pri' (double outline) | 'sec' | 'off' (disabled, dashed)"""
        d = self.d
        x = self.x0 + self._ind() if x is None else x
        w = self._w() if w is None else w
        y = self.y
        cap = self._fits(label, 10.5 if h >= 44 else 9.5, w - 20)
        if kind == "pri":
            d.rect(x, y, w, h, 14, 3.4); d.rect(x + 4, y + 4, w - 8, h - 8, 11, 1.4)
            hand(d, x + w / 2, y + h / 2, label, cap, "m", width=2.3)
        elif kind == "off":
            d.rect(x, y, w, h, 14, 2.2, LIGHT, dashed=True)
            hand(d, x + w / 2, y + h / 2, label, cap, "m", width=1.6, color=LIGHT)
        else:
            d.rect(x, y, w, h, 14, 2.4); hand(d, x + w / 2, y + h / 2, label, cap, "m", width=1.9)
        if advance: self.y += h + 12

    def buttons(self, items, h=46):
        """items: [("Cancel","sec"), ("Accept","pri")] in one row."""
        n, gap = len(items), 10
        w = (self._w() - gap * (n - 1)) / n
        for i, (lab, kind) in enumerate(items):
            self.button(lab, kind, h, self.x0 + self._ind() + i * (w + gap), w, advance=False)
        self.y += h + 12

    def field(self, label, value=None, h=36, multiline=False):
        d = self.d
        self.label(label)
        h = 56 if multiline and h == 36 else h
        x, w = self.x0 + self._ind(), self._w()
        d.rect(x, self.y, w, h, 6, 2.2)
        if value:
            vals = value if isinstance(value, (list, tuple)) else [value]
            for i, v in enumerate(vals):
                hand(d, x + 10, self.y + 17 + i * 16, v, self._fits(v, 7.5, w - 20), width=1.3, color=GRAY)
        self.y += h + 12

    def select(self, label, value):
        self.label(label)
        x, w = self.x0 + self._ind(), self._w()
        self.d.rect(x, self.y, w, 36, 6, 2.2); hand(self.d, x + 10, self.y + 18, value, 8.5, width=1.5)
        self.d.icon("down", x + w - 16, self.y + 18, 9, 2); self.y += 48

    def search(self, placeholder="Search..."):
        x, w = self.x0 + self._ind(), self._w()
        self.d.rect(x, self.y, w, 38, 10, 2.2); self.d.icon("search", x + 18, self.y + 19, 8, 2)
        hand(self.d, x + 34, self.y + 19, placeholder, 8.5, width=1.4, color=GRAY); self.y += 50

    def radios(self, options, h=38):
        """options: ["*Selected", "Other"] — a leading '*' marks the chosen one."""
        d = self.d
        for o in options:
            on = o.startswith("*"); o = o.lstrip("*")
            x, w = self.x0 + self._ind(), self._w()
            d.rect(x, self.y, w, h, 10, 2.8 if on else 1.9)
            d.circle(x + 18, self.y + h / 2, 7, 2)
            if on: d.circle(x + 18, self.y + h / 2, 3, 1, fill=INK)
            hand(d, x + 34, self.y + h / 2, o, self._fits(o, 9, w - 44), width=1.9 if on else 1.5)
            self.y += h + 8
        self.y += 4

    def checkboxes(self, options):
        d = self.d
        for o in options:
            on = o.startswith("*"); o = o.lstrip("*")
            x = self.x0 + self._ind()
            d.rect(x, self.y, 18, 18, 3, 2)
            if on:
                d.line(x + 4, self.y + 9, x + 8, self.y + 14, 2.2, overshoot=False)
                d.line(x + 8, self.y + 14, x + 15, self.y + 4, 2.2, overshoot=False)
            hand(d, x + 28, self.y + 9, o, 8.5, width=1.5); self.y += 28
        self.y += 4

    def toggle(self, label, on=True):
        d, x = self.d, self.x0 + self._ind()
        hand(d, x, self.y + 12, label, 8.5, width=1.6)
        tx = x + self._w() - 44
        d.rect(tx, self.y, 44, 24, 12, 2.2)
        if on: hatch(d, tx + 4, self.y + 4, 36, 16, 4, 0.9)
        d.circle(tx + (32 if on else 12), self.y + 12, 8, 2, fill=(255, 255, 255))
        self.y += 36

    def chips(self, items, cap=8):
        """items: ["*Active", "Other"] — wraps onto several rows if needed."""
        d = self.d
        x0, maxw = self.x0 + self._ind(), self._w()
        cx, cy = x0, self.y
        for s in items:
            on = s.startswith("*"); s = s.lstrip("*")
            w = hand_width(s, cap) + 20
            if cx + w > x0 + maxw: cx, cy = x0, cy + 32
            d.rect(cx, cy, w, 26, 12, 2.8 if on else 1.9)
            if on: hatch(d, cx + 8, cy + 20, w - 16, 4, 4, 0.9)
            hand(d, cx + w / 2, cy + (12 if on else 13), s, cap, "m", width=1.8 if on else 1.4)
            cx += w + 7
        self.y = cy + 38

    def segmented(self, items, active=0, h=36):
        d, x, w = self.d, self.x0 + self._ind(), self._w() / len(items)
        for i, s in enumerate(items):
            d.rect(x + i * w, self.y, w, h, 2, 2.8 if i == active else 1.9)
            if i == active: hatch(d, x + i * w + 2, self.y + h - 8, w - 4, 6, 4, 1)
            hand(d, x + i * w + w / 2, self.y + h / 2 - (2 if i == active else 0), s,
                 self._fits(s, 8.5, w - 12), "m", width=1.9 if i == active else 1.4)
        self.y += h + 12

    def tabs(self, items, active=0): self.segmented(items, active, 38)

    def stepper(self, label, value, unit=""):
        self.label(label); d, x = self.d, self.x0 + self._ind()
        for s, xx, w in [("-", x, 40), (str(value), x + 46, 54), ("+", x + 106, 40)]:
            d.rect(xx, self.y, w, 36, 6, 2.2); hand(d, xx + w / 2, self.y + 18, s, 11, "m", width=2)
        if unit: hand(d, x + 158, self.y + 18, unit, 8, width=1.4, color=GRAY)
        self.y += 48

    def progress(self, n, total, name=None):
        d, x = self.d, self.x0 + self._ind()
        seg = (self._w() - 4 * (total - 1)) / total
        for i in range(total):
            d.rect(x + i * (seg + 4), self.y, seg, 10, 4, 2)
            if i < n: hatch(d, x + i * (seg + 4) + 1, self.y + 1, seg - 2, 8, 4, 1)
        self.y += 32
        hand(d, x, self.y - 8, f"Step {n} of {total}" + (f" · {name}" if name else ""), 7.5, width=1.4, color=GRAY)
        self.y += 12

    def steps(self, names, current=0):
        """Compact 1 → 2 → 3 … indicator with names underneath."""
        d, n = self.d, len(names)
        span = self._w() / n
        cy = self.y + 12
        for i, nm in enumerate(names):
            cx = self.x0 + self._ind() + span * (i + .5)
            d.circle(cx, cy, 11, 3 if i == current else 2.2)
            hand(d, cx, cy, str(i + 1), 8, "m", width=1.7)
            hand(d, cx, cy + 22, nm, self._fits(nm, 6.5, span - 4), "m", width=1.2)
            if i < n - 1:
                nx = cx + span
                d.line(cx + 15, cy, nx - 16, cy, 1.8, overshoot=False)
                d.line(nx - 16, cy, nx - 21, cy - 4, 1.8, overshoot=False)
                d.line(nx - 16, cy, nx - 21, cy + 4, 1.8, overshoot=False)
        self.y += 48

    # ------------------------------------------------------------ containers
    def list_item(self, title, sub=None, avatar=None, right=None, chevron=True, selected=False, h=None):
        d, x, w = self.d, self.x0 + self._ind(), self._w()
        h = h or (54 if sub else 44)
        d.rect(x, self.y, w, h, 10, 2.8 if selected else 2.2)
        tx = x + 12
        if avatar:
            self.avatar(x + 26, self.y + h / 2, avatar, 15); tx = x + 50
        ty = self.y + (h / 2 - 8 if sub else h / 2)
        hand(d, tx, ty, title, self._fits(title, 9, w - (tx - x) - 70), width=1.8)
        if sub: hand(d, tx, ty + 17, sub, 7.5, width=1.3, color=GRAY)
        if right: self._link(x + w - (30 if chevron else 12), self.y + h / 2, right)
        if chevron and not right: d.icon("chev", x + w - 16, self.y + h / 2, 11, 2.4)
        self.y += h + 8

    def card_grid(self, labels, cols=2, h=60, with_image=True):
        d = self.d
        gap = 9
        w = (self._w() - gap * (cols - 1)) / cols
        for i, lab in enumerate(labels):
            x = self.x0 + self._ind() + (i % cols) * (w + gap)
            y = self.y + (i // cols) * (h + 10)
            d.rect(x, y, w, h, 10, 2.6)
            tx = x + 12
            if with_image:
                s = min(36, h - 20); d.xbox(x + 10, y + (h - s) / 2, s, s); tx = x + s + 20
            hand(d, tx, y + h / 2, lab, self._fits(lab, 9, w - (tx - x) - 24), width=1.9)
            d.icon("chev", x + w - 13, y + h / 2, 9, 2)
        rows = (len(labels) + cols - 1) // cols
        self.y += rows * (h + 10) + 4

    def kv(self, pairs, keyw=100):
        for k, v in pairs:
            self.y += 10
            hand(self.d, self.x0 + self._ind(), self.y, k, 7.5, width=1.3, color=GRAY)
            hand(self.d, self.x0 + self._ind() + keyw, self.y, v, self._fits(v, 8.5, self._w() - keyw), width=1.7)
            self.y += 12

    def row_edit(self, label, action="Edit"):
        d, x, w = self.d, self.x0 + self._ind(), self._w()
        d.rect(x, self.y, w, 36, 8, 2); hand(d, x + 12, self.y + 18, label, 8.5, width=1.6)
        self._link(x + w - 12, self.y + 18, action); self.y += 44

    def check_line(self, s):
        d, x = self.d, self.x0 + self._ind()
        cy = self.y + 10
        d.circle(x + 10, cy, 9, 2)
        d.line(x + 6, cy, x + 9, cy + 4, 2.2, overshoot=False); d.line(x + 9, cy + 4, x + 15, cy - 4, 2.2, overshoot=False)
        hand(d, x + 28, cy, s, self._fits(s, 8.5, self._w() - 30), width=1.8); self.y += 30

    def begin_box(self, title=None, kind="normal", state=None, right=None):
        """Group content in a box. kind: normal | strong | dashed | accordion.
        state (accordion): 'open' | 'done' | 'closed'. Close with end_box()."""
        y0 = self.y
        self._groups.append((y0, kind))
        self.y += 10
        if title:
            d, x = self.d, self.x0 + self._ind() + 12
            hy = self.y + 8
            if kind == "accordion" or state:
                ic = {"done": None, "open": "down", "closed": "chev"}.get(state, "chev")
                if state == "done":
                    d.circle(x + 6, hy, 8, 2)
                    d.line(x + 2, hy, x + 5, hy + 4, 2.2, overshoot=False); d.line(x + 5, hy + 4, x + 11, hy - 4, 2.2, overshoot=False)
                else:
                    d.icon(ic, x + 6, hy, 11, 2.4)
                x += 24
            hand(d, x, hy, title, 9, width=2 if state == "open" or kind == "strong" else 1.6)
            if right: self._link(self.x0 + self._ind() + self._w() - 12, hy, right)
            self.y += 26
            if state == "open":
                d.line(self.x0 + self._ind() + 10, self.y - 4, self.x0 + self._ind() + self._w() - 10, self.y - 4, 1.4, GRAY, dashed=True)
                self.y += 6
        if state in ("done", "closed"):
            self.y = y0 + 36
        self._indent = getattr(self, "_indent", 0) + 12

    def end_box(self):
        y0, kind = self._groups.pop()
        self._indent -= 12
        x, w = self.x0 + self._ind(), self._w()
        if self.y - y0 > 40: self.y += 2
        h = self.y - y0
        if kind == "dashed": self.d.rect(x, y0, w, h, 8, 2.4, dashed=True)
        elif kind == "strong": self.d.rect(x, y0, w, h, 12, 3)
        else: self.d.rect(x, y0, w, h, 10, 2.2)
        self.y += 10

    def accordion(self, title, state="closed", right=None):
        """Collapsed or completed accordion on one line. For an open one: begin_box(title, state='open') … end_box()."""
        self.begin_box(title, "accordion", state, right); self.end_box(); self.y -= 2

    def alert(self, title, sub=None, chips=None):
        """Error / validation warning: thick dashed box with '!'."""
        self.begin_box(None, "dashed")
        self.text("! " + title, 9.5, bold=True)
        if sub: self.hint(sub)
        if chips: self.chips(chips); self.y -= 8
        self.end_box()

    def info(self, s, sub=None):
        d, x, w = self.d, self.x0 + self._ind(), self._w()
        h = 40 if not sub else 54
        d.rect(x, self.y, w, h, 8, 1.9)
        d.circle(x + 18, self.y + 20, 8, 1.8); hand(d, x + 18, self.y + 20, "i", 8, "m", width=1.5)
        hand(d, x + 34, self.y + 20, s, self._fits(s, 7.5, w - 44), width=1.5)
        if sub: hand(d, x + 34, self.y + 38, sub, self._fits(sub, 7, w - 44), width=1.2, color=GRAY)
        self.y += h + 12

    def note(self, lines):
        """Design annotation (not UI): confirmations, later states, rules."""
        d, x, w = self.d, self.x0 + self._ind(), self._w()
        h = 26 + 15 * len(lines)
        d.rect(x, self.y, w, h, 2, 1.7, GRAY, dashed=True)
        d.line(x + w - 14, self.y, x + w, self.y + 14, 1.5, GRAY, overshoot=False)
        hand(d, x + 10, self.y + 13, "Note", 7, width=1.4, color=GRAY)
        cap = min([7] + [7 * (w - 22) / max(1, hand_width(t, 7)) for t in lines])
        for i, t in enumerate(lines):
            hand(d, x + 10, self.y + 30 + i * 15, t, cap, width=1.25, color=GRAY)
        self.y += h + 12

    # ------------------------------------------------------------ bottom area
    def footer(self, items):
        """Buttons pinned to the bottom. items: [("Back","sec"), ("Next →","pri")] or a single pair."""
        d = self.d
        d.line(10, self.h - 96, self.w - 10, self.h - 96, 3)
        y_save, ind = self.y, getattr(self, "_indent", 0)
        self._indent = 0
        self.y = self.h - 78
        if len(items) == 2 and items[0][0].lower() in ("back", "cancel", "atrás", "atras", "volver", "cancelar") and len(items[0][0]) < 9:
            self.button(items[0][0], items[0][1], 48, self.x0, 92, advance=False)
            self.button(items[1][0], items[1][1], 48, self.x0 + 102, self.cw - 102, advance=False)
        else:
            self.buttons(items, 48)
        self.y, self._indent = y_save, ind

    def nav(self, items, active=0):
        """Bottom tab bar. items: [(icon, label)] · icons: home search list chat user bell plus."""
        d = self.d
        d.line(10, self.h - 96, self.w - 10, self.h - 96, 3)
        span = (self.w - 40) / len(items)
        for i, (ic, lab) in enumerate(items):
            cx = 20 + span * (i + .5)
            if i == active:
                d.rect(cx - span / 2 + 4, self.h - 86, span - 8, 62, 10, 2.6)
                hatch(d, cx - span / 2 + 6, self.h - 32, span - 12, 6, 4, 1)
            d.icon(ic, cx, self.h - 64, 11, 2.8)
            hand(d, cx, self.h - 42, lab, self._fits(lab, 6, span - 10), "m", width=1.2)

    def fab(self, label, sub=None, hint=None):
        """Labelled floating action button (above the tab bar)."""
        d = self.d
        w = max(hand_width(label, 9.5), hand_width(sub or "", 6.5)) + 40
        x, y = self.x1 - w, self.h - 186
        if hint: hand(d, self.x1, y - 16, hint, 7, "r", width=1.2, color=GRAY)
        d.rect(x, y, w, 50, 25, 3.2); d.rect(x + 4, y + 4, w - 8, 42, 21, 1.3)
        hand(d, x + w / 2, y + (19 if sub else 25), label, 9.5, "m", width=2.1)
        if sub: hand(d, x + w / 2, y + 36, sub, 6.5, "m", width=1.1, color=GRAY)

    def sheet(self, title, dim_title=None):
        """Turn the screen into a bottom sheet: dimmed background on top, content from y≈190."""
        d = self.d
        hatch(d, 14, 18, self.w - 28, 156, 9, 0.8, (200, 200, 200))
        if dim_title: hand(d, self.x0, 50, dim_title, 13, width=2, color=(170, 170, 170))
        d.d.rectangle([12 * S, 86 * S, (self.w - 12) * S, (self.h - 40) * S], fill="white")
        hatch(d, 14, 88, self.w - 28, 86, 9, 0.8, (200, 200, 200))
        d.d.rectangle([12 * S, 176 * S, (self.w - 12) * S, (self.h - 40) * S], fill="white")
        d.line(10, 178, self.w - 10, 178, 3.4); d.line(self.w / 2 - 20, 192, self.w / 2 + 20, 192, 3, (150, 150, 150))
        hand(d, self.x0, 220, title, 12, width=2.2); d.icon("x", self.x1 - 8, 220, 11, 2.6)
        self.y = 248

    # ------------------------------------------------------------ internals
    def _ind(self): return getattr(self, "_indent", 0)
    def _w(self): return self.cw - 2 * self._ind()

    def save(self, path):
        if self.y > self.bottom + 4:
            print(f"  ⚠ {os.path.basename(path)}: content reaches y={self.y:.0f} (limit {self.bottom}). Reduce content.")
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.d.save(path)


# ================================================================ full project
def _row(folder_dir, items, heading, gap=40, top=80, w=375, h=812, seed=7):
    W = len(items) * w + (len(items) + 1) * gap
    Hh = top + 30 + h + gap
    c = Sketch(seed, w=W, h=Hh)
    hand(c, gap, 36, heading, 18, width=2.6)
    for i, (name, _, ttl) in enumerate(items):
        hand(c, gap + i * (w + gap), top + 6, ttl, 10, width=1.9)
    img = c.img.resize((W, Hh), Image.LANCZOS)
    for i, (name, _, _) in enumerate(items):
        img.paste(Image.open(os.path.join(folder_dir, name + ".png")), (gap + i * (w + gap), top + 30))
    return img


def render_project(proposals, out, project_title="Wireframes", w=375, h=812):
    """proposals: {"Proposal_1_Guided": [("01_Home", fn) | ("01_Home", fn, "01 · Home"), ...], ...}
    Writes <out>/<proposal>/<screen>.png and <out>/Comparison/*.png. Returns the list of paths."""
    _hand.MISSING.clear()
    paths, rows = [], []
    for pi, (folder, screens) in enumerate(proposals.items()):
        items = []
        for k, sc in enumerate(screens):
            name, fn = sc[0], sc[1]
            ttl = sc[2] if len(sc) > 2 else name.replace("_", " · ", 1)
            s = Screen(seed=100 + 50 * pi + k, w=w, h=h)
            fn(s)
            p = os.path.join(out, folder, name + ".png"); s.save(p); paths.append(p)
            items.append((name, fn, ttl))
        parts = folder.split("_")
        heading = " ".join(parts[:2]) + (" · " + " ".join(parts[2:]) if len(parts) > 2 else "")
        img = _row(os.path.join(out, folder), items, heading, w=w, h=h, seed=7 + pi)
        os.makedirs(os.path.join(out, "Comparison"), exist_ok=True)
        p = os.path.join(out, "Comparison", f"{folder.split('_')[0]}_{folder.split('_')[1]}_Full.png" if folder.count("_") >= 1 else f"{folder}_Full.png")
        img.save(p); paths.append(p); rows.append(img)
    if len(rows) > 1:
        Wm = max(r.width for r in rows)
        c = Sketch(9, w=Wm, h=80 + sum(r.height for r in rows))
        hand(c, 40, 40, project_title, 20, width=2.8)
        both = c.img.resize((Wm, 80 + sum(r.height for r in rows)), Image.LANCZOS)
        y = 80
        for r in rows: both.paste(r, (0, y)); y += r.height
        p = os.path.join(out, "Comparison", "All_Proposals.png"); both.save(p); paths.append(p)
    if _hand.MISSING:
        print("  ⚠ Characters without a glyph (drawn as blanks):", "".join(sorted(_hand.MISSING)))
    for p in paths:
        if "Comparison" not in p:
            assert Image.open(p).size == (w, h), p
    print(f"✓ {len(paths)} images in {out}")
    return paths

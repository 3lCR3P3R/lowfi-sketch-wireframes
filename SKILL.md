---
name: lowfi-sketch-wireframes
description: Generates low-fidelity, hand-drawn mobile wireframes (imperfect black strokes, hand lettering, hatching, crossed image boxes) as one PNG per screen plus side-by-side comparison sheets. Use it in any project that asks for low-fi wireframes, sketches, hand-drawn mockups or for comparing alternative proposals of a user flow.
---

# Low-fi sketch wireframes

This skill produces mobile screens that look drawn on paper or in FigJam. They exist to **explore structure and flow**, not to present a finished UI. Everything is drawn in code (Python + Pillow): no HTML screenshots and no external fonts.

## Files

| File | Purpose |
|---|---|
| `scripts/lowfi_kit.py` | **Main library.** `Screen` lays a screen out top to bottom with a cursor (no coordinates). `render_project()` writes the PNGs, the comparison sheets and runs the checks. |
| `scripts/template_project.py` | **Starting point.** Fictional example with 2 proposals × 3 screens. Copy it and replace the screens. |
| `scripts/sketch.py` | Drawing base: wobbly lines, rectangles, circles, crossed boxes, icons. |
| `scripts/hand.py` | Uppercase hand lettering drawn stroke by stroke, hatching (`hatch`) and hatched placeholder bars (`bar`). |
| `examples/template_output.png` | Output of the template, as a visual reference. |

Requirement: Python 3 + Pillow (`pip install pillow`).

```bash
cp scripts/template_project.py my_flow.py   # edit the screens
OUT=./MyProject_Wireframes_v1 python3 my_flow.py
```
(Keep `my_flow.py` next to `lowfi_kit.py`, `sketch.py` and `hand.py`, or add `scripts/` to `sys.path`.)

---

## 1. Workflow

1. **Understand the request:** product, user, flow, number of screens and device size (default 375 × 812).
   **Ask how many proposals to create** before drawing (see «Number of proposals» below). Default: **2**.
2. **Write the minimum content of each screen** before drawing: title, actions, sample data and states. Use the same data in every proposal.
3. **Define the structural difference** between proposals (section 4) before composing.
4. **Compose** each screen as a function `def screen(s): ...` using the `Screen` methods.
5. **Run** `render_project({...}, out, "Title")`.
6. **Validate** (section 5) and fix.
7. **Deliver** in a versioned folder (`<Project>_Wireframes_vN/`) **without overwriting earlier versions**. If asked, add a `UX_ANALYSIS.md` (section 6).

### Number of proposals (N)

The number of proposals is a variable **N ≥ 1**, with a **default of 2**.

- **Always ask before composing**, unless the user already gave a number. Use a multiple-choice question when available, for example: «How many alternative proposals do you want for this flow?» → `2 (Recommended)` · `1` · `3` · *Other*.
- If nobody answers (unattended run), use **2** and say at the top of the delivery that you assumed the default.
- **N = 1:** skip the comparison rules in section 4; only `Proposal_1_Full.png` is produced.
- **N ≥ 3:** every proposal needs its own dominant structure. The abstraction test applies to **each pair** of proposals, not only to the first two. If you cannot make a proposal genuinely different, say so and suggest a smaller N instead of producing near-duplicates.
- `render_project` accepts any number of entries in its dictionary. It writes one `Proposal_<i>_Full.png` per proposal and stacks all of them in `All_Proposals.png`.

## 2. `Screen` API (lowfi_kit)

Everything stacks vertically from y≈98. A leading `"*"` marks an option as selected.

| Area | Methods |
|---|---|
| Header | `header(title, left='back'│'x'│'menu'│text, right=text, chip=text, link=text)` |
| Text | `title(s)` · `text(s, cap, gray, bold)` · `label(s)` · `hint(s)` · `link(s)` · `lines(n)` · `placeholder_bar(frac)` |
| Media | `image(h)` (crossed box) · `avatar(cx, cy, initials)` |
| Inputs | `field(label, value│[lines], multiline)` · `select(label, value)` · `search(text)` · `radios([...])` · `checkboxes([...])` · `toggle(label, on)` · `chips([...])` · `segmented([...], active)` · `tabs([...], active)` · `stepper(label, value, unit)` |
| Progress | `progress(n, total, name)` (step bar) · `steps([names], current)` (1 → 2 → 3) |
| Content | `list_item(title, sub, avatar, right, chevron, selected)` · `card_grid([labels], cols)` · `kv([(key, value)])` · `row_edit(label)` · `check_line(s)` · `info(s, sub)` |
| Grouping | `begin_box(title, kind='normal'│'strong'│'dashed', state='open')` … `end_box()` · `accordion(title, 'done'│'closed', right)` |
| Validation | `alert(title, sub, chips)` (dashed box with «!») · `note([lines])` (design annotation, not UI) |
| Buttons | `button(label, 'pri'│'sec'│'off')` · `buttons([(label, kind), ...])` |
| Bottom area | `footer([(label, kind), ...])` (pinned CTAs) · `nav([(icon, label)], active)` · `fab(label, sub, hint)` |
| Variants | `sheet(title, dim_title)` (bottom sheet over a dimmed background) |

- Available icons: `home search list chat user bell plus back x chev down`.
- For anything not covered, draw directly on `s.d` (Sketch) and with `hand(s.d, x, y, text, cap)`.
- `Screen(w=390, h=844)` supports other sizes; `render_project(..., w=390, h=844)` passes them through.

## 3. Visual rules

1. **Black on white only.** Gray is for secondary text and notes. No colors, gradients or shadows.
2. **Imperfect strokes everywhere:** gentle wobble, overshooting line ends, overlapping closures.
3. **Uppercase hand lettering** inside screens. Cap sizes: titles 12–15, body 8–10, notes 7, tab bar 6 minimum. `lowfi_kit` shrinks text automatically when it does not fit.
4. **No solid-filled buttons:** primary = double outline; secondary = single outline; disabled = gray dashed.
5. **Selection = hatching** (bottom stripe or fill), never a black block.
6. **Schematic filler:** hatched bars for names and secondary titles, lines for paragraphs, crossed boxes for images.
7. **Minimal text:** only what is needed to understand each decision.
8. **Nothing decorative:** every element must communicate a function.
9. **Balanced negative space:** if more than a third of the screen is empty, move the main action up or tighten the layout. Never fill it with decoration.

## 4. UX rules for comparing proposals

- **Same scenario:** same user, same data, same features, same number of screens, same end result. Only the information architecture, navigation, hierarchy and arrangement of actions change.
- **Abstraction test:** reduced to boxes and arrows, every proposal must still look different from every other one. Each needs its own dominant shape, for example:
  - *guided:* a column of steps, progress bar, one CTA per screen, progress blocked while a required field is missing;
  - *modular:* tabs or a card grid, collapsible sections in any order, review with in-place fixes, undo;
  - other options: search-first, conversational, card-based, single long page.
- **One state per screen.** Confirmations, later states and rules are documented with `note()` or in a clearly separate extra screen.
- **Actions that look alike must be told apart** with microcopy (for example, "the category is preselected" vs "no category").
- **Error prevention and feedback stay visible:** required fields with `*`, warnings with `alert()`, disabled buttons with `'off'`.
- **Do not declare a winning proposal** without evidence from user testing.

## 5. Validation before delivery

`render_project` already warns about three things:
- `⚠ … content reaches y=…`: the screen overflows. Remove content or reduce heights.
- `⚠ Characters without a glyph`: some characters were drawn as blanks. Replace them or add them to `hand.py` (section 7).
- If any single screen is not exactly `w × h`, the script stops on an `assert`.

Also check the `Comparison/All_Proposals.png` sheet by eye:
- no overlapping text and nothing outside the frame;
- visual consistency across all screens;
- the proposals are genuinely different (abstraction test).

## 6. Delivery structure

```
<Project>_Wireframes_vN/
├── Proposal_1_<Name>/01_<Screen>.png …
├── Proposal_2_<Name>/…
├── …                      (one folder per proposal, N in total)
├── Comparison/Proposal_1_Full.png … Proposal_N_Full.png · All_Proposals.png
└── UX_ANALYSIS.md   (if requested)
```

The comparison sheets paste screens unscaled, aligned horizontally, 40 px apart.

Suggested `UX_ANALYSIS.md`:
1. Problems in the previous version.
2. Changes and their UX rationale (cite Nielsen's heuristics where relevant).
3. Table of differences between proposals.
4. Strengths and limitations of each flow.
5. Questions to validate with users.

## 7. Extending

- **New character:** add it to `G` in `hand.py` as `'X': (width, [[(x, y), …], …])`. The grid is 6 units tall, with y = 0 at the top. It already includes A–Z, Ñ, Ü, accented vowels, 0–9 and `+ - = % # $ & @ ' " , . : · ! ? ¿ ( ) [ ] / * < > → ← —`.
- **New icon:** add it to `Sketch.icon()` using lines or circles relative to `(cx, cy)` and size `s`.
- **New component:** add a method to `Screen` that draws from `self.y` and advances `self.y` when done.
- **More or less wobble:** tune `amp` in `_wobble` (boxes ≈ 0.9, letters ≈ 0.25).

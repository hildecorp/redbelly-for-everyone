"""Draws the five thread images from scratch (no stock art, no logos).

Run: python3 tools/build_images.py
Output: entry/images/*.png at 1600x900 (16:9, X's preferred in-feed ratio).
Colours are from the public Redbelly brand page; the font is Readex Pro
(SIL Open Font License, see fonts/OFL.txt).
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "entry" / "images"
FONTS = ROOT / "fonts"

W, H = 1600, 900
NAVY = "#142530"
SLATE = "#283A46"
RED = "#FF5050"
RED_DARK = "#FA423C"
GREY = "#848B91"
LIGHT = "#ECEBEC"
WHITE = "#FFFFFF"
GREEN = "#3DD68C"

# Every string drawn on any image, collected so check_entry.py can scan them.
ALL_TEXT = []


def font(size, weight="Medium"):
    return ImageFont.truetype(str(FONTS / f"ReadexPro-{weight}.woff"), size)


def text(d, xy, s, size, fill=WHITE, weight="Medium", anchor="la"):
    ALL_TEXT.append(s)
    d.text(xy, s, font=font(size, weight), fill=fill, anchor=anchor)


def wrapped(d, xy, s, size, width, fill=WHITE, weight="Medium", gap=1.3, anchor_center=False):
    ALL_TEXT.append(s)
    f = font(size, weight)
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    x, y = xy
    for line in lines:
        if anchor_center:
            d.text((x, y), line, font=f, fill=fill, anchor="ma")
        else:
            d.text((x, y), line, font=f, fill=fill)
        y += int(size * gap)
    return y


def canvas():
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    # Soft red glow in the corner for depth.
    glow = Image.new("RGB", (W, H), NAVY)
    g = ImageDraw.Draw(glow)
    for r in range(520, 0, -8):
        t = 1 - r / 520
        c = tuple(int(a + (b - a) * t * 0.35) for a, b in
                  zip((0x14, 0x25, 0x30), (0xFF, 0x50, 0x50)))
        g.ellipse((W - r, -r, W + r, r), fill=c)
    im = Image.blend(im, glow, 1.0)
    d = ImageDraw.Draw(im)
    # Accent bar.
    d.rectangle((0, 0, 14, H), fill=RED)
    return im, d


def footer(d, s="Redbelly, in plain English"):
    text(d, (80, H - 60), s, 24, fill=GREY, weight="Regular")


def tick(d, cx, cy, r, colour=GREEN):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=colour)
    w = max(4, r // 4)
    d.line([(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.38),
            (cx + r * 0.5, cy - r * 0.35)], fill=NAVY, width=w, joint="curve")


def cross(d, cx, cy, r, colour=RED):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=colour)
    w = max(4, r // 4)
    k = r * 0.4
    d.line([(cx - k, cy - k), (cx + k, cy + k)], fill=NAVY, width=w)
    d.line([(cx - k, cy + k), (cx + k, cy - k)], fill=NAVY, width=w)


def arrow(d, x1, y, x2, colour=RED, width=8):
    d.line([(x1, y), (x2 - 18, y)], fill=colour, width=width)
    d.polygon([(x2, y), (x2 - 28, y - 18), (x2 - 28, y + 18)], fill=colour)


def card(d, box, fill=SLATE, outline=None, radius=28, width=4):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def building(d, x, y, w, h, colour=LIGHT):
    d.rectangle((x, y, x + w, y + h), fill=colour)
    cols, rows = 4, 6
    pw, ph = w / (cols * 2 + 1), h / (rows * 2 + 1)
    for c in range(cols):
        for r in range(rows):
            wx = x + pw * (1 + 2 * c)
            wy = y + ph * (1 + 2 * r)
            d.rectangle((wx, wy, wx + pw, wy + ph), fill=SLATE)


# ---------------------------------------------------------------- images

def img_money_vs_ownership():
    im, d = canvas()
    text(d, (80, 80), "Money moves fast.", 76, weight="Bold")
    text(d, (80, 170), "Ownership doesn't.", 76, fill=RED, weight="Bold")

    card(d, (80, 330, 760, 780))
    text(d, (130, 380), "Sending money to a friend", 36, fill=LIGHT)
    # phone
    d.rounded_rectangle((130, 460, 250, 690), radius=20, outline=LIGHT, width=6)
    d.rounded_rectangle((165, 475, 215, 485), radius=4, fill=LIGHT)
    tick(d, 190, 575, 34)
    text(d, (300, 520), "Seconds", 84, fill=GREEN, weight="Bold")
    text(d, (304, 625), "tap, sent, done", 30, fill=GREY, weight="Regular")

    card(d, (840, 330, 1520, 780))
    text(d, (890, 380), "Changing who owns a bond,", 36, fill=LIGHT)
    text(d, (890, 427), "a loan or a building", 36, fill=LIGHT)
    # paper stack
    for i in range(3):
        d.rectangle((890 + i * 14, 500 + i * 14, 990 + i * 14, 640 + i * 14),
                    fill=LIGHT, outline=SLATE, width=3)
    for j in range(5):
        d.line([(940, 545 + j * 18), (1010, 545 + j * 18)], fill=GREY, width=4)
    y = 510
    for s in ("Paperwork", "Middlemen", "Days"):
        text(d, (1080, y), s, 46, fill=RED, weight="Bold")
        y += 66
    footer(d)
    return im


def img_pizza():
    im, d = canvas()
    text(d, (80, 70), "Tokenisation", 76, fill=RED, weight="Bold")
    text(d, (80, 165), "= cutting a big asset into digital slices", 46, fill=WHITE)

    building(d, 120, 330, 260, 420)
    text(d, (250, 775), "One big asset", 30, fill=LIGHT, anchor="ma")
    arrow(d, 430, 540, 610)

    cx, cy, r = 960, 545, 285
    owners = ["Ana", "Ben", "Chen", "Dev", "Ella", "Femi", "Gus", "Hira"]
    for i in range(8):
        a0 = i * 45 - 90
        off = 14
        mid = math.radians(a0 + 22.5)
        ox, oy = math.cos(mid) * off, math.sin(mid) * off
        d.pieslice((cx - r + ox, cy - r + oy, cx + r + ox, cy + r + oy), a0, a0 + 45,
                   fill=RED if i % 2 == 0 else RED_DARK, outline=NAVY, width=6)
        tx = cx + math.cos(mid) * r * 0.62 + ox
        ty = cy + math.sin(mid) * r * 0.62 + oy
        text(d, (tx, ty), owners[i], 28, fill=WHITE, weight="Bold", anchor="mm")
    wrapped(d, (1310, 420), "Each slice has a clear owner on record", 34, 250, fill=LIGHT)
    footer(d, "Made-up names, for illustration")
    return im


def img_bouncer():
    im, d = canvas()
    text(d, (80, 70), "The rules travel with the slice", 66, weight="Bold")
    text(d, (80, 160), "Identity and eligibility are checked at the moment of the trade",
         34, fill=LIGHT, weight="Regular")

    def row(y, ok):
        # person
        d.ellipse((110, y - 95, 170, y - 35), fill=LIGHT)
        d.rounded_rectangle((95, y - 25, 185, y + 75), radius=26, fill=LIGHT)
        text(d, (140, y + 95), "Buyer", 28, fill=LIGHT, anchor="ma")
        arrow(d, 210, y, 330, colour=GREY, width=6)
        # door frame holding the checks
        card(d, (350, y - 110, 1010, y + 110), fill=SLATE, outline=RED, width=5)
        tick(d, 410, y - 45, 26)
        text(d, (452, y - 45), "Identity verified", 32, anchor="lm")
        if ok:
            tick(d, 410, y + 45, 26)
        else:
            cross(d, 410, y + 45, 26)
        text(d, (452, y + 45), "Allowed to buy this", 32, anchor="lm")
        arrow(d, 1030, y, 1150, colour=GREEN if ok else RED, width=6)
        if ok:
            text(d, (1180, y - 30), "Trade goes", 44, fill=GREEN, weight="Bold")
            text(d, (1180, y + 22), "through", 44, fill=GREEN, weight="Bold")
        else:
            text(d, (1180, y - 30), "Trade", 44, fill=RED, weight="Bold")
            text(d, (1180, y + 22), "blocked", 44, fill=RED, weight="Bold")

    row(380, True)
    row(660, False)
    footer(d, "Like a bouncer built into the door, not standing beside it")
    return im


def img_loan():
    im, d = canvas()
    text(d, (80, 60), "Paying off a loan:", 64, weight="Bold")
    text(d, (690, 60), "3 steps become 1", 64, fill=RED, weight="Bold")

    text(d, (80, 185), "The usual way", 34, fill=GREY)
    steps = ["Payment made", "Loan closed", "Collateral handed back"]
    systems = ["Payments system", "Loan system", "Collateral system"]
    x = 80
    for i, (s, sys_) in enumerate(zip(steps, systems)):
        card(d, (x, 240, x + 400, 420))
        text(d, (x + 30, 270), sys_, 24, fill=GREY, weight="Regular")
        wrapped(d, (x + 30, 310), s, 34, 340, fill=LIGHT)
        if i < 2:
            arrow(d, x + 410, 330, x + 500, colour=GREY, width=6)
            text(d, (x + 455, 365), "wait", 22, fill=GREY, weight="Regular", anchor="ma")
        x += 510

    text(d, (80, 485), "Redbelly pilot in the RBA's Project Acacia", 34, fill=RED)
    card(d, (80, 540, 1510, 770), fill=SLATE, outline=GREEN, width=5)
    x = 130
    for s in steps:
        tick(d, x + 30, 625, 30)
        text(d, (x + 75, 625), s, 32, anchor="lm")
        x += 420
    text(d, (140, 700), "All in one single step. Collateral free to use again straight away.",
         30, fill=GREEN, weight="Bold")
    footer(d, "Source: RBA and DFCRC, Project Acacia final report, May 2026")
    return im


def img_summary():
    im, d = canvas()
    text(d, (80, 70), "Redbelly in one line", 40, fill=RED, weight="Bold")
    wrapped(d, (80, 130),
            "A public network where real-world things can be split, owned and traded "
            "quickly, with ID checks and the rules built in.",
            50, 1400, fill=WHITE, weight="Bold", gap=1.25)

    tiles = [
        ("Digital slices", "of real assets like bonds, loans and property"),
        ("Rules checked", "at the moment of trade"),
        ("Reusable digital ID", "prove who you are without oversharing"),
        ("Final once confirmed", "no waiting for it to clear"),
    ]
    x = 80
    for i, (h, s) in enumerate(tiles):
        card(d, (x, 420, x + 340, 760))
        d.text((x + 34, 450), f"0{i + 1}", font=font(46, "Bold"), fill=RED)
        y = wrapped(d, (x + 34, 530), h, 34, 280, fill=WHITE, weight="Bold")
        wrapped(d, (x + 34, y + 12), s, 26, 280, fill=LIGHT, weight="Regular")
        x += 365
    footer(d, "Facts from public Redbelly, Tokeniser and RBA material")
    return im


IMAGES = {
    "01-money-fast-ownership-slow.png": img_money_vs_ownership,
    "02-pizza-slices.png": img_pizza,
    "03-bouncer-in-the-door.png": img_bouncer,
    "04-loan-three-steps-to-one.png": img_loan,
    "05-one-line-summary.png": img_summary,
}


def build(save=True):
    ALL_TEXT.clear()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in IMAGES.items():
        im = fn()
        if save:
            im.save(OUT / name, optimize=True)
            print("wrote", (OUT / name).relative_to(ROOT))


if __name__ == "__main__":
    build()
else:
    # Imported by check_entry.py: draw in memory only to collect the text.
    build(save=False)

#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Tuesday 24 November 2026.

Everything here is drawn with Pillow primitives: no photos, no fetched
assets. The page is a newspaper front page -- masthead, red date band,
one lead story with a radar illustration, six short stories in a grid,
and an also-today strip along the bottom.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SHEET = 1024
EDGE = 36                      # outer margin
INK = (24, 24, 22)             # near-black for body copy
PAPER = (250, 246, 236)        # warm newsprint
CARD = (255, 255, 255)
BAND = (178, 28, 28)           # the red date band
NAVY = (16, 34, 58)            # lead picture background
MUTED = (110, 104, 94)
RULE = (190, 182, 168)
ACCENT = (178, 28, 28)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


class Page:
    """One sheet plus the fonts and the little helpers every block uses."""

    def __init__(self):
        self.img = Image.new("RGB", (SHEET, SHEET), PAPER)
        self.pen = ImageDraw.Draw(self.img)
        self.serif = lambda s: load("DejaVuSerif-Bold.ttf", s)
        self.serif_plain = lambda s: load("DejaVuSerif.ttf", s)
        self.sans = lambda s: load("DejaVuSans-Bold.ttf", s)
        self.sans_plain = lambda s: load("DejaVuSans.ttf", s)

    def fit(self, text, font, width):
        """Greedy word wrap; returns a list of lines that fit `width`."""
        out, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.pen.textlength(trial, font=font) <= width:
                current = trial
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        return out

    def block(self, lines, font, x, y, colour, gap):
        """Draw wrapped lines top-down, returning the y below the last."""
        for line in lines:
            self.pen.text((x, y), line, font=font, fill=colour)
            y += font.size + gap
        return y

    def centred(self, text, font, y, colour):
        width = self.pen.textlength(text, font=font)
        self.pen.text(((SHEET - width) / 2, y), text, font=font, fill=colour)
        return y + font.size

    def save(self):
        here = os.path.dirname(os.path.abspath(__file__))
        self.img.save(os.path.join(here, "entry.png"))


def radar_picture(page, box):
    """Radar scope with a sweeping beam and an AWACS jet above it."""
    x0, y0, x1, y1 = box
    page.pen.rectangle(box, fill=NAVY)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 18
    radius = 128
    for step in range(4):
        r = radius - step * 30
        page.pen.ellipse(
            [cx - r, cy - r, cx + r, cy + r], outline=(64, 120, 92), width=2
        )
    page.pen.line([cx - radius, cy, cx + radius, cy], fill=(64, 120, 92), width=1)
    page.pen.line([cx, cy - radius, cx, cy + radius], fill=(64, 120, 92), width=1)
    # sweep wedge: a pale green triangle from the centre, pointing up-right
    page.pen.polygon(
        [(cx, cy), (cx + 92, cy - 88), (cx + 118, cy - 40)],
        fill=(96, 190, 120),
    )
    page.pen.ellipse(
        [cx - 5, cy - 5, cx + 5, cy + 5], fill=(190, 230, 170)
    )
    # blips on the scope
    for bx, by in [(cx - 70, cy + 40), (cx + 60, cy + 66), (cx + 30, cy - 70)]:
        page.pen.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(240, 220, 120))
    # jet silhouette: fuselage, swept wings, tail, radar dome on top
    jy = y0 + 52
    page.pen.polygon(
        [
            (cx - 150, jy + 6), (cx - 60, jy), (cx + 40, jy),
            (cx + 150, jy + 6), (cx + 40, jy + 12), (cx - 60, jy + 12),
        ],
        fill=(226, 232, 238),
    )
    page.pen.polygon(
        [(cx - 40, jy - 2), (cx + 10, jy - 26), (cx + 34, jy - 26), (cx + 26, jy - 2)],
        fill=(226, 232, 238),
    )
    page.pen.ellipse(
        [cx - 26, jy - 34, cx + 26, jy - 18], fill=(200, 210, 220)
    )
    page.pen.polygon(
        [(cx - 118, jy + 4), (cx - 96, jy - 18), (cx - 78, jy + 4)],
        fill=(200, 210, 220),
    )
    caption = page.sans_plain(17)
    page.pen.text((x0 + 14, y1 - 30), "An AWACS jet watches the eastern flank",
                  font=caption, fill=(210, 222, 232))


def lead_story(page):
    """Picture on the left, headline and deck on the right."""
    top, bottom = 170, 468
    radar_picture(page, (EDGE, top, 470, bottom))
    tx = 496
    width = SHEET - EDGE - tx
    page.pen.text((tx, top + 2), "LEAD STORY  —  EUROPE",
                  font=page.sans(19), fill=ACCENT)
    head = page.fit(
        "NATO sends AWACS to watch Poland's skies",
        page.serif(41), width,
    )
    y = page.block(head, page.serif(41), tx, top + 32, INK, 4)
    deck = page.fit(
        "Alliance answers the missiles that fell in Poland",
        page.serif_plain(24), width,
    )
    y = page.block(deck, page.serif_plain(24), tx, y + 12, (58, 54, 48), 2)
    body = page.fit(
        "Three Russian missiles fell in Poland on Friday. "
        "NATO answered on Monday, sending an early-warning jet.",
        page.sans_plain(18), width,
    )
    page.block(body, page.sans_plain(18), tx, y + 14, MUTED, 3)


def story_card(page, box, tag, headline, standfirst, bar):
    """One small story: coloured bar, tag, headline, one-line summary."""
    x0, y0, x1, y1 = box
    page.pen.rectangle(box, fill=CARD, outline=RULE, width=1)
    page.pen.rectangle([x0, y0, x1, y0 + 7], fill=bar)
    inner = x0 + 16
    width = x1 - inner - 14
    page.pen.text((inner, y0 + 20), tag, font=page.sans(16), fill=bar)
    head = page.fit(headline, page.serif(25), width)
    y = page.block(head, page.serif(25), inner, y0 + 46, INK, 2)
    page.block(
        page.fit(standfirst, page.sans_plain(17), width),
        page.sans_plain(17), inner, y + 8, MUTED, 2,
    )


def six_stories(page):
    """Two rows of three cards."""
    stories = [
        ("EUROPE", "Moscow warns Estonia of 'open war'",
         "Border shut from 1 December", (122, 30, 30)),
        ("ASIA", "Tajikistan quits the ICC",
         "Dushanbe leaves the Hague court", (24, 84, 122)),
        ("ASIA", "India pledges $1.6bn to Nepal",
         "Aid package for Kathmandu", (24, 84, 122)),
        ("ASIA", "Java factory fire: 24 dead",
         "Around 30 still missing", (150, 84, 20)),
        ("CLIMATE", "COP31 ends with no deal",
         "Talks close without agreement", (30, 110, 60)),
        ("SPORT", "Verstappen wins in Las Vegas",
         "Red Bull star takes the flag", (120, 60, 140)),
    ]
    gap = 16
    cell_w = (SHEET - 2 * EDGE - 2 * gap) // 3
    cell_h = 158
    y = 490
    for row in range(2):
        for col in range(3):
            item = stories[row * 3 + col]
            x0 = EDGE + col * (cell_w + gap)
            story_card(
                page,
                (x0, y, x0 + cell_w, y + cell_h),
                item[0], item[1], item[2], item[3],
            )
        y += cell_h + gap


def also_today(page):
    """Four short items in a row under an ALSO TODAY heading."""
    y0 = 852
    page.pen.rectangle([EDGE, y0, SHEET - EDGE, 962], fill=(238, 232, 220))
    page.pen.text((EDGE + 16, y0 + 12), "ALSO TODAY",
                  font=page.sans(18), fill=ACCENT)
    items = [
        "CAS to rule on Senegal's AFCON appeal",
        "Trump blames Democrats for the $1tn market slide",
        "Seoul names a new foreign minister",
        "Dhaka vows to arrest Hasina if she returns",
    ]
    gap = 14
    col_w = (SHEET - 2 * EDGE - 32 - 3 * gap) // 4
    for i, item in enumerate(items):
        x = EDGE + 16 + i * (col_w + gap)
        page.pen.text((x, y0 + 46), "•", font=page.sans_plain(18), fill=ACCENT)
        page.block(
            page.fit(item, page.sans_plain(17), col_w - 18),
            page.sans_plain(17), x + 16, y0 + 46, INK, 2,
        )


def build():
    page = Page()
    # Masthead
    page.centred("THE WORLD TODAY", page.serif(74), 26, INK)
    page.pen.line([EDGE, 116, SHEET - EDGE, 116], fill=INK, width=3)
    page.pen.line([EDGE, 121, SHEET - EDGE, 121], fill=INK, width=1)
    # Red date band
    page.pen.rectangle([EDGE, 130, SHEET - EDGE, 160], fill=BAND)
    page.centred("TUESDAY, 24 NOVEMBER 2026", page.sans(26), 133, (255, 255, 255))
    lead_story(page)
    six_stories(page)
    also_today(page)
    page.pen.text(
        (EDGE, 978),
        "THE WORLD TODAY  •  24 NOVEMBER 2026  •  One day's world news in one page",
        font=page.sans_plain(15), fill=MUTED,
    )
    page.save()


if __name__ == "__main__":
    build()

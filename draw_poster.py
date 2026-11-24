#!/usr/bin/env python3
"""Front page for Tuesday 24 November 2026.

Draws a 1024x1024 newspaper front page with Pillow, summarising the
day's world news from reporting published on 24 November 2026:
NATO's AWACS deployment to Poland, Moscow's 'open war' warning to
Estonia, Tajikistan leaving the ICC, India's Nepal package, the Java
factory fire, the COP31 collapse and Verstappen's Las Vegas win.

Run:  python3 draw_poster.py   -> writes entry.png beside this file.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 232)
INK = (22, 22, 22)
NAVY = (18, 30, 58)
RED = (164, 22, 44)
GOLD = (196, 154, 32)
GREY = (96, 92, 84)
RULE = (205, 197, 180)
WHITE = (255, 255, 255)
BODY = (58, 56, 50)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, face, width):
    """Greedy word wrap to lines that fit inside width pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=face) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def lines(d, x, y, text_lines, face, colour, leading):
    """Draw each line; return the y below the last one."""
    for line in text_lines:
        d.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def chip(d, x, y, label, colour):
    """Small filled kicker label; returns the width it occupied."""
    face = font(SANS_B, 15)
    w = d.textlength(label, font=face) + 20
    d.rounded_rectangle([x, y, x + w, y + 25], radius=4, fill=colour)
    d.text((x + 10, y + 4), label, font=face, fill=WHITE)
    return w


def radar(d, box):
    """Early-warning radar scope with an AWACS silhouette."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=NAVY)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 8
    ring = (90, 120, 170)
    for r in (128, 96, 64, 32):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring, width=2)
    d.line([cx - 132, cy, cx + 132, cy], fill=ring, width=2)
    d.line([cx, cy - 132, cx, cy + 132], fill=ring, width=2)
    # sweep: a few pale radial lines fanning down-right, clear of the
    # labels at top-left and of the plane silhouette
    for step in range(5):
        a = math.radians(20 + step * 12)
        px = cx + 128 * math.cos(a)
        py = cy + 128 * math.sin(a)
        d.line([cx, cy, px, py], fill=(110, 190, 110), width=2)
    for bx, by in [(cx - 78, cy - 52), (cx - 40, cy + 66), (cx + 88, cy - 30)]:
        d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(235, 90, 90))
    # AWACS: radar dome, fuselage, wings, tail
    d.ellipse([cx - 12, cy - 66, cx + 12, cy - 46], fill=GOLD)
    d.rectangle([cx - 6, cy - 46, cx + 6, cy + 12], fill=WHITE)
    d.polygon([(cx - 78, cy - 34), (cx + 78, cy - 34),
               (cx + 52, cy - 20), (cx - 52, cy - 20)], fill=WHITE)
    d.polygon([(cx - 6, cy + 12), (cx + 6, cy + 12),
               (cx + 22, cy + 24), (cx - 22, cy + 24)], fill=WHITE)
    d.text((x0 + 14, y0 + 10), "E-3 AWACS", font=font(SANS_B, 18), fill=GOLD)
    d.text((x0 + 14, y0 + 34), "EYES OVER POLAND", font=font(SANS_B, 14),
           fill=(200, 210, 230))
    d.rectangle([x0, y1 - 40, x1, y1], fill=(12, 20, 40))
    d.text((x0 + 14, y1 - 32), "NATO's early-warning fleet",
           font=font(SANS, 16), fill=WHITE)


def card(d, box, kicker, tint, headline, body):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=WHITE, outline=RULE, width=2)
    d.rectangle([x0, y0, x0 + 6, y1], fill=tint)
    d.text((x0 + 18, y0 + 12), kicker, font=font(SANS_B, 14), fill=tint)
    head = font(SERIF_B, 22)
    y = lines(d, x0 + 18, y0 + 38,
              wrap(d, headline, head, (x1 - x0) - 34)[:2], head, INK, 27)
    body_face = font(SANS, 15)
    lines(d, x0 + 18, y + 6,
          wrap(d, body, body_face, (x1 - x0) - 34)[:3], body_face, BODY, 19)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.text((W // 2, 6), "THE WORLD TODAY", font=font(SERIF_B, 58),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 68), "ONE DAY  \u2022  ONE PAGE  \u2022  EVERY STORY THAT MATTERED",
           font=font(SANS_B, 14), fill=GOLD, anchor="ma")

    # ---- date band ----
    d.rectangle([0, 92, W, 148], fill=RED)
    d.text((W // 2, 100), "TUESDAY, 24 NOVEMBER 2026",
           font=font(SERIF_B, 38), fill=WHITE, anchor="ma")
    d.line([0, 148, W, 148], fill=GOLD, width=4)

    # ---- lead story: radar art left, text right ----
    radar(d, (36, 168, 420, 452))
    lx = 448
    chip(d, lx, 172, "EUROPE  \u2022  NATO", RED)
    lead = font(SERIF_B, 42)
    y = lines(d, lx, 208,
              wrap(d, "NATO sends AWACS to watch Poland's skies", lead, 540),
              lead, INK, 48)
    sub = font(SERIF_I, 23)
    y = lines(d, lx, y + 8,
              wrap(d, "Alliance answers the missiles that fell in Poland",
                   sub, 540)[:1], sub, RED, 28)
    body = font(SANS, 18)
    lines(d, lx, y + 12,
          wrap(d, "Three Russian weapons came down in south-east Poland on "
                  "Friday. Warsaw invoked Article 4 and asked for more air "
                  "defences; NATO is sending early-warning aircraft.",
               body, 540)[:3], body, (38, 36, 32), 24)
    d.line([36, 466, 988, 466], fill=RULE, width=2)

    # ---- six stories, two rows of three ----
    stories = [
        ("BALTIC", (150, 30, 30),
         "Moscow warns Estonia of \u2018open war\u2019",
         "Russia summons Tallinn's envoy after Estonia says it will "
         "shut its border from 1 December."),
        ("JUSTICE", (60, 60, 160),
         "Tajikistan quits the ICC",
         "Dushanbe formally leaves the Rome Statute; the EU urges it "
         "to reconsider and reverse course."),
        ("ASIA", (200, 90, 0),
         "India pledges $1.6bn to Nepal",
         "Modi and Nepal's PM Shah agree a big aid package and flag "
         "off a new cross-border rail link."),
        ("INDONESIA", (0, 120, 120),
         "Java factory fire: 24 dead",
         "Rescuers keep searching for about 30 people still missing "
         "after the blaze in Banten."),
        ("CLIMATE", (30, 130, 30),
         "COP31 ends with no deal",
         "Antalya talks collapse over fossil fuels; countries leave "
         "without a consensus text."),
        ("SPORT", (160, 20, 40),
         "Verstappen wins in Las Vegas",
         "Red Bull's champion takes the Grand Prix; India and New "
         "Zealand draw the Wellington Test."),
    ]
    cw, ch, gap = 304, 168, 12
    for i, (kick, tint, head, body) in enumerate(stories):
        cx = 36 + (i % 3) * (cw + gap)
        cy = 480 + (i // 3) * (ch + gap)
        card(d, (cx, cy, cx + cw, cy + ch), kick, tint, head, body)

    # ---- also today ----
    ay = 840
    d.rectangle([0, ay, W, 948], fill=NAVY)
    d.text((36, ay + 10), "ALSO TODAY", font=font(SANS_B, 19), fill=GOLD)
    items = ("CAS to rule on Senegal's AFCON title appeal  \u2022  Trump "
             "blames Democrats for the $1tn market slide  \u2022  Seoul "
             "names a new foreign minister  \u2022  Dhaka vows to arrest "
             "Hasina if she returns")
    lines(d, 36, ay + 40,
          wrap(d, items, font(SANS, 18), 952), font(SANS, 18), WHITE, 25)

    # ---- footer ----
    d.text((W // 2, 958),
           "Drawn from the day\u2019s reporting  \u2022  Reuters  \u2022  AP  \u2022  AFP",
           font=font(SERIF_I, 17), fill=GREY, anchor="ma")
    d.text((W // 2, 982), "THE WORLD TODAY  \u2014  TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 14), fill=BODY, anchor="ma")
    d.line([W // 2 - 60, 1012, W // 2 + 60, 1012], fill=GOLD, width=3)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()

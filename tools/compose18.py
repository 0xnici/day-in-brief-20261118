#!/usr/bin/env python3
"""Front page composer, visual edition — Wednesday 18 November 2026.

The page is described as a list of blocks and painted top to bottom:
masthead, arrival illustration, lead, story grid, numbers band.
Run:  python3 tools/compose18.py   -> writes entry.png (1024x1024)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PAGE_W = 1024
EDGE = 28
PAPER = (246, 242, 233)
BLACK = (24, 22, 19)
RED = (150, 30, 22)
GREY = (92, 86, 74)
FAINT = (198, 190, 170)
BAND_BG = (26, 24, 38)
BAND_TX = (243, 237, 220)
FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(f"{FD}/{name}", size)


def lines(draw, text, fnt, limit):
    out, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= limit:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(draw, x, y, text, fnt, fill, limit, step):
    for ln in lines(draw, text, fnt, limit):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def middle(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((PAGE_W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 6


BLOCKS = [
    ("masthead", "THE DAY IN BRIEF"),
    ("dateline", "Wednesday 18 November 2026  ·  Summit week opens  ·  No. 18"),
    ("art", HERE.parent / "assets" / "hero.png"),
    ("caption", "The red carpet in Shenzhen: an honour guard, a dozen flags, and a skyline waiting for its guests."),
    ("lead", "SHENZHEN SETS THE TABLE"),
    ("leadbody", "Xi meets Putin in Shenzhen as summit week opens — the first of the "
                 "week's arrivals, with Washington watching the guest list grow by the hour."),
    ("stories", None),
    ("band", "56 SENATE SEATS  ·  DAY 2 AT KERCH  ·  $3,735 GOLD  ·  13 YEARS WAITING FOR GTA VI  ·  49 YEARS OF VOYAGER"),
]

LEFT = [
    ("US hits missile site on Qeshm", "American strikes flatten an Iranian missile site on Qeshm Island; Tehran answers with drones."),
    ("Kerch bridge hit again", "A second straight day of strikes halts traffic on the Crimea span; repairs stall."),
    ("Peltola takes Alaska", "Mary Peltola's win carries the Democrats to 56 Senate seats for the winter session."),
]
RIGHT = [
    ("Ebola cases more than double", "DR Congo's outbreak accelerates overnight; clinics plead for staff and vaccine."),
    ("Nvidia posts record revenue", "The chip giant beats every forecast as AI demand refuses to cool."),
    ("Thirteen years of waiting", "GTA VI's spring launch holds as fans mark thirteen years since the last game."),
]


def paint():
    img = Image.new("RGB", (PAGE_W, PAGE_W), PAPER)
    d = ImageDraw.Draw(img)
    y = 14
    for kind, payload in BLOCKS:
        if kind == "masthead":
            y = middle(d, y, payload, F("DejaVuSerif-Bold.ttf", 54), BLACK)
            d.line([EDGE, y + 2, PAGE_W - EDGE, y + 2], fill=BLACK, width=3)
            y += 8
        elif kind == "dateline":
            y = middle(d, y, payload, F("DejaVuSerif.ttf", 16), GREY)
            y += 4
        elif kind == "art":
            art = Image.open(payload).convert("RGB")
            tw, th = PAGE_W - 2 * EDGE, 428
            s = max(tw / art.width, th / art.height)
            art = art.resize((round(art.width * s), round(art.height * s)))
            ox = (art.width - tw) // 2
            oy = int((art.height - th) * 0.62)
            img.paste(art.crop((ox, oy, ox + tw, oy + th)), (EDGE, y))
            d.rectangle([EDGE, y, EDGE + tw, y + th], outline=BLACK, width=3)
            y += th + 8
        elif kind == "caption":
            y = middle(d, y, payload, F("DejaVuSansMono-Oblique.ttf", 16), GREY)
            y += 6
        elif kind == "lead":
            y = middle(d, y, payload, F("DejaVuSerif-Bold.ttf", 42), BLACK)
        elif kind == "leadbody":
            y = para(d, EDGE + 60, y, payload, F("DejaVuSerif.ttf", 19), BLACK,
                     PAGE_W - 2 * EDGE - 120, 25)
            y += 10
            d.line([EDGE, y, PAGE_W - EDGE, y], fill=BLACK, width=2)
            y += 14
        elif kind == "stories":
            col = (PAGE_W - 2 * EDGE - 36) // 2
            tops = []
            for x, group in ((EDGE, LEFT), (EDGE + col + 36, RIGHT)):
                cy = y
                for head, body in group:
                    cy = para(d, x, cy, head.upper(), F("DejaVuSans-Bold.ttf", 20), RED, col, 24)
                    cy = para(d, x, cy + 2, body, F("DejaVuSans.ttf", 18), BLACK, col, 23)
                    cy += 14
                tops.append(cy)
            mid_x = EDGE + col + 18
            d.line([mid_x, y, mid_x, max(tops) - 10], fill=FAINT, width=2)
            y = max(tops)
        elif kind == "band":
            d.rectangle([0, 952, PAGE_W, PAGE_W], fill=BAND_BG)
            middle(d, 966, "THE DAY IN NUMBERS", F("DejaVuSans-Bold.ttf", 17), (196, 170, 90))
            middle(d, 994, payload, F("DejaVuSans-Bold.ttf", 13), BAND_TX)
    out = HERE.parent / "entry.png"
    img.save(out, optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    paint()

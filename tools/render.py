#!/usr/bin/env python3
"""Typeset one day's world news as a one-page newspaper front page.

Usage: render.py <YYYY-MM-DD> <out.png>

The CONTENT table below holds the stories: wire reporting of the date,
rewritten as a headline plus a two-line brief per story, six stories per
day and a one-line "also today" strip for the rest. The layout is a
masthead with the weekday and date in large serif type, a 2x3 grid of
story panels (region kicker, headline, brief), then the strip and a
colophon. Everything is drawn with PIL on system fonts; there is no
network access and no randomness, so a day always renders to the same
PNG bytes.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (248, 244, 233)
INK = (26, 23, 18)
ACCENT = (122, 31, 31)
FAINT = (120, 110, 88)
RULE = (26, 23, 18)
DIV = (201, 192, 171)

W = H = 1024
MARGIN = 46

CONTENT = {
    "2026-11-18": {
        "weekday": "WEDNESDAY",
        "dateline": "18 NOVEMBER 2026",
        "stories": [
            ("GULF · WAR", "US strikes Iranian missile site on Qeshm Island",
             "American forces hit a missile site on Qeshm Island in the Strait of Hormuz. Iran answered with drone attacks on Bahrain and Kuwait."),
            ("UKRAINE · WAR", "Kerch Bridge hit for a second straight day",
             "Ukraine struck the Crimean Bridge again and part of the road span collapsed, as Kyiv kept up pressure on the artery to occupied Crimea."),
            ("DIPLOMACY", "Xi and Putin meet in Shenzhen",
             "China's Xi Jinping and Russia's Vladimir Putin met in Shenzhen ahead of a trilateral summit with President Trump on the sidelines of APEC."),
            ("US POLITICS", "Peltola wins Alaska — Democrats reach 56 Senate seats",
             "Democrat Mary Peltola won Alaska's Senate seat, defeating the Republican incumbent and taking her party to 56 seats in the chamber."),
            ("HEALTH · AFRICA", "Ebola cases more than double in DR Congo",
             "The outbreak passed 11,000 cases with 5,400 deaths, the UN said — the epidemic more than doubled as response teams struggled to reach the east."),
            ("MARKETS", "Nvidia revenue doubles to a record",
             "Nvidia's quarterly revenue doubled on AI chip demand. European shares fell: the CAC 40 lost 1.62% and Germany's DAX 2.08%."),
        ],
        "also": "Category 5 Cyclone Xavier hits the Northern Cook Islands · M6.0 quake in Papua New Guinea · Russian plane crash in Siberia kills 19 · Knesset elects Kahana speaker",
    },
    "2026-11-17": {
        "weekday": "TUESDAY",
        "dateline": "17 NOVEMBER 2026",
        "stories": [
            ("GULF · WAR", "US strikes Qeshm Island after Hormuz shipping attacks",
             "US forces struck targets on Iran's Qeshm Island. The tanker Tara Gas burned off Oman — 24 seafarers evacuated — and Houthi drones hit Saudi pipeline stations."),
            ("UKRAINE · WAR", "Ukrainian strike closes part of the Crimean Bridge",
             "A Ukrainian strike collapsed part of the Kerch Bridge roadway. Russia answered with strikes on bridges in Kyiv, escalating the infrastructure war."),
            ("UNITED STATES", "Outage cascade hits airports, banks and big tech",
             "An NSA classified communications system went down amid cascading outages at US airports and banks and across Microsoft and Apple services."),
            ("HEALTH", "US loses measles elimination status",
             "The Pan American Health Organization stripped the US of measles elimination status as the national case count climbed past 5,400, with 10 deaths."),
            ("ASIA · DIPLOMACY", "Trump at Quad summit in Manila; leaders in Shenzhen",
             "President Trump joined the Quad summit in Manila as leaders gathered in Shenzhen. Washington tightened its AI chip export rules."),
            ("GAZA", "West urges Israel to open Gaza crossings before winter",
             "Western nations pressed Israel to open Gaza's crossings as winter rains flooded shelters and deepened the humanitarian crisis."),
        ],
        "also": "Japan scrambles jets after Russian aircraft violate its airspace · US tightens AI chip export rules · Winter rains flood Gaza shelters",
    },
}


def wrap(draw, text, font, width):
    # Greedy word wrap: keep adding words to the current line while the
    # rendered line still fits the column, then break to a new line.
    lines = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit(draw, text, path, start, width, max_lines, minimum=15):
    # Largest size, starting from `start`, whose wrapped text fits in
    # `max_lines` lines; never below `minimum`, which is returned as-is.
    for size in range(start, minimum, -1):
        font = ImageFont.truetype(path, size)
        if len(wrap(draw, text, font, width)) <= max_lines:
            return font
    return ImageFont.truetype(path, minimum)


def centered(draw, text, font, y, fill):
    # Draw one line of text centred on the page width at height y.
    x = (W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_masthead(draw, edition):
    # Kicker, weekday and date stacked in large type, closed by the
    # double rule every newspaper front page carries. Returns the y the
    # story grid starts at.
    y = 34
    kicker_font = ImageFont.truetype(SANS_B, 23)
    centered(draw, "THE DAY IN BRIEF · THE WORLD ON ONE PAGE", kicker_font, y, ACCENT)
    y += 40
    weekday_font = ImageFont.truetype(SERIF_B, 44)
    centered(draw, edition["weekday"], weekday_font, y, INK)
    y += 54
    dateline_font = ImageFont.truetype(SERIF_B, 63)
    centered(draw, edition["dateline"], dateline_font, y, INK)
    y += 84
    draw.rectangle([MARGIN, y, W - MARGIN, y + 5], fill=RULE)
    draw.rectangle([MARGIN, y + 9, W - MARGIN, y + 11], fill=RULE)
    return y + 26


def draw_story_panel(draw, story, cx, cy, col_w, row_h, index):
    # One panel: accent kicker, a fitted serif headline, a fitted brief,
    # then the hairline dividers that separate it from its neighbours.
    kicker, headline, brief = story
    kicker_font = ImageFont.truetype(SANS_B, 19)
    draw.text((cx, cy), kicker, font=kicker_font, fill=ACCENT)

    headline_font = fit(draw, headline, SERIF_B, 29, col_w, 2)
    y = cy + 30
    for line in wrap(draw, headline, headline_font, col_w):
        draw.text((cx, y), line, font=headline_font, fill=INK)
        y += 34

    brief_font = fit(draw, brief, SERIF, 20, col_w, 4)
    y += 2
    for line in wrap(draw, brief, brief_font, col_w):
        draw.text((cx, y), line, font=brief_font, fill=(52, 48, 40))
        y += 25

    gap = 26
    if index % 2 == 0 and index < 5:
        divider_x = cx + col_w + gap // 2
        draw.line([divider_x, cy + 2, divider_x, cy + row_h - 18], fill=DIV, width=1)
    if index < 4:
        draw.line([cx, cy + row_h - 8, cx + col_w, cy + row_h - 8], fill=DIV, width=1)


def draw_story_grid(draw, edition, top):
    # Six panels in two columns and three rows over a fixed grid height.
    gap = 26
    inner = W - 2 * MARGIN
    col_w = (inner - gap) // 2
    grid_h = 636
    row_h = grid_h // 3
    for index, story in enumerate(edition["stories"]):
        cx = MARGIN + (index % 2) * (col_w + gap)
        cy = top + (index // 2) * row_h
        draw_story_panel(draw, story, cx, cy, col_w, row_h, index)
    return top + grid_h


def draw_closing_strip(draw, edition, grid_bottom):
    # The "also today" strip under a heavy rule, and the colophon that
    # closes the page: sources, and the promise nothing here is invented.
    inner = W - 2 * MARGIN
    y = grid_bottom + 10
    draw.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=RULE)
    y += 14
    strip_font = ImageFont.truetype(SANS_B, 19)
    draw.text((MARGIN, y), "ALSO TODAY", font=strip_font, fill=ACCENT)
    y += 28
    also_font = fit(draw, edition["also"], SANS, 19, inner, 3)
    for line in wrap(draw, edition["also"], also_font, inner):
        draw.text((MARGIN, y), line, font=also_font, fill=INK)
        y += 25
    y += 8
    draw.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=RULE)
    y += 10
    colophon = "Compiled from the day's wire reporting · One page, the whole day · No story here is invented; figures as reported that day"
    colophon_font = ImageFont.truetype(SANS, 16)
    centered(draw, colophon, colophon_font, y, FAINT)


def main():
    day, out_path = sys.argv[1], sys.argv[2]
    edition = CONTENT[day]
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    grid_top = draw_masthead(draw, edition)
    grid_bottom = draw_story_grid(draw, edition, grid_top)
    draw_closing_strip(draw, edition, grid_bottom)
    page.save(out_path, format="PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main()

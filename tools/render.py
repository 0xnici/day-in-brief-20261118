#!/usr/bin/env python3
"""Render a one-page newspaper front page summing up one day's world news.

Usage: render_news.py <YYYY-MM-DD> <out.png>
The day's stories are the CONTENT table below — wire reporting of that date,
rewritten as headlines + two-line briefs. Layout: masthead with the date in
large type, a 2x3 grid of story panels (region kicker, serif headline,
brief), and an "also today" strip. Everything is drawn with PIL on system
fonts; no network, fully deterministic.
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
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, start, width, max_lines, minimum=15):
    size = start
    while size > minimum:
        f = ImageFont.truetype(path, size)
        if len(wrap(draw, text, f, width)) <= max_lines:
            return f
        size -= 1
    return ImageFont.truetype(path, minimum)


def main():
    day, out = sys.argv[1], sys.argv[2]
    c = CONTENT[day]
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN

    # Masthead
    y = 34
    fk = ImageFont.truetype(SANS_B, 23)
    kicker = "THE DAY IN BRIEF · THE WORLD ON ONE PAGE"
    d.text(((W - d.textlength(kicker, font=fk)) / 2, y), kicker, font=fk, fill=ACCENT)
    y += 40
    fw = ImageFont.truetype(SERIF_B, 44)
    d.text(((W - d.textlength(c["weekday"], font=fw)) / 2, y), c["weekday"], font=fw, fill=INK)
    y += 54
    fd = ImageFont.truetype(SERIF_B, 63)
    d.text(((W - d.textlength(c["dateline"], font=fd)) / 2, y), c["dateline"], font=fd, fill=INK)
    y += 84
    d.rectangle([MARGIN, y, W - MARGIN, y + 5], fill=RULE)
    d.rectangle([MARGIN, y + 9, W - MARGIN, y + 11], fill=RULE)
    y += 26

    # Story grid: 2 columns x 3 rows
    gap = 26
    col_w = (inner - gap) // 2
    rows_top = y
    grid_h = 636
    row_h = grid_h // 3
    for i, (kick, head, body) in enumerate(c["stories"]):
        cx = MARGIN + (i % 2) * (col_w + gap)
        cy = rows_top + (i // 2) * row_h
        fkick = ImageFont.truetype(SANS_B, 19)
        d.text((cx, cy), kick, font=fkick, fill=ACCENT)
        fh = fit(d, head, SERIF_B, 29, col_w, 2)
        yy = cy + 30
        for line in wrap(d, head, fh, col_w):
            d.text((cx, yy), line, font=fh, fill=INK)
            yy += 34
        fb = fit(d, body, SERIF, 20, col_w, 4)
        yy += 2
        for line in wrap(d, body, fb, col_w):
            d.text((cx, yy), line, font=fb, fill=(52, 48, 40))
            yy += 25
        if i % 2 == 0 and i < 5:
            d.line([cx + col_w + gap // 2, cy + 2, cx + col_w + gap // 2, cy + row_h - 18], fill=DIV, width=1)
        if i < 4:
            d.line([cx, cy + row_h - 8, cx + col_w, cy + row_h - 8], fill=DIV, width=1)

    # Also-today strip + colophon
    y = rows_top + grid_h + 10
    d.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=RULE)
    y += 14
    fa = ImageFont.truetype(SANS_B, 19)
    d.text((MARGIN, y), "ALSO TODAY", font=fa, fill=ACCENT)
    y += 28
    fb2 = fit(d, c["also"], SANS, 19, inner, 3)
    for line in wrap(d, c["also"], fb2, inner):
        d.text((MARGIN, y), line, font=fb2, fill=INK)
        y += 25
    y += 8
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=RULE)
    y += 10
    fc = ImageFont.truetype(SANS, 16)
    col = "Compiled from the day's wire reporting · One page, the whole day · No story here is invented; figures as reported that day"
    d.text(((W - d.textlength(col, font=fc)) / 2, y), col, font=fc, fill=FAINT)

    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()

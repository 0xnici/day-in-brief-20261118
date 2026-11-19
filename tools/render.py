#!/usr/bin/env python3
"""The Day in Brief, Wednesday 18 November 2026 — dense edition.

Usage: python3 tools/render.py 2026-11-18 /path/to/entry.png

The page is typeset by the Page class below: a masthead, the lead story
with a dotted world map of the day's datelines beside it, a statistics
band, four columns of stories grouped by region, an in-brief strip and
a colophon. The STORIES table is the edition's entire editorial input —
every headline and brief was reported on Wednesday 18 November 2026 —
and the typesetter invents nothing.

Fixed fonts and geometry, no clock, no randomness, no network: the
edition renders byte-identically on every run.
"""

import sys

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
EDGE = 36
SPAN = PAGE_W - 2 * EDGE

PAPER = (250, 247, 240)
INK = (26, 24, 20)
TEXT = (52, 48, 40)
RED = (150, 30, 30)
RULE = (26, 24, 20)
HAIR = (203, 195, 180)
FAINT = (110, 102, 90)
DOT = (168, 158, 140)
BAND_BG = (26, 24, 20)
BAND_FG = (250, 247, 240)
BAND_DIM = (206, 198, 182)

FONTS = "/usr/share/fonts/truetype/dejavu"
SERIF = FONTS + "/DejaVuSerif.ttf"
SERIF_B = FONTS + "/DejaVuSerif-Bold.ttf"
SANS = FONTS + "/DejaVuSans.ttf"
SANS_B = FONTS + "/DejaVuSans-Bold.ttf"

DAY_NAME = "WEDNESDAY"
DAY_DATE = "18 NOVEMBER 2026"

LEAD_TAG = "SHENZHEN \u00b7 SUMMIT EVE \u00b7 THE LEAD"
LEAD_TITLE = "Xi greets Trump in Shenzhen; Putin at his side"
LEAD_BODY = (
    "Trump lands in Shenzhen on Wednesday and Xi Jinping meets him at "
    "the airport, with Putin already in the city and the three set to "
    "sit down together on Thursday. Putin opened with a handshake and "
    "an attack on Western sanctions; the agenda for the hour they will "
    "share runs from nuclear arms control to trade. It is the summit's "
    "eve, and the whole day bent toward it."
)

STATS = [
    ("56", "Senate seats for\nthe Democrats"),
    ("\u20ac45bn", "loan proposed\nfor Ukraine"),
    ("$3,735", "gold's fourteen-\nmonth low"),
    ("2nd", "day of closure for\nthe Kerch Bridge"),
    ("13", "years of waiting\nfor GTA VI"),
    ("49", "years Voyager 1\nhas been flying"),
]

STORIES = [
    ("THE GULF", [
        ("Iranian drones over Kuwait",
         "Iranian drones struck at Kuwait on Wednesday, the Gulf's "
         "second day of fire after the American strike on Qeshm."),
        ("Qeshm strike, day two",
         "Iran answers the US strike on its Qeshm Island missile site; "
         "Bahrain reports interceptions over the Gulf."),
        ("Kerch Bridge shut again",
         "The Crimean Bridge stays closed for a second day as damage "
         "assessment drags on and traffic backs up."),
    ]),
    ("EUROPE", [
        ("EU's \u20ac45bn loan for Ukraine",
         "Brussels tables a \u20ac45 billion loan for Kyiv's budget, to "
         "be repaid once Russia pays reparations."),
        ("Ukraine under fire again",
         "Russian missile and drone strikes continue across Ukraine as "
         "winter approaches and the grid strains."),
    ]),
    ("AMERICAS", [
        ("Peltola win makes 56",
         "Mary Peltola's victory takes the Democrats to 56 Senate "
         "seats, the party's largest haul in nearly seventy years."),
        ("Jeffries in line for Speaker",
         "House Democrats prepare to nominate Hakeem Jeffries, who "
         "would be the first African-American Speaker."),
        ("Fed minutes point to hikes",
         "Minutes of the October meeting, released Wednesday, show "
         "most officials expecting further rate rises."),
        ("Outage fallout, day two",
         "The cascade of US technology outages runs into a second "
         "day, with agencies and airlines still recovering."),
    ]),
    ("HEALTH", [
        ("US loses measles-free status",
         "After a year of continuous transmission, the United States "
         "is stripped of its measles elimination status."),
        ("Ebola cases double in Congo",
         "The outbreak in the Democratic Republic of Congo doubles "
         "again; responders race to ring-fence the zone."),
    ]),
    ("ASIA-PACIFIC", [
        ("Putin lands for summit eve",
         "Putin arrives in Shenzhen ready to lift relations with "
         "China, attacking sanctions as a failed policy."),
        ("Xi's open-trade call",
         "Xi uses the APEC stage to call for open trade and wider "
         "market access across the Pacific."),
        ("Cyclone Akvan strengthens",
         "The Bay of Bengal storm gathers strength on a path toward "
         "the Andhra Pradesh coast."),
        ("Bangladesh on edge",
         "Dhaka stays tense as Hasina's Awami League protests build "
         "and security forces deploy in the capital."),
    ]),
    ("MARKETS", [
        ("Gold slides, dollar climbs",
         "Gold touches $3,735 an ounce, a fourteen-month low, while "
         "the dollar stands at a nineteen-month high."),
        ("Oil slips on stock build",
         "Brent eases about 1% after a surprise build in US crude "
         "inventories; OPEC+ resolve is questioned."),
        ("Sensex rally ends",
         "Indian shares end a two-day rally as profit-booking meets "
         "caution ahead of the Fed minutes."),
    ]),
    ("SCIENCE & TECH", [
        ("Nvidia's record quarter",
         "Nvidia posts record results on insatiable AI demand; "
         "attention turns to Anthropic's IPO pricing."),
        ("Voyager nears a light-day",
         "Voyager 1 closes on one light-day from Earth; NASA's "
         "confirmation briefing is set for Thursday."),
        ("Microsoft\u2013ByteDance talks",
         "Microsoft is reported in talks to sell AI services to "
         "ByteDance, a deal that would need Washington's blessing."),
        ("Anthropic IPO awaited",
         "Wall Street waits on the pricing of Anthropic's market "
         "debut, the year's most watched listing."),
    ]),
    ("SPORT & CULTURE", [
        ("GTA VI: the final countdown",
         "Gamers count down the last hours to Grand Theft Auto VI's "
         "global launch, ending a thirteen-year wait."),
        ("Jollibee goes American",
         "Jollibee bets on fried chicken to crack the United States, "
         "announcing a push across American cities."),
    ]),
]

BRIEFS = [
    "Quad foreign ministers meet on the summit sidelines in Shenzhen",
    "Gaza crossings reopen in part as aid groups press for more",
    "Thailand and the Philippines sign new trade deals with Washington",
    "COP31 enters its final stretch in Antalya, language still contested",
    "A plane comes down in Siberia; a strong quake strikes off Papua New Guinea",
    "A cyclone brushes the Cook Islands; Israel's Knesset elects a new speaker",
]

# Dotted world map as row strings; '#' marks land.
MAP = [
    "                                                                ",
    "        #######                                                 ",
    "     ###########      ##     ##########  ##################     ",
    "   #############    ####   ############ ####################    ",
    "  ##############    ####  ###############################       ",
    "   ############      ##    #############################        ",
    "    ##########              ##########################          ",
    "     ########                ###  #################             ",
    "      ######                  ##    ##############              ",
    "       #####                        ############                ",
    "       ####                          ##########                 ",
    "       ###                            ########                  ",
    "      ####                             ######                   ",
    "      ###                               ####        ##          ",
    "     ####                               ###        ####         ",
    "     ###                                                ##      ",
    "                                                                ",
]
# (grid column, grid row, caption) for the red dateline markers.
PINS = [(49, 4, "SHENZHEN"), (38, 5, "QESHM"), (33, 3, "KERCH"), (10, 4, "WASHINGTON")]

# Which sections sit in which column, top to bottom.
LAYOUT = [
    ["THE GULF", "EUROPE"],
    ["AMERICAS", "HEALTH"],
    ["ASIA-PACIFIC", "MARKETS"],
    ["SCIENCE & TECH", "SPORT & CULTURE"],
]


def lines_for(draw, text, font, width):
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def shrink_to(draw, text, path, size, width, max_lines):
    while size > 9:
        font = ImageFont.truetype(path, size)
        if len(lines_for(draw, text, font, width)) <= max_lines:
            return font
        size -= 1
    return ImageFont.truetype(path, size)


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def centre(self, text, font, y, fill):
        x = (PAGE_W - self.d.textlength(text, font=font)) / 2
        self.d.text((x, y), text, font=font, fill=fill)

    def masthead(self):
        d = self.d
        y = 20
        self.centre("THE DAY IN BRIEF \u00b7 THE WORLD ON ONE PAGE", ImageFont.truetype(SANS_B, 19), y, RED)
        y += 28
        self.centre(f"{DAY_NAME} {DAY_DATE}", ImageFont.truetype(SERIF_B, 48), y, INK)
        y += 60
        d.rectangle([EDGE, y, PAGE_W - EDGE, y + 5], fill=RULE)
        d.rectangle([EDGE, y + 9, PAGE_W - EDGE, y + 11], fill=RULE)
        return y + 20

    def world_map(self, x, y, w):
        d = self.d
        cell = w / len(MAP[0])
        for r, row in enumerate(MAP):
            for c, ch in enumerate(row):
                if ch == "#":
                    cx, cy = x + c * cell + cell / 2, y + r * cell + cell / 2
                    d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=DOT)
        tag = ImageFont.truetype(SANS_B, 10)
        for c, r, label in PINS:
            cx, cy = x + c * cell + cell / 2, y + r * cell + cell / 2
            d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
            d.text((cx + 7, cy - 6), label, font=tag, fill=RED)
        return y + int(len(MAP) * cell)

    def lead(self, top):
        d = self.d
        text_w = 600
        d.text((EDGE, top), LEAD_TAG, font=ImageFont.truetype(SANS_B, 16), fill=RED)
        title_font = shrink_to(d, LEAD_TITLE, SERIF_B, 38, text_w, 2)
        y = top + 24
        for line in lines_for(d, LEAD_TITLE, title_font, text_w):
            d.text((EDGE, y), line, font=title_font, fill=INK)
            y += 42
        body_font = ImageFont.truetype(SERIF, 15)
        y += 2
        for line in lines_for(d, LEAD_BODY, body_font, text_w):
            d.text((EDGE, y), line, font=body_font, fill=TEXT)
            y += 21
        map_x = EDGE + text_w + 28
        map_end = self.world_map(map_x, top + 4, SPAN - text_w - 28)
        d.text((map_x, map_end + 4), "WHERE THE DAY HAPPENED", font=ImageFont.truetype(SANS, 11), fill=FAINT)
        bottom = max(y, map_end + 22)
        d.line([EDGE, bottom + 6, PAGE_W - EDGE, bottom + 6], fill=HAIR, width=1)
        return bottom + 14

    def stats_band(self, top):
        d = self.d
        d.rectangle([EDGE, top, PAGE_W - EDGE, top + 68], fill=BAND_BG)
        d.text((EDGE + 12, top + 5), "THE DAY IN NUMBERS", font=ImageFont.truetype(SANS_B, 11), fill=BAND_DIM)
        col_w = SPAN / len(STATS)
        big = ImageFont.truetype(SERIF_B, 21)
        small = ImageFont.truetype(SANS, 9)
        for i, (figure, caption) in enumerate(STATS):
            x = EDGE + 12 + i * col_w
            d.text((x, top + 19), figure, font=big, fill=BAND_FG)
            for j, line in enumerate(caption.split("\n")):
                d.text((x, top + 45 + j * 11), line, font=small, fill=BAND_DIM)
        return top + 76

    def story(self, headline, brief, x, y, w):
        d = self.d
        head = shrink_to(d, headline, SANS_B, 14, w, 2)
        for line in lines_for(d, headline, head, w):
            d.text((x, y), line, font=head, fill=INK)
            y += 15
        body = shrink_to(d, brief, SERIF, 11, w, 3)
        y += 1
        for line in lines_for(d, brief, body, w):
            d.text((x, y), line, font=body, fill=TEXT)
            y += 12
        return y + 5

    def section(self, name, items, x, y, w):
        d = self.d
        d.text((x, y), name, font=ImageFont.truetype(SANS_B, 13), fill=RED)
        y += 17
        d.line([x, y, x + w, y], fill=HAIR, width=1)
        y += 5
        for headline, brief in items:
            y = self.story(headline, brief, x, y, w)
        return y

    def columns(self, top):
        d = self.d
        by_name = dict(STORIES)
        gap = 22
        col_w = (SPAN - 3 * gap) // 4
        bottom = top
        for i, names in enumerate(LAYOUT):
            x = EDGE + i * (col_w + gap)
            y = top
            for name in names:
                y = self.section(name, by_name[name], x, y, col_w)
                y += 6
            bottom = max(bottom, y)
            if i < 3:
                vx = x + col_w + gap // 2
                d.line([vx, top, vx, bottom], fill=HAIR, width=1)
        return bottom

    def brief_strip(self, top):
        d = self.d
        d.text((EDGE, top), "IN BRIEF", font=ImageFont.truetype(SANS_B, 13), fill=RED)
        font = ImageFont.truetype(SANS, 12)
        y, x = top + 20, EDGE
        for item in BRIEFS:
            text = item + "   \u00b7   "
            width = d.textlength(text, font=font)
            if x + width > PAGE_W - EDGE:
                y += 17
                x = EDGE
            d.text((x, y), text, font=font, fill=TEXT)
            x += width
        return y + 17

    def colophon(self):
        d = self.d
        top = PAGE_H - 34
        d.rectangle([EDGE, top, PAGE_W - EDGE, top + 2], fill=RULE)
        line = "Compiled from the day's wire reporting \u00b7 One page, the whole day \u00b7 No story here is invented; figures as reported that day"
        font = ImageFont.truetype(SANS, 12)
        x = (PAGE_W - d.textlength(line, font=font)) / 2
        d.text((x, top + 8), line, font=font, fill=FAINT)

    def render(self, out_path):
        y = self.masthead()
        y = self.lead(y)
        y = self.stats_band(y)
        y = self.columns(y + 2)
        self.brief_strip(y + 4)
        self.colophon()
        self.img.save(out_path, format="PNG", optimize=True)
        print("wrote", out_path)


def main():
    day, out_path = sys.argv[1], sys.argv[2]
    if day != "2026-11-18":
        print("error: this typesetter carries only the 2026-11-18 edition", file=sys.stderr)
        return 1
    Page().render(out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

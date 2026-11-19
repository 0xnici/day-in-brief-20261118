# day-in-brief-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/0xnici/day-in-brief-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/0xnici/day-in-brief-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One page, one day: Wednesday 18 November 2026 as a dense broadsheet front page. A lead story (Xi greets Trump in Shenzhen on the summit's eve, Putin at his side) beside a dotted world map of the day's datelines, a day-in-numbers band (56 Senate seats, a €45bn loan, gold at $3,735), and twenty-four stories in four columns — Iranian drones over Kuwait and the Qeshm strike's second day, the Kerch Bridge shut again, Peltola's win, the Fed minutes, Ebola doubling in Congo, Cyclone Akvan, Nvidia's record quarter, Voyager nearing a light-day — plus an in-brief strip carrying the Quad meeting, Gaza crossings, the Cook Islands cyclone, the Papua New Guinea quake, the Siberian plane crash and the new Knesset speaker. All of it is that day's wire reporting. `tools/render.py` did the typesetting; `main.py` writes the finished page, byte for byte, to the output directory and verifies the copy against the original before it reports success.

## Visual edition (v3)

The standing entry is a visual-first front page: a large arrival
illustration (`assets/hero.png`) under the masthead, one bold lead
headline, six short stories and the numbers band, composed by
`tools/compose18.py`:

```sh
python3 tools/compose18.py   # writes entry.png
```

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=1n20pv53&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>

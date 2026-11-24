# makefun-news-image-24b

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/theo1603/makefun-news-image-24b/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/theo1603/makefun-news-image-24b/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up the world's news of Tuesday 24 November 2026, drawn as
a newspaper front page: the lead story is NATO sending AWACS early-warning
aircraft to Poland after Russian missiles came down on Polish soil, with a
radar-scope illustration; six story cards cover Moscow warning Estonia of
"open war" over its border closure, Tajikistan quitting the ICC, India's
$1.6bn package for Nepal, the Java factory fire (24 dead, about 30 missing),
the COP31 talks collapsing with no fossil-fuel deal, and Verstappen winning
the Las Vegas Grand Prix — plus the CAS ruling on Senegal's AFCON appeal,
Trump blaming Democrats for the $1tn market slide, Seoul naming a new foreign
minister, and Dhaka vowing to arrest Hasina if she returns in the also-today
strip. Every headline is set from the day's reporting; the image is drawn
programmatically, so no text can garble.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `entry.png` (1024x1024, under 1 MiB) to
`$MAKEFUN_OUTPUT_DIR/entry.png`. Deterministic, no network, standard library
only.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>

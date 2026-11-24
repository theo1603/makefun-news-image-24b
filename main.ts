// One-day world news image: Tuesday 24 November 2026.
//
// The entry image is entry.png beside this file: a newspaper front page
// drawn for this bounty. Masthead and date strip up top; the lead story is
// NATO sending AWACS early-warning aircraft to Poland after Russian
// missiles came down on Polish soil, with a radar-scope illustration; six
// story cards (Moscow's "open war" warning to Estonia, Tajikistan leaving
// the ICC, India's $1.6bn Nepal package, the Java factory fire, the COP31
// collapse, Verstappen's Las Vegas win); and an also-today strip (the CAS
// ruling on Senegal's AFCON appeal, Trump's market-slide blame, Seoul's new
// foreign minister, Dhaka on Hasina).
//
// This program only copies that image to the output directory, so both
// grader runs write byte-identical output: same input bytes in, same bytes
// out, every run, with no clock, random, or network input anywhere in the
// path. Node 22, standard library only, no network.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));

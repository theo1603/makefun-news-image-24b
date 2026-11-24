// Entry point for the news-image-20261124 entry.
//
// The poster is drawn ahead of time by draw_poster.py and shipped in this
// repository as entry.png. All this program does is hand that exact file
// to the grader: it reads the bytes in and writes them out unchanged, so
// every run produces identical output.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The image lives beside this file in the repository checkout.
const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");

// The grader sets MAKEFUN_OUTPUT_DIR; fall back to a local "out" folder
// so the same command works when run by hand.
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const targetPath = join(targetDir, "entry.png");

// Read the whole poster into memory, then write it out verbatim.
const posterBytes = readFileSync(sourcePath);
mkdirSync(targetDir, { recursive: true });
writeFileSync(targetPath, posterBytes);

#!/usr/bin/env python3
# Write sections/02-LOAD-FILE.md from the load file, so the page always shows the CSV as it stands.
import csv, sys
src, out = sys.argv[1], sys.argv[2]
rows = list(csv.reader(open(src, encoding="utf-8-sig")))
hdr, body = rows[0], rows[1:]
cell = lambda v: v.replace("|", "\\|")
lines = [
    "# Load file",
    "",
    f"`{src}` as it stands: {len(body)} rows, {len(hdr)} columns. Blank cells are still open. Scroll sideways to see every column.",
    "",
    "External ID and Item Name both use the item ID. Item Name is the code; Display Name/Code is the name sales and customers read.",
    "",
    "::: {.wide}",
    "| " + " | ".join(f"**{cell(h)}**" for h in hdr) + " |",
    "|" + "---|" * len(hdr),
]
for r in body:
    r = r + [""] * (len(hdr) - len(r))
    lines.append("| " + " | ".join([f"**{cell(r[0])}**"] + [cell(v) for v in r[1:]]) + " |")
lines += [":::", ""]
open(out, "w").write("\n".join(lines))

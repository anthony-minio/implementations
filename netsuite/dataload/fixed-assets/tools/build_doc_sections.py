#!/usr/bin/env python3
# Write the asset tables of the fully depreciated assets document (sections/02-04) from data/assets.json.
#   python3 tools/build.py && python3 tools/build_doc_sections.py && bash tools/build.sh   (run from the fixed-assets folder)
import json, re

assets = [a for a in json.load(open("data/assets.json"))["assets"] if a["status"] == "Fully Depreciated"]
SECTIONS = [("02-COMPUTER-HARDWARE.md", "Computer hardware", ["Computer Hardware"]),
            ("03-FURNITURE.md", "Furniture and trade booths", ["Furniture"]),
            ("04-LEASEHOLD-AND-SOFTWARE.md", "Leasehold improvements and software", ["Lease Improvement", "Software"])]

def esc(s):
    s = re.sub(r"([\\|*_\[\]<>$`#])", r"\\\1", s)
    return s.replace("—", "-").replace("–", "-")
def describe(a):
    d, c = a["description"], a["comment"]
    return esc(d) + (f" ({esc(c)})" if c and c != d and c.lower() not in d.lower() else "")

done = 0
for fname, title, cats in SECTIONS:
    rows = sorted([a for a in assets if a["category"] in cats], key=lambda a: a["purchase"] or "")
    done += len(rows)
    out = [f"# {title}", "",
           f"{len(rows)} assets, cost {sum(a['cost'] for a in rows):,.2f}.", "",
           "| **Ref** | **Purchased** | **Vendor** | **Description** | **Cost** | **Still in use?** | **Where / who has it** |",
           "|----------|---------------|----------------|---------------------------|-----------:|---------|-----------|"]  # dash counts set the column widths
    for a in rows:
        out.append(f"| **{a['ref']}** | {a['purchase'] or ''} | {esc(a['vendor'])} | {describe(a)} | {a['cost']:,.2f} | | |")
    open(f"sections/{fname}", "w").write("\n".join(out) + "\n")
assert done == len(assets), (done, len(assets))
print(f"{done} assets in {len(SECTIONS)} sections")

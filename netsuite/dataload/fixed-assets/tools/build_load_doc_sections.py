#!/usr/bin/env python3
# Write the asset tables of the SOA loads document (soa-loads/sections/02 and 03) from data/assets.json.
#   python3 tools/build.py && python3 tools/build_load_doc_sections.py && bash soa-loads/tools/build.sh
# Rows are the assets in the draft loads: still depreciating. Fully depreciated assets are added after the review.
import json, re

assets = [a for a in json.load(open("data/assets.json"))["assets"] if a["status"] == "Depreciating"]
TYPE = {"Computer Hardware": "Equipment", "Lease Improvement": "Leasehold Improvements"}
assert {a["category"] for a in assets} <= set(TYPE), {a["category"] for a in assets}

def esc(s):
    return re.sub(r"([\\|*_\[\]<>$`#])", r"\\\1", s).replace("—", "-").replace("–", "-")
def money(v):
    return f"{v:,.2f}"
def sep(*widths, right=()):
    return "|" + "|".join("-" * w + (":" if i in right else "") for i, w in enumerate(widths)) + "|"

MIDLIFE_INTRO = """# Mid-life Asset Record

Template `MINIO_FAM_CSVTemplate_Mid-life Asset Record.xlsx`, tab **FAM_Mid-life Asset**. One row per asset.

| **Template column** | **Value** |
|----------------------|-------------------------------------------------------------|
| **Name** | Register Description |
| **Asset Description** | Register Vendor, then the register Comment when it differs from the Description |
| **Quantity** | 1 |
| **Subsidiary** | MinIO, Inc. |
| **Asset Type** | Computer Hardware to Equipment, Lease Improvement to Leasehold Improvements |
| **Asset Status** | Depreciating |
| **Asset Lifetime** | Register useful life in months. FA-076 and FA-082: months done plus months left (question 5) |
| **Asset Original Cost, Asset Current Cost** | Register cost. No write-downs |
| **Residual Value Percentage, Residual Value** | 0 |
| **Depreciation Start Date** | Register Dep Date when it falls in the first month depreciated, else the 1st of that month |
| **Last Depreciation Date** | 2026-10-31 |
| **Last Depreciation Period** | Months depreciated, first month to 2026-10 |
| **Last Depreciation Amount** | 2026-10 depreciation |
| **Current Net Book Value** | Register NBV at 2026-10-31 |

Ref is the row on the register's ALL FA tab (FA-069 is row 69). It is not in the load.
"""

DHR_INTRO = """# Depreciation history (DHR)

Template `MINIO_ FAM_DHR.xlsx`, tab **DHR Import Template**, filled as SOA's **FAM_DHR_lumpsum** example: one Depreciation row per asset for the depreciation taken to 2026-10-31.

| **Template column** | **Value** |
|----------------------|-------------------------------------------------------------|
| **DHR Name** | Blank, as in the example (question 4) |
| **Asset Name** | Name from the mid-life load |
| **Subsidiary, Quantity, Asset Type, Asset Lifetime** | As in the mid-life load |
| **Transaction Type** | Depreciation |
| **Transaction Date** | 2026-10-31 |
| **Transaction Amount** | Accumulated depreciation at 2026-10-31 |
| **Net Book Value (NBV)** | Original Cost less Transaction Amount |
| **Depreciation Period, Period-1** | 1 and 0, as in the example (question 3) |
| **Purchase Date** | Register Purchase Date |
| **Original Cost** | Register cost |
"""

ml = [MIDLIFE_INTRO]
for cat, typ in TYPE.items():
    rows = [a for a in assets if a["category"] == cat]
    ml += [f"## {typ}", "",
           f"{len(rows)} assets.", "",
           "| **Ref** | **Name** | **Lifetime** | **Original Cost** | **Start Date** | **Last Period** | **Last Amount** | **Current NBV** |",
           sep(9, 30, 9, 13, 12, 8, 11, 12, right=(2, 3, 5, 6, 7))]
    for a in rows:
        ml.append(f"| **{a['ref']}** | {esc(a['description'])} | {a['lifetime']} | {money(a['cost'])} | {a['start']} | "
                  f"{a['periods']} | {money(a['dep_last'])} | {money(a['nbv'])} |")
    ml.append(f"| **Total** | | | **{money(sum(a['cost'] for a in rows))}** | | | | **{money(sum(a['nbv'] for a in rows))}** |")
    ml.append("")
open("soa-loads/sections/02-MID-LIFE-ASSET-RECORD.md", "w").write("\n".join(ml))

dh = [DHR_INTRO, f"{len(assets)} assets.", "",
      "| **Ref** | **Asset Name** | **Purchase Date** | **Original Cost** | **Transaction Amount** | **NBV** |",
      sep(9, 36, 13, 14, 15, 13, right=(3, 4, 5))]
for a in assets:
    dh.append(f"| **{a['ref']}** | {esc(a['description'])} | {a['purchase']} | {money(a['cost'])} | {money(a['accum'])} | {money(a['nbv'])} |")
dh.append(f"| **Total** | | | **{money(sum(a['cost'] for a in assets))}** | **{money(sum(a['accum'] for a in assets))}** | **{money(sum(a['nbv'] for a in assets))}** |")
open("soa-loads/sections/03-DHR.md", "w").write("\n".join(dh) + "\n")
print(f"{len(assets)} assets; cost {sum(a['cost'] for a in assets):,.2f}, accumulated {sum(a['accum'] for a in assets):,.2f}, NBV {sum(a['nbv'] for a in assets):,.2f}")

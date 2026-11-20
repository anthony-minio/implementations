#!/usr/bin/env python3
# Write sections 02 to 04 of the SOA loads document: asset types from the draft mid-life workbook, assets from data/assets.json.
#   python3 tools/build.py && python3 tools/build_load_doc_sections.py && bash soa-loads/tools/build.sh
# Rows are the assets in the draft loads: still depreciating. Fully depreciated assets are added after the review.
import json, re
import openpyxl

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
| **Asset Description** | Register Vendor, then the register Comment when it differs from the Description. Blank for FA-098 to FA-100, which have neither |
| **Quantity** | 1 |
| **Subsidiary** | MinIO, Inc. |
| **Asset Type** | Computer Hardware to Equipment, Lease Improvement to Leasehold Improvements |
| **Asset Status** | Depreciating |
| **Asset Lifetime** | Register useful life in months. FA-076 and FA-082, shortened to the lease term: months done plus months left |
| **Asset Original Cost, Asset Current Cost** | Register cost. No write-downs |
| **Residual Value Percentage, Residual Value** | 0 |
| **Depreciation Start Date** | Register Dep Date when it falls in the first month depreciated, else the 1st of that month |
| **Last Depreciation Date** | 2026-10-31 |
| **Last Depreciation Period** | Months depreciated, first month to 2026-10 |
| **Last Depreciation Amount** | 2026-10 depreciation |
| **Current Net Book Value** | Register NBV at 2026-10-31 |
| **Cumulative Depreciation** | Added. Register accumulated depreciation at 2026-10-31 |
| **Accounting Method** | Added. Straight Line, (CC-RV)/AL. FA-076 and FA-082: Straight Line Remaining, (NB-RV)/(AL-CP+1), which spreads the remaining value over the months to the end of the lease. Names as on SOA's Dep Method tab |
| **Department** | Added. Register department mapped through Departments Draft v1 to the NetSuite department, parent : child. FA-070, FA-071 and FA-089 are on D110 (Sales, historic), which is not on the tab: 2100 Sales - Leadership |

Ref is the row on the register's ALL FA tab (FA-069 is row 69). It is not in the load.
"""

DHR_INTRO = """# Depreciation history (DHR)

Template `MINIO_ FAM_DHR.xlsx`, tab **DHR Import Template**, filled as SOA's **FAM_DHR_lumpsum** example: one Depreciation row per asset for the depreciation taken to 2026-10-31.

| **Template column** | **Value** |
|----------------------|-------------------------------------------------------------|
| **DHR Name** | Ref and date, such as FA-069 Depreciation to 2026-10-31 |
| **Asset Name** | Name from the mid-life load. NetSuite's format is the asset ID plus the name (FAM00001 Chairs), so the ID is added once the assets are imported |
| **Subsidiary, Quantity, Asset Type, Asset Lifetime** | As in the mid-life load |
| **Transaction Type** | Depreciation |
| **Transaction Date** | 2026-10-31 |
| **Transaction Amount** | Accumulated depreciation at 2026-10-31 |
| **Net Book Value (NBV)** | Original Cost less Transaction Amount |
| **Depreciation Period, Period-1** | The asset's Last Depreciation Period, and that less 1 |
| **Purchase Date** | Register Purchase Date |
| **Original Cost** | Register cost |
"""

# Asset types: SOA's FAM_Asset Type tab as filled in the draft, laid out as the load: the header and one row per type.
# Row 2 of the tab is SOA's guidance (Months, True/ False, ...), not an asset type, so it is left out.
at = openpyxl.load_workbook("data/MINIO_FAM_CSVTemplate_Mid-life Asset Record - DRAFT 20261117.xlsx")["FAM_Asset Type"]
hdr = [" ".join(str(c.value).split()) for c in at[1]]
types = [r for r in at.iter_rows(min_row=3, values_only=True) if r[0]]
assert len(types) == 5, types
cell = lambda v: "" if v in (None, "") else str(v).upper() if isinstance(v, bool) else esc(str(v))
AT = ["# Asset types", "",
      "Tab **FAM_Asset Type** of the mid-life template, filled as it will load. Changed from SOA's version: Write Off, Write Down and Disposal Cost Account set to 72400 (Ming Fu, 2026-11-13); Depreciation Rules from Disposal to Acquisition, MinIO's practice of depreciating from the month an asset goes into service; Accounting Method from Straightline to Straight Line, the name on SOA's Dep Method tab.", "",
      "| " + " | ".join(f"**{esc(h)}**" for h in hdr) + " |",
      sep(14, 8, 6, 6, 9, 7, 9, 9, 8, 13, 15, 11, 12, 7, 12, right=(2, 3))]
for t in types:
    AT.append("| **" + cell(t[0]) + "** | " + " | ".join(cell(v) for v in t[1:]) + " |")
AT.append("")
open("soa-loads/sections/02-ASSET-TYPES.md", "w").write("\n".join(AT))

# Load tables: every column of SOA's import tab, read from the filled draft workbooks, in file order.
# Ref (the register row) is added in front; it is not in the load.
import datetime as dt
def fmt(v, h):
    if v is None or v == "": return ""
    if isinstance(v, dt.datetime): return v.date().isoformat()
    if isinstance(v, float) or (isinstance(v, int) and ("Cost" in h or "Amount" in h or "Value" in h or "NBV" in h or "Cumulative" in h)):
        return money(v) if "Percentage" not in h else str(v)
    return esc(str(v))
def load_table(path, tab, name_col, cost_col, widths, totals):
    t = list(openpyxl.load_workbook(path)[tab].iter_rows(values_only=True))
    hdr = [" ".join(str(h).split()) for h in t[0]]
    rows = [r for r in t[1:] if any(v is not None for v in r)]
    assert len(rows) == len(assets), (path, len(rows), len(assets))
    for r, a in zip(rows, assets):  # same order as the build writes them
        assert r[hdr.index(name_col)] == a["description"] and abs(r[hdr.index(cost_col)] - a["cost"]) < 0.005, (a["ref"], r)
    right = [k + 1 for k, h in enumerate(hdr) if any(x in h for x in ("Cost", "Amount", "Value", "NBV", "Lifetime", "Period", "Quantity", "Percentage", "Cumulative"))]
    out = ["| **Ref** | " + " | ".join(f"**{esc(h)}**" for h in hdr) + " |", sep(*widths, right=right)]
    for r, a in zip(rows, assets):
        out.append(f"| **{a['ref']}** | " + " | ".join(fmt(v, h) for v, h in zip(r, hdr)) + " |")
    out.append("| **Total** | " + " | ".join(f"**{money(sum(r[k] or 0 for r in rows))}**" if h in totals else "" for k, h in enumerate(hdr)) + " |")
    return out

ml = [MIDLIFE_INTRO, f"{len(assets)} assets, in the order of the load file.", ""]
ml += load_table("data/MINIO_FAM_CSVTemplate_Mid-life Asset Record - DRAFT 20261117.xlsx", "FAM_Mid-life Asset ", "Name", "Asset Original Cost",
                 (6, 18, 14, 4, 7, 9, 9, 5, 9, 9, 4, 4, 8, 8, 5, 8, 9, 9, 10, 14),
                 ("Asset Original Cost", "Asset Current Cost", "Current Net Book Value", "Cumulative Depreciation"))
open("soa-loads/sections/03-MID-LIFE-ASSET-RECORD.md", "w").write("\n".join(ml) + "\n")

dh = [DHR_INTRO, f"{len(assets)} assets, in the order of the load file.", ""]
dh += load_table("data/MINIO_ FAM_DHR - DRAFT 20261117.xlsx", "DHR Import Template", "Asset Name", "Original Cost",
                 (6, 5, 22, 7, 4, 9, 9, 8, 9, 9, 5, 4, 5, 8, 9),
                 ("Transaction Amount", "Net Book Value (NBV)", "Original Cost"))
open("soa-loads/sections/04-DHR.md", "w").write("\n".join(dh) + "\n")
print(f"{len(assets)} assets; cost {sum(a['cost'] for a in assets):,.2f}, accumulated {sum(a['accum'] for a in assets):,.2f}, NBV {sum(a['nbv'] for a in assets):,.2f}")

#!/usr/bin/env python3
# Build the vendor review workbook for the controller and AP: the full (unmasked) review table and the notes.
#   python3 tools/build_delivery.py   (run from the vendors folder after build_review.py --full). Never commit the output.
import json, os, subprocess
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = "data/MinIO_Vendor_Load_FULL_20261026.xlsx"
s = open("data/vendor-review-full.html", encoding="utf-8").read()
data = json.loads(s[s.index("const DATA = ") + 13:s.index(";\nconst $")])
cols, review, required = data["cols"], data["review"], set(data["required"])

# Same colors as the review page (light theme).
FILL = {"ramp": "E3EDF9", "rule": "DCEFEF", "prop": "FFF2CF", "miss": "FCE5E2"}
INK = {"ramp": "2B64A8", "rule": "0D6B70", "prop": "8A5D00", "miss": "A8261F"}
GROUPS = [("Identity", 9), ("Contact and delivery", 8), ("Address 1", 12), ("Address 2", 12), ("Financial", 18),
          ("Source", 2), ("Added columns", 5), ("Bank details", 5), ("Review (not loaded)", len(review) + 1)]
thin = Side(style="thin", color="D6DEE3")
grid = Border(left=thin, right=thin, top=thin, bottom=thin)
head_fill = PatternFill("solid", fgColor="E8EEF1")

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Vendors"
col = 1
for name, span in GROUPS:
    ws.cell(row=1, column=col, value=name.upper())
    ws.merge_cells(start_row=1, start_column=col, end_row=1, end_column=col + span - 1)
    for k in range(col, col + span):
        c = ws.cell(row=1, column=k); c.fill = head_fill; c.border = grid
        c.font = Font(bold=True, size=9, color="5B6874")
    col += span
headers = cols + review + ["Flags"]
for k, h in enumerate(headers, 1):
    c = ws.cell(row=2, column=k, value=h + (" *" if h in required else ""))
    c.font = Font(bold=True); c.fill = head_fill; c.border = grid
    c.alignment = Alignment(vertical="top", wrap_text=True)
for i, r in enumerate(data["rows"], 3):
    vals = [(v, src) for v, src in r["cells"]] + [(v, "") for v in r["review"]] + [("; ".join(r["flags"]), "")]
    for k, (v, src) in enumerate(vals, 1):
        c = ws.cell(row=i, column=k, value=v if v != "" else None)
        c.number_format = "@"
        c.border = grid
        if src in FILL:
            c.fill = PatternFill("solid", fgColor=FILL[src])
            c.font = Font(color=INK[src], italic=(src == "prop"))
        if k > len(cols):
            c.fill = PatternFill("solid", fgColor="F3F6F7") if not c.fill.fgColor.rgb or c.fill.fgColor.rgb == "00000000" else c.fill
widths = {"Company Name": 40, "Addressee": 32, "Address 1": 36, "Address 2": 24, "Email": 32, "Legal Name": 32,
          "Comments": 30, "Flags": 70, "Question Categories": 26, "Bank Name": 28, "Default Expense Account": 30,
          "Default Payables Account": 30, "Ramp Vendor ID": 38}
for k, h in enumerate(headers, 1):
    ws.column_dimensions[get_column_letter(k)].width = widths.get(h, 16)
ws.row_dimensions[2].height = 30
ws.freeze_panes = "E3"
ws.auto_filter.ref = f"A2:{get_column_letter(len(headers))}{len(data['rows']) + 2}"

# Notes tab: the page's Open decisions and Notes, as rendered.
js = """
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[1]);
const t=await p.evaluate(()=>[...document.querySelectorAll('.decisions')].map(s=>({h:s.querySelector('h2').innerText,items:[...s.querySelectorAll('li')].map(l=>l.innerText)})));
console.log(JSON.stringify(t));await b.close()})()"""
notes = json.loads(subprocess.run(["node", "-e", js, os.path.abspath("data/vendor-review-full.html")],
                                  capture_output=True, text=True, check=True).stdout)
ns = wb.create_sheet("Notes")
ns.column_dimensions["A"].width = 5
ns.column_dimensions["B"].width = 120
ns["A1"] = "MinIO vendor load: notes"; ns["A1"].font = Font(bold=True, size=14)
in_ramp = sum(1 for r in data["rows"] if r["cells"][cols.index("In Ramp")][0] == "Yes")
ns["B2"] = (f"Full version for the controller and AP: tax IDs and bank details in full. Do not circulate further. "
            f"The Vendors tab lists every active Sage vendor ({len(data['rows']):,}); {in_ramp} are in Ramp and come into NetSuite "
            f"through the Ramp sync, {len(data['rows']) - in_ramp:,} are loaded from Sage. Columns marked * are required. "
            "Cell colors show where each value comes from:")
ns["B2"].alignment = Alignment(wrap_text=True)
row = 3
for label, key in (("From Sage", None), ("From Ramp", "ramp"), ("Set by rule", "rule"), ("Proposed", "prop"), ("Required, missing", "miss")):
    c = ns.cell(row=row, column=2, value=label)
    if key:
        c.fill = PatternFill("solid", fgColor=FILL[key]); c.font = Font(color=INK[key], italic=(key == "prop"))
    c.border = grid
    row += 1
row += 1
for sec in (x for x in notes if not (len(x["items"]) == 1 and x["items"][0].startswith("None"))):
    ns.cell(row=row, column=1, value=sec["h"]).font = Font(bold=True, size=12)
    row += 1
    for n, item in enumerate(sec["items"], 1):
        ns.cell(row=row, column=1, value=n).alignment = Alignment(vertical="top")
        ns.cell(row=row, column=2, value=item).alignment = Alignment(wrap_text=True, vertical="top")
        row += 1
    row += 1

wb.save(OUT)
print(f"{len(data['rows'])} rows, {len(headers)} columns -> {OUT} (tabs: {wb.sheetnames})")
